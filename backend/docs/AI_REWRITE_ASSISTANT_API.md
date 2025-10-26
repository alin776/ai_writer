# 🎨 AI 改写助手 API 文档

> **适用人员：** 前端开发者
> **版本：** v1.0
> **更新日期：** 2025-10-26
> **基础路径：** `/api/v1`

---

## 📋 目录

- [概述](#概述)
- [认证说明](#认证说明)
- [API 接口列表](#api-接口列表)
  - [1. 获取可用模型列表](#1-获取可用模型列表)
  - [2. 智能分析文本](#2-智能分析文本)
  - [3. 多模型改写](#3-多模型改写)
  - [4. 保存改写记录](#4-保存改写记录)
  - [5. 获取改写历史列表](#5-获取改写历史列表)
  - [6. 获取改写会话详情](#6-获取改写会话详情)
  - [7. 删除改写记录](#7-删除改写记录)
- [数据模型](#数据模型)
- [错误处理](#错误处理)
- [使用场景示例](#使用场景示例)
- [性能建议](#性能建议)

---

## 概述

AI 改写助手提供了完整的文本改写功能，包括：

- **智能分析** - AI 自动分析文本质量，检测问题，给出改写建议
- **多模型改写** - 并发调用多个 AI 模型改写文本，对比效果
- **历史记录** - 保存和管理改写历史，支持查询和删除

### 核心特性

✅ **智能分级上下文** - 根据文本长度自动调整上下文范围
✅ **并发处理** - 多模型同时改写，节省时间
✅ **结构化分析** - 使用 LangChain 确保 AI 返回可解析的 JSON
✅ **完整历史** - 保存所有改写记录，支持分页查询

---

## 认证说明

所有接口都需要用户认证，请在请求头中携带 JWT Token：

```http
Authorization: Bearer <your_jwt_token>
```

**获取 Token：**
- 使用登录接口 `POST /api/v1/auth/login` 获取 Token
- Token 有效期根据系统配置（默认 7 天）

---

## API 接口列表

### 1. 获取可用模型列表

获取改写助手的可用模型列表及配置信息。

#### 请求

```http
GET /api/v1/ai/rewrite-arena/models
```

**Headers:**
```http
Authorization: Bearer <token>
```

**Query Parameters:** 无

#### 响应

**成功 (200 OK):**

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
    }
  ],
  "default_models": ["gemini-2.5-pro", "gpt-5"],
  "max_models": 4
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `models` | Array | 可用模型列表 |
| `models[].id` | String | 模型 ID（调用时使用） |
| `models[].name` | String | 模型显示名称 |
| `models[].description` | String | 模型特点描述 |
| `models[].enabled` | Boolean | 是否启用 |
| `default_models` | Array | 默认使用的模型列表 |
| `max_models` | Integer | 最多可选择的模型数量 |

**使用场景：**
- 页面初始化时获取模型列表
- 用户选择模型时展示可用选项

---

### 2. 智能分析文本

AI 自动分析文本质量，检测问题，给出改写建议。

#### 请求

```http
POST /api/v1/ai/rewrite-arena/analyze
```

**Headers:**
```http
Authorization: Bearer <token>
Content-Type: application/json
```

**Body (JSON):**

```json
{
  "text": "主角走进房间，看到了桌子上的剑。",
  "context_before": "经过三天的跋涉，主角终于来到了目的地...",
  "context_after": "他拿起剑，准备离开..."
}
```

**字段说明：**

| 字段 | 类型 | 必填 | 长度限制 | 说明 |
|------|------|------|---------|------|
| `text` | String | ✅ | 1-5000 字符 | 待分析的文本 |
| `context_before` | String | ❌ | 0-3000 字符 | 前文上下文（可选） |
| `context_after` | String | ❌ | 0-3000 字符 | 后文上下文（可选） |

#### 响应

**成功 (200 OK):**

```json
{
  "quality_score": 45,
  "issues": [
    {
      "type": "too_simple",
      "severity": "high",
      "description": "描写过于简单，缺少画面感"
    },
    {
      "type": "lack_emotion",
      "severity": "medium",
      "description": "缺少情感渲染"
    }
  ],
  "recommended_mode": "expand",
  "reason": "建议增加细节和情感描写，使画面更生动"
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `quality_score` | Integer | 质量评分（0-100） |
| `issues` | Array | 检测到的问题列表 |
| `issues[].type` | String | 问题类型（见下表） |
| `issues[].severity` | String | 严重程度：`low`/`medium`/`high`/`critical` |
| `issues[].description` | String | 问题描述 |
| `recommended_mode` | String | 推荐的改写模式（见下表） |
| `reason` | String | 推荐理由 |

**问题类型 (IssueType)：**

| 类型 | 说明 |
|------|------|
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

**改写模式 (RewriteMode)：**

| 模式 | 说明 |
|------|------|
| `optimize` | 优化提升（默认） |
| `expand` | 扩写丰富 |
| `compress` | 精简压缩 |
| `custom` | 自定义要求 |

**使用场景：**
- 用户点击"开始分析"按钮时调用
- 根据分析结果展示质量评分和问题列表
- 自动选择推荐的改写模式

---

### 3. 多模型改写

使用多个 AI 模型并发改写文本，对比不同模型的效果。

#### 请求

```http
POST /api/v1/ai/rewrite-arena/rewrite
```

**Headers:**
```http
Authorization: Bearer <token>
Content-Type: application/json
```

**Body (JSON):**

```json
{
  "text": "主角走进房间，看到了桌子上的剑。",
  "mode": "expand",
  "custom_requirement": null,
  "context_before": "经过三天的跋涉...",
  "context_after": "他拿起剑...",
  "model_names": ["gemini-2.5-pro", "gpt-5"]
}
```

**字段说明：**

| 字段 | 类型 | 必填 | 长度限制 | 说明 |
|------|------|------|---------|------|
| `text` | String | ✅ | 1-5000 字符 | 待改写的文本 |
| `mode` | String | ✅ | - | 改写模式：`optimize`/`expand`/`compress`/`custom` |
| `custom_requirement` | String | ❌ | 0-500 字符 | 自定义要求（仅当 mode=custom 时需要） |
| `context_before` | String | ❌ | 0-3000 字符 | 前文上下文（可选） |
| `context_after` | String | ❌ | 0-3000 字符 | 后文上下文（可选） |
| `model_names` | Array | ❌ | 最多 4 个 | 指定使用的模型列表（不指定则使用默认） |

#### 响应

**成功 (200 OK):**

```json
{
  "original_text": "主角走进房间，看到了桌子上的剑。",
  "mode": "expand",
  "results": [
    {
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "主角推开那扇厚重的木门，昏暗的房间中唯有一柄长剑泛着幽冷的寒光，静静地躺在陈旧的木桌之上。剑身上隐约可见古老的纹路，仿佛在诉说着一段尘封已久的往事。",
      "word_count": 156,
      "elapsed_time": 2.3,
      "error": null
    },
    {
      "model_name": "gpt-5",
      "rewritten_text": "房门缓缓开启，主角的视线立刻被桌上那柄寒光闪烁的长剑锁定。剑身修长，剑刃锋利，在微弱的光线下散发出凛冽的杀气，让人不由自主地心生敬畏。",
      "word_count": 142,
      "elapsed_time": 1.8,
      "error": null
    }
  ]
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `original_text` | String | 原文 |
| `mode` | String | 改写模式 |
| `results` | Array | 各模型的改写结果 |
| `results[].model_name` | String | 模型名称 |
| `results[].rewritten_text` | String | 改写后的文本 |
| `results[].word_count` | Integer | 字数 |
| `results[].elapsed_time` | Float | 耗时（秒） |
| `results[].error` | String/Null | 错误信息（如果失败） |

**使用场景：**
- 用户确认改写模式后调用
- 并排展示多个模型的改写结果
- 显示性能指标（耗时、字数）

**注意事项：**
- 改写时间通常 2-5 秒，建议显示加载动画
- 如果某个模型失败，`error` 字段会包含错误信息
- 最多可同时使用 4 个模型（由 `max_models` 配置）

---

### 4. 保存改写记录

保存一次改写会话及其所有模型的改写结果到数据库。

#### 请求

```http
POST /api/v1/rewrite-history/sessions
```

**Headers:**
```http
Authorization: Bearer <token>
Content-Type: application/json
```

**Body (JSON):**

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
      "rewritten_text": "房门缓缓开启...",
      "word_count": 142,
      "elapsed_time": 1.8,
      "error": null,
      "is_selected": false
    }
  ]
}
```

**字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `original_text` | String | ✅ | 原文 |
| `context_before` | String | ❌ | 前文上下文 |
| `context_after` | String | ❌ | 后文上下文 |
| `mode` | String | ✅ | 改写模式 |
| `custom_requirement` | String | ❌ | 自定义要求 |
| `results` | Array | ✅ | 改写结果列表 |
| `results[].model_name` | String | ✅ | 模型名称 |
| `results[].rewritten_text` | String | ✅ | 改写后的文本 |
| `results[].word_count` | Integer | ✅ | 字数 |
| `results[].elapsed_time` | Float | ✅ | 耗时（秒） |
| `results[].error` | String/Null | ❌ | 错误信息 |
| `results[].is_selected` | Boolean | ✅ | 是否被用户选中 |

#### 响应

**成功 (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "original_text": "主角走进房间，看到了桌子上的剑。",
  "context_before": "经过三天的跋涉...",
  "context_after": "他拿起剑...",
  "mode": "expand",
  "custom_requirement": null,
  "created_at": "2025-10-26T10:30:00Z",
  "results": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "主角推开那扇厚重的木门...",
      "word_count": 156,
      "elapsed_time": 2.3,
      "error": null,
      "is_selected": true,
      "created_at": "2025-10-26T10:30:00Z"
    }
  ]
}
```

**使用场景：**
- 用户点击"采用"按钮后自动保存
- 保存用户选择的改写结果
- 用于后续查看历史记录

---

### 5. 获取改写历史列表

获取当前用户的改写历史记录列表（分页）。

#### 请求

```http
GET /api/v1/rewrite-history/sessions?page=1&page_size=20
```

**Headers:**
```http
Authorization: Bearer <token>
```

**Query Parameters:**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `page` | Integer | ❌ | 1 | 页码（从 1 开始） |
| `page_size` | Integer | ❌ | 20 | 每页数量（1-100） |

#### 响应

**成功 (200 OK):**

```json
{
  "sessions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "original_text": "主角走进房间，看到了桌子上的剑。",
      "mode": "expand",
      "result_count": 2,
      "created_at": "2025-10-26T10:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "original_text": "夕阳西下，天边的晚霞如同燃烧的火焰...",
      "mode": "optimize",
      "result_count": 3,
      "created_at": "2025-10-26T09:15:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 20
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `sessions` | Array | 会话列表 |
| `sessions[].id` | String | 会话 ID |
| `sessions[].original_text` | String | 原文（可能截断） |
| `sessions[].mode` | String | 改写模式 |
| `sessions[].result_count` | Integer | 结果数量 |
| `sessions[].created_at` | String | 创建时间（ISO 8601） |
| `total` | Integer | 总记录数 |
| `page` | Integer | 当前页码 |
| `page_size` | Integer | 每页数量 |

**使用场景：**
- 历史记录列表页面
- 支持分页加载
- 按创建时间倒序排列（最新的在前）

---

### 6. 获取改写会话详情

获取指定改写会话的完整信息，包括所有模型的改写结果。

#### 请求

```http
GET /api/v1/rewrite-history/sessions/{session_id}
```

**Headers:**
```http
Authorization: Bearer <token>
```

**Path Parameters:**

| 参数 | 类型 | 说明 |
|------|------|------|
| `session_id` | String (UUID) | 会话 ID |

#### 响应

**成功 (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "original_text": "主角走进房间，看到了桌子上的剑。",
  "context_before": "经过三天的跋涉...",
  "context_after": "他拿起剑...",
  "mode": "expand",
  "custom_requirement": null,
  "created_at": "2025-10-26T10:30:00Z",
  "results": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "主角推开那扇厚重的木门...",
      "word_count": 156,
      "elapsed_time": 2.3,
      "error": null,
      "is_selected": true,
      "created_at": "2025-10-26T10:30:00Z"
    },
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "model_name": "gpt-5",
      "rewritten_text": "房门缓缓开启...",
      "word_count": 142,
      "elapsed_time": 1.8,
      "error": null,
      "is_selected": false,
      "created_at": "2025-10-26T10:30:00Z"
    }
  ]
}
```

**使用场景：**
- 查看历史改写记录的详细信息
- 再次对比不同模型的改写结果
- 复制之前改写的文本

---

### 7. 删除改写记录

删除指定的改写会话及其所有结果。

#### 请求

```http
DELETE /api/v1/rewrite-history/sessions/{session_id}
```

**Headers:**
```http
Authorization: Bearer <token>
```

**Path Parameters:**

| 参数 | 类型 | 说明 |
|------|------|------|
| `session_id` | String (UUID) | 会话 ID |

#### 响应

**成功 (200 OK):**

```json
{
  "message": "改写记录删除成功",
  "deleted_session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**错误 (404 Not Found):**

```json
{
  "detail": "改写记录不存在"
}
```

**错误 (403 Forbidden):**

```json
{
  "detail": "无权删除此改写记录"
}
```

**使用场景：**
- 用户删除不需要的历史记录
- 清理个人数据

---

## 数据模型

### IssueSeverity（问题严重程度）

```typescript
enum IssueSeverity {
  LOW = "low",           // 轻微
  MEDIUM = "medium",     // 中等
  HIGH = "high",         // 严重
  CRITICAL = "critical"  // 极严重
}
```

### IssueType（问题类型）

```typescript
enum IssueType {
  TOO_SIMPLE = "too_simple",               // 描写过于简单
  LACK_EMOTION = "lack_emotion",           // 缺少情感渲染
  WEAK_DETAILS = "weak_details",           // 细节不足
  REPETITIVE = "repetitive",               // 重复啰嗦
  UNCLEAR_LOGIC = "unclear_logic",         // 逻辑不清
  POOR_RHYTHM = "poor_rhythm",             // 节奏感差
  WEAK_CHARACTER = "weak_character",       // 人物形象单薄
  INCONSISTENT_STYLE = "inconsistent_style", // 风格不统一
  GRAMMAR_ERROR = "grammar_error",         // 语法错误
  OTHER = "other"                          // 其他
}
```

### RewriteMode（改写模式）

```typescript
enum RewriteMode {
  OPTIMIZE = "optimize",   // 优化提升（默认）
  EXPAND = "expand",       // 扩写丰富
  COMPRESS = "compress",   // 精简压缩
  CUSTOM = "custom"        // 自定义要求
}
```

### TextIssue（文本问题）

```typescript
interface TextIssue {
  type: IssueType;          // 问题类型
  severity: IssueSeverity;  // 严重程度
  description: string;      // 问题描述
}
```

### TextAnalysisResult（文本分析结果）

```typescript
interface TextAnalysisResult {
  quality_score: number;        // 质量评分（0-100）
  issues: TextIssue[];          // 检测到的问题列表
  recommended_mode: RewriteMode; // 推荐的改写模式
  reason: string;               // 推荐理由
}
```

### ModelResult（模型改写结果）

```typescript
interface ModelResult {
  model_name: string;      // 模型名称
  rewritten_text: string;  // 改写后的文本
  word_count: number;      // 字数
  elapsed_time: number;    // 耗时（秒）
  error: string | null;    // 错误信息（如果失败）
}
```

### RewriteResponse（改写响应）

```typescript
interface RewriteResponse {
  original_text: string;   // 原文
  mode: RewriteMode;       // 改写模式
  results: ModelResult[];  // 各模型的改写结果
}
```

---

## 错误处理

### HTTP 状态码

| 状态码 | 说明 | 常见原因 |
|--------|------|---------|
| 200 | 成功 | 请求成功处理 |
| 400 | 请求错误 | 参数验证失败、模型数量超限 |
| 401 | 未认证 | Token 缺失或无效 |
| 403 | 无权限 | 无权访问他人的数据 |
| 404 | 未找到 | 资源不存在 |
| 422 | 验证错误 | 请求体格式错误 |
| 500 | 服务器错误 | AI 服务异常、数据库错误 |

### 错误响应格式

```json
{
  "detail": "错误信息描述"
}
```

### 常见错误示例

**1. Token 缺失或无效**

```json
{
  "detail": "未授权"
}
```

**2. 参数验证失败**

```json
{
  "detail": "text字段不能为空"
}
```

**3. 模型数量超限**

```json
{
  "detail": "最多只能选择 4 个模型"
}
```

**4. 模型不存在或未启用**

```json
{
  "detail": "模型 gpt-6 不存在"
}
```

**5. AI 服务异常**

```json
{
  "detail": "文本分析失败: API 调用超时"
}
```

### 前端错误处理建议

```typescript
try {
  const response = await fetch('/api/v1/ai/rewrite-arena/rewrite', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  });

  if (!response.ok) {
    const error = await response.json();

    switch (response.status) {
      case 401:
        // 跳转到登录页
        router.push('/login');
        break;
      case 400:
        // 显示参数错误提示
        showError(error.detail);
        break;
      case 500:
        // 显示服务器错误提示
        showError('服务暂时不可用，请稍后重试');
        break;
      default:
        showError(error.detail || '未知错误');
    }
    return;
  }

  const data = await response.json();
  // 处理成功响应

} catch (err) {
  // 网络错误
  showError('网络连接失败，请检查网络设置');
}
```

---

## 使用场景示例

### 场景 1：完整的改写流程

```typescript
// 1. 页面初始化 - 获取可用模型
const modelsResponse = await fetch('/api/v1/ai/rewrite-arena/models', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const modelsData = await modelsResponse.json();
console.log('可用模型:', modelsData.models);

// 2. 用户输入文本后 - 智能分析
const analyzeResponse = await fetch('/api/v1/ai/rewrite-arena/analyze', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: userInputText,
    context_before: contextBefore,
    context_after: contextAfter
  })
});
const analysisResult = await analyzeResponse.json();
console.log('分析结果:', analysisResult);
// 显示质量评分、问题列表、推荐模式

// 3. 用户确认模式后 - 多模型改写
const rewriteResponse = await fetch('/api/v1/ai/rewrite-arena/rewrite', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: userInputText,
    mode: analysisResult.recommended_mode, // 或用户选择的模式
    context_before: contextBefore,
    context_after: contextAfter,
    model_names: ['gemini-2.5-pro', 'gpt-5'] // 或使用默认
  })
});
const rewriteData = await rewriteResponse.json();
console.log('改写结果:', rewriteData.results);
// 并排展示多个模型的改写结果

// 4. 用户选择满意的版本后 - 保存记录
const selectedResult = rewriteData.results.find(r => r.model_name === 'gemini-2.5-pro');
const saveResponse = await fetch('/api/v1/rewrite-history/sessions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    original_text: rewriteData.original_text,
    mode: rewriteData.mode,
    context_before: contextBefore,
    context_after: contextAfter,
    results: rewriteData.results.map(r => ({
      ...r,
      is_selected: r.model_name === selectedResult.model_name
    }))
  })
});
const savedSession = await saveResponse.json();
console.log('保存成功:', savedSession.id);
```

### 场景 2：查看历史记录

```typescript
// 获取历史列表（第一页）
const listResponse = await fetch('/api/v1/rewrite-history/sessions?page=1&page_size=20', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const listData = await listResponse.json();
console.log('历史记录:', listData.sessions);
console.log('总记录数:', listData.total);

// 点击某条记录 - 查看详情
const sessionId = listData.sessions[0].id;
const detailResponse = await fetch(`/api/v1/rewrite-history/sessions/${sessionId}`, {
  headers: { 'Authorization': `Bearer ${token}` }
});
const sessionDetail = await detailResponse.json();
console.log('会话详情:', sessionDetail);
// 显示原文、改写模式、所有模型的结果
```

### 场景 3：自定义改写

```typescript
// 用户选择"自定义"模式并输入要求
const rewriteResponse = await fetch('/api/v1/ai/rewrite-arena/rewrite', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: "夕阳西下，天边的晚霞如同燃烧的火焰。",
    mode: "custom",
    custom_requirement: "改成第一人称视角，增加细腻的心理描写",
    model_names: ['gemini-2.5-pro', 'gpt-5']
  })
});
const data = await rewriteResponse.json();
console.log('自定义改写结果:', data.results);
```

---

## 性能建议

### 1. 并发控制

- **改写接口** 耗时较长（2-5秒），建议：
  - 显示加载动画和进度提示
  - 禁用重复提交（防止用户多次点击）
  - 设置合理的超时时间（建议 30 秒）

```typescript
// 示例：显示加载状态
setLoading(true);
setLoadingText('AI 正在改写中，请稍候...');
try {
  const response = await fetch('/api/v1/ai/rewrite-arena/rewrite', {
    method: 'POST',
    headers: { /* ... */ },
    body: JSON.stringify(requestData),
    signal: AbortSignal.timeout(30000) // 30秒超时
  });
  const data = await response.json();
  // 处理结果
} catch (err) {
  if (err.name === 'TimeoutError') {
    showError('请求超时，请重试');
  }
} finally {
  setLoading(false);
}
```

### 2. 缓存策略

- **模型列表** 变化频率低，建议：
  - 缓存到 LocalStorage
  - 设置 5 分钟有效期
  - 减少重复请求

```typescript
const CACHE_KEY = 'rewrite_models_cache';
const CACHE_DURATION = 5 * 60 * 1000; // 5分钟

function getCachedModels() {
  const cached = localStorage.getItem(CACHE_KEY);
  if (cached) {
    const { data, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp < CACHE_DURATION) {
      return data;
    }
  }
  return null;
}

async function getModels() {
  const cached = getCachedModels();
  if (cached) return cached;

  const response = await fetch('/api/v1/ai/rewrite-arena/models', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const data = await response.json();

  localStorage.setItem(CACHE_KEY, JSON.stringify({
    data,
    timestamp: Date.now()
  }));

  return data;
}
```

### 3. 分页加载

- **历史记录** 建议使用虚拟滚动或分页加载：
  - 首次加载 20 条
  - 滚动到底部时自动加载下一页
  - 显示总数和当前页码

```typescript
const [sessions, setSessions] = useState([]);
const [page, setPage] = useState(1);
const [hasMore, setHasMore] = useState(true);

async function loadMore() {
  const response = await fetch(
    `/api/v1/rewrite-history/sessions?page=${page}&page_size=20`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  const data = await response.json();

  setSessions([...sessions, ...data.sessions]);
  setPage(page + 1);
  setHasMore(sessions.length + data.sessions.length < data.total);
}
```

### 4. 错误重试

- 对于网络错误或临时性故障，建议实现自动重试机制：

```typescript
async function fetchWithRetry(url, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;

      // 如果是 5xx 错误且未达到最大重试次数，继续重试
      if (response.status >= 500 && i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1))); // 指数退避
        continue;
      }

      return response; // 返回响应（即使失败）
    } catch (err) {
      // 网络错误
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        continue;
      }
      throw err;
    }
  }
}
```

---

## 附录

### 上下文智能分级策略

后端会根据原文长度自动调整上下文范围：

| 原文长度 | 前文上下文 | 后文上下文 |
|---------|----------|----------|
| < 50 字 | 前 800 字 | 后 800 字 |
| < 200 字 | 前 500 字 | 后 500 字 |
| < 500 字 | 前 300 字 | 后 300 字 |
| ≥ 500 字 | 无上下文 | 无上下文 |

**前端建议：**
- 如果用户从编辑器选中文本，自动提取上下文
- 使用相同的分级逻辑计算提取范围
- 在 UI 上显示提示信息（如"已自动提取前后各 500 字作为上下文"）

### TypeScript 类型定义参考

完整的 TypeScript 类型定义文件可参考项目中的 `src/types/rewrite-arena.ts`（前端开发时创建）。

---

**文档版本：** v1.0
**最后更新：** 2025-10-26
**维护者：** 后端开发团队

如有疑问或发现问题，请联系后端开发团队或提交 Issue。
