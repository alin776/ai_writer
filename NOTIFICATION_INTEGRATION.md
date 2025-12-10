# 通知系统集成指南

## 📋 已完成的组件

### 后端
- ✅ 数据库模型和迁移
- ✅ 服务层 (`NotificationService`)
- ✅ RESTful API（用户端和管理员端）
- ✅ WebSocket 实时推送

### 前端
- ✅ TypeScript 类型定义
- ✅ API 服务层
- ✅ Zustand 状态管理
- ✅ 通知铃铛组件
- ✅ 通知下拉列表
- ✅ 通知弹窗
- ✅ WebSocket Hook

---

## 🚀 快速集成

### 1. 在顶部导航栏添加通知铃铛

在你的 `Header.tsx` 或顶部导航组件中添加：

```tsx
import { NotificationBell } from '../components/notifications';

function Header() {
  return (
    <header>
      {/* 其他导航内容 */}

      {/* 添加通知铃铛 */}
      <NotificationBell />

      {/* 用户头像等 */}
    </header>
  );
}
```

### 2. 在应用根组件启用 WebSocket 和弹窗

在你的 `App.tsx` 或 `AuthLayout.tsx` 中：

```tsx
import { useNotificationWebSocket } from '../hooks/useNotificationWebSocket';
import { NotificationModal } from '../components/notifications';

function App() {
  // 启用 WebSocket 和弹窗
  const { showModal, modalNotification, closeModal } = useNotificationWebSocket();

  return (
    <div>
      {/* 你的应用内容 */}

      {/* 通知弹窗 */}
      {showModal && modalNotification && (
        <NotificationModal
          notification={modalNotification}
          onClose={closeModal}
        />
      )}
    </div>
  );
}
```

### 3. 安装必要的依赖

如果尚未安装，需要安装 `date-fns`：

```bash
npm install date-fns
```

---

## 📖 组件使用说明

### `NotificationBell`
通知铃铛组件，显示在导航栏

**特性**：
- 自动显示未读数量 badge
- 点击展开下拉列表
- 点击外部自动关闭

**用法**：
```tsx
<NotificationBell />
```

---

### `NotificationModal`
登录弹窗，显示重要通知

**Props**：
- `notification`: 要显示的通知对象
- `onClose`: 关闭回调函数

**特性**：
- 支持封面图
- 支持行动按钮
- 优先级指示条
- 稍后查看/立即参与

**用法**：
```tsx
<NotificationModal
  notification={notification}
  onClose={() => setShowModal(false)}
/>
```

---

### `useNotificationWebSocket`
WebSocket Hook，自动连接和管理弹窗

**返回值**：
- `showModal`: 是否显示弹窗
- `modalNotification`: 当前通知对象
- `closeModal`: 关闭弹窗方法

**用法**：
```tsx
const { showModal, modalNotification, closeModal } = useNotificationWebSocket();
```

---

## 🎨 样式自定义

所有组件都使用 Tailwind CSS，你可以通过以下方式自定义：

### 修改颜色主题
在组件中直接修改 Tailwind 类名：

```tsx
// 例如修改铃铛按钮的背景色
<button className="hover:bg-purple-100"> {/* 原: hover:bg-gray-100 */}
```

### 修改下拉列表宽度
在 `NotificationDropdown.tsx` 中：

```tsx
<div className="w-96"> {/* 修改为 w-[500px] 或其他宽度 */}
```

---

## 🔔 手动触发操作

### 标记所有通知为已读

```tsx
import { useNotificationStore } from '../store/notificationStore';

function MyComponent() {
  const markAllAsRead = useNotificationStore((state) => state.markAllAsRead);

  const handleMarkAll = () => {
    markAllAsRead();
  };
}
```

### 获取未读数量

```tsx
const unreadCount = useNotificationStore((state) => state.unreadCount);
```

### 手动刷新通知列表

```tsx
const fetchNotifications = useNotificationStore((state) => state.fetchNotifications);

// 刷新未读通知
fetchNotifications({ isRead: false });

// 刷新所有通知
fetchNotifications();
```

---

## 📡 WebSocket 消息格式

客户端接收的消息格式：

### 1. 新通知
```json
{
  "type": "notification",
  "data": {
    "id": "uuid",
    "title": "通知标题",
    "content": "通知内容",
    "priority": "important",
    "displayType": ["modal"],
    ...
  }
}
```

### 2. 未读数量更新
```json
{
  "type": "unread_count",
  "data": {
    "count": 5
  }
}
```

### 3. 通知列表
```json
{
  "type": "notifications_list",
  "data": {
    "notifications": [...]
  }
}
```

---

## 🛠️ 后续功能扩展

### 创建通知中心页面

创建 `src/pages/Notifications.tsx`：

```tsx
import React, { useEffect } from 'react';
import { useNotificationStore } from '../store/notificationStore';
import { NotificationItem } from '../components/notifications';

function NotificationsPage() {
  const { notifications, fetchNotifications } = useNotificationStore();

  useEffect(() => {
    fetchNotifications(); // 加载所有通知
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">通知中心</h1>

      <div className="bg-white rounded-lg shadow divide-y">
        {notifications.map((notif) => (
          <NotificationItem
            key={notif.id}
            notification={notif}
            onClose={() => {}}
          />
        ))}
      </div>
    </div>
  );
}

export default NotificationsPage;
```

添加路由：
```tsx
<Route path="/notifications" element={<NotificationsPage />} />
```

---

### 创建顶部 Banner 横幅

创建 `src/components/notifications/NotificationBanner.tsx`：

```tsx
import React, { useEffect, useState } from 'react';
import { X } from 'lucide-react';
import { useNotificationStore } from '../../store/notificationStore';

function NotificationBanner() {
  const [bannerNotification, setBannerNotification] = useState(null);
  const { notifications, dismiss } = useNotificationStore();

  useEffect(() => {
    // 找到需要展示为 Banner 的通知
    const banner = notifications.find(
      (n) => n.displayType.includes('banner') && !n.isDismissed
    );
    setBannerNotification(banner || null);
  }, [notifications]);

  if (!bannerNotification) return null;

  return (
    <div
      className="relative px-4 py-3 text-white"
      style={{ backgroundColor: bannerNotification.bannerColor || '#3b82f6' }}
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium">{bannerNotification.title}</p>
          {bannerNotification.content && (
            <p className="text-xs mt-1 opacity-90">{bannerNotification.content}</p>
          )}
        </div>

        <button
          onClick={() => dismiss(bannerNotification.id)}
          className="ml-4 p-1 hover:bg-white/20 rounded transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

export default NotificationBanner;
```

使用：
```tsx
// 在 Header 上方或应用顶部
<NotificationBanner />
```

---

## 🐛 常见问题

### WebSocket 连接失败
- 确保后端服务运行在 `http://localhost:8000`
- 检查 `notificationStore.ts` 中的 WebSocket URL 配置
- 查看浏览器控制台的错误信息

### 通知不显示
- 检查用户是否已登录（`user.id` 存在）
- 检查后端 API 是否正常返回数据
- 查看 Zustand DevTools（如果已安装）

### 样式不正确
- 确保 Tailwind CSS 已正确配置
- 检查 Dark Mode 配置是否正确
- 确认 Lucide React 图标库已安装

---

## 📝 下一步

1. **创建管理后台页面** - 允许管理员创建和管理通知
2. **添加通知筛选** - 按类型、时间等筛选通知
3. **添加通知搜索** - 搜索历史通知
4. **浏览器原生通知** - 使用 Notification API
5. **邮件通知** - 集成邮件发送服务

---

## 💡 提示

- 通知会自动通过 WebSocket 实时推送
- 未读数量会自动更新
- 关闭弹窗后，如果有多个重要通知会依次展示
- 所有 API 调用都会自动处理 camelCase ↔ snake_case 转换

祝你使用愉快！🎉
