# 会话管理功能 - 开发任务清单（后端优先版）

**项目**: AI Writer 智能写作助手 - 会话管理功能
**创建时间**: 2025-11-08
**更新时间**: 2025-11-08（调整为后端优先）
**状态**: 待确认
**策略**: 先完成后端 → 再实现前端

---

## 📊 策略分析：为什么先做后端？

### ✅ 采用"后端优先"的理由

1. **验证技术可行性**
   - 最大风险：LangGraph AsyncRedisSaver 是否支持分支操作？
   - 后端先行可快速验证，避免前端白做

2. **API设计稳定**
   - 后端API确定后，前端基于稳定接口开发
   - 减少返工风险

3. **独立测试**
   - 用 Postman/pytest 直接测试后端
   - 不依赖前端UI

4. **简单原则**
   - 每次专注一个领域，降低复杂度
   - 符合"尽可能简单"的原则

5. **前端改动量大**
   - 预估前端需新增/修改约1000行代码
   - 2个新组件（BranchPanel、BranchTreeView）
   - 如果后端不可行，避免浪费前端时间

---

## 🎯 Sprint 1: 后端核心API（第1天，预计8小时）

### 任务 1.1: 重开Session API（1.5小时）

- [ ] 在 `backend/app/api/v1/agent.py` 添加数据模型
  - [ ] 创建 `ResetConversationRequest` 类
  ```python
  class ResetConversationRequest(BaseModel):
      conversation_id: str = Field(..., description="要重置的会话ID")
  ```
  - [ ] 创建 `ResetConversationResponse` 类
  ```python
  class ResetConversationResponse(BaseModel):
      new_conversation_id: str = Field(..., description="新的会话ID")
      message: str = Field(default="会话已重置", description="提示消息")
  ```

- [ ] 实现 `reset_conversation()` 接口（agent.py:200）
  - [ ] 接收 conversation_id 参数
  - [ ] 验证用户权限
  - [ ] 调用 AsyncRedisSaver 删除 checkpoint 数据
  - [ ] 删除 Redis 中的会话元数据（如果有）
  - [ ] 生成新的 conversation_id（使用 uuid.uuid4()）
  - [ ] 返回 ResetConversationResponse
  - [ ] 添加日志记录
  - [ ] 添加错误处理（try/except）

- [ ] Postman 测试
  - [ ] 创建测试请求
  - [ ] 验证返回的 new_conversation_id 不同
  - [ ] 验证旧会话数据已清空

---

### 任务 1.2: 创建分支 API（2.5小时）

- [ ] 在 `backend/app/api/v1/agent.py` 添加数据模型
  - [ ] 创建 `CreateBranchRequest` 类
  ```python
  class CreateBranchRequest(BaseModel):
      conversation_id: str = Field(..., description="当前会话ID")
      fork_point_message_index: int = Field(..., description="分叉点消息索引（从0开始）")
      branch_name: Optional[str] = Field(None, description="分支名称（可选）")
  ```
  - [ ] 创建 `BranchResponse` 类
  ```python
  class BranchResponse(BaseModel):
      branch_id: str = Field(..., description="分支ID（新的thread_id）")
      parent_branch_id: str = Field(..., description="父分支ID")
      branch_name: str = Field(..., description="分支名称")
      fork_point_index: int = Field(..., description="分叉点索引")
      message_count: int = Field(0, description="分支中的消息数")
      created_at: str = Field(..., description="创建时间")
  ```

- [ ] 实现 `create_branch()` 接口（agent.py:220）
  - [ ] 验证用户权限
  - [ ] 验证参数完整性
  - [ ] 使用 AsyncRedisSaver.alist() 获取当前分支的所有 checkpoint
  - [ ] 找到分叉点对应的 checkpoint
  - [ ] 创建新的 branch_id（thread_id）
  - [ ] 复制分叉点之前的 checkpoint 到新分支
  - [ ] 保存分支元数据到 Redis
    ```python
    # Redis key: branch:{branch_id}
    {
      "branch_id": "xxx",
      "parent_branch_id": "xxx",
      "branch_name": "xxx",
      "fork_point_index": 3,
      "created_at": "2025-11-08T10:00:00",
      "is_active": False
    }
    ```
  - [ ] 更新会话的 branches 列表
    ```python
    # Redis key: conversation:{conversation_id}:branches
    # Set: {branch_id1, branch_id2, ...}
    ```
  - [ ] 返回 BranchResponse
  - [ ] 添加日志和错误处理

- [ ] Postman 测试
  - [ ] 创建分支
  - [ ] 验证返回的 branch_id
  - [ ] 验证 Redis 中的元数据

---

### 任务 1.3: 切换分支 API（2小时）

- [ ] 在 `backend/app/api/v1/agent.py` 添加数据模型
  - [ ] 创建 `SwitchBranchRequest` 类
  ```python
  class SwitchBranchRequest(BaseModel):
      branch_id: str = Field(..., description="要切换到的分支ID")
  ```
  - [ ] 创建 `SwitchBranchResponse` 类
  ```python
  class SwitchBranchResponse(BaseModel):
      branch_id: str
      branch_name: str
      messages: List[Dict[str, Any]] = Field(..., description="分支的消息历史")
  ```

- [ ] 实现 `switch_branch()` 接口（agent.py:300）
  - [ ] 验证分支存在性（检查 Redis 元数据）
  - [ ] 使用 AsyncRedisSaver.alist() 获取分支的 checkpoint 列表
  - [ ] 解析 checkpoint 获取消息历史
  - [ ] 更新会话的 activeBranchId
  - [ ] 更新分支的 isActive 标记
  - [ ] 返回 SwitchBranchResponse（包含消息列表）
  - [ ] 添加日志和错误处理

- [ ] Postman 测试
  - [ ] 切换到已存在的分支
  - [ ] 验证返回的消息历史
  - [ ] 验证 activeBranchId 已更新

---

### 任务 1.4: 获取分支列表 API（1.5小时）

- [ ] 在 `backend/app/api/v1/agent.py` 添加数据模型
  - [ ] 创建 `BranchTreeNode` 类
  ```python
  class BranchTreeNode(BaseModel):
      branch_id: str
      parent_branch_id: Optional[str]
      branch_name: str
      message_count: int
      is_active: bool
      created_at: str
      children: List["BranchTreeNode"] = Field(default_factory=list)
  ```
  - [ ] 创建 `GetBranchesResponse` 类
  ```python
  class GetBranchesResponse(BaseModel):
      conversation_id: str
      branches: List[BranchTreeNode] = Field(..., description="分支树")
  ```

- [ ] 实现 `get_conversation_branches()` 接口（agent.py:350）
  - [ ] 从 Redis 获取会话的所有分支ID
  - [ ] 批量获取分支元数据（使用 Redis Pipeline）
  - [ ] 构建分支关系树
    - [ ] 找到根分支（parent_branch_id 为 None）
    - [ ] 递归构建子分支
  - [ ] 返回 GetBranchesResponse
  - [ ] 添加日志和错误处理

- [ ] Postman 测试
  - [ ] 获取分支列表
  - [ ] 验证树形结构
  - [ ] 验证分支关系正确

---

### 任务 1.5: 后端测试（1小时）

- [ ] Postman 集成测试
  - [ ] 完整流程测试
    1. 发送消息创建会话
    2. 创建分支
    3. 切换分支
    4. 获取分支列表
    5. 重开会话
  - [ ] 边界情况测试
    - [ ] 不存在的分支ID
    - [ ] 无效的分叉点索引
    - [ ] 空会话创建分支
  - [ ] 并发测试
    - [ ] 同时创建多个分支
    - [ ] 快速切换分支

- [ ] 性能测试
  - [ ] 测试 Redis 查询性能
  - [ ] 测试分支切换响应时间（目标 < 500ms）

- [ ] 文档记录
  - [ ] 记录测试结果
  - [ ] 记录发现的问题

---

## 🚀 Sprint 2: 前端基础功能（第2天，预计6小时）

### 任务 2.1: API 服务层（1小时）

- [ ] 在 `src/services/agentApi.ts` 添加方法
  - [ ] 创建 `resetConversation()` 方法
  - [ ] 创建 `createBranch()` 方法
  - [ ] 创建 `switchBranch()` 方法
  - [ ] 创建 `getConversationBranches()` 方法

- [ ] 在 `src/types/agent.ts` 添加类型定义
  - [ ] ResetConversationRequest/Response
  - [ ] CreateBranchRequest/Response
  - [ ] SwitchBranchRequest/Response
  - [ ] BranchTreeNode
  - [ ] GetBranchesResponse

---

### 任务 2.2: 重开会话按钮（1小时）

- [ ] 在 `src/components/agent/AgentChatPanel.tsx` 添加UI
  - [ ] 在工具栏添加"重开会话"按钮
  - [ ] 实现确认对话框
  - [ ] 调用 `agentApi.resetConversation()`
  - [ ] 清空本地消息状态
  - [ ] 更新 conversationId
  - [ ] 显示成功提示

---

### 任务 2.3: 简单分支列表组件（3小时）

- [ ] 创建 `src/components/agent/BranchPanel.tsx`（简化版）
  - [ ] 显示分支列表（扁平列表，不是树形）
  - [ ] 每个分支显示：
    - [ ] 分支名称
    - [ ] 消息数
    - [ ] 创建时间
    - [ ] 是否活跃（高亮显示）
  - [ ] 实现点击切换分支
  - [ ] 调用 `agentApi.switchBranch()`
  - [ ] 更新消息列表
  - [ ] 显示加载状态

- [ ] 在 `src/components/agent/AgentChatPanel.tsx` 集成
  - [ ] 添加"分支管理"按钮（工具栏）
  - [ ] 侧边栏显示 BranchPanel
  - [ ] 处理分支切换后的消息加载

---

### 任务 2.4: 创建分支功能（1小时）

- [ ] 在 `src/components/agent/AgentChatPanel.tsx` 添加
  - [ ] 在每条AI消息旁添加"创建分支"图标（hover显示）
  - [ ] 点击弹出对话框，输入分支名称
  - [ ] 调用 `agentApi.createBranch()`
  - [ ] 刷新分支列表
  - [ ] 显示成功提示

---

## 🎨 Sprint 3: 前端增强（第3天，预计8小时，可选）

### 任务 3.1: 树形视图（4小时）

- [ ] 创建 `src/components/agent/BranchTreeView.tsx`
  - [ ] 递归渲染树形结构
  - [ ] 展开/折叠功能
  - [ ] 显示分支图标（📁/📌）
  - [ ] 样式美化

---

### 任务 3.2: 编辑消息分支（3小时）

- [ ] 后端 API（1.5小时）
  - [ ] 实现 `edit_message_and_branch()` 接口

- [ ] 前端实现（1.5小时）
  - [ ] 在 `AgentMessage.tsx` 添加编辑按钮
  - [ ] 编辑后自动创建分支

---

### 任务 3.3: 分支管理（1小时）

- [ ] 重命名分支
- [ ] 删除分支
- [ ] 分支详情

---

## 🧪 Sprint 4: 测试优化（0.5天，可选）

### 任务 4.1: 端到端测试（2小时）
- [ ] 完整流程测试
- [ ] 性能测试

### 任务 4.2: 优化（1小时）
- [ ] Redis Pipeline 优化
- [ ] 前端缓存

### 任务 4.3: 文档（1小时）
- [ ] 更新文档
- [ ] 使用示例

---

## 📋 验收标准

### Sprint 1（后端）验收标准
- [ ] Postman 可以成功调用所有API
- [ ] 可以重开会话，Redis中数据清空
- [ ] 可以创建分支，元数据正确保存
- [ ] 可以切换分支，消息历史正确返回
- [ ] 可以获取分支列表，树形结构正确
- [ ] 所有API有错误处理和日志

### Sprint 2（前端基础）验收标准
- [ ] 可以点击按钮重开会话
- [ ] 可以看到分支列表
- [ ] 可以切换分支，消息正确显示
- [ ] 可以创建新分支
- [ ] UI 交互流畅

### Sprint 3（前端增强）验收标准
- [ ] 树形视图美观易用
- [ ] 编辑消息自动创建分支
- [ ] 可以管理分支（重命名、删除）

---

## ⚠️ 风险评估

### 高风险项

1. **LangGraph API 兼容性**（P0 风险）
   - 风险：AsyncRedisSaver 可能不支持我们想要的分支操作
   - 应对：Sprint 1 第一时间验证，如不可行立即调整方案
   - 降级方案：自定义实现分支管理，不依赖 LangGraph

2. **Redis 数据一致性**（中风险）
   - 风险：并发操作可能导致数据不一致
   - 应对：使用 Redis 事务（MULTI/EXEC）
   - 测试：并发测试验证

3. **性能问题**（中风险）
   - 风险：大量分支时查询可能变慢
   - 应对：使用 Redis Pipeline 批量查询
   - 测试：性能测试（目标 < 500ms）

---

## 📊 开发进度跟踪

### Sprint 1: 后端核心API（Day 1）
| 任务 | 预计时间 | 实际时间 | 状态 | 备注 |
|------|---------|---------|------|------|
| 1.1 重开Session API | 1.5h | - | ⏳ 待开始 | |
| 1.2 创建分支 API | 2.5h | - | ⏳ 待开始 | |
| 1.3 切换分支 API | 2h | - | ⏳ 待开始 | |
| 1.4 获取分支列表 API | 1.5h | - | ⏳ 待开始 | |
| 1.5 后端测试 | 1h | - | ⏳ 待开始 | |

### Sprint 2: 前端基础（Day 2）
| 任务 | 预计时间 | 实际时间 | 状态 | 备注 |
|------|---------|---------|------|------|
| 2.1 API 服务层 | 1h | - | ⏳ 待开始 | |
| 2.2 重开会话按钮 | 1h | - | ⏳ 待开始 | |
| 2.3 简单分支列表 | 3h | - | ⏳ 待开始 | |
| 2.4 创建分支功能 | 1h | - | ⏳ 待开始 | |

---

## 审查部分（完成后填写）

### Sprint 1 完成情况
- 待填写

### Sprint 2 完成情况
- 待填写

### 遇到的问题
- 待填写

### 解决方案
- 待填写

### 后续优化建议
- 待填写

---

**下一步**: 确认计划后，开始 Sprint 1 - 任务 1.1（重开Session API）
