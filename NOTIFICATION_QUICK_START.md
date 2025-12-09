# 通知系统快速开始指南

## ✅ 已完成集成

通知系统已经完全集成到您的应用中！以下是已完成的工作：

### 后端 ✅
- 数据库表和迁移已完成
- API 端点已创建（用户端 + 管理员端）
- WebSocket 实时推送已配置
- 服务层逻辑已实现

### 前端 ✅
- 顶部导航栏通知铃铛已激活（显示未读数量）
- 通知下拉列表已集成
- 登录弹窗已启用
- WebSocket 自动连接已配置

---

## 🚀 如何使用

### 1. 查看通知效果

**方式一：通过 API 创建测试通知**

```bash
# 创建一个测试通知（需要管理员权限）
curl -X POST http://localhost:8000/api/v1/notifications \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -d '{
    "title": "欢迎使用通知系统",
    "content": "这是一条测试通知，用于验证系统功能",
    "category": "announcement",
    "type": "feature",
    "priority": "important",
    "display_type": ["notification", "modal"],
    "publish_type": "immediate"
  }'
```

**方式二：在 Python 中创建（开发/测试用）**

```python
# backend/test_notification.py
from app.services.notification_service import NotificationService
from app.core.database import SessionLocal
from app.schemas.notification import NotificationCreate, PublishType
from app.models.notification import NotificationPriority

async def create_test_notification():
    db = SessionLocal()
    service = NotificationService(db)

    notification = await service.create_notification(
        NotificationCreate(
            title="🎉 系统新功能上线",
            content="AI Writer 现在支持实时通知推送功能！",
            category="announcement",
            type="feature",
            priority=NotificationPriority.IMPORTANT,
            display_type=["notification", "modal"],
            publish_type=PublishType.IMMEDIATE
        )
    )

    db.close()
    return notification
```

### 2. 查看效果

登录后，您会看到：

1. **顶部导航栏右侧** - 通知铃铛显示红色未读数量徽章
2. **点击铃铛** - 弹出通知下拉列表，显示最近的未读通知
3. **重要通知** - 如果通知优先级为 `important` 或 `urgent`，会在登录时弹出模态框

---

## 📍 集成位置

### 通知铃铛
**文件**: `src/components/layout/Header.tsx` (第 146-172 行)

```tsx
{/* 通知铃铛 */}
<div className="relative">
  <button onClick={() => setShowNotifications(!showNotifications)}>
    <Bell className="w-4 h-4" />
    {unreadCount > 0 && (
      <span className="badge">{unreadCount > 99 ? '99+' : unreadCount}</span>
    )}
  </button>

  {showNotifications && (
    <NotificationDropdown onClose={() => setShowNotifications(false)} />
  )}
</div>
```

### 登录弹窗
**文件**: `src/components/layout/AuthLayout.tsx` (第 26-27 行, 96-101 行)

```tsx
// 启用通知 WebSocket 和弹窗
const { showModal, modalNotification, closeModal } = useNotificationWebSocket();

// 在布局底部渲染弹窗
{showModal && modalNotification && (
  <NotificationModal notification={modalNotification} onClose={closeModal} />
)}
```

---

## 🎯 通知类型和优先级

### 通知类别 (Category)
- `system` - 系统通知（如安全提醒）
- `announcement` - 公告通知（如新功能、活动）

### 通知类型 (Type)
- `writing_habit` - 写作习惯建议
- `statistics` - 统计报告（周报/月报）
- `draft_reminder` - 草稿提醒
- `feature` - 新功能上线
- `maintenance` - 系统维护
- `event` - 活动通知
- `security` - 安全提醒
- `achievement` - 成就解锁

### 优先级 (Priority)
- `urgent` - 紧急（红色边框，强制弹窗）
- `important` - 重要（黄色边框，默认弹窗）
- `normal` - 普通（蓝色边框，仅通知栏）
- `low` - 低优先级（灰色边框）

### 展示方式 (Display Type)
- `notification` - 通知铃铛下拉列表
- `modal` - 登录弹窗
- `banner` - 顶部横幅（待实现）

---

## 🔧 API 端点

### 用户端点
- `GET /api/v1/notifications/my` - 获取我的通知列表
- `GET /api/v1/notifications/unread-count` - 获取未读数量
- `POST /api/v1/notifications/{id}/read` - 标记为已读
- `POST /api/v1/notifications/mark-read` - 批量标记已读
- `POST /api/v1/notifications/{id}/dismiss` - 忽略通知
- `POST /api/v1/notifications/{id}/click-action` - 点击行动按钮

### 管理员端点
- `POST /api/v1/notifications` - 创建通知
- `PUT /api/v1/notifications/{id}` - 更新通知
- `DELETE /api/v1/notifications/{id}` - 删除通知
- `POST /api/v1/notifications/{id}/publish` - 发布通知
- `GET /api/v1/notifications/{id}/stats` - 获取统计数据

### WebSocket
- `ws://localhost:8000/api/v1/ws/notifications/{user_id}` - 实时推送

---

## 🎨 自定义通知样式

### 修改未读徽章颜色
在 `Header.tsx` 中修改第 154 行：

```tsx
<span className="... bg-red-500 ...">  {/* 改为 bg-blue-500 等 */}
```

### 修改下拉列表宽度
在 `NotificationDropdown.tsx` 中修改容器类名：

```tsx
<div className="w-80"> {/* 改为 w-96 或其他宽度 */}
```

### 添加自定义图标
在 `NotificationItem.tsx` 的 `getNotificationIcon()` 函数中添加：

```tsx
case NotificationType.YOUR_TYPE:
  return <YourIcon className="w-5 h-5" />;
```

---

## 📊 后续功能建议

### 1. 管理后台通知创建页面
在 `src/pages/admin/` 中创建：
- 富文本编辑器
- 封面图上传
- 目标用户选择器
- 定时发布功能
- 预览效果

### 2. 通知中心页面
创建 `src/pages/NotificationCenter.tsx`：
- 显示所有历史通知
- 按类型筛选
- 按时间范围筛选
- 搜索功能

### 3. 顶部横幅组件
创建 `NotificationBanner.tsx`：
- 显示紧急公告
- 可关闭或常驻
- 自定义背景色

### 4. 浏览器原生通知
集成 Notification API：
- 请求通知权限
- 桌面通知推送
- 点击跳转到相关页面

---

## 🐛 故障排查

### 通知铃铛没有显示未读数量
1. 检查 WebSocket 是否连接成功（浏览器控制台）
2. 确认用户已登录（`user.id` 存在）
3. 检查后端服务是否运行在 `http://localhost:8000`

### 弹窗没有出现
1. 确认通知的 `display_type` 包含 `modal`
2. 确认通知的优先级为 `important` 或 `urgent`
3. 检查 `AuthLayout.tsx` 中是否正确集成了 `useNotificationWebSocket`

### WebSocket 连接失败
1. 检查后端 WebSocket 端点是否正常
2. 查看浏览器控制台的错误信息
3. 确认 URL 配置正确（`notificationStore.ts` 中）

---

## 💡 使用提示

- **实时推送**: 当创建新通知时，已登录的用户会立即收到 WebSocket 推送
- **自动重连**: 如果 WebSocket 断开，系统会自动尝试重连（5 秒间隔）
- **多标签页支持**: 每个标签页都会建立独立的 WebSocket 连接
- **未读数量缓存**: 未读数量会保存在 Zustand store 中，页面刷新后自动恢复
- **队列式弹窗**: 如果有多个重要通知，会依次弹出而不是同时显示

---

## 📚 相关文档

- [系统详细文档](./NOTIFICATION_SYSTEM_README.md)
- [完整集成指南](./NOTIFICATION_INTEGRATION.md)
- [API 参考](./NOTIFICATION_SYSTEM_README.md#api-参考)

---

🎉 恭喜！通知系统已经可以使用了！

如有任何问题，请参考上述文档或查看源代码注释。
