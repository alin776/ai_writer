"""
Story Bible一致性检查器 (Consistency Checker)

功能:
1. 检查世界观设定的一致性
2. 检查角色特征的一致性
3. 检查情节逻辑的一致性
4. 检查时间线的一致性
5. 自动提示矛盾点

Story Bible (故事圣经):
- 包含作品的所有设定、规则、角色信息
- 确保整部作品的内部逻辑一致

使用场景:
- 撰写新章节时自动检查
- 修改设定时检查影响范围
- 作品完成后全面检查
"""

from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class InconsistencyType(str, Enum):
    """不一致类型"""
    WORLDVIEW = "worldview"  # 世界观矛盾
    CHARACTER = "character"  # 角色矛盾
    PLOT = "plot"  # 情节矛盾
    TIMELINE = "timeline"  # 时间线矛盾
    LOGIC = "logic"  # 逻辑矛盾


class InconsistencySeverity(str, Enum):
    """严重程度"""
    CRITICAL = "critical"  # 严重：完全矛盾
    WARNING = "warning"  # 警告：可能矛盾
    INFO = "info"  # 提示：值得注意


class Inconsistency(BaseModel):
    """不一致记录"""
    type: InconsistencyType
    severity: InconsistencySeverity
    description: str  # 问题描述
    evidence: List[Dict[str, Any]]  # 证据（引用的文本位置）
    suggestion: Optional[str] = None  # 修复建议
    detected_at: str


class StoryElement(BaseModel):
    """故事元素（用于追踪）"""
    element_id: str
    element_type: str  # character/location/item/rule
    name: str
    properties: Dict[str, Any]  # 属性
    first_mentioned: str  # 首次提及的章节ID
    mentioned_in: List[str] = []  # 提及的章节ID列表


class ConsistencyReport(BaseModel):
    """一致性检查报告"""
    work_id: str
    checked_at: str
    total_elements: int  # 检查的元素总数
    total_inconsistencies: int  # 发现的不一致总数
    inconsistencies: List[Inconsistency]  # 不一致列表
    consistency_score: float  # 一致性得分 0-100


class StoryBibleConsistencyChecker:
    """Story Bible一致性检查器"""

    def __init__(self, ai_service: Any = None):
        """
        初始化检查器

        Args:
            ai_service: AI服务（用于语义理解）
        """
        self.ai_service = ai_service
        self.elements: Dict[str, StoryElement] = {}

    # ==================== 元素追踪 ====================

    def track_element(
        self,
        element: StoryElement
    ):
        """
        追踪故事元素

        Args:
            element: 故事元素
        """
        self.elements[element.element_id] = element

    def get_element(self, element_id: str) -> Optional[StoryElement]:
        """获取元素"""
        return self.elements.get(element_id)

    def update_element_mention(
        self,
        element_id: str,
        chapter_id: str
    ):
        """
        更新元素提及记录

        Args:
            element_id: 元素ID
            chapter_id: 章节ID
        """
        element = self.elements.get(element_id)
        if element and chapter_id not in element.mentioned_in:
            element.mentioned_in.append(chapter_id)

    # ==================== 角色一致性检查 ====================

    def check_character_consistency(
        self,
        character_id: str,
        new_properties: Dict[str, Any],
        chapter_id: str
    ) -> List[Inconsistency]:
        """
        检查角色一致性

        Args:
            character_id: 角色ID
            new_properties: 新出现的属性
            chapter_id: 当前章节ID

        Returns:
            List[Inconsistency]: 发现的不一致
        """
        inconsistencies = []

        character = self.get_element(character_id)
        if not character:
            return inconsistencies

        original_props = character.properties

        # 检查物理特征
        physical_attrs = ["height", "eye_color", "hair_color", "age"]
        for attr in physical_attrs:
            if attr in original_props and attr in new_properties:
                if original_props[attr] != new_properties[attr]:
                    inconsistencies.append(Inconsistency(
                        type=InconsistencyType.CHARACTER,
                        severity=InconsistencySeverity.CRITICAL,
                        description=f"角色「{character.name}」的{attr}前后不一致",
                        evidence=[
                            {
                                "chapter": character.first_mentioned,
                                "value": original_props[attr]
                            },
                            {
                                "chapter": chapter_id,
                                "value": new_properties[attr]
                            }
                        ],
                        suggestion=f"保持{attr}一致，建议使用：{original_props[attr]}",
                        detected_at=datetime.now().isoformat()
                    ))

        # 检查性格特征
        if "personality" in original_props and "personality" in new_properties:
            original_personality = set(original_props["personality"])
            new_personality = set(new_properties["personality"])

            contradictions = self._find_personality_contradictions(
                original_personality,
                new_personality
            )

            for contradiction in contradictions:
                inconsistencies.append(Inconsistency(
                    type=InconsistencyType.CHARACTER,
                    severity=InconsistencySeverity.WARNING,
                    description=f"角色「{character.name}」的性格特征可能矛盾：{contradiction}",
                    evidence=[
                        {"chapter": character.first_mentioned},
                        {"chapter": chapter_id}
                    ],
                    suggestion="检查角色性格发展是否合理",
                    detected_at=datetime.now().isoformat()
                ))

        return inconsistencies

    def _find_personality_contradictions(
        self,
        original: Set[str],
        new: Set[str]
    ) -> List[str]:
        """查找性格矛盾"""
        # 定义矛盾的性格特征对
        contradictory_pairs = [
            ("勇敢", "胆小"),
            ("开朗", "内向"),
            ("冷酷", "善良"),
            ("冲动", "冷静"),
            ("慷慨", "吝啬")
        ]

        contradictions = []
        for trait1, trait2 in contradictory_pairs:
            if trait1 in original and trait2 in new:
                contradictions.append(f"{trait1} vs {trait2}")
            elif trait2 in original and trait1 in new:
                contradictions.append(f"{trait2} vs {trait1}")

        return contradictions

    # ==================== 世界观一致性检查 ====================

    def check_worldview_consistency(
        self,
        rule_name: str,
        new_rule: str,
        chapter_id: str
    ) -> List[Inconsistency]:
        """
        检查世界观规则一致性

        Args:
            rule_name: 规则名称
            new_rule: 新的规则描述
            chapter_id: 当前章节ID

        Returns:
            List[Inconsistency]: 发现的不一致
        """
        inconsistencies = []

        # 查找是否已有相同名称的规则
        existing_rule = None
        for element in self.elements.values():
            if element.element_type == "rule" and element.name == rule_name:
                existing_rule = element
                break

        if existing_rule:
            old_rule = existing_rule.properties.get("description", "")

            # 使用AI检测规则是否矛盾（简化版）
            if self._rules_conflict(old_rule, new_rule):
                inconsistencies.append(Inconsistency(
                    type=InconsistencyType.WORLDVIEW,
                    severity=InconsistencySeverity.CRITICAL,
                    description=f"世界观规则「{rule_name}」前后矛盾",
                    evidence=[
                        {
                            "chapter": existing_rule.first_mentioned,
                            "rule": old_rule
                        },
                        {
                            "chapter": chapter_id,
                            "rule": new_rule
                        }
                    ],
                    suggestion="统一世界观规则设定",
                    detected_at=datetime.now().isoformat()
                ))

        return inconsistencies

    def _rules_conflict(self, rule1: str, rule2: str) -> bool:
        """
        判断两条规则是否矛盾

        Args:
            rule1: 规则1
            rule2: 规则2

        Returns:
            bool: 是否矛盾
        """
        # 简化版：检查是否包含否定词
        negation_words = ["不能", "禁止", "不可", "无法"]

        rule1_has_negation = any(word in rule1 for word in negation_words)
        rule2_has_negation = any(word in rule2 for word in negation_words)

        # 如果一个有否定词，一个没有，可能矛盾
        if rule1_has_negation != rule2_has_negation:
            return True

        # 实际应该使用AI进行语义分析
        return False

    # ==================== 时间线一致性检查 ====================

    def check_timeline_consistency(
        self,
        events: List[Dict[str, Any]]
    ) -> List[Inconsistency]:
        """
        检查时间线一致性

        Args:
            events: 事件列表，每个事件包含 {time, event, chapter_id}

        Returns:
            List[Inconsistency]: 发现的不一致
        """
        inconsistencies = []

        # 按时间排序
        sorted_events = sorted(events, key=lambda e: e.get("time", 0))

        # 检查逻辑顺序
        for i in range(len(sorted_events) - 1):
            current = sorted_events[i]
            next_event = sorted_events[i + 1]

            # 检查时间倒流
            if current["time"] > next_event["time"]:
                inconsistencies.append(Inconsistency(
                    type=InconsistencyType.TIMELINE,
                    severity=InconsistencySeverity.CRITICAL,
                    description="时间线出现倒流",
                    evidence=[current, next_event],
                    suggestion="调整事件发生的时间顺序",
                    detected_at=datetime.now().isoformat()
                ))

        return inconsistencies

    # ==================== 综合检查 ====================

    async def check_consistency(
        self,
        work_id: str,
        chapters: List[Dict[str, Any]]
    ) -> ConsistencyReport:
        """
        综合一致性检查

        Args:
            work_id: 作品ID
            chapters: 章节列表

        Returns:
            ConsistencyReport: 检查报告
        """
        all_inconsistencies = []

        # 检查所有已追踪的元素
        for chapter in chapters:
            chapter_id = chapter["id"]
            content = chapter["content"]

            # 提取章节中提及的元素
            # 这里简化处理，实际应该使用NER等技术
            mentioned_elements = self._extract_mentioned_elements(content)

            for element_id, properties in mentioned_elements.items():
                # 检查角色
                element = self.get_element(element_id)
                if element and element.element_type == "character":
                    issues = self.check_character_consistency(
                        element_id,
                        properties,
                        chapter_id
                    )
                    all_inconsistencies.extend(issues)

                # 更新提及记录
                self.update_element_mention(element_id, chapter_id)

        # 生成报告
        consistency_score = self._calculate_consistency_score(
            len(self.elements),
            len(all_inconsistencies)
        )

        return ConsistencyReport(
            work_id=work_id,
            checked_at=datetime.now().isoformat(),
            total_elements=len(self.elements),
            total_inconsistencies=len(all_inconsistencies),
            inconsistencies=all_inconsistencies,
            consistency_score=consistency_score
        )

    def _extract_mentioned_elements(
        self,
        content: str
    ) -> Dict[str, Dict[str, Any]]:
        """
        从内容中提取提及的元素

        Args:
            content: 文本内容

        Returns:
            Dict: {element_id: properties}
        """
        # 简化版：返回空
        # 实际应该使用NER识别人名、地名等
        # 并提取相关属性描述
        return {}

    def _calculate_consistency_score(
        self,
        total_elements: int,
        total_inconsistencies: int
    ) -> float:
        """
        计算一致性得分

        Args:
            total_elements: 元素总数
            total_inconsistencies: 不一致总数

        Returns:
            float: 得分 0-100
        """
        if total_elements == 0:
            return 100.0

        # 每个不一致扣分
        deduction_per_issue = 100.0 / max(total_elements, 1)
        score = 100.0 - (total_inconsistencies * deduction_per_issue)

        return max(0.0, min(100.0, score))

    # ==================== 智能修复建议 ====================

    def suggest_fixes(
        self,
        inconsistencies: List[Inconsistency]
    ) -> Dict[str, List[str]]:
        """
        生成智能修复建议

        Args:
            inconsistencies: 不一致列表

        Returns:
            Dict: {category: [suggestions]}
        """
        suggestions = {
            "immediate": [],  # 需要立即修复
            "review": [],  # 需要审查
            "consider": []  # 可以考虑
        }

        for issue in inconsistencies:
            if issue.severity == InconsistencySeverity.CRITICAL:
                suggestions["immediate"].append(
                    f"[严重] {issue.description} - {issue.suggestion}"
                )
            elif issue.severity == InconsistencySeverity.WARNING:
                suggestions["review"].append(
                    f"[警告] {issue.description} - {issue.suggestion}"
                )
            else:
                suggestions["consider"].append(
                    f"[提示] {issue.description}"
                )

        return suggestions


# ==================== 便捷函数 ====================

async def check_story_consistency(
    work_id: str,
    chapters: List[Dict],
    characters: List[Dict],
    worldview: Dict
) -> ConsistencyReport:
    """
    检查故事一致性

    Args:
        work_id: 作品ID
        chapters: 章节列表
        characters: 角色列表
        worldview: 世界观

    Returns:
        ConsistencyReport: 检查报告
    """
    checker = StoryBibleConsistencyChecker()

    # 追踪角色
    for char in characters:
        element = StoryElement(
            element_id=char["id"],
            element_type="character",
            name=char["name"],
            properties=char,
            first_mentioned=char.get("first_chapter", "")
        )
        checker.track_element(element)

    # 追踪世界观规则
    if worldview:
        for rule_name, rule_desc in worldview.items():
            element = StoryElement(
                element_id=f"rule_{rule_name}",
                element_type="rule",
                name=rule_name,
                properties={"description": rule_desc},
                first_mentioned="worldview_setup"
            )
            checker.track_element(element)

    # 执行检查
    return await checker.check_consistency(work_id, chapters)
