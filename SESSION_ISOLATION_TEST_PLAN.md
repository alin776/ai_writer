# 跨会话泄漏修复 - 测试方案

## 📋 修复概述

本次修复解决了三个核心的跨会话泄漏问题：
1. **LocalStorage 跨标签页泄漏**（严重）
2. **全局状态变量污染**（中等）
3. **SSE连接缺少客户端标识**（轻微）

---

## 🧪 测试计划

### 测试环境准备

1. **启动开发服务器**
   ```bash
   npm run dev
   ```

2. **打开浏览器开发者工具**
   - 打开 Console 标签（查看日志）
   - 打开 Application 标签 → Storage → Session Storage（查看 tabId）
   - 打开 Application 标签 → Storage → Local Storage（查看会话数据）

3. **启用调试模式**
   在浏览器控制台执行：
   ```javascript
   // 查看当前标签页信息
   window.__tabDebug.getTabInfo()

   // 输出示例：
   // {
   //   tabId: "tab_1234567890_abc123",
   //   createdAt: "2025-01-08T10:30:00.000Z",
   //   age: 15.234,
   //   isNew: false
   // }
   ```

---

## 测试用例1：跨标签页隔离验证（核心测试）

### 🎯 目标
验证不同标签页的会话是否完全隔离，不会互相泄漏消息。

### 📝 测试步骤

#### 步骤1：打开第一个标签页
1. 访问 `http://localhost:5173/work/xxx/chapter/123`
2. 打开控制台，查看日志：
   ```
   [TabIdentifier] 新标签页创建: {tabId: "tab_xxx_yyy", ...}
   [Persistence] 🔒 找到chapter_123_tab_xxx_yyy的会话 (tabId: tab_xxx_yyy): session_xxx
   ```
3. 记录 `tabId` 和 `sessionId`（例如：`tab_A` 和 `session_A`）

#### 步骤2：在第一个标签页发送消息
1. 在输入框输入："帮我写第三章"
2. 点击发送
3. 观察控制台日志：
   ```
   [Persistence] 🔒 已保存会话 session_A [chapter_123_tab_A, tabId: tab_A]: 2 messages
   ```
4. 等待 AI 回复完成

#### 步骤3：打开第二个标签页（同一章节）
1. **重要**：复制第一个标签页的 URL
2. 在**新标签页**中打开相同的 URL
3. 观察控制台日志（应该是新的 tabId）：
   ```
   [TabIdentifier] 新标签页创建: {tabId: "tab_xxx_zzz", ...}
   [Persistence] 🔒 找到chapter_123_tab_xxx_zzz的会话 (tabId: tab_xxx_zzz): session_B
   ```
4. **关键验证**：
   - ✅ `tabId` 应该不同（`tab_B` ≠ `tab_A`）
   - ✅ `sessionId` 应该不同（`session_B` ≠ `session_A`）
   - ✅ 第二个标签页应该是**空白对话**（没有第一个标签页的消息）

#### 步骤4：在第二个标签页发送不同的消息
1. 在输入框输入："分析这段文字"
2. 点击发送
3. 观察控制台日志：
   ```
   [Persistence] 🔒 已保存会话 session_B [chapter_123_tab_B, tabId: tab_B]: 2 messages
   ```

#### 步骤5：验证隔离性
1. 切换回第一个标签页
2. **验证点1**：第一个标签页仍然显示"帮我写第三章"的对话（没有第二个标签页的消息）
3. 切换到第二个标签页
4. **验证点2**：第二个标签页仍然显示"分析这段文字"的对话（没有第一个标签页的消息）
5. 打开 Local Storage，查看存储结构：
   ```
   agent_context_session_map:
   {
     "chapter_123_tab_A": "session_A",
     "chapter_123_tab_B": "session_B"
   }

   agent_conversation_session_A: {...}
   agent_conversation_session_B: {...}
   ```

### ✅ 预期结果

- ✅ 两个标签页有**不同的 tabId**
- ✅ 两个标签页有**不同的 sessionId**
- ✅ 两个标签页的**对话历史完全隔离**
- ✅ 标签页A的消息**不会出现**在标签页B
- ✅ 标签页B的消息**不会出现**在标签页A
- ✅ localStorage 中有两个独立的会话记录

### ❌ 失败标志（如果看到以下情况说明修复失败）

- ❌ 两个标签页的 `tabId` 相同
- ❌ 两个标签页的 `sessionId` 相同
- ❌ 标签页B看到了标签页A的消息
- ❌ 标签页A看到了标签页B的消息
- ❌ localStorage 中只有一个会话记录

---

## 测试用例2：刷新页面后的持久化

### 🎯 目标
验证刷新页面后，同一标签页能正确恢复会话历史。

### 📝 测试步骤

1. 在标签页中发送几条消息（建立会话历史）
2. 记录当前的 `tabId`（例如：`tab_A`）
3. 按 `F5` 或点击刷新按钮
4. 观察控制台日志：
   ```
   [Persistence] 🔒 找到chapter_123_tab_A的会话 (tabId: tab_A): session_A
   [useAgentChat] 🔄 恢复会话 session_A: 4 条消息
   ```

### ✅ 预期结果

- ✅ 刷新后 `tabId` **保持不变**（因为使用 sessionStorage）
- ✅ 刷新后 `sessionId` **保持不变**
- ✅ 所有历史消息**正确恢复**
- ✅ AI 思考过程（activities/tasks）**正确恢复**

---

## 测试用例3：多标签页并行请求

### 🎯 目标
验证多个标签页同时发送请求时，SSE 流不会互相干扰。

### 📝 测试步骤

1. 打开标签页A，发送消息："帮我写第三章"（不要等待回复）
2. **立即**打开标签页B，发送消息："分析这段文字"（不要等待回复）
3. 观察两个标签页的控制台和网络请求
4. 验证每个标签页的 SSE 请求头：
   ```
   Request Headers:
   X-Client-ID: tab_A  (标签页A)

   Request Headers:
   X-Client-ID: tab_B  (标签页B)
   ```

### ✅ 预期结果

- ✅ 两个 SSE 连接**独立运行**
- ✅ 标签页A只收到"帮我写第三章"的回复
- ✅ 标签页B只收到"分析这段文字"的回复
- ✅ 不会出现交叉污染

---

## 测试用例4：全局状态隔离（边界测试）

### 🎯 目标
虽然当前项目只有一个 AgentChatPanel 实例，但验证全局状态注释是否正确。

### 📝 测试步骤

1. 打开控制台，执行：
   ```javascript
   // 查看全局状态
   window.sessionManager  // 应该是 undefined（未暴露到全局）
   ```
2. 检查代码注释是否清晰说明了风险和修复方案

### ✅ 预期结果

- ✅ `window.sessionManager` 是 `undefined`（未暴露）
- ✅ 代码注释清晰说明了多实例风险
- ✅ 提供了修复方案（React Context / Zustand）

---

## 测试用例5：压力测试（可选）

### 🎯 目标
验证在极端场景下的稳定性。

### 📝 测试步骤

1. 打开 10 个标签页，都访问同一个章节
2. 在每个标签页发送不同的消息
3. 观察控制台日志和 localStorage

### ✅ 预期结果

- ✅ 每个标签页有独立的 `tabId` 和 `sessionId`
- ✅ localStorage 中有 10 个独立的会话记录
- ✅ 没有内存泄漏或性能问题

---

## 🐛 回归测试清单

修复后需要验证以下功能没有被破坏：

### 基础功能
- [ ] Agent 对话正常发送和接收
- [ ] Planning 模式的任务列表正常显示
- [ ] React 模式的活动流正常显示
- [ ] 建议操作按钮正常工作
- [ ] 清空对话功能正常

### 会话管理
- [ ] 创建新对话按钮正常
- [ ] 切换会话标签页正常
- [ ] 关闭会话标签页正常
- [ ] 会话历史面板正常显示
- [ ] 会话标题自动生成正常

### 持久化
- [ ] 刷新页面后会话正确恢复
- [ ] 浏览器重启后会话正确恢复（localStorage）
- [ ] 关闭标签页后 sessionStorage 正确清除

---

## 📊 测试结果记录

### 测试环境
- **浏览器**: Chrome / Firefox / Safari
- **版本**: ___________
- **日期**: ___________
- **测试人**: ___________

### 测试用例结果

| 用例编号 | 测试项 | 预期结果 | 实际结果 | 通过/失败 | 备注 |
|---------|--------|---------|---------|----------|------|
| 1.1 | 第一个标签页创建 tabId | 唯一 tabId | | ☐ 通过 ☐ 失败 | |
| 1.2 | 第二个标签页创建不同 tabId | 不同 tabId | | ☐ 通过 ☐ 失败 | |
| 1.3 | 两个标签页会话隔离 | 完全隔离 | | ☐ 通过 ☐ 失败 | |
| 2.1 | 刷新后 tabId 保持 | 保持不变 | | ☐ 通过 ☐ 失败 | |
| 2.2 | 刷新后会话恢复 | 正确恢复 | | ☐ 通过 ☐ 失败 | |
| 3.1 | 并行 SSE 请求隔离 | 独立运行 | | ☐ 通过 ☐ 失败 | |
| 3.2 | X-Client-ID 请求头 | 正确携带 | | ☐ 通过 ☐ 失败 | |
| 4.1 | 全局状态未暴露 | undefined | | ☐ 通过 ☐ 失败 | |
| 5.1 | 10个标签页压力测试 | 正常运行 | | ☐ 通过 ☐ 失败 | |

---

## 🔍 调试技巧

### 查看标签页信息
```javascript
// 在控制台执行
window.__tabDebug.getTabInfo()
```

### 查看所有会话映射
```javascript
// 在控制台执行
JSON.parse(localStorage.getItem('agent_context_session_map'))
```

### 查看特定会话数据
```javascript
// 在控制台执行
const sessionId = 'session_xxx_yyy';
JSON.parse(localStorage.getItem(`agent_conversation_${sessionId}`))
```

### 重置标签页ID（调试用）
```javascript
// 在控制台执行
window.__tabDebug.resetTabId()
// 然后刷新页面
```

### 清理所有会话数据
```javascript
// ⚠️ 谨慎使用：会清除所有 Agent 会话数据
Object.keys(localStorage)
  .filter(key => key.startsWith('agent_'))
  .forEach(key => localStorage.removeItem(key));
```

---

## 📝 已知问题和限制

1. **sessionStorage 的生命周期**
   - 标签页关闭后 tabId 会丢失
   - 这是预期行为（防止标签页重新打开时污染旧会话）

2. **隐私模式/无痕浏览**
   - sessionStorage 在隐私模式下可能有限制
   - 建议在正常模式下测试

3. **跨域问题**
   - 如果前后端部署在不同域名，需要配置 CORS 头
   - 确保 `X-Client-ID` 在 CORS 白名单中

---

## ✅ 验收标准

修复被认为成功的标准：

1. **核心功能**
   - ✅ 所有测试用例通过
   - ✅ 没有回归问题
   - ✅ 控制台无错误日志

2. **性能标准**
   - ✅ 页面加载时间不超过 2 秒
   - ✅ 10 个标签页并发无卡顿
   - ✅ localStorage 使用量合理（< 5MB）

3. **代码质量**
   - ✅ 所有注释清晰准确
   - ✅ 代码符合项目规范
   - ✅ 无 TypeScript 错误

---

## 📞 问题反馈

如果测试过程中发现任何问题，请记录以下信息：

- 问题描述
- 重现步骤
- 预期行为 vs 实际行为
- 浏览器和版本
- 控制台日志截图
- localStorage / sessionStorage 快照

---

**测试愉快！🚀**
