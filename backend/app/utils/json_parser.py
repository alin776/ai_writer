"""
统一的JSON解析工具

用于解析AI返回的JSON响应,支持多种格式和容错策略:
1. 纯JSON
2. markdown代码块包裹的JSON
3. 前后有额外文本的JSON (如礼貌性回复)
4. 包含中文标点的JSON (自动修复)
5. 格式错误的JSON (使用json-repair自动修复)

使用示例:
    from app.utils.json_parser import parse_ai_json

    ai_response = '''
    好的,这是分析结果:
    ```json
    {"score": 85, "summary": "很好"}
    ```
    '''

    result = parse_ai_json(ai_response)
    # result = {"score": 85, "summary": "很好"}
"""

import json
import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def parse_ai_json(
    response: str,
    fallback_value: Optional[Dict[str, Any]] = None,
    log_prefix: str = ""
) -> Dict[str, Any]:
    """
    解析AI返回的JSON响应

    支持多种格式和容错策略,自动处理各种边缘情况。

    Args:
        response: AI返回的原始响应文本
        fallback_value: 解析失败时的兜底值 (默认返回{"error": "解析失败", ...})
        log_prefix: 日志前缀,用于区分不同的调用场景

    Returns:
        解析后的字典对象

    Raises:
        ValueError: 如果所有解析方法都失败且没有提供fallback_value

    Examples:
        >>> # 纯JSON
        >>> parse_ai_json('{"name": "test"}')
        {'name': 'test'}

        >>> # Markdown包裹
        >>> parse_ai_json('```json\\n{"name": "test"}\\n```')
        {'name': 'test'}

        >>> # 带前导文本
        >>> parse_ai_json('好的,这是结果:\\n{"name": "test"}')
        {'name': 'test'}

        >>> # 中文标点
        >>> parse_ai_json('{"name"："测试"}')  # 中文冒号
        {'name': '测试'}
    """
    prefix = f"[{log_prefix}] " if log_prefix else ""

    logger.info(f"{prefix}🔍 开始解析AI响应, 长度={len(response)}")
    logger.debug(f"{prefix}📝 原始响应前500字符: {response[:500]}")

    # 步骤1: 预处理 - 替换中文标点符号
    cleaned_response = _normalize_chinese_punctuation(response)
    if cleaned_response != response:
        logger.info(f"{prefix}✅ 预处理: 已替换中文标点符号")
        logger.debug(f"{prefix}📝 替换后前500字符: {cleaned_response[:500]}")

    # 步骤2: 尝试直接解析
    result = _try_parse_direct(cleaned_response, prefix)
    if result is not None:
        return result

    # 步骤3: 提取markdown代码块
    result = _try_parse_markdown(cleaned_response, prefix)
    if result is not None:
        return result

    # 步骤4: 提取花括号内容
    result = _try_parse_braces(cleaned_response, prefix)
    if result is not None:
        return result

    # 步骤5: 使用json-repair修复花括号内容
    result = _try_repair_extracted(cleaned_response, prefix)
    if result is not None:
        return result

    # 步骤6: 对整个响应使用json-repair
    result = _try_repair_full(cleaned_response, prefix)
    if result is not None:
        return result

    # 所有方法都失败
    logger.error(f"{prefix}❌ 所有解析方法都失败 (包括json-repair)")
    logger.error(f"{prefix}📝 完整响应内容:\n{response}")

    # 返回兜底值或抛出异常
    if fallback_value is not None:
        logger.warning(f"{prefix}⚠️ 使用兜底值: {fallback_value}")
        return fallback_value

    # 返回默认的错误对象
    error_obj = {
        "error": "解析失败",
        "raw_response": response[:500]
    }
    logger.warning(f"{prefix}⚠️ 返回错误对象: {error_obj}")
    return error_obj


def _normalize_chinese_punctuation(text: str) -> str:
    """
    替换中文标点符号为英文标点

    常见的中文标点:
    - " " → " " (双引号)
    - ' ' → ' ' (单引号)
    - ： → : (冒号)
    - ， → , (逗号,保守处理)
    """
    text = text.replace('"', '"').replace('"', '"')  # 中文双引号
    text = text.replace(''', "'").replace(''', "'")  # 中文单引号
    text = text.replace('：', ':')  # 中文冒号
    # 注意: 逗号不全局替换,因为可能在字符串值中
    return text


def _try_parse_direct(text: str, prefix: str = "") -> Optional[Dict[str, Any]]:
    """尝试直接解析JSON"""
    try:
        data = json.loads(text)
        logger.info(f"{prefix}✅ 方法1成功: 直接解析JSON")
        return data
    except json.JSONDecodeError as e:
        logger.debug(f"{prefix}❌ 方法1失败: 直接解析 - {e}")
        return None


def _try_parse_markdown(text: str, prefix: str = "") -> Optional[Dict[str, Any]]:
    """尝试提取markdown代码块中的JSON"""
    # 匹配 ```json 或 ``` 包裹的内容
    # 修复: 支持没有换行符的情况
    pattern = r'```(?:json)?\s*(.*?)\s*```'
    match = re.search(pattern, text, re.DOTALL)

    if match:
        extracted = match.group(1).strip()
        logger.info(f"{prefix}🔍 方法2: 从markdown代码块提取JSON, 长度={len(extracted)}")

        try:
            data = json.loads(extracted)
            logger.info(f"{prefix}✅ 方法2成功: markdown代码块解析")
            return data
        except json.JSONDecodeError as e:
            logger.debug(f"{prefix}❌ 方法2失败: markdown解析 - {e}")
    else:
        logger.debug(f"{prefix}❌ 方法2失败: 未找到markdown代码块")

    return None


def _extract_first_json_object(text: str) -> Optional[str]:
    """
    提取第一个完整的JSON对象字符串

    使用栈匹配找到第一个完整的{}对象。
    注意: 这是简化版本,不处理字符串内的{}

    Args:
        text: 包含JSON的文本

    Returns:
        提取的JSON字符串,如果找不到则返回None
    """
    start = text.find('{')
    if start == -1:
        return None

    stack = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            stack += 1
        elif text[i] == '}':
            stack -= 1
            if stack == 0:
                return text[start:i+1]

    return None


def _try_parse_braces(text: str, prefix: str = "") -> Optional[Dict[str, Any]]:
    """尝试提取花括号内容"""
    extracted = _extract_first_json_object(text)

    if not extracted:
        logger.debug(f"{prefix}❌ 方法3失败: 未找到完整的JSON对象")
        return None

    logger.info(f"{prefix}🔍 方法3: 提取花括号内容, 长度={len(extracted)}")

    try:
        data = json.loads(extracted)
        logger.info(f"{prefix}✅ 方法3成功: 花括号内容解析")
        return data
    except json.JSONDecodeError as e:
        logger.debug(f"{prefix}❌ 方法3失败: 花括号解析 - {e}")
        logger.debug(f"{prefix}📝 提取的内容前500字符: {extracted[:500]}")
        return None


def _try_repair_extracted(text: str, prefix: str = "") -> Optional[Dict[str, Any]]:
    """尝试使用json-repair修复提取的花括号内容"""
    extracted = _extract_first_json_object(text)

    if not extracted:
        return None

    # 尝试使用json-repair修复
    try:
        from json_repair import repair_json
        logger.info(f"{prefix}🔧 方法4: 使用json-repair修复花括号内容...")
        repaired = repair_json(extracted)
        data = json.loads(repaired)
        logger.info(f"{prefix}✅ 方法4成功: json-repair修复花括号内容")
        return data
    except Exception as e:
        logger.debug(f"{prefix}❌ 方法4失败: json-repair修复花括号 - {e}")
        return None


def _try_repair_full(text: str, prefix: str = "") -> Optional[Dict[str, Any]]:
    """尝试对整个响应使用json-repair"""
    try:
        from json_repair import repair_json
        logger.info(f"{prefix}🔧 方法5: 对完整响应使用json-repair...")
        repaired = repair_json(text)
        data = json.loads(repaired)
        logger.info(f"{prefix}✅ 方法5成功: json-repair修复完整响应")
        return data
    except Exception as e:
        logger.debug(f"{prefix}❌ 方法5失败: json-repair修复完整响应 - {e}")
        return None


def extract_json_from_text(text: str) -> Optional[str]:
    """
    从文本中提取JSON字符串 (不解析)

    返回第一个完整的JSON对象字符串,如果找不到则返回None。

    Args:
        text: 包含JSON的文本

    Returns:
        提取的JSON字符串,如果找不到则返回None

    Examples:
        >>> extract_json_from_text('结果是 {"a": 1} 很好')
        '{"a": 1}'

        >>> extract_json_from_text('没有JSON')
        None
    """
    return _extract_first_json_object(text)
