"""
网文11维度分析策略

参考番茄小说平台的网文分析方法,提供11个维度的深度分析:
1. 核心卖点
2. 主角设定
3. 金手指系统
4. 世界观框架
5. 等级力量体系
6. 反派势力
7. 情感线设定
8. 爽点布局
9. 期待感钩子
10. 支线剧情
11. 特色设定
"""

import json
import re
from typing import Dict, List, Optional, Any

from .strategy import (
    BookAnalysisStrategy,
    AnalysisDimension,
    DimensionType,
    strategy_registry
)


class WebNovelStrategy(BookAnalysisStrategy):
    """
    网文11维度分析策略

    专为网络小说(特别是爽文)设计的分析策略
    """

    @property
    def strategy_id(self) -> str:
        return "web_novel_11d"

    @property
    def strategy_name(self) -> str:
        return "网文11维度分析"

    @property
    def description(self) -> str:
        return "专为网络小说设计的11维度深度分析,包括核心卖点、金手指系统、爽点布局等网文特有元素"

    def get_dimensions(self) -> List[AnalysisDimension]:
        """定义11个分析维度"""
        return [
            # 1. 核心卖点
            AnalysisDimension(
                id="core_selling_point",
                name="核心卖点",
                description="一句话概括小说的最大吸引力点",
                priority=1,
                output_length="50-80字",
                dimension_type=DimensionType.TECHNIQUE,
                tags=["卖点", "核心定位"]
            ),

            # 2. 主角设定
            AnalysisDimension(
                id="protagonist_setting",
                name="主角设定",
                description="主角的身份背景、性格标签、初始困境",
                priority=2,
                output_length="100-200字",
                dimension_type=DimensionType.CHARACTER_TEMPLATE,
                tags=["角色", "主角"],
                sub_elements=[
                    {"id": "identity", "name": "身份背景"},
                    {"id": "personality", "name": "性格标签"},
                    {"id": "initial_crisis", "name": "初始困境"}
                ]
            ),

            # 3. 金手指系统
            AnalysisDimension(
                id="cheat_system",
                name="金手指系统",
                description="主角的外挂、系统或核心优势",
                priority=3,
                output_length="150-250字",
                dimension_type=DimensionType.POWER_SYSTEM,
                tags=["金手指", "系统"],
                sub_elements=[
                    {"id": "mechanism", "name": "核心机理"},
                    {"id": "growth_path", "name": "成长路径"},
                    {"id": "usage_examples", "name": "用法示例"}
                ]
            ),

            # 4. 世界观框架
            AnalysisDimension(
                id="world_framework",
                name="世界观框架",
                description="故事发生的时代背景与底层规则",
                priority=4,
                output_length="100-200字",
                dimension_type=DimensionType.SETTING,
                tags=["世界观", "背景设定"]
            ),

            # 5. 等级力量体系
            AnalysisDimension(
                id="power_system",
                name="等级力量体系",
                description="角色成长的分层体系与战力规则",
                priority=5,
                output_length="100-200字",
                dimension_type=DimensionType.POWER_SYSTEM,
                tags=["力量体系", "等级"]
            ),

            # 6. 反派势力
            AnalysisDimension(
                id="antagonist_forces",
                name="反派势力",
                description="敌对体系,层级递进的反派设计",
                priority=6,
                output_length="100-200字",
                dimension_type=DimensionType.CHARACTER_TEMPLATE,
                tags=["反派", "势力"],
                sub_elements=[
                    {"id": "tier_1", "name": "前期反派"},
                    {"id": "tier_2", "name": "中期反派"},
                    {"id": "tier_3", "name": "后期反派"}
                ]
            ),

            # 7. 情感线设定
            AnalysisDimension(
                id="romance_line",
                name="情感线设定",
                description="情感关系的发展路径",
                priority=7,
                output_length="100-150字",
                dimension_type=DimensionType.RELATIONSHIP,
                tags=["情感线", "感情"]
            ),

            # 8. 爽点布局
            AnalysisDimension(
                id="satisfaction_points",
                name="爽点布局",
                description="打脸、反差、碾压、绝境翻盘等爽点设计",
                priority=8,
                output_length="150-250字",
                dimension_type=DimensionType.TECHNIQUE,
                tags=["爽点", "节奏"],
                sub_elements=[
                    {"id": "chapter_1_10", "name": "前10章爽点"},
                    {"id": "chapter_10_30", "name": "10-30章爽点"},
                    {"id": "chapter_30_plus", "name": "30章后爽点"}
                ]
            ),

            # 9. 期待感钩子
            AnalysisDimension(
                id="anticipation_hooks",
                name="期待感钩子",
                description="悬念、伏笔、预告等拉期待的设计",
                priority=9,
                output_length="150-250字",
                dimension_type=DimensionType.TECHNIQUE,
                tags=["悬念", "伏笔", "期待感"]
            ),

            # 10. 支线剧情
            AnalysisDimension(
                id="sub_plots",
                name="支线剧情",
                description="增强可读性的副线",
                priority=10,
                output_length="100-200字",
                dimension_type=DimensionType.PLOT_STRUCTURE,
                tags=["支线", "副线"]
            ),

            # 11. 特色设定
            AnalysisDimension(
                id="unique_features",
                name="特色设定",
                description="差异化卖点与母题",
                priority=11,
                output_length="100-150字",
                dimension_type=DimensionType.TECHNIQUE,
                tags=["特色", "差异化"]
            ),
        ]

    def build_system_prompt(self) -> str:
        """构建系统提示词"""
        return """你是一位在番茄小说平台孵化多本爆款的白金大神作家兼策划。

核心理念 (必须贯彻):
- **金手指**: 独特且具成长性的优势/系统,避免平庸或单纯数值堆砌
- **爽点**: 反差、打脸、扮猪吃虎、绝境翻盘、信息差等,每隔几章必须有一波"大爽"
- **期待感**: 悬念、伏笔、信息差形成闭环,每一章都让读者想看下一章
- **网感**: 始终围绕"读者体验"与"商业化结果"思考

输出要求:
1. 严格遵循JSON Schema结构
2. 根节点 (11个维度) 每个50-80字精炼概括
3. 叶子节点 (详细内容) 每个100-200字深度阐述
4. 必须体现"拉期待—给爽点—再拉期待"的循环结构
5. 所有内容必须可落地执行,避免空洞理论

禁止行为:
- 生成与网文商业逻辑脱节的"文学化"设定
- 使用模糊词汇 ("可能"、"也许"、"或许")
- 重复已有网文的套路而不加创新
- 忽略"爽点密度"与"期待感钩子"的布局

【方案B】JSON格式严格要求 (务必遵守):
1. ✅ 必须使用英文标点: 英文双引号("), 英文逗号(,), 英文冒号(:)
2. ❌ 禁止使用中文标点: 中文引号("")('')、中文逗号(,)、中文冒号(:)
3. ❌ 禁止使用markdown代码块包裹 (不要写 ```json 或 ```)
4. ✅ 直接返回纯JSON,第一个字符必须是 {,最后一个字符必须是 }
5. ✅ 所有字符串值必须用英文双引号包裹,内部如需引号请用转义 \"

错误示例: {"name": "食神阁"}  ← 包含中文引号,会导致解析失败
正确示例: {"name": "食神阁"}  ← 使用英文引号

**重要**: 你必须且只能返回纯 JSON 格式,严格使用英文标点符号。"""

    def build_user_prompt(
        self,
        content: str,
        existing_settings: Optional[Dict[str, Any]] = None,
        is_incremental: bool = False,
        chapter_num: Optional[int] = None
    ) -> str:
        """构建用户提示词"""

        # 基础提示词
        prompt = f"""小说内容:
{content}

"""

        # 增量分析模式
        if is_incremental and existing_settings:
            prompt += f"""=== 增量分析模式 ===
当前章节: 第{chapter_num}章

已知设定 (请避免重复):
{self._format_existing_settings(existing_settings)}

你的任务:
ONLY 提取 **新增的** 或 **变化的** 设定元素:
1. 新角色出现?
2. 新技能/装备/系统功能?
3. 新反派/势力?
4. 新的爽点类型?
5. 世界观扩展?

如果本章没有新元素,返回: {{"no_new_content": true}}

"""

        # 维度清单
        dimensions = self.get_dimensions()
        prompt += """根节点清单 (必须包含,顺序不可变):
"""
        for i, dim in enumerate(dimensions, 1):
            prompt += f"{i}. {dim.name} ({dim.id}): {dim.description}\n"
            if dim.sub_elements:
                for sub in dim.sub_elements:
                    prompt += f"   - {sub['name']} ({sub['id']})\n"

        # 输出格式要求
        prompt += """
输出格式要求:
- 使用纯 JSON 格式 (不要用 markdown 代码块包裹)
- 每个维度必须包含: id、name、description、children (如有)
- description 为核心内容,根节点50-80字,叶子节点100-200字
- 所有子节点必须在 children 数组中,不得遗漏
- 必须包含所有11个根节点,不得擅自合并或删减

JSON Schema:
{
  "root_nodes": [
    {
      "id": "core_selling_point",
      "name": "核心卖点",
      "description": "...",
      "children": []  // 可选
    },
    ...
  ]
}

特别提醒:
- 番茄小说读者偏好"快节奏+高爽点密度",前3章必须有至少2个爽点
- 金手指必须"独特+可成长+有具体用法"
- 反派必须有"层级递进"
- 情感线不能"无脑倒贴",必须有情感张力
"""

        return prompt

    def _format_existing_settings(self, settings: Dict[str, Any]) -> str:
        """格式化已有设定为文本摘要"""
        lines = []
        for dim_id, data in settings.items():
            dim = self.get_dimension_by_id(dim_id)
            if dim:
                lines.append(f"- {dim.name}: {data.get('description', '')[:50]}...")
        return "\n".join(lines)

    def parse_ai_response(self, response: str) -> Dict[str, Any]:
        """
        解析AI返回结果

        支持多种格式和容错策略:
        1. 纯JSON
        2. markdown代码块包裹的JSON
        3. 前后有额外文本的JSON
        4. 包含中文标点的JSON (自动修复)
        5. 格式错误的JSON (使用json-repair自动修复)
        """
        import logging
        logger = logging.getLogger(__name__)

        logger.info(f"🔍 开始解析AI响应,长度={len(response)}")
        logger.debug(f"📝 原始响应前500字符: {response[:500]}")

        # 【方案A】预处理: 替换中文标点符号为英文标点
        original_response = response
        response = response.replace('"', '"').replace('"', '"')  # 中文双引号 → 英文双引号
        response = response.replace(''', "'").replace(''', "'")  # 中文单引号 → 英文单引号
        response = response.replace('，', ',')  # 中文逗号 → 英文逗号 (保守,仅在JSON关键位置)

        if response != original_response:
            logger.info(f"✅ 预处理: 已替换中文标点符号")
            logger.debug(f"📝 替换后前500字符: {response[:500]}")

        # 尝试直接解析
        try:
            data = json.loads(response)
            logger.info(f"✅ 直接解析JSON成功")
            return self._normalize_response(data)
        except json.JSONDecodeError as e:
            logger.debug(f"❌ 直接解析失败: {e}")

        # 尝试提取JSON (处理markdown代码块)
        json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            try:
                extracted = json_match.group(1)
                logger.info(f"🔍 从markdown代码块提取JSON,长度={len(extracted)}")
                data = json.loads(extracted)
                logger.info(f"✅ markdown格式解析成功")
                return self._normalize_response(data)
            except json.JSONDecodeError as e:
                logger.debug(f"❌ markdown格式解析失败: {e}")

        # 尝试提取花括号内容
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                extracted = json_match.group(0)
                logger.info(f"🔍 提取花括号内容,长度={len(extracted)}")
                data = json.loads(extracted)
                logger.info(f"✅ 花括号内容解析成功")
                return self._normalize_response(data)
            except json.JSONDecodeError as e:
                logger.debug(f"❌ 花括号内容解析失败: {e}")
                logger.debug(f"📝 提取的内容: {extracted[:500]}...")

                # 【方案D】最后的手段: 使用json-repair自动修复
                try:
                    from json_repair import repair_json
                    logger.info(f"🔧 尝试使用json-repair修复JSON...")
                    repaired = repair_json(extracted)
                    data = json.loads(repaired)
                    logger.info(f"✅ json-repair修复成功!")
                    return self._normalize_response(data)
                except Exception as repair_error:
                    logger.error(f"❌ json-repair修复失败: {repair_error}")

        # 如果提取花括号也失败,对整个响应尝试json-repair
        try:
            from json_repair import repair_json
            logger.info(f"🔧 对完整响应尝试json-repair...")
            repaired = repair_json(response)
            data = json.loads(repaired)
            logger.info(f"✅ json-repair修复完整响应成功!")
            return self._normalize_response(data)
        except Exception as e:
            logger.error(f"❌ json-repair修复完整响应失败: {e}")

        # 解析失败,记录完整响应
        logger.error(f"❌ 所有解析方法都失败 (包括json-repair)")
        logger.error(f"📝 完整响应内容:\n{response}")
        raise ValueError(f"无法解析AI响应为JSON格式,请查看日志获取详细信息")

    def _normalize_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化响应数据结构

        将 {root_nodes: [...]} 转换为 {dimension_id: {...}}
        并补充 dimension_type 字段
        """
        if "root_nodes" in data:
            # 标准格式
            result = {}
            for node in data["root_nodes"]:
                dim_id = node["id"]
                # 从策略定义中获取 dimension_type
                dimension = self.get_dimension_by_id(dim_id)
                if dimension:
                    node["dimension_type"] = dimension.dimension_type.value
                result[dim_id] = node
            return result
        elif "no_new_content" in data:
            # 增量分析无新内容
            return data
        else:
            # 直接是字典格式,也需要补充 dimension_type
            result = {}
            for dim_id, node in data.items():
                dimension = self.get_dimension_by_id(dim_id)
                if dimension:
                    node["dimension_type"] = dimension.dimension_type.value
                result[dim_id] = node
            return result


# 注册策略到全局注册器
web_novel_strategy = WebNovelStrategy()
strategy_registry.register(web_novel_strategy)
