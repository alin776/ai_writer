"""
Fast AI Service - 使用 gemini-2.5-flash-lite 快速模型

专门用于AI去痕迹功能的检测和验证阶段，这些阶段不需要高质量的生成能力，
使用快速模型可以大幅降低响应时间和成本。

性能优势:
- 响应速度: ~3-5秒 (vs gpt-4的15-30秒)
- 成本: ~1/10 (vs gpt-4)
- 适用场景: 检测、验证、分类等不需要复杂生成的任务
"""

import httpx
import json
import logging
from typing import AsyncGenerator, Optional
from datetime import datetime
from app.core.config import settings
from app.core.request_context import get_request_user_id  # ✅ 新增：用于成本追踪
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class FastAIService:
    """基于 gemini-2.5-flash-lite 的快速 AI 服务

    专门用于需要快速响应但不需要高质量生成的场景：
    - AI痕迹检测
    - 改写效果验证
    - 文本分类
    """

    def __init__(self, timeout: int = 60, db=None):
        """初始化快速AI服务

        Args:
            timeout: 超时时间(秒)，默认60秒（gemini-2.5-flash-lite响应较慢）
            db: 可选的外层数据库会话（用于事务原子性）
        """
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = settings.OPENAI_BASE_URL
        self.model = "gemini-2.5-flash-lite"  # 固定使用快速模型
        self.timeout = timeout
        self.db = db  # ✅ 2025-12-14: 支持外层事务控制

        # 创建HTTP客户端
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(
                timeout,
                connect=5.0  # 连接超时5秒
            ),
            follow_redirects=True,
            http2=False,
        )

        print(f"[FastAI] Init OK - Model: {self.model}, Timeout: {timeout}s")
        logger.info(
            f"[FastAI] Init OK - Model: {self.model}, Timeout: {timeout}s"
        )

    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()
        logger.debug("Fast AI Service 已关闭")

    async def _track_cost(
        self,
        usage: dict,
        operation_type: str,
        start_time: datetime
    ):
        """
        追踪API调用成本并扣除积分（使用request context）

        Args:
            usage: usage统计信息（包含prompt_tokens, completion_tokens）
            operation_type: 操作类型
            start_time: 调用开始时间
        """
        from contextlib import asynccontextmanager

        user_id = get_request_user_id()

        if not user_id:
            logger.debug("[FastAI成本追踪] 跳过：缺少user_id")
            return

        try:
            from app.utils.cost_calculator import CostCalculator
            from app.schemas.ai_call_log import AICallLogCreate
            from app.core.database import create_db_session
            from app.services.ai_log_service import AILogService
            from uuid import UUID

            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)

            # 计算成本
            cost_data = CostCalculator.calculate_cost(
                model_name=self.model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )

            # 计算响应时间
            duration_ms = int((get_utc_now() - start_time).total_seconds() * 1000)

            # 创建日志记录
            log_data = AICallLogCreate(
                user_id=UUID(user_id),
                model_name=self.model,
                operation_type=operation_type,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
                prompt_cost=cost_data["prompt_cost"],
                completion_cost=cost_data["completion_cost"],
                total_cost=cost_data["total_cost"],
                duration_ms=duration_ms,
                is_success=True,
                extra_data={}
            )

            # ✅ 2025-12-14: 支持外层事务控制（与HTTPAIService一致）
            @asynccontextmanager
            async def get_db_session():
                """获取数据库会话：优先使用外层会话，否则创建独立会话"""
                if self.db is not None:
                    logger.debug("[FastAI成本追踪] 使用外层数据库会话（事务原子性模式）")
                    yield self.db, False  # 不自动提交
                else:
                    logger.debug("[FastAI成本追踪] 使用独立数据库会话")
                    async with create_db_session() as new_db:
                        yield new_db, True  # 自动提交

            async with get_db_session() as (db, should_auto_commit):
                temp_log_service = AILogService(db)
                ai_call_log = await temp_log_service.create_log(log_data, auto_commit=should_auto_commit)

                # ==================== 积分扣费 ====================
                # ✅ 2025-12-08: 添加积分扣费逻辑（与HTTPAIService一致）
                try:
                    from app.services.credits.credit_service import CreditService
                    from app.services.credits.credit_utils import calculate_credits_from_cost
                    from app.services.credits.credit_exceptions import (
                        InsufficientCreditsError,
                        CreditsExpiredError
                    )
                    from app.models.user import User
                    from sqlalchemy import select

                    # 查询用户信息
                    user_stmt = select(User).where(User.id == UUID(user_id))
                    user_result = await db.execute(user_stmt)
                    user = user_result.scalar_one_or_none()

                    if user:
                        credit_service = CreditService(db)

                        # 计算需要扣除的积分
                        credits_to_deduct = calculate_credits_from_cost(cost_data["total_cost"])

                        # 扣除积分（管理员自动豁免）
                        # ✅ 2025-12-14: 传递 auto_commit 参数
                        transaction = await credit_service.consume(
                            user_id=UUID(user_id),
                            amount=credits_to_deduct,
                            description=f"FastAI调用: {operation_type}",
                            related_id=ai_call_log.id,
                            skip_check=user.is_admin,  # 管理员豁免
                            auto_commit=should_auto_commit  # ✅ 由外层事务控制提交
                        )

                        if transaction:  # 非管理员才有交易记录
                            logger.info(
                                f"[FastAI积分扣费] 用户 {user_id}: 扣除 {float(credits_to_deduct)} 积分, "
                                f"余额: {float(transaction.balance_before)} → {float(transaction.balance_after)}"
                            )
                        else:
                            logger.info(f"[FastAI积分扣费] 管理员 {user_id} 豁免积分扣费")
                    else:
                        logger.warning(f"[FastAI积分扣费] 用户 {user_id} 不存在，跳过扣费")

                except InsufficientCreditsError as e:
                    logger.error(
                        f"[FastAI积分扣费] 用户 {user_id} 余额不足: "
                        f"需要 {float(e.required)} 积分，当前 {float(e.available)} 积分"
                    )
                    # FastAI 是非流式调用，已完成，不抛异常中断
                    # 但记录警告，后续可考虑预检查
                except CreditsExpiredError as e:
                    logger.error(f"[FastAI积分扣费] 用户 {user_id} 积分已过期: {e.expired_at}")
                except Exception as e:
                    logger.error(f"[FastAI积分扣费] 扣费失败: {type(e).__name__}: {str(e)}")
                # ================================================

            logger.info(
                f"[FastAI成本追踪] 已记录: operation={operation_type}, "
                f"tokens={prompt_tokens + completion_tokens}, "
                f"cost=${cost_data['total_cost']:.6f}"
            )

        except Exception as e:
            logger.error(f"[FastAI成本追踪] 失败: {e}")
            # 成本追踪失败不应影响主流程

    async def chat_completion(
        self,
        messages: list,
        max_tokens: int = 1500,
        temperature: float = 0.3,
        operation_type: str = "fast_ai_call"  # ✅ 新增：用于成本追踪
    ) -> tuple[str, dict]:
        """
        非流式聊天完成（用于检测和验证）

        Args:
            messages: 消息列表
            max_tokens: 最大token数
            temperature: 温度参数（默认0.3，保证稳定性）

        Returns:
            tuple: (完整的AI响应文本, usage统计字典)
                usage包含: prompt_tokens, completion_tokens, total_tokens

        Raises:
            Exception: API调用失败时抛出异常
        """
        # ==================== 积分预检查 ====================
        # ✅ 2025-12-08: 添加预检查，与HTTPAIService一致
        user_id = get_request_user_id()
        if user_id:
            try:
                from app.core.database import create_db_session
                from app.services.credits.credit_service import CreditService
                from app.models.user import User
                from app.utils.cost_calculator import CostCalculator
                from app.core.config import settings
                from sqlalchemy import select
                from uuid import UUID

                async with create_db_session() as db:
                    # 查询用户信息
                    user_stmt = select(User).where(User.id == UUID(user_id))
                    user_result = await db.execute(user_stmt)
                    user = user_result.scalar_one_or_none()

                    if user and not user.is_admin:
                        # 非管理员需要检查余额
                        credit_service = CreditService(db)

                        # 粗略估算需要的积分（基于max_tokens）
                        estimated_cost_data = CostCalculator.calculate_cost(
                            model_name=self.model,
                            prompt_tokens=len(str(messages)) // 4,  # 粗略估算
                            completion_tokens=max_tokens  # 使用最大值
                        )
                        estimated_credits = estimated_cost_data["total_cost"] * settings.CREDITS_PER_DOLLAR

                        # 检查余额是否充足
                        is_sufficient, current_balance = await credit_service.check_sufficient(
                            user_id=UUID(user_id),
                            required_credits=estimated_credits
                        )

                        if not is_sufficient:
                            logger.warning(
                                f"[FastAI积分检查] 用户 {user_id} 余额不足: "
                                f"需要约 {float(estimated_credits):.2f} 积分，当前 {float(current_balance):.2f} 积分"
                            )
                            raise Exception(
                                f"积分余额不足：当前余额 {float(current_balance):.2f}，"
                                f"预计需要 {float(estimated_credits):.2f} 积分。请先充值。"
                            )

                        logger.debug(
                            f"[FastAI积分检查] 用户 {user_id} 余额充足: "
                            f"当前 {float(current_balance):.2f} 积分"
                        )

            except Exception as e:
                # 如果是余额不足异常，直接传递
                if "积分余额不足" in str(e):
                    raise
                # 其他检查失败不影响调用（降级处理）
                logger.warning(f"[FastAI积分检查] 检查失败，继续调用: {e}")
        # ====================================================

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False  # 非流式
        }

        logger.debug(
            f"调用快速AI: model={self.model}, "
            f"max_tokens={max_tokens}, temp={temperature}"
        )

        # ✅ 记录开始时间（用于成本追踪）
        start_time = get_utc_now()

        try:
            response = await self.client.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                error_text = response.text[:500]
                logger.error(f"快速AI API错误: {response.status_code}, {error_text}")
                raise Exception(f"API错误: {response.status_code}")

            data = response.json()
            content = data["choices"][0]["message"]["content"]

            # 统计token使用情况
            usage = data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)

            logger.info(
                f"快速AI响应成功: tokens={total_tokens} "
                f"(prompt={prompt_tokens}, completion={completion_tokens})"
            )

            # 返回内容和usage统计
            usage_stats = {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            }

            # ✅ 追踪成本
            await self._track_cost(
                usage=usage_stats,
                operation_type=operation_type,
                start_time=start_time
            )

            return content, usage_stats

        except httpx.TimeoutException:
            logger.error(f"快速AI调用超时 (>{self.timeout}秒)")
            raise Exception(f"API超时 (>{self.timeout}秒)")
        except httpx.RequestError as e:
            logger.error(f"快速AI网络错误: {e}")
            raise Exception(f"网络错误: {e}")
        except KeyError as e:
            logger.error(f"快速AI响应格式错误: {e}")
            raise Exception(f"响应格式错误: {e}")
        except Exception as e:
            logger.error(f"快速AI调用失败: {type(e).__name__}: {e}")
            raise

    async def stream_chat_completion(
        self,
        messages: list,
        max_tokens: int = 1500,
        temperature: float = 0.3
    ) -> AsyncGenerator[str, None]:
        """
        流式聊天完成（一般不用于检测/验证，但保留接口）

        Args:
            messages: 消息列表
            max_tokens: 最大token数
            temperature: 温度参数

        Yields:
            str: 流式响应的文本片段
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }

        logger.debug(
            f"开始流式快速AI调用: model={self.model}, "
            f"max_tokens={max_tokens}, temp={temperature}"
        )

        try:
            async with self.client.stream("POST", url, json=payload, headers=headers) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    error_msg = error_text.decode('utf-8', errors='ignore')[:500]
                    logger.error(f"快速AI流式错误: {response.status_code}, {error_msg}")
                    raise Exception(f"API错误: {response.status_code}")

                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue

                    data_str = line[6:]  # 移除 "data: " 前缀

                    if data_str == "[DONE]":
                        break

                    try:
                        data = json.loads(data_str)
                        delta = data["choices"][0]["delta"]

                        if "content" in delta:
                            yield delta["content"]

                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue

                logger.debug("快速AI流式响应完成")

        except httpx.TimeoutException:
            logger.error(f"快速AI流式调用超时 (>{self.timeout}秒)")
            raise Exception(f"API超时 (>{self.timeout}秒)")
        except httpx.RequestError as e:
            logger.error(f"快速AI流式网络错误: {e}")
            raise Exception(f"网络错误: {e}")
        except Exception as e:
            logger.error(f"快速AI流式调用失败: {type(e).__name__}: {e}")
            raise

    async def detect_ai_traces(self, text: str, prompt: str) -> tuple[str, dict]:
        """
        AI痕迹检测（便捷方法）

        Args:
            text: 待检测文本（仅用于日志）
            prompt: 完整的检测prompt（已经format好的，不是模板）

        Returns:
            tuple: (检测结果的JSON字符串, usage统计字典)
        """
        messages = [
            {
                "role": "system",
                "content": "你是一位专业的AI文本检测专家,请严格按照JSON格式返回检测结果。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        logger.info(f"开始快速AI痕迹检测: 文本长度={len(text)}")

        result, usage = await self.chat_completion(
            messages=messages,
            max_tokens=1500,
            temperature=0.3,  # 低温度保证稳定
            operation_type="humanize_detect"  # ✅ 对应TaskType.HUMANIZE_DETECT
        )

        return result, usage

    async def verify_humanization(
        self,
        original_text: str,
        humanized_text: str,
        prompt: str
    ) -> tuple[str, dict]:
        """
        去痕迹效果验证（便捷方法）

        Args:
            original_text: 原始文本（仅用于日志）
            humanized_text: 改写后文本（仅用于日志）
            prompt: 完整的验证prompt（已经format好的，不是模板）

        Returns:
            tuple: (验证结果的JSON字符串, usage统计字典)
        """
        messages = [
            {
                "role": "system",
                "content": "你是一位AI文本检测专家,请严格按照JSON格式返回验证结果。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        logger.info(
            f"开始快速AI效果验证: 原文={len(original_text)}字, "
            f"改写后={len(humanized_text)}字"
        )

        result, usage = await self.chat_completion(
            messages=messages,
            max_tokens=500,  # 验证结果通常较短
            temperature=0.3,
            operation_type="humanize_verify"  # ✅ 对应TaskType.HUMANIZE_VERIFY
        )

        return result, usage


# 便捷的单例访问（可选）
_fast_ai_service_instance: Optional[FastAIService] = None


def get_fast_ai_service() -> FastAIService:
    """
    获取FastAIService单例

    注意: 这是一个全局单例，适合在无并发配置需求的场景使用。
    如果需要自定义超时等参数，请直接实例化FastAIService。

    Returns:
        FastAIService实例
    """
    global _fast_ai_service_instance

    if _fast_ai_service_instance is None:
        _fast_ai_service_instance = FastAIService()

    return _fast_ai_service_instance


async def close_fast_ai_service():
    """关闭全局FastAIService单例"""
    global _fast_ai_service_instance

    if _fast_ai_service_instance is not None:
        await _fast_ai_service_instance.close()
        _fast_ai_service_instance = None
        logger.info("全局Fast AI Service已关闭")
