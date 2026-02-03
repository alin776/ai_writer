"""
工具类型系统 (Tool Type System)

提供标准化的工具类型定义,支持强类型输入输出验证。

功能:
1. ToolInput/ToolOutput 基类 - 强类型输入输出
2. ToolCategory 枚举 - 工具分类
3. StandardTool[InputT, OutputT] - 标准化工具基类

设计原则:
- 使用 Pydantic 进行输入输出验证
- 使用泛型支持类型提示
- 支持 LangChain 工具转换
"""

from typing import Generic, TypeVar, Any, Dict, Optional, Callable, Awaitable
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime
import logging
import json
from app.utils.datetime_utils import get_utc_now

# 配置日志
logger = logging.getLogger(__name__)


# ==================== 基础类型定义 ====================

class ToolInput(BaseModel):
    """
    工具输入基类

    所有工具的输入都应该继承此类,以获得:
    - Pydantic 自动验证
    - 类型提示支持
    - JSON 序列化支持

    Example:
        >>> class MyToolInput(ToolInput):
        ...     content: str
        ...     max_length: int = 1000
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


class ToolOutput(BaseModel):
    """
    工具输出基类

    标准化的工具输出格式,包含:
    - success: 执行是否成功
    - message: 执行消息(成功/失败原因)
    - data: 实际返回数据
    - metadata: 元数据(执行时间、统计信息等)

    Example:
        >>> output = ToolOutput(
        ...     success=True,
        ...     message="工具执行成功",
        ...     data={"result": "生成的文本"},
        ...     metadata={"execution_time": 1.23}
        ... )
    """

    success: bool = Field(..., description="执行是否成功")
    message: str = Field(..., description="执行消息")
    data: Optional[Any] = Field(default=None, description="返回数据")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


class ToolCategory(str, Enum):
    """
    工具分类枚举

    将工具分为以下类别:
    - WRITING: 写作类工具(续写、扩写、改写等)
    - ANALYSIS: 分析类工具(内容分析、质量评估等)
    - MEMORY: 记忆类工具(记忆存储、检索等)
    - VERSION: 版本类工具(版本管理、回滚等)
    - QUALITY: 质量类工具(一致性检查、风格检查等)
    - UTILITY: 工具类工具(通用辅助功能)

    新增分类（2026-01-09）:
    - CREATIVE: 创作类工具(AI生成内容，不直接修改数据)
    - OPERATION: 操作类工具(修改数据库或编辑器内容，需要用户确认)
    - QUERY: 查询类工具(只读取数据，不修改)
    """

    WRITING = "writing"      # 写作类
    ANALYSIS = "analysis"    # 分析类
    MEMORY = "memory"        # 记忆类
    VERSION = "version"      # 版本类
    QUALITY = "quality"      # 质量类
    UTILITY = "utility"      # 工具类

    # 新增分类（2026-01-09）
    CREATIVE = "creative"    # 创作类：AI生成内容，不直接修改数据
    OPERATION = "operation"  # 操作类：修改数据库或编辑器内容，需要用户确认
    QUERY = "query"          # 查询类：只读取数据，不修改


# ==================== 泛型类型变量 ====================

InputT = TypeVar("InputT", bound=ToolInput)
OutputT = TypeVar("OutputT", bound=ToolOutput)


# ==================== StandardTool 标准化工具 ====================

class StandardTool(Generic[InputT, OutputT]):
    """
    标准化工具基类

    提供统一的工具接口,支持:
    1. 强类型输入输出
    2. 自动输入验证
    3. 执行日志记录
    4. LangChain 工具转换

    Attributes:
        name: 工具名称(唯一标识)
        description: 工具描述
        category: 工具分类
        input_schema: 输入模型类(Pydantic BaseModel)
        output_schema: 输出模型类(Pydantic BaseModel)
        executor: 工具执行函数

    Example:
        >>> class MyInput(ToolInput):
        ...     text: str
        >>>
        >>> class MyOutput(ToolOutput):
        ...     pass
        >>>
        >>> async def my_executor(input_data: MyInput) -> MyOutput:
        ...     return MyOutput(
        ...         success=True,
        ...         message="处理成功",
        ...         data={"processed": input_data.text}
        ...     )
        >>>
        >>> tool = StandardTool(
        ...     name="my_tool",
        ...     description="示例工具",
        ...     category=ToolCategory.UTILITY,
        ...     input_schema=MyInput,
        ...     output_schema=MyOutput,
        ...     executor=my_executor
        ... )
    """

    def __init__(
        self,
        name: str,
        description: str,
        category: ToolCategory,
        input_schema: type[InputT],
        output_schema: type[OutputT],
        executor: Callable[[InputT], Awaitable[OutputT]],
        tags: list[str] = None,
        version: str = "1.0.0"
    ):
        """
        初始化标准化工具

        Args:
            name: 工具名称
            description: 工具描述
            category: 工具分类
            input_schema: 输入模型类
            output_schema: 输出模型类
            executor: 工具执行函数
            tags: 工具标签
            version: 工具版本
        """
        self.name = name
        self.description = description
        self.category = category
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.executor = executor
        self.tags = tags or []
        self.version = version

        # 统计信息
        self._execution_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._total_execution_time = 0.0

    async def execute(self, input_data: InputT) -> OutputT:
        """
        执行工具

        自动处理:
        1. 输入验证(Pydantic自动)
        2. 执行日志记录
        3. 异常捕获
        4. 统计信息更新

        Args:
            input_data: 输入数据(必须是 input_schema 的实例)

        Returns:
            输出数据(output_schema 的实例)

        Raises:
            ValidationError: 输入验证失败
            Exception: 工具执行失败
        """
        import time

        start_time = time.time()
        self._execution_count += 1

        try:
            # 验证输入类型
            if not isinstance(input_data, self.input_schema):
                raise TypeError(
                    f"输入类型错误: 期望 {self.input_schema.__name__}, "
                    f"实际 {type(input_data).__name__}"
                )

            # 执行工具
            logger.info(f"[{self.name}] 开始执行工具")
            result = await self.executor(input_data)

            # 验证输出类型
            if not isinstance(result, self.output_schema):
                raise TypeError(
                    f"输出类型错误: 期望 {self.output_schema.__name__}, "
                    f"实际 {type(result).__name__}"
                )

            # 更新统计
            execution_time = time.time() - start_time
            self._total_execution_time += execution_time

            if result.success:
                self._success_count += 1
                logger.info(
                    f"[{self.name}] 执行成功 "
                    f"(耗时: {execution_time:.3f}s)"
                )
            else:
                self._failure_count += 1
                logger.warning(
                    f"[{self.name}] 执行失败: {result.message} "
                    f"(耗时: {execution_time:.3f}s)"
                )

            # 记录执行日志
            self._log_execution(
                success=result.success,
                execution_time=execution_time,
                error_message=None if result.success else result.message
            )

            return result

        except Exception as e:
            # 执行失败
            execution_time = time.time() - start_time
            self._failure_count += 1
            self._total_execution_time += execution_time

            logger.error(
                f"[{self.name}] 执行异常: {str(e)} "
                f"(耗时: {execution_time:.3f}s)"
            )

            # 记录执行日志
            self._log_execution(
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            )

            # 返回失败结果
            return self.output_schema(
                success=False,
                message=f"工具执行失败: {str(e)}",
                data=None,
                metadata={
                    "error": str(e),
                    "execution_time": execution_time
                }
            )

    def _log_execution(
        self,
        success: bool,
        execution_time: float,
        error_message: Optional[str] = None
    ):
        """
        记录工具执行日志

        将日志同时记录到:
        1. 本地日志文件(logger)
        2. 工具监控系统(如果已启用)

        Args:
            success: 是否成功
            execution_time: 执行时间(秒)
            error_message: 错误消息(如果失败)
        """
        log_entry = {
            "tool_name": self.name,
            "category": self.category.value,
            "success": success,
            "execution_time": execution_time,
            "timestamp": get_utc_now().isoformat(),
            "error": error_message
        }

        # 记录到日志文件
        logger.debug(f"工具执行日志: {json.dumps(log_entry, ensure_ascii=False)}")

        # 记录到监控系统(如果可用)
        try:
            from .tool_monitor import get_tool_monitor
            monitor = get_tool_monitor()
            monitor.log_execution(
                tool_name=self.name,
                execution_time=execution_time,
                success=success,
                error=error_message,
                metadata={
                    "category": self.category.value,
                    "version": self.version
                }
            )
        except Exception as e:
            # 监控系统出错不应该影响工具执行
            logger.warning(f"Failed to log to monitor: {e}")

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取工具统计信息

        Returns:
            统计信息字典
        """
        return {
            "name": self.name,
            "category": self.category.value,
            "execution_count": self._execution_count,
            "success_count": self._success_count,
            "failure_count": self._failure_count,
            "success_rate": (
                self._success_count / self._execution_count
                if self._execution_count > 0 else 0
            ),
            "avg_execution_time": (
                self._total_execution_time / self._execution_count
                if self._execution_count > 0 else 0
            ),
            "total_execution_time": self._total_execution_time
        }

    def to_langchain_tool(self):
        """
        转换为 LangChain Tool

        将 StandardTool 转换为 LangChain 可用的 Tool 对象。
        处理异步转同步的包装。

        Returns:
            LangChain Tool 对象

        Note:
            需要安装 langchain 包
        """
        try:
            from langchain.tools import Tool
            import asyncio
        except ImportError:
            raise ImportError(
                "需要安装 langchain 包才能使用 to_langchain_tool() 方法\n"
                "运行: pip install langchain"
            )

        def sync_wrapper(**kwargs) -> Dict[str, Any]:
            """
            同步包装器

            将异步的 execute 方法包装为同步方法,
            供 LangChain 使用。
            """
            # 创建输入对象
            input_obj = self.input_schema(**kwargs)

            # 获取或创建事件循环
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # 执行异步方法
            result = loop.run_until_complete(self.execute(input_obj))

            # 返回字典格式
            return result.dict()

        # 创建 LangChain Tool
        return Tool(
            name=self.name,
            description=self.description,
            func=sync_wrapper,
            args_schema=self.input_schema
        )

    def __repr__(self) -> str:
        return (
            f"StandardTool(name='{self.name}', "
            f"category={self.category.value}, "
            f"version='{self.version}')"
        )


# ==================== 导出 ====================

__all__ = [
    # 基础类型
    "ToolInput",
    "ToolOutput",
    "ToolCategory",
    # 标准化工具
    "StandardTool",
    # 类型变量
    "InputT",
    "OutputT",
]
