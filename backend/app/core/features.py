"""
功能开关配置

集中管理所有实验性功能和可选功能的开关
"""

from typing import Dict, Any


class FeatureFlags:
    """功能开关"""

    # Agent相关功能
    ENABLE_REACT_STREAM = True  # ReAct流式模式（新功能）
    ENABLE_PLANNING_MODE = True  # Planning模式（现有功能）

    # 其他功能开关可以在这里添加
    # ENABLE_XXX = False

    @classmethod
    def is_enabled(cls, feature_name: str) -> bool:
        """检查功能是否启用"""
        return getattr(cls, feature_name, False)

    @classmethod
    def get_all_flags(cls) -> Dict[str, Any]:
        """获取所有功能开关状态"""
        return {
            key: value
            for key, value in cls.__dict__.items()
            if key.isupper() and not key.startswith('_')
        }


# 便捷访问
def is_react_stream_enabled() -> bool:
    """检查ReAct流式模式是否启用"""
    return FeatureFlags.ENABLE_REACT_STREAM


def is_planning_mode_enabled() -> bool:
    """检查Planning模式是否启用"""
    return FeatureFlags.ENABLE_PLANNING_MODE
