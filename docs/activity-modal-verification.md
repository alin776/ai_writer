# 活动弹窗登录控制 - 验证文档

## 功能目标

确保活动/公告弹窗**仅在用户登录后首次进入作品管理界面时显示**，在同一登录会话期间的其他页面跳转不会重复显示弹窗。

## 实现方案

使用 `sessionStorage` 进行会话级别的状态管理：

### 1. 弹窗显示逻辑 (WorksView/index.tsx:196-229)

```typescript
const checkForActivityNotifications = async () => {
  try {
    // 检查本会话是否已显示过弹窗
    const hasShownModal = sessionStorage.getItem('activity_modal_shown');

    // 如果已显示过，直接返回
    if (hasShownModal === 'true') {
      return;
    }

    // 获取用户通知
    const response = await getUserNotifications({ page: 1, pageSize: 10 });

    // 筛选符合弹窗条件的通知
    const modalNotifications = response.items.filter(n =>
      !n.isRead &&
      (n.type === NotificationType.EVENT || n.type === NotificationType.ANNOUNCEMENT) &&
      n.displayType.includes('modal')
    );

    // 显示第一个符合条件的通知
    if (modalNotifications.length > 0) {
      const notification = modalNotifications[0];
      setActivityNotification(notification);
      setShowActivityModal(true);

      // 标记本会话已显示弹窗
      sessionStorage.setItem('activity_modal_shown', 'true');

      // 标记通知为已读
      await markNotificationsAsRead({ notificationIds: [notification.id] });
    }
  } catch (error) {
    console.error('检查活动通知失败:', error);
  }
};
```

### 2. 登出清理逻辑 (authStore.ts:78-88)

```typescript
// 登出方法
logout: () => {
  // 清除活动弹窗标记，确保下次登录时重新显示
  sessionStorage.removeItem('activity_modal_shown');

  set({
    user: null,
    token: null,
    refreshToken: null,
    isAuthenticated: false,
  });
},
```

## 完整流程验证

### 场景 1: 用户登录 → 首次进入作品管理

1. 用户在登录页输入账号密码
2. 登录成功，跳转到作品管理界面（`/works`）
3. `WorksView` 组件挂载，触发 `useEffect(() => { checkForActivityNotifications() }, [])`
4. 检查 `sessionStorage.getItem('activity_modal_shown')` → 返回 `null`（因为是新会话）
5. 查询后端获取未读的活动/公告通知
6. 如果有符合条件的通知：
   - 显示 `ActivityModal` 弹窗
   - 设置 `sessionStorage.setItem('activity_modal_shown', 'true')`
   - 调用 API 标记通知为已读
7. ✅ **弹窗显示成功**

### 场景 2: 在同一会话中跳转回作品管理

1. 用户从作品管理页面跳转到其他页面（如设置页、通知中心等）
2. 用户点击导航或链接，再次回到作品管理界面（`/works`）
3. `WorksView` 组件重新挂载，触发 `useEffect(() => { checkForActivityNotifications() }, [])`
4. 检查 `sessionStorage.getItem('activity_modal_shown')` → 返回 `'true'`（因为同一会话内已显示过）
5. 函数提前返回，**不执行后续的通知查询和弹窗显示**
6. ✅ **弹窗不显示，用户体验良好**

### 场景 3: 用户登出后重新登录

1. 用户点击"退出登录"按钮
2. 触发 `Header.tsx` 中的 `handleLogout()` 函数
3. 调用 `authStore.logout()`，执行清理操作：
   - 调用 `sessionStorage.removeItem('activity_modal_shown')` 清除弹窗标记
   - 清空用户状态（user, token, refreshToken, isAuthenticated）
4. 跳转到登录页
5. 用户重新登录，再次进入作品管理界面
6. 检查 `sessionStorage.getItem('activity_modal_shown')` → 返回 `null`（已被清除）
7. ✅ **弹窗重新显示，符合预期**

### 场景 4: 用户关闭浏览器标签页后重新打开

1. 用户直接关闭浏览器标签页（没有点击登出）
2. 重新打开浏览器，访问网站
3. 由于使用了 `persist` 中间件，`localStorage` 中的认证信息（user, token）仍然存在
4. **但 `sessionStorage` 中的数据已被浏览器自动清除**
5. 自动登录后进入作品管理界面
6. 检查 `sessionStorage.getItem('activity_modal_shown')` → 返回 `null`
7. ✅ **弹窗显示，相当于新的登录会话**

## 技术要点

### 为什么使用 sessionStorage 而不是 localStorage？

| 特性 | sessionStorage | localStorage |
|------|---------------|--------------|
| **生命周期** | 标签页关闭即清除 | 永久保存，除非手动清除 |
| **作用域** | 仅当前标签页 | 同源所有标签页共享 |
| **适用场景** | 会话级临时数据 | 需要持久化的数据 |

**选择 sessionStorage 的原因：**
1. ✅ 符合"每次登录显示一次"的需求
2. ✅ 标签页关闭后自动清除，无需手动管理
3. ✅ 不会影响其他标签页的独立会话
4. ✅ 登出时清除简单明确

### 为什么在 logout 中清除 sessionStorage？

虽然用户登出后通常会跳转到登录页，sessionStorage 会在标签页关闭时自动清除，但我们仍然在 `logout()` 方法中显式清除 `activity_modal_shown` 标记，原因是：

1. **更清晰的意图表达**：代码明确表示"登出后重置弹窗状态"
2. **避免边界情况**：某些浏览器或扩展可能会保留 sessionStorage
3. **立即生效**：如果用户登出后立即在同一标签页重新登录，不依赖浏览器的自动清除
4. **代码可维护性**：未来如果需要在登出时清除其他 session 数据，已有明确的清理位置

## 测试清单

### ✅ 功能测试

- [ ] 登录后首次进入 `/works` 页面，弹窗正常显示
- [ ] 从 `/works` 跳转到其他页面再回来，弹窗不再显示
- [ ] 登出后重新登录，弹窗再次显示
- [ ] 关闭标签页重新打开（自动登录），弹窗再次显示
- [ ] 弹窗关闭后，通知已标记为已读

### ✅ 边界情况测试

- [ ] 如果没有符合条件的通知，不显示弹窗
- [ ] 多次快速刷新 `/works` 页面，弹窗只显示一次
- [ ] 在弹窗显示前快速离开页面，不会影响后续逻辑

### ✅ 用户体验测试

- [ ] 弹窗动画流畅（fade-in zoom-in）
- [ ] 点击"查看详情"跳转正确
- [ ] 点击"稍后查看"关闭弹窗
- [ ] 点击弹窗外部区域可关闭
- [ ] 点击右上角关闭按钮可关闭

## 相关文件

- `src/views/WorksView/index.tsx` - 弹窗触发逻辑
- `src/store/authStore.ts` - 登出清理逻辑
- `src/components/notifications/ActivityModal.tsx` - 弹窗组件
- `src/components/layout/Header.tsx` - 登出按钮
- `docs/activity-modal-usage.md` - 功能使用文档

## 总结

通过使用 `sessionStorage` 和在 `logout()` 中清除标记的组合方案，我们实现了：

1. ✅ **精确控制**：弹窗只在登录后首次进入作品管理时显示
2. ✅ **良好体验**：同一会话内不重复打扰用户
3. ✅ **正确重置**：登出后重新登录，弹窗能再次显示
4. ✅ **自动清理**：无需担心数据残留，标签页关闭自动清除
5. ✅ **代码清晰**：逻辑简单明了，易于维护和扩展
