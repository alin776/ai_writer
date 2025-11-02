# NovelAIde API 接口文档

> **给前端开发者**：这是完整的后端 API 接口文档，包含所有接口的详细说明、请求参数和响应格式。

## 📋 目录

- [基础信息](#基础信息)
- [认证流程](#认证流程)
- [认证接口](#认证接口)
- [用户接口](#用户接口)
- [作品接口](#作品接口)
- [章节接口](#章节接口)
- [AI 改写助手接口](#ai-改写助手接口) ⭐️ **NEW**
- [改写历史接口](#改写历史接口) ⭐️ **NEW**
- [数据模型](#数据模型)
- [错误码说明](#错误码说明)

---

## 基础信息

### 服务地址

- **开发环境**: http://localhost:8000
- **API 基础路径**: `/api/v1`
- **完整示例**: http://localhost:8000/api/v1/auth/login

### 在线文档

- **Swagger UI**: http://localhost:8000/docs （推荐，可在线测试）
- **ReDoc**: http://localhost:8000/redoc

### 通用请求头

```http
Content-Type: application/json
Authorization: Bearer {access_token}  # 需要认证的接口
```

### 通用响应格式

成功响应：
```json
{
  "data": {...},
  "message": "success"
}
```

错误响应：
```json
{
  "detail": "错误信息"
}
```

---

## 认证流程

### 流程图

```
注册 → 登录 → 获取Token → 使用Token访问接口 → Token过期 → 刷新Token
```

### Token 使用

1. 登录后获得 `access_token` 和 `refresh_token`
2. 在请求头中添加：`Authorization: Bearer {access_token}`
3. `access_token` 有效期：60分钟
4. `refresh_token` 有效期：7天
5. Token 过期后使用 `refresh_token` 刷新

---

## 认证接口

### 1. 用户注册

**POST** `/api/v1/auth/register`

注册新用户账号。

**请求参数**：

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名，3-50字符 |
| email | string | 是 | 邮箱地址 |
| password | string | 是 | 密码，至少6字符 |

**响应示例**：

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "testuser",
  "email": "test@example.com",
  "full_name": null,
  "avatar": null,
  "bio": null,
  "is_active": true,
  "is_admin": false,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login_at": null
}
```

**状态码**：
- `201`: 创建成功
- `400`: 参数错误
- `409`: 用户名或邮箱已存在

---

### 2. 用户登录

**POST** `/api/v1/auth/login`

用户登录获取 Token。

**请求参数**（Form Data）：

```
username: testuser
password: password123
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名或邮箱 |
| password | string | 是 | 密码 |

**响应示例**：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**状态码**：
- `200`: 登录成功
- `401`: 用户名或密码错误
- `403`: 账号已被禁用

**使用示例**：

```javascript
// JavaScript fetch 示例
const response = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    username: 'testuser',
    password: 'password123'
  })
});

const data = await response.json();
localStorage.setItem('access_token', data.access_token);
localStorage.setItem('refresh_token', data.refresh_token);
```

---

### 3. 刷新 Token

**POST** `/api/v1/auth/refresh`

使用 refresh_token 获取新的 access_token。

**请求参数**：

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应示例**：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**状态码**：
- `200`: 刷新成功
- `401`: Token 无效或已过期

---

## 用户接口

### 4. 获取当前用户信息

**GET** `/api/v1/users/me`

获取当前登录用户的详细信息。

**请求头**：

```
Authorization: Bearer {access_token}
```

**响应示例**：

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "张三",
  "avatar": "https://example.com/avatar.jpg",
  "bio": "我是一个小说作者",
  "is_active": true,
  "is_admin": false,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login_at": "2024-01-01T12:00:00"
}
```

**状态码**：
- `200`: 成功
- `401`: 未登录或 Token 无效

---

### 5. 更新当前用户信息

**PUT** `/api/v1/users/me`

更新当前用户的个人信息。

**请求头**：

```
Authorization: Bearer {access_token}
```

**请求参数**（所有字段可选）：

```json
{
  "username": "newusername",
  "email": "newemail@example.com",
  "full_name": "李四",
  "avatar": "https://example.com/new-avatar.jpg",
  "bio": "更新后的个人简介"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 否 | 用户名，3-50字符 |
| email | string | 否 | 邮箱地址 |
| full_name | string | 否 | 真实姓名，最多100字符 |
| avatar | string | 否 | 头像URL |
| bio | string | 否 | 个人简介 |

**响应示例**：同"获取当前用户信息"

**状态码**：
- `200`: 更新成功
- `400`: 参数错误
- `401`: 未登录

---

### 6. 获取指定用户信息

**GET** `/api/v1/users/{user_id}`

根据用户ID获取用户信息。

**请求头**：

```
Authorization: Bearer {access_token}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | string | 用户ID（UUID） |

**响应示例**：同"获取当前用户信息"

**状态码**：
- `200`: 成功
- `404`: 用户不存在
- `401`: 未登录

---

### 7. 获取用户列表

**GET** `/api/v1/users`

获取用户列表（分页、搜索）。

**请求头**：

```
Authorization: Bearer {access_token}
```

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| skip | int | 否 | 0 | 跳过的记录数 |
| limit | int | 否 | 100 | 返回的最大记录数 |
| search | string | 否 | null | 搜索关键词（用户名或邮箱） |

**请求示例**：

```
GET /api/v1/users?skip=0&limit=20&search=test
```

**响应示例**：

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "张三",
    "avatar": "https://example.com/avatar.jpg",
    "bio": "我是一个小说作者",
    "is_active": true,
    "is_admin": false,
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "last_login_at": "2024-01-01T12:00:00"
  }
]
```

**状态码**：
- `200`: 成功
- `401`: 未登录

---

## 作品接口

### 8. 获取作品列表

**GET** `/api/v1/works`

获取作品列表（当前用户的作品或指定作者的作品）。

**请求头**：

```
Authorization: Bearer {access_token}
```

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| skip | int | 否 | 0 | 跳过的记录数 |
| limit | int | 否 | 20 | 每页数量（1-100） |
| search | string | 否 | null | 搜索关键词（标题） |
| author_id | string | 否 | 当前用户ID | 作者ID |

**请求示例**：

```
GET /api/v1/works?skip=0&limit=20&search=玄幻
```

**响应示例**：

```json
{
  "total": 10,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174001",
      "author_id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "我的第一部小说",
      "description": "这是一个关于冒险的故事",
      "genre": "FANTASY",
      "status": "DRAFT",
      "cover_image": "https://example.com/cover.jpg",
      "total_words": 50000,
      "total_chapters": 10,
      "view_count": 100,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-02T00:00:00",
      "published_at": null
    }
  ]
}
```

**状态码**：
- `200`: 成功
- `401`: 未登录

---

### 9. 获取作品详情

**GET** `/api/v1/works/{work_id}`

获取指定作品的详细信息。

**请求头**：

```
Authorization: Bearer {access_token}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| work_id | string | 作品ID（UUID） |

**响应示例**：

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174001",
  "author_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "我的第一部小说",
  "description": "这是一个关于冒险的故事",
  "genre": "FANTASY",
  "status": "DRAFT",
  "cover_image": "https://example.com/cover.jpg",
  "total_words": 50000,
  "total_chapters": 10,
  "view_count": 100,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-02T00:00:00",
  "published_at": null
}
```

**状态码**：
- `200`: 成功
- `404`: 作品不存在
- `403`: 无权访问（只能访问自己的作品）
- `401`: 未登录

---

### 10. 创建作品

**POST** `/api/v1/works`

创建新的作品。

**请求头**：

```
Authorization: Bearer {access_token}
```

**请求参数**：

```json
{
  "title": "我的新小说",
  "description": "这是一个精彩的故事",
  "genre": "FANTASY",
  "status": "DRAFT",
  "cover_image": "https://example.com/cover.jpg"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 作品标题，1-200字符 |
| description | string | 否 | 作品简介 |
| genre | string | 否 | 作品类型（见下方枚举） |
| status | string | 否 | 作品状态（见下方枚举） |
| cover_image | string | 否 | 封面图片URL |

**作品类型（genre）枚举**：
- `FANTASY`: 玄幻
- `URBAN`: 都市
- `ROMANCE`: 言情
- `SCIFI`: 科幻
- `WUXIA`: 武侠
- `HISTORY`: 历史
- `GAME`: 游戏
- `OTHER`: 其他

**作品状态（status）枚举**：
- `DRAFT`: 草稿
- `SERIALIZING`: 连载中
- `COMPLETED`: 已完结
- `PAUSED`: 暂停更新

**响应示例**：同"获取作品详情"

**状态码**：
- `201`: 创建成功
- `400`: 参数错误
- `401`: 未登录

---

### 11. 更新作品

**PUT** `/api/v1/works/{work_id}`

更新作品信息。

**请求头**：

```
Authorization: Bearer {access_token}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| work_id | string | 作品ID（UUID） |

**请求参数**（所有字段可选）：

```json
{
  "title": "更新后的标题",
  "description": "更新后的简介",
  "genre": "SCIFI",
  "status": "SERIALIZING",
  "cover_image": "https://example.com/new-cover.jpg"
}
```

**响应示例**：同"获取作品详情"

**状态码**：
- `200`: 更新成功
- `404`: 作品不存在
- `403`: 无权操作（只能修改自己的作品）
- `401`: 未登录

---

### 12. 删除作品

**DELETE** `/api/v1/works/{work_id}`

删除作品（会同时删除所有章节）。

**请求头**：

```
Authorization: Bearer {access_token}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| work_id | string | 作品ID（UUID） |

**响应**：无内容

**状态码**：
- `204`: 删除成功
- `404`: 作品不存在
- `403`: 无权操作（只能删除自己的作品）
- `401`: 未登录

---

## 章节接口

### 13. 获取作品的章节列表

**GET** `/api/v1/chapters/work/{work_id}`

获取指定作品的所有章节。

**请求头**：

```
Authorization: Bearer {access_token}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| work_id | string | 作品ID（UUID） |

**响应示例**：

```json
{
  "total": 10,
  "items": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174002",
      "work_id": "123e4567-e89b-12d3-a456-426614174001",
      "title": "第一章 初入江湖",
      "content": "这是章节内容...",
      "order": 1,
      "is_published": true,
      "word_count": 5000,
      "view_count": 50,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "published_at": "2024-01-01T00:00:00"
    }
  ]
}
```

**状态码**：
- `200`: 成功
- `404`: 作品不存在
- `403`: 无权访问
- `401`: 未登录

---

### 14. 获取章节详情

**GET** `/api/v1/chapters/{chapter_id}`

获取指定章节的详细信息。

**请求头**：

```
Authorization: Bearer {access_token}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| chapter_id | string | 章节ID（UUID） |

**响应示例**：

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174002",
  "work_id": "123e4567-e89b-12d3-a456-426614174001",
  "title": "第一章 初入江湖",
  "content": "这是章节内容...",
  "order": 1,
  "is_published": true,
  "word_count": 5000,
  "view_count": 50,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "published_at": "2024-01-01T00:00:00"
}
```

**状态码**：
- `200`: 成功
- `404`: 章节不存在
- `403`: 无权访问
- `401`: 未登录

---

### 15. 创建章节

**POST** `/api/v1/chapters`

为指定作品创建新章节。

**请求头**：

```
Authorization: Bearer {access_token}
```

**请求参数**：

```json
{
  "work_id": "123e4567-e89b-12d3-a456-426614174001",
  "title": "第二章 风云再起",
  "content": "章节内容...",
  "order": 2
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| work_id | string | 是 | 作品ID（UUID） |
| title | string | 是 | 章节标题，1-200字符 |
| content | string | 是 | 章节内容 |
| order | int | 否 | 章节排序（不填自动排到最后） |

**响应示例**：同"获取章节详情"

**状态码**：
- `201`: 创建成功
- `404`: 作品不存在
- `403`: 无权操作
- `401`: 未登录

**注意**：创建章节后会自动更新作品的章节数和总字数。

---

### 16. 更新章节

**PUT** `/api/v1/chapters/{chapter_id}`

更新章节信息。

**请求头**：

```
Authorization: Bearer {access_token}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| chapter_id | string | 章节ID（UUID） |

**请求参数**（所有字段可选）：

```json
{
  "title": "更新后的标题",
  "content": "更新后的内容",
  "order": 3,
  "is_published": true
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 章节标题 |
| content | string | 否 | 章节内容 |
| order | int | 否 | 章节排序 |
| is_published | bool | 否 | 是否发布 |

**响应示例**：同"获取章节详情"

**状态码**：
- `200`: 更新成功
- `404`: 章节不存在
- `403`: 无权操作
- `401`: 未登录

---

### 17. 删除章节

**DELETE** `/api/v1/chapters/{chapter_id}`

删除章节。

**请求头**：

```
Authorization: Bearer {access_token}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| chapter_id | string | 章节ID（UUID） |

**响应**：无内容

**状态码**：
- `204`: 删除成功
- `404`: 章节不存在
- `403`: 无权操作
- `401`: 未登录

**注意**：删除章节后会自动更新作品的章节数和总字数。

---

## AI 改写助手接口

> **新功能** 🎉 AI 改写助手可以帮助作者智能分析文本质量，并使用多个 AI 模型同时改写文本，提供多样化选择。

### 19. 获取可用模型列表

**GET** `/api/v1/ai/rewrite-arena/models`

获取所有支持改写功能的 AI 模型列表。

**请求头**：

```
Authorization: Bearer {access_token}
```

**响应示例**：

```json
{
  "models": [
    {
      "id": "gemini-2.5-pro",
      "name": "Gemini 2.5 Pro",
      "provider": "google",
      "description": "擅长创意写作和细节描写，适合扩写和优化",
      "enabled": true
    },
    {
      "id": "gpt-5",
      "name": "GPT-5",
      "provider": "openai",
      "description": "平衡全能，适合各种改写需求",
      "enabled": true
    }
  ],
  "default_models": ["gemini-2.5-pro", "gpt-5"],
  "max_models": 4
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| models | array | 模型列表 |
| models[].id | string | 模型ID |
| models[].name | string | 模型显示名称 |
| models[].provider | string | 提供商 |
| models[].description | string | 模型特点说明 |
| models[].enabled | boolean | 是否启用 |
| default_models | array | 默认使用的模型ID列表 |
| max_models | int | 最多同时使用的模型数 |

**状态码**：
- `200`: 成功
- `401`: 未登录

---

### 20. 智能分析文本

**POST** `/api/v1/ai/rewrite-arena/analyze`

使用 AI 智能分析文本质量，检测问题并给出改写建议。

**请求头**：

```
Authorization: Bearer {access_token}
```

**请求参数**：

```json
{
  "text": "主角走进房间，看到了桌子上的剑。",
  "context_before": "经过三天的跋涉，主角终于来到了目的地...",
  "context_after": "他拿起剑，走出了房间..."
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 要分析的文本（10-5000字） |
| context_before | string | 否 | 前文上下文 |
| context_after | string | 否 | 后文上下文 |

**响应示例**：

```json
{
  "quality_score": 45,
  "issues": [
    {
      "type": "lack_of_detail",
      "severity": "high",
      "description": "描写过于简单，缺少细节"
    },
    {
      "type": "weak_emotion",
      "severity": "medium",
      "description": "缺少情感渲染"
    }
  ],
  "suggested_mode": "expand",
  "reason": "建议增加细节描写和情感渲染，使画面更生动",
  "available_modes": [
    {
      "id": "optimize",
      "name": "优化提升",
      "description": "让文字更优美、更生动、更有感染力"
    },
    {
      "id": "expand",
      "name": "扩写丰富",
      "description": "增加细节描写和情感渲染"
    },
    {
      "id": "compress",
      "name": "精简压缩",
      "description": "保留核心信息，删除冗余"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| quality_score | int | 质量评分 (0-100) |
| issues | array | 检测到的问题列表 |
| issues[].type | string | 问题类型 |
| issues[].severity | string | 严重程度：high/medium/low |
| issues[].description | string | 问题描述 |
| suggested_mode | string | 推荐的改写模式 |
| reason | string | 推荐理由 |
| available_modes | array | 所有可用的改写模式 |

**状态码**：
- `200`: 分析成功
- `400`: 参数错误（文本过长或过短）
- `401`: 未登录
- `500`: AI 服务异常

**性能**：通常 0.5-2 秒完成分析

---

### 21. 多模型改写文本

**POST** `/api/v1/ai/rewrite-arena/rewrite`

使用多个 AI 模型同时改写文本，返回所有模型的改写结果。

**请求头**：

```
Authorization: Bearer {access_token}
```

**请求参数**：

```json
{
  "text": "主角走进房间，看到了桌子上的剑。",
  "mode": "expand",
  "context_before": "经过三天的跋涉，主角终于来到了目的地...",
  "context_after": "他拿起剑，走出了房间...",
  "custom_requirement": null,
  "model_ids": ["gemini-2.5-pro", "gpt-5"]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 要改写的文本（10-5000字） |
| mode | string | 是 | 改写模式：optimize/expand/compress/custom |
| context_before | string | 否 | 前文上下文 |
| context_after | string | 否 | 后文上下文 |
| custom_requirement | string | 否 | 自定义要求（当 mode=custom 时必填） |
| model_ids | array | 否 | 指定使用的模型ID（默认使用全部启用的模型） |

**响应示例**：

```json
{
  "results": [
    {
      "model_id": "gemini-2.5-pro",
      "model_name": "Gemini 2.5 Pro",
      "rewritten_text": "主角推开那扇厚重的木门，缓缓走进了这间房间。昏暗的光线中，唯有桌上那柄长剑泛着幽冷的寒光，吸引着他的目光...",
      "word_count": 156,
      "elapsed_time": 2.3,
      "success": true,
      "error": null
    },
    {
      "model_id": "gpt-5",
      "model_name": "GPT-5",
      "rewritten_text": "房门在主角的推动下缓缓打开，他迈步走了进去。视线立刻被桌上那柄寒光闪烁的长剑锁定...",
      "word_count": 142,
      "elapsed_time": 1.8,
      "success": true,
      "error": null
    }
  ],
  "original_word_count": 15,
  "mode": "expand"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| results | array | 所有模型的改写结果 |
| results[].model_id | string | 模型ID |
| results[].model_name | string | 模型名称 |
| results[].rewritten_text | string | 改写后的文本 |
| results[].word_count | int | 改写后的字数 |
| results[].elapsed_time | float | 耗时（秒） |
| results[].success | boolean | 是否成功 |
| results[].error | string | 错误信息（失败时） |
| original_word_count | int | 原文字数 |
| mode | string | 使用的改写模式 |

**状态码**：
- `200`: 改写成功（即使部分模型失败也返回 200）
- `400`: 参数错误
- `401`: 未登录
- `500`: 所有模型都失败

**性能**：
- 单模型：1-3 秒
- 双模型并发：2-4 秒
- 超时时间：30 秒

**注意**：
- 使用 `asyncio.gather()` 并发调用，提升性能
- 即使部分模型失败，也会返回成功模型的结果
- 可以通过 `success` 字段判断每个模型是否成功

---

## 改写历史接口

> 保存和管理改写历史记录，支持分页查询和详情查看。

### 22. 保存改写记录

**POST** `/api/v1/rewrite-history/sessions`

保存一次改写会话及其所有模型的改写结果。

**请求头**：

```
Authorization: Bearer {access_token}
```

**请求参数**：

```json
{
  "original_text": "主角走进房间，看到了桌子上的剑。",
  "context_before": "经过三天的跋涉...",
  "context_after": "他拿起剑...",
  "mode": "expand",
  "custom_requirement": null,
  "results": [
    {
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "主角推开那扇厚重的木门...",
      "word_count": 156,
      "elapsed_time": 2.3,
      "error": null,
      "is_selected": true
    },
    {
      "model_name": "gpt-5",
      "rewritten_text": "房门在主角的推动下...",
      "word_count": 142,
      "elapsed_time": 1.8,
      "error": null,
      "is_selected": false
    }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| original_text | string | 是 | 原文 |
| context_before | string | 否 | 前文上下文 |
| context_after | string | 否 | 后文上下文 |
| mode | string | 是 | 改写模式 |
| custom_requirement | string | 否 | 自定义要求 |
| results | array | 是 | 改写结果列表 |
| results[].model_name | string | 是 | 模型名称 |
| results[].rewritten_text | string | 是 | 改写文本 |
| results[].word_count | int | 是 | 字数 |
| results[].elapsed_time | float | 是 | 耗时（秒） |
| results[].error | string | 否 | 错误信息 |
| results[].is_selected | boolean | 否 | 是否被用户选中（默认 false） |

**响应示例**：

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174003",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "original_text": "主角走进房间，看到了桌子上的剑。",
  "context_before": "经过三天的跋涉...",
  "context_after": "他拿起剑...",
  "mode": "expand",
  "custom_requirement": null,
  "created_at": "2024-01-01T12:00:00",
  "results": [
    {
      "id": "result-id-1",
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "主角推开那扇厚重的木门...",
      "word_count": 156,
      "elapsed_time": 2.3,
      "error": null,
      "is_selected": true,
      "created_at": "2024-01-01T12:00:00"
    },
    {
      "id": "result-id-2",
      "model_name": "gpt-5",
      "rewritten_text": "房门在主角的推动下...",
      "word_count": 142,
      "elapsed_time": 1.8,
      "error": null,
      "is_selected": false,
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

**状态码**：
- `200`: 保存成功
- `400`: 参数错误
- `401`: 未登录
- `500`: 保存失败

---

### 23. 获取改写历史列表

**GET** `/api/v1/rewrite-history/sessions`

获取当前用户的改写历史记录列表（分页）。

**请求头**：

```
Authorization: Bearer {access_token}
```

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码（从1开始） |
| page_size | int | 否 | 20 | 每页数量（1-100） |

**请求示例**：

```
GET /api/v1/rewrite-history/sessions?page=1&page_size=20
```

**响应示例**：

```json
{
  "sessions": [
    {
      "id": "session-id-1",
      "original_text": "主角走进房间，看到了桌子上的剑。（原文如果超过100字会被截断...）",
      "mode": "expand",
      "result_count": 2,
      "created_at": "2024-01-01T12:00:00"
    },
    {
      "id": "session-id-2",
      "original_text": "另一段文本...",
      "mode": "optimize",
      "result_count": 3,
      "created_at": "2024-01-01T11:00:00"
    }
  ],
  "total": 25,
  "page": 1,
  "page_size": 20
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| sessions | array | 会话列表 |
| sessions[].id | string | 会话ID |
| sessions[].original_text | string | 原文（最多100字，超出截断） |
| sessions[].mode | string | 改写模式 |
| sessions[].result_count | int | 结果数量 |
| sessions[].created_at | string | 创建时间 |
| total | int | 总记录数 |
| page | int | 当前页码 |
| page_size | int | 每页数量 |

**状态码**：
- `200`: 成功
- `401`: 未登录
- `500`: 查询失败

**性能优化**：使用子查询避免 N+1 查询问题

---

### 24. 获取改写会话详情

**GET** `/api/v1/rewrite-history/sessions/{session_id}`

获取指定改写会话的完整详情，包括所有模型的改写结果。

**请求头**：

```
Authorization: Bearer {access_token}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| session_id | string | 会话ID（UUID） |

**响应示例**：同"保存改写记录"的响应格式

**状态码**：
- `200`: 成功
- `404`: 会话不存在
- `403`: 无权访问（只能访问自己的会话）
- `401`: 未登录

---

### 25. 删除改写会话

**DELETE** `/api/v1/rewrite-history/sessions/{session_id}`

删除指定的改写会话及其所有结果（级联删除）。

**请求头**：

```
Authorization: Bearer {access_token}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| session_id | string | 会话ID（UUID） |

**响应示例**：

```json
{
  "detail": "删除成功"
}
```

**状态码**：
- `200`: 删除成功
- `404`: 会话不存在
- `403`: 无权操作（只能删除自己的会话）
- `401`: 未登录

---

### 18. 重新排序章节

**POST** `/api/v1/chapters/reorder`

重新排列作品的章节顺序。

**请求头**：

```
Authorization: Bearer {access_token}
```

**请求参数**：

```json
{
  "work_id": "123e4567-e89b-12d3-a456-426614174001",
  "chapter_ids": [
    "chapter-id-3",
    "chapter-id-1",
    "chapter-id-2"
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| work_id | string | 是 | 作品ID |
| chapter_ids | array | 是 | 章节ID列表（按新顺序排列） |

**响应示例**：

```json
{
  "message": "Chapters reordered successfully"
}
```

**状态码**：
- `200`: 排序成功
- `404`: 作品不存在
- `403`: 无权操作
- `401`: 未登录

---

## 数据模型

### User（用户）

```typescript
interface User {
  id: string;              // UUID
  username: string;        // 用户名
  email: string;           // 邮箱
  full_name: string | null;  // 真实姓名
  avatar: string | null;     // 头像URL
  bio: string | null;        // 个人简介
  is_active: boolean;      // 是否激活
  is_admin: boolean;       // 是否管理员
  is_verified: boolean;    // 是否已验证邮箱
  created_at: string;      // 创建时间（ISO 8601）
  updated_at: string;      // 更新时间
  last_login_at: string | null;  // 最后登录时间
}
```

### Work（作品）

```typescript
interface Work {
  id: string;              // UUID
  author_id: string;       // 作者ID
  title: string;           // 标题
  description: string | null;  // 简介
  genre: WorkGenre;        // 类型
  status: WorkStatus;      // 状态
  cover_image: string | null;  // 封面图片URL
  total_words: number;     // 总字数
  total_chapters: number;  // 总章节数
  view_count: number;      // 浏览次数
  created_at: string;      // 创建时间
  updated_at: string;      // 更新时间
  published_at: string | null;  // 发布时间
}

enum WorkGenre {
  FANTASY = "FANTASY",     // 玄幻
  URBAN = "URBAN",         // 都市
  ROMANCE = "ROMANCE",     // 言情
  SCIFI = "SCIFI",         // 科幻
  WUXIA = "WUXIA",         // 武侠
  HISTORY = "HISTORY",     // 历史
  GAME = "GAME",           // 游戏
  OTHER = "OTHER"          // 其他
}

enum WorkStatus {
  DRAFT = "DRAFT",             // 草稿
  SERIALIZING = "SERIALIZING", // 连载中
  COMPLETED = "COMPLETED",     // 已完结
  PAUSED = "PAUSED"           // 暂停更新
}
```

### Chapter（章节）

```typescript
interface Chapter {
  id: string;              // UUID
  work_id: string;         // 作品ID
  title: string;           // 标题
  content: string;         // 内容
  order: number;           // 排序
  is_published: boolean;   // 是否发布
  word_count: number;      // 字数
  view_count: number;      // 浏览次数
  created_at: string;      // 创建时间
  updated_at: string;      // 更新时间
  published_at: string | null;  // 发布时间
}
```

---

## 错误码说明

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无返回内容） |
| 400 | 请求参数错误 |
| 401 | 未登录或 Token 无效 |
| 403 | 无权访问 |
| 404 | 资源不存在 |
| 409 | 资源冲突（如用户名已存在） |
| 500 | 服务器内部错误 |

### 常见错误响应

#### 401 未授权

```json
{
  "detail": "Not authenticated"
}
```

**解决方法**：检查是否已登录，Token 是否有效。

#### 400 参数错误

```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**解决方法**：检查请求参数是否完整、格式是否正确。

#### 403 无权访问

```json
{
  "detail": "Not authorized to access this work"
}
```

**解决方法**：确认当前用户是否有权限操作该资源。

---

## 使用示例

### JavaScript/TypeScript

#### 登录并保存 Token

```javascript
async function login(username, password) {
  const response = await fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({ username, password })
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  
  return data;
}
```

#### 使用 Token 请求接口

```javascript
async function getMyWorks() {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/api/v1/works?skip=0&limit=20', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch works');
  }
  
  return await response.json();
}
```

#### 创建作品

```javascript
async function createWork(title, description, genre = 'FANTASY') {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/api/v1/works', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title,
      description,
      genre,
      status: 'DRAFT'
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to create work');
  }
  
  return await response.json();
}
```

#### Token 自动刷新

```javascript
async function refreshToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  
  const response = await fetch('http://localhost:8000/api/v1/auth/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  
  if (!response.ok) {
    // Token 已过期，需要重新登录
    localStorage.clear();
    window.location.href = '/login';
    return;
  }
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  
  return data;
}

// 在请求拦截器中自动刷新 Token
async function fetchWithAuth(url, options = {}) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    }
  });
  
  // 如果返回 401，尝试刷新 Token
  if (response.status === 401) {
    await refreshToken();
    
    // 重新发送请求
    const newToken = localStorage.getItem('access_token');
    return fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${newToken}`
      }
    });
  }
  
  return response;
}
```

### Axios 示例

```javascript
import axios from 'axios';

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 10000
});

// 请求拦截器：自动添加 Token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// 响应拦截器：自动刷新 Token
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    
    // 如果返回 401 且还没有重试过
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(
          'http://localhost:8000/api/v1/auth/refresh',
          { refresh_token: refreshToken }
        );
        
        const { access_token, refresh_token: newRefreshToken } = response.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', newRefreshToken);
        
        // 重新发送原始请求
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // 刷新失败，跳转到登录页
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// 使用示例
export const authAPI = {
  login: (username, password) => 
    api.post('/auth/login', new URLSearchParams({ username, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }),
  register: (data) => api.post('/auth/register', data)
};

export const workAPI = {
  getWorks: (params) => api.get('/works', { params }),
  getWork: (id) => api.get(`/works/${id}`),
  createWork: (data) => api.post('/works', data),
  updateWork: (id, data) => api.put(`/works/${id}`, data),
  deleteWork: (id) => api.delete(`/works/${id}`)
};

export const chapterAPI = {
  getChapters: (workId) => api.get(`/chapters/work/${workId}`),
  getChapter: (id) => api.get(`/chapters/${id}`),
  createChapter: (data) => api.post('/chapters', data),
  updateChapter: (id, data) => api.put(`/chapters/${id}`, data),
  deleteChapter: (id) => api.delete(`/chapters/${id}`),
  reorderChapters: (workId, chapterIds) => 
    api.post('/chapters/reorder', { work_id: workId, chapter_ids: chapterIds })
};
```

---

## 测试建议

### 1. 使用 Swagger UI 测试

访问 http://localhost:8000/docs：
1. 点击接口展开
2. 点击 "Try it out"
3. 填写参数
4. 点击 "Execute"
5. 查看响应结果

### 2. 使用 Postman

导入接口：
1. 创建新的 Collection
2. 添加环境变量：`base_url = http://localhost:8000`
3. 设置全局 Token 变量
4. 按照本文档创建请求

### 3. 测试流程

```
1. 注册用户 (POST /auth/register)
   ↓
2. 登录获取 Token (POST /auth/login)
   ↓
3. 获取用户信息 (GET /users/me)
   ↓
4. 创建作品 (POST /works)
   ↓
5. 获取作品列表 (GET /works)
   ↓
6. 创建章节 (POST /chapters)
   ↓
7. 获取章节列表 (GET /chapters/work/{work_id})
   ↓
8. 更新章节 (PUT /chapters/{chapter_id})
   ↓
9. 删除章节 (DELETE /chapters/{chapter_id})
   ↓
10. 删除作品 (DELETE /works/{work_id})
```

---

## 附录

### CORS 配置

默认允许的前端地址：
- http://localhost:5173 (Vite)
- http://localhost:3000 (React/Next.js)

如需添加其他地址，请修改 `backend/.env` 文件中的 `CORS_ORIGINS`。

### 限流说明

当前版本暂无限流，生产环境建议添加。

### WebSocket 支持

当前版本暂不支持 WebSocket，后续版本可能会添加实时协作功能。

---

## 更新日志

- **v1.0.0** (2024-01-01): 初始版本，包含用户、作品、章节基础功能

---

## 支持

遇到问题？
- 📖 查看在线文档：http://localhost:8000/docs
- 🐛 查看日志：`backend/logs/app.log`
- 🔍 运行环境检查：`backend/check_env.bat`
- 💬 联系后端开发者

祝开发顺利！🚀
