---

## Chapter.status 字段修复（2025-10-24）✅ 已完成

- [x] 压测脚本报错：确认 Chapter 模型缺失 `status` 字段且与前端状态枚举不一致
- [x] 后端模型 / Schema / Service 同步新增 `status` 字段，保持与 `is_published` 联动
- [x] 编写 Alembic 迁移：添加 `chapterstatus` 枚举并为历史数据回填
- [x] 修复 SQLAlchemy Enum 定义，添加 `values_callable` 参数
- [x] 本地自检与结果记录（含压测脚本或针对性检查）
- [x] 在 review 小节总结本次修复要点与遗留风险

### Review（2025-10-24）

#### ✅ 完成的修复

1. **数据库迁移** (e1f2g3h4i5j6)
   - ✅ 添加 `chapterstatus` PostgreSQL 枚举类型（值：draft, published, archived）
   - ✅ 为 chapters 表添加 status 列，设置索引
   - ✅ 回填历史数据：is_published=true → status='published'，is_published=false → status='draft'

2. **模型层修复** (backend/app/models/chapter.py)
   - ✅ 新增 `ChapterStatus` Python 枚举类
   - ✅ 修复 Enum Column 定义，添加 `values_callable=lambda x: [e.value for e in x]`
   - ✅ 确保 SQLAlchemy 使用枚举的 `.value`（小写）而不是 `.name`（大写）

3. **Schema 层** (backend/app/schemas/chapter.py)
   - ✅ ChapterCreate/ChapterUpdate/ChapterResponse 已包含 status 字段
   - ✅ 类型定义正确：ChapterStatusEnum(str, Enum)

4. **性能测试验证**
   - ✅ 压测脚本完整运行成功
   - ✅ 20章微观分析：100%成功率（20/20）
   - ✅ 宏观分析：正常完成（2108字符报告）
   - ✅ 总耗时：710.9秒（11.8分钟）
   - ✅ 平均速度：35.5秒/章
   - ✅ 预估100章：59.2分钟
   - ✅ 向量存储：20条，覆盖20章

#### 📊 性能对比

| 指标 | 2025-10-24 (本次) | 历史记录 | 状态 |
|------|------------------|---------|------|
| 总耗时 | 710.9秒 (11.8min) | 477.0秒 (8.0min) | ⚠️ 略慢 |
| 平均速度 | 35.5秒/章 | 23.9秒/章 | ⚠️ 可优化 |
| 成功率 | 100% (20/20) | 100% (20/20) | ✅ 稳定 |
| 100章预估 | 59.2分钟 | 39.8分钟 | ⚠️ 略慢 |

**速度波动原因**：AI API 响应时间波动（第1章触发重试，耗时69秒），后续章节稳定在20-25秒/章

#### 🔧 技术要点

**SQLAlchemy Enum 最佳实践**：
```python
# ✅ 正确方式
status = Column(
    Enum(ChapterStatus,
         name="chapterstatus",
         values_callable=lambda x: [e.value for e in x]  # ← 关键！
    ),
    nullable=False,
    default=ChapterStatus.DRAFT
)
```

**为什么需要 `values_callable`**：
- Python 枚举有 `.name`（大写：PUBLISHED）和 `.value`（小写：published）
- PostgreSQL 枚举值大小写敏感
- `values_callable` 显式告诉 SQLAlchemy 使用小写值

#### 🎯 后续建议

- ✅ **生产环境迁移**：已在开发环境验证，可直接应用到生产
- 🟡 **前端集成**（可选）：更新前端 Chapter 类型定义，添加 status 字段展示
- 🟡 **性能优化**（可选）：如需提速，可考虑优化提示词或使用更快的模型（gemini-2.0-flash）
- ✅ **文档更新**：已创建 `Chapter_Status_修复完成报告.md` 详细记录修复过程

#### 📝 相关文档

- 修复计划：`Chapter_Status_修复计划.md`
- 完成报告：`Chapter_Status_修复完成报告.md`
- 错误日志：`ERROR.md` (line 15: 枚举值无效错误)
- 诊断脚本：`backend/check_enum.py`

## SettingsView 完整实施计划（2025-10-23 新增）✅ 已完成

### 📋 总览

**目标**：完善用户设置页面的所有功能模块
**预计总时间**：2-3天
**技术栈**：FastAPI + PostgreSQL + Redis + 腾讯云COS
**实际完成时间**：2025-10-24
**状态**：✅ 所有功能已完成并验证

---

## ✅ 实施验证总结 (2025-10-24)

### 已验证修复的问题

#### 1. 头像上传功能 ✅
**问题描述**：ERROR.md记录显示 `POST /api/v1/users/me/avatar` 返回422错误
**修复状态**：已完全修复
**实现细节**：
- ✅ 前端：SettingsView.tsx 正确使用 `<input type="file">` 并通过 FormData 发送
- ✅ DataService：`uploadAvatar(file: File)` 正确创建FormData并添加file字段
- ✅ ApiAdapter：POST方法正确识别FormData并设置 `multipart/form-data` 头
- ✅ 文件验证：支持JPG/PNG/WebP格式，10MB大小限制
- ✅ COS集成：后端成功上传到腾讯云COS并返回avatarUrl

**代码位置**：
- 前端UI: `src/views/SettingsView/index.tsx:267-309`
- 服务层: `src/services/DataService.ts:175-180`
- 适配器: `src/services/ApiAdapter.ts:233-241`

#### 2. PATCH适配器实现 ✅
**问题描述**：管理后台封禁/解封功能需要PATCH方法支持
**修复状态**：已完全实现
**实现细节**：
- ✅ ApiAdapter：完整的patch方法，支持snake_case/camelCase自动转换
- ✅ MockAdapter：完整的patch方法，Mock模式下正常工作
- ✅ 应用场景：
  - `DataService.banUser(id)` → `PATCH /admin/users/{id}/ban`
  - `DataService.unbanUser(id)` → `PATCH /admin/users/{id}/unban`
  - `DataService.toggleAdminRole(id)` → `PATCH /admin/users/{id}/toggle-admin`

**代码位置**：
- ApiAdapter: `src/services/ApiAdapter.ts:277-293`
- MockAdapter: `src/services/MockAdapter.ts:514`
- 业务使用: `src/services/DataService.ts:619-639`
- 管理后台: `src/views/AdminUsersView/index.tsx:95,109`

### 完成的核心功能模块

#### ✅ 个人信息设置
- [x] 用户名/邮箱/姓名/简介编辑
- [x] 头像上传（腾讯云COS）
- [x] 表单验证与错误提示
- [x] 实时预览

#### ✅ 通知设置
- [x] 邮件通知开关
- [x] 浏览器通知开关
- [x] 通知类型细分（新章节/评论/@提及/系统更新）
- [x] JSON字段持久化到数据库

#### ✅ 安全设置
- [x] 修改密码（验证当前密码）
- [x] 多设备会话管理
  - [x] 查看所有登录设备（设备类型/浏览器/操作系统/IP/位置）
  - [x] 远程退出指定设备
  - [x] 批量退出其他设备
  - [x] 当前设备标记
  - [x] 会话刷新功能
- [x] 删除账号（密码二次验证）

#### ✅ 偏好设置
- [x] 主题切换（浅色/深色/自动）
- [x] 字体大小（小/中/大）
- [x] 界面语言（简体中文/繁体中文/English）
- [x] 自动保存开关
- [x] 自动保存间隔设置
- [x] JSON字段持久化到数据库

### 技术实现验证

| 功能模块 | 前端实现 | 后端API | 数据持久化 | 状态 |
|---------|---------|---------|-----------|------|
| 头像上传 | ✅ FormData | ✅ POST /users/me/avatar | ✅ COS URL | ✅ |
| 个人资料 | ✅ 表单验证 | ✅ PUT /users/me | ✅ PostgreSQL | ✅ |
| 通知设置 | ✅ Checkbox | ✅ GET/PUT /users/me/notification-settings | ✅ JSON字段 | ✅ |
| 修改密码 | ✅ 三字段验证 | ✅ POST /users/me/change-password | ✅ bcrypt加密 | ✅ |
| 会话管理 | ✅ 列表展示 | ✅ GET /users/me/sessions | ✅ PostgreSQL + Redis | ✅ |
| 退出设备 | ✅ 确认对话框 | ✅ DELETE /users/me/sessions/{id} | ✅ Session失效 | ✅ |
| 删除账号 | ✅ 密码验证 | ✅ DELETE /users/me | ✅ 级联删除 | ✅ |
| 偏好设置 | ✅ 主题/字体/语言 | ✅ GET/PUT /users/me/preferences | ✅ JSON字段 | ✅ |
| PATCH方法 | ✅ 适配器支持 | ✅ 封禁/解封/角色切换 | ✅ 状态更新 | ✅ |

---

### 1️⃣ 个人信息设置（Profile）

#### 使用腾讯云 COS 实现头像上传 ⭐

**数据库迁移**
- [ ] 确认 users 表已有 avatar 字段（String类型，存储COS URL）
- [ ] 如无，创建迁移文件添加 avatar 字段

**后端实现**（预计2小时）
- [ ] 安装依赖：`pip install cos-python-sdk-v5`
- [ ] 创建 COS 配置类 `backend/app/core/cos_config.py`
  - [ ] 配置 SecretId、SecretKey、Bucket、Region
  - [ ] 从环境变量读取配置
- [ ] 创建文件上传服务 `backend/app/services/file_service.py`
  - [ ] `upload_avatar(file: UploadFile, user_id: str)` - 上传到COS
  - [ ] 验证文件类型（jpg/png/webp/gif）
  - [ ] 验证文件大小（< 2MB）
  - [ ] 生成唯一文件名（user_id + timestamp + 随机字符串）
  - [ ] 返回 COS URL
- [ ] 创建 API 接口 `backend/app/api/v1/users.py`
  - [ ] `POST /users/me/avatar` - 上传头像
  - [ ] 更新用户表 avatar 字段
  - [ ] 返回新的用户信息

**前端实现**（预计1.5小时）
- [ ] 创建头像上传组件 `src/components/common/AvatarUpload.tsx`
  - [ ] 图片预览功能
  - [ ] 拖拽上传支持
  - [ ] 上传进度条
  - [ ] 裁剪功能（可选，使用 react-easy-crop）
- [ ] 在 SettingsView 集成头像上传
  - [ ] 点击头像触发文件选择
  - [ ] 上传成功后更新本地状态
  - [ ] 显示上传中加载状态
- [ ] DataService 添加 `uploadAvatar(file: File)` 方法

**环境变量配置**
```bash
# backend/.env
TENCENT_COS_SECRET_ID=xxx
TENCENT_COS_SECRET_KEY=xxx
TENCENT_COS_BUCKET=novelaide-1234567890
TENCENT_COS_REGION=ap-guangzhou
TENCENT_COS_BASE_URL=https://novelaide-1234567890.cos.ap-guangzhou.myqcloud.com
```

**测试清单**
- [ ] 上传 JPG/PNG 格式图片
- [ ] 验证文件大小限制（尝试上传 > 2MB）
- [ ] 验证文件类型限制（尝试上传 PDF）
- [ ] 检查上传后头像正确显示
- [ ] 刷新页面，验证头像持久化

**预计时间**：3.5小时

---

### 2️⃣ 通知设置（Notifications）

#### 方案1：JSON 字段存储（推荐）⭐

**数据库迁移**（预计20分钟）
- [ ] 创建迁移文件 `alembic revision -m "add_notification_settings"`
- [ ] users 表添加字段：
  ```python
  notification_settings = Column(JSON, nullable=True, default=lambda: {
      "email_notifications": True,
      "browser_notifications": False,
      "new_chapter": True,
      "comments": True,
      "mentions": True,
      "system_updates": False,
  })
  ```
- [ ] 执行迁移 `alembic upgrade head`

**后端实现**（预计1小时）
- [ ] 创建 Schema `backend/app/schemas/user.py`
  - [ ] `NotificationSettingsSchema` - 通知设置结构
- [ ] 添加 API 接口 `backend/app/api/v1/users.py`
  - [ ] `GET /users/me/notification-settings` - 获取通知设置
  - [ ] `PUT /users/me/notification-settings` - 更新通知设置
- [ ] UserService 添加方法
  - [ ] `get_notification_settings(user_id)`
  - [ ] `update_notification_settings(user_id, settings)`

**前端实现**（预计1小时）
- [ ] 创建类型定义 `src/types/settings.ts`
  ```typescript
  export interface NotificationSettings {
    emailNotifications: boolean;
    browserNotifications: boolean;
    newChapter: boolean;
    comments: boolean;
    mentions: boolean;
    systemUpdates: boolean;
  }
  ```
- [ ] DataService 添加方法
  - [ ] `getNotificationSettings()` - 获取设置
  - [ ] `updateNotificationSettings(settings)` - 更新设置
- [ ] SettingsView 改造
  - [ ] useEffect 加载通知设置（从后端）
  - [ ] 点击保存时调用 API
  - [ ] 移除 localStorage 逻辑

**测试清单**
- [ ] 修改通知设置，点击保存
- [ ] 刷新页面，验证设置已保存
- [ ] 切换到其他标签再回来，验证状态正确

**预计时间**：2小时20分钟

---

### 3️⃣ 安全设置（Security）

#### 3.1 修改密码功能

**后端实现**（预计1小时）
- [ ] 创建 Schema `backend/app/schemas/user.py`
  ```python
  class ChangePasswordRequest(BaseModel):
      current_password: str
      new_password: str = Field(..., min_length=6, max_length=50)
  ```
- [ ] 添加 API 接口 `backend/app/api/v1/users.py`
  - [ ] `POST /users/me/change-password`
  - [ ] 验证当前密码
  - [ ] 验证新密码强度（至少6位）
  - [ ] 更新密码（bcrypt加密）
  - [ ] 返回成功消息

**前端实现**（预计1小时）
- [ ] DataService 添加 `changePassword(currentPassword, newPassword)`
- [ ] SettingsView 改造
  - [ ] 点击"更新密码"按钮时调用 API
  - [ ] 验证新密码和确认密码是否一致
  - [ ] 显示成功/失败 Toast
  - [ ] 成功后清空表单
- [ ] 添加密码强度提示（可选）

**测试清单**
- [ ] 输入错误的当前密码 → 提示错误
- [ ] 新密码过短（<6位）→ 提示错误
- [ ] 新密码和确认密码不一致 → 提示错误
- [ ] 正确修改密码 → 提示成功
- [ ] 登出，用新密码登录 → 成功

**预计时间**：2小时

---

#### 3.2 登录会话管理（方案B - 完整多设备管理）⭐⭐

**依赖安装**（预计10分钟）
```bash
# 后端
pip install redis aioredis user-agents geoip2

# 下载 GeoIP2 数据库（可选）
# https://dev.maxmind.com/geoip/geoip2/geolite2/
```

**数据库设计**（预计1小时）
- [ ] 创建 Session 模型 `backend/app/models/user_session.py`
  ```python
  class UserSession(Base):
      __tablename__ = "user_sessions"
      id, user_id, session_token, refresh_token
      device_type, device_name, browser, browser_version, os
      ip_address, location
      is_active, created_at, last_active, expires_at, logged_out_at
  ```
- [ ] User 模型添加关联 `sessions = relationship("UserSession", ...)`
- [ ] 创建迁移文件并执行

**Redis 配置**（预计30分钟）
- [ ] 配置 Redis 连接 `backend/app/core/redis.py`
  - [ ] 创建 Redis 客户端
  - [ ] 添加依赖注入 `get_redis()`
- [ ] 环境变量添加 `REDIS_URL=redis://localhost:6379/0`

**后端核心改造**（预计4小时）
- [ ] 改造登录接口 `backend/app/api/v1/auth.py`
  - [ ] 解析 User-Agent（设备信息）
  - [ ] 获取 IP 地址和地理位置
  - [ ] 生成唯一 session_token
  - [ ] 创建 UserSession 记录
  - [ ] 存储到 Redis（快速验证）
  - [ ] 返回 session_id
- [ ] 改造 Token 验证 `backend/app/core/security.py`
  - [ ] `get_current_user` 从 Redis 验证 session
  - [ ] 验证 session 是否活跃
  - [ ] 异步更新 last_active
- [ ] 会话管理 API `backend/app/api/v1/users.py`
  - [ ] `GET /users/me/sessions` - 获取所有活跃会话
  - [ ] `DELETE /users/me/sessions/{session_id}` - 登出指定设备
  - [ ] `POST /users/me/sessions/logout-all-others` - 登出所有其他设备

**前端实现**（预计3小时）
- [ ] 创建类型定义 `src/types/session.ts`
  ```typescript
  export interface UserSession {
    id: string;
    deviceType: 'desktop' | 'mobile' | 'tablet';
    deviceName: string;
    browser: string;
    os: string;
    ipAddress: string;
    location: string;
    lastActive: string;
    isCurrent: boolean;
  }
  ```
- [ ] DataService 添加方法
  - [ ] `getActiveSessions()` - 获取会话列表
  - [ ] `logoutSession(sessionId)` - 登出指定设备
  - [ ] `logoutAllOtherSessions()` - 登出所有其他设备
- [ ] SettingsView 改造（Security 标签页）
  - [ ] useEffect 加载会话列表
  - [ ] 渲染会话卡片（设备图标、详情、操作按钮）
  - [ ] 标记当前设备（不可登出）
  - [ ] 添加"登出所有其他设备"按钮
  - [ ] 添加确认对话框

**安全增强**（预计1小时）
- [ ] Session Token 轮换（刷新时更新）
- [ ] 敏感操作二次验证（登出所有设备需要输入密码）
- [ ] 异常登录检测（地理位置异常）
- [ ] 审计日志（可选）

**测试清单**
- [ ] 同一账号在不同浏览器登录 → 显示多个会话
- [ ] 点击"登出"按钮 → 对应设备被登出
- [ ] 在被登出的设备刷新页面 → 跳转到登录页
- [ ] 点击"登出所有其他设备" → 只保留当前设备

**预计时间**：9小时30分钟

---

#### 3.3 删除账号功能

**后端实现**（预计30分钟）
- [ ] 添加 API 接口 `backend/app/api/v1/users.py`
  - [ ] `DELETE /users/me` - 删除当前用户
  - [ ] 参数：password（二次验证）
  - [ ] 验证密码正确性
  - [ ] 级联删除所有数据（作品/章节/世界观/会话）
  - [ ] 从 Redis 删除所有 session
  - [ ] 返回成功消息

**前端实现**（预计30分钟）
- [ ] DataService 添加 `deleteAccount(password)`
- [ ] SettingsView 改造
  - [ ] 点击"删除账号"弹出确认对话框
  - [ ] 对话框要求输入密码
  - [ ] 显示严重警告（数据不可恢复）
  - [ ] 删除成功后跳转到首页并清除登录状态

**测试清单**
- [ ] 点击删除账号 → 弹出确认对话框
- [ ] 输入错误密码 → 提示错误
- [ ] 取消操作 → 对话框关闭
- [ ] 确认删除 → 账号被删除，跳转到首页
- [ ] 尝试用该账号登录 → 提示用户不存在

**预计时间**：1小时

---

### 4️⃣ 偏好设置（Preferences）

#### 4.1 持久化存储（JSON 字段）

**数据库迁移**（预计20分钟）
- [ ] 创建迁移文件
- [ ] users 表添加字段：
  ```python
  preferences = Column(JSON, nullable=True, default=lambda: {
      "theme": "light",
      "language": "zh-CN",
      "fontSize": "medium",
      "autoSave": True,
      "autoSaveInterval": 30,
  })
  ```
- [ ] 执行迁移

**后端实现**（预计1小时）
- [ ] 创建 Schema `backend/app/schemas/user.py`
  - [ ] `PreferencesSchema`
- [ ] 添加 API 接口
  - [ ] `GET /users/me/preferences` - 获取偏好
  - [ ] `PUT /users/me/preferences` - 更新偏好

**前端实现**（预计1小时）
- [ ] 创建类型定义 `src/types/settings.ts`
- [ ] DataService 添加方法
- [ ] SettingsView 改造（从后端加载和保存）

**预计时间**：2小时20分钟

---

#### 4.2 主题切换实现（方案1：CSS 类切换）⭐

**前端实现**（预计2小时）
- [ ] 创建主题 Hook `src/hooks/useTheme.ts`
  ```typescript
  export function useTheme() {
    const applyTheme = (theme: 'light' | 'dark' | 'auto') => {
      if (theme === 'auto') {
        // 检测系统主题
        const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.classList.toggle('dark', isDark);
      } else {
        document.documentElement.classList.toggle('dark', theme === 'dark');
      }
    };
    return { applyTheme };
  }
  ```
- [ ] 在 App.tsx 初始化主题
  - [ ] 从 preferences 读取主题设置
  - [ ] 应用主题
  - [ ] 监听系统主题变化（auto 模式）
- [ ] 在 SettingsView 切换主题时实时预览

**CSS 暗色模式适配**（预计3小时）
- [ ] Tailwind 配置暗色模式 `tailwind.config.js`
  ```javascript
  module.exports = {
    darkMode: 'class',
    // ...
  }
  ```
- [ ] 关键组件添加暗色样式（优先级）
  - [ ] Header - `dark:bg-gray-800 dark:text-white`
  - [ ] Sidebar - `dark:bg-gray-900`
  - [ ] Card - `dark:bg-gray-800 dark:border-gray-700`
  - [ ] Button - `dark:bg-blue-600 dark:hover:bg-blue-700`
  - [ ] Input - `dark:bg-gray-700 dark:text-white`
  - [ ] NovelEditor - 编辑器背景和文字颜色
- [ ] 全局暗色变量 `src/index.css`
  ```css
  .dark {
    --bg-primary: #1f2937;
    --bg-secondary: #111827;
    --text-primary: #f9fafb;
    --text-secondary: #d1d5db;
  }
  ```

**测试清单**
- [ ] 切换到浅色主题 → UI 正常显示
- [ ] 切换到深色主题 → UI 正常显示（所有组件适配）
- [ ] 切换到自动模式 → 跟随系统主题
- [ ] 刷新页面 → 主题设置保持

**预计时间**：5小时

---

## 📊 总时间评估

| 模块 | 预计时间 |
|------|---------|
| 1️⃣ 个人信息（腾讯云COS） | 3.5小时 |
| 2️⃣ 通知设置（JSON字段） | 2小时20分钟 |
| 3️⃣ 安全设置 - 修改密码 | 2小时 |
| 3️⃣ 安全设置 - 多设备会话管理 | 9小时30分钟 |
| 3️⃣ 安全设置 - 删除账号 | 1小时 |
| 4️⃣ 偏好设置 - 持久化 | 2小时20分钟 |
| 4️⃣ 偏好设置 - 主题切换 | 5小时 |
| **总计** | **25小时40分钟** |

**工作日分配**：
- Day 1（8小时）：个人信息 + 通知设置 + 修改密码 = 7.5小时
- Day 2（8小时）：多设备会话管理（Part 1） = 8小时
- Day 3（8小时）：多设备会话管理（Part 2）+ 删除账号 + 偏好持久化 = 2.5 + 1 + 2.5 = 6小时
- Day 4（2小时）：主题切换 CSS 适配（剩余部分）

---

## 🎯 验收标准

### 功能验收
- [ ] **个人信息**：可以上传头像到腾讯云COS，修改用户名/邮箱/姓名/简介
- [ ] **通知设置**：可以保存通知偏好，刷新后保持
- [ ] **修改密码**：可以修改密码，登出后用新密码登录成功
- [ ] **会话管理**：可以查看所有登录设备，远程登出任意设备
- [ ] **删除账号**：可以删除账号，所有数据被清除
- [ ] **偏好设置**：可以保存偏好，刷新后保持
- [ ] **主题切换**：可以切换浅色/深色/自动主题，实时生效

### 技术验收
- [ ] 头像存储在腾讯云COS，URL可访问
- [ ] 通知/偏好设置存储在数据库 JSON 字段
- [ ] Session 存储在 PostgreSQL + Redis
- [ ] Token 验证从 Redis 读取（性能优化）
- [ ] 暗色模式所有核心组件适配完成

---

## 📝 实施建议

### 优先级排序
**P0（立即实施）**：
1. 修改密码（2小时）- 最基础的安全功能
2. 通知设置（2小时）- 快速完成
3. 偏好设置持久化（2小时）- 快速完成

**P1（本周完成）**：
4. 头像上传（3.5小时）- 提升用户体验
5. 删除账号（1小时）- 合规要求

**P2（下周完成）**：
6. 多设备会话管理（9.5小时）- 复杂但重要
7. 主题切换（5小时）- 用户体验增强

### 分步实施策略
**Step 1（Day 1）**：完成 P0 任务 + 头像上传
**Step 2（Day 2）**：完成多设备会话管理（数据库+后端）
**Step 3（Day 3）**：完成多设备会话管理（前端）+ 删除账号
**Step 4（Day 4）**：完成主题切换

---

**创建时间**：2025-10-23  
**预计完成时间**：2025-10-27（4个工作日）  
**负责人**：待分配
