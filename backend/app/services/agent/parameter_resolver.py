"""
参数解析器 - 解决工具参数占位符问题

功能:
1. 注册任务执行结果
2. 解析占位符并替换为实际值
3. 支持两种占位符格式:
   - $TASK_N$ : 任务N的完整输出
   - $TASK_N.field$ : 任务N输出的特定字段（JSON解析）

使用示例:
    resolver = ParameterResolver()

    # 执行任务1
    task1_result = '{"content": "第30章内容...", "title": "第30章"}'
    resolver.register_result(1, task1_result)

    # 执行任务2，参数依赖任务1
    task2_params = {"text": "$TASK_1.content$", "focus": "情节"}
    resolved_params = resolver.resolve_params(task2_params, task_id=2)
    # 结果: {"text": "第30章内容...", "focus": "情节"}

作者: Claude Code
日期: 2025-01-09
"""

import re
import json
import logging
import asyncio
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ParameterResolverError(Exception):
    """参数解析器异常"""
    pass


class ParameterResolver:
    """
    参数解析器

    解决Planning阶段生成的占位符参数问题。
    在Execution阶段将占位符替换为实际的任务结果。

    Attributes:
        task_results: 存储任务执行结果 {task_id: result_string}
        strict_mode: 是否严格模式（严格模式下，依赖未执行的任务会抛出异常）
    """

    # 占位符正则模式
    # 匹配: $TASK_1$ 或 $TASK_1.content$ 或 $TASK_1.chapter_info.title$
    # 🔧 2025-12-25: 扩展支持数组索引格式 $TASK_1.chapters[3].content$
    PLACEHOLDER_PATTERN = re.compile(
        r'\$TASK_(\d+)(?:\.([a-zA-Z_][a-zA-Z0-9_.\[\]]*))?\$'
    )

    # 兼容旧格式占位符（逐步废弃）
    # 匹配: 【步骤1返回的章节内容】、【任务1的结果】等
    LEGACY_PATTERN = re.compile(
        r'【(?:步骤|任务)(\d+).*?】'
    )

    def __init__(self, strict_mode: bool = False):
        """
        初始化参数解析器

        Args:
            strict_mode: 是否启用严格模式
                - True: 依赖未执行的任务会抛出异常
                - False: 依赖未执行的任务会返回占位符并记录警告
        """
        self.task_results: Dict[int, str] = {}
        self.strict_mode = strict_mode
        self._lock = asyncio.Lock()  # ✅ 【修复-问题1】添加异步锁保证并发安全
        logger.info(
            f"[ParameterResolver] 初始化完成, "
            f"严格模式: {strict_mode}"
        )

    async def register_result(self, task_id: int, result: str) -> None:
        """
        注册任务执行结果（线程安全）

        Args:
            task_id: 任务ID
            result: 任务执行结果（字符串）

        Raises:
            ParameterResolverError: task_id无效时
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ParameterResolverError(
                f"无效的task_id: {task_id}，必须是正整数"
            )

        # ✅ 【修复-问题4】验证result不为None和类型检查
        if result is None:
            logger.warning(
                f"[ParameterResolver] 任务{task_id}结果为None，转换为空字符串"
            )
            result = ""

        if not isinstance(result, str):
            logger.warning(
                f"[ParameterResolver] 任务{task_id}结果类型为{type(result).__name__}，"
                f"转换为字符串"
            )
            result = str(result)

        # ✅ 【修复-问题1】使用锁保证并发安全
        async with self._lock:
            self.task_results[task_id] = result
            logger.debug(
                f"[ParameterResolver] 注册任务{task_id}结果, "
                f"长度={len(result)}字符"
            )

    async def resolve_params(
        self,
        params: Dict[str, Any],
        current_task_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        解析参数中的占位符（线程安全）

        Args:
            params: 原始参数字典
            current_task_id: 当前任务ID（用于循环依赖检测）

        Returns:
            解析后的参数字典

        Raises:
            ParameterResolverError: 严格模式下，依赖任务未执行时
        """
        # ✅ 【修复-问题1】使用锁保证并发安全
        async with self._lock:
            return self._resolve_params_internal(params, current_task_id)

    def _resolve_params_internal(
        self,
        params: Dict[str, Any],
        current_task_id: Optional[int]
    ) -> Dict[str, Any]:
        """
        内部解析方法（已在锁内调用）

        Args:
            params: 原始参数字典
            current_task_id: 当前任务ID

        Returns:
            解析后的参数字典
        """
        resolved = {}

        for key, value in params.items():
            if isinstance(value, str):
                # 🔧 2026-01-11: 检查是否是纯占位符，如果是则保留原始类型
                pure_placeholder_match = self.PLACEHOLDER_PATTERN.fullmatch(value)
                if pure_placeholder_match:
                    # 纯占位符（如 "$TASK_1.paragraph_index$"），提取原始值并保留类型
                    resolved[key] = self._extract_typed_value(
                        pure_placeholder_match,
                        current_task_id
                    )
                else:
                    # 混合字符串或非占位符，使用字符串替换
                    resolved[key] = self._resolve_string(
                        value,
                        current_task_id
                    )
            elif isinstance(value, dict):
                # 递归解析嵌套字典
                resolved[key] = self._resolve_params_internal(value, current_task_id)
            elif isinstance(value, list):
                # ✅ 【修复-问题5】递归解析列表中的字符串和字典
                resolved[key] = []
                for item in value:
                    if isinstance(item, str):
                        # 🔧 2026-01-11: 列表元素也检查纯占位符
                        pure_match = self.PLACEHOLDER_PATTERN.fullmatch(item)
                        if pure_match:
                            resolved[key].append(
                                self._extract_typed_value(pure_match, current_task_id)
                            )
                        else:
                            resolved[key].append(
                                self._resolve_string(item, current_task_id)
                            )
                    elif isinstance(item, dict):
                        # 递归解析字典元素
                        resolved[key].append(
                            self._resolve_params_internal(item, current_task_id)
                        )
                    else:
                        # 其他类型直接保留
                        resolved[key].append(item)
            else:
                # 其他类型直接保留
                resolved[key] = value

        return resolved

    def _extract_typed_value(
        self,
        match: re.Match,
        current_task_id: Optional[int]
    ) -> Any:
        """
        从占位符中提取值，保留原始类型（整数、布尔等）

        🔧 2026-01-11: 新增方法，解决 paragraph_index 等整数字段被转为字符串的问题

        Args:
            match: 正则匹配对象
            current_task_id: 当前任务ID

        Returns:
            提取的原始值（保留类型）
        """
        task_id = int(match.group(1))
        field_path = match.group(2)

        # 检测自引用
        if current_task_id and task_id == current_task_id:
            logger.warning(
                f"[ParameterResolver] 检测到自引用占位符: 任务{current_task_id}引用自己"
            )
            return None

        # 检查任务是否已执行
        if task_id not in self.task_results:
            if self.strict_mode:
                raise ParameterResolverError(
                    f"任务{task_id}尚未执行，无法解析占位符"
                )
            else:
                logger.warning(
                    f"[ParameterResolver] 任务{task_id}尚未执行，返回None"
                )
                return None

        task_result = self.task_results[task_id]

        # 如果没有字段路径，返回完整结果（字符串）
        if not field_path:
            return task_result

        # 提取JSON字段，保留原始类型
        try:
            data = json.loads(task_result)
            tokens = self._parse_field_path(field_path)

            value = data
            for token in tokens:
                if isinstance(token, int):
                    if isinstance(value, list) and 0 <= token < len(value):
                        value = value[token]
                    else:
                        return task_result  # 降级返回完整结果
                elif isinstance(value, dict) and token in value:
                    value = value[token]
                else:
                    return task_result  # 降级返回完整结果

            # 🔧 关键：直接返回原始值，不转换为字符串
            logger.debug(
                f"[ParameterResolver] $TASK_{task_id}.{field_path}$ → "
                f"{type(value).__name__}: {value}"
            )
            return value

        except json.JSONDecodeError:
            return task_result

    def _resolve_string(
        self,
        text: str,
        current_task_id: Optional[int]
    ) -> str:
        """
        解析字符串中的占位符

        支持两种格式:
        1. $TASK_1$ : 完整输出
        2. $TASK_1.content$ : JSON字段提取

        Args:
            text: 原始字符串
            current_task_id: 当前任务ID

        Returns:
            解析后的字符串
        """
        # 1. 尝试解析新格式占位符 $TASK_N.field$
        result = self.PLACEHOLDER_PATTERN.sub(
            lambda m: self._replace_placeholder(m, current_task_id),
            text
        )

        # 2. 兼容旧格式占位符 【步骤1...】
        if self.LEGACY_PATTERN.search(result):
            logger.warning(
                f"[ParameterResolver] 检测到旧格式占位符: {text}, "
                f"建议使用新格式 $TASK_N$ 或 $TASK_N.field$"
            )
            result = self._resolve_legacy_placeholder(result, current_task_id)

        return result

    def _replace_placeholder(
        self,
        match: re.Match,
        current_task_id: Optional[int]
    ) -> str:
        """
        替换单个占位符

        Args:
            match: 正则匹配对象
            current_task_id: 当前任务ID

        Returns:
            替换后的值
        """
        task_id = int(match.group(1))
        field_path = match.group(2)  # 可能为None

        # 检测自引用（AI 规划错误）
        # 2025-12-24: 改为警告并清理，而非抛出异常，避免中断执行流程
        if current_task_id and task_id == current_task_id:
            logger.warning(
                f"[ParameterResolver] 检测到自引用占位符: 任务{current_task_id}引用自己 "
                f"(可能是AI规划错误)，清理占位符"
            )
            # 返回空字符串，让 TaskRunner 的兜底逻辑处理
            return ""

        # 检查任务是否已执行
        if task_id not in self.task_results:
            error_msg = (
                f"任务{task_id}尚未执行，无法解析占位符 "
                f"$TASK_{task_id}{'.' + field_path if field_path else ''}$"
            )

            if self.strict_mode:
                logger.error(f"[ParameterResolver] {error_msg}")
                raise ParameterResolverError(error_msg)
            else:
                logger.warning(
                    f"[ParameterResolver] {error_msg}, "
                    f"保留占位符（非严格模式）"
                )
                return match.group(0)  # 返回原占位符

        task_result = self.task_results[task_id]

        # 如果没有字段路径，返回完整结果
        if not field_path:
            logger.debug(
                f"[ParameterResolver] $TASK_{task_id}$ → "
                f"完整输出（{len(task_result)}字符）"
            )
            return task_result

        # 提取JSON字段
        return self._extract_field(task_result, field_path, task_id)

    def _extract_field(
        self,
        json_string: str,
        field_path: str,
        task_id: int
    ) -> str:
        """
        从JSON字符串中提取字段

        支持嵌套字段: "content" 或 "chapter_info.title"
        🔧 2025-12-25: 扩展支持数组索引: "chapters[3].content"

        Args:
            json_string: JSON格式的字符串
            field_path: 字段路径，如 "content"、"chapter_info.title" 或 "chapters[3].content"
            task_id: 任务ID（用于日志）

        Returns:
            提取的字段值（转为字符串）
        """
        try:
            # 尝试解析JSON
            data = json.loads(json_string)

            # 解析字段路径，支持数组索引
            # 例如: "chapters[3].content" -> ["chapters", 3, "content"]
            tokens = self._parse_field_path(field_path)

            # 逐层访问
            value = data
            for token in tokens:
                if isinstance(token, int):
                    # 数组索引访问
                    if isinstance(value, list) and 0 <= token < len(value):
                        value = value[token]
                    else:
                        logger.debug(
                            f"[ParameterResolver] 任务{task_id}的结果中"
                            f"数组索引 [{token}] 无效, 使用完整输出"
                        )
                        return json_string
                elif isinstance(value, dict) and token in value:
                    value = value[token]
                else:
                    # 🔧 P3修复: 字段不存在是正常降级行为，改为 debug 级别
                    # 因为很多工具（如 analyze_text_tool）返回纯文本，不是 JSON
                    logger.debug(
                        f"[ParameterResolver] 任务{task_id}的结果中"
                        f"不存在字段 '{field_path}', 使用完整输出"
                    )
                    return json_string

            # 转为字符串
            if isinstance(value, str):
                result = value
            else:
                result = json.dumps(value, ensure_ascii=False)

            logger.debug(
                f"[ParameterResolver] $TASK_{task_id}.{field_path}$ → "
                f"{len(result)}字符"
            )

            return result

        except json.JSONDecodeError as e:
            # 🔧 P3修复: JSON解析失败是正常降级行为，改为 debug 级别
            # 因为很多工具（如 analyze_text_tool）返回纯文本，不是 JSON
            logger.debug(
                f"[ParameterResolver] 任务{task_id}结果不是有效JSON, "
                f"无法提取字段 '{field_path}', 使用完整输出"
            )
            return json_string

    def _parse_field_path(self, field_path: str) -> list:
        """
        解析字段路径为访问令牌列表

        🔧 2025-12-25: 新增方法，支持数组索引解析

        Args:
            field_path: 字段路径，如 "chapters[3].content"

        Returns:
            访问令牌列表，如 ["chapters", 3, "content"]
        """
        tokens = []
        # 匹配字段名或数组索引
        # 例如: "chapters[3].content" -> ["chapters", "[3]", "content"]
        pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)|\[(\d+)\]')

        for match in pattern.finditer(field_path):
            if match.group(1):
                # 字段名
                tokens.append(match.group(1))
            elif match.group(2):
                # 数组索引
                tokens.append(int(match.group(2)))

        return tokens

    def _resolve_legacy_placeholder(
        self,
        text: str,
        current_task_id: Optional[int]
    ) -> str:
        """
        解析旧格式占位符（兼容性）

        旧格式: 【步骤1返回的章节内容】、【任务2的结果】

        Args:
            text: 包含旧格式占位符的文本
            current_task_id: 当前任务ID

        Returns:
            解析后的文本
        """
        def replace_legacy(match: re.Match) -> str:
            task_id = int(match.group(1))

            if task_id not in self.task_results:
                logger.warning(
                    f"[ParameterResolver] 旧格式占位符：任务{task_id}未执行, "
                    f"保留原文"
                )
                return match.group(0)

            logger.info(
                f"[ParameterResolver] 兼容旧格式占位符: "
                f"{match.group(0)} → 任务{task_id}完整输出"
            )

            return self.task_results[task_id]

        return self.LEGACY_PATTERN.sub(replace_legacy, text)

    async def has_result(self, task_id: int) -> bool:
        """
        检查任务是否已注册结果（线程安全）

        Args:
            task_id: 任务ID

        Returns:
            是否已注册
        """
        # ✅ 【修复-问题6】添加锁保证并发安全
        async with self._lock:
            return task_id in self.task_results

    async def get_result(self, task_id: int) -> Optional[str]:
        """
        获取任务结果（线程安全）

        Args:
            task_id: 任务ID

        Returns:
            任务结果，如果未注册则返回None
        """
        # ✅ 【修复-问题6】添加锁保证并发安全
        async with self._lock:
            return self.task_results.get(task_id)

    async def clear(self) -> None:
        """
        清空所有任务结果（线程安全）
        """
        # ✅ 【修复-问题6】添加锁保证并发安全
        async with self._lock:
            self.task_results.clear()
            logger.debug("[ParameterResolver] 已清空所有任务结果")

    async def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息（线程安全）

        Returns:
            统计信息字典
        """
        # ✅ 【修复-问题6】添加锁保证并发安全
        async with self._lock:
            return {
                "total_tasks": len(self.task_results),
                "registered_task_ids": sorted(list(self.task_results.keys())),
                "strict_mode": self.strict_mode
            }


# 导出
__all__ = [
    "ParameterResolver",
    "ParameterResolverError"
]
