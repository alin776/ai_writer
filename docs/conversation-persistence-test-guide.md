# 对话持久化功能 - 测试指南

## 🧪 测试步骤

### 测试1: 基本持久化功能

**目标**: 验证对话能在刷新页面后恢复

1. 打开浏览器 http://localhost:5174/works/你的作品ID
2. 选择任意章节（比如"第一章"）
3. 打开右侧"AI对话"面板
4. 发送一条消息，比如："帮我写第一章的开头"
5. 等待AI回复
6. **刷新浏览器** (F5)
7. ✅ **期望结果**: 对话历史自动恢复，之前的消息还在

### 测试2: 章节隔离功能

**目标**: 验证不同章节有独立的对话历史

1. 在"第一章"的AI面板发送："帮我写第一章"
2. 等待AI回复
3. **切换到"第二章"**
4. ✅ **期望结果**: AI面板对话清空（因为这是新章节）
5. 发送："第二章要写什么？"
6. 等待AI回复
7. **切换回"第一章"**
8. ✅ **期望结果**: 自动恢复第一章的对话历史（"帮我写第一章"和AI回复）
9. **切换到"第二章"**
10. ✅ **期望结果**: 自动恢复第二章的对话历史（"第二章要写什么？"和AI回复）

### 测试3: 切换面板不丢失

**目标**: 验证切换右侧面板时对话不丢失

1. 在"第一章"的AI面板发送消息
2. 等待AI回复
3. **切换到"世界观"面板**
4. 查看世界观内容
5. **切换回"AI对话"面板**
6. ✅ **期望结果**: 对话历史还在

### 测试4: 对话历史管理（仅适用于AgentChatPanel）

**目标**: 验证对话历史管理UI

**注意**: 此功能仅在 `AgentChatPanel` 组件中可用，不在 `AIPanel` 中

1. 打开独立的Agent对话页面
2. 点击右上角"📚 历史"按钮
3. ✅ **期望结果**: 显示历史对话列表
4. 点击"➕ 新建对话"
5. ✅ **期望结果**: 清空当前对话，开始新对话
6. 发送几条消息后，再次打开历史
7. ✅ **期望结果**: 看到刚才创建的对话

## 🔍 调试方法

### 查看浏览器控制台日志

按 F12 打开开发者工具，切换到 Console 标签，应该能看到：

```
[Persistence] 找到chapter_chapter-001的会话: session_xxx
[Persistence] Restored session session_xxx: 5 messages
[useAgentChat] 恢复历史会话 session_xxx: 5 条消息
```

### 查看localStorage数据

在 Console 中输入：

```javascript
// 查看上下文映射
console.log(JSON.parse(localStorage.getItem('agent_context_session_map')))

// 查看特定章节的会话ID
const map = JSON.parse(localStorage.getItem('agent_context_session_map'))
console.log('章节1的会话ID:', map['chapter_你的章节ID'])

// 查看会话数据
const sessionId = map['chapter_你的章节ID']
console.log(JSON.parse(localStorage.getItem(`agent_conversation_${sessionId}`)))
```

### 清空所有数据（重置测试）

```javascript
// 清空所有对话数据
localStorage.removeItem('agent_context_session_map')
localStorage.removeItem('agent_conversation_sessions')
Object.keys(localStorage)
  .filter(key => key.startsWith('agent_conversation_session_'))
  .forEach(key => localStorage.removeItem(key))
console.log('已清空所有对话数据')

// 刷新页面
location.reload()
```

## ❌ 常见问题排查

### 问题1: 刷新后对话消失

**检查点**:
1. 打开 Console，看是否有 `[Persistence]` 或 `[useAgentChat]` 的日志
2. 检查 localStorage 是否有数据：
   ```javascript
   Object.keys(localStorage).filter(k => k.startsWith('agent_'))
   ```
3. 如果没有数据，说明保存失败，检查是否有JavaScript错误

### 问题2: 切换章节后对话没有切换

**检查点**:
1. 打开 Console，看是否有 `[Persistence] 找到chapter_xxx的会话` 日志
2. 检查上下文映射表：
   ```javascript
   console.log(JSON.parse(localStorage.getItem('agent_context_session_map')))
   ```
3. 验证 `AIPanel` 是否正确传递了 `chapterId`

### 问题3: 对话历史按钮不显示

**原因**: `AIPanel` 组件没有对话历史管理UI，只有 `AgentChatPanel` 有

**解决**: 对话历史功能仅在独立的Agent对话页面可用，作品详情页的AI面板不显示历史按钮（但数据仍然持久化）

## ✅ 预期行为总结

| 场景 | 预期行为 |
|------|---------|
| 刷新页面 | 对话历史自动恢复 |
| 切换章节 | 自动切换到对应章节的对话 |
| 切换面板 | 对话不丢失 |
| 关闭浏览器 | 数据保存在localStorage |
| 第二天打开 | 对话历史还在 |

## 🎯 成功标准

- ✅ 刷新页面后对话不丢失
- ✅ 章节A的对话 ≠ 章节B的对话
- ✅ 切换回章节A能看到之前的对话
- ✅ Console没有错误
- ✅ localStorage有数据

---

**测试环境**: http://localhost:5174/
**浏览器**: Chrome/Edge/Firefox（推荐Chrome）
**测试时间**: 2025-11-22

如有问题，请查看浏览器Console的错误信息。
