# Agent 会话存储优化方案

## 问题背景

Agent 对话历史累积导致 localStorage 配额超限：
- 每个会话存储完整的 messages，包含 `flowItems`（执行轨迹）
- `flowItems` 包含大量 Explore 工具的检索结果、工具调用详情
- 单个会话可能达到数百 KB 甚至 MB
- 默认保留 10 个会话，总计可能超过 10MB（超出浏览器限制）

## 已实施的优化方案

### ✅ 方案 1：智能压缩 flowItems（已实现）

**文件**: `src/utils/sessionCompression.ts`

**策略**:
1. **Explore 工具结果压缩**
   - 只保留前 3 条检索结果
   - 移除详细的 content 字段
   - 保留 title 和 score 用于展示

2. **工具调用参数压缩**
   - 只保留关键参数（query, type, limit, filter）
   - 移除其他冗余参数

3. **长文本截断**
   - 工具输出超过 500 字符时截断
   - 消息内容超过 1000 字符时截断
   - 保留"已截断"标记

4. **历史会话激进压缩**
   - 非当前会话完全移除 flowItems
   - 只保留摘要和状态信息

**效果预估**:
- 单个会话从 500KB → 50-100KB（压缩 80-90%）
- 3 个会话总计 150-300KB（原来 1.5MB）

### ✅ 方案 2：减少保留会话数（已实现）

**文件**: `src/hooks/useConversationPersistence.ts`

**修改**:
```typescript
const DEFAULT_MAX_SESSIONS = 3; // 从 10 → 3
```

**效果**:
- 存储占用减少 70%
- 用户仍可访问最近 3 个会话
- 超过 3 个的旧会话自动删除

### ✅ 方案 3：自动压缩策略（已实现）

**文件**: `src/hooks/useConversationPersistence.ts`

**策略**:
```typescript
// 使用率 < 50%: 不压缩
// 使用率 50-80%: 轻度压缩（压缩 flowItems）
// 使用率 > 80%: 重度压缩（移除历史会话的 flowItems）

if (storageStats.usage > 50) {
  compressedMessages = compressSessionMessages(messages, sessionId, sessionId);
}
```

**优点**:
- 动态调整压缩级别
- 不影响用户体验
- 自动适应存储空间

## 进阶优化方案（可选）

### 方案 4：分离当前会话和历史会话

**实现思路**:
```typescript
// 当前会话：完整存储在内存 + localStorage
const currentSession = {
  messages: [...], // 包含完整 flowItems
};

// 历史会话：只存储摘要
const historicalSession = {
  id: 'xxx',
  title: '会话标题',
  summary: '会话摘要（前 3 条消息）',
  messageCount: 20,
  createdAt: '...',
  updatedAt: '...',
  // flowItems 完全不存储
};
```

**优点**:
- 历史会话占用极小（每个 < 5KB）
- 可以保留更多历史会话（10-20 个）
- 需要查看历史时从后端加载（如果有后端存储）

**实施难度**: 中等

### 方案 5：使用 LZ-String 压缩

**依赖**: `lz-string` 库

```typescript
import LZString from 'lz-string';

// 保存时压缩
const compressed = LZString.compress(JSON.stringify(session));
localStorage.setItem(key, compressed);

// 读取时解压
const compressed = localStorage.getItem(key);
const session = JSON.parse(LZString.decompress(compressed));
```

**效果**:
- 文本压缩率 50-70%
- 适合压缩重复性高的数据
- 解压需要 CPU 时间（10-50ms）

**实施难度**: 简单

### 方案 6：迁移到 IndexedDB（长期方案）

**优点**:
- 配额更大（50MB - 几百 MB）
- 支持结构化存储和索引
- 支持分页加载

**实施思路**:
```typescript
// 使用 idb-keyval 简化 IndexedDB 操作
import { set, get, keys, del } from 'idb-keyval';

// 保存会话
await set(`session_${sessionId}`, session);

// 加载会话
const session = await get(`session_${sessionId}`);

// 列出所有会话
const allKeys = await keys();
```

**实施难度**: 中等

### 方案 7：后端存储（最佳方案）

**优点**:
- 不受浏览器存储限制
- 数据可跨设备同步
- 可实现搜索、过滤、导出等高级功能

**API 设计**:
```typescript
// 保存会话
POST /api/agent/sessions
{
  sessionId: 'xxx',
  messages: [...],
  metadata: { workId, chapterId }
}

// 获取会话列表
GET /api/agent/sessions?limit=10&offset=0

// 获取单个会话
GET /api/agent/sessions/:sessionId

// 删除会话
DELETE /api/agent/sessions/:sessionId
```

**本地缓存策略**:
```typescript
// 1. 当前会话在内存 + localStorage
// 2. 历史会话只缓存列表（metadata）
// 3. 按需从后端加载完整会话
// 4. LRU 缓存最近访问的 3 个会话
```

**实施难度**: 高（需要后端支持）

## 混合方案（推荐）

结合多个方案的优点：

### 第一阶段（已完成）✅
- [x] 智能压缩 flowItems
- [x] 减少保留会话数（3个）
- [x] 自动压缩策略

**效果**: 存储占用减少 70-80%

### 第二阶段（短期，2-4 周）
- [ ] 添加 LZ-String 压缩
- [ ] 分离当前会话和历史会话
- [ ] 历史会话只保存摘要

**预期效果**: 可保留 10-20 个会话，总占用 < 500KB

### 第三阶段（中期，1-2 个月）
- [ ] 迁移到 IndexedDB
- [ ] 实现本地缓存策略
- [ ] 添加会话导出功能

**预期效果**: 可保留 100+ 个会话，性能优秀

### 第四阶段（长期，3-6 个月）
- [ ] 后端会话存储
- [ ] 跨设备同步
- [ ] 会话搜索和过滤

**预期效果**: 无限会话，云端同步

## 监控和预警

添加存储使用监控：

```typescript
// 在应用启动时检查
useEffect(() => {
  const stats = analyzeLocalStorage();

  console.log('localStorage 使用情况:', {
    usage: `${stats.usage.toFixed(2)}%`,
    total: stats.totalFormatted,
    items: stats.items.length,
  });

  // 使用率 > 70% 时显示警告
  if (stats.usage > 70) {
    showWarning('存储空间不足，建议清理旧会话');
  }

  // 使用率 > 90% 时强制清理
  if (stats.usage > 90) {
    autoCleanupStorage();
    showInfo('已自动清理旧数据，释放存储空间');
  }
}, []);
```

## 用户配置选项

可以添加设置项让用户自定义：

```typescript
interface SessionStorageSettings {
  maxSessions: number;          // 保留会话数量 (1-10)
  compressionLevel: 'none' | 'light' | 'aggressive'; // 压缩级别
  autoCleanup: boolean;         // 自动清理
  cleanupThreshold: number;     // 清理阈值 (50-90%)
}
```

## 性能影响

| 方案 | CPU 开销 | 内存开销 | 用户体验 |
|------|---------|---------|---------|
| flowItems 压缩 | 极低 (< 5ms) | 无影响 | 无感知 |
| 减少会话数 | 无 | 减少 | 轻微影响 |
| LZ-String | 低 (10-50ms) | 无影响 | 无感知 |
| IndexedDB | 中 (50-100ms) | 减少 | 无感知 |
| 后端存储 | 低 | 大幅减少 | 加载延迟 |

## 测试计划

1. **单元测试**
   - 压缩函数正确性
   - 解压后数据完整性
   - 边界情况处理

2. **性能测试**
   - 压缩耗时（目标 < 10ms）
   - 解压耗时（目标 < 10ms）
   - 内存占用

3. **用户测试**
   - 功能完整性
   - 用户体验影响
   - 错误处理

## 回滚计划

如果出现问题，可以快速回滚：

```typescript
// 添加功能开关
const USE_COMPRESSION = import.meta.env.VITE_USE_SESSION_COMPRESSION !== 'false';

if (USE_COMPRESSION) {
  compressedMessages = compressSessionMessages(messages, sessionId, sessionId);
} else {
  compressedMessages = messages;
}
```

## 总结

**已完成的优化**（第一阶段）:
1. ✅ 智能压缩 flowItems - 减少 80-90% 单个会话大小
2. ✅ 减少保留会话数 (10 → 3) - 减少 70% 总占用
3. ✅ 自动压缩策略 - 动态调整压缩级别

**预期效果**:
- 存储占用从 10MB+ 降低到 150-300KB
- 解决 localStorage 配额超限问题
- 用户体验无明显影响

**后续优化**（可选）:
- 第二阶段: LZ-String + 历史会话分离
- 第三阶段: IndexedDB 迁移
- 第四阶段: 后端存储 + 云同步

**建议**:
- 先观察第一阶段效果
- 如果仍有问题，再实施第二阶段
- 长期建议实施后端存储方案
