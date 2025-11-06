# 合并 alin3.0 和 alin_qianduan 分支功能

## 任务列表

- [ ] 分析两个分支的代码差异
- [ ] 合并 useAgentChat.ts 文件，同时保留两个功能
  - 保留 alin3.0 的会话ID状态管理功能
  - 保留 alin_qianduan 的任务时间记录功能
- [ ] 测试合并后的代码是否能正常工作

## 详细说明

### alin3.0 分支的特性：
1. ✅ 在组件级别定义 `conversationId` 状态
2. ✅ 在 API 调用时传递保存的 `conversation_id`
3. ✅ 在 `onStart` 回调中保存会话ID到状态
4. ✅ 在清空消息时重置会话ID

### alin_qianduan 分支的特性：
1. ✅ 使用 `taskStartTimes` Map 记录每个任务的开始时间
2. ✅ 在 `onTaskStart` 中记录任务开始时间
3. ✅ 在 `onTaskDone` 中计算实际执行时间（如果后端没提供则使用前端计算）
4. ✅ 任务完成后清理时间记录

### 合并策略：
- 保持 alin3.0 的会话ID管理方式（作为组件状态）
- 在 `sendMessageStream` 函数中添加 alin_qianduan 的任务时间追踪逻辑
- 合并两个版本的回调处理逻辑

## 审查
