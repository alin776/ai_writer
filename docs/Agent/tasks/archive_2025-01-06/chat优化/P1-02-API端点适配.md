# P1-02-API端点适配：支持mode参数

## 📋 文档信息

- **优先级**：P1（核心功能）
- **预估工作量**：2-3天（需要处理两种模式的事件格式统一）
- **依赖**：P1-01-chat_stream实现完成
- **验收标准**：API层支持mode参数，可以切换planning和react模式

---

## 🎯 功能概述

修改现有API端点，添加`mode`参数支持，允许前端选择使用planning模式或react模式。保持向后兼容性，逐步迁移到新的chat_stream机制。

### 核心目标

1. **模式切换**：支持"planning"和"react"两种模式
2. **向后兼容**：现有API调用不受影响
3. **统一接口**：API层统一处理两种模式
4. **灵活配置**：支持全局和会话级模式设置

---

## 🔍 技术分析

### 当前API现状

**现有的agent_chat_stream端点**：

```python
# 当前的API实现
@router.post("/agent/chat/stream")
async def agent_chat_stream(
    request: ChatRequest,
    session_id: str = Header(...),
    # 其他参数...
):
    """
    硬编码使用planning模式
    """
    # 直接调用chat_with_planning
    async for chunk in agent.chat_with_planning(
        message=request.message,
        session_id=session_id,
        model_selector=model_selector,
        **kwargs
    ):
        yield chunk
```

**问题分析**：
- ❌ 硬编码planning模式，无法选择其他模式
- ❌ 无法利用新的chat_stream能力
- ❌ 缺乏灵活性，不满足A/B测试需求
- ❌ 扩展性差，新增模式需要修改API

### 目标API设计

**支持mode参数的API**：

```python
# 目标API实现
@router.post("/agent/chat/stream")
async def agent_chat_stream(
    request: ChatRequest,
    session_id: str = Header(...),
    mode: str = Header("planning")  # 新增mode参数
):
    """
    支持planning和react两种模式
    """
    # 根据mode选择执行方式
    if mode == "react":
        # 使用新的chat_stream
        async for event in agent.chat_stream(
            message=request.message,
            session_id=session_id,
            model_selector=model_selector,
            **kwargs
        ):
            yield _format_chat_event(event)
    else:
        # 默认使用planning模式（向后兼容）
        async for chunk in agent.chat_with_planning(
            message=request.message,
            session_id=session_id,
            model_selector=model_selector,
            **kwargs
        ):
            yield chunk
```

---

## 🏗️ 实现方案

### 1. 数据模型扩展

```python
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, Any

class ChatMode(str, Enum):
    """聊天模式枚举"""
    PLANNING = "planning"
    REACT = "react"

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Field(..., description="用户消息")
    mode: Optional[ChatMode] = Field(None, description="聊天模式")
    model_selector: Optional[Dict[str, Any]] = Field(None, description="模型选择器")
    context: Optional[Dict[str, Any]] = Field(None, description="额外上下文")

    class Config:
        use_enum_values = True

class ChatEvent(BaseModel):
    """聊天事件模型"""
    type: str = Field(..., description="事件类型")
    content: Dict[str, Any] = Field(..., description="事件内容")
    timestamp: float = Field(..., description="时间戳")
    session_id: str = Field(..., description="会话ID")
    mode: str = Field(..., description="当前模式")

class ChatChunk(BaseModel):
    """聊天数据块模型（兼容现有格式）"""
    content: str = Field(..., description="内容块")
    type: str = Field("content", description="块类型")
    finished: bool = Field(False, description="是否结束")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
```

### 2. API端点修改

```python
from fastapi import Header, HTTPException, Depends
from fastapi.responses import StreamingResponse
import json

@router.post("/agent/chat/stream")
async def agent_chat_stream(
    request: ChatRequest,
    session_id: str = Header(..., description="会话ID"),
    mode: ChatMode = Header(ChatMode.PLANNING, description="聊天模式"),
    user_context: UserContext = Depends(get_user_context)
) -> StreamingResponse:
    """
    Agent聊天流式接口

    Args:
        request: 聊天请求
        session_id: 会话ID
        mode: 聊天模式（planning或react）
        user_context: 用户上下文

    Returns:
        StreamingResponse: 流式响应
    """

    try:
        # 获取模型选择器
        model_selector = _create_model_selector(
            request.model_selector,
            user_context,
            request.mode
        )

        # 根据模式选择处理方式
        if mode == ChatMode.REACT:
            return StreamingResponse(
                _handle_react_mode(request, session_id, model_selector),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no"  # 禁用Nginx缓冲
                }
            )
        else:
            # 默认使用planning模式（向后兼容）
            return StreamingResponse(
                _handle_planning_mode(request, session_id, model_selector),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no"
                }
            )

    except Exception as e:
        logger.error(f"API错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="内部服务器错误")

async def _handle_react_mode(
    request: ChatRequest,
    session_id: str,
    model_selector: ModelSelector
) -> AsyncGenerator[str, None]:
    """处理react模式"""

    try:
        async for event in agent.chat_stream(
            message=request.message,
            session_id=session_id,
            model_selector=model_selector,
            **(request.context or {})
        ):
            # 转换事件为SSE格式
            sse_data = _format_chat_event_to_sse(event, session_id)
            yield sse_data

    except Exception as e:
        # 发送错误事件
        error_event = ChatEvent(
            type="error",
            content={"error": str(e), "phase": "api"},
            timestamp=time.time(),
            session_id=session_id,
            mode="react"
        )
        yield _format_chat_event_to_sse(error_event, session_id)

async def _handle_planning_mode(
    request: ChatRequest,
    session_id: str,
    model_selector: ModelSelector
) -> AsyncGenerator[str, None]:
    """处理planning模式（保持向后兼容）"""

    try:
        async for chunk in agent.chat_with_planning(
            message=request.message,
            session_id=session_id,
            model_selector=model_selector,
            **(request.context or {})
        ):
            # 转换为现有格式
            sse_data = _format_planning_chunk_to_sse(chunk, session_id)
            yield sse_data

    except Exception as e:
        error_chunk = {
            "content": f"错误: {str(e)}",
            "type": "error",
            "finished": True,
            "metadata": {"error": True}
        }
        yield _format_planning_chunk_to_sse(error_chunk, session_id)
```

### 3. 事件格式化

```python
def _format_chat_event_to_sse(event: ChatEvent, session_id: str) -> str:
    """将ChatEvent转换为SSE格式"""

    # 构建SSE数据
    data = {
        "event_type": event.type,
        "content": event.content,
        "timestamp": event.timestamp,
        "session_id": session_id,
        "mode": "react"
    }

    # 转换为SSE格式
    sse_data = f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
    return sse_data

def _format_planning_chunk_to_sse(chunk: Dict[str, Any], session_id: str) -> str:
    """将planning模式数据块转换为SSE格式"""

    # 添加元数据
    chunk_with_meta = chunk.copy()
    chunk_with_meta["session_id"] = session_id
    chunk_with_meta["mode"] = "planning"

    # 转换为SSE格式
    sse_data = f"data: {json.dumps(chunk_with_meta, ensure_ascii=False)}\n\n"
    return sse_data

# 示例输出格式：

# React模式事件：
# data: {
#   "event_type": "intent_classified",
#   "content": {"intent": "writing", "confidence": 0.9},
#   "timestamp": 1641234567.890,
#   "session_id": "session_123",
#   "mode": "react"
# }

# Planning模式事件（保持兼容）：
# data: {
#   "content": "正在分析您的需求...",
#   "type": "content",
#   "finished": false,
#   "metadata": {"phase": "analysis"},
#   "session_id": "session_123",
#   "mode": "planning"
# }
```

### 4. 模型选择器处理

```python
def _create_model_selector(
    request_selector: Optional[Dict[str, Any]],
    user_context: UserContext,
    mode: Optional[ChatMode]
) -> ModelSelector:
    """创建模型选择器"""

    # 基础配置
    config = {
        "user_id": user_context.user_id,
        "user_level": user_context.level,
        "mode": mode or ChatMode.PLANNING
    }

    # 合并请求中的配置
    if request_selector:
        config.update(request_selector)

    # 根据模式调整模型选择策略
    if mode == ChatMode.REACT:
        # React模式倾向于使用更快的模型
        config["prefer_fast_model"] = True
        config["enable_caching"] = True
    else:
        # Planning模式可以使用更强的模型
        config["prefer_fast_model"] = False
        config["enable_caching"] = False

    return ModelSelector(config)
```

### 5. 配置管理

```python
# config/chat_modes.py
class ChatModeConfig:
    """聊天模式配置"""

    @staticmethod
    def get_default_mode(user_level: str) -> ChatMode:
        """根据用户等级获取默认模式"""
        mode_mapping = {
            "free": ChatMode.REACT,      # 免费用户使用react模式（成本控制）
            "basic": ChatMode.REACT,     # 基础用户使用react模式
            "premium": ChatMode.PLANNING,  # 高级用户使用planning模式
            "enterprise": ChatMode.PLANNING  # 企业用户使用planning模式
        }
        return mode_mapping.get(user_level, ChatMode.REACT)

    @staticmethod
    def is_mode_available(user_level: str, mode: ChatMode) -> bool:
        """检查用户是否可以使用指定模式"""
        if mode == ChatMode.PLANNING:
            return user_level in ["premium", "enterprise"]
        return True  # React模式对所有用户开放

    @staticmethod
    def get_mode_limits(user_level: str, mode: ChatMode) -> Dict[str, Any]:
        """获取模式使用限制"""
        limits = {
            "free": {
                "react": {"requests_per_hour": 20, "max_tokens": 2000},
                "planning": {"requests_per_hour": 0}  # 不可用
            },
            "basic": {
                "react": {"requests_per_hour": 100, "max_tokens": 4000},
                "planning": {"requests_per_hour": 10, "max_tokens": 8000}
            },
            "premium": {
                "react": {"requests_per_hour": 500, "max_tokens": 8000},
                "planning": {"requests_per_hour": 100, "max_tokens": 16000}
            }
        }
        return limits.get(user_level, {}).get(mode.value, {})
```

---

## 📝 实施步骤

### 上午（4小时）：基础框架搭建

**1. 数据模型定义（1小时）**
- 创建ChatMode枚举
- 扩展ChatRequest模型
- 定义ChatEvent模型

**2. API端点修改（2小时）**
- 修改agent_chat_stream端点
- 添加mode参数支持
- 实现模式选择逻辑

**3. 事件格式化（1小时）**
- 实现SSE格式化函数
- 确保向后兼容性

### 下午（4小时）：功能完善

**1. 模型选择器集成（1小时）**
- 修改模型选择器创建逻辑
- 添加模式相关的配置

**2. 配置管理（1小时）**
- 实现ChatModeConfig
- 添加用户权限检查

**3. 测试和文档（2小时）**
- 编写单元测试
- 更新API文档

---

## 🧪 测试策略

### 1. 单元测试

```python
# 测试模式切换
@pytest.mark.asyncio
async def test_mode_switching():
    """测试不同模式的选择"""

    # React模式测试
    request = ChatRequest(
        message="测试消息",
        mode=ChatMode.REACT
    )

    # 验证选择了正确的处理方法
    response = await client.post(
        "/agent/chat/stream",
        json=request.dict(),
        headers={"session-id": "test_001", "mode": "react"}
    )

    # Planning模式测试
    request_planning = ChatRequest(
        message="测试消息",
        mode=ChatMode.PLANNING
    )

    response_planning = await client.post(
        "/agent/chat/stream",
        json=request_planning.dict(),
        headers={"session-id": "test_002", "mode": "planning"}
    )

# 测试向后兼容性
@pytest.mark.asyncio
async def test_backward_compatibility():
    """测试向后兼容性"""

    # 不传mode参数，应该默认使用planning
    request = ChatRequest(message="测试消息")

    response = await client.post(
        "/agent/chat/stream",
        json=request.dict(),
        headers={"session-id": "test_003"}
        # 注意：不传mode header
    )

    # 验证响应格式与原来一致
    async for chunk in response.aiter_text():
        data = json.loads(chunk.split("data: ")[1])
        assert "mode" in data
        assert data["mode"] == "planning"
```

### 2. 集成测试

```python
# 测试完整流程
@pytest.mark.asyncio
async def test_full_chat_flow():
    """测试完整的聊天流程"""

    test_cases = [
        {
            "mode": "react",
            "message": "写一个Python函数",
            "expected_events": ["intent_classified", "agent_thinking", "response_complete"]
        },
        {
            "mode": "planning",
            "message": "制定一个学习计划",
            "expected_chunks": ["content", "finished"]
        }
    ]

    for case in test_cases:
        request = ChatRequest(
            message=case["message"],
            mode=ChatMode(case["mode"])
        )

        response = await client.post(
            "/agent/chat/stream",
            json=request.dict(),
            headers={"session-id": f"test_{case['mode']}", "mode": case["mode"]}
        )

        # 验证响应内容
        if case["mode"] == "react":
            await _verify_react_response(response, case["expected_events"])
        else:
            await _verify_planning_response(response, case["expected_chunks"])
```

### 3. 性能测试

```python
# 测试API性能
@pytest.mark.asyncio
async def test_api_performance():
    """测试API性能"""

    modes = ["react", "planning"]

    for mode in modes:
        start_time = time.time()

        request = ChatRequest(
            message="简单对话测试",
            mode=ChatMode(mode)
        )

        async with client.stream(
            "POST",
            "/agent/chat/stream",
            json=request.dict(),
            headers={"session-id": f"perf_test_{mode}", "mode": mode}
        ) as response:
            async for chunk in response.aiter_text():
                pass  # 消费所有数据

        end_time = time.time()
        response_time = end_time - start_time

        # 验证响应时间
        assert response_time < 10.0, f"{mode}模式响应时间过长: {response_time}s"
```

---

## 📊 预期收益

### 1. 功能增强

- **模式选择**：用户可以选择最适合的执行模式
- **A/B测试**：可以对比不同模式的效果
- **渐进迁移**：支持逐步从planning迁移到react

### 2. 向后兼容性

- **无破坏性变更**：现有API调用不受影响
- **平滑过渡**：可以逐步引导用户使用新模式
- **风险控制**：可以随时回退到原有模式

### 3. 扩展性

- **模式扩展**：未来可以轻松添加新的执行模式
- **配置灵活**：支持多种配置策略
- **监控支持**：可以监控不同模式的使用情况

---

## ⚠️ 风险评估

### 中风险

1. **兼容性问题**：可能影响现有客户端
   - **缓解措施**：严格的向后兼容测试
   - **监控方案**：监控API调用失败率

2. **性能影响**：新模式可能影响API性能
   - **缓解措施**：详细的性能测试
   - **监控指标**：响应时间、错误率

### 低风险

1. **配置复杂性**：配置管理可能变得复杂
   - **缓解措施**：详细的文档和测试
   - **默认策略**：提供合理的默认值

---

## 🔗 相关文档

### 依赖文档
- [P1-01-实现chat_stream.md](./P1-01-实现chat_stream.md) - chat_stream实现
- [P0-01-修复task_type传递.md](./P0-01-修复task_type传递.md) - 确保模型选择正确

### 相关文档
- [P1-03-前端事件处理.md](./P1-03-前端事件处理.md) - 前端如何处理事件
- [P2-01-监控日志.md](./P2-01-监控日志.md) - 监控不同模式的使用情况

---

## 📝 实施记录

### 问题记录
*（实施过程中记录遇到的问题和解决方案）*

### 变更记录
*（记录对方案的修改和调整）*

### 测试结果
*（记录测试结果和性能指标）*

---

## ✅ 验收标准

- [ ] API端点支持mode参数
- [ ] React模式可以正常工作
- [ ] Planning模式保持向后兼容
- [ ] 不传mode参数时默认使用planning
- [ ] 支持用户权限检查
- [ ] 所有单元测试通过
- [ ] 集成测试验证完整流程
- [ ] 性能测试满足要求
- [ ] API文档更新完整

---

**文档版本**：v1.0
**创建时间**：2025-01-05
**预计完成时间**：P1-01完成后1天内
**负责人**：API开发团队