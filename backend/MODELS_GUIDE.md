# AI 模型配置指南

## 📍 模型配置位置

### 1. **环境变量配置**（推荐）

**文件**: `backend/.env`

```env
# OpenAI 配置
OPENAI_API_KEY=sk-6d9175726392996b969a9ded28fe2a47dce1884c2023f28fc3cb666d22db57d8
OPENAI_BASE_URL=https://204992.xyz/v1
OPENAI_MODEL=gpt-4  # ⬅️ 在这里修改模型
```

### 2. **代码配置位置**

**文件**: `backend/app/core/config.py` (第 44 行)

```python
class Settings(BaseSettings):
    # OpenAI 配置
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://204992.xyz/v1"
    OPENAI_MODEL: str = "gpt-4"  # 默认模型
```

**文件**: `backend/app/services/ai/openai_service.py` (第 28 行)

```python
class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL
        )
        self.default_model = settings.OPENAI_MODEL  # 从配置读取
```

---

## 🤖 常用 AI 模型列表

### **OpenAI 模型**

如果使用 OpenAI 官方 API (`https://api.openai.com/v1`)：

| 模型名称 | 说明 | 推荐场景 | 价格 |
|---------|------|---------|------|
| `gpt-4` | 最强大的模型 | 复杂创作、推理任务 | 最贵 |
| `gpt-4-turbo` | GPT-4 快速版 | 平衡性能和成本 | 较贵 |
| `gpt-4-turbo-preview` | GPT-4 Turbo 预览版 | 测试最新功能 | 较贵 |
| `gpt-3.5-turbo` | 性价比高 | 日常续写、润色 | 便宜 |
| `gpt-3.5-turbo-16k` | 长上下文版本 | 长文本处理 | 便宜 |

### **DeepSeek 模型**

如果使用 DeepSeek API (`https://api.deepseek.com`)：

| 模型名称 | 说明 | 特点 |
|---------|------|------|
| `deepseek-chat` | DeepSeek 对话模型 | 中文友好、价格低 |
| `deepseek-coder` | DeepSeek 代码模型 | 适合代码相关任务 |

### **第三方 API 支持的模型**

如果使用 `https://204992.xyz/v1`，通常支持：

| 模型名称 | 说明 |
|---------|------|
| `gpt-4` | GPT-4 |
| `gpt-3.5-turbo` | GPT-3.5 |
| `claude-3-opus` | Claude 3 Opus（如果支持）|
| `claude-3-sonnet` | Claude 3 Sonnet（如果支持）|

---

## 🔧 如何修改模型

### **方法1：修改环境变量**（推荐）

编辑 `backend/.env` 文件：

```env
# 修改为其他模型
OPENAI_MODEL=gpt-3.5-turbo
```

然后重启后端服务：

```bash
# 停止服务（Ctrl+C）
# 重新启动
python -m uvicorn app.main:app --reload
```

### **方法2：针对不同功能使用不同模型**

修改 `backend/app/services/ai/openai_service.py`，为不同任务指定不同模型：

```python
class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL
        )
        # 不同任务使用不同模型
        self.complete_model = settings.OPENAI_MODEL      # 续写用 gpt-4
        self.polish_model = "gpt-3.5-turbo"              # 润色用 3.5（便宜）
        self.translate_model = "gpt-3.5-turbo"           # 翻译用 3.5
        self.expand_model = settings.OPENAI_MODEL        # 扩写用 gpt-4
        self.summarize_model = "gpt-3.5-turbo"           # 总结用 3.5
    
    async def stream_complete(self, ...):
        # 使用 self.complete_model
        stream = await self.client.chat.completions.create(
            model=self.complete_model,  # ⬅️ 使用特定模型
            ...
        )
    
    async def stream_polish(self, ...):
        # 使用 self.polish_model
        stream = await self.client.chat.completions.create(
            model=self.polish_model,  # ⬅️ 使用特定模型
            ...
        )
```

### **方法3：通过 API 参数指定模型**

修改 API 路由，允许前端传递模型参数：

```python
# backend/app/api/v1/ai.py

class AICompleteRequest(BaseModel):
    context: str
    prompt: str = "续写"
    style: str = ""
    max_tokens: int = 500
    model: Optional[str] = None  # ⬅️ 新增：允许前端指定模型

@router.post("/complete")
async def ai_complete(
    request: AICompleteRequest,
    current_user: User = Depends(get_current_active_user)
):
    ai_service = OpenAIService()
    
    # 如果前端指定了模型，则使用前端的；否则使用默认
    model = request.model or ai_service.default_model
    
    # 需要修改 OpenAIService 支持传递 model 参数
    async for chunk in ai_service.stream_complete(
        context=request.context,
        model=model  # ⬅️ 传递模型参数
    ):
        yield f"data: {chunk}\n\n"
```

---

## 💰 模型成本对比（参考）

### **OpenAI 官方价格**（2024年1月）

| 模型 | 输入（/1K tokens） | 输出（/1K tokens） |
|------|------------------|------------------|
| GPT-4 | $0.03 | $0.06 |
| GPT-4 Turbo | $0.01 | $0.03 |
| GPT-3.5 Turbo | $0.0005 | $0.0015 |

### **成本优化建议**

1. **简单任务用 3.5**：润色、翻译、总结等
2. **复杂任务用 4.0**：创意续写、扩写等
3. **设置 max_tokens 限制**：避免生成过长内容
4. **启用缓存**：相同输入返回缓存结果
5. **监控使用量**：记录每次调用的 token 消耗

---

## 🧪 测试不同模型

### **快速测试**

修改 `.env` 中的模型：

```env
# 测试 GPT-3.5
OPENAI_MODEL=gpt-3.5-turbo
```

重启服务后运行测试：

```bash
python test_ai_service.py
```

观察效果差异：
- **速度**：3.5 更快，4.0 较慢
- **质量**：4.0 更好，3.5 略逊
- **成本**：3.5 便宜 60 倍

---

## ⚙️ 高级配置：多模型策略

### **场景1：按任务复杂度自动选择**

```python
class OpenAIService:
    def choose_model(self, task_type: str, text_length: int) -> str:
        """根据任务类型和文本长度选择模型"""
        
        # 简单任务 + 短文本 → 3.5
        if task_type in ["polish", "translate", "summarize"] and text_length < 1000:
            return "gpt-3.5-turbo"
        
        # 复杂任务 + 长文本 → 4.0
        if task_type in ["complete", "expand"] or text_length > 2000:
            return "gpt-4"
        
        # 默认 3.5
        return "gpt-3.5-turbo"
```

### **场景2：用户订阅等级决定**

```python
class OpenAIService:
    def get_user_model(self, user: User) -> str:
        """根据用户订阅等级返回可用模型"""
        
        if user.subscription == "premium":
            return "gpt-4"  # 付费用户用 GPT-4
        else:
            return "gpt-3.5-turbo"  # 免费用户用 3.5
```

---

## 📊 模型监控

### **记录每次调用的模型和成本**

```python
# backend/app/models/ai_log.py
class AIRequestLog(Base):
    __tablename__ = "ai_request_logs"
    
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID)
    request_type = Column(String)  # complete/polish/translate
    model = Column(String)  # 使用的模型
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    total_tokens = Column(Integer)
    cost = Column(Float)  # 成本（美元）
    created_at = Column(DateTime)
```

在 API 中记录：

```python
@router.post("/complete")
async def ai_complete(...):
    model_used = ai_service.default_model
    
    # ... AI 调用
    
    # 记录日志
    log = AIRequestLog(
        user_id=current_user.id,
        request_type="complete",
        model=model_used,
        total_tokens=response.usage.total_tokens,
        cost=calculate_cost(model_used, response.usage)
    )
    db.add(log)
```

---

## ✅ 验证配置

运行健康检查：

```bash
curl http://localhost:8000/api/v1/ai/health
```

返回示例：

```json
{
  "status": "healthy",
  "service": "OpenAI",
  "base_url": "https://204992.xyz/v1",
  "model": "gpt-4"  // ⬅️ 当前使用的模型
}
```

---

## 🔗 相关资源

- [OpenAI 模型文档](https://platform.openai.com/docs/models)
- [OpenAI 价格表](https://openai.com/pricing)
- [DeepSeek API 文档](https://api-docs.deepseek.com/)

---

**建议**：
- 开发环境：用 `gpt-3.5-turbo`（省钱）
- 生产环境：用 `gpt-4`（质量好）
- 或根据用户订阅等级动态切换
