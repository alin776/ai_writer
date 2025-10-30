"""
工具动态注册系统 (Dynamic Tool Registry)

功能:
1. 自动发现和注册现有的139个API为工具
2. 动态加载工具定义
3. 工具版本管理
4. 工具权限控制

目标:
- 快速将现有API封装为Agent可用的工具
- 支持热插拔工具
- 统一的工具调用接口
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
import inspect
import json


class ToolParameter(BaseModel):
    """工具参数定义"""
    name: str
    type: str  # string/integer/boolean/object/array
    description: str
    required: bool = True
    default: Optional[Any] = None
    enum: Optional[List[Any]] = None  # 枚举值


class ToolDefinition(BaseModel):
    """工具定义"""
    tool_id: str  # 工具唯一ID
    name: str  # 工具名称
    description: str  # 工具描述
    category: str  # 分类: writing/editing/analysis/knowledge/worldview
    parameters: List[ToolParameter]  # 参数列表
    returns: str  # 返回值描述
    examples: List[Dict[str, Any]] = []  # 使用示例
    version: str = "1.0.0"
    tags: List[str] = []  # 标签
    deprecated: bool = False


class ToolMetadata(BaseModel):
    """工具元数据"""
    tool_id: str
    registered_at: str
    last_used: Optional[str] = None
    usage_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    avg_duration_ms: float = 0.0


class DynamicToolRegistry:
    """动态工具注册表"""

    def __init__(self):
        """初始化工具注册表"""
        self.tools: Dict[str, ToolDefinition] = {}
        self.executors: Dict[str, Callable] = {}
        self.metadata: Dict[str, ToolMetadata] = {}

    # ==================== 工具注册 ====================

    def register_tool(
        self,
        tool_def: ToolDefinition,
        executor: Callable
    ):
        """
        注册工具

        Args:
            tool_def: 工具定义
            executor: 执行函数
        """
        tool_id = tool_def.tool_id

        # 保存定义
        self.tools[tool_id] = tool_def
        self.executors[tool_id] = executor

        # 初始化元数据
        if tool_id not in self.metadata:
            self.metadata[tool_id] = ToolMetadata(
                tool_id=tool_id,
                registered_at=datetime.now().isoformat()
            )

    def register_from_function(
        self,
        func: Callable,
        tool_id: str,
        category: str,
        description: str = None,
        examples: List[Dict] = None
    ):
        """
        从Python函数自动注册工具

        Args:
            func: 函数
            tool_id: 工具ID
            category: 分类
            description: 描述（可选，否则从docstring提取）
            examples: 示例
        """
        # 提取函数签名
        sig = inspect.signature(func)
        params = []

        for param_name, param in sig.parameters.items():
            # 跳过特殊参数
            if param_name in ["self", "cls", "kwargs"]:
                continue

            param_type = "string"
            if param.annotation != inspect.Parameter.empty:
                annotation = param.annotation
                if annotation == int:
                    param_type = "integer"
                elif annotation == bool:
                    param_type = "boolean"
                elif annotation == dict:
                    param_type = "object"
                elif annotation == list:
                    param_type = "array"

            params.append(ToolParameter(
                name=param_name,
                type=param_type,
                description=f"参数 {param_name}",
                required=param.default == inspect.Parameter.empty
            ))

        # 使用docstring或提供的描述
        final_description = description or func.__doc__ or f"工具: {tool_id}"

        tool_def = ToolDefinition(
            tool_id=tool_id,
            name=tool_id,
            description=final_description.strip(),
            category=category,
            parameters=params,
            returns="函数返回值",
            examples=examples or []
        )

        self.register_tool(tool_def, func)

    def register_api_endpoint(
        self,
        tool_id: str,
        endpoint: str,
        method: str,
        category: str,
        description: str,
        parameters: List[ToolParameter],
        api_caller: Callable
    ):
        """
        注册API端点为工具

        Args:
            tool_id: 工具ID
            endpoint: API端点
            method: HTTP方法
            category: 分类
            description: 描述
            parameters: 参数列表
            api_caller: API调用函数
        """
        tool_def = ToolDefinition(
            tool_id=tool_id,
            name=tool_id,
            description=description,
            category=category,
            parameters=parameters,
            returns="API响应",
            tags=[method.lower(), "api"]
        )

        # 包装API调用
        async def executor(**kwargs):
            return await api_caller(endpoint, method, kwargs)

        self.register_tool(tool_def, executor)

    def batch_register_from_config(self, config: List[Dict[str, Any]]):
        """
        从配置文件批量注册工具

        Args:
            config: 工具配置列表
        """
        for tool_cfg in config:
            tool_def = ToolDefinition(**tool_cfg["definition"])
            # executor需要单独提供
            # 这里简化处理
            self.tools[tool_def.tool_id] = tool_def

    # ==================== 工具调用 ====================

    async def call_tool(
        self,
        tool_id: str,
        parameters: Dict[str, Any]
    ) -> Any:
        """
        调用工具

        Args:
            tool_id: 工具ID
            parameters: 参数

        Returns:
            Any: 执行结果
        """
        if tool_id not in self.tools:
            raise ValueError(f"Tool {tool_id} not found")

        executor = self.executors.get(tool_id)
        if not executor:
            raise ValueError(f"No executor for tool {tool_id}")

        # 验证参数
        tool_def = self.tools[tool_id]
        self._validate_parameters(tool_def, parameters)

        # 记录开始时间
        start = datetime.now()

        try:
            # 执行
            if inspect.iscoroutinefunction(executor):
                result = await executor(**parameters)
            else:
                result = executor(**parameters)

            # 更新统计
            self._update_stats(tool_id, success=True, start=start)

            return result

        except Exception as e:
            # 更新统计
            self._update_stats(tool_id, success=False, start=start)
            raise e

    def _validate_parameters(
        self,
        tool_def: ToolDefinition,
        parameters: Dict[str, Any]
    ):
        """验证参数"""
        required_params = [p.name for p in tool_def.parameters if p.required]

        for param in required_params:
            if param not in parameters:
                raise ValueError(f"Missing required parameter: {param}")

    def _update_stats(
        self,
        tool_id: str,
        success: bool,
        start: datetime
    ):
        """更新统计信息"""
        metadata = self.metadata[tool_id]

        metadata.usage_count += 1
        metadata.last_used = datetime.now().isoformat()

        if success:
            metadata.success_count += 1
        else:
            metadata.failure_count += 1

        # 更新平均耗时
        duration_ms = (datetime.now() - start).total_seconds() * 1000
        metadata.avg_duration_ms = (
            (metadata.avg_duration_ms * (metadata.usage_count - 1) + duration_ms)
            / metadata.usage_count
        )

    # ==================== 工具查询 ====================

    def get_tool(self, tool_id: str) -> Optional[ToolDefinition]:
        """获取工具定义"""
        return self.tools.get(tool_id)

    def list_tools(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[ToolDefinition]:
        """
        列出工具

        Args:
            category: 按分类筛选
            tags: 按标签筛选

        Returns:
            List[ToolDefinition]: 工具列表
        """
        tools = list(self.tools.values())

        if category:
            tools = [t for t in tools if t.category == category]

        if tags:
            tools = [
                t for t in tools
                if any(tag in t.tags for tag in tags)
            ]

        return tools

    def search_tools(self, query: str) -> List[ToolDefinition]:
        """
        搜索工具

        Args:
            query: 搜索关键词

        Returns:
            List[ToolDefinition]: 匹配的工具
        """
        query_lower = query.lower()
        results = []

        for tool in self.tools.values():
            if (query_lower in tool.name.lower() or
                query_lower in tool.description.lower() or
                any(query_lower in tag.lower() for tag in tool.tags)):
                results.append(tool)

        return results

    def get_tool_stats(self, tool_id: str) -> Optional[ToolMetadata]:
        """获取工具统计信息"""
        return self.metadata.get(tool_id)

    # ==================== 工具管理 ====================

    def unregister_tool(self, tool_id: str):
        """注销工具"""
        if tool_id in self.tools:
            del self.tools[tool_id]
        if tool_id in self.executors:
            del self.executors[tool_id]

    def update_tool(self, tool_id: str, updates: Dict[str, Any]):
        """更新工具定义"""
        if tool_id not in self.tools:
            raise ValueError(f"Tool {tool_id} not found")

        tool = self.tools[tool_id]
        for key, value in updates.items():
            if hasattr(tool, key):
                setattr(tool, key, value)

    def export_tools(self) -> List[Dict[str, Any]]:
        """导出所有工具定义"""
        return [tool.dict() for tool in self.tools.values()]

    def import_tools(self, tools_data: List[Dict[str, Any]]):
        """导入工具定义"""
        for tool_data in tools_data:
            tool = ToolDefinition(**tool_data)
            self.tools[tool.tool_id] = tool


# ==================== 全局注册表实例 ====================

# 全局工具注册表
global_registry = DynamicToolRegistry()


# ==================== 便捷装饰器 ====================

def register_as_tool(
    tool_id: str,
    category: str,
    description: str = None,
    examples: List[Dict] = None
):
    """
    装饰器：将函数注册为工具

    使用方法:
    ```python
    @register_as_tool("continue_writing", "writing", "续写章节")
    async def continue_writing(text: str, work_id: str):
        # 实现
        pass
    ```
    """
    def decorator(func: Callable):
        global_registry.register_from_function(
            func,
            tool_id,
            category,
            description,
            examples
        )
        return func

    return decorator


# ==================== 预定义工具注册 ====================

def register_core_writing_tools():
    """注册核心写作工具"""

    # 这里应该导入实际的服务函数
    # 简化示例

    @register_as_tool("continue_writing", "writing", "续写文本")
    async def continue_writing(text: str, work_id: str, chapter_id: str):
        """续写工具"""
        # 实际应该调用 AI 服务
        return {"continued_text": text + "... 续写内容"}

    @register_as_tool("polish_text", "editing", "润色文本")
    async def polish_text(text: str):
        """润色工具"""
        return {"polished_text": text}

    @register_as_tool("expand_text", "writing", "扩写文本")
    async def expand_text(text: str, target_length: int):
        """扩写工具"""
        return {"expanded_text": text}

    @register_as_tool("search_knowledge", "knowledge", "搜索知识库")
    async def search_knowledge(query: str, user_id: str):
        """知识库搜索"""
        return {"results": []}

    @register_as_tool("get_chapter_context", "knowledge", "获取章节上下文")
    async def get_chapter_context(chapter_id: str):
        """获取章节上下文"""
        return {"context": {}}

    @register_as_tool("evaluate_text", "analysis", "评估文本质量")
    async def evaluate_text(text: str):
        """评估工具"""
        return {"score": 85, "feedback": []}

    @register_as_tool("create_character", "worldview", "创建角色")
    async def create_character(name: str, role: str, work_id: str):
        """创建角色"""
        return {"character_id": "xxx", "created": True}

    @register_as_tool("create_worldview", "worldview", "创建世界观")
    async def create_worldview(genre: str, work_id: str):
        """创建世界观"""
        return {"worldview_id": "xxx", "created": True}


def register_all_tools_from_api_definitions(api_definitions_path: str):
    """
    从API定义文件批量注册工具

    Args:
        api_definitions_path: API定义文件路径（JSON）
    """
    with open(api_definitions_path, "r", encoding="utf-8") as f:
        api_defs = json.load(f)

    for api_def in api_defs:
        # 根据API定义创建工具定义
        tool_id = api_def["tool_id"]
        # ... 其他逻辑
        pass
