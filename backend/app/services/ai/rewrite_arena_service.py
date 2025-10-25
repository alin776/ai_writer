"""
改写对战服务

支持多模型并发改写，对比不同模型的改写效果
"""

import httpx
import asyncio
import time
import logging
from typing import List, Optional, Dict

from app.core.config import settings
from app.schemas.text_analysis import (
    RewriteMode,
    ModelResult
)

logger = logging.getLogger(__name__)


class RewriteArenaService:
    """改写对战服务 - 支持多模型并发改写"""

    def __init__(self):
        """初始化服务"""
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = settings.OPENAI_BASE_URL
        self.default_model = settings.OPENAI_MODEL

        # 创建 HTTP 客户端
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(60.0, connect=10.0),
            follow_redirects=True,
            http2=False,
        )

        logger.info("RewriteArenaService 初始化成功")

    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()

    def _build_rewrite_prompt(
        self,
        text: str,
        mode: RewriteMode,
        custom_requirement: Optional[str] = None,
        context_before: Optional[str] = None,
        context_after: Optional[str] = None
    ) -> str:
        """
        构建改写提示词

        Args:
            text: 待改写的文本
            mode: 改写模式
            custom_requirement: 自定义要求
            context_before: 前文上下文
            context_after: 后文上下文

        Returns:
            str: 完整的提示词
        """
        # 模式说明
        mode_instructions = {
            RewriteMode.OPTIMIZE: "优化提升：让文字更优美、更生动、更有感染力，提升整体表达质量",
            RewriteMode.EXPAND: "扩写丰富：增加细节描写、情感渲染和画面感，让内容更丰富生动",
            RewriteMode.COMPRESS: "精简压缩：保留核心信息和关键内容，删除冗余和重复，使表达更简洁",
            RewriteMode.CUSTOM: f"自定义要求：{custom_requirement}" if custom_requirement else "按照用户要求改写"
        }

        mode_instruction = mode_instructions.get(mode, mode_instructions[RewriteMode.OPTIMIZE])

        # 构建上下文部分
        context_info = ""
        if context_before or context_after:
            context_info = "\n【上下文参考】\n"
            if context_before:
                context_info += f"前文：{context_before}\n"
            if context_after:
                context_info += f"后文：{context_after}\n"
            context_info += "\n请注意保持与上下文的连贯性和风格统一。\n"

        # 构建完整提示词
        prompt = f"""你是一位专业的小说改写助手，擅长提升文本质量。

【改写模式】
{mode_instruction}

【待改写文本】
{text}
{context_info}

【改写要求】
1. 保持原文的核心意思和情节发展
2. 根据改写模式的要求进行优化
3. 保持自然流畅，避免生硬
4. 保持原文的叙述视角和人称
5. 直接输出改写后的文本，不要添加任何说明或标记

请开始改写：
"""
        return prompt

    async def rewrite_with_model(
        self,
        model_name: str,
        text: str,
        mode: RewriteMode,
        custom_requirement: Optional[str] = None,
        context_before: Optional[str] = None,
        context_after: Optional[str] = None
    ) -> ModelResult:
        """
        使用单个模型进行改写

        Args:
            model_name: 模型名称
            text: 待改写的文本
            mode: 改写模式
            custom_requirement: 自定义要求
            context_before: 前文上下文
            context_after: 后文上下文

        Returns:
            ModelResult: 改写结果
        """
        start_time = time.time()

        try:
            prompt = self._build_rewrite_prompt(
                text, mode, custom_requirement,
                context_before, context_after
            )

            messages = [
                {
                    "role": "system",
                    "content": "你是一位专业的小说改写助手，擅长根据要求改写文本。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            logger.info(f"开始使用 {model_name} 改写文本")

            # 调用 API
            rewritten_text = await self._call_api(
                messages,
                model=model_name,
                temperature=0.7,
                max_tokens=2000
            )

            elapsed_time = time.time() - start_time
            word_count = len(rewritten_text)

            logger.info(
                f"{model_name} 改写完成，耗时: {elapsed_time:.2f}s, "
                f"字数: {word_count}"
            )

            return ModelResult(
                model_name=model_name,
                rewritten_text=rewritten_text,
                word_count=word_count,
                elapsed_time=round(elapsed_time, 2),
                error=None
            )

        except Exception as e:
            elapsed_time = time.time() - start_time
            error_msg = f"{type(e).__name__}: {str(e)}"

            logger.error(f"{model_name} 改写失败: {error_msg}")

            return ModelResult(
                model_name=model_name,
                rewritten_text="",
                word_count=0,
                elapsed_time=round(elapsed_time, 2),
                error=error_msg
            )

    async def rewrite_with_multiple_models(
        self,
        model_names: List[str],
        text: str,
        mode: RewriteMode,
        custom_requirement: Optional[str] = None,
        context_before: Optional[str] = None,
        context_after: Optional[str] = None
    ) -> List[ModelResult]:
        """
        使用多个模型并发改写

        Args:
            model_names: 模型名称列表
            text: 待改写的文本
            mode: 改写模式
            custom_requirement: 自定义要求
            context_before: 前文上下文
            context_after: 后文上下文

        Returns:
            List[ModelResult]: 各模型的改写结果
        """
        logger.info(f"开始多模型改写，模型数量: {len(model_names)}")

        # 创建所有任务
        tasks = [
            self.rewrite_with_model(
                model_name,
                text,
                mode,
                custom_requirement,
                context_before,
                context_after
            )
            for model_name in model_names
        ]

        # 并发执行所有任务
        results = await asyncio.gather(*tasks, return_exceptions=False)

        logger.info(f"多模型改写完成，成功: {sum(1 for r in results if not r.error)}/{len(results)}")

        return results

    async def _call_api(
        self,
        messages: list,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        调用 AI API 获取完整响应

        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数

        Returns:
            str: API 响应的完整文本

        Raises:
            Exception: API 调用失败
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            response = await self.client.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                error_text = response.text[:500]
                logger.error(f"API 错误 ({model}): {response.status_code}, {error_text}")
                raise Exception(f"API 请求失败: {response.status_code}")

            data = response.json()

            # 提取内容
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content.strip()
            else:
                raise Exception("API 响应格式错误")

        except httpx.HTTPError as e:
            logger.error(f"HTTP 请求错误 ({model}): {type(e).__name__}: {str(e)}")
            raise Exception(f"网络请求失败: {str(e)}")


# 全局服务实例
_arena_service: Optional[RewriteArenaService] = None


def get_arena_service() -> RewriteArenaService:
    """获取改写对战服务单例"""
    global _arena_service
    if _arena_service is None:
        _arena_service = RewriteArenaService()
    return _arena_service


async def close_arena_service():
    """关闭改写对战服务"""
    global _arena_service
    if _arena_service is not None:
        await _arena_service.close()
        _arena_service = None
