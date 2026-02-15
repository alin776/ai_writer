"""
AI去痕迹功能配置管理

集中管理所有配置参数,便于调优和维护
"""

from dataclasses import dataclass, field
from typing import Dict, Literal


@dataclass
class HumanizeConfig:
    """AI去痕迹配置"""

    # ========== 功能开关 ==========
    enable_detection: bool = True  # 是否启用检测阶段
    enable_verification: bool = False  # 是否启用验证阶段 (默认关闭,节省时间)
    enable_cache: bool = True  # 是否启用缓存
    enable_nlp_preprocessing: bool = True  # 是否启用NLP预处理 (V2新增)

    # ========== 输入限制（安全） ==========
    max_text_chars: int = 5000  # 最大字符数（5000字符）
    max_text_bytes: int = 200 * 1024  # 最大字节数（200KB），防止超大UTF-8字符攻击

    # ========== 模型配置 ==========
    # 注意: 当前使用HTTPAIService统一管理模型,这里保留配置选项供未来扩展
    detection_model: str = "default"  # 检测模型 (可以用小模型)
    rewrite_model: str = "default"  # 改写模型 (用大模型保证质量)
    verification_model: str = "default"  # 验证模型 (可以用小模型)

    # ========== 温度参数 ==========
    detection_temperature: float = 0.3  # 检测温度 (低温度保证稳定)
    rewrite_temperature: Dict[str, float] = field(
        default_factory=lambda: {
            "light": 0.5,  # 轻度改写:保守一些
            "medium": 0.8,  # 中度改写:提高创造性，增强去痕迹效果
            "strong": 1.0,  # 强度改写:最大变化，彻底改写风格
        }
    )
    verification_temperature: float = 0.3  # 验证温度 (低温度保证稳定)

    # ========== Token限制 ==========
    detection_max_tokens: int = 1500  # 检测最大token
    verification_max_tokens: int = 500  # 验证最大token

    def get_rewrite_max_tokens(self, text_length: int) -> int:
        """
        根据原文长度动态计算改写的最大token数

        Args:
            text_length: 原文长度(字符数)

        Returns:
            最大token数
        """
        # 经验公式: 改写后文本长度约为原文的1.2-2倍
        # 1个中文字符约等于1.5个token
        estimated_tokens = int(text_length * 1.5 * 2)

        # 设置上下限
        min_tokens = 500
        max_tokens = 4000

        return max(min_tokens, min(estimated_tokens, max_tokens))

    # ========== 阈值配置 ==========
    detection_threshold: float = 60.0  # AI痕迹分数阈值,低于此值无需去痕迹

    # ========== 缓存配置 ==========
    cache_ttl: int = 3600  # 缓存有效期(秒) - 1小时
    cache_similarity_threshold: float = 0.95  # 相似度阈值(用于缓存匹配)

    # ========== 性能配置 ==========
    enable_parallel_detection: bool = False  # 是否并行检测(实验性)
    timeout_seconds: int = 30  # 单次AI调用超时时间

    # ========== 监控配置 ==========
    enable_metrics: bool = True  # 是否启用性能指标记录
    log_level: str = "INFO"  # 日志级别

    def get_rewrite_temperature(
        self, intensity: Literal["light", "medium", "strong"]
    ) -> float:
        """获取改写温度"""
        return self.rewrite_temperature.get(intensity, 0.7)

    def should_skip_detection(self, text_length: int) -> bool:
        """
        判断是否应该跳过检测阶段

        对于极短文本,可能不需要检测直接改写

        Args:
            text_length: 文本长度

        Returns:
            是否跳过检测
        """
        # 文本太短(<50字)可以跳过检测
        if text_length < 50:
            return True

        return False


# 默认配置实例 (用于快速获取默认值)
# 注意: 这是一个全局单例,多个Service实例会共享此配置
# 如果需要自定义配置,请创建新的HumanizeConfig实例传递给Service
_default_config = HumanizeConfig()


def get_config() -> HumanizeConfig:
    """
    获取默认配置的新副本

    每次调用返回新的配置实例,避免并发修改问题。
    如果需要共享配置,请手动传递配置实例。

    Returns:
        HumanizeConfig: 新的配置实例

    Example:
        >>> # 每次获取新实例,互不影响
        >>> config1 = get_config()
        >>> config2 = get_config()
        >>> config1.enable_verification = True
        >>> assert config2.enable_verification == False  # config2不受影响
    """
    # 返回新实例,避免并发问题
    return HumanizeConfig()


def get_shared_config() -> HumanizeConfig:
    """
    获取共享的默认配置实例

    警告: 返回全局单例,所有调用者共享同一个配置对象。
    请勿修改此配置,仅用于读取默认值。

    Returns:
        HumanizeConfig: 共享的配置实例
    """
    return _default_config
