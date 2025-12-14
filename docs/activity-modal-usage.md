# 活动/公告弹窗功能使用说明

## 功能概述

当用户登录进入作品管理界面时，系统会自动检查是否有未读的活动或公告通知，并以弹窗形式展示给用户。

## 弹窗显示规则

弹窗会显示满足以下**所有条件**的通知：

1. ✅ **未读状态**：`isRead === false`
2. ✅ **通知类型**：`type` 为 `EVENT`（活动）或 `ANNOUNCEMENT`（公告）
3. ✅ **展示方式**：`displayType` 包含 `'modal'`

如果有多个符合条件的通知，会优先显示**最新的一个**。

## 创建会弹窗的通知

在管理后台创建通知时，需要这样配置：

### 1. 基础配置
- **通知类型**：选择"活动"或"公告"
- **标题和内容**：填写通知的标题和详细内容
- **封面图片**（可选）：上传活动/公告的封面图

### 2. 展示方式（必选）
在"其他设置"部分，至少选择一种展示方式：
- ☑️ **通知铃铛**：在顶部通知铃铛中显示
- ☑️ **弹窗提醒**：用户登录时自动弹出（仅显示一次）

> 💡 **提示**：可以同时勾选两种展示方式，这样通知既会在铃铛中显示，也会在登录时弹窗

### 3. 活动配置（仅活动类型需要）

如果选择了"活动"类型，需要配置活动详情：

#### 活动类型选择
- **邀请活动** 🎁：用户邀请好友可获得奖励
- **比赛活动** 🏆：根据排名发放奖励
- **积分活动** 🎖️：完成任务获得积分

#### 邀请活动配置示例
```
邀请者奖励：
  - 类型：积分
  - 数量：500
  - 名称：邀请奖励积分

被邀请者奖励：
  - 类型：积分
  - 数量：300
  - 名称：新用户欢迎积分

完成条件：完成首次任务
```

#### 比赛活动配置示例
```
评分标准：作品质量（40%）+ 创新性（30%）+ 完成度（30%）

排名奖励：
  - 第1名：积分10000 + 冠军徽章
  - 第2-3名：积分5000
  - 第4-10名：积分2000
```

#### 活动时间
- **开始时间**：活动开始日期和时间
- **结束时间**：活动结束日期和时间

### 4. 目标用户
选择通知的目标用户群体：
- **全部用户**：所有注册用户
- **活跃用户**：最近有登录的用户
- **不活跃用户**：长期未登录的用户

### 5. 发布方式
- **立即发布**：保存后立即发送给用户
- **保存为草稿**：暂不发布，稍后手动发布

> ⚠️ **注意**：草稿状态的通知不会显示给用户，也不会触发弹窗

## 弹窗组件功能

### 显示内容
- 封面图片（如果有）
- 通知标题
- 活动时间（如果是活动类型）
- 简短描述（第一段内容）

### 用户操作
1. **查看详情**：点击"查看详情"按钮跳转到活动详情页
2. **稍后查看**：点击"稍后查看"关闭弹窗
3. **点击外部**：点击弹窗外部区域关闭弹窗
4. **关闭按钮**：点击右上角关闭按钮关闭弹窗

### 自动标记已读
当弹窗显示时，系统会自动将该通知标记为已读，确保用户下次登录时不会再看到同一个通知。

## 技术实现

### 文件结构
```
src/
├── components/
│   └── notifications/
│       └── ActivityModal.tsx          # 活动弹窗组件
├── views/
│   └── WorksView/
│       └── index.tsx                   # 作品管理页面（集成弹窗）
└── services/
    └── notificationApi.ts              # 通知API服务
```

### 核心逻辑

**WorksView/index.tsx**
```typescript
// 检查并显示活动/公告弹窗
useEffect(() => {
  checkForActivityNotifications();
}, []);

const checkForActivityNotifications = async () => {
  const response = await getUserNotifications({ page: 1, pageSize: 10 });

  // 筛选符合条件的通知
  const modalNotifications = response.items.filter(n =>
    !n.isRead &&
    (n.type === NotificationType.EVENT || n.type === NotificationType.ANNOUNCEMENT) &&
    n.displayType.includes('modal')
  );

  if (modalNotifications.length > 0) {
    const notification = modalNotifications[0];
    setActivityNotification(notification);
    setShowActivityModal(true);

    // 自动标记为已读
    await markNotificationsAsRead({ notificationIds: [notification.id] });
  }
};
```

**ActivityModal.tsx**
```typescript
export function ActivityModal({ notification, onClose }: ActivityModalProps) {
  const navigate = useNavigate();

  const handleViewDetails = () => {
    navigate(`/activities/${notification.id}`);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 ...">
      {/* 弹窗内容 */}
    </div>
  );
}
```

## 使用场景示例

### 场景 1：邀请活动通知
```typescript
// 管理员创建通知
{
  title: "邀请好友赢积分",
  content: "邀请1位好友注册，双方各得500积分！",
  type: NotificationType.EVENT,
  displayType: ['notification', 'modal'],  // 包含 modal
  coverImageUrl: "https://...",
  validFrom: "2025-12-12T00:00:00Z",
  validUntil: "2025-12-20T23:59:59Z",
  activityType: ActivityType.INVITATION,
  activityRules: {
    inviterRewards: [{ type: 'points', amount: 500 }],
    inviteeRewards: [{ type: 'points', amount: 500 }]
  }
}
```

用户登录后：
1. 进入作品管理页面
2. 自动弹出活动弹窗
3. 显示活动标题、时间、描述
4. 用户可选择"查看详情"或"稍后查看"

### 场景 2：系统公告
```typescript
// 管理员创建通知
{
  title: "系统升级通知",
  content: "系统将于本周六凌晨进行升级维护...",
  type: NotificationType.ANNOUNCEMENT,
  displayType: ['notification', 'modal'],  // 包含 modal
  priority: NotificationPriority.IMPORTANT
}
```

用户登录后：
1. 自动弹出公告弹窗
2. 显示公告内容
3. 用户确认后关闭

### 场景 3：不弹窗的通知
```typescript
// 管理员创建通知
{
  title: "新功能上线",
  type: NotificationType.FEATURE,
  displayType: ['notification'],  // 不包含 modal，不弹窗
}
```

用户登录后：
- 不会弹窗
- 只在通知铃铛中显示

## 注意事项

1. **避免频繁弹窗**：建议只对重要的活动和公告开启弹窗功能
2. **已读状态**：通知一旦弹出就会标记为已读，用户不会重复看到
3. **性能优化**：只获取最近10条通知进行检查，避免性能问题
4. **用户体验**：弹窗支持点击外部关闭，不会打断用户操作

## 扩展功能建议

### 1. 支持多个弹窗排队
目前只显示第一个符合条件的通知，可以改进为依次显示多个。

### 2. 添加"不再显示"选项
让用户选择不再显示某类通知。

### 3. 定时弹窗
根据活动时间，在特定时间点再次提醒用户。

### 4. 统计弹窗效果
记录弹窗的展示次数、点击率等数据。
