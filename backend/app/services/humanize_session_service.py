"""
HumanizeSessionService - 去痕迹会话数据持久化服务

负责:
1. 保存去痕迹会话数据 (核心数据 + 详情数据)
2. 计算 Token 消耗和成本
3. 更新用户画像统计
"""

from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from uuid import UUID
import logging

from app.models.humanize_session import HumanizeSession, HumanizeSessionDetail
from app.schemas.humanize import AIDetectionResult, HumanizeVerification
from app.services.user_profile_service import UserProfileService

logger = logging.getLogger(__name__)


class HumanizeSessionService:
    """去痕迹会话数据持久化服务"""

    # Token 价格 (示例,根据实际模型调整)
    # OpenAI GPT-4 Turbo 价格: $0.01 / 1K prompt tokens, $0.03 / 1K completion tokens
    PROMPT_TOKEN_PRICE = 0.00001  # $0.01 / 1000 tokens
    COMPLETION_TOKEN_PRICE = 0.00003  # $0.03 / 1000 tokens

    def __init__(self, db: AsyncSession):
        self.db = db
        self.profile_service = UserProfileService(db)

    async def save_session(
        self,
        user_id: UUID,
        ai_function: str,
        detection_result: AIDetectionResult,
        verification_result: HumanizeVerification,
        intensity: str,
        processing_time: float,
        original_text: str,
        humanized_text: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> HumanizeSession:
        """
        保存去痕迹会话数据

        Args:
            user_id: 用户ID
            ai_function: AI功能类型
            detection_result: 检测结果
            verification_result: 验证结果
            intensity: 强度
            processing_time: 处理耗时(秒)
            original_text: 原始文本
            humanized_text: 改写后文本
            prompt_tokens: Prompt消耗的token数
            completion_tokens: Completion消耗的token数

        Returns:
            HumanizeSession: 保存的会话对象
        """
        # 计算总 token 和成本
        total_tokens = prompt_tokens + completion_tokens
        cost = self._calculate_cost(prompt_tokens, completion_tokens)

        # 创建核心会话数据 (永久保存)
        session = HumanizeSession(
            user_id=user_id,
            ai_function=ai_function,
            score_before=verification_result.score_before,
            score_after=verification_result.score_after,
            improvement=verification_result.improvement,
            intensity=intensity,
            processing_time=processing_time,
            tokens_used=total_tokens,
            cost=cost
        )
        self.db.add(session)
        await self.db.flush()  # 获取 session.id

        # 创建详情数据 (30天后自动过期)
        detail = HumanizeSessionDetail(
            session_id=session.id,
            dimensions_before=self._serialize_dimensions(detection_result.dimensions),
            dimensions_after={},  # 验证结果没有维度详情,暂时为空
            detected_patterns=detection_result.detected_patterns,
            original_preview=original_text[:100] if original_text else None,
            humanized_preview=humanized_text[:100] if humanized_text else None,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        self.db.add(detail)

        # 更新用户画像
        await self.profile_service.update_profile_after_use(
            user_id=user_id,
            ai_function=ai_function,
            text_length=len(original_text),
            user_accepted=None  # 初始时未反馈
        )

        await self.db.commit()
        await self.db.refresh(session)

        logger.info(
            f"保存去痕迹会话: user_id={user_id}, ai_function={ai_function}, "
            f"improvement={verification_result.improvement:.1f}, "
            f"tokens={total_tokens}, cost=${cost:.4f}"
        )

        return session

    def _calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """
        计算成本

        Args:
            prompt_tokens: Prompt token数
            completion_tokens: Completion token数

        Returns:
            float: 成本 (美元)
        """
        prompt_cost = prompt_tokens * self.PROMPT_TOKEN_PRICE
        completion_cost = completion_tokens * self.COMPLETION_TOKEN_PRICE
        return prompt_cost + completion_cost

    def _serialize_dimensions(self, dimensions: Dict[str, Any]) -> Dict[str, Any]:
        """
        序列化维度数据为 JSON 可存储格式

        Args:
            dimensions: 维度字典

        Returns:
            Dict: 序列化后的维度数据
        """
        serialized = {}
        for key, value in dimensions.items():
            if hasattr(value, 'dict'):
                # Pydantic 模型
                serialized[key] = value.dict()
            elif isinstance(value, dict):
                serialized[key] = value
            else:
                serialized[key] = str(value)
        return serialized

    async def get_session(self, session_id: UUID) -> Optional[HumanizeSession]:
        """
        获取会话

        Args:
            session_id: 会话ID

        Returns:
            HumanizeSession 或 None
        """
        result = await self.db.execute(
            select(HumanizeSession).where(HumanizeSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def update_session_feedback(
        self,
        session_id: UUID,
        user_accepted: bool
    ) -> Optional[HumanizeSession]:
        """
        更新会话反馈

        Args:
            session_id: 会话ID
            user_accepted: 用户是否接受

        Returns:
            HumanizeSession 或 None
        """
        session = await self.get_session(session_id)
        if not session:
            return None

        session.user_accepted = user_accepted

        # 更新用户画像
        await self.profile_service.record_feedback(session.user_id, user_accepted)

        await self.db.commit()
        await self.db.refresh(session)

        logger.info(
            f"更新会话反馈: session_id={session_id}, accepted={user_accepted}"
        )

        return session

    def estimate_tokens(self, text: str) -> int:
        """
        估算文本的 token 数量 (简化版)

        实际应该使用 tiktoken 库,这里用简单估算

        Args:
            text: 文本

        Returns:
            int: 估算的 token 数
        """
        # 简化估算: 中文 1字 ≈ 1.5 tokens, 英文 1词 ≈ 1.3 tokens
        # 这里简单按字符数 / 2 估算
        return len(text) // 2

    async def estimate_cost(
        self,
        text: str,
        intensity: str = "medium"
    ) -> Dict[str, Any]:
        """
        估算去痕迹的成本

        Args:
            text: 待处理文本
            intensity: 强度

        Returns:
            Dict: 包含估算信息的字典
        """
        input_tokens = self.estimate_tokens(text)

        # 根据强度估算输出 token 数
        intensity_multiplier = {
            "light": 1.1,     # 轻度改写,输出略多于输入
            "medium": 1.3,    # 中度改写
            "strong": 1.5     # 强度改写
        }
        multiplier = intensity_multiplier.get(intensity, 1.3)
        output_tokens = int(input_tokens * multiplier)

        # 去痕迹需要3次调用: 检测 + 改写 + 验证
        # 检测: input + 少量输出
        detection_prompt_tokens = input_tokens + 500  # prompt overhead
        detection_completion_tokens = 500  # JSON 响应

        # 改写: input + 改写输出
        humanize_prompt_tokens = input_tokens + 800
        humanize_completion_tokens = output_tokens

        # 验证: 2倍 input + 少量输出
        verify_prompt_tokens = (input_tokens * 2) + 300
        verify_completion_tokens = 200

        total_prompt_tokens = (
            detection_prompt_tokens +
            humanize_prompt_tokens +
            verify_prompt_tokens
        )
        total_completion_tokens = (
            detection_completion_tokens +
            humanize_completion_tokens +
            verify_completion_tokens
        )

        total_cost = self._calculate_cost(total_prompt_tokens, total_completion_tokens)

        return {
            "input_tokens": input_tokens,
            "estimated_output_tokens": output_tokens,
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "total_tokens": total_prompt_tokens + total_completion_tokens,
            "estimated_cost": total_cost,
            "intensity": intensity
        }
