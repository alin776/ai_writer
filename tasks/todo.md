# SettingsView 完善开发计划

## 📊 总体进度：85% 完成

### ✅ 已完成部分（85%）

#### 1. 个人信息设置
- [x] 前端 UI 实现
- [x] 头像上传组件
- [x] 腾讯云 COS 集成
- [x] 后端 API：PUT /users/me
- [x] 后端 API：POST /users/me/avatar
- [x] 文件类型和大小验证

#### 2. 通知设置
- [x] 前端 UI 实现
- [x] 后端 API：GET /users/me/notification-settings
- [x] 后端 API：PUT /users/me/notification-settings
- [x] User 模型 notification_settings 字段（JSONB）

#### 3. 偏好设置
- [x] 前端 UI 实现
- [x] useTheme hook 实现
- [x] 主题切换（浅色/深色/自动）
- [x] 后端 API：GET /users/me/preferences
- [x] 后端 API：PUT /users/me/preferences
- [x] User 模型 preferences 字段（JSONB）

#### 4. 安全设置 - 修改密码
- [x] 前端 UI 实现
- [x] 密码验证逻辑
- [x] 后端 API：POST /users/me/change-password

#### 5. 安全设置 - 删除账号
- [x] 前端 UI 实现
- [x] 确认对话框
- [x] 后端 API：DELETE /users/me

---

### 🔧 待实现部分（15%）

#### 6. 安全设置 - 多设备会话管理

**前端（已完成）：**
- [x] 会话列表 UI
- [x] 设备图标显示
- [x] 退出按钮
- [x] 退出其他设备按钮
- [x] DataService 方法

**后端（待实现）：**
- [ ] 任务 1：添加会话管理 Schema 定义
- [ ] 任务 2：实现 UserService 会话管理方法
- [ ] 任务 3：实现会话管理 API 路由
- [ ] 任务 4：前后端联调测试

---

## 🎯 实施步骤

### 任务 1：Schema 定义（预计0.5小时）
**文件：** `backend/app/schemas/user.py`
- 添加 UserSessionResponse schema
- 定义会话数据结构

### 任务 2：UserService 会话方法（预计1.5小时）
**文件：** `backend/app/services/user_service.py`
- 实现 get_user_sessions 方法
- 实现 logout_session 方法
- 实现 logout_other_sessions 方法

### 任务 3：API 路由实现（预计1小时）
**文件：** `backend/app/api/v1/users.py`
- 添加 GET /me/sessions 端点
- 添加 DELETE /me/sessions/{session_id} 端点
- 添加 POST /me/sessions/logout-others 端点

### 任务 4：联调测试（预计1小时）
- 测试获取会话列表
- 测试退出指定会话
- 测试退出其他设备

---

## ⏱️ 预计总时间：4 小时
