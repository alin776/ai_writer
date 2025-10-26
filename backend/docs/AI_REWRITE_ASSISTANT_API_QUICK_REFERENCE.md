# 🚀 AI 改写助手 API 速查表

> **快速参考文档** - 打印或保存此文档以便快速查找
> **完整文档：** [AI_REWRITE_ASSISTANT_API.md](./AI_REWRITE_ASSISTANT_API.md)

---

## 📌 基本信息

**基础路径：** `/api/v1`
**认证方式：** JWT Token（请求头 `Authorization: Bearer <token>`）

---

## 🔗 接口列表

| # | 接口 | 方法 | 路径 | 说明 |
|---|------|------|------|------|
| 1 | 获取模型列表 | GET | `/ai/rewrite-arena/models` | 获取可用模型 |
| 2 | 智能分析 | POST | `/ai/rewrite-arena/analyze` | 分析文本质量 |
| 3 | 多模型改写 | POST | `/ai/rewrite-arena/rewrite` | 改写文本 |
| 4 | 保存记录 | POST | `/rewrite-history/sessions` | 保存改写历史 |
| 5 | 历史列表 | GET | `/rewrite-history/sessions` | 获取历史记录 |
| 6 | 历史详情 | GET | `/rewrite-history/sessions/{id}` | 获取详情 |
| 7 | 删除记录 | DELETE | `/rewrite-history/sessions/{id}` | 删除历史 |

---

## 📋 快速示例

### 1️⃣ 获取模型列表

```http
GET /api/v1/ai/rewrite-arena/models
Authorization: Bearer <token>
```

**响应：**
```json
{
  "models": [
    { "id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro", "enabled": true },
    { "id": "gpt-5", "name": "GPT-5", "enabled": true }
  ],
  "default_models": ["gemini-2.5-pro", "gpt-5"],
  "max_models": 4
}
```

---

### 2️⃣ 智能分析

```http
POST /api/v1/ai/rewrite-arena/analyze
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "主角走进房间，看到了桌子上的剑。",
  "context_before": "经过三天的跋涉...",  // 可选
  "context_after": "他拿起剑..."          // 可选
}
```

**响应：**
```json
{
  "quality_score": 45,
  "issues": [
    { "type": "too_simple", "severity": "high", "description": "描写过于简单" }
  ],
  "recommended_mode": "expand",
  "reason": "建议增加细节和情感描写"
}
```

---

### 3️⃣ 多模型改写

```http
POST /api/v1/ai/rewrite-arena/rewrite
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "主角走进房间，看到了桌子上的剑。",
  "mode": "expand",                       // optimize/expand/compress/custom
  "custom_requirement": null,            // 仅 mode=custom 时需要
  "context_before": "经过三天的跋涉...", // 可选
  "context_after": "他拿起剑...",        // 可选
  "model_names": ["gemini-2.5-pro", "gpt-5"] // 可选，不指定则使用默认
}
```

**响应：**
```json
{
  "original_text": "主角走进房间，看到了桌子上的剑。",
  "mode": "expand",
  "results": [
    {
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "主角推开那扇厚重的木门...",
      "word_count": 156,
      "elapsed_time": 2.3,
      "error": null
    }
  ]
}
```

---

### 4️⃣ 保存改写记录

```http
POST /api/v1/rewrite-history/sessions
Authorization: Bearer <token>
Content-Type: application/json

{
  "original_text": "主角走进房间，看到了桌子上的剑。",
  "mode": "expand",
  "context_before": "...",  // 可选
  "context_after": "...",   // 可选
  "custom_requirement": null, // 可选
  "results": [
    {
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "主角推开那扇厚重的木门...",
      "word_count": 156,
      "elapsed_time": 2.3,
      "error": null,
      "is_selected": true  // 是否被用户选中
    }
  ]
}
```

**响应：** 返回完整的会话信息（包含 ID 和 created_at）

---

### 5️⃣ 获取历史列表

```http
GET /api/v1/rewrite-history/sessions?page=1&page_size=20
Authorization: Bearer <token>
```

**响应：**
```json
{
  "sessions": [
    {
      "id": "550e8400-...",
      "original_text": "主角走进房间...",
      "mode": "expand",
      "result_count": 2,
      "created_at": "2025-10-26T10:30:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 20
}
```

---

### 6️⃣ 获取会话详情

```http
GET /api/v1/rewrite-history/sessions/{session_id}
Authorization: Bearer <token>
```

**响应：** 返回完整会话信息（包括所有 results）

---

### 7️⃣ 删除记录

```http
DELETE /api/v1/rewrite-history/sessions/{session_id}
Authorization: Bearer <token>
```

**响应：**
```json
{
  "message": "改写记录删除成功",
  "deleted_session_id": "550e8400-..."
}
```

---

## 📊 数据枚举

### RewriteMode（改写模式）

| 值 | 说明 |
|---|------|
| `optimize` | 优化提升（默认） |
| `expand` | 扩写丰富 |
| `compress` | 精简压缩 |
| `custom` | 自定义要求 |

### IssueType（问题类型）

| 值 | 说明 |
|---|------|
| `too_simple` | 描写过于简单 |
| `lack_emotion` | 缺少情感渲染 |
| `weak_details` | 细节不足 |
| `repetitive` | 重复啰嗦 |
| `unclear_logic` | 逻辑不清 |
| `poor_rhythm` | 节奏感差 |
| `weak_character` | 人物形象单薄 |
| `inconsistent_style` | 风格不统一 |
| `grammar_error` | 语法错误 |
| `other` | 其他 |

### IssueSeverity（严重程度）

| 值 | 说明 |
|---|------|
| `low` | 轻微 |
| `medium` | 中等 |
| `high` | 严重 |
| `critical` | 极严重 |

---

## ⚠️ 常见错误

| 状态码 | 说明 | 常见原因 |
|--------|------|---------|
| 400 | 请求错误 | 参数验证失败、模型数量超限 |
| 401 | 未认证 | Token 缺失或无效 |
| 403 | 无权限 | 无权访问他人数据 |
| 404 | 未找到 | 资源不存在 |
| 422 | 验证错误 | 请求体格式错误 |
| 500 | 服务器错误 | AI 服务异常、数据库错误 |

**错误响应格式：**
```json
{
  "detail": "错误信息描述"
}
```

---

## 💡 使用提示

### 字段长度限制

| 字段 | 最小长度 | 最大长度 |
|------|---------|---------|
| `text`（原文） | 1 | 5000 |
| `context_before` | 0 | 3000 |
| `context_after` | 0 | 3000 |
| `custom_requirement` | 0 | 500 |

### 性能建议

⏱️ **改写接口耗时：** 2-5 秒（建议显示加载动画）
📦 **分页建议：** 每页 20 条记录
🔄 **重试策略：** 对 5xx 错误实施指数退避重试
💾 **缓存策略：** 模型列表缓存 5 分钟

### 上下文智能分级

后端会根据原文长度自动调整上下文范围：

| 原文长度 | 前后上下文 |
|---------|-----------|
| < 50 字 | 各 800 字 |
| < 200 字 | 各 500 字 |
| < 500 字 | 各 300 字 |
| ≥ 500 字 | 无上下文 |

---

## 🔧 TypeScript 类型参考

```typescript
// 改写模式
enum RewriteMode {
  OPTIMIZE = "optimize",
  EXPAND = "expand",
  COMPRESS = "compress",
  CUSTOM = "custom"
}

// 文本分析请求
interface TextAnalysisRequest {
  text: string;
  context_before?: string;
  context_after?: string;
}

// 文本分析结果
interface TextAnalysisResult {
  quality_score: number;        // 0-100
  issues: TextIssue[];
  recommended_mode: RewriteMode;
  reason: string;
}

// 改写请求
interface RewriteRequest {
  text: string;
  mode: RewriteMode;
  custom_requirement?: string;
  context_before?: string;
  context_after?: string;
  model_names?: string[];       // 可选，不指定则使用默认
}

// 改写响应
interface RewriteResponse {
  original_text: string;
  mode: RewriteMode;
  results: ModelResult[];
}

// 模型结果
interface ModelResult {
  model_name: string;
  rewritten_text: string;
  word_count: number;
  elapsed_time: number;
  error: string | null;
}
```

---

## 📞 联系方式

**完整文档：** [AI_REWRITE_ASSISTANT_API.md](./AI_REWRITE_ASSISTANT_API.md)
**问题反馈：** 联系后端开发团队

---

**文档版本：** v1.0 | **更新日期：** 2025-10-26
