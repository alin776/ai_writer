# 🔔 AI Writer - 通知与活动系统

一个功能完整的通知和活动运营系统，支持实时推送、多种展示方式和智能提醒。

---

## ✨ 核心特性

### 🎯 多种展示方式
- **📱 通知铃铛** - 顶部导航栏，实时显示未读数量
- **📋 下拉列表** - 点击铃铛展开，查看最近通知
- **🎊 登录弹窗** - 重要活动登录后自动弹出
- **📢 顶部横幅** - 紧急通知以横幅形式展示（可扩展）

### 🚀 实时推送
- **WebSocket 连接** - 自动建立，实时接收新通知
- **心跳机制** - 保持连接稳定，自动重连
- **多设备同步** - 支持同一用户多设备同时在线

### 🎨 智能化功能
- **优先级系统** - 紧急/重要/普通三级优先级
- **目标用户筛选** - 全部/活跃/不活跃/自定义用户
- **定时发布** - 支持定时发布和草稿保存
- **统计分析** - 触达率、已读率、点击率

---

## 📁 项目结构

```
ai-writer/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── notification.py          # 数据库模型
│   │   ├── schemas/
│   │   │   └── notification.py          # Pydantic Schemas
│   │   ├── services/
│   │   │   └── notification_service.py  # 业务逻辑层
│   │   ├── api/v1/
│   │   │   ├── notifications.py         # API 路由
│   │   │   └── ws.py                    # WebSocket 推送
│   │   └── core/
│   │       └── security.py              # 权限验证
│   └── alembic/versions/
│       └── 20251130_*_add_notifications_system.py
│
└── src/
    ├── types/
    │   └── notification.ts               # TypeScript 类型
    ├── services/
    │   └── notificationApi.ts            # API 服务
    ├── store/
    │   └── notificationStore.ts          # Zustand 状态管理
    ├── hooks/
    │   └── useNotificationWebSocket.ts   # WebSocket Hook
    └── components/notifications/
        ├── NotificationBell.tsx          # 铃铛组件
        ├── NotificationDropdown.tsx      # 下拉列表
        ├── NotificationItem.tsx          # 单个通知项
        ├── NotificationModal.tsx         # 弹窗组件
        └── index.ts                      # 导出
```

---

## 🗄️ 数据库设计

### `notifications` 表
通知主表，存储所有通知和活动

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| title | String(200) | 标题 |
| content | Text | 内容（支持 Markdown） |
| cover_image_url | String(500) | 封面图 |
| category | Enum | 分类（system/announcement） |
| type | Enum | 类型（见下方） |
| priority | Enum | 优先级（urgent/important/normal） |
| display_type | Array | 展示方式 ['modal', 'banner', 'notification'] |
| action_button | JSONB | 行动按钮 {text, url} |
| target_users | Enum | 目标用户（all/active/inactive/custom） |
| status | Enum | 状态（draft/scheduled/active/expired） |
| published_at | DateTime | 发布时间 |
| valid_from / valid_until | DateTime | 有效期 |

**通知类型**：
- 系统：`ai_task_completed`, `analysis_ready`, `smart_reminder`, `milestone`, `inactivity_alert`
- 运营：`event`, `feature`, `announcement`, `maintenance`

### `user_notifications` 表
用户-通知关系表，记录已读、点击等状态

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | UUID | 用户 ID |
| notification_id | UUID | 通知 ID |
| is_read | Boolean | 是否已读 |
| read_at | DateTime | 已读时间 |
| is_dismissed | Boolean | 是否关闭弹窗 |
| clicked | Boolean | 是否点击了行动按钮 |

### `notification_templates` 表
通知模板，用于系统自动通知

| 字段 | 类型 | 说明 |
|------|------|------|
| name | String(100) | 模板名称（唯一） |
| type | Enum | 通知类型 |
| title_template | String(200) | 标题模板 |
| content_template | Text | 内容模板（支持变量） |

**变量替换示例**：
```
标题: {{username}}，您的{{task_name}}已完成！
内容: 《{{work_title}}》的{{chapter_title}}分析报告已生成
```

---

## 🔌 API 端点

### 用户端 API

```http
# 获取通知列表
GET /api/v1/notifications/user/notifications
  ?page=1&pageSize=20&isRead=false

# 获取未读数量
GET /api/v1/notifications/user/notifications/unread-count

# 标记已读
POST /api/v1/notifications/user/notifications/mark-read
Body: { "notificationIds": ["uuid1", "uuid2"] } # 或留空标记全部

# 关闭弹窗
POST /api/v1/notifications/user/notifications/{id}/dismiss

# 点击行动按钮
POST /api/v1/notifications/user/notifications/{id}/click
```

### 管理员 API

```http
# 创建通知
POST /api/v1/notifications/admin/notifications
Body: {
  "title": "春节30天日更挑战",
  "content": "新春佳节，挑战自我...",
  "type": "event",
  "priority": "important",
  "displayType": ["modal", "notification"],
  "actionButton": { "text": "立即参与", "url": "/activities/spring" },
  "publishType": "scheduled",
  "scheduledAt": "2025-02-01T00:00:00Z"
}

# 获取通知列表
GET /api/v1/notifications/admin/notifications
  ?page=1&category=announcement&status=active

# 获取统计
GET /api/v1/notifications/admin/notifications/{id}/stats

# 发布通知
POST /api/v1/notifications/admin/notifications/{id}/publish

# 更新/删除
PUT /api/v1/notifications/admin/notifications/{id}
DELETE /api/v1/notifications/admin/notifications/{id}
```

### WebSocket

```
WS ws://localhost:8000/ws/notifications/{user_id}

# 发送心跳
{ "type": "ping" }

# 接收消息
{ "type": "notification", "data": {...} }
{ "type": "unread_count", "data": { "count": 5 } }
{ "type": "notifications_list", "data": { "notifications": [...] } }
```

---

## 🎨 使用场景

### 1. 系统自动通知

```python
# 后端：AI 任务完成后发送通知
from app.services.notification_service import NotificationService
from app.api.v1.ws import broadcast_notification

# 从模板创建通知
notification = await notification_service.create_notification_from_template(
    template_name="ai_task_completed",
    variables={
        "username": user.username,
        "task_name": "章节续写",
        "chapter_title": "第一章"
    },
    user_id=user.id
)

# 实时推送
await broadcast_notification(
    user_id=user.id,
    notification_data={
        "id": str(notification.id),
        "title": notification.title,
        "content": notification.content,
        ...
    }
)
```

### 2. 运营活动推广

```python
# 管理员创建活动通知
notification = await notification_service.create_notification(
    notification_data=NotificationCreate(
        title="🎉 春节30天日更挑战",
        content="参与即可获得勋章和积分奖励！",
        cover_image_url="https://example.com/spring.jpg",
        category=NotificationCategory.ANNOUNCEMENT,
        type=NotificationType.EVENT,
        priority=NotificationPriority.IMPORTANT,
        display_type=["modal", "notification"],
        action_button={"text": "立即参与", "url": "/activities/spring"},
        target_users=TargetUserType.ALL,
        valid_from=datetime(2025, 2, 1),
        valid_until=datetime(2025, 3, 2),
        publish_type="scheduled",
        scheduled_at=datetime(2025, 2, 1, 0, 0)
    ),
    created_by=admin_user.id
)
```

### 3. 前端集成

```tsx
// 在 Header 中添加通知铃铛
import { NotificationBell } from '../components/notifications';

function Header() {
  return (
    <header>
      <NotificationBell />
    </header>
  );
}

// 在 App 中启用弹窗
import { useNotificationWebSocket } from '../hooks/useNotificationWebSocket';
import { NotificationModal } from '../components/notifications';

function App() {
  const { showModal, modalNotification, closeModal } = useNotificationWebSocket();

  return (
    <>
      {/* 应用内容 */}

      {showModal && modalNotification && (
        <NotificationModal
          notification={modalNotification}
          onClose={closeModal}
        />
      )}
    </>
  );
}
```

---

## 📊 管理员统计

访问 `/api/v1/notifications/admin/notifications/{id}/stats` 可获取：

```json
{
  "notificationId": "uuid",
  "title": "春节30天日更挑战",
  "totalUsers": 1000,      // 总触达用户
  "readCount": 850,        // 已读用户
  "dismissedCount": 120,   // 关闭弹窗用户
  "clickedCount": 650,     // 点击行动按钮用户
  "readRate": 85.0,        // 查看率 %
  "clickRate": 65.0        // 点击率 %
}
```

---

## 🔒 权限控制

- **用户端 API** - 需要登录认证（`get_current_active_user`）
- **管理员 API** - 需要管理员权限（`get_current_admin_user`）
- **WebSocket** - 需要提供有效的 `user_id`

---

## 🎯 后续扩展

### 已规划功能
1. ✅ 基础通知系统
2. ✅ WebSocket 实时推送
3. ⏳ 通知中心页面（完整历史记录）
4. ⏳ 顶部 Banner 横幅
5. ⏳ 浏览器原生通知
6. ⏳ 邮件通知
7. ⏳ 通知分组和筛选
8. ⏳ 智能提醒（写作习惯分析）
9. ⏳ 周报/月报自动生成

### 管理后台功能
1. ⏳ 通知/活动创建页面（富文本编辑器）
2. ⏳ 实时预览功能
3. ⏳ 通知列表管理
4. ⏳ 统计数据可视化
5. ⏳ A/B 测试支持

---

## 🐛 故障排查

### WebSocket 连接失败
```bash
# 检查后端服务
curl http://localhost:8000/health

# 查看 WebSocket 日志
# 浏览器控制台应显示：[WebSocket] 通知连接已建立
```

### 通知不显示
```tsx
// 检查 Zustand store 状态
import { useNotificationStore } from './store/notificationStore';

console.log(useNotificationStore.getState());
// 应输出：{ notifications: [...], unreadCount: N, isConnected: true }
```

### API 调用失败
```bash
# 测试 API
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/notifications/user/notifications/unread-count
```

---

## 📚 相关文档

- [集成指南](./NOTIFICATION_INTEGRATION.md) - 详细的集成步骤
- [API 文档](http://localhost:8000/docs) - FastAPI 自动生成的 Swagger 文档
- [类型定义](./src/types/notification.ts) - TypeScript 类型参考

---

## 👥 联系我们

如有问题或建议，欢迎提 Issue 或 PR！

---

**Made with ❤️ by AI Writer Team**
