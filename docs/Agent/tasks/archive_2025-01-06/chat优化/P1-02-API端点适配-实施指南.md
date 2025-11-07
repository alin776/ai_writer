# P1-02: API端点适配 - 实施指南

**任务编号**: P1-02
**所属阶段**: Phase 1 - P1核心功能
**预计时间**: 2天
**状态**: ⏸️ 待开始
**依赖**: Phase 0完成

---

## 🎯 任务目标

修改现有API端点，添加mode参数支持，实现react/planning模式切换，保持向后兼容性。

### 核心成果
- API支持mode参数（react/planning）
- 统一的事件格式
- 向后兼容（默认planning模式）
- 完整的测试覆盖

---

## 📋 Day 1: 数据模型和API修改

### 上午 (4小时): 设计数据模型

#### 任务1.1: 定义ChatMode枚举 (30分钟)

**文件**: `backend/app/models/chat_models.py` (新建)

```python
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class ChatMode(str, Enum):
    """聊天模式枚举"""
    PLANNING = "planning"
    REACT = "react"

    def __str__(self):
        return self.value

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Field(..., description="用户消息", min_length=1)
    mode: Optional[ChatMode] = Field(None, description="聊天模式")
    work_id: Optional[str] = Field(None, description="作品ID")
    chapter_id: Optional[str] = Field(None, description="章节ID")
    conversation_id: Optional[str] = Field(None, description="会话ID")
    context: Optional[Dict[str, Any]] = Field(None, description="额外上下文")

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "message": "帮我写一篇关于AI的文章",
                "mode": "react",
                "work_id": "work_123",
                "conversation_id": "conv_456"
            }
        }

class ChatEvent(BaseModel):
    """聊天事件模型 - React模式"""
    type: str = Field(..., description="事件类型")
    content: Dict[str, Any] = Field(..., description="事件内容")
    timestamp: float = Field(..., description="时间戳")
    session_id: str = Field(..., description="会话ID")
    mode: str = Field("react", description="模式标识")

    class Config:
        schema_extra = {
            "example": {
                "type": "intent_classified",
                "content": {"intent": "writing", "confidence": 0.95},
                "timestamp": 1641234567.890,
                "session_id": "session_123",
                "mode": "react"
            }
        }

class ChatChunk(BaseModel):
    """聊天数据块模型 - Planning模式（兼容现有格式）"""
    content: str = Field(..., description="内容块")
    type: str = Field("content", description="块类型")
    finished: bool = Field(False, description="是否结束")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
    session_id: Optional[str] = Field(None, description="会话ID")
    mode: str = Field("planning", description="模式标识")
```

**检查点**:
- [ ] 文件创建成功
- [ ] 枚举定义正确
- [ ] 模型验证通过
  ```bash
  cd backend
  python -c "from app.models.chat_models import ChatMode, ChatRequest; print('OK')"
  ```

---

#### 任务1.2: 实现事件格式化函数 (1小时)

**文件**: `backend/app/api/v1/formatters.py` (新建)

```python
import json
import time
from typing import Dict, Any
from app.models.chat_models import ChatEvent, ChatChunk

def format_chat_event_to_sse(event: ChatEvent) -> str:
    """
    将ChatEvent转换为SSE格式

    Args:
        event: ChatEvent对象

    Returns:
        SSE格式字符串
    """
    data = {
        "event_type": event.type,
        "content": event.content,
        "timestamp": event.timestamp,
        "session_id": event.session_id,
        "mode": event.mode
    }

    # SSE格式: data: {json}\n\n
    sse_data = f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
    return sse_data

def format_planning_chunk_to_sse(chunk: Dict[str, Any], session_id: str) -> str:
    """
    将planning模式数据块转换为SSE格式

    Args:
        chunk: 数据块字典
        session_id: 会话ID

    Returns:
        SSE格式字符串
    """
    chunk_with_meta = chunk.copy()
    chunk_with_meta["session_id"] = session_id
    chunk_with_meta["mode"] = "planning"

    sse_data = f"data: {json.dumps(chunk_with_meta, ensure_ascii=False)}\n\n"
    return sse_data

def create_error_event(error: Exception, session_id: str, mode: str = "react") -> str:
    """
    创建错误事件

    Args:
        error: 异常对象
        session_id: 会话ID
        mode: 模式

    Returns:
        SSE格式错误事件
    """
    error_event = ChatEvent(
        type="error",
        content={
            "error": str(error),
            "error_type": type(error).__name__,
            "phase": "api"
        },
        timestamp=time.time(),
        session_id=session_id,
        mode=mode
    )

    return format_chat_event_to_sse(error_event)
```

**测试**:
```python
# tests/test_formatters.py
import pytest
from app.api.v1.formatters import format_chat_event_to_sse
from app.models.chat_models import ChatEvent

def test_format_chat_event():
    event = ChatEvent(
        type="test",
        content={"key": "value"},
        timestamp=1234567890.0,
        session_id="test_123",
        mode="react"
    )

    result = format_chat_event_to_sse(event)

    assert "data: " in result
    assert "test_123" in result
    assert result.endswith("\n\n")
```

**检查点**:
- [ ] 格式化函数实现
- [ ] 单元测试通过
- [ ] SSE格式正确

---

### 下午 (4小时): 修改API端点

#### 任务1.3: 修改主API端点 (2小时)

**文件**: `backend/app/api/v1/agent.py` (修改)

```python
from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator, Optional
import logging

from app.models.chat_models import ChatRequest, ChatMode
from app.api.v1.formatters import (
    format_chat_event_to_sse,
    format_planning_chunk_to_sse,
    create_error_event
)
from app.services.agent.langgraph_agent import LangGraphAgent

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/agent/chat/stream")
async def agent_chat_stream(
    request: ChatRequest,
    session_id: str = Header(..., description="会话ID"),
    mode: Optional[str] = Header(None, description="聊天模式")
) -> StreamingResponse:
    """
    Agent聊天流式接口

    支持两种模式:
    - react: 使用chat_stream()，实时流式事件
    - planning: 使用chat_with_planning()，兼容现有逻辑

    Args:
        request: 聊天请求
        session_id: 会话ID
        mode: 聊天模式（可选，默认planning）

    Returns:
        StreamingResponse: 流式响应
    """

    # 确定使用的模式
    actual_mode = ChatMode(mode) if mode else ChatMode.PLANNING
    if request.mode:
        actual_mode = request.mode

    logger.info(f"[API] Chat stream request - mode: {actual_mode}, session: {session_id}")

    try:
        # 根据模式选择处理方式
        if actual_mode == ChatMode.REACT:
            return StreamingResponse(
                handle_react_mode(request, session_id),
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
                handle_planning_mode(request, session_id),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no"
                }
            )

    except Exception as e:
        logger.error(f"[API] Error in chat stream: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="内部服务器错误")


async def handle_react_mode(
    request: ChatRequest,
    session_id: str
) -> AsyncGenerator[str, None]:
    """
    处理React模式

    使用chat_stream()方法，提供实时事件流
    """
    logger.info(f"[API] Handling react mode for session: {session_id}")

    agent = LangGraphAgent()

    # 事件收集器
    events = []

    # 定义回调函数
    async def on_progress(event: Dict):
        """进度事件回调"""
        chat_event = ChatEvent(
            type="progress",
            content=event,
            timestamp=time.time(),
            session_id=session_id,
            mode="react"
        )
        events.append(chat_event)
        yield format_chat_event_to_sse(chat_event)

    async def on_tool_call(tool_name: str, tool_args: Dict):
        """工具调用回调"""
        chat_event = ChatEvent(
            type="tool_call",
            content={"tool": tool_name, "args": tool_args},
            timestamp=time.time(),
            session_id=session_id,
            mode="react"
        )
        events.append(chat_event)
        yield format_chat_event_to_sse(chat_event)

    async def on_content(content: str):
        """内容生成回调"""
        chat_event = ChatEvent(
            type="content",
            content={"text": content},
            timestamp=time.time(),
            session_id=session_id,
            mode="react"
        )
        events.append(chat_event)
        yield format_chat_event_to_sse(chat_event)

    try:
        # 调用chat_stream
        result = await agent.chat_stream(
            message=request.message,
            work_id=request.work_id,
            chapter_id=request.chapter_id,
            conversation_id=request.conversation_id or session_id,
            context=request.context,
            on_progress=on_progress,
            on_tool_call=on_tool_call,
            on_content=on_content
        )

        # 发送最终结果
        final_event = ChatEvent(
            type="completed",
            content={"result": result},
            timestamp=time.time(),
            session_id=session_id,
            mode="react"
        )
        yield format_chat_event_to_sse(final_event)

    except Exception as e:
        logger.error(f"[API] Error in react mode: {str(e)}", exc_info=True)
        yield create_error_event(e, session_id, "react")


async def handle_planning_mode(
    request: ChatRequest,
    session_id: str
) -> AsyncGenerator[str, None]:
    """
    处理Planning模式（保持向后兼容）

    使用chat_with_planning()方法
    """
    logger.info(f"[API] Handling planning mode for session: {session_id}")

    agent = LangGraphAgent()

    try:
        # 调用现有的planning方法
        async for chunk in agent.chat_with_planning(
            message=request.message,
            work_id=request.work_id,
            chapter_id=request.chapter_id,
            conversation_id=request.conversation_id or session_id,
            context=request.context
        ):
            # 转换为统一格式
            yield format_planning_chunk_to_sse(chunk, session_id)

    except Exception as e:
        logger.error(f"[API] Error in planning mode: {str(e)}", exc_info=True)
        error_chunk = {
            "content": f"错误: {str(e)}",
            "type": "error",
            "finished": True,
            "metadata": {"error": True}
        }
        yield format_planning_chunk_to_sse(error_chunk, session_id)
```

**检查点**:
- [ ] API端点修改完成
- [ ] mode参数支持
- [ ] React/Planning分支逻辑
- [ ] 错误处理完善

---

#### 任务1.4: 配置路由 (30分钟)

**文件**: `backend/app/api/v1/__init__.py` (修改)

```python
from fastapi import APIRouter
from app.api.v1 import agent  # 导入修改后的agent路由

api_router = APIRouter()

# 注册agent路由
api_router.include_router(
    agent.router,
    prefix="/agent",
    tags=["agent"]
)
```

**检查点**:
- [ ] 路由注册成功
- [ ] API可访问

---

## 📋 Day 2: 测试和完善

### 上午 (4小时): 单元测试和集成测试

#### 任务2.1: 编写API测试 (2小时)

**文件**: `backend/tests/test_api_chat_stream.py` (新建)

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_stream_default_mode():
    """测试默认模式（应该是planning）"""
    response = client.post(
        "/api/v1/agent/chat/stream",
        json={"message": "测试消息"},
        headers={"session-id": "test_001"}
    )

    assert response.status_code == 200

    # 检查响应包含planning模式标识
    content = response.text
    assert "planning" in content.lower()

def test_chat_stream_react_mode():
    """测试React模式"""
    response = client.post(
        "/api/v1/agent/chat/stream",
        json={"message": "测试消息", "mode": "react"},
        headers={"session-id": "test_002", "mode": "react"}
    )

    assert response.status_code == 200

    # 检查响应包含react模式标识
    content = response.text
    assert "react" in content.lower()

def test_chat_stream_planning_mode():
    """测试Planning模式"""
    response = client.post(
        "/api/v1/agent/chat/stream",
        json={"message": "测试消息", "mode": "planning"},
        headers={"session-id": "test_003", "mode": "planning"}
    )

    assert response.status_code == 200

def test_chat_stream_invalid_mode():
    """测试无效模式"""
    response = client.post(
        "/api/v1/agent/chat/stream",
        json={"message": "测试消息", "mode": "invalid"},
        headers={"session-id": "test_004"}
    )

    # 应该返回400错误
    assert response.status_code == 422  # Validation error

def test_chat_stream_backward_compatibility():
    """测试向后兼容性（不传mode参数）"""
    response = client.post(
        "/api/v1/agent/chat/stream",
        json={"message": "测试消息"},
        headers={"session-id": "test_005"}
        # 注意：不传mode header
    )

    assert response.status_code == 200

    # 应该默认使用planning模式
    content = response.text
    assert "planning" in content.lower()
```

**运行测试**:
```bash
cd backend
python -m pytest tests/test_api_chat_stream.py -v
```

**检查点**:
- [ ] 所有测试通过
- [ ] 覆盖率>80%

---

#### 任务2.2: 手动测试 (2小时)

**测试脚本**: `scripts/test_chat_modes.py`

```python
import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_react_mode():
    """测试React模式"""
    print("=== 测试React模式 ===")

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            f"{BASE_URL}/api/v1/agent/chat/stream",
            json={"message": "写一个Python函数计算斐波那契数列", "mode": "react"},
            headers={"session-id": "manual_test_react"}
        ) as response:
            print(f"Status: {response.status_code}")

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    print(f"Event: {data.get('event_type', 'unknown')} - {data.get('mode')}")

async def test_planning_mode():
    """测试Planning模式"""
    print("\n=== 测试Planning模式 ===")

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            f"{BASE_URL}/api/v1/agent/chat/stream",
            json={"message": "制定一个学习Python的计划", "mode": "planning"},
            headers={"session-id": "manual_test_planning"}
        ) as response:
            print(f"Status: {response.status_code}")

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    print(f"Mode: {data.get('mode')}")

async def test_default_mode():
    """测试默认模式"""
    print("\n=== 测试默认模式（不传mode）===")

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            f"{BASE_URL}/api/v1/agent/chat/stream",
            json={"message": "你好"},
            headers={"session-id": "manual_test_default"}
        ) as response:
            print(f"Status: {response.status_code}")

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    print(f"Mode: {data.get('mode')} (应该是planning)")
                    break

if __name__ == "__main__":
    asyncio.run(test_react_mode())
    asyncio.run(test_planning_mode())
    asyncio.run(test_default_mode())
```

**运行测试**:
```bash
# 启动服务
cd backend
python -m uvicorn app.main:app --reload

# 新终端运行测试
cd backend
python scripts/test_chat_modes.py
```

**检查点**:
- [ ] React模式正常工作
- [ ] Planning模式正常工作
- [ ] 默认模式正确（planning）
- [ ] 事件格式正确

---

### 下午 (4小时): 文档和优化

#### 任务2.3: 更新API文档 (1小时)

**文件**: `docs/API文档.md` (更新)

```markdown
## POST /api/v1/agent/chat/stream

### 描述
Agent聊天流式接口，支持Planning和React两种模式。

### 请求

**Headers**:
- `session-id` (必需): 会话ID
- `mode` (可选): 聊天模式，可选值: `react`, `planning`，默认`planning`

**Body**:
```json
{
  "message": "用户消息",
  "mode": "react",  // 可选，优先级高于Header
  "work_id": "作品ID",  // 可选
  "chapter_id": "章节ID",  // 可选
  "conversation_id": "会话ID",  // 可选
  "context": {}  // 可选，额外上下文
}
```

### 响应

**Content-Type**: `text/event-stream`

**React模式事件**:
```
data: {"event_type": "progress", "content": {...}, "mode": "react", ...}
data: {"event_type": "tool_call", "content": {...}, "mode": "react", ...}
data: {"event_type": "content", "content": {...}, "mode": "react", ...}
data: {"event_type": "completed", "content": {...}, "mode": "react", ...}
```

**Planning模式事件**:
```
data: {"content": "...", "type": "content", "mode": "planning", ...}
data: {"content": "...", "finished": true, "mode": "planning", ...}
```

### 示例

**React模式**:
```bash
curl -X POST http://localhost:8000/api/v1/agent/chat/stream \
  -H "session-id: test_001" \
  -H "mode: react" \
  -H "Content-Type: application/json" \
  -d '{"message": "写一个Python函数"}'
```

**Planning模式（默认）**:
```bash
curl -X POST http://localhost:8000/api/v1/agent/chat/stream \
  -H "session-id: test_002" \
  -H "Content-Type: application/json" \
  -d '{"message": "制定学习计划"}'
```
```

**检查点**:
- [ ] API文档更新
- [ ] 示例正确

---

#### 任务2.4: 性能优化 (2小时)

**优化点**:

1. **添加请求验证**
```python
# 在API端点中添加
if len(request.message) > 10000:
    raise HTTPException(status_code=400, detail="消息过长")
```

2. **添加超时控制**
```python
import asyncio

async def handle_react_mode_with_timeout(request, session_id):
    try:
        async with asyncio.timeout(300):  # 5分钟超时
            async for event in handle_react_mode(request, session_id):
                yield event
    except asyncio.TimeoutError:
        yield create_error_event(
            Exception("请求超时"),
            session_id,
            "react"
        )
```

3. **添加限流**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/agent/chat/stream")
@limiter.limit("10/minute")  # 每分钟10次
async def agent_chat_stream(...):
    ...
```

**检查点**:
- [ ] 添加输入验证
- [ ] 添加超时控制
- [ ] 考虑限流（可选）

---

#### 任务2.5: Code Review (1小时)

**检查清单**:
- [ ] 代码风格符合规范
- [ ] 错误处理完善
- [ ] 日志记录充分
- [ ] 注释清晰
- [ ] 无安全隐患
- [ ] 性能可接受

---

## ✅ 验收标准

### 功能验收
- [ ] API支持mode参数（Header和Body）
- [ ] React模式正常工作
- [ ] Planning模式正常工作
- [ ] 不传mode时默认planning
- [ ] 事件格式统一且正确

### 测试验收
- [ ] 所有单元测试通过
- [ ] 手动测试通过
- [ ] 向后兼容性验证通过

### 代码质量
- [ ] Code Review通过
- [ ] 文档完整
- [ ] 无明显性能问题

---

## 📦 交付物

- [ ] `app/models/chat_models.py` - 数据模型
- [ ] `app/api/v1/formatters.py` - 格式化函数
- [ ] `app/api/v1/agent.py` - 修改后的API端点
- [ ] `tests/test_api_chat_stream.py` - 单元测试
- [ ] `scripts/test_chat_modes.py` - 手动测试脚本
- [ ] `docs/API文档.md` - 更新的API文档

---

## 📝 实施记录

**Day 1**:
- 开始时间: _____
- 完成情况: [ ] 数据模型 [ ] API修改
- 遇到问题: _____
- 解决方案: _____

**Day 2**:
- 开始时间: _____
- 完成情况: [ ] 测试 [ ] 文档 [ ] 优化
- 遇到问题: _____
- 解决方案: _____

**最终状态**: ⏸️ 待开始 → 🔄 进行中 → ✅ 已完成

---

**负责人**: _____
**审核人**: _____
**完成时间**: _____
