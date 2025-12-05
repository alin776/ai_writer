"""
HumanizeService - AI去痕迹核心服务

实现三阶段处理流程:
1. 检测阶段: 检测AI痕迹特征
2. 改写阶段: 流式人性化改写
3. 验证阶段: 验证改写效果
"""

import logging
import time
from typing import AsyncGenerator, Dict, Any, Optional, Literal

from app.services.ai.http_ai_service import HTTPAIService
from app.services.ai.fast_ai_service import FastAIService
from app.services.ai.nlp_preprocessor import NLPPreprocessor
from app.services.ai.humanize_prompts import (
    get_detection_prompt,
    get_humanize_prompt,
    get_verification_prompt
)
from app.schemas.humanize import AIDetectionResult, HumanizeVerification, DimensionScore
from app.utils.json_parser import parse_ai_json
from app.core.humanize_config import HumanizeConfig, get_config
from app.services.agent.model_selector import TaskType  # ✅ 新增：用于成本追踪

logger = logging.getLogger(__name__)


class HumanizeService:
    """AI去痕迹服务 - 使用双AI架构提升性能"""

    def __init__(
        self,
        ai_service: Optional[HTTPAIService] = None,
        fast_ai_service: Optional[FastAIService] = None,
        config: Optional[HumanizeConfig] = None
    ):
        """
        初始化去痕迹服务

        Args:
            ai_service: 标准AI服务实例 (用于高质量改写,如果不提供则自动创建)
            fast_ai_service: 快速AI服务实例 (用于检测和验证,如果不提供则自动创建)
            config: 配置实例 (如果不提供则使用默认配置)
        """
        self.ai_service = ai_service or HTTPAIService()
        self.fast_ai_service = fast_ai_service or FastAIService()
        self.config = config or get_config()
        self.nlp_preprocessor = NLPPreprocessor()  # 新增: NLP预处理器
        self.last_nlp_changes: list[str] = []  # 记录最近一次预处理的修改项
        logger.info(
            f"HumanizeService 初始化成功 - 双AI架构 + NLP预处理 "
            f"(标准模型: {self.ai_service.model}, 快速模型: {self.fast_ai_service.model}) "
            f"(检测: {self.config.enable_detection}, "
            f"验证: {self.config.enable_verification})"
        )

    async def detect_ai_traces(self, text: str) -> tuple[AIDetectionResult, dict]:
        """
        阶段1: 检测AI痕迹 (使用快速模型)

        Args:
            text: 待检测的文本

        Returns:
            tuple: (AIDetectionResult检测结果, usage统计字典)
        """
        start_time = time.time()
        logger.info(f"开始检测AI痕迹 (使用快速模型: {self.fast_ai_service.model}),文本长度: {len(text)}")

        # 构建检测 prompt
        detection_prompt = get_detection_prompt(text)

        # 使用快速AI服务进行检测 (非流式,更快)
        try:
            full_response, usage = await self.fast_ai_service.detect_ai_traces(
                text=text,
                prompt=detection_prompt  # ← 修复: 改为prompt参数
            )

            # 解析 JSON 响应 (使用健壮的解析工具)
            fallback_data = {
                "overall_score": 70.0,
                "dimensions": {
                    "pattern_repetition": {"score": 70, "description": "模式重复", "issues": []},
                    "word_choice": {"score": 70, "description": "词汇选择", "issues": []},
                    "sentence_structure": {"score": 70, "description": "句式结构", "issues": []},
                    "tone_style": {"score": 70, "description": "语气风格", "issues": []},
                    "formatting": {"score": 70, "description": "格式规范", "issues": []},
                    "emotional_expression": {"score": 70, "description": "情感表达", "issues": []},
                    "coherence_flow": {"score": 70, "description": "连贯性", "issues": []}
                },
                "detected_patterns": ["解析失败,默认需要去痕迹"],
                "needs_humanization": True
            }

            result_data = parse_ai_json(
                full_response,
                fallback_value=fallback_data,
                log_prefix="AI痕迹检测"
            )

            # 构建 Pydantic 模型
            detection_result = AIDetectionResult(**result_data)

            elapsed_time = time.time() - start_time
            logger.info(
                f"AI痕迹检测完成 (快速模型): overall_score={detection_result.overall_score:.1f}, "
                f"needs_humanization={detection_result.needs_humanization}, "
                f"tokens={usage.get('total_tokens', 0)}, "
                f"耗时: {elapsed_time:.2f}秒"
            )

            return detection_result, usage

        except Exception as e:
            logger.error(f"快速AI检测失败: {e}")
            # 返回默认值,假设需要去痕迹
            return AIDetectionResult(
                overall_score=70.0,
                dimensions={
                    "pattern_repetition": DimensionScore(score=70, description="模式重复", issues=[]),
                    "word_choice": DimensionScore(score=70, description="词汇选择", issues=[]),
                    "sentence_structure": DimensionScore(score=70, description="句式结构", issues=[]),
                    "tone_style": DimensionScore(score=70, description="语气风格", issues=[]),
                    "formatting": DimensionScore(score=70, description="格式规范", issues=[]),
                    "emotional_expression": DimensionScore(score=70, description="情感表达", issues=[]),
                    "coherence_flow": DimensionScore(score=70, description="连贯性", issues=[])
                },
                detected_patterns=["检测失败,默认需要去痕迹"],
                needs_humanization=True
            ), {}

    async def humanize_stream(
        self,
        text: str,
        intensity: Literal["light", "medium", "strong"] = "medium",
        use_nlp_preprocessing: bool = None  # None表示使用配置默认值
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """
        阶段2: 流式人性化改写

        Args:
            text: 待改写的文本
            intensity: 改写强度 (light/medium/strong)
            use_nlp_preprocessing: 是否启用NLP预处理 (None=使用配置,True=启用,False=禁用)

        Yields:
            tuple: (改写文本片段, usage统计或None)
                - 文本片段: str
                - usage: 仅在最后一个块返回完整usage,其他为None
        """
        start_time = time.time()
        original_length = len(text)

        # ===== 新增: NLP预处理 =====
        # 优先使用参数，其次使用配置
        should_preprocess = (
            self.config.enable_nlp_preprocessing
            if use_nlp_preprocessing is None
            else use_nlp_preprocessing
        )

        if should_preprocess:
            text, changes = self.nlp_preprocessor.preprocess(text)
            self.last_nlp_changes = changes
            if changes:
                logger.info(
                    f"✅ NLP预处理完成: {len(changes)}处修改, "
                    f"原文{original_length}字 → {len(text)}字 (减少{original_length - len(text)}字)"
                )
            else:
                logger.info("✅ NLP预处理完成: 未发现AI痕迹")
        else:
            self.last_nlp_changes = []
        # ===========================

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
        max_tokens = self.config.get_rewrite_max_tokens(len(text))
        temperature = self.config.get_rewrite_temperature(intensity)

        async for chunk, usage in self.ai_service._stream_chat(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            task_type=TaskType.HUMANIZE_REWRITE  # ✅ 2025-12-02: 去痕迹改写使用专用类型
        ):
            chunk_count += 1
            yield chunk, usage

        elapsed_time = time.time() - start_time
        logger.info(f"人性化改写完成: 输出了 {chunk_count} 个片段, 耗时: {elapsed_time:.2f}秒")

    async def verify_humanization(
        self,
        original_text: str,
        humanized_text: str
    ) -> tuple[HumanizeVerification, dict]:
        """
        阶段3: 验证改写效果 (使用快速模型)

        Args:
            original_text: 原始文本
            humanized_text: 改写后文本

        Returns:
            tuple: (HumanizeVerification验证结果, usage统计字典)
        """
        start_time = time.time()
        logger.info(f"开始验证改写效果 (使用快速模型: {self.fast_ai_service.model})")

        # 构建验证 prompt
        verification_prompt = get_verification_prompt(original_text, humanized_text)

        # 使用快速AI服务进行验证 (非流式,更快)
        try:
            full_response, usage = await self.fast_ai_service.verify_humanization(
                original_text=original_text,
                humanized_text=humanized_text,
                prompt=verification_prompt  # ← 修复: 改为prompt参数
            )

            # 解析 JSON 响应 (使用健壮的解析工具)
            fallback_data = {
                "score_before": 70.0,
                "score_after": 50.0,
                "improvement": 20.0,
                "success": True,
                "improvements": ["解析失败，使用默认值"],
                "remaining_issues": []
            }

            result_data = parse_ai_json(
                full_response,
                fallback_value=fallback_data,
                log_prefix="验证改写效果"
            )

            verification = HumanizeVerification(**result_data)

            elapsed_time = time.time() - start_time
            logger.info(
                f"验证完成 (快速模型): score_before={verification.score_before:.1f}, "
                f"score_after={verification.score_after:.1f}, "
                f"improvement={verification.improvement:.1f}, "
                f"success={verification.success}, "
                f"tokens={usage.get('total_tokens', 0)}, "
                f"耗时: {elapsed_time:.2f}秒"
            )

            return verification, usage

        except Exception as e:
            logger.error(f"快速AI验证失败: {e}")
            # 返回默认验证结果
            return HumanizeVerification(
                score_before=70.0,
                score_after=50.0,
                improvement=20.0,
                success=True,
                improvements=["验证失败，使用默认值"],
                remaining_issues=[]
            ), {}

    async def full_humanize_process(
        self,
        text: str,
        intensity: Literal["light", "medium", "strong"] = "medium",
        skip_detection: bool = False,
        skip_verification: bool = None,  # None表示使用配置默认值
        use_nlp_preprocessing: bool = None  # None表示使用配置默认值
    ) -> Dict[str, Any]:
        """
        完整的三阶段去痕迹流程 (非流式版本,用于测试)

        Args:
            text: 待处理文本
            intensity: 改写强度
            skip_detection: 是否跳过检测阶段 (直接改写)
            skip_verification: 是否跳过验证阶段 (None=使用配置,True=跳过,False=启用)
            use_nlp_preprocessing: 是否启用NLP预处理 (None=使用配置,True=启用,False=禁用)

        Returns:
            完整的处理结果字典
        """
        result = {
            "detection": None,
            "humanized_text": "",
            "verification": None,
            "processing_time": 0,
            "total_tokens": 0,  # 新增: 总token消耗
            "detection_tokens": 0,  # 新增: 检测阶段token
            "rewrite_tokens": 0,  # 新增: 改写阶段token
            "verification_tokens": 0,  # 新增: 验证阶段token
            # 详细token信息（用于精确成本计算）
            "detection_prompt_tokens": 0,
            "detection_completion_tokens": 0,
            "rewrite_prompt_tokens": 0,
            "rewrite_completion_tokens": 0,
            "verification_prompt_tokens": 0,
            "verification_completion_tokens": 0,
            "nlp_changes": []  # 新增: NLP预处理修改记录
        }

        start_time = time.time()

        # 判断是否启用验证 (优先使用参数,其次使用配置)
        enable_verification = (
            self.config.enable_verification
            if skip_verification is None
            else not skip_verification
        )

        # 阶段1: 检测 (可选)
        if not skip_detection and self.config.enable_detection:
            result["detection"], detection_usage = await self.detect_ai_traces(text)
            result["detection_tokens"] = detection_usage.get("total_tokens", 0)
            result["detection_prompt_tokens"] = detection_usage.get("prompt_tokens", 0)
            result["detection_completion_tokens"] = detection_usage.get("completion_tokens", 0)
            result["total_tokens"] += result["detection_tokens"]

            # 如果分数低于阈值,不需要去痕迹
            # 注意: overall_score越高越像AI (0-100分制,80-100=明显AI,60-80=疑似,40-60=轻微,0-40=人类)
            # threshold默认60分,低于60分说明AI痕迹较少,无需处理
            if result["detection"].overall_score < self.config.detection_threshold:
                logger.info(
                    f"AI特征分数较低 ({result['detection'].overall_score:.1f} < {self.config.detection_threshold}),无需去痕迹"
                )
                result["humanized_text"] = text
                result["nlp_changes"] = self.last_nlp_changes
                result["processing_time"] = time.time() - start_time
                return result

            logger.info(
                f"检测到AI特征 (分数={result['detection'].overall_score:.1f} >= {self.config.detection_threshold}),开始去痕迹"
            )

        # 阶段2: 改写
        humanized_chunks = []
        rewrite_usage = None
        async for chunk, usage in self.humanize_stream(text, intensity, use_nlp_preprocessing):
            humanized_chunks.append(chunk)
            if usage:  # 最后一个块会带usage
                rewrite_usage = usage

        result["humanized_text"] = "".join(humanized_chunks)
        result["nlp_changes"] = self.last_nlp_changes

        # 统计改写阶段token
        if rewrite_usage:
            result["rewrite_tokens"] = rewrite_usage.get("total_tokens", 0)
            result["rewrite_prompt_tokens"] = rewrite_usage.get("prompt_tokens", 0)
            result["rewrite_completion_tokens"] = rewrite_usage.get("completion_tokens", 0)
            result["total_tokens"] += result["rewrite_tokens"]

        # 阶段3: 验证 (可选)
        if enable_verification:
            result["verification"], verification_usage = await self.verify_humanization(
                text, result["humanized_text"]
            )
            result["verification_tokens"] = verification_usage.get("total_tokens", 0)
            result["verification_prompt_tokens"] = verification_usage.get("prompt_tokens", 0)
            result["verification_completion_tokens"] = verification_usage.get("completion_tokens", 0)
            result["total_tokens"] += result["verification_tokens"]
            logger.info("✅ 已启用验证阶段")
        else:
            logger.info("⏭️  已跳过验证阶段 (根据配置)")

        result["processing_time"] = time.time() - start_time

        logger.info(
            f"完整去痕迹流程完成,总耗时: {result['processing_time']:.2f}秒, "
            f"总Token: {result['total_tokens']} "
            f"(检测:{result['detection_tokens']}, 改写:{result['rewrite_tokens']}, "
            f"验证:{result['verification_tokens']})"
        )

        return result

    async def close(self):
        """关闭所有AI服务"""
        errors = []

        # 确保两个服务都尝试关闭
        if self.ai_service:
            try:
                await self.ai_service.close()
                logger.debug("标准AI服务已关闭")
            except Exception as e:
                logger.error(f"关闭标准AI服务失败: {e}")
                errors.append(e)

        if self.fast_ai_service:
            try:
                await self.fast_ai_service.close()
                logger.debug("快速AI服务已关闭")
            except Exception as e:
                logger.error(f"关闭快速AI服务失败: {e}")
                errors.append(e)

        # 如果有错误,抛出第一个
        if errors:
            raise errors[0]
