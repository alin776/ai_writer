"""角色守护 Agent

负责检查内容中角色表现的一致性。
"""

from typing import Dict, Any, List
from app.services.agent.model_selector import TaskType
from .base_agent import BaseAgent
from ..prompts import CHARACTER_GUARD_PROMPT
from ..character_extractor import (
    extract_characters_from_text,
    check_character_presence
)

import logging

logger = logging.getLogger(__name__)


class CharacterGuard(BaseAgent):
    """角色守护 Agent

    职责：
    - 检查角色性格一致性
    - 检查对话风格一致性
    - 检查角色行为合理性
    - 识别人设崩塌问题
    - ✅ P2增强：无角色设定时从前文提取角色进行检查
    - ✅ 重构：使用公共模块 character_extractor 进行角色提取
    """

    @property
    def name(self) -> str:
        return "角色守护"

    @property
    def role_description(self) -> str:
        return "负责检查角色一致性，防止人设崩塌"

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行角色检查

        Args:
            input_data: 初稿内容
            context: 上下文信息

        Returns:
            检查结果
        """
        return await self.check(input_data, context.get("work_id", ""), context)

    async def check(
        self,
        draft: Dict[str, Any],
        work_id: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """检查角色一致性

        Args:
            draft: 初稿（包含 content）
            work_id: 作品 ID
            context: 上下文（character_document, analysis_result, previous_summary）

        Returns:
            检查结果，包含 status 和 issues
        """
        self._log_execution("开始角色一致性检查")

        content = draft.get("content", "")
        character_doc = context.get("character_document", "")

        # ✅ P2增强：即使没有角色文档，也尝试从分析结果中提取角色进行检查
        if not character_doc:
            # 尝试从分析结果中提取角色
            analysis = context.get("analysis_result", "") or context.get("previous_summary", "")

            if analysis:
                # ✅ 重构：使用公共模块提取角色（基于特征过滤）
                extracted_chars = extract_characters_from_text(analysis, max_count=10)

                if extracted_chars:
                    self._log_execution(f"无角色文档，从分析中提取{len(extracted_chars)}个角色进行检查")

                    # ✅ 重构：使用公共模块检查角色出现情况
                    presence_check = check_character_presence(content, extracted_chars)

                    # 如果匹配率过低，说明内容可能跑题
                    if presence_check["is_off_topic"]:
                        self._log_execution(
                            "内容跑题警告",
                            {"found": presence_check["found"], "missing": presence_check["missing"]}
                        )
                        return {
                            "status": "NEED_REVISION",
                            "issues": [
                                {
                                    "type": "content_drift",
                                    "severity": "high",
                                    "description": f"新章节与前文角色严重不匹配，前文角色: {extracted_chars[:5]}，"
                                                   f"新章节中仅出现: {presence_check['found']}",
                                    "suggestion": "请确保新章节延续前文的角色和故事线"
                                }
                            ],
                            "summary": f"内容跑题警告：前文主要角色 {extracted_chars[:5]} 在新章节中几乎未出现",
                            "extracted_characters": extracted_chars,
                            "presence_check": presence_check
                        }
                    else:
                        return {
                            "status": "PASS",
                            "issues": [],
                            "summary": f"角色匹配检查通过（{presence_check['match_count']}/{presence_check['total']}个角色匹配）",
                            "extracted_characters": extracted_chars,
                            "presence_check": presence_check
                        }

            # 完全没有参考信息
            self._log_execution("无角色设定且无分析结果，跳过检查")
            return {
                "status": "PASS",
                "issues": [],
                "summary": "无角色设定文档和分析结果，跳过检查"
            }

        # 有角色文档时，使用 LLM 进行深度检查
        user_prompt = f"""请检查以下章节内容中的角色表现是否符合角色设定：

## 角色设定
{character_doc}

## 章节内容
{content[:6000]}  # 限制长度避免超出 token

请进行角色一致性检查。"""

        # 调用 LLM
        response = await self._call_llm(
            system_prompt=CHARACTER_GUARD_PROMPT,
            user_prompt=user_prompt,
            temperature=0.3,  # 审查需要更稳定
            max_tokens=2000,
            task_type=TaskType.TEXT_CLASSIFICATION
        )

        # 解析响应
        result = self._parse_json_response(response)

        check_result = {
            "status": result.get("status", "PASS"),
            "issues": result.get("issues", []),
            "summary": result.get("summary", "检查完成")
        }

        self._log_execution(
            "角色检查完成",
            {"status": check_result["status"], "issue_count": len(check_result["issues"])}
        )

        return check_result
