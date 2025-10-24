# API 参考文档

> **NovelAIde API 参考文档**
> 版本: v2.13
> 最后更新: 2025-10-24

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
- [9. 小说分析API](#9-小说分析api)
- [10. 管理后台API](#10-管理后台api)
- [11. 时间线API](#11-时间线api)
- [12. 关系管理API](#12-关系管理api)
- [13. 分组管理API](#13-分组管理api)
- [14. 搜索API](#14-搜索api)
- [15. AI日志API](#15-ai日志api)
- [16. 导出导入API](#16-导出导入api)
- [17. 错误代码](#17-错误代码)
- [18. 相关链接](#18-相关链接)

---

## 1. 概述

NovelAIde API 提供完整的RESTful接口，支持小说创作的全流程功能，包括：

- **用户认证**：注册、登录、Token管理
- **作品管理**：作品CRUD、章节管理、统计数据
- **世界观构建**：角色、地点、设定、关系管理
- **AI辅助**：续写、润色、翻译、扩写、总结
- **小说分析**：微观分析、宏观分析、章节概括
- **管理后台**：用户管理、统计数据、系统配置

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

**响应**:
```json
{
  "suggestion": "一个陌生的男子站在门外，手里拿着一封信"
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

## 17. 错误代码

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

## 18. 相关链接

- **上一章**: [前端开发规范](./06-frontend-specs.md)
- **下一章**: [部署运维指南](./08-deployment.md)
- **返回**: [文档导航](./README.md)

---

**文档版本**: v2.13
**最后更新**: 2025-10-24
**维护者**: NovelAIde开发团队
