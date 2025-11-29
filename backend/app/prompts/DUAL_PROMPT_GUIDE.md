# 双Prompt架构使用指南

## 概述

将Agent的Prompt拆分为两层：
- **系统层Prompt**（`system_agent_prompt.yaml`）：轻量级，专注逻辑判断和工具调用决策
- **创作层Prompt**（`creative_writing_prompt.yaml`）：重量级，专注内容质量和文学指导

## 架构对比

### 之前（单Prompt）
```
用户输入 → Agent（单个Prompt，2000+ tokens）
         ├─ 50%算力：逻辑判断（哪个工具？什么参数？）
         └─ 50%算力：内容创作（生成文字）
         → 输出质量：⭐⭐⭐
```

### 现在（双Prompt）
```
用户输入 → Agent（系统层Prompt，500 tokens）
         └─ 100%算力：决策逻辑
         → 调用工具

工具返回 → Agent（创作层Prompt，800 tokens + Few-Shot）
         └─ 100%算力：内容创作
         → 输出质量：⭐⭐⭐⭐⭐
```

## 代码集成示例

### 1. 加载Prompt模板

```python
# backend/app/services/agent/langgraph_agent.py

import yaml
from pathlib import Path

class LangGraphAgent:
    def __init__(self):
        prompt_dir = Path(__file__).parent.parent / "prompts" / "templates"

        # 加载系统层Prompt（轻量级）
        with open(prompt_dir / "system_agent_prompt.yaml") as f:
            self.system_prompt_template = yaml.safe_load(f)

        # 加载创作层Prompt（重量级）
        with open(prompt_dir / "creative_writing_prompt.yaml") as f:
            self.creative_prompt_template = yaml.safe_load(f)
```

### 2. 阶段1：使用系统层Prompt做决策

```python
async def _handle_writing_task(self, state: AgentState):
    """处理写作任务的两阶段流程"""

    # === 阶段1：决策阶段 ===
    # 使用系统层Prompt（轻量级，专注逻辑）
    system_prompt = self.system_prompt_template["template"].format(
        user_message=state["messages"][-1].content
    )

    # LLM决策：调用哪些工具
    decision_response = await self.llm_with_tools.ainvoke([
        SystemMessage(content=system_prompt),
        *state["messages"]
    ])

    # 执行工具调用
    if decision_response.tool_calls:
        for tool_call in decision_response.tool_calls:
            if tool_call["name"] == "read_chapter_tool":
                chapter_content = await self._execute_tool(tool_call)
            elif tool_call["name"] == "smart_rewrite":
                # 继续到阶段2
                return await self._generate_rewrite_content(
                    state,
                    tool_call["args"],
                    chapter_content
                )
```

### 3. 阶段2：使用创作层Prompt生成内容

```python
async def _generate_rewrite_content(
    self,
    state: AgentState,
    rewrite_args: Dict,
    chapter_content: str
):
    """使用创作层Prompt生成高质量改写内容"""

    # === 阶段2：创作阶段 ===
    # 使用创作层Prompt（重量级，包含Few-Shot）
    creative_prompt = self.creative_prompt_template["template"].format(
        task_type="rewrite",
        original_text=rewrite_args["text_to_rewrite"],
        user_requirement=rewrite_args.get("user_requirement", ""),
        base_version=rewrite_args.get("base_version", ""),
        style_reference=chapter_content[:500],  # 取前500字作为风格参考
        current_plot=state.get("context", {}).get("plot_state", ""),
        character_context=state.get("context", {}).get("characters", "")
    )

    # LLM创作：100%算力专注于内容质量
    creative_response = await self.ai_service.call_ai(
        system_prompt="你是资深网文作家，专注于高质量内容创作。",
        user_prompt=creative_prompt,
        max_tokens=4000,
        temperature=0.8,
        task_type=TaskType.CONTENT_CREATION
    )

    return creative_response
```

### 4. 动态注入风格参考

```python
def _extract_style_reference(self, chapter_content: str) -> str:
    """从章节中提取风格参考（前500字）"""
    if not chapter_content:
        return ""

    # 取前500字，去除HTML标签
    import re
    text = re.sub(r'<[^>]+>', '', chapter_content)
    return text[:500]
```

## 效果预期

### Token消耗对比

| 阶段 | 之前（单Prompt） | 现在（双Prompt） |
|------|-----------------|-----------------|
| 决策阶段 | 2000 tokens（包含无关的创作指导） | 500 tokens（纯逻辑） |
| 创作阶段 | 2000 tokens（包含无关的工具说明） | 800 tokens（纯创作+Few-Shot） |
| **总计** | **2000 tokens** | **1300 tokens** |
| **节省** | - | **35%** |

### 质量对比

**改写任务："白光退去太平淡"**

**之前输出**：
```
版本A：白光缓缓退去，神女终于看清了勇者的背影，心中涌起复杂的情绪。
版本B：白光散去，神女的目光落在勇者的身影上。
版本C：当白光消失后，勇者的背影映入神女眼帘。
```
*评价*：平淡、公式化，3个版本差异不大

**现在输出（预期）**：
```
版本A：白光如潮水褪去，她终于看见他——那个背影孤绝如剑，站在天地之间，再无半分温度。

版本B：光芒碎裂成千万缕星尘，她看见了他的背影，笔直、冰冷，像一座不会回头的山。

版本C：白光退散的一瞬，她看见他的背影，那样决绝，仿佛在告诉她：这一别，便是永别。
```
*评价*：有画面感、有情绪、有意境，3个版本各具特色

## 实施步骤

### 第1步：测试系统层Prompt（已完成 ✅）
- 创建 `system_agent_prompt.yaml`
- 专注于意图识别和工具调用决策

### 第2步：测试创作层Prompt（已完成 ✅）
- 创建 `creative_writing_prompt.yaml`
- 包含10组Few-Shot示例
- 支持动态注入风格参考

### 第3步：修改Agent代码（待实施）
在 `langgraph_agent.py` 中：
1. 加载两个Prompt模板
2. 实现两阶段调用逻辑
3. 动态注入上下文（风格参考、剧情状态等）

### 第4步：测试验证（待实施）
测试场景：
- [x] 基础改写："白光退去太平淡"
- [ ] 用户自定义要求："加强情感描写"
- [ ] 迭代改进："在第二版基础上再改"
- [ ] 用户给出最终版本："改成XXX"
- [ ] 续写任务

## 注意事项

1. **保持向后兼容**：
   - 旧的 `writing_agent.yaml` 暂时保留
   - 可以通过配置开关切换新旧模式

2. **性能监控**：
   - 记录两阶段调用的总耗时
   - 对比单Prompt和双Prompt的延迟差异

3. **质量评估**：
   - 收集用户反馈
   - A/B测试对比输出质量

4. **逐步迁移**：
   - 先在部分用户上测试
   - 验证稳定后全量上线

## 下一步

1. 修改 `langgraph_agent.py`，实现双Prompt调用逻辑
2. 添加配置开关，支持新旧模式切换
3. 进行测试验证
4. 根据效果调整Prompt内容
