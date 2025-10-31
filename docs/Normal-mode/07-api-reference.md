# API 参考文档

> **NovelAIde API 参考文档**
> 版本: v2.17
> 最后更新: 2025-01-28

**重要说明**:
- 本文档覆盖核心API模块(认证、用户、作品、章节、世界观、AI服务等)
- 详细的新功能API请参考: [BACKEND_API_FOR_FRONTEND.md](./BACKEND_API_FOR_FRONTEND.md)
  - 个人知识库系统 (7个接口)
  - AI拆书功能 (8个接口)
  - 小说评审增强系统 (15个接口)
  - 去AI痕迹功能 (7个接口)
  - 改写历史管理 (4个接口)

---

## 目录

- [1. 概述](#1-概述)
- [2. 认证方式](#2-认证方式)
- [3. 认证API](#3-认证api)
- [4. 用户管理API](#4-用户管理api)
- [5. 作品管理API](#5-作品管理api)
- [6. 章节管理API](#6-章节管理api)
- [7. 世界观API](#7-世界观api)
- [8. AI服务API](#8-ai服务api)
  - [8.9 AI人性化重写](#89-ai人性化重写-new) ⭐⭐ NEW
  - [8.10 获取人性化重写用户画像](#810-获取人性化重写用户画像)
  - [8.11 更新人性化重写设置](#811-更新人性化重写设置)
  - [8.12 获取人性化重写历史](#812-获取人性化重写历史)
  - [8.13 获取人性化重写统计](#813-获取人性化重写统计)
- [9. 小说分析API](#9-小说分析api)
- [10. 管理后台API](#10-管理后台api)
- [11. 时间线API](#11-时间线api)
- [12. 关系管理API](#12-关系管理api)
- [13. 分组管理API](#13-分组管理api)
- [14. 搜索API](#14-搜索api)
- [15. AI日志API](#15-ai日志api)
- [16. 导出导入API](#16-导出导入api)
- [17. AI改写助手API](#17-ai改写助手api) ⭐⭐ NEW
- [18. 错误代码](#18-错误代码)
- [19. 相关链接](#19-相关链接)

---

## 1. 概述

NovelAIde API 提供完整的RESTful接口，支持小说创作的全流程功能，包括：

- **用户认证**：注册、登录、Token管理
- **作品管理**：作品CRUD、章节管理、统计数据
- **世界观构建**：角色、地点、设定、关系管理
- **AI辅助**：续写、润色、翻译、扩写、总结、评估
- **AI改写助手**：多模型并发改写对比 ⭐⭐
- **AI人性化重写**：三阶段处理+双AI架构 ⭐⭐
- **小说评审系统**：8维度评审+任务管理+版本控制 ⭐⭐⭐
- **AI拆书功能**：11维度分析+智能建议 ⭐⭐⭐
- **知识库系统**：RAG语义搜索 ⭐⭐⭐⭐⭐
- **小说分析**：微观分析、宏观分析、章节概括
- **管理后台**：用户管理、统计数据、系统配置

**API模块统计**: 19个模块，150+个端点

**Base URL**: `http://localhost:8000/api/v1`

**技术栈**: FastAPI + Python 3.11+ + PostgreSQL + Redis

---

## 2. 认证方式

### JWT Token认证

所有需要认证的API请求必须在请求头中携带JWT Token：

```http
Authorization: Bearer <access_token>
```

### Token获取

通过登录接口获取Token：

```http
POST /auth/login
```

### Token刷新

Access Token过期后，使用Refresh Token刷新：

```http
POST /auth/refresh
```

### Token存储

- 前端使用`localStorage`存储Token
- 存储键名：`auth-storage`
- 包含`accessToken`和`refreshToken`

---

## 3. 认证API

### 3.1 用户注册

**接口**: `POST /api/v1/auth/register`

**描述**: 创建新用户账号

**请求体**:
```json
{
  "username": "novelist",
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**响应**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "novelist",
  "email": "user@example.com",
  "isAdmin": false,
  "createdAt": "2025-10-24T10:00:00Z",
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "Bearer"
}
```

**特性**:
- ✅ 注册即登录（自动返回Token）
- ✅ 自动创建登录会话记录
- ✅ 密码bcrypt加密存储
- ✅ 邮箱唯一性验证

---

### 3.2 用户登录

**接口**: `POST /api/v1/auth/login`

**描述**: 用户登录认证

**请求体**:
```json
{
  "username": "novelist",
  "password": "SecurePass123!"
}
```

**响应**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "novelist",
  "email": "user@example.com",
  "isAdmin": false,
  "createdAt": "2025-10-24T10:00:00Z",
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "Bearer"
}
```

**特性**:
- ✅ 支持用户名或邮箱登录
- ✅ 自动创建会话记录（包含设备指纹、IP地址）
- ✅ Token有效期：Access 24小时，Refresh 7天

---

### 3.3 Token刷新

**接口**: `POST /api/v1/auth/refresh`

**描述**: 使用Refresh Token刷新Access Token

**请求体**:
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应**:
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "Bearer"
}
```

---

### 3.4 获取当前用户信息

**接口**: `GET /api/v1/auth/me`

**描述**: 获取当前登录用户信息

**请求头**:
```http
Authorization: Bearer <access_token>
```

**响应**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "novelist",
  "email": "user@example.com",
  "isAdmin": false,
  "avatarUrl": "https://cdn.example.com/avatars/user.jpg",
  "bio": "热爱写作的小说家",
  "createdAt": "2025-10-24T10:00:00Z",
  "updatedAt": "2025-10-24T12:00:00Z"
}
```

---

## 4. 用户管理API

### 4.1 更新用户资料

**接口**: `PUT /api/v1/users/me`

**描述**: 更新当前用户的个人资料

**请求头**:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求体**:
```json
{
  "username": "new_novelist",
  "email": "newemail@example.com",
  "bio": "专注于奇幻小说创作"
}
```

**响应**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "new_novelist",
  "email": "newemail@example.com",
  "bio": "专注于奇幻小说创作",
  "updatedAt": "2025-10-24T12:00:00Z"
}
```

---

### 4.2 上传头像

**接口**: `POST /api/v1/users/me/avatar`

**描述**: 上传用户头像（集成腾讯云COS）

**请求头**:
```http
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**请求体**:
```
file: <binary_image_data>
```

**响应**:
```json
{
  "avatarUrl": "https://cdn.example.com/avatars/550e8400-e29b-41d4.jpg"
}
```

**限制**:
- 文件类型：JPG, PNG, WebP
- 文件大小：最大10MB
- 图片尺寸：建议200x200

---

### 4.3 修改密码

**接口**: `POST /api/v1/users/me/change-password`

**描述**: 修改当前用户密码

**请求体**:
```json
{
  "currentPassword": "OldPass123!",
  "newPassword": "NewPass456!",
  "confirmPassword": "NewPass456!"
}
```

**响应**:
```json
{
  "success": true,
  "message": "密码修改成功"
}
```

---

### 4.4 删除账号

**接口**: `DELETE /api/v1/users/me`

**描述**: 删除当前用户账号（级联删除所有数据）

**请求体**:
```json
{
  "password": "SecurePass123!"
}
```

**响应**:
```json
{
  "success": true,
  "message": "账号已成功删除"
}
```

---

### 4.5 获取会话列表

**接口**: `GET /api/v1/users/me/sessions`

**描述**: 获取当前用户的所有登录会话

**响应**:
```json
[
  {
    "id": "session_001",
    "deviceType": "Desktop",
    "browser": "Chrome 119",
    "os": "Windows 11",
    "ipAddress": "192.168.1.100",
    "location": "北京, 中国",
    "lastActiveAt": "2025-10-24T12:00:00Z",
    "isCurrent": true,
    "createdAt": "2025-10-24T10:00:00Z"
  },
  {
    "id": "session_002",
    "deviceType": "Mobile",
    "browser": "Safari 17",
    "os": "iOS 17",
    "ipAddress": "192.168.1.101",
    "location": "上海, 中国",
    "lastActiveAt": "2025-10-23T20:00:00Z",
    "isCurrent": false,
    "createdAt": "2025-10-23T18:00:00Z"
  }
]
```

---

### 4.6 退出指定会话

**接口**: `DELETE /api/v1/users/me/sessions/{session_id}`

**描述**: 退出指定设备的登录会话

**响应**:
```json
{
  "success": true,
  "message": "会话已终止"
}
```

---

### 4.7 退出其他设备

**接口**: `POST /api/v1/users/me/sessions/logout-others`

**描述**: 退出除当前设备外的所有会话

**响应**:
```json
{
  "success": true,
  "message": "已退出3个其他设备",
  "loggedOutCount": 3
}
```

---

### 4.8 获取通知设置

**接口**: `GET /api/v1/users/me/notifications`

**描述**: 获取用户的通知偏好设置

**响应**:
```json
{
  "emailNotifications": true,
  "browserNotifications": false,
  "notificationTypes": {
    "newChapter": true,
    "comment": true,
    "mention": false,
    "systemUpdate": true
  }
}
```

---

### 4.9 更新通知设置

**接口**: `PUT /api/v1/users/me/notifications`

**描述**: 更新用户的通知偏好设置

**请求体**:
```json
{
  "emailNotifications": true,
  "browserNotifications": true,
  "notificationTypes": {
    "newChapter": true,
    "comment": true,
    "mention": true,
    "systemUpdate": true
  }
}
```

**响应**:
```json
{
  "success": true,
  "message": "通知设置已更新"
}
```

---

### 4.10 获取偏好设置

**接口**: `GET /api/v1/users/me/preferences`

**描述**: 获取用户的偏好设置

**响应**:
```json
{
  "theme": "dark",
  "fontSize": "medium",
  "language": "zh-CN",
  "autoSave": true
}
```

---

### 4.11 更新偏好设置

**接口**: `PUT /api/v1/users/me/preferences`

**描述**: 更新用户的偏好设置

**请求体**:
```json
{
  "theme": "light",
  "fontSize": "large",
  "language": "en-US",
  "autoSave": false
}
```

**响应**:
```json
{
  "success": true,
  "message": "偏好设置已更新"
}
```

---

## 5. 作品管理API

### 5.1 获取作品列表

**接口**: `GET /api/v1/works`

**描述**: 获取当前用户的所有作品

**查询参数**:
- `page`: 页码（默认1）
- `pageSize`: 每页数量（默认20）
- `status`: 作品状态筛选（可选）

**响应**:
```json
{
  "total": 15,
  "page": 1,
  "pageSize": 20,
  "works": [
    {
      "id": "work_001",
      "title": "《奇幻世界》",
      "description": "一个充满魔法的世界...",
      "coverUrl": "https://cdn.example.com/covers/work_001.jpg",
      "genre": "奇幻",
      "status": "draft",
      "totalWords": 50000,
      "totalChapters": 10,
      "createdAt": "2025-10-01T10:00:00Z",
      "updatedAt": "2025-10-24T12:00:00Z"
    }
  ]
}
```

---

### 5.2 获取作品详情

**接口**: `GET /api/v1/works/{work_id}`

**描述**: 获取指定作品的详细信息

**响应**:
```json
{
  "id": "work_001",
  "title": "《奇幻世界》",
  "description": "一个充满魔法的世界...",
  "coverUrl": "https://cdn.example.com/covers/work_001.jpg",
  "genre": "奇幻",
  "status": "draft",
  "totalWords": 50000,
  "totalChapters": 10,
  "authorId": "550e8400-e29b-41d4-a716-446655440000",
  "createdAt": "2025-10-01T10:00:00Z",
  "updatedAt": "2025-10-24T12:00:00Z"
}
```

---

### 5.3 创建作品

**接口**: `POST /api/v1/works`

**描述**: 创建新作品

**请求体**:
```json
{
  "title": "《我的新小说》",
  "description": "这是一部精彩的小说",
  "genre": "都市",
  "status": "draft"
}
```

**响应**:
```json
{
  "id": "work_002",
  "title": "《我的新小说》",
  "description": "这是一部精彩的小说",
  "genre": "都市",
  "status": "draft",
  "totalWords": 0,
  "totalChapters": 0,
  "createdAt": "2025-10-24T12:00:00Z",
  "updatedAt": "2025-10-24T12:00:00Z"
}
```

---

### 5.4 更新作品

**接口**: `PUT /api/v1/works/{work_id}`

**描述**: 更新作品信息

**请求体**:
```json
{
  "title": "《奇幻世界·修订版》",
  "description": "全新修订的奇幻巨作",
  "status": "published"
}
```

**响应**:
```json
{
  "id": "work_001",
  "title": "《奇幻世界·修订版》",
  "description": "全新修订的奇幻巨作",
  "status": "published",
  "updatedAt": "2025-10-24T12:30:00Z"
}
```

---

### 5.5 删除作品

**接口**: `DELETE /api/v1/works/{work_id}`

**描述**: 删除指定作品（级联删除所有章节和世界观数据）

**响应**:
```json
{
  "success": true,
  "message": "作品《奇幻世界》已删除"
}
```

---

## 6. 章节管理API

### 6.1 获取章节列表

**接口**: `GET /api/v1/chapters/work/{work_id}`

**描述**: 获取指定作品的所有章节

**响应**:
```json
[
  {
    "id": "chapter_001",
    "workId": "work_001",
    "title": "第一章 初次相遇",
    "content": "故事从这里开始...",
    "wordCount": 3000,
    "order": 1,
    "status": "published",
    "summary": "主角在咖啡馆遇到了神秘女子",
    "createdAt": "2025-10-01T10:00:00Z",
    "updatedAt": "2025-10-24T11:00:00Z"
  },
  {
    "id": "chapter_002",
    "workId": "work_001",
    "title": "第二章 命运转折",
    "content": "意外的发现...",
    "wordCount": 2800,
    "order": 2,
    "status": "draft",
    "summary": null,
    "createdAt": "2025-10-02T10:00:00Z",
    "updatedAt": "2025-10-24T12:00:00Z"
  }
]
```

---

### 6.2 获取章节详情

**接口**: `GET /api/v1/chapters/{chapter_id}`

**描述**: 获取指定章节的详细内容

**响应**:
```json
{
  "id": "chapter_001",
  "workId": "work_001",
  "title": "第一章 初次相遇",
  "content": "<p>故事从这里开始...</p><p>那是一个阳光明媚的下午...</p>",
  "wordCount": 3000,
  "order": 1,
  "status": "published",
  "summary": "主角在咖啡馆遇到了神秘女子",
  "viewCount": 150,
  "publishedAt": "2025-10-01T15:00:00Z",
  "createdAt": "2025-10-01T10:00:00Z",
  "updatedAt": "2025-10-24T11:00:00Z"
}
```

---

### 6.3 创建章节

**接口**: `POST /api/v1/chapters`

**描述**: 在作品中创建新章节

**请求体**:
```json
{
  "workId": "work_001",
  "title": "第三章 意外发现",
  "content": "<p>新章节的内容...</p>",
  "order": 3
}
```

**响应**:
```json
{
  "id": "chapter_003",
  "workId": "work_001",
  "title": "第三章 意外发现",
  "content": "<p>新章节的内容...</p>",
  "wordCount": 0,
  "order": 3,
  "status": "draft",
  "createdAt": "2025-10-24T12:00:00Z",
  "updatedAt": "2025-10-24T12:00:00Z"
}
```

---

### 6.4 更新章节

**接口**: `PUT /api/v1/chapters/{chapter_id}`

**描述**: 更新章节内容

**请求体**:
```json
{
  "title": "第一章 命运的相遇",
  "content": "<p>修改后的内容...</p>",
  "status": "published"
}
```

**响应**:
```json
{
  "id": "chapter_001",
  "title": "第一章 命运的相遇",
  "content": "<p>修改后的内容...</p>",
  "wordCount": 3200,
  "status": "published",
  "updatedAt": "2025-10-24T12:30:00Z"
}
```

**特性**:
- ✅ 自动计算字数（去除HTML标签）
- ✅ 自动保存功能
- ✅ 更新作品统计数据

---

### 6.5 删除章节

**接口**: `DELETE /api/v1/chapters/{chapter_id}`

**描述**: 删除指定章节

**响应**:
```json
{
  "success": true,
  "message": "章节已删除"
}
```

---

### 6.6 章节排序

**接口**: `POST /api/v1/chapters/reorder`

**描述**: 批量更新章节顺序

**请求体**:
```json
{
  "workId": "work_001",
  "chapterOrders": [
    { "id": "chapter_003", "order": 1 },
    { "id": "chapter_001", "order": 2 },
    { "id": "chapter_002", "order": 3 }
  ]
}
```

**响应**:
```json
{
  "success": true,
  "message": "章节顺序已更新"
}
```

---

### 6.7 生成章节概括

**接口**: `POST /api/v1/chapters/{chapter_id}/summary`

**描述**: 使用AI生成章节剧情概括（150-300字）

**查询参数**:
- `regenerate`: 是否强制重新生成（默认false）

**响应**:
```json
{
  "id": "chapter_001",
  "summary": "主角林风在咖啡馆偶遇神秘女子苏雨，两人因为一本古书展开对话。苏雨透露她正在寻找失落的魔法典籍，而林风恰好在旧书市场见过类似的书。两人决定合作寻找，这次相遇成为了命运的转折点。",
  "updatedAt": "2025-10-24T12:00:00Z"
}
```

**特性**:
- ✅ AI自动提取主要事件、人物行动、冲突转折
- ✅ 概括自动保存到数据库
- ✅ 支持强制重新生成

---

## 7. 世界观API

### 7.1 角色管理

#### 7.1.1 获取角色列表

**接口**: `GET /api/v1/worldview/works/{work_id}/characters`

**响应**:
```json
[
  {
    "id": "char_001",
    "workId": "work_001",
    "name": "林风",
    "role": "主角",
    "description": "一个寻找真相的年轻人",
    "personality": "勇敢、好奇、善良",
    "goal": "找到失落的魔法典籍",
    "relationships": [
      {
        "targetId": "char_002",
        "type": "friend",
        "description": "志同道合的伙伴"
      }
    ],
    "tags": ["主角", "男性", "20岁"],
    "createdAt": "2025-10-01T10:00:00Z",
    "updatedAt": "2025-10-24T11:00:00Z"
  }
]
```

#### 7.1.2 创建角色

**接口**: `POST /api/v1/worldview/works/{work_id}/characters`

**请求体**:
```json
{
  "name": "苏雨",
  "role": "女主角",
  "description": "神秘的魔法师",
  "personality": "冷静、聪慧、神秘",
  "goal": "保护魔法世界的平衡",
  "tags": ["女主角", "女性", "22岁", "魔法师"]
}
```

#### 7.1.3 更新角色

**接口**: `PUT /api/v1/worldview/characters/{character_id}`

#### 7.1.4 删除角色

**接口**: `DELETE /api/v1/worldview/characters/{character_id}`

---

### 7.2 地点管理

#### 7.2.1 获取地点列表

**接口**: `GET /api/v1/worldview/works/{work_id}/locations`

**响应**:
```json
[
  {
    "id": "loc_001",
    "workId": "work_001",
    "name": "星辰咖啡馆",
    "type": "建筑",
    "description": "城市中心的一家古老咖啡馆，据说隐藏着许多秘密",
    "relatedLocations": ["loc_002"],
    "tags": ["咖啡馆", "城市", "重要地点"],
    "createdAt": "2025-10-01T10:00:00Z",
    "updatedAt": "2025-10-24T11:00:00Z"
  }
]
```

#### 7.2.2 创建地点

**接口**: `POST /api/v1/worldview/works/{work_id}/locations`

**请求体**:
```json
{
  "name": "魔法学院",
  "type": "建筑",
  "description": "培养魔法师的神秘学府",
  "tags": ["学院", "魔法", "重要地点"]
}
```

#### 7.2.3 更新地点

**接口**: `PUT /api/v1/worldview/locations/{location_id}`

#### 7.2.4 删除地点

**接口**: `DELETE /api/v1/worldview/locations/{location_id}`

---

### 7.3 设定管理

#### 7.3.1 获取设定列表

**接口**: `GET /api/v1/worldview/works/{work_id}/settings`

**响应**:
```json
[
  {
    "id": "setting_001",
    "workId": "work_001",
    "title": "魔法体系",
    "category": "力量体系",
    "content": "本世界的魔法分为五大元素：火、水、风、土、光。每个魔法师只能掌握一种元素...",
    "tags": ["魔法", "体系", "核心设定"],
    "createdAt": "2025-10-01T10:00:00Z",
    "updatedAt": "2025-10-24T11:00:00Z"
  }
]
```

#### 7.3.2 创建设定

**接口**: `POST /api/v1/worldview/works/{work_id}/settings`

**请求体**:
```json
{
  "title": "魔法等级",
  "category": "力量体系",
  "content": "魔法师分为五个等级：见习、初级、中级、高级、大师",
  "tags": ["魔法", "等级", "核心设定"]
}
```

#### 7.3.3 更新设定

**接口**: `PUT /api/v1/worldview/settings/{setting_id}`

#### 7.3.4 删除设定

**接口**: `DELETE /api/v1/worldview/settings/{setting_id}`

---

### 7.4 作品规范

#### 7.4.1 获取作品规范

**接口**: `GET /api/v1/worldview/works/{work_id}/guidelines`

**响应**:
```json
{
  "id": "guideline_001",
  "workId": "work_001",
  "genre": "奇幻",
  "tone": "严肃",
  "theme": "成长与冒险",
  "targetAudience": "青年读者",
  "createdAt": "2025-10-01T10:00:00Z",
  "updatedAt": "2025-10-24T11:00:00Z"
}
```

#### 7.4.2 创建/更新作品规范

**接口**: `POST /api/v1/worldview/works/{work_id}/guidelines`

**请求体**:
```json
{
  "genre": "奇幻冒险",
  "tone": "轻松幽默",
  "theme": "友情与正义",
  "targetAudience": "全年龄读者"
}
```

---

### 7.5 AI创作规范

#### 7.5.1 获取AI规范

**接口**: `GET /api/v1/worldview/works/{work_id}/ai-guidelines`

**响应**:
```json
{
  "id": "ai_guideline_001",
  "workId": "work_001",
  "businessGoal": "打造年度热门奇幻小说",
  "targetReaders": "18-30岁喜欢奇幻的年轻读者",
  "writingStyle": "生动形象，富有画面感",
  "coreConflict": "个人成长与世界危机的双线冲突",
  "narrativeRhythm": "快节奏，每3-5章一个爽点",
  "primaryGenre": "奇幻",
  "worldIntro": "一个魔法与科技并存的现代世界",
  "powerSystemName": "元素魔法体系",
  "protagonistName": "林风",
  "protagonistGoal": "成为最强魔法师，守护世界和平",
  "createdAt": "2025-10-01T10:00:00Z",
  "updatedAt": "2025-10-24T11:00:00Z"
}
```

#### 7.5.2 AI生成规范

**接口**: `POST /api/v1/worldview/works/{work_id}/ai-guidelines/generate`

**描述**: 使用AI自动生成31个字段的完整创作规范

**请求体**:
```json
{
  "workTitle": "奇幻世界",
  "workDescription": "一个充满魔法的现代都市故事",
  "genre": "都市奇幻"
}
```

**响应**: 返回完整的31字段AI规范（参考7.5.1的响应格式）

**特性**:
- ✅ 自动生成31个字段（战略定位/IP架构/叙事引擎/文字质感等）
- ✅ 首次创建时自动分散到其他标签页
- ✅ 支持流式响应

---

### 7.6 关系管理

#### 7.6.1 获取关系列表

**接口**: `GET /api/v1/worldview/works/{work_id}/relationships`

**响应**:
```json
[
  {
    "id": "rel_001",
    "workId": "work_001",
    "sourceId": "char_001",
    "sourceType": "character",
    "targetId": "char_002",
    "targetType": "character",
    "type": "friend",
    "description": "志同道合的冒险伙伴",
    "strength": 8,
    "createdAt": "2025-10-01T10:00:00Z"
  }
]
```

#### 7.6.2 创建关系

**接口**: `POST /api/v1/worldview/works/{work_id}/relationships`

**请求体**:
```json
{
  "sourceId": "char_001",
  "sourceType": "character",
  "targetId": "char_003",
  "targetType": "character",
  "type": "enemy",
  "description": "宿命的对手",
  "strength": 9
}
```

---

### 7.7 时间线管理

#### 7.7.1 获取时间线事件

**接口**: `GET /api/v1/worldview/works/{work_id}/timeline`

**响应**:
```json
[
  {
    "id": "event_001",
    "workId": "work_001",
    "title": "初次觉醒",
    "description": "林风第一次使用魔法",
    "chapterId": "chapter_001",
    "eventType": "milestone",
    "relatedEntities": ["char_001"],
    "timestamp": "2025-01-01T00:00:00Z",
    "createdAt": "2025-10-01T10:00:00Z"
  }
]
```

#### 7.7.2 创建时间线事件

**接口**: `POST /api/v1/worldview/works/{work_id}/timeline`

---

### 7.8 实体分组

#### 7.8.1 获取分组列表

**接口**: `GET /api/v1/worldview/works/{work_id}/groups`

**响应**:
```json
[
  {
    "id": "group_001",
    "workId": "work_001",
    "name": "主要角色",
    "color": "#3B82F6",
    "icon": "users",
    "memberCount": 5,
    "createdAt": "2025-10-01T10:00:00Z"
  }
]
```

#### 7.8.2 创建分组

**接口**: `POST /api/v1/worldview/works/{work_id}/groups`

---

### 7.9 聚合接口

#### 7.9.1 获取完整世界观数据

**接口**: `GET /api/v1/worldview/works/{work_id}/all`

**描述**: 一次性获取作品的所有世界观数据（角色+地点+设定+规范+关系+时间线）

**响应**:
```json
{
  "characters": [...],
  "locations": [...],
  "settings": [...],
  "guidelines": {...},
  "aiGuidelines": {...},
  "relationships": [...],
  "timeline": [...],
  "groups": [...]
}
```

---

## 8. AI服务API

### 8.1 AI续写

**接口**: `POST /api/v1/ai/continue`

**描述**: AI根据上下文自动续写故事（支持SSE流式响应）

**请求体**:
```json
{
  "context": "夜色如墨，月光洒在窗台上...",
  "length": 500,
  "style": "suspense"
}
```

**响应**（流式SSE）:
```
data: {"chunk": "他", "done": false}
data: {"chunk": "缓缓", "done": false}
data: {"chunk": "走", "done": false}
...
data: {"chunk": "。", "done": true}
```

**特性**:
- ✅ 支持流式实时输出
- ✅ 自动过滤`<think>`标签和reasoning内容
- ✅ 生成内容自动黄色高亮标记

---

### 8.2 AI扩写

**接口**: `POST /api/v1/ai/expand`

**描述**: 将选中文本扩写3-5倍，增加细节描写

**请求体**:
```json
{
  "text": "他走进了房间",
  "expandRatio": 3
}
```

**响应**（流式SSE）:
```
data: {"chunk": "他轻轻推开房门", "done": false}
data: {"chunk": "，门轴发出吱呀的声响", "done": false}
...
```

**特性**:
- ✅ 五感描写（视觉、听觉、触觉、嗅觉、味觉）
- ✅ 慢镜头动作分解
- ✅ 电影编剧视角

---

### 8.3 AI总结

**接口**: `POST /api/v1/ai/summarize`

**描述**: 将选中文本总结为150字精简概要

**请求体**:
```json
{
  "text": "长篇文本内容...",
  "maxLength": 150
}
```

**响应**（流式SSE）:
```
data: {"chunk": "主角发现了", "done": false}
...
```

**特性**:
- ✅ 专业编辑视角
- ✅ 侧重转折点和伏笔
- ✅ 保留核心信息

---

### 8.4 AI润色

**接口**: `POST /api/v1/ai/polish`

**描述**: 优化选中文本，提升流畅度和文学性

**请求体**:
```json
{
  "text": "他很高兴地走了过来",
  "style": "literary"
}
```

**响应**（流式SSE）:
```
data: {"chunk": "他面带喜色", "done": false}
...
```

**特性**:
- ✅ 语言大师视角
- ✅ 4步润色策略（词语/句式/修辞/节奏）
- ✅ 出版级标准

---

### 8.5 AI翻译

**接口**: `POST /api/v1/ai/translate`

**描述**: 智能识别语言并翻译（中英互译）

**请求体**:
```json
{
  "text": "这是一个美好的早晨",
  "targetLanguage": "en"
}
```

**响应**（流式SSE）:
```
data: {"chunk": "This is", "done": false}
data: {"chunk": " a beautiful", "done": false}
...
```

---

### 8.6 AI自动补全

**接口**: `POST /api/v1/ai/autocomplete`

**描述**: 根据当前输入实时提供补全建议

**请求体**:
```json
{
  "context": "他打开门，看到",
  "maxLength": 50
}
```

---

### 8.7 AI评价内容质量 ⭐ NEW

**接口**: `POST /api/v1/ai/evaluate`

**描述**: 对AI生成的内容进行专业评价,返回5维度评分和改进建议

**请求体**:
```json
{
  "text": "林风深吸一口气,缓缓推开了那扇厚重的木门...",
  "operation_type": "continue",
  "context": {
    "work_id": "work_001",
    "chapter_id": "chapter_001",
    "work_title": "我的小说",
    "chapter_title": "第一章",
    "previous_text": "这是前文片段..."
  }
}
```

**参数说明**:
- `text` (required): 待评价的AI生成内容 (10-10000字符)
- `operation_type` (required): 操作类型
  - `continue`: 续写
  - `polish`: 润色
  - `expand`: 扩写
  - `translate`: 翻译
  - `summarize`: 总结
- `context` (optional): 上下文信息
  - `work_id`: 作品ID
  - `chapter_id`: 章节ID
  - `work_title`: 作品标题
  - `chapter_title`: 章节标题
  - `previous_text`: 前文片段 (最多1000字)

**响应**:
```json
{
  "overall_score": 82.0,
  "dimensions": {
    "literary_quality": 85.0,
    "coherence": 80.0,
    "creativity": 75.0,
    "emotional_impact": 88.0,
    "pacing": 82.0
  },
  "highlights": [
    "语言流畅,文字优美",
    "情感表达细腻,有感染力",
    "节奏把控得当,张弛有度"
  ],
  "issues": [
    "部分描写过于抽象,缺乏具体细节",
    "某些情节转折略显生硬"
  ],
  "suggestions": [
    "增加感官描写,让场景更生动",
    "在情节转折处增加铺垫"
  ],
  "evaluation_id": "770e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-10-26T14:30:00Z"
}
```

**5维度评价体系**:

| 维度 | 说明 | 评分范围 |
|------|------|---------|
| literary_quality | 文学性 - 语言质量、修辞手法、文字美感 | 0-100 |
| coherence | 连贯性 - 与前文衔接、逻辑流畅度 | 0-100 |
| creativity | 创意性 - 新颖度、想象力、打破常规 | 0-100 |
| emotional_impact | 情感感染力 - 情感表达、读者共鸣度 | 0-100 |
| pacing | 节奏把控 - 快慢适度、张弛有度 | 0-100 |

**特性**:
- ✅ 5维度专业评分
- ✅ 具体优点/问题/建议列表
- ✅ 自动记录到AI日志系统
- ✅ Token消耗和成本统计
- ✅ 评价记录持久化

**成本估算**:
- 评价500字文本: ~1,450 prompt tokens + ~500 completion tokens ≈ $0.02 (GPT-4)

**注意事项**:
- 评价由用户主动触发,不会自动执行
- 评价结果保存到 `evaluation_records` 表
- AI调用记录到 `ai_call_logs` 表,operation_type 为 `evaluate`

---

### 8.8 AI自动补全

**接口**: `POST /api/v1/ai/autocomplete`

**描述**: 根据当前输入实时提供补全建议

**请求体**:
```json
{
  "context": "他打开门，看到",
  "maxLength": 50
}
```

**响应**:
```json
{
  "suggestion": "一个陌生的男子站在门外，手里拿着一封信"
}
```

---

### 8.9 AI人性化重写 ⭐⭐ NEW

**接口**: `POST /api/v1/humanize/rewrite`

**描述**: 检测并去除AI生成文本的机器痕迹,使其更加自然、人性化

**请求头**:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求体**:
```json
{
  "text": "首先,我们需要认真分析这个问题。其次,我们应该制定详细的计划。",
  "intensity": "medium",
  "function_type": "continue",
  "enable_detection": true,
  "enable_validation": false
}
```

**请求参数**:
- `text` (string, 必填): 待处理的文本 (10-5000字符)
- `intensity` (enum, 默认medium): 去痕迹强度
  - `light` - 轻度去痕迹 (保守)
  - `medium` - 中度去痕迹 (平衡)
  - `strong` - 强度去痕迹 (激进)
- `function_type` (enum, 必填): 功能类型
  - `continue` - 续写
  - `polish` - 润色
  - `expand` - 扩写
  - `translate` - 翻译
  - `summarize` - 总结
- `enable_detection` (bool, 默认true): 是否执行AI痕迹检测
- `enable_validation` (bool, 默认false): 是否执行结果验证

**响应** (200 OK):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "original_text": "首先,我们需要认真分析这个问题...",
  "humanized_text": "我们先分析一下这个问题，再决定怎么做。",
  "intensity": "medium",
  "overall_score_before": 77.0,
  "overall_score_after": 45.0,
  "improvement_rate": 0.42,
  "dimensions_before": {
    "structure": {
      "score": 80,
      "description": "文本结构规整度",
      "issues": ["使用'首先...其次'结构"]
    },
    "language": {
      "score": 75,
      "description": "语言风格",
      "issues": ["书面语过多", "词汇过于正式"]
    },
    "expression": {
      "score": 70,
      "description": "表达方式",
      "issues": ["缺乏口语化表达"]
    }
  },
  "dimensions_after": {
    "structure": {
      "score": 45,
      "description": "文本结构规整度",
      "issues": []
    },
    "language": {
      "score": 40,
      "description": "语言风格",
      "issues": []
    },
    "expression": {
      "score": 50,
      "description": "表达方式",
      "issues": []
    }
  },
  "detected_patterns": [
    "首先...其次...最后...",
    "需要认真",
    "详细的计划"
  ],
  "processing_time": 8.5,
  "created_at": "2025-10-28T10:00:00Z"
}
```

**特性**:
- ✅ **三阶段智能处理**: 检测 → 改写 → 验证(可选)
- ✅ **7维度AI痕迹评分**: 结构/语言/表达/逻辑/情感/创意/整体
- ✅ **双AI架构**: 快速模型(gemini-2.5-flash-lite)检测+标准模型改写
- ✅ **智能画像学习**: 自动记录用户偏好,动态调整策略
- ✅ **分级数据存储**: 核心数据永久保存,详情数据7天过期
- ✅ **改写支持流式输出**: 实时显示改写进度

**处理流程**:
1. **检测阶段** (~3-5秒): 使用快速AI模型检测7维度AI痕迹
2. **改写阶段** (~5-10秒): 使用标准AI模型进行人性化改写(支持流式)
3. **验证阶段** (~3-5秒,可选): 再次检测确认改写效果

**7维度评分说明**:

| 维度 | 说明 | 高分特征(AI痕迹) | 低分特征(自然) |
|------|------|----------------|---------------|
| structure | 文本结构 | 规整、模板化 | 自然、灵活 |
| language | 语言风格 | 书面、正式 | 口语、随意 |
| expression | 表达方式 | 客观、理性 | 主观、感性 |
| logic | 逻辑连贯 | 过于严密 | 适度跳跃 |
| emotion | 情感表达 | 平淡、客观 | 丰富、真实 |
| creativity | 创意性 | 套路、常见 | 独特、新颖 |
| overall | 整体印象 | 综合评分 | 综合评分 |

**成本估算**:
- 检测: ~1,500 tokens → $0.001
- 改写: ~2,000 tokens → $0.003
- 验证: ~1,500 tokens → $0.001
- 总计: ~$0.005/次 (含验证)

**注意事项**:
- 文本长度限制: 10-5000字符
- 检测和验证使用快速模型,改写使用标准模型
- 改写结果自动保存到 `humanize_sessions` 表
- AI调用记录到 `ai_call_logs` 表

**相关接口**:
- GET /api/v1/humanize/profile - 获取用户画像
- GET /api/v1/humanize/history - 获取历史记录
- GET /api/v1/humanize/stats - 获取统计数据
- POST /api/v1/humanize/feedback - 提交用户反馈

---

### 8.10 获取人性化重写用户画像

**接口**: `GET /api/v1/humanize/profile`

**描述**: 获取当前用户的人性化重写偏好设置和使用统计

**响应** (200 OK):
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "total_uses": 15,
  "avg_text_length": 250,
  "most_used_function": "continue",
  "preferred_intensity": "medium",
  "preferred_speed_over_quality": false,
  "is_novel_writer": true,
  "total_accepted": 12,
  "total_rejected": 3,
  "accept_rate": 0.8,
  "humanize_enabled_global": true,
  "humanize_enabled_by_function": {
    "continue": true,
    "polish": false,
    "expand": true
  },
  "display_mode": "full",
  "created_at": "2025-10-20T10:00:00Z",
  "updated_at": "2025-10-28T10:00:00Z"
}
```

---

### 8.11 更新人性化重写设置

**接口**: `PUT /api/v1/humanize/profile/settings`

**描述**: 更新用户的人性化重写偏好设置

**请求体**:
```json
{
  "humanize_enabled_global": true,
  "humanize_enabled_by_function": {
    "continue": true,
    "polish": false,
    "expand": true
  },
  "preferred_intensity": "strong",
  "display_mode": "simplified"
}
```

**响应** (200 OK): 返回更新后的画像对象

---

### 8.12 获取人性化重写历史

**接口**: `GET /api/v1/humanize/history?page=1&page_size=20`

**描述**: 获取用户的人性化重写历史记录列表

**响应** (200 OK):
```json
{
  "sessions": [
    {
      "id": "session1",
      "original_text_preview": "首先,我们需要...",
      "humanized_text_preview": "我们先分析...",
      "overall_score_before": 77.0,
      "overall_score_after": 45.0,
      "intensity": "medium",
      "user_feedback": "accepted",
      "created_at": "2025-10-28T10:00:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 20
}
```

---

### 8.13 获取人性化重写统计

**接口**: `GET /api/v1/humanize/stats`

**描述**: 获取用户的人性化重写使用统计

**响应** (200 OK):
```json
{
  "total_uses": 15,
  "total_accepted": 12,
  "total_rejected": 3,
  "accept_rate": 0.8,
  "avg_improvement_rate": 0.38,
  "most_common_patterns": [
    "首先...其次...最后...",
    "综上所述",
    "值得注意的是"
  ],
  "avg_text_length": 250,
  "by_intensity": {
    "light": 3,
    "medium": 10,
    "strong": 2
  },
  "by_function": {
    "continue": 8,
    "polish": 5,
    "expand": 2
  }
}
```

---

## 9. 小说分析API

### 9.1 启动小说分析

**接口**: `POST /api/v1/analysis/works/{work_id}/start`

**描述**: 启动作品的完整分析（微观+宏观分析）

**响应**:
```json
{
  "taskId": "analysis_task_001",
  "status": "processing",
  "message": "分析任务已启动"
}
```

**特性**:
- ✅ 后台异步处理
- ✅ 微观分析：逐章节JSON结构化
- ✅ 宏观分析：人物成长轨迹、世界观图谱、核心矛盾演变
- ✅ 向量存储与相似度检索

---

### 9.2 查询分析状态

**接口**: `GET /api/v1/analysis/works/{work_id}/status`

**描述**: 查询分析任务的进度和状态

**响应**:
```json
{
  "status": "processing",
  "progress": 65,
  "currentChapter": 13,
  "totalChapters": 20,
  "estimatedTime": "5分钟",
  "startedAt": "2025-10-24T12:00:00Z"
}
```

**状态说明**:
- `pending`: 等待开始
- `processing`: 处理中
- `completed`: 已完成
- `failed`: 失败

---

### 9.3 获取分析结果

**接口**: `GET /api/v1/analysis/works/{work_id}/result`

**描述**: 获取完整的分析报告

**响应**:
```json
{
  "id": "analysis_001",
  "workId": "work_001",
  "status": "completed",
  "microAnalysis": {
    "chapterSummaries": [
      {
        "chapterId": "chapter_001",
        "summary": "主角初次觉醒魔法能力",
        "keyEvents": ["觉醒", "遇见导师"],
        "characters": ["林风", "苏雨"],
        "locations": ["星辰咖啡馆"]
      }
    ]
  },
  "macroAnalysis": {
    "characterGrowth": "主角从普通学生成长为强大魔法师...",
    "worldView": "魔法与科技并存的现代都市世界...",
    "coreConflict": "个人成长与世界危机的双线冲突..."
  },
  "completedAt": "2025-10-24T12:35:00Z"
}
```

---

### 9.4 提取世界观

**接口**: `POST /api/v1/analysis/works/{work_id}/extract-worldview`

**描述**: 从分析结果中自动提取世界观数据（角色/地点/设定）

**请求体**:
```json
{
  "extractCharacters": true,
  "extractLocations": true,
  "extractSettings": true
}
```

**响应**:
```json
{
  "success": true,
  "extracted": {
    "charactersCount": 5,
    "locationsCount": 3,
    "settingsCount": 4
  },
  "message": "成功提取12个世界观实体"
}
```

**特性**:
- ✅ 智能合并微观+宏观数据
- ✅ 多级验证（黑名单+正则+描述质量）
- ✅ 自动去重

---

## 10. 管理后台API

### 10.1 获取统计数据

**接口**: `GET /api/v1/admin/statistics`

**描述**: 获取系统统计概览

**权限**: 仅管理员

**响应**:
```json
{
  "totalUsers": 1250,
  "totalWorks": 3500,
  "totalChapters": 45000,
  "aiCallsToday": 8900,
  "activeTasks": 12
}
```

---

### 10.2 获取用户增长数据

**接口**: `GET /api/v1/admin/users-growth`

**描述**: 获取用户增长趋势数据

**权限**: 仅管理员

**查询参数**:
- `days`: 天数（默认30）

**响应**:
```json
[
  { "date": "2025-10-01", "count": 1200 },
  { "date": "2025-10-02", "count": 1215 },
  ...
  { "date": "2025-10-24", "count": 1250 }
]
```

---

### 10.3 获取用户列表

**接口**: `GET /api/v1/admin/users`

**描述**: 获取用户列表（支持搜索和分页）

**权限**: 仅管理员

**查询参数**:
- `page`: 页码（默认1）
- `pageSize`: 每页数量（默认20）
- `search`: 搜索关键词（可选）

**响应**:
```json
{
  "total": 1250,
  "page": 1,
  "pageSize": 20,
  "users": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "novelist",
      "email": "user@example.com",
      "isAdmin": false,
      "isBanned": false,
      "worksCount": 3,
      "createdAt": "2025-10-01T10:00:00Z"
    }
  ]
}
```

---

### 10.4 封禁用户

**接口**: `PATCH /api/v1/admin/users/{user_id}/ban`

**描述**: 封禁指定用户

**权限**: 仅管理员

**响应**:
```json
{
  "success": true,
  "message": "用户已被封禁"
}
```

---

### 10.5 解封用户

**接口**: `PATCH /api/v1/admin/users/{user_id}/unban`

**描述**: 解封指定用户

**权限**: 仅管理员

**响应**:
```json
{
  "success": true,
  "message": "用户已解封"
}
```

---

### 10.6 切换管理员角色

**接口**: `PATCH /api/v1/admin/users/{user_id}/toggle-admin`

**描述**: 切换用户的管理员权限

**权限**: 仅管理员

**响应**:
```json
{
  "success": true,
  "message": "用户角色已更新",
  "isAdmin": true
}
```

---

### 10.7 获取AI使用统计

**接口**: `GET /api/v1/admin/ai-usage`

**描述**: 获取AI调用统计数据

**权限**: 仅管理员

**响应**:
```json
{
  "totalCalls": 125000,
  "totalCost": 1250.50,
  "avgCallsPerDay": 4000,
  "topModels": [
    { "model": "gpt-4", "calls": 50000, "cost": 800.00 },
    { "model": "claude-3.5-sonnet", "calls": 45000, "cost": 300.50 }
  ]
}
```

---

## 11. 时间线API

### 11.1 创建时间线事件

**接口**: `POST /api/v1/timeline/`

**描述**: 创建新的时间线事件

**请求体**:
```json
{
  "workId": "550e8400-e29b-41d4-a716-446655440000",
  "entityId": "character-123",
  "entityType": "character",
  "eventType": "milestone",
  "title": "主角觉醒天赋",
  "description": "在第5章，主角意外觉醒了冰系天赋",
  "chapterId": "chapter-456",
  "chapterNumber": 5,
  "color": "#3b82f6"
}
```

**响应**:
```json
{
  "id": "event-789",
  "workId": "550e8400-e29b-41d4-a716-446655440000",
  "entityId": "character-123",
  "entityType": "character",
  "eventType": "milestone",
  "title": "主角觉醒天赋",
  "description": "在第5章，主角意外觉醒了冰系天赋",
  "chapterId": "chapter-456",
  "chapterNumber": 5,
  "color": "#3b82f6",
  "createdAt": "2025-10-24T10:00:00Z"
}
```

---

### 11.2 获取事件详情

**接口**: `GET /api/v1/timeline/{event_id}`

**描述**: 获取单个时间线事件详情

**响应**: 同创建接口

---

### 11.3 获取作品时间线

**接口**: `GET /api/v1/timeline/work/{work_id}`

**描述**: 获取作品的所有时间线事件

**查询参数**:
- `entityId` (可选): 筛选特定实体的事件
- `entityType` (可选): 筛选特定类型的实体 (`character`, `location`, `setting`)
- `eventType` (可选): 筛选事件类型 (`milestone`, `change`, `created`, `removed`)

**响应**:
```json
{
  "events": [
    {
      "id": "event-789",
      "entityId": "character-123",
      "entityType": "character",
      "eventType": "milestone",
      "title": "主角觉醒天赋",
      "chapterNumber": 5,
      "color": "#3b82f6"
    }
  ],
  "total": 15
}
```

---

### 11.4 更新时间线事件

**接口**: `PUT /api/v1/timeline/{event_id}`

**描述**: 更新时间线事件信息

**请求体**: 同创建接口（所有字段可选）

**响应**: 更新后的事件对象

---

### 11.5 删除时间线事件

**接口**: `DELETE /api/v1/timeline/{event_id}`

**描述**: 删除时间线事件

**响应**:
```json
{
  "success": true,
  "message": "事件已删除"
}
```

---

### 11.6 获取章节锚点

**接口**: `GET /api/v1/timeline/work/{work_id}/chapter-anchors`

**描述**: 获取作品所有章节作为时间线锚点

**响应**:
```json
{
  "anchors": [
    {
      "chapterId": "chapter-1",
      "chapterNumber": 1,
      "title": "第一章 开端",
      "eventCount": 3
    },
    {
      "chapterId": "chapter-2",
      "chapterNumber": 2,
      "title": "第二章 修炼",
      "eventCount": 5
    }
  ]
}
```

---

## 12. 关系管理API

### 12.1 创建关系

**接口**: `POST /api/v1/relationships/`

**描述**: 创建实体间的关系

**请求体**:
```json
{
  "workId": "550e8400-e29b-41d4-a716-446655440000",
  "sourceId": "character-123",
  "sourceType": "character",
  "targetId": "character-456",
  "targetType": "character",
  "relationshipType": "亲属",
  "label": "父子",
  "description": "主角与父亲的关系",
  "strength": 9,
  "direction": "two-way",
  "lineStyle": "solid",
  "color": "#ef4444"
}
```

**关系类型**:
- `亲属` (红色)
- `师徒` (紫色)
- `好友` (绿色)
- `敌对` (橙色)
- `同伴` (蓝色)
- `恋人` (粉色)
- `上下级` (灰色)
- `竞争` (黄色)
- `其他` (默认)

**响应**:
```json
{
  "id": "rel-789",
  "workId": "550e8400-e29b-41d4-a716-446655440000",
  "sourceId": "character-123",
  "sourceType": "character",
  "targetId": "character-456",
  "targetType": "character",
  "relationshipType": "亲属",
  "label": "父子",
  "description": "主角与父亲的关系",
  "strength": 9,
  "direction": "two-way",
  "lineStyle": "solid",
  "color": "#ef4444",
  "createdAt": "2025-10-24T10:00:00Z"
}
```

---

### 12.2 获取关系详情

**接口**: `GET /api/v1/relationships/{relationship_id}`

**描述**: 获取单个关系详情

**响应**: 同创建接口

---

### 12.3 获取作品关系列表

**接口**: `GET /api/v1/relationships/work/{work_id}`

**描述**: 获取作品的所有关系

**查询参数**:
- `entityId` (可选): 筛选包含特定实体的关系
- `relationshipType` (可选): 筛选关系类型

**响应**:
```json
{
  "relationships": [
    {
      "id": "rel-789",
      "sourceId": "character-123",
      "targetId": "character-456",
      "relationshipType": "亲属",
      "label": "父子",
      "strength": 9
    }
  ],
  "total": 25
}
```

---

### 12.4 更新关系

**接口**: `PUT /api/v1/relationships/{relationship_id}`

**描述**: 更新关系信息

**请求体**: 同创建接口（所有字段可选）

**响应**: 更新后的关系对象

---

### 12.5 删除关系

**接口**: `DELETE /api/v1/relationships/{relationship_id}`

**描述**: 删除关系

**响应**:
```json
{
  "success": true,
  "message": "关系已删除"
}
```

---

## 13. 分组管理API

### 13.1 创建分组

**接口**: `POST /api/v1/groups/`

**描述**: 创建实体分组

**请求体**:
```json
{
  "workId": "550e8400-e29b-41d4-a716-446655440000",
  "name": "主角团队",
  "description": "主角及其伙伴",
  "color": "#3b82f6"
}
```

**响应**:
```json
{
  "id": "group-123",
  "workId": "550e8400-e29b-41d4-a716-446655440000",
  "name": "主角团队",
  "description": "主角及其伙伴",
  "color": "#3b82f6",
  "memberIds": [],
  "createdAt": "2025-10-24T10:00:00Z"
}
```

---

### 13.2 获取分组详情

**接口**: `GET /api/v1/groups/{group_id}`

**描述**: 获取分组详情（包含成员列表）

**响应**:
```json
{
  "id": "group-123",
  "workId": "550e8400-e29b-41d4-a716-446655440000",
  "name": "主角团队",
  "description": "主角及其伙伴",
  "color": "#3b82f6",
  "memberIds": [
    { "entityId": "character-1", "entityType": "character" },
    { "entityId": "character-2", "entityType": "character" }
  ],
  "createdAt": "2025-10-24T10:00:00Z"
}
```

---

### 13.3 获取作品分组列表

**接口**: `GET /api/v1/groups/work/{work_id}`

**描述**: 获取作品的所有分组

**响应**:
```json
{
  "groups": [
    {
      "id": "group-123",
      "name": "主角团队",
      "color": "#3b82f6",
      "memberCount": 5
    },
    {
      "id": "group-456",
      "name": "反派阵营",
      "color": "#ef4444",
      "memberCount": 3
    }
  ],
  "total": 8
}
```

---

### 13.4 更新分组

**接口**: `PUT /api/v1/groups/{group_id}`

**描述**: 更新分组信息

**请求体**: 同创建接口（所有字段可选）

**响应**: 更新后的分组对象

---

### 13.5 删除分组

**接口**: `DELETE /api/v1/groups/{group_id}`

**描述**: 删除分组

**响应**:
```json
{
  "success": true,
  "message": "分组已删除"
}
```

---

### 13.6 添加分组成员（批量）

**接口**: `POST /api/v1/groups/{group_id}/members`

**描述**: 向分组添加成员

**请求体**:
```json
{
  "members": [
    { "entityId": "character-1", "entityType": "character" },
    { "entityId": "character-2", "entityType": "character" },
    { "entityId": "location-1", "entityType": "location" }
  ]
}
```

**响应**:
```json
{
  "success": true,
  "message": "已添加3个成员",
  "group": {
    "id": "group-123",
    "memberCount": 5
  }
}
```

---

### 13.7 移除分组成员

**接口**: `DELETE /api/v1/groups/{group_id}/members/{member_id}`

**描述**: 从分组移除单个成员

**路径参数**:
- `member_id`: 格式为 `{entityType}-{entityId}`，如 `character-123`

**响应**:
```json
{
  "success": true,
  "message": "成员已移除"
}
```

---

### 13.8 批量移除分组成员

**接口**: `POST /api/v1/groups/{group_id}/members/batch-remove`

**描述**: 批量移除分组成员

**请求体**:
```json
{
  "memberIds": [
    "character-1",
    "character-2",
    "location-1"
  ]
}
```

**响应**:
```json
{
  "success": true,
  "message": "已移除3个成员"
}
```

---

## 14. 搜索API

### 14.1 全局搜索

**接口**: `GET /api/v1/search`

**描述**: 跨类型全局搜索（作品、章节、人物、地点、设定）

**查询参数**:
- `q` (必需): 搜索关键词
- `types` (可选): 搜索类型，逗号分隔，如 `work,chapter,character`
- `limit` (可选): 每种类型返回数量，默认10
- `offset` (可选): 偏移量，默认0

**搜索类型**:
- `work`: 作品（标题、简介）
- `chapter`: 章节（标题、内容）
- `character`: 人物（名称、描述）
- `location`: 地点（名称、描述）
- `setting`: 设定（标题、内容）

**请求示例**:
```
GET /api/v1/search?q=修仙&types=work,chapter&limit=5
```

**响应**:
```json
{
  "query": "修仙",
  "results": {
    "works": [
      {
        "id": "work-1",
        "title": "修仙传",
        "type": "work",
        "snippet": "一部经典的<em>修仙</em>小说...",
        "matchFields": ["title"]
      }
    ],
    "chapters": [
      {
        "id": "chapter-1",
        "title": "踏入修仙之路",
        "workId": "work-1",
        "workTitle": "修仙传",
        "type": "chapter",
        "snippet": "主角开始了<em>修仙</em>之旅...",
        "matchFields": ["title", "content"]
      }
    ],
    "characters": [],
    "locations": [],
    "settings": []
  },
  "total": {
    "works": 3,
    "chapters": 15,
    "characters": 0,
    "locations": 0,
    "settings": 0
  }
}
```

**特性**:
- ✅ 模糊匹配（部分匹配）
- ✅ 高亮显示匹配文本（使用 `<em>` 标签）
- ✅ 内容片段提取（前后各50字符）
- ✅ 多字段搜索
- ✅ 分类统计

---

## 15. AI日志API

### 15.1 获取个人AI调用日志

**接口**: `GET /api/v1/ai-logs/me`

**描述**: 获取当前用户的AI调用日志列表

**查询参数**:
- `limit` (可选): 每页数量，默认20
- `offset` (可选): 偏移量，默认0
- `startDate` (可选): 开始日期，格式 `YYYY-MM-DD`
- `endDate` (可选): 结束日期，格式 `YYYY-MM-DD`
- `function` (可选): 筛选功能类型 (`continue`, `polish`, `translate`, `expand`, `summarize`)
- `status` (可选): 筛选状态 (`success`, `error`)

**响应**:
```json
{
  "logs": [
    {
      "id": "log-123",
      "userId": "user-456",
      "function": "continue",
      "model": "gpt-4",
      "promptTokens": 150,
      "completionTokens": 300,
      "totalTokens": 450,
      "estimatedCost": 0.0045,
      "status": "success",
      "createdAt": "2025-10-24T10:00:00Z",
      "executionTime": 2.5
    }
  ],
  "total": 150,
  "limit": 20,
  "offset": 0
}
```

---

### 15.2 获取个人AI统计

**接口**: `GET /api/v1/ai-logs/me/stats`

**描述**: 获取当前用户的AI使用统计

**查询参数**:
- `startDate` (可选): 开始日期
- `endDate` (可选): 结束日期

**响应**:
```json
{
  "totalCalls": 150,
  "totalTokens": 45000,
  "totalCost": 12.50,
  "successRate": 98.5,
  "functionBreakdown": {
    "continue": { "calls": 80, "tokens": 25000, "cost": 7.50 },
    "polish": { "calls": 50, "tokens": 15000, "cost": 3.75 },
    "translate": { "calls": 20, "tokens": 5000, "cost": 1.25 }
  },
  "modelBreakdown": {
    "gpt-4": { "calls": 100, "cost": 10.00 },
    "claude-3.5-sonnet": { "calls": 50, "cost": 2.50 }
  },
  "dailyUsage": [
    { "date": "2025-10-24", "calls": 15, "cost": 1.25 },
    { "date": "2025-10-23", "calls": 20, "cost": 1.80 }
  ]
}
```

---

### 15.3 获取全局AI统计（管理员）

**接口**: `GET /api/v1/ai-logs/admin/stats`

**描述**: 获取全系统的AI使用统计

**权限**: 仅管理员

**查询参数**: 同15.2

**响应**:
```json
{
  "totalCalls": 125000,
  "totalTokens": 5000000,
  "totalCost": 5000.00,
  "successRate": 99.2,
  "totalUsers": 500,
  "activeUsers": 350,
  "functionBreakdown": { ... },
  "modelBreakdown": { ... },
  "dailyUsage": [ ... ],
  "topUsers": [
    { "userId": "user-1", "username": "writer1", "calls": 500, "cost": 50.00 },
    { "userId": "user-2", "username": "writer2", "calls": 450, "cost": 45.00 }
  ]
}
```

---

### 15.4 获取成本指标（管理员）

**接口**: `GET /api/v1/ai-logs/admin/cost-metrics`

**描述**: 获取详细的成本指标

**权限**: 仅管理员

**查询参数**:
- `startDate` (可选)
- `endDate` (可选)
- `groupBy` (可选): 分组方式 (`day`, `week`, `month`)，默认 `day`

**响应**:
```json
{
  "totalCost": 5000.00,
  "avgCostPerCall": 0.04,
  "avgCostPerUser": 10.00,
  "costByModel": {
    "gpt-4": 3500.00,
    "claude-3.5-sonnet": 1200.00,
    "qwen-max": 300.00
  },
  "costByFunction": {
    "continue": 2500.00,
    "polish": 1500.00,
    "translate": 500.00,
    "expand": 400.00,
    "summarize": 100.00
  },
  "costTrend": [
    { "date": "2025-10-24", "cost": 150.00, "calls": 3500 },
    { "date": "2025-10-23", "cost": 180.00, "calls": 4200 }
  ],
  "projectedMonthlyCost": 4500.00
}
```

---

### 15.5 获取用户日志（管理员）

**接口**: `GET /api/v1/ai-logs/admin/user/{user_id}/logs`

**描述**: 获取指定用户的AI调用日志

**权限**: 仅管理员

**查询参数**: 同15.1

**响应**: 同15.1

---

### 15.6 获取用户统计（管理员）

**接口**: `GET /api/v1/ai-logs/admin/user/{user_id}/stats`

**描述**: 获取指定用户的AI使用统计

**权限**: 仅管理员

**查询参数**: 同15.2

**响应**: 同15.2

---

## 16. 导出导入API

### 16.1 导出作品

**接口**: `POST /api/v1/works/{work_id}/export`

**描述**: 导出作品数据

**请求体**:
```json
{
  "format": "json",
  "includeChapters": true,
  "includeWorldview": true,
  "includeGuidelines": true,
  "includeAnalysis": false
}
```

**支持格式**:
- `json`: 完整JSON备份（包含所有数据）
- `markdown`: Markdown文本格式（正文+附录）

**响应**:
```json
{
  "downloadUrl": "/api/v1/downloads/3e22b191-a5b2-4d3c-8f7e-9a1b2c3d4e5f",
  "fileName": "我的小说_20251024.json",
  "fileSize": 2457600,
  "expiresAt": "2025-10-25T10:00:00Z"
}
```

---

### 16.2 下载文件

**接口**: `GET /api/v1/downloads/{file_id}`

**描述**: 下载导出的临时文件

**响应**: 文件流（自动触发浏览器下载）

**特性**:
- ✅ 临时文件24小时后自动清理
- ✅ 原始文件名保留
- ✅ 支持断点续传

---

### 16.3 删除临时文件

**接口**: `DELETE /api/v1/downloads/{file_id}`

**描述**: 手动删除临时文件

**响应**:
```json
{
  "success": true,
  "message": "文件已删除"
}
```

---

### 16.4 预览导入

**接口**: `POST /api/v1/works/import/preview`

**描述**: 预览导入数据（不实际导入）

**请求体**: `multipart/form-data`
- `file`: 文件（JSON/TXT/Markdown）
- `format`: 文件格式 (`json`, `txt`, `markdown`)

**响应**:
```json
{
  "work": {
    "title": "我的小说",
    "totalWords": 50000,
    "totalChapters": 10
  },
  "chapters": [
    { "title": "第一章 开端", "wordCount": 5000, "order": 1 },
    { "title": "第二章 修炼", "wordCount": 4800, "order": 2 }
  ],
  "charactersCount": 5,
  "locationsCount": 3,
  "settingsCount": 2,
  "warnings": [
    "检测到重复章节标题：第三章"
  ]
}
```

---

### 16.5 导入作品

**接口**: `POST /api/v1/works/import`

**描述**: 导入作品数据

**请求体**: `multipart/form-data`
- `file`: 文件（JSON/TXT/Markdown）
- `format`: 文件格式
- `includeChapters`: 是否导入章节（默认true）
- `includeWorldview`: 是否导入世界观（默认true）
- `includeGuidelines`: 是否导入规范（默认true）

**响应**:
```json
{
  "success": true,
  "workId": "work-123",
  "title": "我的小说",
  "stats": {
    "chaptersCreated": 10,
    "charactersCreated": 5,
    "locationsCreated": 3,
    "settingsCreated": 2
  }
}
```

**特性**:
- ✅ 智能章节分割（TXT/Markdown）
- ✅ 选择性导入
- ✅ 导入前预览
- ✅ 数据验证

---

## 17. AI改写助手API ⭐⭐

> **核心功能**: 多模型并发改写对比 - 同时调用4-6个顶级AI模型,对比选择最佳结果
>
> **差异化优势**: 市场少见的多模型并发功能,大幅提升用户满意度
>
> **别名**: AI写作竞技场 (同一功能的不同称呼)

### 17.1 获取可用模型列表

**接口**: `GET /api/v1/ai/rewrite-arena/models`

**描述**: 获取改写助手支持的AI模型列表及其配置信息

**请求头**:
```http
Authorization: Bearer <access_token>
```

**响应** (200 OK):
```json
{
  "models": [
    {
      "id": "gemini-2.5-pro",
      "name": "Gemini 2.5 Pro",
      "description": "擅长创意和细节描写",
      "enabled": true
    },
    {
      "id": "gpt-5",
      "name": "GPT-5",
      "description": "平衡全能，表现稳定",
      "enabled": true
    },
    {
      "id": "claude-3-5-sonnet",
      "name": "Claude 3.5 Sonnet",
      "description": "逻辑性强，适合情节构思",
      "enabled": true
    },
    {
      "id": "qwen-max",
      "name": "通义千问Max",
      "description": "中文理解优秀",
      "enabled": true
    }
  ],
  "default_models": ["gemini-2.5-pro", "gpt-5", "claude-3-5-sonnet"],
  "max_models": 6
}
```

**特性**:
- ✅ 返回所有可用模型
- ✅ 包含模型特点说明
- ✅ 支持动态启用/禁用

---

### 17.2 智能分析文本

**接口**: `POST /api/v1/ai/rewrite-arena/analyze`

**描述**: AI自动分析文本质量,检测问题,给出改写建议

**请求头**:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求体**:
```json
{
  "text": "待分析的文本内容...",
  "context_before": "前文上下文 (可选)",
  "context_after": "后文上下文 (可选)"
}
```

**响应** (200 OK):
```json
{
  "analysis": {
    "ai_trace_score": 75,
    "issues": [
      {
        "type": "repetition",
        "description": "检测到重复使用'然而'连接词",
        "severity": "medium"
      },
      {
        "type": "logic",
        "description": "情节转折略显生硬",
        "severity": "low"
      }
    ],
    "suggestions": [
      "建议增加感官描写,让场景更生动",
      "可以调整句子长度,避免过于整齐",
      "部分对话可以更加口语化"
    ],
    "overall_quality": 7.5
  }
}
```

**特性**:
- ✅ AI痕迹检测 (0-100分)
- ✅ 问题诊断 (重复/逻辑/风格)
- ✅ 具体改写建议
- ✅ 整体质量评分

---

### 17.3 多模型并发改写 ⭐⭐ 核心功能

**接口**: `POST /api/v1/ai/rewrite-arena/rewrite`

**描述**: 同时调用多个AI模型改写文本,返回对比结果

**请求头**:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求体**:
```json
{
  "text": "待改写的原文...",
  "models": ["gemini-2.5-pro", "gpt-5", "claude-3-5-sonnet"],
  "mode": "improve",
  "custom_requirement": "增加感官描写,保持原意 (可选)",
  "context_before": "前文上下文 (可选)",
  "context_after": "后文上下文 (可选)"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 原文 (50-2000字) |
| models | array | 是 | 模型列表 (最多6个) |
| mode | string | 是 | 改写模式: improve/expand/polish/creative |
| custom_requirement | string | 否 | 自定义要求 |
| context_before | string | 否 | 前文 (最多1000字) |
| context_after | string | 否 | 后文 (最多1000字) |

**响应** (200 OK):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "results": [
    {
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "改写后的文本内容...",
      "word_count": 456,
      "elapsed_time": 2.3,
      "status": "success"
    },
    {
      "model_name": "gpt-5",
      "rewritten_text": "改写后的文本内容...",
      "word_count": 432,
      "elapsed_time": 1.8,
      "status": "success"
    },
    {
      "model_name": "claude-3-5-sonnet",
      "rewritten_text": "改写后的文本内容...",
      "word_count": 489,
      "elapsed_time": 2.1,
      "status": "success"
    }
  ],
  "total_models": 3,
  "successful": 3,
  "failed": 0
}
```

**特性**:
- ✅ 并发调用,节省时间
- ✅ 智能上下文分级 (根据文本长度自动调整)
- ✅ 失败容错 (部分模型失败不影响其他)
- ✅ 实时进度反馈
- ✅ 自动保存会话

**改写模式说明**:
- `improve`: 提升质量,保持长度
- `expand`: 扩写3-5倍,增加细节
- `polish`: 润色优化,文学性提升
- `creative`: 创意改写,风格变化

---

### 17.4 保存改写记录

**接口**: `POST /api/v1/rewrite-history`

**描述**: 保存改写会话到历史记录

**请求头**:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求体**:
```json
{
  "original_text": "原文",
  "context_before": "前文 (可选)",
  "context_after": "后文 (可选)",
  "mode": "improve",
  "custom_requirement": "自定义要求 (可选)",
  "results": [
    {
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "改写文本",
      "word_count": 456,
      "elapsed_time": 2.3,
      "is_selected": true
    }
  ]
}
```

**响应** (201 Created):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-10-26T15:30:00Z"
}
```

---

### 17.5 获取改写历史列表

**接口**: `GET /api/v1/rewrite-history`

**描述**: 分页查询用户的改写历史记录

**请求头**:
```http
Authorization: Bearer <access_token>
```

**Query参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码 (默认1) |
| page_size | int | 否 | 每页数量 (默认20,最大100) |
| mode | string | 否 | 筛选模式 |

**响应** (200 OK):
```json
{
  "total": 45,
  "page": 1,
  "page_size": 20,
  "sessions": [
    {
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "mode": "improve",
      "original_text_preview": "原文前100字...",
      "models_count": 3,
      "selected_model": "gemini-2.5-pro",
      "created_at": "2025-10-26T15:30:00Z"
    }
  ]
}
```

**特性**:
- ✅ 分页查询
- ✅ 模式筛选
- ✅ 原文预览
- ✅ 按时间倒序

---

### 17.6 获取改写会话详情

**接口**: `GET /api/v1/rewrite-history/{session_id}`

**描述**: 获取指定会话的完整信息

**请求头**:
```http
Authorization: Bearer <access_token>
```

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| session_id | UUID | 会话ID |

**响应** (200 OK):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "original_text": "完整原文...",
  "context_before": "前文",
  "context_after": "后文",
  "mode": "improve",
  "custom_requirement": "自定义要求",
  "results": [
    {
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "完整改写文本...",
      "word_count": 456,
      "elapsed_time": 2.3,
      "is_selected": true
    }
  ],
  "created_at": "2025-10-26T15:30:00Z"
}
```

**特性**:
- ✅ 完整会话数据
- ✅ 所有模型结果
- ✅ 用户选择标记

---

### 17.7 删除改写记录

**接口**: `DELETE /api/v1/rewrite-history/{session_id}`

**描述**: 删除指定的改写会话

**请求头**:
```http
Authorization: Bearer <access_token>
```

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| session_id | UUID | 会话ID |

**响应** (204 No Content):
无响应体

**错误响应** (404 Not Found):
```json
{
  "detail": "改写会话不存在"
}
```

**特性**:
- ✅ 软删除机制
- ✅ 权限校验 (只能删除自己的记录)

---

### 💡 使用场景示例

#### 场景1: 快速多模型对比
```javascript
// 1. 选择3个模型进行对比
const response = await fetch('/api/v1/ai/rewrite-arena/rewrite', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: "他走进了房间，心情很复杂。",
    models: ["gemini-2.5-pro", "gpt-5", "claude-3-5-sonnet"],
    mode: "expand"
  })
});

// 2. 获取3个模型的改写结果
const { session_id, results } = await response.json();

// 3. 用户选择最满意的版本
// 4. 保存历史记录 (自动保存,无需手动调用)
```

#### 场景2: 带上下文的智能改写
```javascript
const response = await fetch('/api/v1/ai/rewrite-arena/rewrite', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: "他打开了门。",
    models: ["gemini-2.5-pro", "gpt-5"],
    mode: "expand",
    custom_requirement: "增加五感描写，营造紧张氛围",
    context_before: "夜色如墨，四周一片死寂...",
    context_after: "门后传来了诡异的声音..."
  })
});
```

### 📊 技术特性

**智能上下文分级**:
- 文本 < 200字: 提供完整前后文 (各500字)
- 文本 200-500字: 提供部分前后文 (各300字)
- 文本 > 500字: 只提供关键前后文 (各100字)

**并发性能**:
- 6个模型并发: ~3-5秒完成
- 失败容错: 部分失败不影响其他模型
- 超时设置: 单模型最长30秒

**成本优化**:
- 智能缓存: 相同内容24小时内不重复调用
- 按需加载: 用户主动触发,不自动调用
- 成本统计: 记录到 `ai_call_logs` 表

---

## 18. 错误代码

### HTTP状态码

| 状态码 | 说明 | 示例 |
|--------|------|------|
| 200 | 请求成功 | GET /works |
| 201 | 创建成功 | POST /works |
| 204 | 删除成功 | DELETE /works/{id} |
| 400 | 请求参数错误 | 缺少必需字段 |
| 401 | 未授权 | Token无效或过期 |
| 403 | 禁止访问 | 非管理员访问管理接口 |
| 404 | 资源不存在 | 作品ID不存在 |
| 422 | 验证失败 | 字段类型不匹配 |
| 500 | 服务器错误 | 数据库连接失败 |

### 错误响应格式

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": [
      {
        "field": "email",
        "message": "邮箱格式不正确"
      }
    ]
  }
}
```

### 常见错误代码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `AUTH_FAILED` | 认证失败 | 检查Token是否有效 |
| `PERMISSION_DENIED` | 权限不足 | 需要管理员权限 |
| `RESOURCE_NOT_FOUND` | 资源不存在 | 检查资源ID是否正确 |
| `VALIDATION_ERROR` | 验证失败 | 检查请求参数 |
| `DUPLICATE_ENTRY` | 数据重复 | 用户名或邮箱已存在 |
| `TOKEN_EXPIRED` | Token过期 | 使用刷新Token获取新Token |

---

## 19. 相关链接

- **上一章**: [前端开发规范](./06-frontend-specs.md)
- **下一章**: [部署运维指南](./08-deployment.md)
- **返回**: [文档导航](./README.md)

---

**文档版本**: v2.13
**最后更新**: 2025-10-24
**维护者**: NovelAIde开发团队
