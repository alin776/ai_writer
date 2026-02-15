"""
Agent 绯荤粺閰嶇疆绠＄悊

鎻愪緵缁熶竴鐨勯厤缃鐞嗭紝鏀寔鐜鍙橀噺銆侀厤缃枃浠跺拰榛樿鍊笺€?
"""

import os
from typing import Dict, Any, Optional, List
from pydantic import Field, ConfigDict
from pathlib import Path

# 灏濊瘯浠?pydantic-settings 瀵煎叆锛屽鏋滀笉鍙敤鍒欎娇鐢?pydantic
try:
    from pydantic_settings import BaseSettings
except ImportError:
    # 闄嶇骇浣跨敤 pydantic v2 鍏煎鏂瑰紡
    from pydantic import BaseModel as BaseSettings


class AgentConfig(BaseSettings):
    """
    Agent 绯荤粺閰嶇疆绫?

    鏀寔浠庣幆澧冨彉閲忋€?env鏂囦欢鍜岄粯璁ゅ€煎姞杞介厤缃?
    """

    # ==================== 妯″瀷閰嶇疆 ====================

    # 榛樿妯″瀷
    DEFAULT_MODEL: str = Field(
        default="gemini-2.5-flash",
        description="榛樿浣跨敤鐨凙I妯″瀷"
    )

    FALLBACK_MODEL: str = Field(
        default="gemini-2.5-flash-lite",
        description="闄嶇骇浣跨敤鐨凙I妯″瀷"
    )

    # 妯″瀷閫夋嫨鍣ㄩ厤缃?
    ENABLE_MODEL_SELECTOR: bool = Field(
        default=True,
        description="鏄惁鍚敤鏅鸿兘妯″瀷閫夋嫨鍣?"
    )

    ENABLE_COST_TRACKING: bool = Field(
        default=True,
        description="鏄惁鍚敤鎴愭湰杩借釜"
    )

    # ==================== 鎬ц兘閰嶇疆 ====================

    # 骞跺彂鎺у埗
    MAX_CONCURRENT_ACTIONS: int = Field(
        default=5,
        ge=1,
        le=20,
        description="鏈€澶у苟鍙慉ction鏁伴噺"
    )

    MAX_CONCURRENT_TOOLS: int = Field(
        default=3,
        ge=1,
        le=10,
        description="鏈€澶у苟鍙戝伐鍏疯皟鐢ㄦ暟閲?"
    )

    # 瓒呮椂閰嶇疆
    ACTION_TIMEOUT: int = Field(
        default=300,
        ge=30,
        le=600,
        description="Action鎵ц瓒呮椂鏃堕棿锛堢锛?"
    )

    TOOL_TIMEOUT: int = Field(
        default=60,
        ge=10,
        le=300,
        description="宸ュ叿璋冪敤瓒呮椂鏃堕棿锛堢锛?"
    )

    LLM_TIMEOUT: int = Field(
        default=120,
        ge=30,
        le=300,
        description="LLM璋冪敤瓒呮椂鏃堕棿锛堢锛?"
    )

    # ==================== 缂撳瓨閰嶇疆 ====================

    # Memory绯荤粺
    MEMORY_SHORT_TERM_SIZE: int = Field(
        default=10,
        ge=5,
        le=50,
        description="鐭湡璁板繂鏈€澶ф潯鏁?"
    )

    MEMORY_MEDIUM_TERM_SIZE: int = Field(
        default=100,
        ge=50,
        le=500,
        description="涓湡璁板繂鏈€澶ф潯鏁?"
    )

    MEMORY_CACHE_SIZE: int = Field(
        default=1000,
        ge=100,
        le=10000,
        description="鍐呭瓨缂撳瓨澶у皬"
    )

    MEMORY_FORGET_THRESHOLD: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="璁板繂閬楀繕闃堝€?"
    )

    # Redis閰嶇疆
    REDIS_TTL: int = Field(
        default=3600,
        ge=60,
        le=86400,
        description="Redis缂撳瓨TTL锛堢锛?"
    )

    REDIS_CONNECTION_POOL_SIZE: int = Field(
        default=20,
        ge=5,
        le=50,
        description="Redis杩炴帴姹犲ぇ灏?"
    )

    # ==================== 璐ㄩ噺鎺у埗閰嶇疆 ====================

    # 璐ㄩ噺璇勪及
    QUALITY_THRESHOLD: float = Field(
        default=8.0,
        ge=1.0,
        le=10.0,
        description="鍐呭璐ㄩ噺闃堝€?"
    )

    MAX_QUALITY_RETRIES: int = Field(
        default=3,
        ge=1,
        le=5,
        description="璐ㄩ噺寰幆鏈€澶ч噸璇曟鏁?"
    )

    ENABLE_QUALITY_CACHE: bool = Field(
        default=True,
        description="鏄惁鍚敤璐ㄩ噺璇勪及缂撳瓨"
    )

    # ==================== 閿欒澶勭悊閰嶇疆 ====================

    # 閲嶈瘯閰嶇疆
    DEFAULT_MAX_RETRIES: int = Field(
        default=3,
        ge=1,
        le=10,
        description="榛樿鏈€澶ч噸璇曟鏁?"
    )

    DEFAULT_RETRY_DELAY: float = Field(
        default=1.0,
        ge=0.1,
        le=10.0,
        description="榛樿閲嶈瘯寤惰繜锛堢锛?"
    )

    # 鐔旀柇鍣ㄩ厤缃?
    CIRCUIT_BREAKER_THRESHOLD: int = Field(
        default=5,
        ge=1,
        le=20,
        description="鐔旀柇鍣ㄥけ璐ラ槇鍊?"
    )

    CIRCUIT_BREAKER_TIMEOUT: float = Field(
        default=60.0,
        ge=10.0,
        le=300.0,
        description="鐔旀柇鍣ㄦ仮澶嶈秴鏃讹紙绉掞級"
    )

    # ==================== 鏃ュ織閰嶇疆 ====================

    LOG_LEVEL: str = Field(
        default="INFO",
        description="鏃ュ織绾у埆"
    )

    LOG_FORMAT: str = Field(
        default="json",
        description="鏃ュ織鏍煎紡 (json/text)"
    )

    ENABLE_STRUCTURED_LOGGING: bool = Field(
        default=True,
        description="鏄惁鍚敤缁撴瀯鍖栨棩蹇?"
    )

    # ==================== 鐩戞帶閰嶇疆 ====================

    # 鎬ц兘鐩戞帶
    ENABLE_PERFORMANCE_MONITORING: bool = Field(
        default=True,
        description="鏄惁鍚敤鎬ц兘鐩戞帶"
    )

    SLOW_QUERY_THRESHOLD: float = Field(
        default=10.0,
        ge=1.0,
        le=60.0,
        description="鎱㈡煡璇㈤槇鍊硷紙绉掞級"
    )

    # 鎴愭湰鐩戞帶
    COST_ALERT_THRESHOLD: float = Field(
        default=10.0,
        ge=1.0,
        description="鎴愭湰鍛婅闃堝€硷紙缇庡厓锛?"
    )

    DAILY_COST_LIMIT: float = Field(
        default=50.0,
        ge=0.0,
        description="姣忔棩鎴愭湰闄愬埗锛堢編鍏冿級"
    )

    # ==================== 瀹夊叏閰嶇疆 ====================

    # 鏁版嵁淇濇姢
    ENABLE_DATA_ENCRYPTION: bool = Field(
        default=False,
        description="鏄惁鍚敤鏁版嵁鍔犲瘑"
    )

    MAX_CONTENT_LENGTH: int = Field(
        default=10000,
        ge=1000,
        le=100000,
        description="鏈€澶у唴瀹归暱搴︼紙瀛楃锛?"
    )

    # ==================== 瀹為獙鎬у姛鑳?====================

    ENABLE_EXPERIMENTAL_FEATURES: bool = Field(
        default=False,
        description="鏄惁鍚敤瀹為獙鎬у姛鑳?"
    )

    ENABLE_ADVANCED_CACHING: bool = Field(
        default=False,
        description="鏄惁鍚敤楂樼骇缂撳瓨绛栫暐"
    )

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    @classmethod
    def from_env(cls, **overrides) -> "AgentConfig":
        """Create config from environment overrides."""
        return cls(**overrides)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return self.dict()

    def validate_config(self) -> List[str]:
        """
        楠岃瘉閰嶇疆鐨勬湁鏁堟€?

        Returns:
            List[str]: 楠岃瘉閿欒鍒楄〃锛岀┖鍒楄〃琛ㄧず楠岃瘉閫氳繃
        """
        errors = []

        # 楠岃瘉闃堝€奸€昏緫
        if self.QUALITY_THRESHOLD < 1.0 or self.QUALITY_THRESHOLD > 10.0:
            errors.append("QUALITY_THRESHOLD 蹇呴』鍦?1.0-10.0 涔嬮棿")

        if self.MEMORY_FORGET_THRESHOLD < 0.0 or self.MEMORY_FORGET_THRESHOLD > 1.0:
            errors.append("MEMORY_FORGET_THRESHOLD 蹇呴』鍦?0.0-1.0 涔嬮棿")

        # 楠岃瘉瓒呮椂閰嶇疆
        if self.TOOL_TIMEOUT >= self.ACTION_TIMEOUT:
            errors.append("TOOL_TIMEOUT 搴旇灏忎簬 ACTION_TIMEOUT")

        # 楠岃瘉骞跺彂閰嶇疆
        if self.MAX_CONCURRENT_TOOLS > self.MAX_CONCURRENT_ACTIONS:
            errors.append("MAX_CONCURRENT_TOOLS 涓嶅簲璇ヨ秴杩?MAX_CONCURRENT_ACTIONS")

        return errors

    def get_model_config(self, complexity: str = "medium") -> Dict[str, Any]:
        """
        鏍规嵁澶嶆潅搴﹁幏鍙栨ā鍨嬮厤缃?

        Args:
            complexity: 浠诲姟澶嶆潅搴?(simple/medium/complex)

        Returns:
            Dict[str, Any]: 妯″瀷閰嶇疆
        """
        model_configs = {
            "simple": {
                "model": self.FALLBACK_MODEL,
                "temperature": 0.1,
                "max_tokens": 1000
            },
            "medium": {
                "model": self.DEFAULT_MODEL,
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "complex": {
                "model": "gemini-2.5-pro",
                "temperature": 0.8,
                "max_tokens": 4000
            }
        }

        return model_configs.get(complexity, model_configs["medium"])

    def get_cache_config(self) -> Dict[str, Any]:
        """鑾峰彇缂撳瓨閰嶇疆"""
        return {
            "memory_cache_size": self.MEMORY_CACHE_SIZE,
            "redis_ttl": self.REDIS_TTL,
            "connection_pool_size": self.REDIS_CONNECTION_POOL_SIZE,
            "enable_quality_cache": self.ENABLE_QUALITY_CACHE
        }

    def get_timeout_config(self) -> Dict[str, Any]:
        """鑾峰彇瓒呮椂閰嶇疆"""
        return {
            "action_timeout": self.ACTION_TIMEOUT,
            "tool_timeout": self.TOOL_TIMEOUT,
            "llm_timeout": self.LLM_TIMEOUT
        }

    def get_monitoring_config(self) -> Dict[str, Any]:
        """鑾峰彇鐩戞帶閰嶇疆"""
        return {
            "enable_performance_monitoring": self.ENABLE_PERFORMANCE_MONITORING,
            "slow_query_threshold": self.SLOW_QUERY_THRESHOLD,
            "cost_alert_threshold": self.COST_ALERT_THRESHOLD,
            "daily_cost_limit": self.DAILY_COST_LIMIT
        }


# 鍏ㄥ眬閰嶇疆瀹炰緥
config = AgentConfig()


def get_config() -> AgentConfig:
    """鑾峰彇鍏ㄥ眬閰嶇疆瀹炰緥"""
    return config


def reload_config(**overrides) -> AgentConfig:
    """
    閲嶆柊鍔犺浇閰嶇疆

    Args:
        **overrides: 閰嶇疆瑕嗙洊鍊?

    Returns:
        AgentConfig: 鏂扮殑閰嶇疆瀹炰緥
    """
    global config
    config = AgentConfig.from_env(**overrides)

    # 楠岃瘉閰嶇疆
    errors = config.validate_config()
    if errors:
        raise ValueError(f"閰嶇疆楠岃瘉澶辫触: {', '.join(errors)}")

    return config


def load_config_from_file(config_path: Path) -> AgentConfig:
    """
    浠庢枃浠跺姞杞介厤缃?

    Args:
        config_path: 閰嶇疆鏂囦欢璺緞

    Returns:
        AgentConfig: 閰嶇疆瀹炰緥
    """
    if not config_path.exists():
        raise FileNotFoundError(f"閰嶇疆鏂囦欢涓嶅瓨鍦? {config_path}")

    # 杩欓噷鍙互娣诲姞 YAML/JSON 閰嶇疆鏂囦欢瑙ｆ瀽閫昏緫
    # 鏆傛椂鍙敮鎸佺幆澧冨彉閲?

    return AgentConfig()


# 瀵煎嚭閰嶇疆甯搁噺
DEFAULT_CONFIG = config.to_dict()


