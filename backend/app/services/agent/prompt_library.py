"""
Prompt Library - Prompt 库管理系统

提供统一的 Prompt 访问、注册、追踪和优化功能
"""

from typing import Dict, List, Optional, Callable
from datetime import datetime
from collections import defaultdict

from .prompts.novel_phases import NovelPhase, SceneType
from .prompts.content_creation_prompts import ContentCreationPrompts
from .prompts.novel_planning_prompts import NovelPlanningPrompts
from .prompts.prompt_optimizer import PromptOptimizer


class PromptLibrary:
    """Prompt 库管理器"""

    def __init__(self):
        """初始化 Prompt 库"""
        self._prompts: Dict[str, Dict[str, str]] = {}
        self._usage_stats: Dict[str, Dict] = defaultdict(lambda: {
            'usage_count': 0,
            'avg_quality': 0.0,
            'total_quality': 0.0,
            'last_used': None
        })

        # 注册内置 Prompts
        self._register_builtin_prompts()

    def _register_builtin_prompts(self):
        """注册所有内置 Prompt"""

        # 注册内容创作 Prompts
        self.register_prompt(
            'content_creation',
            'system',
            ContentCreationPrompts.CONTENT_CREATION_SYSTEM
        )

        # 注册分阶段 Prompts
        for phase in NovelPhase:
            self.register_prompt(
                'content_creation',
                f'phase_{phase.value}',
                ContentCreationPrompts.PHASE_PROMPTS[phase]
            )

        # 注册场景模板 Prompts
        self.register_prompt(
            'content_creation',
            'scene_slap_face',
            ContentCreationPrompts.SLAP_FACE_TEMPLATE
        )
        self.register_prompt(
            'content_creation',
            'scene_upgrade',
            ContentCreationPrompts.UPGRADE_TEMPLATE
        )
        self.register_prompt(
            'content_creation',
            'scene_battle',
            ContentCreationPrompts.BATTLE_TEMPLATE
        )

        # 注册规划类 Prompts
        planning_types = {
            'theme': NovelPlanningPrompts.THEME_ANALYSIS,
            'world': NovelPlanningPrompts.WORLD_SETTING,
            'character': NovelPlanningPrompts.CHARACTER_DESIGN,
            'outline': NovelPlanningPrompts.STORY_OUTLINE,
            'synopsis': NovelPlanningPrompts.CHAPTER_SYNOPSIS,
            'tone': NovelPlanningPrompts.TONE_STYLE,
            'title': NovelPlanningPrompts.TITLE_GENERATION
        }

        for name, prompt in planning_types.items():
            self.register_prompt('planning', name, prompt)

    def register_prompt(
        self,
        category: str,
        subcategory: str,
        template: str
    ) -> bool:
        """
        注册一个 Prompt 模板

        Args:
            category: 类别 ('content_creation', 'planning', 'custom')
            subcategory: 子类别
            template: Prompt 模板内容

        Returns:
            注册是否成功
        """
        if category not in self._prompts:
            self._prompts[category] = {}

        self._prompts[category][subcategory] = template
        return True

    def get_prompt(
        self,
        category: str,
        subcategory: str,
        **kwargs
    ) -> Optional[str]:
        """
        获取 Prompt 模板

        Args:
            category: 类别
            subcategory: 子类别
            **kwargs: 可选的格式化参数

        Returns:
            Prompt 文本,如果不存在返回 None
        """
        prompt = self._prompts.get(category, {}).get(subcategory)

        if prompt and kwargs:
            try:
                prompt = prompt.format(**kwargs)
            except KeyError:
                pass  # 如果格式化失败,返回原始 Prompt

        # 记录使用
        prompt_id = f"{category}.{subcategory}"
        self._usage_stats[prompt_id]['usage_count'] += 1
        self._usage_stats[prompt_id]['last_used'] = datetime.now()

        return prompt

    def list_available_prompts(self, category: Optional[str] = None) -> Dict:
        """
        列出所有可用的 Prompt

        Args:
            category: 如果指定,只列出该类别的 Prompts

        Returns:
            Prompt 列表字典
        """
        if category:
            return {category: list(self._prompts.get(category, {}).keys())}

        return {
            cat: list(subs.keys())
            for cat, subs in self._prompts.items()
        }

    def track_prompt_usage(
        self,
        prompt_id: str,
        result_quality: float
    ):
        """
        追踪 Prompt 使用效果

        Args:
            prompt_id: Prompt 标识 (category.subcategory)
            result_quality: 结果质量评分 (0-10)
        """
        stats = self._usage_stats[prompt_id]
        stats['total_quality'] += result_quality
        stats['avg_quality'] = stats['total_quality'] / stats['usage_count']

    def get_usage_stats(self, prompt_id: Optional[str] = None) -> Dict:
        """
        获取 Prompt 使用统计

        Args:
            prompt_id: Prompt 标识,如果为 None 则返回所有统计

        Returns:
            使用统计字典
        """
        if prompt_id:
            return self._usage_stats.get(prompt_id, {})

        return dict(self._usage_stats)

    def get_best_prompts(self, category: str, top_n: int = 5) -> List[Dict]:
        """
        获取效果最好的 Prompts

        Args:
            category: 类别
            top_n: 返回前 N 个

        Returns:
            最佳 Prompts 列表
        """
        category_prompts = []

        for prompt_id, stats in self._usage_stats.items():
            if prompt_id.startswith(f"{category}.") and stats['usage_count'] > 0:
                category_prompts.append({
                    'prompt_id': prompt_id,
                    'avg_quality': stats['avg_quality'],
                    'usage_count': stats['usage_count']
                })

        # 按平均质量排序
        category_prompts.sort(key=lambda x: x['avg_quality'], reverse=True)
        return category_prompts[:top_n]

    # ==================== 便捷方法 ====================

    def get_content_creation_prompt(
        self,
        phase: Optional[NovelPhase] = None,
        scene_type: Optional[str] = None,
        user_preferences: Optional[Dict] = None,
        context: Optional[Dict] = None
    ) -> str:
        """
        获取内容创作 Prompt(组合多个 Prompt)

        Args:
            phase: 网文阶段
            scene_type: 场景类型
            user_preferences: 用户偏好
            context: 上下文

        Returns:
            组合后的 Prompt
        """
        # 系统 Prompt
        system_prompt = self.get_prompt('content_creation', 'system')

        # 阶段 Prompt
        phase_prompt = ""
        if phase:
            phase_prompt = self.get_prompt('content_creation', f'phase_{phase.value}')

        # 场景 Prompt
        scene_prompt = ""
        if scene_type:
            scene_prompt = self.get_prompt('content_creation', f'scene_{scene_type}')

        # 组合 Prompts
        combined = PromptOptimizer.combine_prompts(
            system_prompt,
            phase_prompt if phase_prompt else "",
            scene_prompt=scene_prompt if scene_prompt else None
        )

        # 添加用户偏好
        if user_preferences:
            combined = PromptOptimizer.add_user_preferences(combined, user_preferences)

        # 添加上下文
        if context:
            combined = PromptOptimizer.add_context(combined, context)

        return combined

    def get_planning_prompt(
        self,
        planning_type: str,
        **kwargs
    ) -> str:
        """
        获取规划类 Prompt

        Args:
            planning_type: 规划类型
                - 'theme': 主题分析
                - 'world': 世界观构建
                - 'character': 角色设计
                - 'outline': 故事大纲
                - 'synopsis': 章节梗概
                - 'tone': 基调风格
                - 'title': 标题生成
            **kwargs: 格式化参数

        Returns:
            Prompt 文本
        """
        return self.get_prompt('planning', planning_type, **kwargs)

    def create_custom_prompt(
        self,
        base_prompt: str,
        enhancements: Optional[List[Callable]] = None
    ) -> str:
        """
        创建自定义 Prompt(应用多个增强函数)

        Args:
            base_prompt: 基础 Prompt
            enhancements: 增强函数列表

        Returns:
            增强后的 Prompt
        """
        prompt = base_prompt

        if enhancements:
            for enhance_func in enhancements:
                prompt = enhance_func(prompt)

        return prompt

    def export_prompts(self, category: Optional[str] = None) -> Dict:
        """
        导出 Prompts(用于备份或分享)

        Args:
            category: 如果指定,只导出该类别

        Returns:
            Prompts 字典
        """
        if category:
            return {category: self._prompts.get(category, {})}

        return self._prompts.copy()

    def import_prompts(self, prompts_data: Dict) -> int:
        """
        导入 Prompts

        Args:
            prompts_data: Prompts 数据字典

        Returns:
            导入的 Prompt 数量
        """
        count = 0
        for category, subcategories in prompts_data.items():
            for subcategory, template in subcategories.items():
                self.register_prompt(category, subcategory, template)
                count += 1

        return count


# 创建全局 Prompt 库实例
prompt_library = PromptLibrary()


# ==================== 便捷函数 ====================

def get_content_prompt(
    phase: Optional[NovelPhase] = None,
    scene_type: Optional[str] = None,
    **kwargs
) -> str:
    """
    快速获取内容创作 Prompt

    Args:
        phase: 网文阶段
        scene_type: 场景类型
        **kwargs: 其他参数

    Returns:
        Prompt 文本
    """
    return prompt_library.get_content_creation_prompt(
        phase=phase,
        scene_type=scene_type,
        **kwargs
    )


def get_planning_prompt(planning_type: str, **kwargs) -> str:
    """
    快速获取规划 Prompt

    Args:
        planning_type: 规划类型
        **kwargs: 格式化参数

    Returns:
        Prompt 文本
    """
    return prompt_library.get_planning_prompt(planning_type, **kwargs)
