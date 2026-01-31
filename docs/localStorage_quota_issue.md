# localStorage 配额超限问题分析与解决方案

## 问题现象

用户在作品详情页刷新后，页面跳转回登录页，历史记录丢失。

## 根本原因

### 1. localStorage 配额限制

浏览器的 localStorage 通常有 5-10MB 的配额限制（不同浏览器略有差异）：
- Chrome/Edge: 10MB
- Firefox: 10MB
- Safari: 5MB

### 2. 大量数据累积

应用中存储了大量数据到 localStorage，主要来源：

#### (1) Agent 对话历史 (`agent_conversation_*`)
- 每个会话存储完整的消息数组
- 每条消息包含：
  - `content`: 消息内容
  - `agentSteps`: Agent 执行步骤
  - **`flowItems`**: 执行轨迹（v5.1 新增，数据量大）
  - **`tasksSnapshot`**: 任务列表快照（v6.2 新增）
- 默认保留最多 10 个会话
- 问题：**flowItems 包含大量 Explore 工具的检索结果、工具调用详情等，单个会话可能达到数百 KB 甚至 MB**

#### (2) 编辑器草稿 (`chapter_content_*`, `chapter_json_*`)
- 每个编辑中的章节存储 HTML 和 JSON 两份数据
- 长章节内容可能达到几百 KB

#### (3) 其他持久化数据
- `auth-storage`: 认证信息
- `work-nav-storage`: 作品导航状态
- 其他配置和缓存

### 3. 配额超限的后果

当 localStorage 写入失败时：
- `zustand persist` 中间件**静默失败**，不抛出错误
- `authStore` 无法将认证信息持久化
- 刷新页面后，`authStore.isAuthenticated = false`
- `ProtectedRoute` 检查失败，重定向到登录页

## 数据累积示例

假设一个典型场景：
```
- Agent 会话 1: 包含 20 条消息，每条消息有 flowItems (平均 50KB) = 1MB
- Agent 会话 2-10: 类似规模 = 9MB
- 编辑器草稿 3 个: 每个 200KB = 600KB
- 其他数据: 500KB
总计: ≈ 11MB → 超出配额！
```

## 已实施的解决方案

### 1. 为 authStore 添加安全的 localStorage 包装器

**文件**: `src/store/authStore.ts`

```typescript
const safeStorage = {
  getItem: (name: string) => { /* 错误处理 */ },
  setItem: (name: string, value: string) => {
    try {
      localStorage.setItem(name, value);
    } catch (error) {
      if (isQuotaExceeded(error)) {
        // 尝试清理后重试
        localStorage.removeItem(name);
        localStorage.setItem(name, value);

        // 触发全局事件通知用户
        window.dispatchEvent(
          new CustomEvent('storage-quota-exceeded', {
            detail: { store: 'auth', message: '存储空间不足...' }
          })
        );
      }
    }
  },
  removeItem: (name: string) => { /* 错误处理 */ }
};
```

### 2. 全局错误提示

**文件**: `src/App.tsx`

监听 `storage-quota-exceeded` 事件，向用户显示友好的错误提示：
```
存储空间不足：认证信息无法保存，刷新页面可能需要重新登录。
请清理浏览器缓存后重试。
```

### 3. 存储诊断工具

**文件**: `src/utils/storageDebug.ts`

开发模式下可在控制台使用：
```javascript
// 查看存储使用情况
storageDebug.print()

// 自动清理旧数据
storageDebug.cleanup()

// 清理 Agent 会话（保留最近 3 个）
storageDebug.cleanupSessions(3)

// 清理编辑器草稿
storageDebug.cleanupDrafts()
```

## 建议的长期优化方案

### 1. 减少 flowItems 存储（高优先级）

**问题**: flowItems 包含完整的执行轨迹，数据量大

**方案**:
- 对于历史会话，只存储概要信息，不存储详细的 flowItems
- 或压缩 flowItems 数据（移除冗余字段、压缩文本）
- 考虑只在内存中保留当前会话的 flowItems，历史会话从后端获取

```typescript
// 保存会话时，清理旧会话的 flowItems
const saveSession = (messages) => {
  const cleanedMessages = messages.map(msg => {
    if (/* 不是当前会话 */) {
      return { ...msg, flowItems: undefined };
    }
    return msg;
  });
  // ...
};
```

### 2. 实现智能清理策略（中优先级）

**方案**:
- 监控 localStorage 使用率
- 当使用率超过 80% 时，自动清理最旧的数据
- 优先清理：
  1. 旧的 Agent 会话（保留最近 3-5 个）
  2. 旧的编辑器草稿（保留最近编辑的）
  3. 过期的缓存数据

```typescript
// 在 authStore persist 配置中添加
onRehydrateStorage: () => (state) => {
  // 检查存储使用情况
  const stats = analyzeLocalStorage();
  if (stats.usage > 80) {
    autoCleanupStorage();
  }
  state?.setHasHydrated?.(true);
}
```

### 3. 迁移到 IndexedDB（长期方案）

**方案**:
- Agent 对话历史迁移到 IndexedDB（配额通常更大，50MB+）
- 编辑器草稿迁移到 IndexedDB
- localStorage 只保留轻量级配置（认证信息、用户偏好等）

**优点**:
- IndexedDB 配额更大
- 支持结构化存储
- 可以分页加载历史数据

### 4. 后端持久化（最佳方案）

**方案**:
- Agent 会话保存到后端数据库
- 本地只缓存当前活跃的会话
- 按需从后端加载历史会话

**优点**:
- 不受浏览器存储限制
- 数据可跨设备同步
- 可以实现更复杂的搜索和过滤

## 用户自助清理指南

如果用户遇到存储空间不足问题：

### 方法 1: 使用开发者工具清理
1. 打开浏览器开发者工具（F12）
2. 切换到 Console 标签
3. 输入 `storageDebug.cleanup()` 并回车
4. 刷新页面

### 方法 2: 清除浏览器缓存
1. Chrome: 设置 → 隐私和安全 → 清除浏览数据 → 选择"Cookie 和其他网站数据"
2. 选择时间范围：全部时间
3. 点击"清除数据"
4. 重新登录应用

### 方法 3: 手动清理 localStorage
1. 打开浏览器开发者工具（F12）
2. 切换到 Application 标签
3. 左侧找到 Storage → Local Storage → 选择当前域名
4. 删除不需要的键（特别是 `agent_conversation_*`）

## 监控和预警

建议添加监控：

```typescript
// 在应用启动时检查
useEffect(() => {
  const stats = analyzeLocalStorage();
  if (stats.usage > 80) {
    console.warn('localStorage 使用率:', stats.usage.toFixed(2) + '%');
    // 可选：显示用户提示
  }
}, []);
```

## 相关文件

- `src/store/authStore.ts` - 认证状态管理（已修复）
- `src/store/workNavStore.ts` - 作品导航状态（已有 safeStorage）
- `src/hooks/useConversationPersistence.ts` - Agent 会话持久化（待优化）
- `src/components/editor/NovelEditor.tsx` - 编辑器草稿缓存（待优化）
- `src/utils/storageDebug.ts` - 存储诊断工具（新增）

## 总结

localStorage 配额超限问题的根源是 **Agent 对话历史的 flowItems 数据量过大**，导致存储空间不足，进而导致认证信息无法持久化。

短期解决方案已实施（安全的存储包装器 + 错误提示），可以防止应用崩溃并提醒用户。

长期建议实施 **flowItems 数据精简** 和 **智能清理策略**，或将大数据迁移到后端/IndexedDB。
