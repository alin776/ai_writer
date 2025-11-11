# AI去痕迹化集成Agent实施方案

> 生成时间: 2025-11-11
> 架构方案: 混合模式（Agent工具 + 独立API）

---

## 📊 架构设计

### 总体架构图

```
┌────────────────────────────────────────────────────┐
│  前端UI层                                           │
│  ┌──────────────────┐  ┌──────────────────────┐   │
│  │ Agent对话面板    │  │ 独立去痕迹面板        │   │
│  │ - 对话式交互     │  │ - 参数配置           │   │
│  │ - 智能识别       │  │ - 对比显示           │   │
│  │ - 工具调用显示   │  │ - 历史记录           │   │
│  └──────────────────┘  └──────────────────────┘   │
└────────────────────────────────────────────────────┘
         │                        │
         ▼                        ▼
┌────────────────────────────────────────────────────┐
│  API层                                              │
│  ┌──────────────────┐  ┌──────────────────────┐   │
│  │ Agent API        │  │ Humanize API         │   │
│  │ /agent/chat      │  │ /humanize/submit     │   │
│  │ - 调用tool       │  │ /humanize/status     │   │
│  │ - 流式响应       │  │ /humanize/result     │   │
│  └──────────────────┘  └──────────────────────┘   │
└────────────────────────────────────────────────────┘
         │                        │
         └────────┬───────────────┘
                  ▼
┌────────────────────────────────────────────────────┐
│  服务层                                             │
│  ┌──────────────────────────────────────────────┐ │
│  │ HumanizeService (共享)                       │ │
│  │ ├─ 检测阶段 (FastAI)                         │ │
│  │ ├─ 改写阶段 (GPT-4)                          │ │
│  │ └─ 验证阶段 (FastAI)                         │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────┐
│  任务队列层 (新增)                                  │
│  ┌──────────────────────────────────────────────┐ │
│  │ Celery Worker Pool                           │ │
│  │ ├─ humanize_task (异步处理)                  │ │
│  │ ├─ 任务优先级队列                            │ │
│  │ └─ 重试和错误恢复                            │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────┐
│  存储层                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ PostgreSQL  │  │ Redis Cache  │  │ Redis    │ │
│  │ - 会话记录  │  │ - 结果缓存   │  │ - 任务队 │ │
│  │ - 用户画像  │  │ - 相似度匹配 │  │   列状态 │ │
│  └─────────────┘  └──────────────┘  └──────────┘ │
└────────────────────────────────────────────────────┘
```

---

## 🔧 实施步骤

### Phase 1: 重构现有API为异步模式（3-5天）

#### 1.1 集成Celery任务队列

**安装依赖**：
```bash
pip install celery[redis]
```

**配置Celery**：
```python
# backend/app/core/celery_app.py
from celery import Celery

celery_app = Celery(
    "ai_writer",
    broker="redis://localhost:6379/1",
    backend="redis://localhost:6379/2"
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5分钟超时
    task_soft_time_limit=270,
    worker_prefetch_multiplier=1,
)
```

#### 1.2 创建异步任务

**新文件：`backend/app/tasks/humanize_tasks.py`**
```python
from app.core.celery_app import celery_app
from app.services.ai.humanize_service import HumanizeService
from app.core.database import get_db_context
from uuid import UUID
import json

@celery_app.task(bind=True, name="humanize.process_text")
def humanize_task(
    self,
    text: str,
    intensity: str,
    user_id: str,
    ai_function: str = "rewrite"
):
    """
    异步去痕迹化任务

    Args:
        self: Celery task实例
        text: 待处理文本
        intensity: 处理强度
        user_id: 用户ID
        ai_function: AI功能类型
    """
    try:
        # 更新进度: 0%
        self.update_state(
            state="PROGRESS",
            meta={"progress": 0, "stage": "初始化"}
        )

        # 初始化服务
        service = HumanizeService()

        # 更新进度: 10%
        self.update_state(
            state="PROGRESS",
            meta={"progress": 10, "stage": "检测AI痕迹"}
        )

        # 执行处理（带进度回调）
        async def progress_callback(stage, progress):
            self.update_state(
                state="PROGRESS",
                meta={"progress": progress, "stage": stage}
            )

        result = await service.full_humanize_process_with_progress(
            text=text,
            intensity=intensity,
            progress_callback=progress_callback
        )

        # 保存到数据库
        async with get_db_context() as db:
            # 保存会话记录（复用现有逻辑）
            session = await save_humanize_session(
                db=db,
                user_id=UUID(user_id),
                text=text,
                result=result,
                intensity=intensity,
                ai_function=ai_function
            )

        # 返回结果
        return {
            "success": True,
            "session_id": str(session.id),
            "humanized_text": result["humanized_text"],
            "score_before": result["detection"].overall_score,
            "score_after": result.get("verification", {}).get("score_after", 0),
            "improvement": result.get("verification", {}).get("improvement", 0),
            "processing_time": result["processing_time"],
            "tokens_used": result["total_tokens"],
            "cost": result.get("cost", 0)
        }

    except Exception as e:
        # 错误处理
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise
    finally:
        # 关闭服务
        await service.close()
```

#### 1.3 修改API端点

**修改：`backend/app/api/v1/humanize.py`**

```python
from app.tasks.humanize_tasks import humanize_task
from celery.result import AsyncResult

@router.post("/submit", response_model=HumanizeTaskResponse)
async def submit_humanize_task(
    request: HumanizeRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    提交去痕迹化任务（异步）

    立即返回任务ID，后台处理
    """
    # 提交任务到Celery
    task = humanize_task.delay(
        text=request.text,
        intensity=request.intensity,
        user_id=str(current_user.id),
        ai_function=request.ai_function or "rewrite"
    )

    # 估算处理时间
    text_length = len(request.text)
    estimated_time = int(text_length / 50)  # 每50字约1秒

    return HumanizeTaskResponse(
        task_id=task.id,
        status="pending",
        estimated_time=estimated_time
    )


@router.get("/status/{task_id}", response_model=HumanizeTaskStatusResponse)
async def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    查询任务状态

    返回任务进度和预估剩余时间
    """
    task = AsyncResult(task_id)

    if task.state == "PENDING":
        return HumanizeTaskStatusResponse(
            task_id=task_id,
            status="pending",
            progress=0,
            stage="等待处理"
        )

    elif task.state == "PROGRESS":
        return HumanizeTaskStatusResponse(
            task_id=task_id,
            status="processing",
            progress=task.info.get("progress", 0),
            stage=task.info.get("stage", "处理中"),
            eta=task.info.get("eta", None)
        )

    elif task.state == "SUCCESS":
        return HumanizeTaskStatusResponse(
            task_id=task_id,
            status="completed",
            progress=100,
            stage="完成"
        )

    elif task.state == "FAILURE":
        return HumanizeTaskStatusResponse(
            task_id=task_id,
            status="failed",
            progress=0,
            stage="失败",
            error=str(task.info)
        )


@router.get("/result/{task_id}", response_model=HumanizeSessionResponse)
async def get_task_result(
    task_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取任务结果

    任务完成后调用此接口获取结果
    """
    task = AsyncResult(task_id)

    if task.state != "SUCCESS":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"任务未完成，当前状态: {task.state}"
        )

    result = task.result
    session_id = UUID(result["session_id"])

    # 查询会话详情
    session = await db.get(HumanizeSession, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )

    # 返回完整结果
    return HumanizeSessionResponse.from_orm(session)
```

#### 1.4 新增Schema

**添加到：`backend/app/schemas/humanize.py`**
```python
class HumanizeTaskResponse(BaseModel):
    """任务提交响应"""
    task_id: str
    status: Literal["pending"]
    estimated_time: int  # 预估处理秒数

class HumanizeTaskStatusResponse(BaseModel):
    """任务状态响应"""
    task_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    progress: int  # 0-100
    stage: str  # 当前阶段描述
    eta: Optional[int] = None  # 预估剩余秒数
    error: Optional[str] = None  # 错误信息
```

---

### Phase 2: 集成到Agent工具（2-3天）

#### 2.1 创建Agent工具

**添加到：`backend/app/services/agent/langgraph_agent.py`**

```python
@tool
async def humanize_text_tool(
    text: str,
    intensity: Literal["light", "medium", "strong"] = "medium"
) -> str:
    """
    AI去痕迹化工具 - 将AI生成的文本转换为更自然的人类写作风格

    适用场景:
    - 文本听起来太像AI生成的
    - 需要让内容更自然、更口语化
    - 避免被AI检测工具识别

    参数:
        text: 需要处理的文本（建议50-5000字）
        intensity: 处理强度
            - "light": 轻度处理，保持原文95%相似度
            - "medium": 中度处理，改动15-20%
            - "strong": 强度处理，改动30-40%

    返回:
        处理后的自然文本

    注意: 此工具处理时间较长（约30-40秒），请耐心等待
    """
    try:
        # 验证文本长度
        if len(text) < 50:
            return "错误：文本太短（少于50字），无法进行有效的去痕迹化处理"

        if len(text) > 10000:
            return "错误：文本太长（超过10000字），请分段处理"

        # 创建服务实例
        service = HumanizeService()

        # 执行去痕迹化（同步等待）
        result = await service.full_humanize_process(
            text=text,
            intensity=intensity,
            skip_detection=False,
            skip_verification=True  # Agent模式跳过验证以加速
        )

        # 格式化返回
        detection = result.get("detection")
        humanized_text = result.get("humanized_text", "")

        # 构建响应
        response = f"""已完成AI去痕迹化处理：

【原文AI特征分数】: {detection.overall_score:.1f}/100
【处理强度】: {intensity}
【处理后文本】:
{humanized_text}

💡 提示：分数越低表示越接近人类写作风格
"""
        return response

    except Exception as e:
        logger.error(f"humanize_text_tool执行失败: {e}")
        return f"去痕迹化处理失败: {str(e)}"
    finally:
        await service.close()


# 添加到工具列表
WRITING_TOOLS.append(humanize_text_tool)
```

#### 2.2 增强意图识别

**修改：`backend/app/services/agent/langgraph_agent.py`**

在 `_classify_intent` 函数中添加去痕迹化意图识别：

```python
def _classify_intent(self, message: str) -> str:
    """意图分类"""
    message_lower = message.lower()

    # 去痕迹化意图（新增）
    humanize_keywords = [
        "ai痕迹", "去痕迹", "ai化", "太ai",
        "更自然", "人性化", "像人写的",
        "机器味", "太机械", "不够自然"
    ]
    if any(keyword in message_lower for keyword in humanize_keywords):
        return "writing"  # 归类到writing场景

    # 其他意图...
    # ...
```

#### 2.3 添加工具使用提示

**修改：`backend/app/services/agent/actions/writing_action.py`**

在system_prompt中添加humanize_text_tool的使用指引：

```python
system_prompt = f"""你是一位专业的写作助手...

## 可用工具说明

### humanize_text_tool - AI去痕迹化
- **何时使用**: 用户提到文本"太AI"、"不自然"、"机器味"时
- **参数配置**:
  - intensity="light": 轻微调整，适合已经较自然的文本
  - intensity="medium": 标准处理，适合大部分场景
  - intensity="strong": 深度改写，适合AI味很重的文本
- **注意事项**:
  - 处理时间约30-40秒，提前告知用户
  - 仅支持中文文本
  - 文本长度50-10000字

### 使用示例
用户: "这段话太AI了，帮我改自然点"
工具调用: humanize_text_tool(text="...", intensity="medium")
"""
```

---

### Phase 3: 前端集成（3-4天）

#### 3.1 创建独立去痕迹面板

**新文件：`src/components/humanize/HumanizePanel.tsx`**

```tsx
import React, { useState } from 'react';
import { Card, Button, Progress, Select, Radio } from 'antd';
import { useHumanizeTask } from '@/hooks/useHumanizeTask';

interface HumanizePanelProps {
  initialText?: string;
  onComplete?: (result: HumanizeResult) => void;
}

export const HumanizePanel: React.FC<HumanizePanelProps> = ({
  initialText = '',
  onComplete
}) => {
  const [text, setText] = useState(initialText);
  const [intensity, setIntensity] = useState<'light' | 'medium' | 'strong'>('medium');
  const [readability, setReadability] = useState('College');

  const {
    submit,
    status,
    progress,
    stage,
    result,
    error
  } = useHumanizeTask();

  const handleSubmit = async () => {
    const taskId = await submit({
      text,
      intensity,
      readability
    });

    // 轮询状态直到完成
    await pollUntilComplete(taskId);
  };

  return (
    <Card title="AI去痕迹化" className="humanize-panel">
      {/* 输入区 */}
      <div className="input-section">
        <TextArea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="输入需要处理的文本..."
          rows={10}
        />
      </div>

      {/* 参数配置 */}
      <div className="config-section">
        <div className="config-item">
          <label>处理强度</label>
          <Radio.Group value={intensity} onChange={(e) => setIntensity(e.target.value)}>
            <Radio value="light">轻度（5%改动）</Radio>
            <Radio value="medium">中度（15-20%改动）</Radio>
            <Radio value="strong">强度（30-40%改动）</Radio>
          </Radio.Group>
        </div>

        <div className="config-item">
          <label>阅读难度</label>
          <Select value={readability} onChange={setReadability}>
            <Option value="High School">高中</Option>
            <Option value="College">大学</Option>
            <Option value="University">研究生</Option>
            <Option value="Doctorate">博士</Option>
          </Select>
        </div>
      </div>

      {/* 进度显示 */}
      {status === 'processing' && (
        <div className="progress-section">
          <Progress percent={progress} status="active" />
          <p className="stage-text">{stage}</p>
        </div>
      )}

      {/* 结果对比 */}
      {result && (
        <div className="result-section">
          <div className="comparison">
            <div className="original">
              <h4>原文（AI分数: {result.score_before}）</h4>
              <div className="text-preview">{text}</div>
            </div>
            <div className="humanized">
              <h4>改写后（AI分数: {result.score_after}）</h4>
              <div className="text-preview">{result.humanized_text}</div>
            </div>
          </div>

          <div className="actions">
            <Button type="primary" onClick={() => onComplete?.(result)}>
              使用改写结果
            </Button>
            <Button onClick={handleSubmit}>重新处理</Button>
          </div>
        </div>
      )}

      {/* 提交按钮 */}
      {!result && (
        <Button
          type="primary"
          size="large"
          loading={status === 'processing'}
          disabled={!text || text.length < 50}
          onClick={handleSubmit}
        >
          {status === 'processing' ? '处理中...' : '开始处理'}
        </Button>
      )}
    </Card>
  );
};
```

#### 3.2 创建Hook

**新文件：`src/hooks/useHumanizeTask.ts`**

```typescript
import { useState, useCallback } from 'react';
import { humanizeApi } from '@/services/humanizeApi';

export const useHumanizeTask = () => {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<'idle' | 'processing' | 'completed' | 'failed'>('idle');
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState('');
  const [result, setResult] = useState<HumanizeResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // 提交任务
  const submit = useCallback(async (request: HumanizeRequest) => {
    try {
      const response = await humanizeApi.submit(request);
      setTaskId(response.task_id);
      setStatus('processing');
      return response.task_id;
    } catch (err) {
      setError(err.message);
      setStatus('failed');
      throw err;
    }
  }, []);

  // 轮询状态
  const pollStatus = useCallback(async (taskId: string) => {
    const statusResponse = await humanizeApi.getStatus(taskId);

    setProgress(statusResponse.progress);
    setStage(statusResponse.stage);

    if (statusResponse.status === 'completed') {
      // 获取结果
      const resultResponse = await humanizeApi.getResult(taskId);
      setResult(resultResponse);
      setStatus('completed');
      return true;
    } else if (statusResponse.status === 'failed') {
      setError(statusResponse.error || '处理失败');
      setStatus('failed');
      return true;
    }

    return false;
  }, []);

  // 轮询直到完成
  const pollUntilComplete = useCallback(async (taskId: string) => {
    while (true) {
      const isComplete = await pollStatus(taskId);
      if (isComplete) break;

      // 等待5秒后再次轮询
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  }, [pollStatus]);

  return {
    submit,
    pollStatus,
    pollUntilComplete,
    taskId,
    status,
    progress,
    stage,
    result,
    error
  };
};
```

#### 3.3 在Agent中集成

**修改：`src/components/agent/AgentChatPanel.tsx`**

添加去痕迹化工具调用的特殊显示：

```tsx
// 检测到humanize_text_tool调用时显示特殊UI
const renderToolCall = (toolCall) => {
  if (toolCall.name === 'humanize_text_tool') {
    return (
      <div className="humanize-tool-call">
        <div className="tool-header">
          <HumanizeIcon />
          <span>正在去除AI痕迹...</span>
        </div>
        <Progress percent={50} status="active" />
        <p className="tip">
          💡 提示：处理时间约30-40秒，请耐心等待
        </p>
      </div>
    );
  }

  // 其他工具的默认显示
  return <DefaultToolCallDisplay toolCall={toolCall} />;
};
```

#### 3.4 添加快捷入口

**修改：`src/components/editor/EditorToolbar.tsx`**

```tsx
import { HumanizePanel } from '@/components/humanize/HumanizePanel';

// 添加按钮
<Tooltip title="AI去痕迹化">
  <Button
    icon={<HumanizeIcon />}
    onClick={() => setShowHumanizePanel(true)}
  >
    去AI痕迹
  </Button>
</Tooltip>

// 弹出面板
<Modal
  visible={showHumanizePanel}
  onCancel={() => setShowHumanizePanel(false)}
  width={1000}
  footer={null}
>
  <HumanizePanel
    initialText={selectedText}
    onComplete={(result) => {
      // 替换编辑器中的文本
      replaceText(result.humanized_text);
      setShowHumanizePanel(false);
    }}
  />
</Modal>
```

---

### Phase 4: 缓存系统（2-3天）

#### 4.1 Redis缓存实现

**新文件：`backend/app/services/cache/humanize_cache.py`**

```python
import hashlib
import json
from typing import Optional
from redis.asyncio import Redis
from app.core.config import settings

class HumanizeCache:
    """AI去痕迹化结果缓存"""

    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.prefix = "humanize:"
        self.ttl = 3600  # 1小时

    def _generate_key(self, text: str, intensity: str) -> str:
        """生成缓存键"""
        content = f"{text}:{intensity}"
        hash_value = hashlib.sha256(content.encode()).hexdigest()
        return f"{self.prefix}{hash_value}"

    async def get(self, text: str, intensity: str) -> Optional[dict]:
        """获取缓存结果"""
        key = self._generate_key(text, intensity)
        cached = await self.redis.get(key)

        if cached:
            return json.loads(cached)
        return None

    async def set(self, text: str, intensity: str, result: dict):
        """保存缓存结果"""
        key = self._generate_key(text, intensity)
        await self.redis.setex(
            key,
            self.ttl,
            json.dumps(result, ensure_ascii=False)
        )

    async def exists(self, text: str, intensity: str) -> bool:
        """检查缓存是否存在"""
        key = self._generate_key(text, intensity)
        return await self.redis.exists(key)
```

#### 4.2 集成缓存到任务

**修改：`backend/app/tasks/humanize_tasks.py`**

```python
from app.services.cache.humanize_cache import HumanizeCache
from app.core.redis import get_redis

@celery_app.task(bind=True, name="humanize.process_text")
async def humanize_task(self, text, intensity, user_id, ai_function):
    try:
        # 初始化缓存
        redis = await get_redis()
        cache = HumanizeCache(redis)

        # 检查缓存
        cached_result = await cache.get(text, intensity)
        if cached_result:
            logger.info(f"命中缓存，直接返回结果")
            return {
                "success": True,
                "cached": True,
                **cached_result
            }

        # 执行处理...
        service = HumanizeService()
        result = await service.full_humanize_process(text, intensity)

        # 保存到缓存
        await cache.set(text, intensity, {
            "humanized_text": result["humanized_text"],
            "score_before": result["detection"].overall_score,
            "score_after": result.get("verification", {}).get("score_after", 0),
            "processing_time": result["processing_time"]
        })

        return {
            "success": True,
            "cached": False,
            **result
        }
    finally:
        await redis.close()
```

---

## 📊 性能对比

### 优化前 vs 优化后

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **API响应时间** | 30-40秒 | <200ms | ⭐⭐⭐⭐⭐ |
| **用户等待感知** | 完全阻塞 | 后台处理 | ⭐⭐⭐⭐⭐ |
| **缓存命中率** | 0% | 30-50% | ⭐⭐⭐⭐ |
| **重复请求成本** | 100% | 50% | ⭐⭐⭐⭐ |
| **并发处理能力** | 受限于连接池 | Worker池 | ⭐⭐⭐⭐ |

---

## 🎯 使用场景对比

### 场景1：对话中顺便提及

**用户**: "帮我写第三章的开头，写完后顺便去掉AI痕迹"

**Agent模式处理**:
```
1. Agent调用 continue_writing_tool → 生成开头
2. Agent自动调用 humanize_text_tool → 去痕迹化
3. 返回最终结果
```

**优势**: 一次对话完成多个任务

---

### 场景2：批量处理已有章节

**用户**: 选中5个章节 → 点击"批量去AI痕迹"

**独立API模式**:
```
1. 提交5个任务到队列 → 立即返回5个task_id
2. 后台Worker并行处理
3. WebSocket推送完成通知
4. 用户查看对比结果
```

**优势**: 异步批量处理，不阻塞

---

### 场景3：精细调整参数

**用户**: 打开独立面板 → 配置多个参数 → 预览对比

**独立面板模式**:
```
1. 选择强度: medium
2. 选择难度: College
3. 选择用途: Novel
4. 提交处理
5. 对比原文和改写
6. 满意后应用
```

**优势**: 精细控制，可视化对比

---

## 📅 实施时间表

| 阶段 | 任务 | 工作量 | 开始日期 | 完成日期 |
|------|------|--------|----------|----------|
| Phase 1 | 重构API为异步 | 3-5天 | Day 1 | Day 5 |
| Phase 2 | 集成Agent工具 | 2-3天 | Day 6 | Day 8 |
| Phase 3 | 前端集成 | 3-4天 | Day 9 | Day 12 |
| Phase 4 | 缓存系统 | 2-3天 | Day 13 | Day 15 |
| **总计** | | **10-15天** | | |

---

## ✅ 验收标准

### 功能验收

- [ ] Agent对话中可以自然触发去痕迹化
- [ ] 独立面板可以配置参数并处理
- [ ] API立即返回任务ID（<200ms）
- [ ] 支持状态轮询和进度显示
- [ ] 缓存命中时秒级返回
- [ ] 批量处理支持（提交多个任务）

### 性能验收

- [ ] API响应时间 < 200ms
- [ ] 缓存命中率 > 30%
- [ ] Worker处理时间 < 45秒
- [ ] 并发处理能力 > 10个任务
- [ ] 错误率 < 1%

### 用户体验验收

- [ ] 进度条实时更新
- [ ] 预估时间准确（误差<20%）
- [ ] 可以取消任务
- [ ] 结果可以对比查看
- [ ] 历史记录完整保存

---

## 🔄 兼容性保证

### 保留现有API

```python
# 旧版API保持兼容（同步模式）
@router.post("/rewrite", response_model=HumanizeSessionResponse)
async def humanize_rewrite_sync(...):
    """
    同步版本（兼容旧代码）

    ⚠️ 已废弃，建议使用 /submit + /status 异步模式
    """
    # ... 现有实现保持不变
```

### 渐进式迁移

```python
# 前端根据配置选择模式
if (useAsyncMode) {
  // 新版：异步模式
  const taskId = await humanizeApi.submit(request);
  await pollUntilComplete(taskId);
} else {
  // 旧版：同步模式
  const result = await humanizeApi.rewrite(request);
}
```

---

## 📚 参考文档

- [Celery官方文档](https://docs.celeryq.dev/)
- [LangGraph工具集成](https://langchain-ai.github.io/langgraph/tutorials/tools/)
- [Redis缓存最佳实践](https://redis.io/docs/manual/patterns/)
- [Undetectable.ai API参考](https://docs.undetectable.ai/)

---

## 🎉 总结

通过此方案，AI去痕迹化功能将获得：

1. **双入口模式** - Agent智能调用 + 独立工具面板
2. **异步处理** - 立即响应，后台处理
3. **流式进度** - 实时反馈，提升体验
4. **缓存优化** - 重复请求秒级返回
5. **灵活扩展** - 易于添加新功能

**最终目标**: 让AI去痕迹化成为用户自然使用的功能，而不是一个"慢且令人烦躁"的工具。
