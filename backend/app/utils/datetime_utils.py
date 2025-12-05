"""
日期时间工具函数

提供统一的timezone-aware datetime处理，避免naive和aware datetime混用导致的问题
"""
from datetime import datetime, timezone
from typing import Optional


def get_utc_now() -> datetime:
    """
    获取当前UTC时间（timezone-aware）

    替代 datetime.now()，确保返回的datetime对象包含时区信息

    Returns:
        timezone-aware datetime对象（UTC时区）

    Example:
        >>> now = get_utc_now()
        >>> now.tzinfo  # datetime.timezone.utc
    """
    return datetime.now(timezone.utc)


def make_aware(dt: datetime, tz: Optional[timezone] = None) -> datetime:
    """
    将naive datetime转换为aware datetime

    Args:
        dt: datetime对象
        tz: 时区，默认UTC

    Returns:
        timezone-aware datetime对象

    Example:
        >>> naive_dt = datetime(2025, 12, 3, 10, 0, 0)
        >>> aware_dt = make_aware(naive_dt)
        >>> aware_dt.tzinfo  # datetime.timezone.utc
    """
    if dt.tzinfo is not None:
        return dt
    return dt.replace(tzinfo=tz or timezone.utc)


def is_aware(dt: datetime) -> bool:
    """
    检查datetime对象是否是timezone-aware

    Args:
        dt: datetime对象

    Returns:
        True如果是aware，False如果是naive
    """
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


def compare_datetime_safe(dt1: datetime, dt2: datetime) -> int:
    """
    安全地比较两个datetime对象

    自动处理naive和aware datetime的转换

    Args:
        dt1: 第一个datetime对象
        dt2: 第二个datetime对象

    Returns:
        -1: dt1 < dt2
         0: dt1 == dt2
         1: dt1 > dt2

    Example:
        >>> dt1 = datetime.now()  # naive
        >>> dt2 = get_utc_now()   # aware
        >>> result = compare_datetime_safe(dt1, dt2)  # 自动转换，不会抛异常
    """
    dt1_aware = make_aware(dt1) if not is_aware(dt1) else dt1
    dt2_aware = make_aware(dt2) if not is_aware(dt2) else dt2

    if dt1_aware < dt2_aware:
        return -1
    elif dt1_aware > dt2_aware:
        return 1
    return 0
