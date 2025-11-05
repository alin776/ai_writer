# AI_Gen_Novel 上下文压缩方案

## 📋 方案概述

**项目名称：** AI_Gen_Novel
**压缩策略：** 滚动记忆压缩（Rolling Memory Compression）
**核心思想：** 增量式压缩，累积一定量新内容后才触发AI摘要生成

---

## 🎯 设计理念

### 问题场景

在长篇小说创作中，随着章节增加，上下文会无限膨胀：

```
第1章：3000字
第2章：3000字
...
第50章：3000字

总计：150,000字 ≈ 100,000 tokens
```

如果每次生成新章节都发送所有历史内容：
- 💰 成本：$1.25（按Gemini 2.5 Pro计算）
- ⏱️ 时间：15-20秒
- 📊 Token：100,000+

### 解决方案

**AI_Gen_Novel 的策略：**
1. 不保存完整历史，只保留**压缩后的记忆**
2. 新内容先累积，超过阈值才触发压缩
3. 用AI生成的摘要替代完整内容

---

## 🏗️ 技术架构

### 核心数据结构

```python
class AIGN:
    def __init__(self, chatLLM):
        # 核心存储
        self.writing_memory = ""           # 压缩后的历史记忆（重要！）
        self.no_memory_paragraph = ""      # 还未压缩的新内容
        self.paragraph_list = []            # 所有段落的完整列表

        # 辅助信息
        self.novel_outline = ""             # 小说大纲
        self.writing_plan = ""              # 当前写作计划
        self.temp_setting = ""              # 临时设定

        # 专门的记忆生成Agent
        self.memory_maker = MarkdownAgent(
            chatLLM=self.chatLLM,
            sys_prompt=memory_maker_prompt,  # 记忆生成提示词
            temperature=0.66,                # 较低温度保证稳定性
        )
```

### 关键字段说明

| 字段 | 作用 | 示例 |
|------|------|------|
| `writing_memory` | 存储压缩后的历史摘要 | "前49章：主角从普通学生成长为强者，经历了..." |
| `no_memory_paragraph` | 暂存未压缩的新内容 | "第50章内容：主角进入秘境..." |
| `paragraph_list` | 完整段落列表（用于最终输出） | ["第1章...", "第2章...", ...] |

---

## 🔄 工作流程

### 完整流程图

```
┌─────────────────┐
│  生成新段落     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 累积到临时区域  │ ← no_memory_paragraph += new_content
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 检查长度        │ ← if len(no_memory_paragraph) > 2000
└────────┬────────┘
         │
    ┌────┴────┐
    │ >= 2000?│
    └────┬────┘
         │
    YES ─┼─ NO → 继续累积
         │
         ▼
┌─────────────────┐
│ 调用AI压缩      │ ← memory_maker.invoke()
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 更新记忆        │ ← writing_memory = new_summary
│ 清空临时区域    │ ← no_memory_paragraph = ""
└─────────────────┘
```

### 详细步骤

#### 步骤1：生成新段落

```python
def genNextParagraph(self, user_requriments=None, embellishment_idea=None):
    # 使用当前记忆生成新内容
    resp = self.novel_writer.invoke(
        inputs={
            "大纲": self.novel_outline,
            "前文记忆": self.writing_memory,        # ← 使用压缩记忆
            "临时设定": self.temp_setting,
            "计划": self.writing_plan,
            "上文内容": self.getLastParagraph(),    # ← 只保留最近2000字
        },
        output_keys=["段落", "计划", "临时设定"],
    )

    next_paragraph = resp["段落"]

    # 添加到段落列表
    self.paragraph_list.append(next_paragraph)

    # 累积到临时区域（关键！）
    self.no_memory_paragraph += f"\n{next_paragraph}"

    # 触发压缩检查
    self.updateMemory()

    return next_paragraph
```

#### 步骤2：检查并触发压缩

```python
def updateMemory(self):
    """当未压缩内容超过2000字时，触发压缩"""

    # 阈值判断
    if len(self.no_memory_paragraph) > 2000:

        # 调用AI生成新记忆
        resp = self.memory_maker.invoke(
            inputs={
                "前文记忆": self.writing_memory,      # 旧记忆
                "正文内容": self.no_memory_paragraph,  # 新内容
            },
            output_keys=["新的记忆"],
        )

        # 更新压缩记忆
        self.writing_memory = resp["新的记忆"]

        # 清空临时区域
        self.no_memory_paragraph = ""
```

#### 步骤3：获取上下文（生成时使用）

```python
def getLastParagraph(self, max_length=2000):
    """只保留最近的段落（最多2000字）"""
    last_paragraph = ""

    # 从后往前累积段落
    for i in range(0, len(self.paragraph_list)):
        next_para = self.paragraph_list[-1 - i]

        if (len(last_paragraph) + len(next_para)) < max_length:
            last_paragraph = next_para + "\n" + last_paragraph
        else:
            break  # 超过长度限制就停止

    return last_paragraph
```

---

## 📝 记忆生成提示词

### memory_maker_prompt 核心内容

```python
memory_maker_prompt = """
# Role:
网络小说作家

## Background And Goals:
作为长篇网络小说的作者，你面临一个挑战：记忆力不足，经常忘记之前写过的内容。
为了解决这个问题，你需要系统地记录之前的写作内容，形成"前文记忆"。

## Inputs:
- 前文记忆：之前已压缩的记忆内容
- 正文内容：新写的内容（约2000字）

## Outputs:
以固定格式输出：
```
# 新的记忆
结合前文记忆和正文内容，总结并记录下新的重要信息和剧情要点。
# END
```

## Workflows:
1. **前文回顾**：回顾之前的记忆，了解故事发展
2. **内容提炼**：从新内容中提取核心信息和剧情要点
3. **记忆更新**：将新信息整合到记忆中，保持连贯性
4. **质量检验**：确保记忆准确反映所有重要元素
5. **记忆输出**：以规范格式输出更新后的记忆

重点记录：
- 人物发展和变化
- 重要事件和转折点
- 关键设定和伏笔
- 情节推进方向
"""
```

### 生成示例

**输入：**
```
前文记忆：
主角林风是一名普通高中生，意外获得了修仙系统。
经过三个月修炼，他突破到了筑基期。
在学校遇到了神秘的转学生苏雪，后来得知她是修仙家族的后代。

正文内容：
第50章：林风和苏雪一起参加了宗门试炼...（2000字）
第51章：试炼中遭遇强敌，林风觉醒了特殊能力...（2000字）
```

**输出：**
```
# 新的记忆
主角林风原本是普通高中生，获得修仙系统后突破到筑基期。
遇到修仙家族后代苏雪并成为朋友。
最近两章：林风和苏雪参加宗门试炼，遭遇强敌时觉醒了雷属性特殊能力，
成功通过试炼并引起了宗门长老的注意。当前实力：筑基后期。
# END
```

---

## 💡 实现细节

### 1. 压缩时机选择

**为什么是 2000 字？**

```python
# 经验值设定
COMPRESSION_THRESHOLD = 2000

# 理由：
# 1. 对话历史限制：避免单次对话过长
# 2. Token成本：约1500 tokens，成本可控
# 3. 语义完整性：2000字通常包含1-2个完整段落
# 4. 压缩效率：既不过于频繁，也不过于稀疏
```

### 2. 温度参数设置

```python
# 不同Agent使用不同温度

self.novel_outline_writer = MarkdownAgent(
    temperature=0.98  # 高创造性，生成创意大纲
)

self.novel_writer = MarkdownAgent(
    temperature=0.81  # 中等创造性，写作内容
)

self.memory_maker = MarkdownAgent(
    temperature=0.66  # 低温度，保证摘要稳定和准确
)
```

**为什么记忆生成用低温度？**
- ✅ 需要准确提取关键信息，不能发挥创造力
- ✅ 避免产生幻觉或遗漏重要细节
- ✅ 保持摘要风格的一致性

### 3. 上下文组成

每次生成新内容时，发送给AI的上下文包括：

```python
context = {
    "大纲": self.novel_outline,           # 完整大纲（约1000字）
    "前文记忆": self.writing_memory,      # 压缩记忆（约500-1000字）
    "临时设定": self.temp_setting,        # 临时设定（约200字）
    "计划": self.writing_plan,            # 写作计划（约100字）
    "上文内容": self.getLastParagraph(), # 最近段落（最多2000字）
}

# 总Token估算：(1000+1000+200+100+2000) = 4,300字 ≈ 3,000 tokens
```

---

## 📊 性能分析

### Token消耗对比

| 生成场景 | 不压缩 | AI_Gen_Novel压缩 | 节省率 |
|---------|--------|------------------|--------|
| **生成第10章** | 30,000 tokens | 3,000 tokens | **90%** |
| **生成第50章** | 150,000 tokens | 3,000 tokens | **98%** |
| **生成第100章** | 300,000 tokens | 3,000 tokens | **99%** |

### 成本对比（以Gemini 2.5 Pro为例）

| 章节数 | 不压缩成本 | 压缩后成本 | 节省金额 |
|--------|-----------|-----------|---------|
| **10章** | $0.375 | $0.00375 | $0.37 |
| **50章** | $1.875 | $0.00375 | $1.87 |
| **100章** | $3.75 | $0.00375 | $3.75 |

**结论：** 章节越多，节省越明显！

### 时间消耗对比

```
不压缩方式：
- 第50章生成：15-20秒（处理150K tokens）

AI_Gen_Novel方式：
- 第50章生成：2-3秒（处理3K tokens）
- 偶尔触发压缩：+5秒（每2000字一次）
- 平均时间：3-4秒

时间节省：~75%
```

---

## ✅ 优点

1. **实现极其简单**
   - 只需要一个记忆生成Agent
   - 代码量少，易于维护
   - 不需要额外的数据库或依赖

2. **Token节省显著**
   - 节省率高达 97-99%
   - 成本几乎恒定（不随章节增长）

3. **适合线性创作**
   - 小说、故事等连续性内容
   - 时间线清晰的场景

4. **质量可控**
   - 通过调整temperature控制稳定性
   - 摘要生成可验证和调试

---

## ⚠️ 缺点

1. **记忆不可逆**
   - 一旦压缩，原始细节无法恢复
   - 如果压缩质量差，会影响后续生成

2. **无智能检索**
   - 不能根据需要查找特定信息
   - 只能使用最新的压缩记忆

3. **无去重机制**
   - 可能重复记录相似内容
   - 记忆膨胀需要人工调整提示词

4. **单一维度**
   - 只有一个记忆字段
   - 不能分类管理角色、设定、情节等

---

## 🔧 改进建议

### 1. 分类记忆

```python
class ImprovedAIGN(AIGN):
    def __init__(self, chatLLM):
        super().__init__(chatLLM)

        # 分类记忆存储
        self.character_memory = {}  # 角色记忆
        self.plot_memory = ""       # 情节记忆
        self.setting_memory = ""    # 设定记忆
```

### 2. 可配置阈值

```python
def updateMemory(self, threshold=2000):
    """允许动态调整压缩阈值"""
    if len(self.no_memory_paragraph) > threshold:
        # 压缩逻辑...
```

### 3. 记忆版本控制

```python
class MemoryVersion:
    def __init__(self):
        self.versions = []  # 记忆历史版本

    def save_version(self, memory):
        self.versions.append({
            "timestamp": datetime.now(),
            "content": memory,
            "chapter": current_chapter
        })
```

### 4. 质量评估

```python
async def evaluate_memory_quality(self, memory, original):
    """评估压缩质量"""
    prompt = f"""
    原始内容关键点：{extract_keypoints(original)}
    压缩记忆：{memory}

    评估压缩质量（0-10分）：
    - 是否保留了关键信息？
    - 是否遗漏了重要细节？
    - 是否引入了错误信息？
    """
    score = await ai_evaluate(prompt)
    return score
```

---

## 📖 使用示例

### 完整代码示例

```python
from AI_Gen_Novel.AIGN import AIGN
from AI_Gen_Novel.LLM import get_chatLLM

# 初始化
chatLLM = get_chatLLM(api_key="your_key")
novel_gen = AIGN(chatLLM)

# 1. 生成大纲
outline = novel_gen.genNovelOutline(
    user_idea="一个关于修仙的故事，主角从凡人成长为强者"
)
print("大纲：", outline)

# 2. 生成开头
beginning = novel_gen.genBeginning()
print("开头：", beginning)

# 3. 连续生成50章
for i in range(50):
    print(f"\n=== 生成第 {i+1} 章 ===")

    # 生成新段落
    paragraph = novel_gen.genNextParagraph()
    print(f"段落长度：{len(paragraph)}")

    # 查看记忆状态
    print(f"压缩记忆长度：{len(novel_gen.writing_memory)}")
    print(f"未压缩内容长度：{len(novel_gen.no_memory_paragraph)}")

    # 保存进度
    novel_gen.recordNovel()  # 保存到 novel_record.md

# 4. 输出最终小说
print("\n完整小说内容：")
print(novel_gen.novel_content)
```

### 输出示例

```
=== 生成第 1 章 ===
段落长度：2000
压缩记忆长度：0
未压缩内容长度：2000

=== 生成第 2 章 ===
段落长度：2000
压缩记忆长度：500      ← 第一次压缩触发
未压缩内容长度：0

=== 生成第 3 章 ===
段落长度：2000
压缩记忆长度：500
未压缩内容长度：2000

=== 生成第 4 章 ===
段落长度：2000
压缩记忆长度：800      ← 第二次压缩触发
未压缩内容长度：0

...
```

---

## 📚 相关资源

- **源代码位置：** `D:\Java\NovelAIde\AI_Gen_Novel\AIGN.py`
- **提示词定义：** `D:\Java\NovelAIde\AI_Gen_Novel\AIGN_Prompt.py`
- **项目对比：** [03-方案对比分析.md](./03-方案对比分析.md)

---

## 🎯 适用场景总结

✅ **推荐使用：**
- 长篇小说创作
- 连续性博客文章
- 线性剧情游戏脚本
- 个人创意写作项目

❌ **不推荐使用：**
- 需要频繁引用历史细节的场景
- 非线性、复杂关联的内容
- 需要精确溯源的应用
- 多人协作的大型项目

---

**文档版本：** v1.0
**最后更新：** 2025-11-05
**参考项目：** AI_Gen_Novel (D:\Java\NovelAIde\AI_Gen_Novel)
