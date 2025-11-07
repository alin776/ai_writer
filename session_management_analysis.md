# AI写作项目 - 会话对话管理系统深度分析

## 执行摘要

本项目采用**三层混合存储架构**管理会话和对话：
- **即时层**（Redis）：对话历史checkpoints，7天过期
- **中期层**（Redis）：用户偏好和记忆，90天过期  
- **长期层**（PostgreSQL）：评审记录、人工审查，永久保存

## 一、会话/对话存储

### 1.1 LangGraph状态持久化（生产推荐）

**文件**：`backend/app/services/agent/langgraph_agent.py`

关键技术：AsyncRedisSaver（Redis checkpoint）
- 每个conversation_id对应一个Redis键
- 自动保存完整对话历史和上下文
- 7天TTL自动过期

### 1.2 MemoryManager用户记忆系统

**文件**：`backend/app/services/agent/memory/`

三层记忆：
```
短期：最近10条完整消息
中期：最近100条摘要（按重要度）
长期：历史总结（压缩文本）
```

**Redis键结构**：
```
user:{user_id}:preferences        # 用户偏好
user:{user_id}:profile            # 用户画像
user:{user_id}:recent_conversations  # 最近对话
```

## 二、数据库模型

### UserSession（登录会话）
位置：`backend/app/models/user_session.py`
- 管理用户身份认证
- 与对话无直接关联

### ReviewSession（评审会话）
位置：`backend/app/models/review_session.py`
- 存储AI评审结果（段落/章节/作品）
- 多维度评分、建议、问题列表
- 永久保存

### HumanizeSession（去痕迹会话）
位置：`backend/app/models/humanize_session.py`
- 追踪AI特征消除功能执行
- 核心数据永久保存，详情30天清理

## 三、API接口

### POST /api/v1/agent/chat（非流式）
- 请求：message, conversation_id(可选)
- 响应：response, conversation_id, agent_steps, metadata

### POST /api/v1/agent/chat/stream（流式Planning）
- SSE实时推送规划、任务进度
- 支持task_start/task_progress/task_done回调

### POST /api/v1/agent/chat/react-stream（流式ReAct）
- SSE实时推送节点执行进度
- 支持progress/tool_call回调

**会话管理关键点**：
```python
conversation_id = request.conversation_id or str(uuid.uuid4())
# 传递给LangGraph作为thread_id
config = {"configurable": {"thread_id": conversation_id}}
# 自动从Redis恢复历史消息
result = await agent_graph.chat(..., conversation_id=...)
```

## 四、前端交互

### AgentChatPanel（Planning模式）
文件：`src/components/agent/AgentChatPanel.tsx`

状态管理：
```typescript
const [conversationId, setConversationId] = useState<string | null>(null);
const [useStreaming, setUseStreaming] = useState(true);

// 发送消息时传递conversation_id
const request = {
  message,
  conversation_id: conversationId  // 关键！
};

// 收到响应时保存conversation_id
if (response?.conversation_id) {
  setConversationId(response.conversation_id);
}
```

### useAgentChat Hook（Planning）
文件：`src/hooks/useAgentChat.ts`
- 管理messages[]、isLoading等状态
- 调用agentApi.chat()和agentApi.chatStream()

### useAgentChatStream Hook（ReAct）
文件：`src/hooks/useAgentChatStream.ts`
- 管理currentProgress、toolCalls等状态
- 处理SSE事件流

### agentApi服务
文件：`src/services/agentApi.ts`
- `chat()` 非流式请求
- `chatStream()` Planning流式监听
- `chatReactStream()` ReAct流式监听

## 五、关键流程

### 会话生命周期

```
用户第1条消息（无conversation_id）
  ↓
后端生成UUID作为conversation_id
  ↓
创建AsyncRedisSaver checkpoint
  ↓
执行Agent（从空消息列表开始）
  ↓
保存状态到Redis（conversation_id作为key）
  ↓
返回conversation_id给前端

用户第2条消息（传递conversation_id）
  ↓
后端查询Redis: langgraph_checkpoint_{conversation_id}
  ↓
恢复完整的消息历史和上下文
  ↓
新消息追加到历史
  ↓
Agent使用完整历史生成回复
  ↓
更新Redis中的checkpoint
  ↓
更新用户记忆（Memory Manager）
```

### 用户记忆自动更新

```
每次chat()后 → memory.record_user_interaction()
  ↓
1. 追踪到user_profile（行为统计）
  ↓
2. 更新user_preferences（常用操作）
  ↓
3. 追加到recent_conversations（对话摘要）
  ↓
下次chat() → get_complete_context() 自动读取
  ↓
Agent使用更新后的记忆生成更个性化的回复
```

## 六、存储对比

| 位置 | 生命周期 | 访问速度 | 用途 |
|------|---------|---------|------|
| Redis Checkpoint | 7天 | 毫秒 | 对话历史 |
| Redis KeyValue | 90天 | 毫秒 | 用户偏好 |
| PostgreSQL | 永久 | 秒 | 评审记录 |

## 七、关键文件速查

后端：
- `app/services/agent/langgraph_agent.py` - Agent核心实现
- `app/services/agent/memory/memory_manager.py` - 记忆管理
- `app/api/v1/agent.py` - /chat 和 /chat/stream 端点
- `app/api/v1/agent_react_stream.py` - /chat/react-stream 端点

前端：
- `src/components/agent/AgentChatPanel.tsx` - Planning主UI
- `src/hooks/useAgentChat.ts` - Planning Hook
- `src/hooks/useAgentChatStream.ts` - ReAct Hook
- `src/services/agentApi.ts` - API服务封装

## 八、常见问题

Q: 为什么不在数据库存储对话？
A: Redis毫秒级访问，适合频繁查询；数据库用于永久存储和分析。

Q: 消息如何跨请求保持？
A: 通过conversation_id标识，LangGraph自动从Redis恢复。

Q: 用户记忆如何自动更新？
A: 每次chat()后自动调用memory.record_user_interaction()追踪。

Q: 7天后对话丢失怎么办？
A: Redis过期，但用户偏好保留90天；可开始新会话继承特征。

Q: ReAct和Planning有什么区别？
A: 两个独立的API端点和Hook；对话历史存储方式相同。

