"""
智能建议生成器

从11维度分析结果生成可关联的世界观元素建议
"""

import json
from typing import Dict, List, Optional, Any
from uuid import UUID

from app.models.worldview_suggestion import (
    WorldviewSuggestion,
    SuggestionType,
    SuggestionAction,
    SuggestionStatus
)
from app.services.book_analysis.strategy import DimensionType


class SuggestionGenerator:
    """
    智能建议生成器

    将11维度分析结果映射为可关联的世界观元素建议
    """

    # 维度类型到建议类型的映射
    DIMENSION_TO_SUGGESTION = {
        DimensionType.CHARACTER_TEMPLATE: SuggestionType.CHARACTER,
        DimensionType.POWER_SYSTEM: SuggestionType.POWER_SYSTEM,
        DimensionType.SETTING: SuggestionType.SETTING,
        DimensionType.RELATIONSHIP: SuggestionType.RELATIONSHIP,
    }

    # 置信度阈值
    MIN_CONFIDENCE = 0.6  # 最小置信度

    def __init__(self, ai_service=None):
        """
        初始化建议生成器

        Args:
            ai_service: AI服务实例 (可选,用于评估置信度)
        """
        self.ai_service = ai_service

    def generate_suggestions(
        self,
        analysis_result: Dict[str, Any],
        job_id: UUID,
        user_id: UUID,
        work_id: Optional[UUID] = None,
        strategy_id: str = "web_novel_11d"
    ) -> List[Dict[str, Any]]:
        """
        从分析结果生成智能建议

        Args:
            analysis_result: 11维度分析结果
            job_id: 分析任务ID
            user_id: 用户ID
            work_id: 关联作品ID (可选)
            strategy_id: 使用的策略ID

        Returns:
            建议列表 (字典格式,待存入数据库)
        """
        suggestions = []

        # 遍历分析结果
        for dim_id, data in analysis_result.items():
            # 跳过无新内容标记
            if dim_id == "no_new_content":
                continue

            # 获取维度类型
            dimension_type = data.get("dimension_type")
            if not dimension_type:
                continue

            # 检查是否可以生成建议
            suggestion_type = self.DIMENSION_TO_SUGGESTION.get(
                DimensionType(dimension_type)
            )
            if not suggestion_type:
                # 不可关联的维度类型,跳过
                continue

            # 生成建议
            suggestion = self._create_suggestion(
                dimension_id=dim_id,
                dimension_data=data,
                suggestion_type=suggestion_type,
                job_id=job_id,
                user_id=user_id,
                work_id=work_id
            )

            if suggestion and suggestion["confidence_score"] >= self.MIN_CONFIDENCE:
                suggestions.append(suggestion)

        return suggestions

    def _create_suggestion(
        self,
        dimension_id: str,
        dimension_data: Dict[str, Any],
        suggestion_type: SuggestionType,
        job_id: UUID,
        user_id: UUID,
        work_id: Optional[UUID]
    ) -> Optional[Dict[str, Any]]:
        """
        创建单个建议

        Args:
            dimension_id: 维度ID
            dimension_data: 维度数据
            suggestion_type: 建议类型
            job_id: 任务ID
            user_id: 用户ID
            work_id: 作品ID

        Returns:
            建议字典,如果无法创建则返回None
        """
        # 根据维度ID和类型构建建议数据
        suggested_data = self._build_suggested_data(
            dimension_id=dimension_id,
            dimension_data=dimension_data,
            suggestion_type=suggestion_type
        )

        if not suggested_data:
            return None

        # 评估置信度
        confidence = self._assess_confidence(
            dimension_data=dimension_data,
            suggestion_type=suggestion_type
        )

        # 生成建议理由
        reason = self._generate_reason(
            dimension_id=dimension_id,
            dimension_data=dimension_data,
            suggestion_type=suggestion_type,
            confidence=confidence
        )

        return {
            "user_id": user_id,
            "job_id": job_id,
            "work_id": work_id,
            "suggestion_type": suggestion_type.value,
            "action": SuggestionAction.CREATE_NEW.value,
            "suggested_data": suggested_data,
            "confidence_score": confidence,
            "reason": reason,
            "status": SuggestionStatus.PENDING.value,
        }

    def _build_suggested_data(
        self,
        dimension_id: str,
        dimension_data: Dict[str, Any],
        suggestion_type: SuggestionType
    ) -> Optional[Dict[str, Any]]:
        """
        构建建议数据

        根据维度类型和建议类型,提取并预填充数据
        """
        name = dimension_data.get("name", "")
        description = dimension_data.get("description", "")
        children = dimension_data.get("children", [])

        if suggestion_type == SuggestionType.CHARACTER:
            # 角色建议
            return self._build_character_suggestion(
                dimension_id, name, description, children
            )

        elif suggestion_type == SuggestionType.POWER_SYSTEM:
            # 力量体系建议
            return self._build_power_system_suggestion(
                dimension_id, name, description, children
            )

        elif suggestion_type == SuggestionType.SETTING:
            # 设定建议
            return self._build_setting_suggestion(
                dimension_id, name, description, children
            )

        elif suggestion_type == SuggestionType.RELATIONSHIP:
            # 关系建议
            return self._build_relationship_suggestion(
                dimension_id, name, description, children
            )

        return None

    def _build_character_suggestion(
        self, dim_id: str, name: str, desc: str, children: List
    ) -> Dict[str, Any]:
        """构建角色建议数据"""
        # 提取子元素
        identity = ""
        personality = ""
        for child in children:
            child_id = child.get("id", "")
            if "identity" in child_id or "背景" in child.get("name", ""):
                identity = child.get("description", "")
            elif "personality" in child_id or "性格" in child.get("name", ""):
                personality = child.get("description", "")

        # 尝试从描述中提取角色名
        character_name = self._extract_character_name(desc)

        return {
            "name": character_name or f"{name}原型",
            "role": self._infer_character_role(dim_id, name),
            "identity": identity or desc[:100],
            "personality_tags": self._extract_tags(personality),
            "background": identity or desc,
            "description": desc,
            "source": "AI拆书分析",
        }

    def _build_power_system_suggestion(
        self, dim_id: str, name: str, desc: str, children: List
    ) -> Dict[str, Any]:
        """构建力量体系建议数据"""
        mechanism = ""
        growth_path = ""

        for child in children:
            child_id = child.get("id", "")
            if "mechanism" in child_id or "机理" in child.get("name", ""):
                mechanism = child.get("description", "")
            elif "growth" in child_id or "成长" in child.get("name", ""):
                growth_path = child.get("description", "")

        return {
            "name": name,
            "category": self._infer_power_category(dim_id, name, desc),
            "description": desc,
            "mechanism": mechanism or desc,
            "levels": self._extract_levels(growth_path),
            "source": "AI拆书分析",
        }

    def _build_setting_suggestion(
        self, dim_id: str, name: str, desc: str, children: List
    ) -> Dict[str, Any]:
        """构建设定建议数据"""
        return {
            "name": name,
            "category": "background",
            "description": desc,
            "details": {
                "era": self._extract_era(desc),
                "rules": self._extract_rules(desc),
                "children_details": [
                    {"name": child.get("name"), "desc": child.get("description")}
                    for child in children
                ]
            },
            "source": "AI拆书分析",
        }

    def _build_relationship_suggestion(
        self, dim_id: str, name: str, desc: str, children: List
    ) -> Dict[str, Any]:
        """构建关系建议数据"""
        return {
            "name": name,
            "type": "romantic",  # 情感线默认为romantic
            "description": desc,
            "stages": [
                child.get("description", "")
                for child in children
            ],
            "source": "AI拆书分析",
        }

    def _assess_confidence(
        self,
        dimension_data: Dict[str, Any],
        suggestion_type: SuggestionType
    ) -> float:
        """
        评估建议的置信度

        基于以下因素:
        - 描述长度和完整性
        - 子元素数量
        - 关键信息是否齐全
        """
        description = dimension_data.get("description", "")
        children = dimension_data.get("children", [])

        confidence = 0.5  # 基础分

        # 描述长度
        if len(description) >= 100:
            confidence += 0.2
        elif len(description) >= 50:
            confidence += 0.1

        # 子元素数量
        if len(children) >= 2:
            confidence += 0.15
        elif len(children) >= 1:
            confidence += 0.1

        # 关键信息完整性
        if suggestion_type == SuggestionType.CHARACTER:
            if any("性格" in child.get("name", "") for child in children):
                confidence += 0.05
            if any("背景" in child.get("name", "") for child in children):
                confidence += 0.05

        # 上限1.0
        return min(confidence, 1.0)

    def _generate_reason(
        self,
        dimension_id: str,
        dimension_data: Dict[str, Any],
        suggestion_type: SuggestionType,
        confidence: float
    ) -> str:
        """生成建议理由"""
        name = dimension_data.get("name", "")

        reason_templates = {
            SuggestionType.CHARACTER: f"从'{name}'维度中提取到详细的角色设定,建议创建为世界观角色元素。",
            SuggestionType.POWER_SYSTEM: f"从'{name}'维度中识别到完整的力量体系,建议创建为世界观力量体系。",
            SuggestionType.SETTING: f"从'{name}'维度中发现世界观相关设定,建议创建为背景设定元素。",
            SuggestionType.RELATIONSHIP: f"从'{name}'维度中识别到情感关系设定,建议创建为关系元素。",
        }

        reason = reason_templates.get(suggestion_type, "")

        if confidence >= 0.8:
            reason += " (高置信度推荐)"
        elif confidence >= 0.7:
            reason += " (推荐采纳)"

        return reason

    # ========== 辅助方法 ==========

    def _extract_character_name(self, text: str) -> Optional[str]:
        """从文本中提取角色名"""
        # 简单策略: 查找常见的角色名模式
        import re
        patterns = [
            r'([\u4e00-\u9fa5]{2,4})(?:是|为|乃)',  # "XXX是..."
            r'主角[^\s]*?(?:叫|名为)([\u4e00-\u9fa5]{2,4})',  # "主角叫XXX"
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None

    def _infer_character_role(self, dim_id: str, name: str) -> str:
        """推断角色类型"""
        if "protagonist" in dim_id or "主角" in name:
            return "protagonist"
        elif "antagonist" in dim_id or "反派" in name:
            return "antagonist"
        else:
            return "supporting"

    def _infer_power_category(self, dim_id: str, name: str, desc: str) -> str:
        """推断力量体系类别"""
        if "金手指" in name or "cheat" in dim_id:
            return "cheat_system"
        elif "等级" in name or "power" in dim_id:
            return "level_system"
        else:
            return "other"

    def _extract_tags(self, text: str) -> List[str]:
        """提取标签"""
        # 简单实现: 按逗号、顿号分割
        import re
        tags = re.split(r'[,、;;\s]+', text)
        return [tag.strip() for tag in tags if tag.strip() and len(tag.strip()) < 10][:5]

    def _extract_levels(self, text: str) -> List[str]:
        """提取等级列表"""
        import re
        # 查找 "XX阶/级/层/境" 模式
        levels = re.findall(r'[\u4e00-\u9fa5]+(?:阶|级|层|境|期)', text)
        return levels[:10]  # 最多10个

    def _extract_era(self, text: str) -> str:
        """提取时代背景"""
        import re
        era_patterns = [
            r'([\u4e00-\u9fa5]+朝代|[\u4e00-\u9fa5]+时代|[\u4e00-\u9fa5]+年)',
            r'(现代|古代|未来|科幻|玄幻|仙侠|武侠)',
        ]
        for pattern in era_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return "未指定"

    def _extract_rules(self, text: str) -> str:
        """提取世界规则"""
        # 简单实现: 提取前100字
        return text[:100] + "..." if len(text) > 100 else text
