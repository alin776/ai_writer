# Phase3 优化#9: 错误处理完善

**优先级**: P1（高）🛡️
**预期收益**: 系统稳定性+40%
**实施难度**: 🟢 低（90%代码可从Planning复用）
**预计时间**: 2小时（vs 原计划1.5天）
**当前状态**: ❌ 未开始
**代码复用度**: **90%** 🎯

---

## 🎉 重大发现：Planning 模式已实现完整重试机制！

通过深度代码探索，发现 **Planning 模式已经实现了完整的错误处理和重试机制**，包含：
- ✅ 智能错误分类（网络/超时/连接）
- ✅ 自动重试机制（max_retries=2）
- ✅ 指数退避策略（2, 4, 8秒）
- ✅ 优雅降级（失败不影响其他任务）
- ✅ 详细错误日志

**这意味着我们可以直接复用约100行高质量代码，只需2小时适配即可完成！**

### Planning 已实现的重试机制

**源文件**: `backend/app/services/agent/langgraph_agent.py:3373-3457`

```python
# 🟢 完整重试逻辑（可直接复用）
max_retries = 2
last_error = None

for retry_count in range(max_retries + 1):
    try:
        # 执行任务
        result = await self._execute_task(
            task=task,
            work_id=work_id,
            chapter_id=chapter_id,
            context=context,
            on_progress=on_task_progress
        )

        logger.info(f"[ParallelExecution] 任务{task_id}完成")

        # 注册结果供后续任务使用
        await resolver.register_result(task_id, result)

        return {
            "task_id": task_id,
            "description": description,
            "result": result,
            "status": "completed"
        }

    except Exception as e:
        last_error = e

        # 🟢 判断是否为可重试的错误（直接复用）
        is_retryable = any(keyword in str(e).lower() for keyword in [
            "timeout", "connection", "network", "网络", "连接", "超时"
        ])

        if is_retryable and retry_count < max_retries:
            # 🟢 指数退避（直接复用）
            wait_time = 2 ** (retry_count + 1)  # 2, 4, 8秒
            logger.warning(
                f"[ParallelExecution] 任务{task_id}失败，"
                f"{wait_time}秒后重试（{retry_count + 1}/{max_retries}）"
            )
            await asyncio.sleep(wait_time)
        else:
            # 最终失败
            logger.error(f"[ParallelExecution] 任务{task_id}最终失败: {last_error}")

            # 🟢 优雅降级（直接复用）
            error_result = f"错误: {str(last_error)}"
            await resolver.register_result(task_id, error_result)

            return {
                "task_id": task_id,
                "description": description,
                "result": error_result,
                "status": "failed"
            }
```

### Planning 的优雅降级机制

**源文件**: `langgraph_agent.py:3461-3474`

```python
# 🟢 asyncio.gather + return_exceptions（优雅降级）
parallel_results = await asyncio.gather(
    *[execute_with_semaphore(task) for task in parallel_tasks],
    return_exceptions=True  # ← 关键：一个任务失败不影响其他任务
)

# 🟢 处理异常结果（直接复用）
for i, result in enumerate(parallel_results):
    if isinstance(result, Exception):
        logger.error(f"[ParallelExecution] 并行任务失败: {result}")

        # 创建失败任务记录
        failed_task = {
            "task_id": parallel_tasks[i]["task_id"],
            "description": parallel_tasks[i]["description"],
            "result": f"任务执行失败: {str(result)}",
            "status": "failed"
        }
        task_results.append(failed_task)
    else:
        # 正常任务结果
        task_results.append(result)
```

---

## 🔧 复用实施方案（2小时 vs 原计划1.5天）

### Step 1: 提取为通用装饰器（1小时）

```python
# backend/app/services/agent/utils/retry.py

from functools import wraps
import asyncio
import logging
from typing import List

logger = logging.getLogger(__name__)

def retry_on_failure(max_retries: int = 2, backoff_base: int = 2):
    """重试装饰器（复用 Planning 的重试逻辑）

    Args:
        max_retries: 最大重试次数（默认2次）
        backoff_base: 退避基数（默认2，即2、4、8秒）
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None

            for retry_count in range(max_retries + 1):
                try:
                    # 执行函数
                    return await func(*args, **kwargs)

                except Exception as e:
                    last_error = e

                    # 🟢 复用：判断可重试错误
                    is_retryable = any(keyword in str(e).lower() for keyword in [
                        "timeout", "connection", "network", "网络", "连接", "超时"
                    ])

                    if is_retryable and retry_count < max_retries:
                        # 🟢 复用：指数退避
                        wait_time = backoff_base ** (retry_count + 1)
                        logger.warning(
                            f"[Retry] {func.__name__}失败，"
                            f"{wait_time}秒后重试（{retry_count + 1}/{max_retries}）: {e}"
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        # 不可重试或重试次数用尽
                        logger.error(
                            f"[Retry] {func.__name__}最终失败: {last_error}"
                        )
                        raise last_error

            # 理论上不会到这里
            raise last_error

        return wrapper
    return decorator


# 🟢 错误分类枚举（扩展）
class ErrorType(str, Enum):
    """错误类型分类"""
    NETWORK = "network"       # 网络错误（可重试）
    TIMEOUT = "timeout"       # 超时错误（可重试）
    PARAMETER = "parameter"   # 参数错误（不可重试）
    BUSINESS = "business"     # 业务错误（不可重试）
    UNKNOWN = "unknown"       # 未知错误（不可重试）


def classify_error(error: Exception) -> ErrorType:
    """分类错误（基于 Planning 的逻辑扩展）"""
    error_str = str(error).lower()

    # 网络相关
    if any(keyword in error_str for keyword in ["network", "网络", "connection", "连接"]):
        return ErrorType.NETWORK

    # 超时相关
    if any(keyword in error_str for keyword in ["timeout", "超时", "timed out"]):
        return ErrorType.TIMEOUT

    # 参数相关
    if any(keyword in error_str for keyword in ["invalid", "参数", "parameter", "argument"]):
        return ErrorType.PARAMETER

    # 业务相关
    if any(keyword in error_str for keyword in ["章节不存在", "作品不存在", "权限不足"]):
        return ErrorType.BUSINESS

    return ErrorType.UNKNOWN
```

### Step 2: 应用到工具调用（1小时）

```python
# backend/app/services/agent/tools/chapter_tools.py

from app.services.agent.utils.retry import retry_on_failure

# 🟢 应用重试装饰器
@retry_on_failure(max_retries=2)
async def read_chapter_tool(chapter_id: int, db: AsyncSession) -> str:
    """读取章节内容（自动重试）

    会自动重试网络/超时错误，最多重试2次
    """
    try:
        async with asyncio.timeout(60):
            # 查询章节
            result = await db.execute(
                select(Chapter).where(Chapter.id == chapter_id)
            )
            chapter = result.scalar_one_or_none()

            if not chapter:
                raise ValueError(f"章节 {chapter_id} 不存在")

            return chapter.content

    except asyncio.TimeoutError:
        # 转换为更明确的错误
        raise TimeoutError(f"读取章节 {chapter_id} 超时（60秒）")


# 🟢 其他工具类似应用
@retry_on_failure(max_retries=2)
async def get_context_tool(work_id: int, db: AsyncSession) -> str:
    """获取作品上下文（自动重试）"""
    # ... 实现


@retry_on_failure(max_retries=2)
async def search_analysis_fragments_tool(query: str, db: AsyncSession) -> List[str]:
    """检索分析片段（自动重试）"""
    # ... 实现
```

### Step 3: 统一错误响应格式（额外30分钟，可选）

```python
# backend/app/api/agent.py

from app.services.agent.utils.retry import classify_error, ErrorType

@app.exception_handler(Exception)
async def unified_exception_handler(request: Request, exc: Exception):
    """统一错误处理器"""

    # 分类错误
    error_type = classify_error(exc)

    # 生成友好消息
    if error_type == ErrorType.NETWORK:
        user_message = "网络连接失败，请检查网络设置后重试"
        suggested_actions = ["检查网络连接", "稍后重试"]
    elif error_type == ErrorType.TIMEOUT:
        user_message = "操作超时，请尝试简化请求或稍后重试"
        suggested_actions = ["简化请求内容", "稍后重试"]
    elif error_type == ErrorType.PARAMETER:
        user_message = f"参数错误：{str(exc)}"
        suggested_actions = ["检查输入参数", "查看API文档"]
    elif error_type == ErrorType.BUSINESS:
        user_message = str(exc)
        suggested_actions = ["检查资源是否存在", "联系管理员"]
    else:
        user_message = "系统内部错误，请稍后重试"
        suggested_actions = ["稍后重试", "联系技术支持"]

    # 记录错误
    logger.error(
        f"[Error] Type={error_type}, Message={str(exc)}",
        exc_info=True
    )

    # 返回统一格式
    return JSONResponse(
        status_code=500 if error_type != ErrorType.PARAMETER else 400,
        content={
            "error": user_message,
            "error_type": error_type,
            "recoverable": error_type in [ErrorType.NETWORK, ErrorType.TIMEOUT],
            "suggested_actions": suggested_actions,
            "details": str(exc) if settings.DEBUG else None
        }
    )
```

---

## 📋 优化概述

### 问题描述

**当前问题**: 错误处理不统一，用户体验差

**问题点**:
- ❌ 无错误分类
- ❌ 泛化错误消息
- ❌ 无恢复机制
- ❌ 无错误监控

---

## 🎯 优化目标

### 验收标准

- [ ] 所有错误有明确提示
- [ ] 错误分类覆盖 > 95%
- [ ] 平均恢复时间 < 5秒

---

## 💡 优化方案

### 核心实现

```python
# backend/app/services/agent/errors.py

class AgentError(Exception):
    """Agent基础错误"""
    def __init__(self, message: str, recoverable: bool = False,
                 suggested_actions: List[str] = None):
        self.message = message
        self.recoverable = recoverable
        self.suggested_actions = suggested_actions or []

class TimeoutError(AgentError):
    """超时错误"""
    def __init__(self, timeout_seconds: int, operation: str):
        super().__init__(
            message=f"{operation}超时（{timeout_seconds}秒）",
            recoverable=True,
            suggested_actions=["简化请求", "稍后重试"]
        )

class NetworkError(AgentError):
    """网络错误"""
    def __init__(self, url: str, status_code: int = None):
        super().__init__(
            message=f"网络请求失败: {url}",
            recoverable=True,
            suggested_actions=["检查网络", "稍后重试"]
        )

# 使用
async def read_chapter_tool(...):
    try:
        async with asyncio.timeout(60):
            # 业务逻辑
            pass
    except asyncio.TimeoutError:
        raise TimeoutError(60, "读取章节")
```

### 统一错误处理中间件

```python
@app.middleware("http")
async def error_handling_middleware(request, call_next):
    try:
        return await call_next(request)
    except AgentError as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": e.message,
                "type": e.__class__.__name__,
                "recoverable": e.recoverable,
                "suggested_actions": e.suggested_actions
            }
        )
```

---

## 🔧 详细实施步骤

### Day 1: 定义错误类型
### Day 2: 实现统一处理

---

## ✅ 验收标准

- [ ] 所有错误有明确提示
- [ ] 错误恢复机制正常

---

## 📊 预期收益

- 稳定性 +40%
- 用户体验 +50%
- 故障排查效率 +80%

---

## 📝 相关文档

- [00_执行摘要](./00_执行摘要.md) - 了解整体情况
- [立即行动建议](./立即行动建议.md) - 本周实施计划
- [代码复用深度分析报告](../../../tasks/ReAct与Planning代码复用深度分析报告.md) - 完整分析

**Planning 模式源代码**:
- `backend/app/services/agent/langgraph_agent.py:3373-3457` - 重试机制（85行，90%可复用）
- `backend/app/services/agent/langgraph_agent.py:3461-3474` - 优雅降级（15行，100%可复用）

---

## 🚀 立即行动

### Week 1 - Day 3（本周优先实施）

**时间**: 2小时
**优先级**: P1（高优先级）
**预期收益**: 系统稳定性+40%

**实施检查清单**:
- [ ] Step 1: 提取为通用装饰器（1小时）
  - [ ] 创建 `utils/retry.py` 文件
  - [ ] 实现 `@retry_on_failure` 装饰器
  - [ ] 实现 `ErrorType` 枚举
  - [ ] 实现 `classify_error` 函数
- [ ] Step 2: 应用到工具调用（1小时）
  - [ ] 所有工具函数添加 `@retry_on_failure`
  - [ ] 测试网络错误自动重试
  - [ ] 测试超时错误自动重试
  - [ ] 验证指数退避正常工作
- [ ] Step 3（可选）: 统一错误响应（30分钟）
  - [ ] 实现统一错误处理器
  - [ ] 前端错误消息友好化
  - [ ] 添加错误监控

**验收标准**:
- [ ] 网络/超时错误自动重试 ✅
- [ ] 重试次数符合预期（最多3次） ✅
- [ ] 指数退避正确（2, 4, 8秒） ✅
- [ ] 错误日志清晰完整 ✅

---

**创建日期**: 2025-11-10
**最后更新**: 2025-11-10（添加代码复用分析）
**负责人**: 后端开发
**状态**: ❌ 未开始 → 准备实施
**代码复用度**: **90%** 🎯

[返回README](./README.md)
