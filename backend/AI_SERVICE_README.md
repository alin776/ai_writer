# AI 服务实现文档

## 📋 概述

本文档说明 NovelAIde 项目的 AI 服务实现，包括：
- OpenAI 服务封装
- 5个 AI 功能接口（续写、润色、翻译、扩写、总结）
- 流式响应 (Server-Sent Events)
- 完整的测试方案

## 📁 文件结构

```
backend/
├── app/
│   ├── services/
│   │   └── ai/
│   │       ├── __init__.py              # AI 服务模块初始化
│   │       └── openai_service.py        # OpenAI 服务封装（核心）
│   └── api/
│       └── v1/
│           └── ai.py                    # AI API 路由（5个接口）
├── test_ai_service.py                   # AI 服务测试脚本
└── AI_SERVICE_README.md                 # 本文档
```

## 🚀 快速开始

### 1. 环境准备

确保 `.env` 文件配置正确：

```bash
# OpenAI 配置（必须）
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://204992.xyz/v1

# 其他配置...
DATABASE_URL=sqlite:///./novelaide.db
SECRET_KEY=your-secret-key
```

### 2. 安装依赖

```bash
# 进入后端目录
cd backend

# 激活虚拟环境
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 确认 openai 已安装（已在 requirements.txt 中）
pip install openai
```

### 3. 启动后端服务

```bash
# 方式1：开发模式（推荐）
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 方式2：使用启动脚本
.\start_server.bat  # Windows
```

### 4. 测试 AI 服务

#### 方式1：自动化测试脚本（推荐）

```bash
python test_ai_service.py
```

测试脚本会自动：
1. 注册/登录用户
2. 测试 AI 健康检查
3. 测试所有 5 个 AI 功能
4. 实时显示流式响应结果

#### 方式2：Swagger 文档测试

访问：http://localhost:8000/docs

在 Swagger UI 中：
1. 先调用 `/api/v1/auth/login` 获取 Token
2. 点击右上角 "Authorize" 按钮，输入 Token
3. 测试各个 AI 接口

#### 方式3：curl 命令测试

```bash
# 1. 登录获取 Token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"

# 2. 测试 AI 续写（替换 YOUR_TOKEN）
curl -X POST "http://localhost:8000/api/v1/ai/complete" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "context": "从前有座山，山里有座庙",
    "prompt": "续写",
    "style": "童话故事",
    "max_tokens": 300
  }'
```

## 📡 API 接口说明

### 1. AI 续写

**接口**: `POST /api/v1/ai/complete`

**请求体**:
```json
{
  "context": "上下文内容（用户已写的内容）",
  "prompt": "续写",
  "style": "玄幻小说",
  "max_tokens": 500
}
```

**响应**: 流式响应（SSE 格式）
```
data: 庙里
data: 有个
data: 老和尚
data: [DONE]
```

### 2. AI 润色

**接口**: `POST /api/v1/ai/polish`

**请求体**:
```json
{
  "text": "待润色的文本"
}
```

### 3. AI 翻译

**接口**: `POST /api/v1/ai/translate`

**请求体**:
```json
{
  "text": "待翻译的文本",
  "target_lang": "auto"  // auto/english/chinese
}
```

### 4. AI 扩写

**接口**: `POST /api/v1/ai/expand`

**请求体**:
```json
{
  "text": "待扩写的文本"
}
```

### 5. AI 总结

**接口**: `POST /api/v1/ai/summarize`

**请求体**:
```json
{
  "text": "待总结的文本"
}
```

### 6. 健康检查

**接口**: `GET /api/v1/ai/health`

**响应**:
```json
{
  "status": "healthy",
  "service": "OpenAI",
  "base_url": "https://204992.xyz/v1",
  "model": "gpt-4"
}
```

## 🔧 核心实现说明

### OpenAI 服务类 (`openai_service.py`)

**主要功能**：
- 封装 OpenAI API 调用
- 支持流式响应（AsyncGenerator）
- 自动过滤思考标签（`<think>`, `</think>`）
- 完善的错误处理和日志记录

**核心方法**：
```python
class OpenAIService:
    async def stream_complete(...)      # AI 续写
    async def stream_polish(...)        # AI 润色
    async def stream_translate(...)     # AI 翻译
    async def stream_expand(...)        # AI 扩写
    async def stream_summarize(...)     # AI 总结
    async def _stream_chat(...)         # 通用流式聊天
```

### AI API 路由 (`ai.py`)

**主要功能**：
- 提供 RESTful API 接口
- 处理请求参数验证（Pydantic）
- 返回 SSE 流式响应
- 集成用户认证（JWT Token）

**SSE 响应格式**：
```python
async def event_generator():
    async for chunk in ai_service.stream_complete(...):
        yield f"data: {chunk}\n\n"
    yield "data: [DONE]\n\n"
```

## 🧪 测试指南

### 测试检查清单

- [ ] 后端服务正常启动
- [ ] 用户可以注册/登录
- [ ] 获取 JWT Token 成功
- [ ] AI 健康检查通过
- [ ] AI 续写功能正常，实时流式输出
- [ ] AI 润色功能正常
- [ ] AI 翻译功能正常（中英互译）
- [ ] AI 扩写功能正常
- [ ] AI 总结功能正常
- [ ] 错误处理正确（无效 Token、网络错误等）

### 预期测试结果

运行 `python test_ai_service.py` 应该看到：

```
============================================================
🚀 开始测试 AI 服务
============================================================

============================================================
步骤 1: 用户注册/登录
============================================================
✅ 注册成功
Token: eyJhbGciOiJIUzI1NiIs...

============================================================
步骤 2: AI 服务健康检查
============================================================
✅ AI 服务正常
   服务: OpenAI
   模型: gpt-4
   Base URL: https://204992.xyz/v1

============================================================
步骤 3: 测试 AI 续写
============================================================
上下文: 从前有座山，山里有座庙，庙里有个老和尚在讲故事。

AI 续写结果:
------------------------------------------------------------
故事讲的是在很久很久以前，有一个小和尚，他非常调皮...
------------------------------------------------------------
✅ AI 续写完成，共生成 XXX 个字符

... (其他测试)

============================================================
✅ 所有测试完成！
============================================================
```

## ⚠️ 常见问题

### 1. 导入错误：`ModuleNotFoundError: No module named 'openai'`

**解决方案**：
```bash
pip install openai
```

### 2. OpenAI API 错误：`Incorrect API key provided`

**原因**：`.env` 文件中的 `OPENAI_API_KEY` 配置错误

**解决方案**：
- 检查 `backend/.env` 文件
- 确保 API Key 正确无误
- 确保 `OPENAI_BASE_URL` 正确（https://204992.xyz/v1）

### 3. 流式响应中断或卡死

**可能原因**：
- 网络不稳定
- OpenAI API 超时
- Nginx 缓冲配置问题（生产环境）

**解决方案**：
- 检查网络连接
- 增加 `timeout` 配置
- 在响应头中添加 `X-Accel-Buffering: no`（已实现）

### 4. 401 Unauthorized 错误

**原因**：Token 无效或过期

**解决方案**：
- 重新登录获取新 Token
- 检查 Token 是否正确添加到请求头
- 确保使用 `Bearer` 前缀：`Authorization: Bearer <token>`

### 5. CORS 错误（前端调用时）

**原因**：跨域配置问题

**解决方案**：
- 检查 `backend/app/core/config.py` 中的 `CORS_ORIGINS`
- 确保前端地址在允许列表中
- 默认已配置：`http://localhost:5173`, `http://localhost:3000`

## 📊 性能优化建议

### 1. Token 计费追踪

未来可以添加 AI 请求日志表，记录每次调用的 token 使用量和成本：

```python
class AIRequestLog(Base):
    user_id = Column(UUID)
    request_type = Column(String)  # complete/polish/translate
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    cost = Column(Float)
    created_at = Column(DateTime)
```

### 2. 缓存策略

对于相同的输入，可以缓存 AI 响应结果（使用 Redis）：

```python
cache_key = f"ai:{request_type}:{hash(text)}"
cached_result = await redis.get(cache_key)
if cached_result:
    return cached_result
```

### 3. 频率限制

防止滥用，可以添加用户级别的频率限制：

```python
@router.post("/complete")
@rate_limit(max_requests=10, window=60)  # 每分钟最多10次
async def ai_complete(...):
    ...
```

## 🔗 相关文档

- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [FastAPI 流式响应](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- [Server-Sent Events 规范](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

## 📝 更新日志

### v1.0.0 (2025-01-XX)
- ✅ 实现 OpenAI 服务封装
- ✅ 实现 5 个 AI 功能接口
- ✅ 支持流式响应（SSE）
- ✅ 添加完整测试脚本
- ✅ 添加文档和使用说明

## 👨‍💻 开发者

如有问题或建议，请联系后端开发团队。

---

**祝测试顺利！** 🎉
