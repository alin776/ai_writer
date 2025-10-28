# 后端已完成但前端未实现的API接口文档

> **文档最后更新**: 2025-01-28
> **目标**: 为前端开发提供完整的API接口清单
> **状态**: 后端100%完成,前端0%完成
> **优先级**: P0 (最高优先级)
> **实际API路由**: 所有API均已在backend/app/api/v1/目录下实现

---

## 📋 目录

1. [个人知识库系统 (7个接口)](#1-个人知识库系统) ⭐⭐⭐⭐⭐
2. [AI拆书功能 (8个接口)](#2-ai拆书功能) ⭐⭐⭐⭐
3. [AI改写助手/写作竞技场 (4个接口)](#3-ai改写助手写作竞技场) ⭐⭐⭐
4. [小说评审增强系统 (15个接口)](#4-小说评审增强系统) ⭐⭐⭐
5. [AI评估反馈系统 (1个接口)](#5-ai评估反馈系统) ⭐⭐
6. [去AI痕迹功能 (7个接口)](#6-去ai痕迹功能) ⭐⭐
7. [改写历史管理 (4个接口)](#7-改写历史管理) ⭐

**总计**: 46个API接口

---

## 🔥 P0级功能 - 核心差异化竞争力

## 1. 个人知识库系统

> **后端状态**: ✅ 100%完成 (2025-10-28)
> **战略意义**: 最强用户粘性功能
> **Base URL**: `/api/v1/knowledge`

### 1.1 创建知识条目

```http
POST /api/v1/knowledge
```

**请求头**:
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**请求体**:
```json
{
  "title": "金手指系统设计技巧",
  "content": "网文中的金手指系统需要满足三个核心要素：1. 独特性...",
  "summary": "关于金手指系统的设计要点",
  "category": "TECHNIQUE",
  "tags": ["金手指", "网文技巧", "系统流"],
  "source_type": "BOOK_ANALYSIS",
  "source_id": "uuid-of-book-job",
  "source_reference": "《全职法师》第1-30章分析",
  "work_id": "uuid-of-work",
  "chapter_id": "uuid-of-chapter",
  "extra_data": {
    "difficulty": "advanced",
    "genre": "玄幻"
  }
}
```

**请求参数说明**:
- `title` (string, 必填): 知识条目标题
- `content` (string, 必填): 详细内容
- `summary` (string, 可选): 摘要
- `category` (enum, 必填): 分类
  - `CHARACTER` - 人物设定
  - `WORLDVIEW` - 世界观
  - `PLOT` - 情节灵感
  - `DIALOGUE` - 对话金句
  - `DESCRIPTION` - 场景描写
  - `TECHNIQUE` - 写作技巧
  - `REFERENCE` - 参考资料
  - `OTHER` - 其他
- `tags` (array, 可选): 标签列表
- `source_type` (enum, 必填): 来源类型
  - `MANUAL` - 手动创建
  - `BOOK_ANALYSIS` - AI拆书
  - `AI_GENERATED` - AI生成
  - `IMPORTED` - 导入
- `source_id` (string, 可选): 来源ID
- `source_reference` (string, 可选): 来源说明
- `work_id` (uuid, 可选): 关联作品ID
- `chapter_id` (uuid, 可选): 关联章节ID
- `extra_data` (object, 可选): 扩展数据

**响应** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-uuid",
  "title": "金手指系统设计技巧",
  "content": "网文中的金手指系统需要满足三个核心要素：1. 独特性...",
  "summary": "关于金手指系统的设计要点",
  "category": "TECHNIQUE",
  "tags": ["金手指", "网文技巧", "系统流"],
  "source_type": "BOOK_ANALYSIS",
  "source_id": "uuid-of-book-job",
  "source_reference": "《全职法师》第1-30章分析",
  "work_id": "uuid-of-work",
  "chapter_id": "uuid-of-chapter",
  "view_count": 0,
  "reference_count": 0,
  "extra_data": {
    "difficulty": "advanced",
    "genre": "玄幻"
  },
  "created_at": "2025-10-28T10:00:00Z",
  "updated_at": "2025-10-28T10:00:00Z",
  "last_accessed_at": null
}
```

---

### 1.2 获取知识条目列表

```http
GET /api/v1/knowledge?skip=0&limit=20&category=TECHNIQUE&tags=金手指,系统流&work_id=xxx&search=金手指
```

**查询参数**:
- `skip` (int, 默认0): 跳过数量
- `limit` (int, 默认20, 最大100): 每页大小
- `category` (enum, 可选): 分类过滤
- `tags` (string, 可选): 标签过滤(逗号分隔)
- `work_id` (uuid, 可选): 作品ID过滤
- `search` (string, 可选): 搜索关键词

**响应** (200 OK):
```json
{
  "total": 150,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": "uuid1",
      "title": "金手指系统设计技巧",
      "summary": "关于金手指系统的设计要点",
      "category": "TECHNIQUE",
      "tags": ["金手指", "网文技巧"],
      "source_type": "BOOK_ANALYSIS",
      "view_count": 5,
      "reference_count": 2,
      "created_at": "2025-10-28T10:00:00Z"
    }
  ]
}
```

---

### 1.3 获取知识条目详情

```http
GET /api/v1/knowledge/{item_id}
```

**路径参数**:
- `item_id` (uuid): 知识条目ID

**响应** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-uuid",
  "title": "金手指系统设计技巧",
  "content": "详细内容...",
  "summary": "摘要",
  "category": "TECHNIQUE",
  "tags": ["金手指"],
  "source_type": "BOOK_ANALYSIS",
  "view_count": 6,
  "reference_count": 2,
  "created_at": "2025-10-28T10:00:00Z",
  "updated_at": "2025-10-28T10:00:00Z",
  "last_accessed_at": "2025-10-28T11:00:00Z"
}
```

**说明**:
- 调用此接口会自动增加 `view_count` 和更新 `last_accessed_at`

---

### 1.4 更新知识条目

```http
PUT /api/v1/knowledge/{item_id}
```

**请求体**:
```json
{
  "title": "金手指系统设计技巧 (修订版)",
  "content": "更新后的内容...",
  "tags": ["金手指", "网文技巧", "新增标签"]
}
```

**响应** (200 OK): 同创建响应

---

### 1.5 删除知识条目

```http
DELETE /api/v1/knowledge/{item_id}
```

**响应** (204 No Content)

**说明**:
- 删除知识条目时会自动删除关联的向量数据

---

### 1.6 语义搜索 (RAG)

```http
POST /api/v1/knowledge/search
```

**请求体**:
```json
{
  "query": "如何设计一个有吸引力的金手指系统?",
  "top_k": 10,
  "threshold": 0.3,
  "category": "TECHNIQUE",
  "tags": ["金手指"]
}
```

**请求参数**:
- `query` (string, 必填): 搜索查询
- `top_k` (int, 默认10): 返回结果数量
- `threshold` (float, 默认0.3): 相似度阈值 (0-1)
- `category` (enum, 可选): 分类过滤
- `tags` (array, 可选): 标签过滤

**响应** (200 OK):
```json
{
  "query": "如何设计一个有吸引力的金手指系统?",
  "results": [
    {
      "item": {
        "id": "uuid1",
        "title": "金手指系统设计技巧",
        "content": "详细内容...",
        "category": "TECHNIQUE",
        "tags": ["金手指", "网文技巧"]
      },
      "similarity_score": 0.85,
      "highlight": "...核心要素：1. 独特性 2. 成长性 3. 限制性..."
    },
    {
      "item": {
        "id": "uuid2",
        "title": "系统流小说分析",
        "content": "...",
        "category": "REFERENCE"
      },
      "similarity_score": 0.72,
      "highlight": "...金手指的平衡性设计..."
    }
  ],
  "total": 2
}
```

**技术说明**:
- 使用向量相似度搜索 (Sentence-BERT)
- 支持中文语义理解
- 自动提取关键片段高亮

---

### 1.7 增加引用次数

```http
POST /api/v1/knowledge/{item_id}/reference
```

**用途**: 当用户在编辑器中引用某个知识条目时调用

**响应** (200 OK):
```json
{
  "item_id": "uuid",
  "reference_count": 3
}
```

---

## 2. AI拆书功能

> **后端状态**: ✅ 100%完成 (2025-01-27)
> **差异化优势**: 市场首个网文11维度分析系统
> **Base URL**: `/api/v1/books` (实际路由在 `backend/app/api/v1/endpoints/books.py`)
> **注意**: 此API路由在endpoints子目录下

### 2.1 上传图书并启动分析

```http
POST /api/v1/books/upload
```

**请求类型**: `multipart/form-data`

**表单字段**:
```
file: [文件] (必填)
book_title: "全职法师" (可选,默认使用文件名)
strategy_id: "web_novel_11d" (必填)
work_id: "uuid-of-work" (可选)
```

**支持的文件格式**:
- `.txt` (已实现)
- `.epub` (待实现)
- `.pdf` (待实现)

**文件大小限制**: 50MB

**响应** (200 OK):
```json
{
  "id": "job-uuid",
  "user_id": "user-uuid",
  "book_title": "全职法师",
  "original_filename": "全职法师.txt",
  "file_format": "txt",
  "file_size_bytes": 1024000,
  "file_hash": "sha256-hash",
  "status": "pending",
  "progress": 0,
  "current_step": "等待开始分析...",
  "total_chapters": 0,
  "analyzed_chapters": 0,
  "extracted_items_count": 0,
  "strategy_id": "web_novel_11d",
  "work_id": "uuid-of-work",
  "error_message": null,
  "retry_count": 0,
  "created_at": "2025-10-28T10:00:00Z",
  "started_at": null,
  "completed_at": null
}
```

**任务状态说明**:
- `pending` - 等待开始
- `parsing` - 解析文件中
- `analyzing` - 分析中
- `completed` - 已完成
- `failed` - 失败

---

### 2.2 查询任务详情

```http
GET /api/v1/books/jobs/{job_id}
```

**响应** (200 OK):
```json
{
  "id": "job-uuid",
  "user_id": "user-uuid",
  "book_title": "全职法师",
  "status": "analyzing",
  "progress": 45,
  "current_step": "正在分析第35章...",
  "total_chapters": 150,
  "analyzed_chapters": 68,
  "extracted_items_count": 11,
  "created_at": "2025-10-28T10:00:00Z",
  "started_at": "2025-10-28T10:01:00Z",
  "completed_at": null
}
```

---

### 2.3 查询任务状态 (轻量级)

```http
GET /api/v1/books/jobs/{job_id}/status
```

**用途**: 用于前端轮询,只返回核心状态字段

**响应** (200 OK):
```json
{
  "id": "job-uuid",
  "status": "analyzing",
  "progress": 45,
  "current_step": "正在分析第35章..."
}
```

**前端轮询建议**:
- 轮询间隔: 2-3秒
- 最大轮询次数: 600次 (30分钟)
- 超时后提示用户刷新

---

### 2.4 获取任务列表

```http
GET /api/v1/books/jobs?page=1&page_size=20&status=completed
```

**查询参数**:
- `page` (int, 默认1): 页码
- `page_size` (int, 默认20): 每页大小
- `status` (enum, 可选): 状态过滤

**响应** (200 OK):
```json
{
  "jobs": [
    {
      "id": "job1",
      "book_title": "全职法师",
      "status": "completed",
      "progress": 100,
      "total_chapters": 150,
      "extracted_items_count": 11,
      "created_at": "2025-10-28T10:00:00Z",
      "completed_at": "2025-10-28T10:15:00Z"
    }
  ],
  "total": 5,
  "page": 1,
  "page_size": 20
}
```

---

### 2.5 删除任务

```http
DELETE /api/v1/books/jobs/{job_id}
```

**响应** (204 No Content)

---

### 2.6 获取智能建议列表

```http
GET /api/v1/books/jobs/{job_id}/suggestions
```

**响应** (200 OK):
```json
{
  "suggestions": [
    {
      "id": "suggestion1",
      "job_id": "job-uuid",
      "suggestion_type": "character",
      "action": "create_new",
      "suggested_data": {
        "name": "莫凡",
        "description": "主角,拥有雷火双系金手指",
        "attributes": {
          "age": "17",
          "初始能力": "觉醒雷系+火系"
        }
      },
      "confidence_score": 0.95,
      "reason": "主角设定明确,出场频率高,核心角色",
      "status": "pending",
      "created_at": "2025-10-28T10:15:00Z"
    },
    {
      "id": "suggestion2",
      "suggestion_type": "power_system",
      "action": "create_new",
      "suggested_data": {
        "name": "魔法等级体系",
        "description": "初阶-中阶-高阶-超阶-禁咒",
        "attributes": {
          "系统类型": "魔法修炼",
          "等级数量": "5"
        }
      },
      "confidence_score": 0.88,
      "reason": "完整的力量体系,是作品核心设定",
      "status": "pending"
    }
  ],
  "total": 6,
  "by_type": {
    "character": 2,
    "power_system": 2,
    "setting": 1,
    "relationship": 1
  }
}
```

**建议类型说明**:
- `character` - 角色建议
- `power_system` - 力量体系建议
- `setting` - 设定建议
- `location` - 地点建议
- `item` - 物品建议
- `relationship` - 关系建议

---

### 2.7 批量采纳建议

```http
POST /api/v1/books/jobs/{job_id}/adopt
```

**请求体**:
```json
{
  "suggestion_ids": [
    "suggestion1",
    "suggestion2",
    "suggestion3"
  ],
  "target_work_id": "work-uuid"
}
```

**响应** (200 OK):
```json
{
  "adopted_count": 3,
  "failed_count": 0,
  "results": [
    {
      "suggestion_id": "suggestion1",
      "success": true,
      "created_entity_id": "character-uuid",
      "entity_type": "character"
    },
    {
      "suggestion_id": "suggestion2",
      "success": true,
      "created_entity_id": "power-system-uuid",
      "entity_type": "setting"
    },
    {
      "suggestion_id": "suggestion3",
      "success": true,
      "created_entity_id": "location-uuid",
      "entity_type": "location"
    }
  ]
}
```

---

### 2.8 修改单个建议

```http
PATCH /api/v1/books/suggestions/{suggestion_id}
```

**请求体**:
```json
{
  "suggested_data": {
    "name": "莫凡 (修改后)",
    "description": "更新后的描述..."
  },
  "status": "adopted"
}
```

**响应** (200 OK): 返回更新后的建议对象

---

## 3. AI改写助手/写作竞技场

> **后端状态**: ✅ 100%完成 (2025-01-26)
> **营销卖点**: "6个顶级AI同时为你改写"
> **Base URL**: `/api/v1/ai/rewrite-arena`
> **实际实现**: 在 `backend/app/api/v1/ai.py` 中实现

### 3.1 获取可用模型列表

```http
GET /api/v1/ai/rewrite-arena/models
```

**响应** (200 OK):
```json
{
  "models": [
    {
      "id": "gemini-2.5-pro",
      "name": "Gemini 2.5 Pro",
      "provider": "Google",
      "description": "Google最新旗舰模型",
      "speed": "fast",
      "quality": "high",
      "cost_per_1k_tokens": 0.01,
      "available": true
    },
    {
      "id": "gpt-4o",
      "name": "GPT-4o",
      "provider": "OpenAI",
      "description": "OpenAI多模态模型",
      "speed": "fast",
      "quality": "very_high",
      "available": true
    },
    {
      "id": "claude-3.5-sonnet",
      "name": "Claude 3.5 Sonnet",
      "provider": "Anthropic",
      "description": "Claude最新版本",
      "speed": "medium",
      "quality": "very_high",
      "available": true
    },
    {
      "id": "qwen-max",
      "name": "通义千问 Max",
      "provider": "Alibaba",
      "description": "阿里云最强大模型",
      "speed": "fast",
      "quality": "high",
      "available": true
    }
  ]
}
```

---

### 3.2 智能分析文本

```http
POST /api/v1/ai/rewrite-arena/analyze
```

**请求体**:
```json
{
  "text": "林羽看着眼前的景象，心中暗暗震惊。",
  "context_before": "...",
  "context_after": "..."
}
```

**响应** (200 OK):
```json
{
  "analysis": {
    "text_length": 18,
    "word_count": 18,
    "sentence_count": 1,
    "detected_issues": [
      {
        "type": "cliche",
        "description": "使用了常见的网文套路短语",
        "examples": ["心中暗暗震惊"]
      },
      {
        "type": "weak_verb",
        "description": "动词缺乏力量感",
        "examples": ["看着"]
      }
    ],
    "suggestions": [
      "增强动作描写的画面感",
      "避免使用'心中暗暗'等套路短语",
      "补充环境细节描写"
    ],
    "estimated_rewrite_time": 15
  }
}
```

---

### 3.3 多模型并发改写

```http
POST /api/v1/ai/rewrite-arena/rewrite
```

**请求体**:
```json
{
  "original_text": "林羽看着眼前的景象，心中暗暗震惊。",
  "context_before": "...",
  "context_after": "...",
  "mode": "enhance",
  "custom_requirement": "增强画面感,减少套路",
  "selected_models": [
    "gemini-2.5-pro",
    "gpt-4o",
    "claude-3.5-sonnet",
    "qwen-max"
  ]
}
```

**请求参数**:
- `original_text` (string, 必填): 原文
- `context_before` (string, 可选): 前文上下文
- `context_after` (string, 可选): 后文上下文
- `mode` (enum, 必填): 改写模式
  - `enhance` - 增强表达
  - `simplify` - 简化文字
  - `formal` - 正式化
  - `creative` - 创意改写
  - `custom` - 自定义
- `custom_requirement` (string, 可选): 自定义要求
- `selected_models` (array, 必填): 选择的模型列表

**响应** (200 OK):
```json
{
  "session_id": "session-uuid",
  "original_text": "林羽看着眼前的景象，心中暗暗震惊。",
  "mode": "enhance",
  "results": [
    {
      "model_id": "gemini-2.5-pro",
      "model_name": "Gemini 2.5 Pro",
      "rewritten_text": "林羽抬眸望去，瞳孔骤然一缩——眼前的景象，远超他的预料。",
      "word_count": 23,
      "elapsed_time": 3.2,
      "quality_score": 85,
      "improvements": [
        "增强了动作细节",
        "避免了套路短语",
        "提升了画面感"
      ],
      "error": null,
      "status": "success"
    },
    {
      "model_id": "gpt-4o",
      "model_name": "GPT-4o",
      "rewritten_text": "林羽凝视眼前，内心翻涌，难以置信。",
      "word_count": 15,
      "elapsed_time": 2.8,
      "quality_score": 78,
      "status": "success"
    },
    {
      "model_id": "claude-3.5-sonnet",
      "model_name": "Claude 3.5 Sonnet",
      "rewritten_text": "当林羽的目光落在眼前的景象时，他屏住了呼吸。",
      "word_count": 20,
      "elapsed_time": 3.5,
      "quality_score": 82,
      "status": "success"
    },
    {
      "model_id": "qwen-max",
      "model_name": "通义千问 Max",
      "rewritten_text": "林羽瞪大了双眼，这一幕完全超出了他的预期。",
      "word_count": 18,
      "elapsed_time": 2.5,
      "quality_score": 80,
      "status": "success"
    }
  ],
  "statistics": {
    "total_models": 4,
    "successful": 4,
    "failed": 0,
    "average_time": 3.0,
    "average_quality_score": 81.25
  },
  "created_at": "2025-10-28T10:00:00Z"
}
```

**技术说明**:
- 使用 `asyncio.gather` 并发调用4-6个模型
- 单个模型失败不影响其他模型
- 总耗时 = max(单个模型耗时) ≈ 3-5秒

---

### 3.4 保存改写会话 (已在3.3中自动保存)

改写会话会自动保存到 `rewrite_history` 表,无需单独调用保存接口。

---

## 4. 小说评审增强系统

> **后端状态**: ✅ 100%完成 (2025-01-26)
> **功能价值**: 专业的小说质量评审系统
> **Base URL**: `/api/v1/review`
> **实际实现**: 在 `backend/app/api/v1/review.py` 中实现

### 4.1 发起章节评审

```http
POST /api/v1/review/chapters/{chapter_id}/review
```

**请求体**:
```json
{
  "review_type": "standard",
  "auto_generate_tasks": true,
  "create_version": true,
  "custom_requirements": "重点关注节奏和人物塑造"
}
```

**请求参数**:
- `review_type` (enum, 必填): 评审深度
  - `quick` - 快速评审 (4维度)
  - `standard` - 标准评审 (8维度)
  - `deep` - 深度评审 (10维度)
- `auto_generate_tasks` (bool, 默认true): 是否自动生成任务
- `create_version` (bool, 默认true): 是否创建版本快照
- `custom_requirements` (string, 可选): 自定义要求

**响应** (200 OK):
```json
{
  "session": {
    "id": "session-uuid",
    "chapter_id": "chapter-uuid",
    "user_id": "user-uuid",
    "review_type": "standard",
    "overall_score": 82,
    "dimensions": [
      {
        "name": "文学性",
        "score": 85,
        "description": "语言质量、修辞手法",
        "strengths": ["词汇丰富", "意象生动"],
        "issues": ["部分句子过长"]
      },
      {
        "name": "情节合理性",
        "score": 80,
        "strengths": ["逻辑自洽"],
        "issues": ["转折略显突兀"]
      },
      {
        "name": "人物塑造",
        "score": 78,
        "strengths": ["主角性格鲜明"],
        "issues": ["配角刻画不足"]
      },
      {
        "name": "节奏把控",
        "score": 85,
        "strengths": ["快慢得当"],
        "issues": []
      },
      {
        "name": "场景描写",
        "score": 82
      },
      {
        "name": "情感感染力",
        "score": 80
      },
      {
        "name": "伏笔铺垫",
        "score": 88
      },
      {
        "name": "创意性",
        "score": 75
      }
    ],
    "detailed_feedback": "整体来看,本章节质量较高...",
    "key_issues": [
      "部分句子过长,影响阅读流畅度",
      "配角刻画不足,存在工具人倾向",
      "情节转折略显突兀,需要更多铺垫"
    ],
    "created_at": "2025-10-28T10:00:00Z"
  },
  "generated_tasks": [
    {
      "id": "task1",
      "title": "简化长句",
      "description": "将第3段的长句拆分,提升可读性",
      "priority": "P1",
      "estimated_time": 10,
      "location": "第3段",
      "status": "pending"
    },
    {
      "id": "task2",
      "title": "丰富配角描写",
      "description": "为张三增加性格细节描写",
      "priority": "P2",
      "estimated_time": 20,
      "location": "第5段",
      "status": "pending"
    }
  ],
  "version": {
    "id": "version-uuid",
    "chapter_id": "chapter-uuid",
    "version_number": 3,
    "is_milestone": false,
    "version_tag": "评审后版本",
    "change_summary": "评审总分: 82",
    "created_at": "2025-10-28T10:00:00Z"
  }
}
```

**8维度评审标准**:
1. **文学性** - 语言质量、修辞手法
2. **情节合理性** - 逻辑自洽、因果关系
3. **人物塑造** - 角色刻画深度
4. **节奏把控** - 快慢得当、张弛有度
5. **场景描写** - 画面感、代入感
6. **情感感染力** - 共鸣度
7. **伏笔铺垫** - 悬念设置
8. **创意性** - 新颖度、想象力

---

### 4.2 获取评审结果

```http
GET /api/v1/review/sessions/{session_id}
```

**响应** (200 OK): 同4.1的session对象

---

### 4.3 获取章节评审历史

```http
GET /api/v1/review/chapters/{chapter_id}/review-history
```

**响应** (200 OK):
```json
[
  {
    "id": "session1",
    "review_type": "standard",
    "overall_score": 82,
    "created_at": "2025-10-28T10:00:00Z"
  },
  {
    "id": "session2",
    "review_type": "quick",
    "overall_score": 78,
    "created_at": "2025-10-27T15:00:00Z"
  }
]
```

---

### 4.4 获取章节任务列表

```http
GET /api/v1/review/chapters/{chapter_id}/tasks?status=pending&priority=P1
```

**查询参数**:
- `status` (enum, 可选): 任务状态过滤
  - `pending` - 待处理
  - `in_progress` - 进行中
  - `completed` - 已完成
  - `skipped` - 已跳过
- `priority` (enum, 可选): 优先级过滤
  - `P0` - 最高优先级
  - `P1` - 高优先级
  - `P2` - 中优先级
  - `P3` - 低优先级

**响应** (200 OK):
```json
{
  "tasks": [
    {
      "id": "task1",
      "title": "简化长句",
      "description": "将第3段的长句拆分",
      "priority": "P1",
      "status": "pending",
      "estimated_time": 10,
      "location": "第3段",
      "created_at": "2025-10-28T10:00:00Z"
    }
  ],
  "total": 5,
  "stats": {
    "pending": 3,
    "in_progress": 1,
    "completed": 1,
    "skipped": 0
  }
}
```

---

### 4.5 创建任务

```http
POST /api/v1/review/tasks
```

**请求体**:
```json
{
  "chapter_id": "chapter-uuid",
  "review_session_id": "session-uuid",
  "title": "修改开头",
  "description": "开头需要更吸引人",
  "priority": "P0",
  "estimated_time": 30,
  "location": "第1段"
}
```

**响应** (201 Created): 返回创建的任务对象

---

### 4.6 更新任务

```http
PATCH /api/v1/review/tasks/{task_id}
```

**请求体**:
```json
{
  "title": "修改开头 (已调整)",
  "description": "...",
  "priority": "P1",
  "status": "completed"
}
```

**响应** (200 OK): 返回更新后的任务对象

---

### 4.7 更新任务状态

```http
PATCH /api/v1/review/tasks/{task_id}/status
```

**请求体**:
```json
{
  "status": "completed",
  "completion_notes": "已完成修改,效果不错"
}
```

**响应** (200 OK): 返回更新后的任务对象

---

### 4.8 批量操作任务

```http
POST /api/v1/review/tasks/batch-operations
```

**请求体**:
```json
{
  "task_ids": ["task1", "task2", "task3"],
  "operation": "complete",
  "data": {
    "completion_notes": "批量完成"
  }
}
```

**支持的操作**:
- `complete` - 完成
- `skip` - 跳过
- `delete` - 删除
- `change_priority` - 修改优先级

**响应** (200 OK):
```json
{
  "success_count": 3,
  "failed_count": 0,
  "results": [
    {
      "task_id": "task1",
      "success": true
    }
  ]
}
```

---

### 4.9 删除任务

```http
DELETE /api/v1/review/tasks/{task_id}
```

**响应** (204 No Content)

---

### 4.10 获取任务统计

```http
GET /api/v1/review/tasks/stats?chapter_id={chapter_id}
```

**响应** (200 OK):
```json
{
  "total_tasks": 10,
  "pending": 5,
  "in_progress": 2,
  "completed": 3,
  "skipped": 0,
  "by_priority": {
    "P0": 2,
    "P1": 4,
    "P2": 3,
    "P3": 1
  },
  "completion_rate": 0.3,
  "average_completion_time": 25
}
```

---

### 4.11 创建章节版本

```http
POST /api/v1/review/chapters/{chapter_id}/versions
```

**请求体**:
```json
{
  "is_milestone": true,
  "version_tag": "第一次大改完成",
  "change_summary": "修复了所有P0和P1任务",
  "review_session_id": "session-uuid"
}
```

**响应** (201 Created):
```json
{
  "id": "version-uuid",
  "chapter_id": "chapter-uuid",
  "user_id": "user-uuid",
  "version_number": 5,
  "is_milestone": true,
  "version_tag": "第一次大改完成",
  "change_summary": "修复了所有P0和P1任务",
  "content_snapshot": "章节完整内容...",
  "word_count": 3500,
  "review_score": 85,
  "created_at": "2025-10-28T10:00:00Z"
}
```

---

### 4.12 获取章节版本列表

```http
GET /api/v1/review/chapters/{chapter_id}/versions?milestones_only=true
```

**查询参数**:
- `milestones_only` (bool, 默认false): 只返回里程碑版本

**响应** (200 OK):
```json
{
  "versions": [
    {
      "id": "version1",
      "version_number": 5,
      "is_milestone": true,
      "version_tag": "第一次大改完成",
      "review_score": 85,
      "created_at": "2025-10-28T10:00:00Z"
    },
    {
      "id": "version2",
      "version_number": 3,
      "is_milestone": true,
      "version_tag": "初稿完成",
      "review_score": 72,
      "created_at": "2025-10-27T10:00:00Z"
    }
  ],
  "total": 2
}
```

---

### 4.13 获取版本详情

```http
GET /api/v1/review/versions/{version_id}
```

**响应** (200 OK):
```json
{
  "id": "version-uuid",
  "chapter_id": "chapter-uuid",
  "version_number": 5,
  "is_milestone": true,
  "version_tag": "第一次大改完成",
  "change_summary": "修复了所有P0和P1任务",
  "content_snapshot": "章节完整内容...",
  "word_count": 3500,
  "review_score": 85,
  "diff_from_previous": {
    "added_lines": 12,
    "removed_lines": 8,
    "modified_lines": 15
  },
  "created_at": "2025-10-28T10:00:00Z"
}
```

---

### 4.14 标记为里程碑版本

```http
PATCH /api/v1/review/versions/{version_id}/milestone
```

**请求体**:
```json
{
  "is_milestone": true,
  "version_tag": "大改完成版"
}
```

**响应** (200 OK): 返回更新后的版本对象

---

### 4.15 版本对比

```http
GET /api/v1/review/versions/compare?version_a={version_id_1}&version_b={version_id_2}
```

**响应** (200 OK):
```json
{
  "version_a": {
    "id": "version1",
    "version_number": 3,
    "word_count": 3200,
    "review_score": 72
  },
  "version_b": {
    "id": "version2",
    "version_number": 5,
    "word_count": 3500,
    "review_score": 85
  },
  "comparison": {
    "word_count_diff": 300,
    "score_diff": 13,
    "improvement_rate": 0.18,
    "diff_html": "<p>章节内容diff...</p>"
  }
}
```

---

## 5. AI评估反馈系统

> **后端状态**: ✅ 100%完成 (2025-01-26)
> **功能价值**: 5维度AI内容质量评价
> **Base URL**: `/api/v1/ai`
> **实际实现**: 在 `backend/app/api/v1/ai.py` 中实现 (evaluate接口)

### 5.1 评估AI生成内容

```http
POST /api/v1/ai/evaluate
```

**请求体**:
```json
{
  "text": "AI生成的文本内容...",
  "context": "上下文环境",
  "operation_type": "continue",
  "work_id": "work-uuid",
  "chapter_id": "chapter-uuid"
}
```

**请求参数**:
- `text` (string, 必填): 待评估的文本
- `context` (string, 可选): 上下文
- `operation_type` (enum, 必填): 操作类型
  - `continue` - 续写
  - `polish` - 润色
  - `expand` - 扩写
  - `translate` - 翻译
  - `summarize` - 总结
- `work_id` (uuid, 可选): 作品ID
- `chapter_id` (uuid, 可选): 章节ID

**响应** (200 OK):
```json
{
  "evaluation_id": "eval-uuid",
  "overall_score": 82,
  "dimensions": [
    {
      "name": "文学性",
      "score": 85,
      "description": "语言质量、修辞手法",
      "max_score": 100
    },
    {
      "name": "连贯性",
      "score": 80,
      "description": "上下文衔接、逻辑流畅",
      "max_score": 100
    },
    {
      "name": "创意性",
      "score": 75,
      "description": "新颖度、想象力",
      "max_score": 100
    },
    {
      "name": "情感感染力",
      "score": 88,
      "description": "感染力、共鸣度",
      "max_score": 100
    },
    {
      "name": "节奏把控",
      "score": 82,
      "description": "快慢适度、张弛有度",
      "max_score": 100
    }
  ],
  "strengths": [
    "语言流畅,词汇丰富",
    "情感表达细腻,有感染力",
    "节奏把控得当"
  ],
  "weaknesses": [
    "创意性略显不足,存在套路化倾向",
    "部分转折略显突兀"
  ],
  "suggestions": [
    "可以增加一些独特的比喻或意象",
    "在情节转折处增加铺垫",
    "避免使用过于常见的网文套路"
  ],
  "created_at": "2025-10-28T10:00:00Z"
}
```

**5维度评价标准**:
1. **文学性** (0-100) - 语言质量、修辞手法
2. **连贯性** (0-100) - 上下文衔接、逻辑流畅
3. **创意性** (0-100) - 新颖度、想象力
4. **情感感染力** (0-100) - 感染力、共鸣度
5. **节奏把控** (0-100) - 快慢适度、张弛有度

---

## 6. 去AI痕迹功能

> **后端状态**: ✅ 100%完成 (2025-01-28)
> **功能价值**: 检测并去除AI生成文本的机器痕迹
> **Base URL**: `/api/v1/humanize`
> **实际实现**: 在 `backend/app/api/v1/humanize.py` 中完整实现

### 6.1 获取用户画像

```http
GET /api/v1/humanize/profile
```

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

### 6.2 更新用户设置

```http
PUT /api/v1/humanize/profile/settings
```

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

### 6.3 获取历史记录

```http
GET /api/v1/humanize/history?page=1&page_size=20
```

**响应** (200 OK):
```json
{
  "sessions": [
    {
      "id": "session1",
      "original_text_preview": "林羽看着眼前的景象...",
      "humanized_text_preview": "林羽抬眸望去...",
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

### 6.4 获取单个会话详情

```http
GET /api/v1/humanize/history/{session_id}
```

**响应** (200 OK):
```json
{
  "id": "session-uuid",
  "user_id": "user-uuid",
  "original_text": "完整原文...",
  "humanized_text": "完整去痕迹后文本...",
  "intensity": "medium",
  "overall_score_before": 77.0,
  "overall_score_after": 45.0,
  "improvement_rate": 0.42,
  "dimensions_before": {
    "structure": {"score": 80, "issues": ["结构过于规整"]},
    "language": {"score": 75, "issues": ["书面语过多"]}
  },
  "dimensions_after": {
    "structure": {"score": 50, "issues": []},
    "language": {"score": 40, "issues": []}
  },
  "detected_patterns": ["首先...其次...最后...", "综上所述"],
  "user_feedback": "accepted",
  "created_at": "2025-10-28T10:00:00Z"
}
```

---

### 6.5 获取统计数据

```http
GET /api/v1/humanize/stats
```

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

### 6.6 提交用户反馈

```http
POST /api/v1/humanize/feedback
```

**请求体**:
```json
{
  "session_id": "session-uuid",
  "feedback": "accepted",
  "comments": "效果很好"
}
```

**feedback枚举**:
- `accepted` - 采纳
- `rejected` - 拒绝
- `partial` - 部分采纳

**响应** (200 OK):
```json
{
  "success": true,
  "message": "反馈已记录"
}
```

---

### 6.7 去痕迹改写

```http
POST /api/v1/humanize/rewrite
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
- `text` (string, 必填): 待去痕迹的文本
- `intensity` (enum, 默认medium): 去痕迹强度
  - `light` - 轻度 (保守)
  - `medium` - 中度 (平衡)
  - `strong` - 强度 (激进)
- `function_type` (enum, 必填): 功能类型 (continue/polish/expand)
- `enable_detection` (bool, 默认true): 是否检测AI痕迹
- `enable_validation` (bool, 默认false): 是否验证改写结果

**响应** (200 OK):
```json
{
  "session_id": "session-uuid",
  "original_text": "首先,我们需要...",
  "humanized_text": "我们先分析一下这个问题...",
  "intensity": "medium",
  "overall_score_before": 77.0,
  "overall_score_after": 45.0,
  "improvement_rate": 0.42,
  "detected_patterns": ["首先...其次..."],
  "processing_time": 8.5,
  "created_at": "2025-10-28T10:00:00Z"
}
```

**✅ 技术说明**:
- 使用三阶段处理引擎: 检测(gemini-2.5-flash-lite) → 改写(标准模型) → 验证(快速模型,可选)
- 双AI架构: 快速模型用于检测/验证,标准模型用于高质量改写
- 支持流式输出,实时显示改写进度
- 自动保存到humanize_sessions表和AI日志系统

**⚡ 性能指标**:
- 检测阶段: ~3-5秒
- 改写阶段: ~5-10秒 (流式输出)
- 验证阶段: ~3-5秒 (可选)
- 总耗时: ~10-20秒 (含验证)
- 成本: ~$0.002-0.005/次

---

## 7. 改写历史管理

> **后端状态**: ✅ 100%完成
> **功能价值**: 管理AI改写助手的历史会话
> **Base URL**: `/api/v1/rewrite-history`
> **实际实现**: 在 `backend/app/api/v1/rewrite_history.py` 中实现

### 7.1 保存改写会话

```http
POST /api/v1/rewrite-history
```

**请求体**:
```json
{
  "original_text": "原文内容...",
  "context_before": "...",
  "context_after": "...",
  "mode": "enhance",
  "custom_requirement": "增强画面感",
  "results": [
    {
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "改写后内容...",
      "word_count": 23,
      "elapsed_time": 3.2,
      "error": null,
      "is_selected": true
    }
  ]
}
```

**响应** (201 Created):
```json
{
  "id": "session-uuid",
  "user_id": "user-uuid",
  "original_text": "原文内容...",
  "mode": "enhance",
  "created_at": "2025-10-28T10:00:00Z",
  "results": [
    {
      "id": "result1",
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "改写后内容...",
      "word_count": 23,
      "elapsed_time": 3.2,
      "is_selected": true,
      "created_at": "2025-10-28T10:00:00Z"
    }
  ]
}
```

---

### 7.2 获取改写历史列表

```http
GET /api/v1/rewrite-history?page=1&page_size=20
```

**响应** (200 OK):
```json
{
  "sessions": [
    {
      "id": "session1",
      "original_text": "林羽看着眼前的景象...(前50字)",
      "mode": "enhance",
      "result_count": 4,
      "created_at": "2025-10-28T10:00:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "page_size": 20
}
```

---

### 7.3 获取会话详情

```http
GET /api/v1/rewrite-history/{session_id}
```

**响应** (200 OK):
```json
{
  "id": "session-uuid",
  "user_id": "user-uuid",
  "original_text": "完整原文...",
  "context_before": "...",
  "context_after": "...",
  "mode": "enhance",
  "custom_requirement": "增强画面感",
  "created_at": "2025-10-28T10:00:00Z",
  "results": [
    {
      "id": "result1",
      "model_name": "gemini-2.5-pro",
      "rewritten_text": "完整改写后内容...",
      "word_count": 23,
      "elapsed_time": 3.2,
      "error": null,
      "is_selected": true,
      "created_at": "2025-10-28T10:00:00Z"
    },
    {
      "id": "result2",
      "model_name": "gpt-4o",
      "rewritten_text": "...",
      "word_count": 18,
      "elapsed_time": 2.8,
      "is_selected": false
    }
  ]
}
```

---

### 7.4 删除改写会话

```http
DELETE /api/v1/rewrite-history/{session_id}
```

**响应** (204 No Content)

---

## 📋 前端开发检查清单

### DataService接口扩展

需要在 `src/services/DataService.ts` 中新增以下方法:

#### 知识库 (7个方法)
```typescript
async createKnowledgeItem(data: KnowledgeItemCreate): Promise<KnowledgeItem>
async getKnowledgeItems(filters?: KnowledgeFilters): Promise<KnowledgeItemList>
async getKnowledgeItem(id: string): Promise<KnowledgeItem>
async updateKnowledgeItem(id: string, data: KnowledgeItemUpdate): Promise<KnowledgeItem>
async deleteKnowledgeItem(id: string): Promise<void>
async searchKnowledge(query: KnowledgeSearchRequest): Promise<KnowledgeSearchResponse>
async incrementKnowledgeReference(id: string): Promise<void>
```

#### AI拆书 (8个方法)
```typescript
async uploadBook(file: File, options: BookUploadOptions): Promise<BookAnalysisJob>
async getBookJob(jobId: string): Promise<BookAnalysisJob>
async getBookJobStatus(jobId: string): Promise<BookAnalysisJobStatus>
async getBookJobs(filters?: BookJobFilters): Promise<BookAnalysisJobList>
async deleteBookJob(jobId: string): Promise<void>
async getBookSuggestions(jobId: string): Promise<WorldviewSuggestionList>
async adoptSuggestions(jobId: string, request: AdoptSuggestionRequest): Promise<AdoptSuggestionResponse>
async updateSuggestion(suggestionId: string, data: UpdateSuggestionRequest): Promise<WorldviewSuggestion>
```

#### AI改写助手 (4个方法)
```typescript
async getRewriteModels(): Promise<AIModel[]>
async analyzeText(request: TextAnalysisRequest): Promise<TextAnalysisResult>
async rewriteWithArena(request: RewriteRequest): Promise<RewriteResponse>
async getRewriteHistory(page: number, pageSize: number): Promise<RewriteSessionList>
```

#### 小说评审 (15个方法)
```typescript
async reviewChapter(chapterId: string, request: ReviewSessionCreate): Promise<ChapterReviewResponse>
async getReviewSession(sessionId: string): Promise<ReviewSessionResponse>
async getChapterReviewHistory(chapterId: string): Promise<ReviewSessionResponse[]>
async getChapterTasks(chapterId: string, filters?: TaskFilters): Promise<ReviewTaskListResponse>
async createTask(data: ReviewTaskCreate): Promise<ReviewTaskResponse>
async updateTask(taskId: string, data: ReviewTaskUpdate): Promise<ReviewTaskResponse>
async updateTaskStatus(taskId: string, data: ReviewTaskStatusUpdate): Promise<ReviewTaskResponse>
async batchOperateTasks(request: BatchOperationRequest): Promise<void>
async deleteTask(taskId: string): Promise<void>
async getTaskStats(chapterId?: string): Promise<TaskStatsResponse>
async createVersion(chapterId: string, data: ChapterVersionCreate): Promise<ChapterVersionResponse>
async getChapterVersions(chapterId: string, milestonesOnly?: boolean): Promise<ChapterVersionListResponse>
async getVersionDetail(versionId: string): Promise<ChapterVersionDetailResponse>
async updateVersionMilestone(versionId: string, data: VersionMilestoneUpdate): Promise<ChapterVersionResponse>
async compareVersions(versionA: string, versionB: string): Promise<VersionComparisonResponse>
```

#### AI评估 (1个方法)
```typescript
async evaluateAIContent(request: EvaluationRequest): Promise<EvaluationResponse>
```

#### 去痕迹 (7个方法)
```typescript
async getHumanizeProfile(): Promise<UserProfileResponse>
async updateHumanizeSettings(settings: UserProfileUpdateRequest): Promise<UserProfileResponse>
async getHumanizeHistory(page: number, pageSize: number): Promise<HumanizeHistoryResponse>
async getHumanizeSession(sessionId: string): Promise<HumanizeSessionResponse>
async getHumanizeStats(): Promise<HumanizeStatsResponse>
async submitHumanizeFeedback(request: UserFeedbackRequest): Promise<void>
async humanizeText(request: HumanizeRequest): Promise<HumanizeSessionResponse> // ⚠️ 有Bug
```

---

## 🐛 已知问题和修复建议

### ~~1. 去痕迹功能序列化Bug (严重)~~ ✅ 已修复

**问题**: `DimensionScore` 对象无法序列化为JSON
**影响**: 去痕迹功能完全不可用 (HTTP 500)
**修复时间**: 2025-01-28
**修复方案**: 使用Pydantic BaseModel和FastAPI默认序列化

```python
# backend/app/schemas/humanize.py
from pydantic import BaseModel

class DimensionScore(BaseModel):
    score: float
    description: str
    issues: List[str] = []

    class Config:
        from_attributes = True
```

**修复结果**: ✅ 功能完全可用,已完成测试

---

## 📊 总结

### 已完成的后端功能

| 功能模块 | API数量 | 后端状态 | 前端状态 | 优先级 |
|---------|--------|---------|---------|--------|
| 个人知识库 | 7 | ✅ 100% | ❌ 0% | ⭐⭐⭐⭐⭐ |
| AI拆书 | 8 | ✅ 100% | ❌ 0% | ⭐⭐⭐⭐ |
| AI改写助手 | 4 | ✅ 100% | ❌ 0% | ⭐⭐⭐ |
| 小说评审 | 15 | ✅ 100% | ❌ 0% | ⭐⭐⭐ |
| AI评估 | 1 | ✅ 100% | ❌ 0% | ⭐⭐ |
| 去痕迹 | 7 | ✅ 100% | ❌ 0% | ⭐⭐ |
| 改写历史 | 4 | ✅ 100% | ❌ 0% | ⭐ |
| **总计** | **46** | **100%** | **0%** | - |

### 开发工作量估算

| 功能模块 | 前端工作量 | 预计时间 |
|---------|----------|----------|
| 个人知识库 | 高 | 2周 |
| AI拆书 | 高 | 2周 |
| AI改写助手 | 中 | 1.5周 |
| 小说评审 | 中 | 1周 |
| AI评估 | 低 | 2天 |
| 去痕迹 | 中 | 3天 |
| 改写历史 | 低 | 1天 |
| **总计** | - | **约7-8周** |

---

**文档最后更新**: 2025-01-28
**最后更新**: 2025-01-28
**维护者**: 前端开发团队

## 📝 更新日志

**2025-01-28**:
- 修正文档日期从10月改为1月
- 确认所有API路由实际实现位置
- 标注books.py在endpoints子目录下
- 明确各API在哪个文件中实现
- 更新序列化Bug修复时间
