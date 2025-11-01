"""
Prompt 优化器

提供 Prompt 的动态组合、优化和增强功能
"""

from typing import Dict, List, Optional


class PromptOptimizer:
    """Prompt 优化和组合工具"""

    @staticmethod
    def add_user_preferences(base_prompt: str, user_preferences: Dict) -> str:
        """
        在基础 Prompt 中添加用户偏好

        Args:
            base_prompt: 基础 Prompt
            user_preferences: 用户偏好字典
                - style: 写作风格偏好
                - focus: 重点关注内容
                - avoid: 避免的元素
                - special_requirements: 特殊要求

        Returns:
            增强后的 Prompt
        """
        enhanced_prompt = base_prompt

        # 添加用户偏好部分
        if user_preferences:
            enhanced_prompt += "\n\n---\n\n【用户偏好设置】\n"

            # 风格偏好
            if 'style' in user_preferences:
                enhanced_prompt += f"- 写作风格: {user_preferences['style']}\n"

            # 重点关注
            if 'focus' in user_preferences:
                focus_items = user_preferences['focus']
                if isinstance(focus_items, list):
                    enhanced_prompt += f"- 重点关注: {', '.join(focus_items)}\n"
                else:
                    enhanced_prompt += f"- 重点关注: {focus_items}\n"

            # 避免元素
            if 'avoid' in user_preferences:
                avoid_items = user_preferences['avoid']
                if isinstance(avoid_items, list):
                    enhanced_prompt += f"- 避免: {', '.join(avoid_items)}\n"
                else:
                    enhanced_prompt += f"- 避免: {avoid_items}\n"

            # 特殊要求
            if 'special_requirements' in user_preferences:
                enhanced_prompt += f"\n特殊要求:\n{user_preferences['special_requirements']}\n"

        return enhanced_prompt

    @staticmethod
    def add_quality_feedback(base_prompt: str, feedback: str) -> str:
        """
        在 Prompt 中添加质量反馈,用于质量循环

        Args:
            base_prompt: 基础 Prompt
            feedback: 质量反馈信息

        Returns:
            包含反馈的 Prompt
        """
        if not feedback:
            return base_prompt

        feedback_section = f"""

---

【上一次生成的反馈】
{feedback}

请根据以上反馈改进本次生成内容,特别注意:
1. 修正上次指出的问题
2. 保持或增强做得好的部分
3. 提升整体质量
"""

        return base_prompt + feedback_section

    @staticmethod
    def add_context(base_prompt: str, context: Dict) -> str:
        """
        在 Prompt 中添加上下文信息

        Args:
            base_prompt: 基础 Prompt
            context: 上下文字典
                - previous_content: 前文内容
                - target_length: 目标字数
                - current_chapter: 当前章节号
                - total_chapters: 总章节数
                - phase: 当前阶段

        Returns:
            包含上下文的 Prompt
        """
        context_prompt = base_prompt

        if context:
            context_prompt += "\n\n---\n\n【上下文信息】\n"

            # 章节信息
            if 'current_chapter' in context and 'total_chapters' in context:
                context_prompt += f"- 当前进度: 第{context['current_chapter']}/{context['total_chapters']}章\n"

            # 目标字数
            if 'target_length' in context:
                context_prompt += f"- 目标字数: {context['target_length']}字\n"

            # 当前阶段
            if 'phase' in context:
                context_prompt += f"- 当前阶段: {context['phase']}\n"

            # 前文内容
            if 'previous_content' in context:
                prev_content = context['previous_content']
                # 限制前文长度,只取最后200字
                if len(prev_content) > 200:
                    prev_content = "..." + prev_content[-200:]
                context_prompt += f"\n前文内容:\n{prev_content}\n"

        return context_prompt

    @staticmethod
    def combine_prompts(
        system_prompt: str,
        phase_prompt: str,
        user_prompt: Optional[str] = None,
        scene_prompt: Optional[str] = None
    ) -> str:
        """
        组合多个 Prompt

        Args:
            system_prompt: 系统级 Prompt
            phase_prompt: 阶段 Prompt
            user_prompt: 用户 Prompt(可选)
            scene_prompt: 场景 Prompt(可选)

        Returns:
            组合后的完整 Prompt
        """
        combined = system_prompt
        combined += "\n\n" + "="*50 + "\n\n"
        combined += phase_prompt

        if scene_prompt:
            combined += "\n\n" + "="*50 + "\n\n"
            combined += scene_prompt

        if user_prompt:
            combined += "\n\n" + "="*50 + "\n\n"
            combined += "【用户指令】\n" + user_prompt

        return combined

    @staticmethod
    def optimize_for_retry(
        original_prompt: str,
        previous_output: str,
        issue_description: str
    ) -> str:
        """
        为重试优化 Prompt

        Args:
            original_prompt: 原始 Prompt
            previous_output: 上一次的输出
            issue_description: 问题描述

        Returns:
            优化后的 Prompt
        """
        retry_prompt = original_prompt

        retry_prompt += f"""

---

【重试说明】
上一次生成的内容存在以下问题:
{issue_description}

上一次的输出片段:
{previous_output[:300]}...

请重新生成,确保:
1. 解决上述问题
2. 提升整体质量
3. 保持内容的新鲜感(不要简单重复)
"""

        return retry_prompt

    @staticmethod
    def extract_key_requirements(prompt: str) -> List[str]:
        """
        从 Prompt 中提取关键要求(用于质量评估)

        Args:
            prompt: Prompt 文本

        Returns:
            关键要求列表
        """
        requirements = []

        # 查找包含 "要求"、"注意"、"确保" 等关键词的行
        keywords = ["要求", "注意", "确保", "必须", "禁止", "避免"]

        for line in prompt.split('\n'):
            line = line.strip()
            if any(keyword in line for keyword in keywords):
                # 去除编号和符号
                cleaned = line.lstrip('- *•123456789. ')
                if cleaned and len(cleaned) > 5:
                    requirements.append(cleaned)

        return requirements

    @staticmethod
    def add_examples(base_prompt: str, examples: List[str]) -> str:
        """
        在 Prompt 中添加示例

        Args:
            base_prompt: 基础 Prompt
            examples: 示例列表

        Returns:
            包含示例的 Prompt
        """
        if not examples:
            return base_prompt

        examples_section = "\n\n---\n\n【参考示例】\n"

        for i, example in enumerate(examples, 1):
            examples_section += f"\n示例{i}:\n{example}\n"

        return base_prompt + examples_section

    @staticmethod
    def adjust_temperature_guidance(
        base_prompt: str,
        creativity_level: str = "medium"
    ) -> str:
        """
        根据创造性需求调整 Prompt 的指导语

        Args:
            base_prompt: 基础 Prompt
            creativity_level: 创造性水平
                - 'low': 低创造性,强调准确和一致性
                - 'medium': 中等创造性
                - 'high': 高创造性,鼓励创新

        Returns:
            调整后的 Prompt
        """
        guidance = {
            'low': """

【创作指导】
- 严格遵循既定设定和规则
- 保持与前文的高度一致性
- 避免过度创新或意外转折
- 注重细节的准确性
""",
            'medium': """

【创作指导】
- 在既定框架内发挥创造力
- 保持与前文的合理一致性
- 可以有适度的创新和转折
- 平衡准确性和新颖性
""",
            'high': """

【创作指导】
- 鼓励大胆的创新和想象
- 可以有出人意料的转折
- 注重情节的震撼性和新颖性
- 在合理范围内自由发挥
"""
        }

        return base_prompt + guidance.get(creativity_level, guidance['medium'])

    @staticmethod
    def create_iterative_prompt(
        base_prompt: str,
        iteration_num: int,
        previous_results: List[str],
        best_aspects: Optional[List[str]] = None
    ) -> str:
        """
        创建迭代式 Prompt(用于多次生成和改进)

        Args:
            base_prompt: 基础 Prompt
            iteration_num: 当前迭代次数
            previous_results: 之前的生成结果
            best_aspects: 之前结果中最好的方面

        Returns:
            迭代 Prompt
        """
        iterative_prompt = base_prompt

        iterative_prompt += f"""

---

【迭代生成 - 第{iteration_num}次】
"""

        if previous_results:
            iterative_prompt += f"\n已经生成了{len(previous_results)}个版本。\n"

        if best_aspects:
            iterative_prompt += "\n之前版本的优点:\n"
            for aspect in best_aspects:
                iterative_prompt += f"- {aspect}\n"
            iterative_prompt += "\n请在本次生成中保持并强化这些优点。\n"

        iterative_prompt += f"""
本次生成要求:
1. 避免与之前版本过于相似
2. 尝试新的角度和表达方式
3. 提升整体质量
4. 保持核心要求不变
"""

        return iterative_prompt
