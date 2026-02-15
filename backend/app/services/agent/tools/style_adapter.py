"""
风格自适应 - 根据章节现有风格推荐改写风格
"""
from typing import List


class StyleAdapter:
    """根据章节现有风格推荐改写风格"""

    # 风格特征词
    STYLE_FEATURES = {
        "formal": ["然而", "因此", "此外", "综上所述", "显而易见", "由此可见", "换言之"],
        "casual": ["其实", "反正", "不过", "话说", "简直", "居然", "竟然"],
        "poetic": ["宛如", "仿佛", "恰似", "犹如", "如同", "宛若", "好似"],
        "suspense": ["突然", "竟然", "居然", "不料", "岂料", "没想到", "谁知"],
        "humorous": ["哈哈", "嘿嘿", "竟敢", "偏偏", "倒是", "得了", "好嘛"]
    }

    # 风格中文名称
    STYLE_NAMES = {
        "formal": "正式风格",
        "casual": "口语风格",
        "poetic": "诗意风格",
        "suspense": "悬疑风格",
        "humorous": "幽默风格",
        "neutral": "中性风格"
    }

    def analyze_style(self, content: str) -> dict:
        """
        分析文本风格特征

        Returns:
            {
                "primary_style": str,
                "style_scores": dict,
                "features": list
            }
        """
        style_scores = {}
        found_features = []

        for style, features in self.STYLE_FEATURES.items():
            score = 0
            for feature in features:
                count = content.count(feature)
                if count > 0:
                    score += count
                    found_features.append({
                        "style": style,
                        "feature": feature,
                        "count": count
                    })

            style_scores[style] = score

        # 找出主要风格
        primary_style = "neutral"
        if any(style_scores.values()):
            primary_style = max(style_scores, key=style_scores.get)

        return {
            "primary_style": primary_style,
            "style_scores": style_scores,
            "features": found_features
        }

    def recommend_styles(self, content: str, num_recommendations: int = 3) -> List[dict]:
        """
        根据内容风格推荐改写风格

        Returns:
            [
                {"style": "formal", "style_name": "正式风格", "reason": "..."},
                ...
            ]
        """
        analysis = self.analyze_style(content)
        primary = analysis["primary_style"]

        # 推荐策略：相似风格 + 对比风格 + 其他风格
        recommendations = []

        # 1. 相似风格（保持当前风格）
        if primary != "neutral":
            recommendations.append({
                "style": primary,
                "style_name": self._get_style_name(primary),
                "reason": f"保持当前{self._get_style_name(primary)}"
            })

        # 2. 对比风格
        contrast_map = {
            "formal": "casual",
            "casual": "formal",
            "poetic": "casual",
            "suspense": "humorous",
            "humorous": "suspense",
            "neutral": "formal"
        }

        if primary in contrast_map:
            contrast = contrast_map[primary]
            if contrast not in [r["style"] for r in recommendations]:
                recommendations.append({
                    "style": contrast,
                    "style_name": self._get_style_name(contrast),
                    "reason": f"对比风格：{self._get_style_name(contrast)}"
                })

        # 3. 补充其他风格
        all_styles = list(self.STYLE_FEATURES.keys())
        for style in all_styles:
            if len(recommendations) >= num_recommendations:
                break
            if style not in [r["style"] for r in recommendations]:
                recommendations.append({
                    "style": style,
                    "style_name": self._get_style_name(style),
                    "reason": f"尝试{self._get_style_name(style)}"
                })

        return recommendations[:num_recommendations]

    def get_style_prompt(self, style: str) -> str:
        """
        获取特定风格的改写提示词

        Args:
            style: 风格标识符

        Returns:
            用于AI改写的提示词
        """
        prompts = {
            "formal": "请使用正式、规范的书面语言改写，措辞严谨，逻辑清晰，避免口语化表达。",
            "casual": "请使用轻松、自然的口语风格改写，语言亲切随意，如同日常对话。",
            "poetic": "请使用富有诗意的语言改写，运用比喻、拟人等修辞手法，营造优美的意境。",
            "suspense": "请使用制造悬念的手法改写，设置疑问，控制节奏，增强紧张感。",
            "humorous": "请使用幽默诙谐的语言改写，适当添加俏皮话或有趣的比喻，增加趣味性。"
        }
        return prompts.get(style, "请保持原有风格进行改写。")

    def _get_style_name(self, style: str) -> str:
        """获取风格的中文名称"""
        return self.STYLE_NAMES.get(style, style)


# 单例实例
style_adapter = StyleAdapter()
