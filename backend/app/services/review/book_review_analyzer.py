"""
作品级评审分析器

功能:
- 整体情节脉络分析
- 人物关系网络构建
- 世界观一致性检查
- 文风统计分析
- 结构化输出评审报告
"""

from typing import Dict, Any, List, Optional
import json
import logging
import asyncio
from datetime import datetime

from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.model_selector import TaskType  # ✅ 新增：用于成本追踪
from app.core.cache import cache_review
from app.core.config import settings
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class BookReviewAnalyzer:
    """作品级评审分析器"""

    def __init__(self, db: Optional[Any] = None, user_id: Optional[str] = None):
        """
        初始化评审分析器

        Args:
            db: 数据库会话（用于成本追踪）
            user_id: 用户ID（用于成本追踪）
        """
        # ✅ 2025-12-02: 传递db和user_id以启用成本追踪
        self.ai_service = HTTPAIService(
            model=settings.REVIEW_MODEL,
            timeout=settings.REVIEW_TIMEOUT,
            db=db,
            user_id=user_id
        )
        logger.info(
            f"[BookReviewAnalyzer] 初始化完成, "
            f"使用模型: {settings.REVIEW_MODEL}, "
            f"超时: {settings.REVIEW_TIMEOUT}秒, "
            f"成本追踪: {'启用' if db and user_id else '禁用'}"
        )

    async def analyze_full_book(
        self,
        book_title: str,
        chapters: List[Dict[str, Any]],
        author_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        完整作品分析 (并发优化版本)

        性能优化:
        - 前4个分析器并发执行 (情节/人物/世界观/文风)
        - 综合建议依赖前4个结果,串行执行
        - 预期加速比: 2.24x

        Args:
            book_title: 书名
            chapters: 章节列表 [{"title": "第1章", "content": "...", "order": 1}, ...]
            author_notes: 作者备注 (可选,暂未使用)

        Returns:
            完整分析报告
        """
        logger.info(f"[BookReviewAnalyzer] 开始分析作品: {book_title}, 章节数={len(chapters)}")
        logger.info("[BookReviewAnalyzer] 并发执行4个维度分析...")

        # ✅ 并发执行4个独立分析器 (直接在gather中传入协程)
        plot_analysis, character_analysis, worldview_analysis, writing_style = \
            await asyncio.gather(
                self._analyze_plot_structure(book_title, chapters),
                self._analyze_characters(book_title, chapters),
                self._analyze_worldview(book_title, chapters),
                self._analyze_writing_style(book_title, chapters),
                return_exceptions=True  # 容错: 某个分析器失败不影响其他
            )

        logger.info("[BookReviewAnalyzer] 4个维度分析完成,开始计算评分和建议")

        # 处理异常情况 (增强日志记录)
        if isinstance(plot_analysis, Exception):
            logger.error(
                f"情节分析失败: {type(plot_analysis).__name__}: {plot_analysis}",
                exc_info=plot_analysis
            )
            plot_analysis = self._get_default_plot_analysis()

        if isinstance(character_analysis, Exception):
            logger.error(
                f"人物分析失败: {type(character_analysis).__name__}: {character_analysis}",
                exc_info=character_analysis
            )
            character_analysis = self._get_default_character_analysis()

        if isinstance(worldview_analysis, Exception):
            logger.error(
                f"世界观分析失败: {type(worldview_analysis).__name__}: {worldview_analysis}",
                exc_info=worldview_analysis
            )
            worldview_analysis = self._get_default_worldview_analysis()

        if isinstance(writing_style, Exception):
            logger.error(
                f"文风分析失败: {type(writing_style).__name__}: {writing_style}",
                exc_info=writing_style
            )
            writing_style = self._get_default_style_analysis()

        # 5. 整体评分 (依赖前4个结果)
        overall_score = await self._calculate_overall_score(
            plot_analysis,
            character_analysis,
            worldview_analysis,
            writing_style
        )

        # 6. 综合建议 (依赖前4个结果)
        recommendations = await self._generate_recommendations(
            book_title,
            plot_analysis,
            character_analysis,
            worldview_analysis,
            writing_style
        )

        result = {
            "book_title": book_title,
            "total_chapters": len(chapters),
            "analysis_date": get_utc_now().isoformat(),
            "overall_score": overall_score,
            "plot_analysis": plot_analysis,
            "character_analysis": character_analysis,
            "worldview_analysis": worldview_analysis,
            "writing_style": writing_style,
            "recommendations": recommendations
        }

        logger.info(f"[BookReviewAnalyzer] 分析完成, 总分={overall_score}")
        return result

    async def _analyze_plot_structure(
        self,
        book_title: str,
        chapters: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        情节结构分析

        分析:
        - 起承转合是否完整
        - 高潮低谷分布
        - 节奏控制
        - 伏笔呼应
        """
        logger.info("[BookReviewAnalyzer] 开始情节结构分析")

        # 提取章节摘要
        chapter_summaries = self._extract_chapter_summaries(chapters)

        system_prompt = """你是一位资深小说编辑,擅长分析小说的情节结构。
请从以下维度分析作品的情节:
1. 结构完整性 (起承转合)
2. 高潮设计 (冲突强度、转折点)
3. 节奏控制 (快慢节奏的搭配)
4. 伏笔呼应 (铺垫与揭示)

输出格式: JSON
{
    "structure_type": "三幕式/四幕式/环形结构等",
    "acts": [
        {"act": 1, "chapters": [1, 3], "summary": "世界观建立"},
        {"act": 2, "chapters": [4, 8], "summary": "冲突升级"}
    ],
    "climax_points": [5, 10, 15],
    "rhythm_score": 85,
    "rhythm_analysis": "节奏描述",
    "foreshadowing": {
        "count": 5,
        "examples": [{"chapter": 3, "hint": "伏笔内容", "reveal_chapter": 10}]
    },
    "issues": ["问题1", "问题2"],
    "strengths": ["优点1", "优点2"]
}"""

        user_prompt = f"""书名: {book_title}
章节数: {len(chapters)}

章节概要:
{json.dumps(chapter_summaries, ensure_ascii=False, indent=2)}

请分析这部作品的情节结构。"""

        response = await self.ai_service.call_ai(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=2000,
            temperature=0.7,
            task_type=TaskType.DEEP_ANALYSIS  # ✅ 新增：作品分析任务
        )

        return self._parse_json_response(response)

    async def _analyze_characters(
        self,
        book_title: str,
        chapters: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        人物分析

        分析:
        - 主要角色识别
        - 人物弧光 (成长曲线)
        - 人物关系网络
        - 性格一致性
        """
        logger.info("[BookReviewAnalyzer] 开始人物分析")

        # 提取人物相关内容
        full_text = "\n\n".join([ch.get("content", "")[:1000] for ch in chapters[:5]])

        system_prompt = """你是一位角色塑造专家,擅长分析小说中的人物。
请从以下维度分析:
1. 主要角色识别 (主角、配角)
2. 人物弧光 (成长/转变)
3. 人物关系 (冲突、合作、情感)
4. 性格一致性

输出格式: JSON
{
    "main_characters": [
        {
            "name": "角色名",
            "role": "主角/配角",
            "traits": ["性格1", "性格2"],
            "arc": "成长描述",
            "first_appearance": 1,
            "consistency_score": 90
        }
    ],
    "relationships": [
        {"from": "角色A", "to": "角色B", "type": "敌对/合作/爱情", "strength": 8}
    ],
    "character_score": 85,
    "issues": ["人物问题"],
    "strengths": ["人物优点"]
}"""

        user_prompt = f"""书名: {book_title}
前5章内容摘要:
{full_text[:3000]}...

请分析这部作品的人物塑造。"""

        response = await self.ai_service.call_ai(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=2000,
            temperature=0.7,
            task_type=TaskType.DEEP_ANALYSIS  # ✅ 新增：作品分析任务
        )

        return self._parse_json_response(response)

    async def _analyze_worldview(
        self,
        book_title: str,
        chapters: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        世界观分析

        分析:
        - 设定完整性
        - 规则一致性
        - 背景深度
        """
        logger.info("[BookReviewAnalyzer] 开始世界观分析")

        # 提取世界观相关内容
        full_text = "\n\n".join([ch.get("content", "")[:800] for ch in chapters[:3]])

        system_prompt = """你是一位世界观设定专家。
请分析小说的世界观设定:
1. 设定完整性 (时代、地域、规则)
2. 逻辑一致性
3. 独特性与创新性

输出格式: JSON
{
    "setting": {
        "era": "时代背景",
        "location": "地点",
        "genre": "类型标签"
    },
    "rules": ["规则1", "规则2"],
    "uniqueness_score": 80,
    "consistency_score": 90,
    "depth_score": 85,
    "issues": ["问题"],
    "strengths": ["优点"]
}"""

        user_prompt = f"""书名: {book_title}
前3章内容:
{full_text[:2500]}...

请分析世界观设定。"""

        response = await self.ai_service.call_ai(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=1500,
            temperature=0.7,
            task_type=TaskType.DEEP_ANALYSIS  # ✅ 新增：作品分析任务
        )

        return self._parse_json_response(response)

    async def _analyze_writing_style(
        self,
        book_title: str,
        chapters: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        文风分析

        分析:
        - 语言特色
        - 描写手法
        - 对话质量
        - 节奏感
        """
        logger.info("[BookReviewAnalyzer] 开始文风分析")

        # 采样分析
        samples = [ch.get("content", "")[:500] for ch in chapters[::3]][:5]
        sample_text = "\n\n---\n\n".join(samples)

        system_prompt = """你是一位文学评论家,擅长分析写作风格。
请分析:
1. 语言风格 (简洁/华丽/朴实)
2. 描写手法 (视觉/心理/环境)
3. 对话质量
4. 整体美感

输出格式: JSON
{
    "style_tags": ["风格标签1", "风格标签2"],
    "language_score": 85,
    "description_score": 80,
    "dialogue_score": 90,
    "readability_score": 88,
    "analysis": "整体文风描述",
    "issues": ["问题"],
    "strengths": ["优点"]
}"""

        user_prompt = f"""书名: {book_title}
文本采样:
{sample_text[:2000]}

请分析文风特色。"""

        response = await self.ai_service.call_ai(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=1500,
            temperature=0.7,
            task_type=TaskType.DEEP_ANALYSIS  # ✅ 新增：作品分析任务
        )

        return self._parse_json_response(response)

    async def _calculate_overall_score(
        self,
        plot: Dict[str, Any],
        character: Dict[str, Any],
        worldview: Dict[str, Any],
        style: Dict[str, Any]
    ) -> float:
        """
        计算综合评分

        权重:
        - 情节: 35%
        - 人物: 30%
        - 世界观: 20%
        - 文风: 15%
        """
        plot_score = plot.get("rhythm_score", 0)
        char_score = character.get("character_score", 0)
        world_score = (
            worldview.get("consistency_score", 0) * 0.4 +
            worldview.get("depth_score", 0) * 0.3 +
            worldview.get("uniqueness_score", 0) * 0.3
        )
        style_score = (
            style.get("language_score", 0) * 0.3 +
            style.get("dialogue_score", 0) * 0.3 +
            style.get("readability_score", 0) * 0.4
        )

        overall = (
            plot_score * 0.35 +
            char_score * 0.30 +
            world_score * 0.20 +
            style_score * 0.15
        )

        return round(overall, 1)

    async def _generate_recommendations(
        self,
        book_title: str,
        plot: Dict[str, Any],
        character: Dict[str, Any],
        worldview: Dict[str, Any],
        style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成综合建议
        """
        logger.info("[BookReviewAnalyzer] 生成综合建议")

        all_issues = {
            "plot": plot.get("issues", []),
            "character": character.get("issues", []),
            "worldview": worldview.get("issues", []),
            "style": style.get("issues", [])
        }

        all_strengths = {
            "plot": plot.get("strengths", []),
            "character": character.get("strengths", []),
            "worldview": worldview.get("strengths", []),
            "style": style.get("strengths", [])
        }

        system_prompt = """你是一位资深编辑,需要给作者提供建设性的修改建议。
基于各维度的分析,生成:
1. 核心优势 (最多3条)
2. 关键问题 (最多5条)
3. 优先修改建议 (按重要性排序)

输出格式: JSON
{
    "core_strengths": ["优势1", "优势2"],
    "critical_issues": ["问题1", "问题2"],
    "priority_actions": [
        {"priority": 1, "action": "修改建议", "reason": "原因"},
        {"priority": 2, "action": "修改建议", "reason": "原因"}
    ],
    "next_steps": "下一步建议"
}"""

        user_prompt = f"""书名: {book_title}

各维度问题:
{json.dumps(all_issues, ensure_ascii=False, indent=2)}

各维度优势:
{json.dumps(all_strengths, ensure_ascii=False, indent=2)}

请生成综合建议。"""

        response = await self.ai_service.call_ai(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=1500,
            temperature=0.8,
            task_type=TaskType.DEEP_ANALYSIS  # ✅ 新增：综合建议是深度分析任务
        )

        return self._parse_json_response(response)

    def _extract_chapter_summaries(self, chapters: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """提取章节摘要"""
        summaries = []
        for ch in chapters:
            content = ch.get("content", "")
            summary = content[:200] + "..." if len(content) > 200 else content
            summaries.append({
                "chapter": ch.get("order", 0),
                "title": ch.get("title", ""),
                "summary": summary
            })
        return summaries

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        解析JSON响应

        使用统一的JSON解析工具,支持:
        - 纯JSON
        - markdown代码块
        - 前后有额外文本
        - 中文标点自动修复
        - json-repair自动修复
        """
        from app.utils.json_parser import parse_ai_json

        return parse_ai_json(
            response=response,
            log_prefix="BookReviewAnalyzer"
        )

    def _get_default_plot_analysis(self) -> Dict[str, Any]:
        """
        情节分析失败时的默认值

        使用中等分数60而非0,避免单个分析器失败拉低整体评分
        """
        return {
            "structure_type": "未分析",
            "acts": [],
            "climax_points": [],
            "rhythm_score": 60,  # 使用中等分数,避免过度惩罚
            "rhythm_analysis": "分析失败,请重试",
            "foreshadowing": {"count": 0, "examples": []},
            "issues": ["分析过程出错,请重试"],
            "strengths": []
        }

    def _get_default_character_analysis(self) -> Dict[str, Any]:
        """
        人物分析失败时的默认值

        使用中等分数60而非0,避免单个分析器失败拉低整体评分
        """
        return {
            "main_characters": [],
            "relationships": [],
            "character_score": 60,  # 使用中等分数
            "issues": ["分析过程出错,请重试"],
            "strengths": []
        }

    def _get_default_worldview_analysis(self) -> Dict[str, Any]:
        """
        世界观分析失败时的默认值

        使用中等分数60而非0,避免单个分析器失败拉低整体评分
        """
        return {
            "setting": {"era": "未知", "location": "未知", "genre": "未知"},
            "rules": [],
            "uniqueness_score": 60,  # 使用中等分数
            "consistency_score": 60,  # 使用中等分数
            "depth_score": 60,  # 使用中等分数
            "issues": ["分析过程出错,请重试"],
            "strengths": []
        }

    def _get_default_style_analysis(self) -> Dict[str, Any]:
        """
        文风分析失败时的默认值

        使用中等分数60而非0,避免单个分析器失败拉低整体评分
        """
        return {
            "style_tags": [],
            "language_score": 60,  # 使用中等分数
            "description_score": 60,  # 使用中等分数
            "dialogue_score": 60,  # 使用中等分数
            "readability_score": 60,  # 使用中等分数
            "analysis": "分析过程出错,请重试",
            "issues": [],
            "strengths": []
        }
