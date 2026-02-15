# 会话管理功能 - 后端API设计

**文档版本**: v1.1
**创建时间**: 2025-11-07
**更新时间**: 2025-11-07（标注实际状态）
**文档类型**: 📋 设计方案 + ✅ 部分实现
**实施进度**: 基础API已实现，分支管理API待开发
**验证日期**: 2025-11-08（/chat和/chat/stream已验证）

---

## ⚠️ API实现状态

### 📊 现有 vs 计划

| 接口 | 状态 | 说明 |
|------|------|------|
| `POST /chat` | ✅ 已存在 | conversation_id在请求体中 |
| `POST /chat/stream` | ✅ 已存在 | 支持planning和react模式 |
| `POST /chat/reset` | ❌ **待实现** | 新增功能 |
| `POST /branches` | ❌ **待实现** | 新增功能 |
| `GET /conversations/{id}/branches` | ❌ **待实现** | 新增功能 |
| 其他分支管理接口 | ❌ **待实现** | 新增功能 |

**当前机制**:
```typescript
// 前端生成conversation_id
const conversationId = request.conversation_id || uuid.v4()

// 后端作为LangGraph的thread_id使用
config = {"configurable": {"thread_id": conversationId}}
```

---

## 🌐 API总览

### 基础路径
```
/api/v1/agent
```

### 认证方式
所有接口需要Bearer Token认证：
```
Authorization: Bearer {token}
```

### 计划新增接口清单

以下接口为**计划实现**的新功能：

| 接口 | 方法 | 功能 | 优先级 | 状态 |
|------|------|------|--------|------|
| `/chat/reset` | POST | 重开会话 | P0 | ❌ 待实现 |
| `/branches` | POST | 创建分支 | P0 | ❌ 待实现 |
| `/branches/{id}` | GET | 获取分支详情 | P0 | ❌ 待实现 |
| `/branches/{id}/messages` | GET | 获取分支消息 | P0 | ❌ 待实现 |
| `/branches/{id}/switch` | POST | 切换分支 | P0 | ❌ 待实现 |
| `/conversations/{id}/branches` | GET | 获取会话所有分支 | P1 | ❌ 待实现 |
| `/branches/{id}` | PUT | 更新分支（重命名） | P1 | ❌ 待实现 |
| `/branches/{id}` | DELETE | 删除分支 | P2 | ❌ 待实现 |

---

## 📡 API详细设计

### 1. 重开Session

**接口**: `POST /api/v1/agent/chat/reset`

**功能**: 清空当前对话历史，生成新的conversation_id

**请求体**:
```json
{
  "conversation_id": "conv_xyz789"
}
```

**响应**:
```json
{
  "new_conversation_id": "conv_abc123",
  "message": "会话已重置"
}
```

**Python实现**:
```python
@router.post("/chat/reset")
async def reset_conversation(
    request: ResetConversationRequest,
    current_user: User = Depends(get_current_active_user),
    redis_client: Redis = Depends(get_redis_client),
    checkpointer: AsyncRedisSaver = Depends(get_checkpointer)
):
    \"\"\"重置会话，清空对话历史\"\"\"
    user_id = str(current_user.id)
    old_conv_id = request.conversation_id

    # 1. 验证权限
    conv_data = redis_client.get(f"conversation:{old_conv_id}")
    if not conv_data:
        raise HTTPException(404, "会话不存在")

    conversation = json.loads(conv_data)
    if conversation['userId'] != user_id:
        raise HTTPException(403, "无权操作此会话")

    # 2. 删除旧会话的所有数据
    # 删除会话元数据
    redis_client.delete(f"conversation:{old_conv_id}")

    # 删除分支元数据
    redis_client.delete(f"conversation_branches:{old_conv_id}")

    # 删除LangGraph checkpoint（所有分支）
    for branch_id in conversation['branches']:
        await checkpointer.adelete(
            {"configurable": {"thread_id": branch_id}}
        )

    # 3. 创建新会话
    new_conv_id = str(uuid.uuid4())
    main_branch_id = f"branch_main_{uuid.uuid4().hex[:8]}"

    new_conversation = {
        "id": new_conv_id,
        "userId": user_id,
        "title": "新对话",
        "mainBranchId": main_branch_id,
        "activeBranchId": main_branch_id,
        "branches": [main_branch_id],
        "totalMessages": 0,
        "totalBranches": 1,
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
        "lastActivity": datetime.now().isoformat()
    }

    # 保存新会话
    redis_client.setex(
        f"conversation:{new_conv_id}",
        7 * 24 * 60 * 60,
        json.dumps(new_conversation)
    )

    # 添加到用户索引
    redis_client.zadd(
        f"user:{user_id}:conversations",
        {new_conv_id: time.time()}
    )

    logger.info(f"[Reset] User {user_id} reset conversation {old_conv_id} -> {new_conv_id}")

    return {
        "new_conversation_id": new_conv_id,
        "message": "会话已重置"
    }
```

---

### 2. 创建分支

**接口**: `POST /api/v1/agent/branches`

**功能**: 在指定消息处创建新分支

**请求体**:
```json
{
  "conversation_id": "conv_xyz789",
  "fork_message_id": "msg_abc123",
  "branch_name": "探索方案A"
}
```

**响应**:
```json
{
  "branch_id": "branch_def456",
  "name": "探索方案A",
  "created_at": "2025-11-07T10:45:00Z",
  "message_count": 5
}
```

**Python实现**:
```python
@router.post("/branches", response_model=BranchResponse)
async def create_branch(
    request: CreateBranchRequest,
    current_user: User = Depends(get_current_active_user),
    redis_client: Redis = Depends(get_redis_client),
    checkpointer: AsyncRedisSaver = Depends(get_checkpointer)
):
    \"\"\"创建新分支\"\"\"
    user_id = str(current_user.id)
    conv_id = request.conversation_id

    # 1. 验证权限和会话存在性
    conv_data = redis_client.get(f"conversation:{conv_id}")
    if not conv_data:
        raise HTTPException(404, "会话不存在")

    conversation = json.loads(conv_data)
    if conversation['userId'] != user_id:
        raise HTTPException(403, "无权操作此会话")

    # 2. 获取当前活跃分支的消息
    current_branch_id = conversation['activeBranchId']
    config = {"configurable": {"thread_id": current_branch_id}}
    state = await checkpointer.aget(config)

    if not state:
        raise HTTPException(500, "无法获取当前分支状态")

    messages = state.get('messages', [])

    # 3. 找到分叉点消息的索引
    fork_index = -1
    for i, msg in enumerate(messages):
        if msg.get('id') == request.fork_message_id:
            fork_index = i
            break

    if fork_index == -1:
        raise HTTPException(404, "分叉消息不存在")

    # 4. 创建新分支ID
    new_branch_id = f"branch_{uuid.uuid4().hex[:8]}_{uuid.uuid4().hex[:8]}"

    # 5. 复制分叉点之前的消息到新分支
    messages_to_fork = messages[:fork_index + 1]

    # 创建新的checkpoint
    new_state = {
        "messages": messages_to_fork,
        "context": state.get('context', {}),
        "intent": state.get('intent', 'general')
    }

    new_config = {"configurable": {"thread_id": new_branch_id}}
    await checkpointer.aput(new_config, new_state, {})

    # 6. 保存分支元数据
    branch_data = {
        "id": new_branch_id,
        "conversationId": conv_id,
        "name": request.branch_name or f"分支 {len(conversation['branches']) + 1}",
        "parentBranchId": current_branch_id,
        "forkMessageId": request.fork_message_id,
        "isMain": False,
        "isActive": False,
        "messageCount": len(messages_to_fork),
        "lastActivity": datetime.now().isoformat(),
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }

    redis_client.hset(
        f"conversation_branches:{conv_id}",
        new_branch_id,
        json.dumps(branch_data)
    )

    # 7. 更新会话元数据
    conversation['branches'].append(new_branch_id)
    conversation['totalBranches'] = len(conversation['branches'])
    conversation['updatedAt'] = datetime.now().isoformat()

    redis_client.setex(
        f"conversation:{conv_id}",
        7 * 24 * 60 * 60,
        json.dumps(conversation)
    )

    # 8. 记录分支关系
    redis_client.sadd(f"branch_children:{current_branch_id}", new_branch_id)
    redis_client.expire(f"branch_children:{current_branch_id}", 7 * 24 * 60 * 60)

    logger.info(f"[Branch] Created {new_branch_id} from {current_branch_id} at message {request.fork_message_id}")

    return BranchResponse(**branch_data)
```

---

### 3. 切换分支

**接口**: `POST /api/v1/agent/branches/{branch_id}/switch`

**功能**: 切换到指定分支

**路径参数**:
- `branch_id`: 分支ID

**请求体**:
```json
{
  "conversation_id": "conv_xyz789"
}
```

**响应**:
```json
{
  "branch_id": "branch_def456",
  "messages": [
    {
      "id": "msg_1",
      "content": "帮我写个故事",
      "role": "user",
      "created_at": "2025-11-07T10:30:00Z"
    },
    {
      "id": "msg_2",
      "content": "好的，从前有座山...",
      "role": "assistant",
      "created_at": "2025-11-07T10:30:05Z"
    }
  ],
  "message_count": 5
}
```

**Python实现**:
```python
@router.post("/branches/{branch_id}/switch")
async def switch_branch(
    branch_id: str,
    request: SwitchBranchRequest,
    current_user: User = Depends(get_current_active_user),
    redis_client: Redis = Depends(get_redis_client),
    checkpointer: AsyncRedisSaver = Depends(get_checkpointer)
):
    \"\"\"切换到指定分支\"\"\"
    user_id = str(current_user.id)
    conv_id = request.conversation_id

    # 1. 验证权限
    conv_data = redis_client.get(f"conversation:{conv_id}")
    if not conv_data:
        raise HTTPException(404, "会话不存在")

    conversation = json.loads(conv_data)
    if conversation['userId'] != user_id:
        raise HTTPException(403, "无权操作此会话")

    # 2. 验证分支存在
    if branch_id not in conversation['branches']:
        raise HTTPException(404, "分支不存在")

    # 3. 获取目标分支的消息
    config = {"configurable": {"thread_id": branch_id}}
    state = await checkpointer.aget(config)

    if not state:
        raise HTTPException(500, "无法加载分支数据")

    messages = state.get('messages', [])

    # 4. 更新会话的activeBranchId
    old_active_branch = conversation['activeBranchId']
    conversation['activeBranchId'] = branch_id
    conversation['updatedAt'] = datetime.now().isoformat()
    conversation['lastActivity'] = datetime.now().isoformat()

    redis_client.setex(
        f"conversation:{conv_id}",
        7 * 24 * 60 * 60,
        json.dumps(conversation)
    )

    # 5. 更新分支的isActive标记
    # 旧分支设为false
    old_branch_data = redis_client.hget(f"conversation_branches:{conv_id}", old_active_branch)
    if old_branch_data:
        old_branch = json.loads(old_branch_data)
        old_branch['isActive'] = False
        redis_client.hset(
            f"conversation_branches:{conv_id}",
            old_active_branch,
            json.dumps(old_branch)
        )

    # 新分支设为true
    new_branch_data = redis_client.hget(f"conversation_branches:{conv_id}", branch_id)
    if new_branch_data:
        new_branch = json.loads(new_branch_data)
        new_branch['isActive'] = True
        new_branch['lastActivity'] = datetime.now().isoformat()
        redis_client.hset(
            f"conversation_branches:{conv_id}",
            branch_id,
            json.dumps(new_branch)
        )

    logger.info(f"[Branch] User {user_id} switched from {old_active_branch} to {branch_id}")

    # 6. 格式化消息
    formatted_messages = [
        {
            "id": msg.get('id', f"msg_{i}"),
            "content": msg.get('content', ''),
            "role": msg.get('role', 'user'),
            "created_at": msg.get('created_at', datetime.now().isoformat())
        }
        for i, msg in enumerate(messages)
    ]

    return {
        "branch_id": branch_id,
        "messages": formatted_messages,
        "message_count": len(formatted_messages)
    }
```

---

### 4. 获取会话所有分支

**接口**: `GET /api/v1/agent/conversations/{conversation_id}/branches`

**功能**: 获取会话的分支树结构

**路径参数**:
- `conversation_id`: 会话ID

**响应**:
```json
{
  "conversation_id": "conv_xyz789",
  "branches": [
    {
      "id": "branch_main",
      "name": "主线",
      "is_main": true,
      "is_active": false,
      "message_count": 4,
      "children": ["branch_abc", "branch_def"]
    },
    {
      "id": "branch_abc",
      "name": "探索方案A",
      "is_main": false,
      "is_active": true,
      "message_count": 7,
      "children": []
    }
  ],
  "total_branches": 3
}
```

**Python实现**:
```python
@router.get("/conversations/{conversation_id}/branches")
async def get_conversation_branches(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user),
    redis_client: Redis = Depends(get_redis_client)
):
    \"\"\"获取会话的所有分支\"\"\"
    user_id = str(current_user.id)

    # 1. 验证权限
    conv_data = redis_client.get(f"conversation:{conversation_id}")
    if not conv_data:
        raise HTTPException(404, "会话不存在")

    conversation = json.loads(conv_data)
    if conversation['userId'] != user_id:
        raise HTTPException(403, "无权访问此会话")

    # 2. 获取所有分支
    branches_raw = redis_client.hgetall(f"conversation_branches:{conversation_id}")
    branches = []

    for branch_raw in branches_raw.values():
        branch = json.loads(branch_raw)

        # 获取子分支列表
        children = list(redis_client.smembers(f"branch_children:{branch['id']}"))

        branches.append({
            **branch,
            "children": children
        })

    return {
        "conversation_id": conversation_id,
        "branches": branches,
        "total_branches": len(branches)
    }
```

---

### 5. 更新分支（重命名）

**接口**: `PUT /api/v1/agent/branches/{branch_id}`

**功能**: 更新分支信息（主要是重命名）

**路径参数**:
- `branch_id`: 分支ID

**请求体**:
```json
{
  "conversation_id": "conv_xyz789",
  "name": "方案A - 优化版"
}
```

**响应**:
```json
{
  "branch_id": "branch_abc",
  "name": "方案A - 优化版",
  "updated_at": "2025-11-07T11:00:00Z"
}
```

---

### 6. 删除分支

**接口**: `DELETE /api/v1/agent/branches/{branch_id}`

**功能**: 删除指定分支（软删除，保留30天）

**路径参数**:
- `branch_id`: 分支ID

**查询参数**:
- `conversation_id`: 会话ID
- `force`: 是否强制删除（默认false，软删除）

**响应**:
```json
{
  "message": "分支已删除",
  "deleted_branch_id": "branch_abc",
  "deleted_at": "2025-11-07T11:00:00Z"
}
```

**注意事项**:
- 不能删除主分支
- 不能删除当前活跃分支
- 删除父分支时需要处理子分支

---

## 🔐 认证和权限

### 权限检查中间件

```python
async def check_conversation_permission(
    conversation_id: str,
    user_id: str,
    redis_client: Redis
) -> dict:
    \"\"\"检查用户对会话的访问权限\"\"\"
    conv_data = redis_client.get(f"conversation:{conversation_id}")

    if not conv_data:
        raise HTTPException(
            status_code=404,
            detail="会话不存在"
        )

    conversation = json.loads(conv_data)

    if conversation['userId'] != user_id:
        raise HTTPException(
            status_code=403,
            detail="无权访问此会话"
        )

    return conversation
```

---

## 📊 错误处理

### 标准错误响应

```json
{
  "error": {
    "code": "BRANCH_NOT_FOUND",
    "message": "分支不存在",
    "details": "Branch ID: branch_abc not found in conversation conv_xyz789"
  },
  "request_id": "req_123456",
  "timestamp": "2025-11-07T11:00:00Z"
}
```

### 错误码定义

| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| `CONVERSATION_NOT_FOUND` | 404 | 会话不存在 |
| `BRANCH_NOT_FOUND` | 404 | 分支不存在 |
| `UNAUTHORIZED` | 403 | 无权访问 |
| `INVALID_FORK_MESSAGE` | 400 | 分叉消息无效 |
| `CANNOT_DELETE_MAIN_BRANCH` | 400 | 不能删除主分支 |
| `CANNOT_DELETE_ACTIVE_BRANCH` | 400 | 不能删除活跃分支 |
| `CHECKPOINT_ERROR` | 500 | Checkpoint操作失败 |

---

## ✅ API测试

### cURL示例

```bash
# 1. 重开会话
curl -X POST http://localhost:8000/api/v1/agent/chat/reset \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "conv_xyz789"}'

# 2. 创建分支
curl -X POST http://localhost:8000/api/v1/agent/branches \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_xyz789",
    "fork_message_id": "msg_abc123",
    "branch_name": "探索方案A"
  }'

# 3. 切换分支
curl -X POST http://localhost:8000/api/v1/agent/branches/branch_abc/switch \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "conv_xyz789"}'
```

---

**下一步**: 阅读 `06_前端组件设计.md` 了解React组件架构
