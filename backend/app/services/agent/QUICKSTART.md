# Agent功能快速开始指南

## 🚀 5分钟快速体验

### 步骤1：安装依赖

```bash
pip install redis pydantic
```

### 步骤2：初始化Redis连接

```python
import redis

# 连接Redis
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=1,
    decode_responses=False  # 重要：保持为False
)
```

### 步骤3：测试长期记忆系统

```python
from app.services.agent.memory import MemoryManager

# 创建记忆管理器
memory = MemoryManager(redis_client)

# 记录用户偏好
memory.long_term_memory.update_user_preferences(
    user_id="test_user",
    preferences={
        "preferred_style": "玄幻",
        "preferred_length": "medium",
        "tone": "neutral"
    }
)

# 获取用户记忆上下文
context = memory.get_complete_context("test_user")
print(context)

# 格式化为Agent Prompt
prompt = memory.format_context_for_agent("test_user", mode="full")
print(prompt)
```

### 步骤4：测试规划Agent

```python
from app.services.agent.agents import PlanningAgent

# 创建规划Agent
planner = PlanningAgent()

# 生成小说创作计划
plan = planner.create_plan_for_novel_writing(
    user_goal="我想写一部玄幻小说",
    genre="玄幻"
)

# 查看计划
print(f"目标: {plan.goal}")
print(f"任务数: {len(plan.tasks)}")

for task in plan.tasks:
    print(f"- {task.description}")
```

### 步骤5：测试人机协同

```python
from app.services.agent.tools import HITLManager

# 创建HITL管理器
hitl = HITLManager(redis_client)

# 创建批准请求
request = hitl.create_approval_request(
    agent_id="test_agent",
    user_id="test_user",
    title="测试批准请求",
    description="这是一个测试",
    proposed_action={"action": "test"}
)

print(f"请求ID: {request.request_id}")
print(f"请求状态: {request.status}")

# 获取待处理请求
pending = hitl.get_pending_requests("test_user")
print(f"待处理请求数: {len(pending)}")
```

---

## 📚 完整示例

### 示例1：完整的小说创作流程

```python
import asyncio
from app.services.agent.memory import MemoryManager
from app.services.agent.agents import PlanningAgent
from app.services.agent.tools import HITLManager

async def create_novel_flow():
    # 初始化
    redis_client = redis.Redis(host='localhost', port=6379, db=1)
    memory = MemoryManager(redis_client)
    planner = PlanningAgent()
    hitl = HITLManager(redis_client)

    user_id = "user123"

    # 1. 加载用户记忆
    user_context = memory.get_complete_context(user_id)
    print(f"用户记忆质量: {user_context['user_context']['memory_quality']}")

    # 2. 生成创作计划
    plan = planner.create_plan_for_novel_writing(
        user_goal="我想写玄幻小说",
        genre="玄幻",
        context=user_context
    )

    print(f"已生成 {len(plan.tasks)} 个任务")

    # 3. 执行计划（带人机协同）
    async def on_task_complete(task, plan):
        """任务完成回调"""
        print(f"✅ 完成: {task.description}")

        # 如果是生成大纲，请求批准
        if task.task_type == "create_outline":
            request = hitl.create_approval_request(
                agent_id="planning_agent",
                user_id=user_id,
                title="大纲生成完成",
                description=f"已生成{len(task.result)}章大纲",
                proposed_action={"outline": task.result}
            )
            print(f"⏸️ 等待批准: {request.request_id}")

    # 开始执行
    result = await planner.execute_plan(
        plan,
        on_task_complete=on_task_complete
    )

    print(f"计划状态: {result.status}")
    print(f"进度: {result.progress * 100}%")

# 运行
asyncio.run(create_novel_flow())
```

### 示例2：风格学习和应用

```python
from app.services.agent.tools.style_learning import (
    learn_user_style,
    get_style_prompt,
    analyze_writing_style
)

# 1. 分析用户文本
user_text = """
他站在山巅，凝望着远方的云海。
寒风呼啸而过，吹得衣袍猎猎作响。
这一刻，他终于明白了师父临终前的那句话。
修道，不在于境界的高低，而在于心境的超脱。
"""

features = analyze_writing_style(user_text)
print(f"平均句长: {features.avg_sentence_length}")
print(f"叙事视角: {features.pov}")
print(f"常用词: {features.common_words}")

# 2. 学习用户风格
profile = learn_user_style(
    user_id="user123",
    text=user_text,
    profile_name="default"
)

print(f"风格档案置信度: {profile.confidence_score}")

# 3. 获取风格指导（用于生成内容时）
style_prompt = get_style_prompt("user123")
print(f"风格指导: {style_prompt}")

# 4. 在AI生成时使用
full_prompt = f"""请续写以下小说章节。

{style_prompt}

上文：
{user_text}

请继续：
"""
# 然后调用AI服务生成
```

### 示例3：Story Bible一致性检查

```python
from app.services.agent.tools.consistency_checker import check_story_consistency

# 准备数据
chapters = [
    {
        "id": "ch1",
        "content": "张三是一个身高180cm的年轻人..."
    },
    {
        "id": "ch5",
        "content": "张三身高只有170cm..."  # 矛盾
    }
]

characters = [
    {
        "id": "char1",
        "name": "张三",
        "height": "180cm",
        "first_chapter": "ch1"
    }
]

worldview = {
    "魔法系统": "这个世界的魔法需要咒语",
    "魔法限制": "魔法无需咒语，心念即可"  # 矛盾
}

# 执行检查
report = await check_story_consistency(
    work_id="work123",
    chapters=chapters,
    characters=characters,
    worldview=worldview
)

print(f"一致性得分: {report.consistency_score}/100")
print(f"发现问题: {report.total_inconsistencies}个")

for issue in report.inconsistencies:
    print(f"\n[{issue.severity.upper()}]")
    print(f"问题: {issue.description}")
    print(f"建议: {issue.suggestion}")
```

### 示例4：并行批量生成

```python
from app.services.agent.agents.parallel_executor import parallel_map

# 定义生成函数
async def generate_chapter_outline(chapter_num: int):
    """生成单个章节大纲"""
    # 这里应该调用实际的AI服务
    await asyncio.sleep(1)  # 模拟API调用
    return {
        "chapter": chapter_num,
        "title": f"第{chapter_num}章",
        "summary": f"第{chapter_num}章的情节..."
    }

# 并行生成10个章节大纲
chapter_numbers = list(range(1, 11))

results = await parallel_map(
    items=chapter_numbers,
    async_fn=generate_chapter_outline,
    max_concurrent=5  # 最多5个并发
)

print(f"生成了 {len(results)} 个大纲")
for outline in results:
    print(f"- {outline['title']}: {outline['summary']}")
```

---

## 🔧 配置建议

### Redis配置

```python
# config/redis.py
import redis

def get_redis_client():
    """获取Redis客户端"""
    return redis.Redis(
        host='localhost',
        port=6379,
        db=1,
        decode_responses=False,
        max_connections=50
    )
```

### Agent配置

```python
# config/agent.py

AGENT_CONFIG = {
    # 记忆系统
    "memory": {
        "ttl_days": 90,  # 记忆保留90天
        "max_conversations": 50  # 最多保留50个会话摘要
    },

    # HITL配置
    "hitl": {
        "default_timeout_hours": 2,  # 默认2小时超时
        "require_approval_for": [
            "create_outline",  # 生成大纲需要批准
            "create_worldview",  # 创建世界观需要批准
            "batch_operation"  # 批量操作需要批准
        ]
    },

    # 反思机制
    "reflection": {
        "quality_threshold": 80.0,  # 质量阈值
        "max_iterations": 3  # 最多迭代3次
    },

    # 并行执行
    "parallel": {
        "max_concurrent": 5  # 最大并发数
    },

    # 风格学习
    "style": {
        "min_samples": 3,  # 至少3个样本才可靠
        "min_words": 300  # 每个样本至少300字
    }
}
```

---

## 🐛 常见问题

### Q1: Redis连接失败

```python
# 解决方案：检查Redis是否启动
redis-cli ping  # 应该返回PONG

# 或者使用Docker启动Redis
docker run -d -p 6379:6379 redis:latest
```

### Q2: 记忆数据丢失

```python
# 检查TTL设置
redis_client.ttl("user:user123:preferences")

# 如果返回-1，说明没有设置过期时间
# 如果返回-2，说明key不存在
```

### Q3: Agent执行卡住

```python
# 使用超时机制
import asyncio

try:
    result = await asyncio.wait_for(
        planner.execute_plan(plan),
        timeout=300  # 5分钟超时
    )
except asyncio.TimeoutError:
    print("执行超时")
```

---

## 📈 性能优化建议

### 1. Redis连接池

```python
import redis

pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=1,
    max_connections=50
)

redis_client = redis.Redis(connection_pool=pool)
```

### 2. 批量操作

```python
# 使用pipeline批量操作
pipe = redis_client.pipeline()
for i in range(100):
    pipe.set(f"key_{i}", f"value_{i}")
pipe.execute()
```

### 3. 异步执行

```python
# 使用asyncio并发执行
tasks = [
    analyze_chapter(ch1),
    analyze_chapter(ch2),
    analyze_chapter(ch3)
]

results = await asyncio.gather(*tasks)
```

---

## 📝 测试

### 单元测试示例

```python
# tests/test_memory.py
import pytest
from app.services.agent.memory import LongTermMemoryService

def test_user_preferences():
    redis_client = get_test_redis_client()
    memory = LongTermMemoryService(redis_client)

    # 更新偏好
    prefs = memory.update_user_preferences(
        "test_user",
        {"preferred_style": "玄幻"}
    )

    assert prefs.preferred_style == "玄幻"

    # 获取偏好
    retrieved = memory.get_user_preferences("test_user")
    assert retrieved.preferred_style == "玄幻"
```

---

## 🎓 学习资源

1. **LangGraph教程**: https://langchain-ai.github.io/langgraph/tutorials/
2. **Redis Python客户端**: https://redis-py.readthedocs.io/
3. **Pydantic文档**: https://docs.pydantic.dev/

---

**祝你使用愉快！** 🎉

如有问题，请查看 [README.md](./README.md) 或联系开发团队。
