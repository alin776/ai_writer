"""
Context 配置集中管理

将常用阈值 / 超时集中在此，避免在各处硬编码。
"""


class ContextConfig:
    # Token 硬限制
    HARD_LIMIT_RATIO: float = 0.95          # >95% 触发截断
    TRUNCATE_TARGET_RATIO: float = 0.7      # 截断后目标占比

    # 摘要 / 检索超时（秒）
    SUMMARY_TIMEOUT: int = 8
    LTM_TIMEOUT: int = 6

    # 去重阈值（按消息长度自适应）
    SHORT_MSG_TOKEN_THRESHOLD: int = 50
    MEDIUM_MSG_TOKEN_THRESHOLD: int = 200
    DEDUP_THRESHOLD_SHORT: float = 0.92
    DEDUP_THRESHOLD_MEDIUM: float = 0.85
    DEDUP_THRESHOLD_LONG: float = 0.80

    # thread_id 长度（在 agent 侧同时使用）
    MAX_THREAD_ID_LENGTH: int = 256

    @classmethod
    def dedup_threshold(cls, token_count: int) -> float:
        if token_count < cls.SHORT_MSG_TOKEN_THRESHOLD:
            return cls.DEDUP_THRESHOLD_SHORT
        if token_count < cls.MEDIUM_MSG_TOKEN_THRESHOLD:
            return cls.DEDUP_THRESHOLD_MEDIUM
        return cls.DEDUP_THRESHOLD_LONG
