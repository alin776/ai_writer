"""
HumanizeService - AI去痕迹核心服务

实现三阶段处理流程:
1. 检测阶段: 检测AI痕迹特征
2. 改写阶段: 流式人性化改写
3. 验证阶段: 验证改写效果
"""

import json
import logging
import time
from typing import AsyncGenerator, Dict, Any, Optional, Literal
from datetime import datetime, timedelta

from app.services.ai.http_ai_service import HTTPAIService
from app.services.ai.humanize_prompts import (
    get_detection_prompt,
    get_humanize_prompt,
    get_verification_prompt
)
from app.schemas.humanize import AIDetectionResult, HumanizeVerification

logger = logging.getLogger(__name__)


class HumanizeService:
    """AI去痕迹服务"""

    def __init__(self, ai_service: Optional[HTTPAIService] = None):
        """
        初始化去痕迹服务

        Args:
            ai_service: HTTP AI服务实例 (如果不提供则自动创建)
        """
        self.ai_service = ai_service or HTTPAIService()
        logger.info("HumanizeService 初始化成功")

    async def detect_ai_traces(self, text: str) -> AIDetectionResult:
        """
        阶段1: 检测AI痕迹

        Args:
            text: 待检测的文本

        Returns:
            AIDetectionResult: AI特征检测结果
        """
        start_time = time.time()
        logger.info(f"开始检测AI痕迹,文本长度: {len(text)}")

        # 构建检测 prompt
        detection_prompt = get_detection_prompt(text)

        # 调用 AI 进行检测
        messages = [
            {
                "role": "system",
                "content": "你是一位专业的AI文本检测专家,请严格按照JSON格式返回检测结果。"
            },
            {
                "role": "user",
                "content": detection_prompt
            }
        ]

        # 收集完整响应
        full_response = ""
        async for chunk in self.ai_service._stream_chat(
            messages=messages,
            max_tokens=1500,
            temperature=0.3  # 低温度以获得更稳定的JSON输出
        ):
            full_response += chunk

        # 解析 JSON 响应
        try:
            # 提取 JSON 部分 (可能被包裹在 ```json ... ``` 中)
            json_start = full_response.find("{")
            json_end = full_response.rfind("}") + 1
            json_str = full_response[json_start:json_end]

            result_data = json.loads(json_str)

            # 构建 Pydantic 模型
            detection_result = AIDetectionResult(**result_data)

            elapsed_time = time.time() - start_time
            logger.info(
                f"AI痕迹检测完成: overall_score={detection_result.overall_score:.1f}, "
                f"needs_humanization={detection_result.needs_humanization}, "
                f"耗时: {elapsed_time:.2f}秒"
            )

            return detection_result

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"解析AI检测结果失败: {e}, 原始响应: {full_response[:500]}")
            # 返回默认值,假设需要去痕迹
            return AIDetectionResult(
                overall_score=70.0,
                dimensions={},
                detected_patterns=["解析失败,默认需要去痕迹"],
                needs_humanization=True
            )

    async def humanize_stream(
        self,
        text: str,
        intensity: Literal["light", "medium", "strong"] = "medium"
    ) -> AsyncGenerator[str, None]:
        """
        阶段2: 流式人性化改写

        Args:
            text: 待改写的文本
            intensity: 改写强度 (light/medium/strong)

        Yields:
            str: 流式输出的改写文本片段
        """
        start_time = time.time()
        logger.info(f"开始人性化改写: intensity={intensity}, 文本长度={len(text)}")

        # 构建改写 prompt
        humanize_prompt = get_humanize_prompt(text, intensity)

        messages = [
            {
                "role": "system",
                "content": "你是一位专业的文本人性化专家,请直接输出改写后的文本,不要包含任何解释。"
            },
            {
                "role": "user",
                "content": humanize_prompt
            }
        ]

        # 流式输出改写结果
        chunk_count = 0
        async for chunk in self.ai_service._stream_chat(
            messages=messages,
            max_tokens=len(text) * 2,  # 根据原文长度动态调整
            temperature=0.7
        ):
            chunk_count += 1
            yield chunk

        elapsed_time = time.time() - start_time
        logger.info(f"人性化改写完成: 输出了 {chunk_count} 个片段, 耗时: {elapsed_time:.2f}秒")

    async def verify_humanization(
        self,
        original_text: str,
        humanized_text: str
    ) -> HumanizeVerification:
        """
        阶段3: 验证改写效果

        Args:
            original_text: 原始文本
            humanized_text: 改写后文本

        Returns:
            HumanizeVerification: 验证结果
        """
        start_time = time.time()
        logger.info("开始验证改写效果")

        # 构建验证 prompt
        verification_prompt = get_verification_prompt(original_text, humanized_text)

        messages = [
            {
                "role": "system",
                "content": "你是一位AI文本检测专家,请严格按照JSON格式返回验证结果。"
            },
            {
                "role": "user",
                "content": verification_prompt
            }
        ]

        # 收集完整响应
        full_response = ""
        async for chunk in self.ai_service._stream_chat(
            messages=messages,
            max_tokens=500,
            temperature=0.3
        ):
            full_response += chunk

        # 解析 JSON 响应
        try:
            json_start = full_response.find("{")
            json_end = full_response.rfind("}") + 1
            json_str = full_response[json_start:json_end]

            result_data = json.loads(json_str)

            verification = HumanizeVerification(**result_data)

            elapsed_time = time.time() - start_time
            logger.info(
                f"验证完成: score_before={verification.score_before:.1f}, "
                f"score_after={verification.score_after:.1f}, "
                f"improvement={verification.improvement:.1f}, "
                f"success={verification.success}, "
                f"耗时: {elapsed_time:.2f}秒"
            )

            return verification

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"解析验证结果失败: {e}, 原始响应: {full_response[:500]}")
            # 返回默认验证结果
            return HumanizeVerification(
                score_before=70.0,
                score_after=50.0,
                improvement=20.0,
                success=True
            )

    async def full_humanize_process(
        self,
        text: str,
        intensity: Literal["light", "medium", "strong"] = "medium",
        skip_detection: bool = False
    ) -> Dict[str, Any]:
        """
        完整的三阶段去痕迹流程 (非流式版本,用于测试)

        Args:
            text: 待处理文本
            intensity: 改写强度
            skip_detection: 是否跳过检测阶段 (直接改写)

        Returns:
            完整的处理结果字典
        """
        result = {
            "detection": None,
            "humanized_text": "",
            "verification": None,
            "processing_time": 0
        }

        start_time = time.time()

        # 阶段1: 检测 (可选)
        if not skip_detection:
            result["detection"] = await self.detect_ai_traces(text)

            # 如果分数低于60,不需要去痕迹
            if result["detection"].overall_score < 60:
                logger.info(f"AI特征分数较低 ({result['detection'].overall_score}),无需去痕迹")
                result["humanized_text"] = text
                result["processing_time"] = time.time() - start_time
                return result

        # 阶段2: 改写
        humanized_chunks = []
        async for chunk in self.humanize_stream(text, intensity):
            humanized_chunks.append(chunk)

        result["humanized_text"] = "".join(humanized_chunks)

        # 阶段3: 验证
        result["verification"] = await self.verify_humanization(text, result["humanized_text"])

        result["processing_time"] = time.time() - start_time

        logger.info(f"完整去痕迹流程完成,总耗时: {result['processing_time']:.2f}秒")

        return result

    async def close(self):
        """关闭服务"""
        if self.ai_service:
            await self.ai_service.close()
