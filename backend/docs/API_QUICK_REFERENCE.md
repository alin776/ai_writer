# API 接口快速参考表

> 一页纸速查所有接口

## 🔐 认证接口

| 接口 | 方法 | 路径 | 需要Token | 说明 |
|------|------|------|-----------|------|
| 用户注册 | POST | `/api/v1/auth/register` | ❌ | 注册新用户 |
| 用户登录 | POST | `/api/v1/auth/login` | ❌ | 获取Token |
| 刷新Token | POST | `/api/v1/auth/refresh` | ❌ | 刷新access_token |

## 👤 用户接口

| 接口 | 方法 | 路径 | 需要Token | 说明 |
|------|------|------|-----------|------|
| 获取当前用户信息 | GET | `/api/v1/users/me` | ✅ | 获取登录用户信息 |
| 更新当前用户信息 | PUT | `/api/v1/users/me` | ✅ | 更新个人资料 |
| 获取指定用户信息 | GET | `/api/v1/users/{user_id}` | ✅ | 查看其他用户 |
| 获取用户列表 | GET | `/api/v1/users` | ✅ | 分页查询用户 |

## 📚 作品接口

| 接口 | 方法 | 路径 | 需要Token | 说明 |
|------|------|------|-----------|------|
| 获取作品列表 | GET | `/api/v1/works` | ✅ | 分页、搜索 |
| 获取作品详情 | GET | `/api/v1/works/{work_id}` | ✅ | 查看单个作品 |
| 创建作品 | POST | `/api/v1/works` | ✅ | 新建作品 |
| 更新作品 | PUT | `/api/v1/works/{work_id}` | ✅ | 修改作品信息 |
| 删除作品 | DELETE | `/api/v1/works/{work_id}` | ✅ | 删除作品及章节 |

## 📖 章节接口

| 接口 | 方法 | 路径 | 需要Token | 说明 |
|------|------|------|-----------|------|
| 获取章节列表 | GET | `/api/v1/chapters/work/{work_id}` | ✅ | 获取作品的所有章节 |
| 获取章节详情 | GET | `/api/v1/chapters/{chapter_id}` | ✅ | 查看单个章节 |
| 创建章节 | POST | `/api/v1/chapters` | ✅ | 新建章节 |
| 更新章节 | PUT | `/api/v1/chapters/{chapter_id}` | ✅ | 修改章节内容 |
| 删除章节 | DELETE | `/api/v1/chapters/{chapter_id}` | ✅ | 删除章节 |
| 重新排序章节 | POST | `/api/v1/chapters/reorder` | ✅ | 调整章节顺序 |

## 🌐 其他接口

| 接口 | 方法 | 路径 | 需要Token | 说明 |
|------|------|------|-----------|------|
| 根路径 | GET | `/` | ❌ | 服务信息 |
| 健康检查 | GET | `/health` | ❌ | 服务状态 |

## 📊 请求参数速查

### 注册

```json
POST /api/v1/auth/register
{
  "username": "string",    // 必填，3-50字符
  "email": "string",       // 必填，邮箱格式
  "password": "string"     // 必填，至少6字符
}
```

### 登录

```
POST /api/v1/auth/login (Form Data)
username: string   // 必填
password: string   // 必填
```

### 创建作品

```json
POST /api/v1/works
{
  "title": "string",          // 必填，1-200字符
  "description": "string",    // 可选
  "genre": "FANTASY",         // 可选，默认OTHER
  "status": "DRAFT",          // 可选，默认DRAFT
  "cover_image": "string"     // 可选，URL
}
```

### 创建章节

```json
POST /api/v1/chapters
{
  "work_id": "uuid",     // 必填
  "title": "string",     // 必填，1-200字符
  "content": "string",   // 必填
  "order": 1             // 可选，默认自动排序
}
```

## 🎨 枚举值速查

### 作品类型（genre）

```
FANTASY   - 玄幻
URBAN     - 都市
ROMANCE   - 言情
SCIFI     - 科幻
WUXIA     - 武侠
HISTORY   - 历史
GAME      - 游戏
OTHER     - 其他
```

### 作品状态（status）

```
DRAFT        - 草稿
SERIALIZING  - 连载中
COMPLETED    - 已完结
PAUSED       - 暂停更新
```

## 🔑 Token 使用

### 获取 Token
1. 调用登录接口
2. 保存返回的 `access_token` 和 `refresh_token`

### 使用 Token
在请求头添加：
```
Authorization: Bearer {access_token}
```

### Token 有效期
- `access_token`: 60分钟
- `refresh_token`: 7天

### Token 过期处理
1. 捕获 401 错误
2. 使用 `refresh_token` 调用刷新接口
3. 获取新的 Token
4. 重新发送原始请求

## 📋 HTTP 状态码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无内容） |
| 400 | 参数错误 |
| 401 | 未登录/Token无效 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 500 | 服务器错误 |

## 💡 常用查询参数

### 分页

```
?skip=0&limit=20
```

- `skip`: 跳过的记录数
- `limit`: 每页数量

### 搜索

```
?search=关键词
```

### 筛选

```
?author_id=uuid   // 按作者筛选
```

## 🚀 快速上手

### 1. 完整流程

```javascript
// 1. 注册
POST /api/v1/auth/register
{ username, email, password }

// 2. 登录
POST /api/v1/auth/login
{ username, password }
→ 获取 access_token

// 3. 获取用户信息
GET /api/v1/users/me
Headers: { Authorization: "Bearer {access_token}" }

// 4. 创建作品
POST /api/v1/works
Headers: { Authorization: "Bearer {access_token}" }
Body: { title, description, genre }

// 5. 创建章节
POST /api/v1/chapters
Headers: { Authorization: "Bearer {access_token}" }
Body: { work_id, title, content }
```

### 2. Axios 封装示例

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1'
});

// 自动添加 Token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 导出接口
export const auth = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', new URLSearchParams(data)),
  refresh: (token) => api.post('/auth/refresh', { refresh_token: token })
};

export const works = {
  list: (params) => api.get('/works', { params }),
  get: (id) => api.get(`/works/${id}`),
  create: (data) => api.post('/works', data),
  update: (id, data) => api.put(`/works/${id}`, data),
  delete: (id) => api.delete(`/works/${id}`)
};

export const chapters = {
  list: (workId) => api.get(`/chapters/work/${workId}`),
  get: (id) => api.get(`/chapters/${id}`),
  create: (data) => api.post('/chapters', data),
  update: (id, data) => api.put(`/chapters/${id}`, data),
  delete: (id) => api.delete(`/chapters/${id}`),
  reorder: (workId, ids) => api.post('/chapters/reorder', { 
    work_id: workId, 
    chapter_ids: ids 
  })
};
```

## 📝 注意事项

1. ✅ 所有需要认证的接口必须在请求头添加 Token
2. ✅ 登录接口使用 Form Data 格式，其他接口使用 JSON
3. ✅ 所有 ID 都是 UUID 格式的字符串
4. ✅ 时间格式为 ISO 8601 字符串
5. ✅ 枚举值全部大写
6. ✅ 只能操作自己的作品和章节
7. ✅ 删除作品会同时删除所有章节
8. ✅ 创建/更新/删除章节会自动更新作品统计

## 📚 完整文档

详细的接口说明、响应格式、错误处理等，请查看：
- **API_REFERENCE.md** - 完整 API 文档（推荐）
- **在线文档**: http://localhost:8000/docs （可在线测试）

---

打印此页，放在手边，开发更高效！📄
