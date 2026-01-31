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
from typing import Dict, Any, Optional, Set

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
    # 🔧 2026-01-12: 修复正则表达式，使用 [$] 匹配字面量 $ 符号
    PLACEHOLDER_PATTERN = re.compile(
        r'[$]TASK_(\d+)(?:\.([a-zA-Z_][a-zA-Z0-9_.\[\]]*))?[$]'
    )

    # 🆕 2026-01-12: 兼容模式 - 支持没有结尾 $ 的占位符（AI 偶尔生成错误格式）
    # 匹配: $TASK_1 或 $TASK_1.content（没有结尾 $，后面跟空白、逗号、引号等）
    LOOSE_PLACEHOLDER_PATTERN = re.compile(
        r'[$]TASK_(\d+)(?:\.([a-zA-Z_][a-zA-Z0-9_.\[\]]*))?(?=\s|$|,|\}|\"|\')'
    )

    # 兼容旧格式占位符（逐步废弃）
    # 匹配: 【步骤1返回的章节内容】、【任务1的结果】等
    LEGACY_PATTERN = re.compile(
        r'【(?:步骤|任务)(\d+).*?】'
    )

    # 🆕 2026-01-25: 支持模板占位符 {{TASK_1.field}}
    TEMPLATE_PATTERN = re.compile(
        r'\{\{\s*TASK_(\d+)(?:\.([a-zA-Z_][a-zA-Z0-9_.\[\]]*))?\s*\}\}'
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
        self.task_payloads: Dict[int, Any] = {}
        self.strict_mode = strict_mode
        self._lock = asyncio.Lock()  # ✅ 【修复-问题1】添加异步锁保证并发安全
        logger.info(
            f"[ParameterResolver] 初始化完成, "
            f"严格模式: {strict_mode}"
        )

    async def register_result(self, task_id: int, result: Any) -> None:
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

        raw_result = result
        result_str = ""

        # ✅ 【修复-问题4】验证result不为None和类型检查
        if result is None:
            logger.warning(
                f"[ParameterResolver] 任务{task_id}结果为None，转换为空字符串"
            )
            raw_result = None
            result_str = ""
        elif isinstance(result, str):
            result_str = result
            try:
                raw_result = json.loads(result)
            except Exception:
                raw_result = result
        else:
            try:
                result_str = json.dumps(result, ensure_ascii=False)
            except Exception:
                result_str = str(result)
            raw_result = result

        # ✅ 【修复-问题1】使用锁保证并发安全
        async with self._lock:
            self.task_results[task_id] = result_str
            self.task_payloads[task_id] = raw_result
            logger.debug(
                f"[ParameterResolver] 注册任务{task_id}结果, "
                f"长度={len(result_str)}字符"
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
                # 🆕 2026-01-12: 兼容模式 - 也检查没有结尾 $ 的占位符
                if not pure_placeholder_match:
                    pure_placeholder_match = self.LOOSE_PLACEHOLDER_PATTERN.fullmatch(value)
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
                if self._is_ref_obj(value):
                    resolved[key] = self._resolve_ref(value, current_task_id)
                elif self._is_template_obj(value):
                    resolved[key] = self._resolve_template_obj(value, current_task_id)
                else:
                    # 递归解析嵌套字典
                    resolved[key] = self._resolve_params_internal(value, current_task_id)
            elif isinstance(value, list):
                # ✅ 【修复-问题5】递归解析列表中的字符串和字典
                resolved[key] = []
                for item in value:
                    if isinstance(item, str):
                        # 🔧 2026-01-11: 列表元素也检查纯占位符
                        pure_match = self.PLACEHOLDER_PATTERN.fullmatch(item)
                        # 🆕 2026-01-12: 兼容模式
                        if not pure_match:
                            pure_match = self.LOOSE_PLACEHOLDER_PATTERN.fullmatch(item)
                        if pure_match:
                            resolved[key].append(
                                self._extract_typed_value(pure_match, current_task_id)
                            )
                        else:
                            resolved[key].append(
                                self._resolve_string(item, current_task_id)
                            )
                    elif isinstance(item, dict):
                        if self._is_ref_obj(item):
                            resolved[key].append(self._resolve_ref(item, current_task_id))
                        else:
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

        # 🔧 2026-01-13: 添加调试日志
        logger.info(f"[ParameterResolver] 解析占位符: $TASK_{task_id}.{field_path}$")

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
        payload = self.task_payloads.get(task_id, task_result)

        # 🔧 2026-01-13: 添加调试日志
        logger.info(f"[ParameterResolver] 任务{task_id}结果长度: {len(task_result) if task_result else 0}")

        # 如果没有字段路径，返回完整结果（保留类型）
        if not field_path:
            return payload

        value = self._extract_from_payload(payload, field_path, None)
        # 🔧 关键：直接返回原始值，不转换为字符串
        logger.info(
            f"[ParameterResolver] $TASK_{task_id}.{field_path}$ → "
            f"{type(value).__name__}: {str(value)[:100]}"
        )
        return value

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

        # 🆕 2026-01-12: 兼容模式 - 尝试解析没有结尾 $ 的占位符
        if self.LOOSE_PLACEHOLDER_PATTERN.search(result):
            logger.warning(
                f"[ParameterResolver] 检测到不规范占位符（缺少结尾$）: {text[:100]}, "
                f"建议使用标准格式 $TASK_N$ 或 $TASK_N.field$"
            )
            result = self.LOOSE_PLACEHOLDER_PATTERN.sub(
                lambda m: self._replace_placeholder(m, current_task_id),
                result
            )

        # 2. 兼容旧格式占位符 【步骤1...】
        if self.LEGACY_PATTERN.search(result):
            logger.warning(
                f"[ParameterResolver] 检测到旧格式占位符: {text}, "
                f"建议使用新格式 $TASK_N$ 或 $TASK_N.field$"
            )
            result = self._resolve_legacy_placeholder(result, current_task_id)

        # 3. 解析模板占位符 {{TASK_N.field}}
        if self.TEMPLATE_PATTERN.search(result):
            result = self.TEMPLATE_PATTERN.sub(
                lambda m: self._replace_template_placeholder(m, current_task_id),
                result
            )

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

    def _replace_template_placeholder(
        self,
        match: re.Match,
        current_task_id: Optional[int]
    ) -> str:
        task_id = int(match.group(1))
        field_path = match.group(2)

        if current_task_id and task_id == current_task_id:
            logger.warning(
                f"[ParameterResolver] 检测到自引用模板占位符: 任务{current_task_id}引用自己"
            )
            return ""

        if task_id not in self.task_results:
            error_msg = (
                f"任务{task_id}尚未执行，无法解析模板占位符 "
                f"{{{{TASK_{task_id}{'.' + field_path if field_path else ''}}}}}"
            )
            if self.strict_mode:
                logger.error(f"[ParameterResolver] {error_msg}")
                raise ParameterResolverError(error_msg)
            logger.warning(
                f"[ParameterResolver] {error_msg}, 保留模板占位符（非严格模式）"
            )
            return match.group(0)

        payload = self.task_payloads.get(task_id, self.task_results.get(task_id))
        if not field_path:
            result = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
            return result

        value = self._extract_from_payload(payload, field_path, match.group(0))
        if isinstance(value, str):
            return value
        try:
            return json.dumps(value, ensure_ascii=False)
        except Exception:
            return str(value)

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

    def _extract_from_payload(
        self,
        payload: Any,
        field_path: str,
        fallback: str
    ) -> Any:
        """从结构化结果中提取字段，失败则回退到 fallback。"""
        data = payload
        if isinstance(payload, str):
            try:
                data = json.loads(payload)
            except Exception:
                return fallback

        tokens = self._parse_field_path(field_path)
        logger.info(f"[ParameterResolver] 解析路径 {field_path} -> tokens: {tokens}")

        value = data
        for token in tokens:
            if isinstance(token, int):
                if isinstance(value, list) and 0 <= token < len(value):
                    value = value[token]
                else:
                    logger.warning(f"[ParameterResolver] 数组索引 {token} 越界，降级返回完整结果")
                    return fallback
            elif isinstance(value, dict) and token in value:
                value = value[token]
            else:
                logger.warning(f"[ParameterResolver] 字段 {token} 不存在于 {type(value).__name__}，降级返回完整结果")
                return fallback

        return value

    @classmethod
    def extract_dependencies(cls, params: Any) -> Set[int]:
        """从参数中提取任务依赖（占位符 + $ref）。"""
        deps: Set[int] = set()

        def _walk(value: Any) -> None:
            if isinstance(value, dict):
                if cls._is_ref_obj(value):
                    ref_obj = value.get("$ref") or value.get("ref") or {}
                    task_id = ref_obj.get("task_id")
                    try:
                        deps.add(int(task_id))
                    except (TypeError, ValueError):
                        pass
                    return
                for item in value.values():
                    _walk(item)
            elif isinstance(value, list):
                for item in value:
                    _walk(item)
            elif isinstance(value, str):
                for match in cls.PLACEHOLDER_PATTERN.finditer(value):
                    try:
                        deps.add(int(match.group(1)))
                    except (TypeError, ValueError):
                        continue
                for match in cls.LOOSE_PLACEHOLDER_PATTERN.finditer(value):
                    try:
                        deps.add(int(match.group(1)))
                    except (TypeError, ValueError):
                        continue
                for match in cls.TEMPLATE_PATTERN.finditer(value):
                    try:
                        deps.add(int(match.group(1)))
                    except (TypeError, ValueError):
                        continue

        _walk(params)
        return deps

    @staticmethod
    def _is_ref_obj(value: Any) -> bool:
        if not isinstance(value, dict):
            return False
        keys = set(value.keys())
        if keys == {"$ref"} and isinstance(value.get("$ref"), dict):
            return True
        if keys == {"ref"} and isinstance(value.get("ref"), dict):
            return True
        return False

    @staticmethod
    def _is_template_obj(value: Any) -> bool:
        if not isinstance(value, dict):
            return False
        keys = set(value.keys())
        if keys == {"$template"}:
            return True
        if keys == {"template"}:
            return True
        return False

    def _resolve_template_obj(
        self,
        template_obj: Dict[str, Any],
        current_task_id: Optional[int]
    ) -> str:
        template = template_obj.get("$template", template_obj.get("template", ""))
        if not isinstance(template, str):
            template = str(template)
        return self._resolve_string(template, current_task_id)

    def _resolve_ref(
        self,
        ref_wrapper: Dict[str, Any],
        current_task_id: Optional[int]
    ) -> Any:
        ref_obj = ref_wrapper.get("$ref") or ref_wrapper.get("ref") or {}
        task_id = ref_obj.get("task_id")
        try:
            task_id = int(task_id)
        except (TypeError, ValueError):
            return ref_obj.get("default")

        if current_task_id and task_id == current_task_id:
            logger.warning(
                f"[ParameterResolver] 检测到自引用引用: 任务{current_task_id}引用自己"
            )
            return ref_obj.get("default")

        if task_id not in self.task_results:
            if self.strict_mode:
                raise ParameterResolverError(
                    f"任务{task_id}尚未执行，无法解析引用"
                )
            logger.warning(
                f"[ParameterResolver] 任务{task_id}尚未执行，返回默认值"
            )
            return ref_obj.get("default")

        payload = self.task_payloads.get(task_id, self.task_results.get(task_id))
        path = ref_obj.get("path") or ""
        if not path:
            return payload

        default_value = ref_obj.get("default")
        return self._extract_from_payload(payload, path, default_value)
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
