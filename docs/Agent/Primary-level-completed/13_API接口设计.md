# API接口设计

> **版本**: v1.1
> **创建日期**: 2025-10-31
> **最后更新**: 2025-11-01
> **项目状态**: ✅ 项目100%完成

---

## 📋 目录

- [1. Agent增强功能API](#1-agent增强功能api)
- [2. Memory管理API](#2-memory管理api)
- [3. 版本控制API](#3-版本控制api)
- [4. 质量评估API](#4-质量评估api)
- [5. 成本追踪API](#5-成本追踪api)

---

## 1. Agent增强功能API

### 1.1 智能写作 (带质量循环)

**端点**: `POST /api/v1/agent/write-enhanced`

**描述**: 使用质量循环机制生成高质量内容

**请求体**:
```json
{
  "conversation_id": "conv_123",
  "user_id": "user_456",
  "context": "前文内容...",
  "requirements": "续写要求",
  "target_length": 1000,
  "enable_quality_loop": true,
  "max_iterations": 3
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "generated_text": "生成的内容...",
    "word_count": 1050,
    "quality_evaluation": {
      "overall_score": 8.5,
      "dimension_scores": [
        {
          "dimension": "content_quality",
          "score": 9.0,
          "feedback": "内容质量优秀"
        }
      ],
      "iterations": 2
    },
    "version_id": "v_789"
  }
}
```

### 1.2 流式写作

**端点**: `POST /api/v1/agent/write-stream`

**描述**: 流式返回生成内容

**响应**: SSE流

```
data: {"type": "start", "message": "开始生成..."}

data: {"type": "content", "text": "生成的内容片段..."}

data: {"type": "quality", "score": 8.5}

data: {"type": "done", "version_id": "v_789"}
```

---

## 2. Memory管理API

### 2.1 添加记忆

**端点**: `POST /api/v1/agent/memory`

**请求体**:
```json
{
  "user_id": "user_456",
  "conversation_id": "conv_123",
  "role": "user",
  "content": "记忆内容",
  "importance": 0.8
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "memory_id": "mem_001",
    "layer": "short_term"
  }
}
```

### 2.2 获取相关记忆

**端点**: `GET /api/v1/agent/memory/relevant`

**查询参数**:
- `conversation_id`: 会话ID
- `query`: 查询内容
- `limit`: 返回数量 (默认10)

**响应**:
```json
{
  "success": true,
  "data": {
    "memories": [
      {
        "memory_id": "mem_001",
        "content": "记忆内容",
        "importance": 0.8,
        "layer": "medium_term",
        "relevance": 0.95
      }
    ]
  }
}
```

### 2.3 创建快照

**端点**: `POST /api/v1/agent/memory/snapshot`

**请求体**:
```json
{
  "user_id": "user_456",
  "conversation_id": "conv_123",
  "description": "快照描述"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "snapshot_id": "snap_001",
    "timestamp": "2025-10-31T10:00:00Z"
  }
}
```

### 2.4 恢复快照

**端点**: `POST /api/v1/agent/memory/restore`

**请求体**:
```json
{
  "snapshot_id": "snap_001"
}
```

---

## 3. 版本控制API

### 3.1 创建内容版本

**端点**: `POST /api/v1/agent/versions`

**请求体**:
```json
{
  "content_id": "content_123",
  "base_content": "基础内容",
  "description": "初始版本"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "version_id": "v_001",
    "content_id": "content_123"
  }
}
```

### 3.2 应用补丁

**端点**: `POST /api/v1/agent/versions/apply-patch`

**请求体**:
```json
{
  "content_id": "content_123",
  "patch": {
    "operation": "insert",
    "position": 100,
    "content": "插入的内容"
  },
  "description": "添加新段落"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "version_id": "v_002",
    "content": "更新后的完整内容"
  }
}
```

### 3.3 获取版本内容

**端点**: `GET /api/v1/agent/versions/{version_id}`

**响应**:
```json
{
  "success": true,
  "data": {
    "version_id": "v_002",
    "content": "该版本的内容",
    "parent_version_id": "v_001",
    "created_at": "2025-10-31T10:00:00Z"
  }
}
```

### 3.4 回滚版本

**端点**: `POST /api/v1/agent/versions/rollback`

**请求体**:
```json
{
  "content_id": "content_123",
  "target_version_id": "v_001"
}
```

### 3.5 获取版本历史

**端点**: `GET /api/v1/agent/versions/history/{content_id}`

**响应**:
```json
{
  "success": true,
  "data": {
    "versions": [
      {
        "version_id": "v_002",
        "description": "添加新段落",
        "created_at": "2025-10-31T10:05:00Z"
      },
      {
        "version_id": "v_001",
        "description": "初始版本",
        "created_at": "2025-10-31T10:00:00Z"
      }
    ]
  }
}
```

---

## 4. 质量评估API

### 4.1 评估内容质量

**端点**: `POST /api/v1/agent/quality/evaluate`

**请求体**:
```json
{
  "content": "待评估的内容",
  "context": "上下文",
  "dimensions": ["content_quality", "coherence", "length_check"]
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "overall_score": 8.5,
    "passes": true,
    "dimension_scores": [
      {
        "dimension": "content_quality",
        "score": 9.0,
        "feedback": "内容质量优秀",
        "weight": 0.5
      },
      {
        "dimension": "coherence",
        "score": 8.5,
        "feedback": "连贯性良好",
        "weight": 0.3
      },
      {
        "dimension": "length_check",
        "score": 8.0,
        "feedback": "字数符合要求",
        "weight": 0.2
      }
    ],
    "suggestions": [
      "可以增强情节冲突",
      "对话可以更生动"
    ]
  }
}
```

---

## 5. 成本追踪API

### 5.1 获取用户成本统计

**端点**: `GET /api/v1/agent/cost/stats`

**查询参数**:
- `user_id`: 用户ID
- `start_date`: 开始日期
- `end_date`: 结束日期

**响应**:
```json
{
  "success": true,
  "data": {
    "total_cost": 12.50,
    "total_tokens": 125000,
    "api_calls": 250,
    "breakdown": {
      "gpt-4": {
        "cost": 10.00,
        "tokens": 50000,
        "calls": 100
      },
      "gpt-3.5-turbo": {
        "cost": 2.00,
        "tokens": 50000,
        "calls": 100
      },
      "deepseek-chat": {
        "cost": 0.50,
        "tokens": 25000,
        "calls": 50
      }
    }
  }
}
```

### 5.2 获取成本报告

**端点**: `GET /api/v1/agent/cost/report`

**查询参数**:
- `period`: 时间周期 (daily/weekly/monthly)

**响应**:
```json
{
  "success": true,
  "data": {
    "period": "daily",
    "date": "2025-10-31",
    "total_cost": 12.50,
    "average_cost_per_user": 0.25,
    "cost_trend": "+5%",
    "top_users": [
      {
        "user_id": "user_456",
        "cost": 5.00
      }
    ]
  }
}
```

---

## 📝 通用响应格式

### 成功响应

```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

### 错误响应

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "参数验证失败",
    "details": {
      "field": "target_length",
      "reason": "必须大于0"
    }
  }
}
```

### 错误码

| 错误码 | 说明 |
|--------|------|
| `VALIDATION_ERROR` | 参数验证失败 |
| `NOT_FOUND` | 资源不存在 |
| `UNAUTHORIZED` | 未授权 |
| `RATE_LIMIT` | 请求频率超限 |
| `COST_LIMIT_EXCEEDED` | 成本超限 |
| `INTERNAL_ERROR` | 服务器内部错误 |

---

**文档完成** ✅
