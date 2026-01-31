"""
段落级评审服务

功能:
- 快速4维度评审 (5秒内返回)
- 上下文理解
- 智能缓存
"""

from typing import Dict, Any, Optional
import json
import logging

from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.model_selector import TaskType  # ✅ 新增：用于成本追踪
from app.prompts.review_prompts import ReviewPromptTemplates
from app.core.cache import cache_review

logger = logging.getLogger(__name__)


class ParagraphReviewService:
    """段落评审服务"""

    def __init__(self, db: Optional[Any] = None, user_id: Optional[str] = None):
        """
        初始化段落评审服务

        Args:
            db: 数据库会话（用于成本追踪）
            user_id: 用户ID（用于成本追踪）
        """
        # ✅ 2025-12-02: 传递db和user_id以启用成本追踪
        self.ai_service = HTTPAIService(db=db, user_id=user_id)

    @cache_review(expire=3600, key_prefix="paragraph_review")  # 缓存1小时
    async def review_paragraph(
        self,
        text: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        评审段落

        Args:
            text: 段落文本 (50-2000字)
            context: 上下文信息 (可选)

        Returns:
            评审结果字典:
            {
                "overall_score": 85.5,
                "dimension_scores": {
                    "language": 88,
                    "vividness": 80,
                    "dialogue": 85,
                    "emotion": 90
                },
                "quick_feedback": "文字流畅,情感饱满",
                "suggestions": ["建议1", "建议2"]
            }
        """
        logger.info(f"[ParagraphReviewService] 开始评审段落, 长度={len(text)}")

        # 生成Prompt
        system_prompt, user_prompt = ReviewPromptTemplates.get_paragraph_review_prompt(
            content=text,
            context=context
        )

        # 调用AI
        logger.info("[ParagraphReviewService] 调用AI进行评审...")
        ai_response = await self.ai_service.call_ai(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=800,  # 段落级评审输出较少
            temperature=0.7,
            task_type=TaskType.TEXT_CLASSIFICATION  # ✅ 新增：段落评审是分类任务
        )

        logger.info(f"[ParagraphReviewService] AI响应长度: {len(ai_response)}")

        # 解析JSON
        result = self._extract_json_from_response(ai_response)

        logger.info(f"[ParagraphReviewService] 评审完成, 总分={result.get('overall_score', 0)}")

        return result

    def _extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """
        从AI响应中提取JSON

        Args:
            response: AI响应文本

        Returns:
            解析后的字典
        """
        try:
            # 尝试直接解析
            return json.loads(response)
        except json.JSONDecodeError:
            # 如果有markdown标记,尝试提取
            response = response.strip()

            # 移除markdown代码块标记
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]

            if response.endswith("```"):
                response = response[:-3]

            response = response.strip()

            try:
                return json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {e}")
                logger.error(f"原始响应: {response[:500]}")

                # 返回默认结构
                return {
                    "overall_score": 0,
                    "dimension_scores": {
                        "language": 0,
                        "vividness": 0,
                        "dialogue": 0,
                        "emotion": 0
                    },
                    "quick_feedback": "解析失败",
                    "suggestions": []
                }
