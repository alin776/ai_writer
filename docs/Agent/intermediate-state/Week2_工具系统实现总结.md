# Week 2 - 工具系统标准化实现总结

> **实现日期**: 2025-10-31
> **对应Week**: Week 2 (阶段一 - 第2周)
> **实现目标**: 标准化工具接口、强类型输入输出、工具监控系统

---

## 📋 目录

1. [系统架构设计](#1-系统架构设计)
2. [核心模块实现](#2-核心模块实现)
3. [工具实现详解](#3-工具实现详解)
4. [监控系统设计](#4-监控系统设计)
5. [技术难点和解决方案](#5-技术难点和解决方案)
6. [使用示例](#6-使用示例)
7. [最佳实践](#7-最佳实践)

---

## 1. 系统架构设计

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        Agent 系统                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │  LangGraph   │ ◄─────► │ Tool Registry │                 │
│  │   Agent      │         │  (统一接口)   │                 │
│  └──────────────┘         └───────┬──────┘                  │
│                                    │                          │
│         ┌──────────────────────────┼───────────────────────┐ │
│         │                          │                        │ │
│         ▼                          ▼                        ▼ │
│  ┌─────────────┐          ┌─────────────┐        ┌──────────────┐
│  │ @tool       │          │ StandardTool │        │ ToolMonitor  │
│  │ (Legacy)    │          │ (New)        │        │ (监控统计)    │
│  └─────────────┘          └──────┬──────┘        └──────────────┘
│                                   │                          │
│                    ┌──────────────┼───────────────┐         │
│                    │              │               │          │
│                    ▼              ▼               ▼          │
│            ┌────────────┐ ┌────────────┐ ┌────────────┐    │
│            │  Writing   │ │ Analysis   │ │  Future    │    │
│            │   Tools    │ │   Tools    │ │   Tools    │    │
│            │ (续写/润色) │ │ (分析/评估) │ │    ...     │    │
│            └────────────┘ └────────────┘ └────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 核心概念

#### StandardTool - 标准化工具

**设计理念**:
- 每个工具都是一个`StandardTool[InputT, OutputT]`实例
- 输入输出强类型约束
- 统一的执行流程和错误处理

**关键特性**:
1. **强类型** - 使用Pydantic + 泛型
2. **自动验证** - 输入输出自动验证
3. **统计监控** - 自动记录执行统计
4. **LangChain兼容** - 可转换为LangChain Tool

#### ToolInput/ToolOutput - 类型定义

**ToolInput**:
- 所有工具输入的基类
- 继承自Pydantic BaseModel
- 支持自动验证、类型转换、JSON序列化

**ToolOutput**:
- 统一的输出格式: `{success, message, data, metadata}`
- 标准化成功和失败的返回结构
- 便于上层统一处理

#### ToolMonitor - 监控系统

**功能**:
- 记录每次工具执行的日志
- 统计工具执行次数、成功率、执行时间
- 追踪错误和异常
- 支持Redis + 内存双存储

---

## 2. 核心模块实现

### 2.1 tool_types.py - 类型系统

**文件位置**: `backend/app/services/agent/tools/tool_types.py`

#### ToolInput 基类

```python
class ToolInput(BaseModel):
    """
    工具输入基类

    所有工具的输入都应该继承此类,以获得:
    - Pydantic 自动验证
    - 类型提示支持
    - JSON 序列化支持
    """

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

**使用示例**:
```python
class MyToolInput(ToolInput):
    content: str = Field(..., min_length=10, max_length=1000)
    options: List[str] = Field(default_factory=list)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
```

#### ToolOutput 基类

```python
class ToolOutput(BaseModel):
    """
    工具输出基类

    标准化的工具输出格式,包含:
    - success: 执行是否成功
    - message: 执行消息(成功/失败原因)
    - data: 实际返回数据
    - metadata: 元数据(执行时间、统计信息等)
    """

    success: bool = Field(..., description="执行是否成功")
    message: str = Field(..., description="执行消息")
    data: Optional[Any] = Field(default=None, description="返回数据")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
```

#### ToolCategory 枚举

```python
class ToolCategory(str, Enum):
    """
    工具分类枚举
    """
    WRITING = "writing"      # 写作类(续写、扩写、改写等)
    ANALYSIS = "analysis"    # 分析类(内容分析、质量评估等)
    MEMORY = "memory"        # 记忆类(记忆存储、检索等)
    VERSION = "version"      # 版本类(版本管理、回滚等)
    QUALITY = "quality"      # 质量类(一致性检查、风格检查等)
    UTILITY = "utility"      # 工具类(通用辅助功能)
```

#### StandardTool 基类

**核心方法**:

**1. `__init__()` - 初始化**
```python
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
```

**2. `execute()` - 执行工具**
```python
async def execute(self, input_data: InputT) -> OutputT:
    """
    执行工具

    自动处理:
    1. 输入验证(Pydantic自动)
    2. 执行日志记录
    3. 异常捕获
    4. 统计信息更新
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
            logger.info(f"[{self.name}] 执行成功 (耗时: {execution_time:.3f}s)")
        else:
            self._failure_count += 1
            logger.warning(f"[{self.name}] 执行失败: {result.message} (耗时: {execution_time:.3f}s)")

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

        logger.error(f"[{self.name}] 执行异常: {str(e)} (耗时: {execution_time:.3f}s)")

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
```

**3. `_log_execution()` - 记录执行日志**
```python
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
    """
    log_entry = {
        "tool_name": self.name,
        "category": self.category.value,
        "success": success,
        "execution_time": execution_time,
        "timestamp": datetime.now().isoformat(),
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
```

**4. `get_statistics()` - 获取统计信息**
```python
def get_statistics(self) -> Dict[str, Any]:
    """
    获取工具统计信息
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
```

**5. `to_langchain_tool()` - 转换为LangChain Tool**
```python
def to_langchain_tool(self):
    """
    转换为 LangChain Tool

    将 StandardTool 转换为 LangChain 可用的 Tool 对象。
    处理异步转同步的包装。
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
```

### 2.2 tool_registry.py - 工具注册表

**文件位置**: `backend/app/services/agent/tools/tool_registry.py`

#### StandardToolRegistry 类

```python
class StandardToolRegistry:
    """
    标准化工具注册表

    管理所有StandardTool实例,提供:
    1. 工具注册
    2. 工具检索
    3. 统一调用接口
    4. 与DynamicToolRegistry兼容
    """

    def __init__(self):
        self._standard_tools: Dict[str, StandardTool] = {}
        self._dynamic_registry = DynamicToolRegistry()  # 兼容现有@tool

    # ==================== 标准化工具管理 ====================

    def register_standard_tool(self, tool: StandardTool):
        """注册StandardTool"""
        self._standard_tools[tool.name] = tool
        logger.info(f"[OK] Registered StandardTool: {tool.name}")

    def get_standard_tool(self, name: str) -> Optional[StandardTool]:
        """获取StandardTool"""
        return self._standard_tools.get(name)

    def list_standard_tools(self) -> List[StandardTool]:
        """列出所有StandardTool"""
        return list(self._standard_tools.values())

    # ==================== 统一调用接口 ====================

    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        统一的工具调用接口

        支持:
        1. StandardTool (新)
        2. @tool (现有)

        自动判断工具类型并调用
        """
        # 优先尝试StandardTool
        standard_tool = self.get_standard_tool(tool_name)
        if standard_tool:
            try:
                input_obj = standard_tool.input_schema(**params)
                result = await standard_tool.execute(input_obj)
                return result.dict()
            except ValidationError as e:
                return {
                    "success": False,
                    "message": f"输入验证失败: {str(e)}",
                    "data": None,
                    "metadata": {"validation_error": str(e)}
                }

        # 回退到DynamicToolRegistry (@tool)
        tool_def = self._dynamic_registry.get_tool(tool_name)
        if tool_def:
            return await self._dynamic_registry.call_tool(tool_name, params)

        # 工具不存在
        return {
            "success": False,
            "message": f"工具不存在: {tool_name}",
            "data": None,
            "metadata": {}
        }
```

### 2.3 tool_monitor.py - 监控系统

详见 [4. 监控系统设计](#4-监控系统设计)

---

## 3. 工具实现详解

### 3.1 Writing Tools (写作工具)

**文件位置**: `backend/app/services/agent/tools/writing_tools.py`

#### 3.1.1 continue_writing_tool (续写工具)

**用途**: 根据上下文续写内容

**输入**:
```python
class ContinueWritingInput(ToolInput):
    context: str = Field(..., min_length=10, max_length=10000, description="已有的文本上下文")
    requirements: str = Field(default="", description="续写的具体要求")
    target_length: int = Field(default=500, ge=100, le=5000, description="期望续写的长度(字数)")
    style: str = Field(default="", description="写作风格(如:正式、轻松、幽默等)")
```

**输出**:
```python
class ContinueWritingOutput(ToolOutput):
    success: bool
    message: str
    data: Dict  # {
        # generated_text: 生成的续写文本
        # word_count: 生成的字数
        # context_summary: 上下文摘要
        # style_notes: 风格说明
    # }
```

**实现**:
```python
async def continue_writing_executor(input_data: ContinueWritingInput) -> ContinueWritingOutput:
    """续写工具执行器"""
    try:
        # 构建续写提示词
        prompt = f"""你是一位专业的小说续写助手。请根据以下上下文续写内容。

【上下文】
{input_data.context}

【续写要求】
- 目标字数: {input_data.target_length} 字
- 写作风格: {input_data.style or '保持与上文一致'}
- 具体要求: {input_data.requirements or '自然流畅地续写'}

【任务】
请自然流畅地续写约 {input_data.target_length} 字的内容,保持与上文风格一致。
"""

        # 调用AI服务生成文本
        generated_text = await _generate_text(
            prompt=prompt,
            temperature=0.8,
            max_tokens=int(input_data.target_length * 1.5)
        )

        # 统计字数
        word_count = len(generated_text)

        # 生成上下文摘要
        context_summary = input_data.context[:100] + "..." if len(input_data.context) > 100 else input_data.context

        return ContinueWritingOutput(
            success=True,
            message="续写成功",
            data={
                "generated_text": generated_text,
                "word_count": word_count,
                "context_summary": context_summary,
                "style_notes": input_data.style or "保持与上文一致"
            }
        )

    except Exception as e:
        return ContinueWritingOutput(
            success=False,
            message=f"续写失败: {str(e)}",
            data=None
        )

# 创建工具实例
continue_writing_tool = StandardTool(
    name="continue_writing",
    description="根据上下文续写内容,保持风格一致",
    category=ToolCategory.WRITING,
    input_schema=ContinueWritingInput,
    output_schema=ContinueWritingOutput,
    executor=continue_writing_executor,
    tags=["writing", "generation", "continuation"],
    version="1.0.0"
)
```

#### 3.1.2 polish_text_tool (润色工具)

**用途**: 多维度润色文本

**输入**:
```python
class PolishTextInput(ToolInput):
    content: str = Field(..., min_length=10, max_length=20000, description="需要润色的文本")
    aspects: List[str] = Field(
        default_factory=lambda: ["grammar", "expression", "style"],
        description="润色维度(grammar/expression/style/structure)"
    )
    target_style: str = Field(default="professional", description="目标风格")
```

**实现逻辑**: 类似continue_writing_tool,构建润色提示词,调用AI服务

#### 3.1.3 expand_text_tool (扩写工具)

**用途**: 扩写文本,增加细节

**输入**:
```python
class ExpandTextInput(ToolInput):
    content: str = Field(..., min_length=10, max_length=10000, description="需要扩写的文本")
    expansion_points: List[str] = Field(default_factory=list, description="需要重点扩展的要点")
    target_length: int = Field(default=1000, ge=200, le=5000, description="目标字数")
    detail_level: str = Field(default="medium", pattern="^(low|medium|high)$", description="细节程度")
```

### 3.2 Analysis Tools (分析工具)

**文件位置**: `backend/app/services/agent/tools/analysis_tools.py`

#### 3.2.1 analyze_content_tool (内容分析工具)

**用途**: 多维度分析文本内容

**输入**:
```python
class AnalyzeContentInput(ToolInput):
    content: str = Field(..., min_length=10, max_length=20000, description="需要分析的文本")
    aspects: List[str] = Field(
        default_factory=lambda: ["grammar", "logic", "style", "structure"],
        description="分析维度"
    )
    depth: str = Field(default="normal", pattern="^(shallow|normal|deep)$", description="分析深度")
    context: str = Field(default="", description="上下文信息")
```

**输出**:
```python
class AnalyzeContentOutput(ToolOutput):
    data: Dict  # {
        # summary: 分析摘要
        # issues: 发现的问题列表 [{type, description, severity}]
        # suggestions: 改进建议列表 [string]
        # scores: 各维度评分 {grammar: 85, logic: 90, style: 88, structure: 87}
    # }
```

**核心实现**:
```python
async def analyze_content_executor(input_data: AnalyzeContentInput) -> AnalyzeContentOutput:
    """内容分析执行器"""
    try:
        # 构建分析维度描述
        aspect_descriptions = {
            "grammar": "语法错误和用词不当",
            "logic": "逻辑连贯性和因果关系",
            "style": "写作风格和表达方式",
            "structure": "文章结构和段落组织"
        }

        selected_aspects = "\n".join([
            f"- {aspect}: {aspect_descriptions.get(aspect, aspect)}"
            for aspect in input_data.aspects
        ])

        # 构建分析提示词
        prompt = f"""你是一位专业的文本分析专家。请对以下文本进行全面分析。

【待分析文本】
{input_data.content}

【分析维度】
{selected_aspects}

【分析深度】{input_data.depth}
{'【上下文】' + input_data.context if input_data.context else ''}

【输出格式】
## 分析摘要
[整体评价]

## 详细分析
### [维度1]
[分析内容]

### [维度2]
[分析内容]

## 主要问题
1. [问题描述]
2. [问题描述]

## 改进建议
1. [建议内容]
2. [建议内容]

## 评分 (0-100)
- [维度1]: [分数]
- [维度2]: [分数]
"""

        # 调用AI服务
        analysis_text = await _generate_text(
            prompt=prompt,
            temperature=0.3,
            max_tokens=3000
        )

        # 解析分析结果
        parsed_result = _parse_analysis_result(analysis_text)

        return AnalyzeContentOutput(
            success=True,
            message="分析完成",
            data=parsed_result
        )

    except Exception as e:
        return AnalyzeContentOutput(
            success=False,
            message=f"分析失败: {str(e)}",
            data=None
        )
```

**结果解析函数**:
```python
def _parse_analysis_result(analysis_text: str) -> Dict:
    """
    解析分析结果

    从AI返回的文本中提取:
    - summary: 分析摘要
    - issues: 问题列表
    - suggestions: 建议列表
    - scores: 评分字典
    """
    result = {
        "summary": "",
        "issues": [],
        "suggestions": [],
        "scores": {}
    }

    # 提取摘要
    if "## 分析摘要" in analysis_text:
        summary_section = analysis_text.split("## 分析摘要")[1].split("##")[0].strip()
        result["summary"] = summary_section

    # 提取问题
    if "## 主要问题" in analysis_text:
        issues_section = analysis_text.split("## 主要问题")[1].split("##")[0].strip()
        issues = [line.strip().lstrip("0123456789. ") for line in issues_section.split("\n") if line.strip()]
        result["issues"] = issues

    # 提取建议
    if "## 改进建议" in analysis_text:
        suggestions_section = analysis_text.split("## 改进建议")[1].split("##")[0].strip()
        suggestions = [line.strip().lstrip("0123456789. ") for line in suggestions_section.split("\n") if line.strip()]
        result["suggestions"] = suggestions

    # 提取评分
    if "## 评分" in analysis_text:
        scores_section = analysis_text.split("## 评分")[1].strip()
        for line in scores_section.split("\n"):
            if ":" in line:
                parts = line.split(":")
                if len(parts) == 2:
                    aspect = parts[0].strip().lstrip("- ")
                    score_str = parts[1].strip()
                    try:
                        score = int(''.join(filter(str.isdigit, score_str)))
                        result["scores"][aspect] = score
                    except:
                        pass

    return result
```

#### 3.2.2 evaluate_quality_tool (质量评估工具)

**用途**: 评估内容质量,打分和等级评定

**输入**:
```python
class EvaluateQualityInput(ToolInput):
    content: str = Field(..., min_length=10, max_length=20000, description="需要评估的文本")
    context: str = Field(default="", description="内容类型(novel/article/essay等)")
    criteria: List[str] = Field(
        default_factory=lambda: ["readability", "creativity", "coherence", "engagement"],
        description="评估标准"
    )
```

**输出**:
```python
class EvaluateQualityOutput(ToolOutput):
    data: Dict  # {
        # overall_score: 总体评分 (0-100)
        # grade: 等级评定 (S/A/B/C/D/F)
        # dimension_scores: 各维度评分 {readability: 85, creativity: 78, ...}
        # strengths: 优势列表 [string]
        # weaknesses: 不足列表 [string]
        # detailed_feedback: 详细反馈
    # }
```

**评分标准**:
```python
# 等级评定
def _calculate_grade(overall_score: int) -> str:
    if overall_score >= 95: return "S"
    elif overall_score >= 85: return "A"
    elif overall_score >= 75: return "B"
    elif overall_score >= 65: return "C"
    elif overall_score >= 55: return "D"
    else: return "F"
```

---

## 4. 监控系统设计

### 4.1 ToolMonitor 类

**文件位置**: `backend/app/services/agent/tools/tool_monitor.py`

#### 核心功能

**1. 双存储支持**
- Redis存储 (生产环境)
- 内存存储 (开发环境)
- 自动降级

**2. 执行日志记录**
```python
def log_execution(
    self,
    tool_name: str,
    execution_time: float,
    success: bool,
    input_data: Optional[Dict] = None,
    output_data: Optional[Dict] = None,
    error: Optional[str] = None,
    metadata: Optional[Dict] = None
):
    """
    记录工具执行日志

    存储到:
    - Redis: tool_monitor:logs:{tool_name}
    - 内存: _memory_logs
    """
```

**3. 统计查询**
```python
def get_tool_stats(self, tool_name: str, days: int = 1) -> Dict:
    """
    获取工具统计信息

    返回:
    {
        "tool_name": "continue_writing",
        "total_count": 100,
        "success_count": 98,
        "failure_count": 2,
        "success_rate": 0.98,
        "avg_execution_time": 1.23,
        "total_execution_time": 123.45,
        "recent_errors": [...]
    }
    """
```

**4. 数据保留策略**
- Redis: 自动过期 (retention_days, 默认7天)
- 内存: 手动清理 (限制1000条)

#### Redis存储结构

```
# 日志存储
tool_monitor:logs:{tool_name}  (Redis List)
[
    {
        "tool_name": "continue_writing",
        "timestamp": "2025-10-31T10:30:00",
        "execution_time": 1.23,
        "success": true,
        "error": null,
        "metadata": {...}
    },
    ...
]

# 统计存储
tool_monitor:stats:{tool_name}  (Redis Hash)
{
    "total_count": "100",
    "success_count": "98",
    "failure_count": "2",
    "total_time": "123.45"
}

# 错误记录
tool_monitor:errors:{tool_name}  (Redis List)
[
    {
        "timestamp": "2025-10-31T10:35:00",
        "error": "Connection timeout"
    },
    ...
]
```

### 4.2 监控集成

在 `StandardTool._log_execution()` 中集成监控:

```python
def _log_execution(self, success, execution_time, error_message=None):
    # 1. 记录到日志文件
    logger.debug(f"工具执行日志: ...")

    # 2. 记录到监控系统 (优雅失败)
    try:
        from .tool_monitor import get_tool_monitor
        monitor = get_tool_monitor()
        monitor.log_execution(
            tool_name=self.name,
            execution_time=execution_time,
            success=success,
            error=error_message,
            metadata={...}
        )
    except Exception as e:
        # 监控系统出错不应该影响工具执行
        logger.warning(f"Failed to log to monitor: {e}")
```

---

## 5. 技术难点和解决方案

### 5.1 泛型类型系统

**难点**: Python泛型类型提示复杂,如何正确实现 `StandardTool[InputT, OutputT]`?

**解决方案**:
```python
from typing import Generic, TypeVar

# 定义类型变量
InputT = TypeVar("InputT", bound=ToolInput)
OutputT = TypeVar("OutputT", bound=ToolOutput)

# 使用Generic
class StandardTool(Generic[InputT, OutputT]):
    def __init__(
        self,
        input_schema: type[InputT],
        output_schema: type[OutputT],
        executor: Callable[[InputT], Awaitable[OutputT]],
        ...
    ):
        ...

    async def execute(self, input_data: InputT) -> OutputT:
        ...
```

**优势**:
- ✅ 编译时类型检查 (IDE支持)
- ✅ 运行时类型验证 (isinstance)
- ✅ 清晰的类型提示

### 5.2 向后兼容

**难点**: 如何在不破坏现有@tool工具的情况下引入StandardTool?

**解决方案**:
1. **双注册表架构**
   - `StandardToolRegistry` (新)
   - `DynamicToolRegistry` (现有)

2. **统一调用接口**
   ```python
   async def call_tool(self, tool_name, params):
       # 优先尝试StandardTool
       if standard_tool := self.get_standard_tool(tool_name):
           return await standard_tool.execute(...)

       # 回退到@tool
       if tool_def := self._dynamic_registry.get_tool(tool_name):
           return await self._dynamic_registry.call_tool(tool_name, params)
   ```

3. **零破坏性修改**
   - 不修改现有@tool工具
   - 不修改现有调用代码
   - 透明切换

### 5.3 异步转同步 (LangChain集成)

**难点**: LangChain工具需要同步函数,但StandardTool是异步的?

**解决方案**:
```python
def to_langchain_tool(self):
    def sync_wrapper(**kwargs):
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

    return Tool(
        name=self.name,
        description=self.description,
        func=sync_wrapper,
        args_schema=self.input_schema
    )
```

### 5.4 监控系统优雅失败

**难点**: 监控系统故障不应该影响工具执行?

**解决方案**:
```python
def _log_execution(self, ...):
    # 1. 必须的日志记录
    logger.debug(f"工具执行日志: ...")

    # 2. 可选的监控记录 (优雅失败)
    try:
        monitor = get_tool_monitor()
        monitor.log_execution(...)
    except Exception as e:
        # 只记录警告,不抛出异常
        logger.warning(f"Failed to log to monitor: {e}")

    # 3. 工具执行继续
```

### 5.5 AI结果解析

**难点**: AI返回的格式不固定,如何稳定提取结构化数据?

**解决方案**:
1. **使用固定的输出格式提示词**
   ```python
   prompt = """
   【输出格式】
   ## 分析摘要
   [内容]

   ## 主要问题
   1. [问题1]
   2. [问题2]

   ## 评分
   - 语法: [分数]
   - 逻辑: [分数]
   """
   ```

2. **灵活的解析逻辑**
   ```python
   def _parse_analysis_result(text):
       result = {"summary": "", "issues": [], "scores": {}}

       # 提取摘要 (section分割)
       if "## 分析摘要" in text:
           summary_section = text.split("## 分析摘要")[1].split("##")[0].strip()
           result["summary"] = summary_section

       # 提取问题 (列表解析)
       if "## 主要问题" in text:
           issues_section = text.split("## 主要问题")[1].split("##")[0].strip()
           result["issues"] = [
               line.strip().lstrip("0123456789. ")
               for line in issues_section.split("\n")
               if line.strip()
           ]

       # 提取评分 (正则表达式)
       if "## 评分" in text:
           for line in text.split("## 评分")[1].split("\n"):
               if ":" in line:
                   aspect, score = line.split(":")
                   result["scores"][aspect.strip()] = int(score.strip())

       return result
   ```

3. **默认值兜底**
   ```python
   result = {
       "summary": parsed.get("summary", "分析完成"),
       "issues": parsed.get("issues", []),
       "suggestions": parsed.get("suggestions", []),
       "scores": parsed.get("scores", {})
   }
   ```

---

## 6. 使用示例

### 6.1 创建和注册工具

```python
from app.services.agent.tools import (
    StandardTool,
    ToolInput,
    ToolOutput,
    ToolCategory,
    registry
)
from pydantic import Field

# 1. 定义输入模型
class MyToolInput(ToolInput):
    text: str = Field(..., min_length=1, max_length=1000)
    options: List[str] = Field(default_factory=list)

# 2. 定义输出模型
class MyToolOutput(ToolOutput):
    pass  # 使用默认的 success, message, data, metadata

# 3. 定义执行器
async def my_tool_executor(input_data: MyToolInput) -> MyToolOutput:
    try:
        # 处理逻辑
        result = process_text(input_data.text, input_data.options)

        return MyToolOutput(
            success=True,
            message="处理成功",
            data={"result": result},
            metadata={"input_length": len(input_data.text)}
        )
    except Exception as e:
        return MyToolOutput(
            success=False,
            message=f"处理失败: {str(e)}",
            data=None
        )

# 4. 创建工具实例
my_tool = StandardTool(
    name="my_tool",
    description="我的自定义工具",
    category=ToolCategory.UTILITY,
    input_schema=MyToolInput,
    output_schema=MyToolOutput,
    executor=my_tool_executor,
    tags=["custom", "utility"],
    version="1.0.0"
)

# 5. 注册工具
registry.register_standard_tool(my_tool)
```

### 6.2 调用工具

**方法1: 直接调用**
```python
from app.services.agent.tools import continue_writing_tool, ContinueWritingInput

# 创建输入
input_data = ContinueWritingInput(
    context="主角走进了房间,四周一片寂静。",
    requirements="继续描写主角的所见所闻",
    target_length=300,
    style="悬疑紧张"
)

# 执行工具
result = await continue_writing_tool.execute(input_data)

if result.success:
    print(f"生成的文本: {result.data['generated_text']}")
    print(f"字数: {result.data['word_count']}")
else:
    print(f"执行失败: {result.message}")
```

**方法2: 通过Registry调用**
```python
from app.services.agent.tools import registry

# 通过统一接口调用
result = await registry.call_tool("continue_writing", {
    "context": "主角走进了房间,四周一片寂静。",
    "requirements": "继续描写主角的所见所闻",
    "target_length": 300,
    "style": "悬疑紧张"
})

if result['success']:
    print(f"生成的文本: {result['data']['generated_text']}")
else:
    print(f"执行失败: {result['message']}")
```

### 6.3 转换为LangChain Tool

```python
from app.services.agent.tools import continue_writing_tool

# 转换为LangChain Tool
langchain_tool = continue_writing_tool.to_langchain_tool()

# 在LangGraph中使用
from langgraph.prebuilt import ToolNode

tool_node = ToolNode([langchain_tool])
```

### 6.4 查看统计信息

```python
from app.services.agent.tools import continue_writing_tool

# 获取工具统计
stats = continue_writing_tool.get_statistics()

print(f"执行次数: {stats['execution_count']}")
print(f"成功率: {stats['success_rate']:.2%}")
print(f"平均执行时间: {stats['avg_execution_time']:.3f}s")
```

### 6.5 监控查询

```python
from app.services.agent.tools import get_tool_monitor

# 获取监控器
monitor = get_tool_monitor()

# 查询工具统计
stats = monitor.get_tool_stats("continue_writing", days=7)

print(f"7天内执行: {stats['total_count']} 次")
print(f"成功率: {stats['success_rate']:.2%}")
print(f"平均耗时: {stats['avg_execution_time']:.3f}s")

# 查看最近错误
for error in stats['recent_errors']:
    print(f"{error['timestamp']}: {error['error']}")
```

---

## 7. 最佳实践

### 7.1 工具设计原则

1. **单一职责** - 每个工具只做一件事
2. **清晰的输入输出** - 使用Pydantic明确定义
3. **详细的文档** - description清晰描述功能
4. **合理的验证** - Field级别的验证规则
5. **统一的错误处理** - 返回标准化的ToolOutput

### 7.2 命名规范

**工具名称** (name):
- 使用小写字母 + 下划线
- 清晰描述功能
- 示例: `continue_writing`, `analyze_content`

**类名称**:
- 使用PascalCase
- 输入: `{ToolName}Input`
- 输出: `{ToolName}Output`
- 示例: `ContinueWritingInput`, `AnalyzeContentOutput`

**执行器名称**:
- 使用小写字母 + 下划线
- 格式: `{tool_name}_executor`
- 示例: `continue_writing_executor`

### 7.3 输入验证建议

```python
class MyToolInput(ToolInput):
    # 字符串长度限制
    text: str = Field(..., min_length=10, max_length=10000)

    # 数值范围限制
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    # 枚举验证
    mode: str = Field(default="normal", pattern="^(normal|advanced)$")

    # 列表验证
    options: List[str] = Field(default_factory=list, max_items=10)

    # 可选字段
    extra_info: Optional[str] = Field(default=None)
```

### 7.4 错误处理模式

```python
async def my_tool_executor(input_data: MyToolInput) -> MyToolOutput:
    try:
        # 1. 参数验证 (Pydantic自动处理)

        # 2. 业务逻辑
        result = await process_data(input_data)

        # 3. 返回成功结果
        return MyToolOutput(
            success=True,
            message="处理成功",
            data={"result": result},
            metadata={"processing_time": time.time() - start_time}
        )

    except ValidationError as e:
        # 验证错误
        return MyToolOutput(
            success=False,
            message=f"输入验证失败: {str(e)}",
            data=None,
            metadata={"validation_error": str(e)}
        )

    except ConnectionError as e:
        # 网络错误
        return MyToolOutput(
            success=False,
            message=f"网络连接失败: {str(e)}",
            data=None,
            metadata={"error_type": "connection"}
        )

    except Exception as e:
        # 未知错误
        logger.error(f"Unexpected error in my_tool: {str(e)}", exc_info=True)
        return MyToolOutput(
            success=False,
            message=f"未知错误: {str(e)}",
            data=None,
            metadata={"error_type": "unknown"}
        )
```

### 7.5 性能优化建议

1. **控制AI生成长度**
   ```python
   max_tokens = int(target_length * 1.5)  # 留20-50%余量
   ```

2. **使用合适的temperature**
   ```python
   # 创作类: 0.7-0.9 (更有创意)
   # 分析类: 0.3-0.5 (更稳定)
   # 严格任务: 0.0-0.2 (确定性)
   ```

3. **批量处理**
   ```python
   # 多个分析任务可以并发执行
   results = await asyncio.gather(
       analyze_content_tool.execute(input1),
       analyze_content_tool.execute(input2),
       analyze_content_tool.execute(input3)
   )
   ```

4. **缓存常用结果**
   ```python
   # 对于相同输入,可以缓存结果
   cache_key = hashlib.md5(input_data.json().encode()).hexdigest()
   if cache_key in cache:
       return cache[cache_key]
   ```

### 7.6 测试建议

1. **使用Mock Service**
   ```python
   class MockHTTPAIService:
       async def _stream_chat(self, messages, max_tokens, temperature):
           # 返回固定的模拟数据
           yield "模拟的AI响应", None
           yield "", {"total_tokens": 100}

   # 设置Mock Service
   set_ai_service(MockHTTPAIService())
   ```

2. **测试各种输入情况**
   ```python
   # 正常输入
   # 边界值输入 (min_length, max_length)
   # 非法输入
   # 空输入
   ```

3. **验证输出格式**
   ```python
   result = await tool.execute(input_data)
   assert result.success is True
   assert "generated_text" in result.data
   assert len(result.data["generated_text"]) > 0
   ```

---

## 📚 相关文档

- [阶段一任务清单](./10_阶段一任务清单.md)
- [实施路线图](./09_实施路线图.md)
- [Week2 任务跟踪](../../tasks/Week2_任务跟踪.md)
- [Week2 Day1-3 工作总结](../../tasks/Week2_Day1-3工作总结.md)

---

**文档完成** ✅
**最后更新**: 2025-10-31
