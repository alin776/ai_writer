# AI去痕迹功能 - 快速开始指南

## 📋 功能概述

AI去痕迹功能是一个智能的后处理层,可以将AI生成的文本变得更加自然、人性化,减少明显的AI痕迹。

### 核心特性

1. **三阶段处理流程**
   - 🔍 检测: 5维度AI特征评分
   - ✍️ 改写: 支持 light/medium/strong 三种强度
   - ✅ 验证: 对比改写效果

2. **智能用户画像**
   - 自动学习用户偏好
   - 智能显示策略 (详细 → 简化 → 静默)
   - 自动检测用户类型

3. **灵活的控制选项**
   - 全局开关
   - 分功能开关
   - 强度可调

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
# 在虚拟环境中执行
cd backend
alembic upgrade head
```

### 3. 启动服务

```bash
cd backend
python -m uvicorn app.main:app --reload
```

---

## 📡 API 使用示例

### 1. 获取用户画像

```bash
GET /api/v1/humanize/profile
Authorization: Bearer <token>
```

**响应:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "total_uses": 10,
  "accept_rate": 0.8,
  "humanize_enabled_global": true,
  "humanize_enabled_by_function": {
    "complete": true,
    "polish": true,
    "expand": true
  },
  "display_mode": "simplified"
}
```

### 2. 更新设置

```bash
PUT /api/v1/humanize/profile/settings
Authorization: Bearer <token>
Content-Type: application/json

{
  "humanize_enabled_global": true,
  "humanize_enabled_by_function": {
    "complete": true,
    "polish": false
  },
  "preferred_intensity": "medium"
}
```

### 3. 查看历史记录

```bash
GET /api/v1/humanize/history?page=1&page_size=20
Authorization: Bearer <token>
```

### 4. 查看统计数据

```bash
GET /api/v1/humanize/stats
Authorization: Bearer <token>
```

**响应:**
```json
{
  "total_uses": 100,
  "avg_improvement": 25.5,
  "accept_rate": 0.75,
  "total_tokens": 150000,
  "total_cost": 4.50,
  "most_used_function": "complete"
}
```

### 5. 提交反馈

```bash
POST /api/v1/humanize/feedback
Authorization: Bearer <token>
Content-Type: application/json

{
  "session_id": "uuid",
  "accepted": true
}
```

---

## 💻 代码集成示例

### 方式一: 独立使用 HumanizeService

```python
from app.services.ai.humanize_service import HumanizeService
from app.services.ai.http_ai_service import HTTPAIService

# 初始化服务
ai_service = HTTPAIService()
humanize_service = HumanizeService(ai_service)

# 完整的三阶段处理
result = await humanize_service.full_humanize_process(
    text="AI生成的文本",
    intensity="medium",
    skip_detection=False
)

print(f"原始分数: {result['detection'].overall_score}")
print(f"改写后分数: {result['verification'].score_after}")
print(f"改进幅度: {result['verification'].improvement}")
print(f"改写后文本: {result['humanized_text']}")
```

### 方式二: 流式输出

```python
# 流式改写 (适用于前端实时显示)
async for chunk in humanize_service.humanize_stream(
    text="AI生成的文本",
    intensity="medium"
):
    print(chunk, end="", flush=True)
```

### 方式三: 集成到现有 AI 接口 (推荐)

```python
from fastapi import APIRouter
from app.services.ai.http_ai_service import HTTPAIService
from app.services.ai.humanize_service import HumanizeService
from app.services.user_profile_service import UserProfileService

@router.post("/ai/complete")
async def ai_complete(
    request: CompleteRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # 获取用户画像
    profile_service = UserProfileService(db)
    profile = await profile_service.get_or_create_profile(current_user.id)

    # 判断是否启用去痕迹
    if not profile.should_enable_humanize("complete"):
        # 直接返回原始AI输出
        async for chunk in ai_service.stream_complete(context):
            yield chunk
        return

    # 启用去痕迹
    # 1. 先生成完整文本
    full_text = ""
    async for chunk in ai_service.stream_complete(context):
        full_text += chunk

    # 2. 检测AI痕迹
    detection = await humanize_service.detect_ai_traces(full_text)
    if detection.overall_score < 60:
        # 分数低,无需去痕迹
        yield full_text
        return

    # 3. 流式去痕迹
    async for chunk in humanize_service.humanize_stream(
        full_text,
        intensity=profile_service.get_recommended_intensity(profile)
    ):
        yield chunk
```

---

## 🔧 配置说明

### 数据库表

1. **user_profiles** - 用户画像
   - 存储用户偏好、统计数据、开关配置

2. **humanize_sessions** - 去痕迹会话 (永久保存)
   - 存储核心数据: 分数、Token、成本

3. **humanize_session_details** - 会话详情 (30天自动清理)
   - 存储详情数据: 维度评分、检测到的痕迹、文本预览

### 定时任务

- **清理过期数据**: 每天凌晨 2:00 执行
- **清理逻辑**: 删除 `expires_at < 当前时间` 的详情记录

---

## 📊 成本估算

### Token 消耗

去痕迹需要3次AI调用:

1. **检测阶段**: ~1000 tokens (input + 500 JSON 输出)
2. **改写阶段**: ~2x input tokens (input + 改写输出)
3. **验证阶段**: ~500 tokens (2x input + 200 JSON 输出)

**总计**: 约为原始文本的 **2-3倍** Token 消耗

### 成本示例

假设使用 GPT-4 Turbo:
- Prompt: $0.01 / 1K tokens
- Completion: $0.03 / 1K tokens

处理 500 字文本 (~750 tokens):
- 总 Prompt tokens: ~2500
- 总 Completion tokens: ~1500
- **总成本**: ~$0.07

---

## ⚠️ 注意事项

1. **Token 消耗**
   - 去痕迹会增加 2-3倍 Token 消耗
   - 建议对用户设置配额限制

2. **处理时间**
   - 三阶段处理预计 4-6秒
   - 适合异步处理或流式返回

3. **数据隐私**
   - 全文不保存,仅保留前100字预览
   - 详情数据30天自动清理

4. **容错机制**
   - AI调用失败时自动返回原文
   - 不会因去痕迹失败而中断业务流程

---

## 🐛 调试与监控

### 查看日志

```bash
# 查看去痕迹相关日志
tail -f backend/logs/app.log | grep -i humanize
```

### 监控指标

```python
# 查看统计数据
GET /api/v1/humanize/stats

# 查看最近的会话
GET /api/v1/humanize/history?page=1&page_size=10
```

---

## 📚 相关文档

- [完整开发计划](./todo.md)
- [API 文档](http://localhost:8000/docs) (Swagger UI)
- [数据库模型](../backend/app/models/humanize_session.py)
- [核心服务](../backend/app/services/ai/humanize_service.py)

---

**版本:** 1.0.0
**更新日期:** 2025-10-26
