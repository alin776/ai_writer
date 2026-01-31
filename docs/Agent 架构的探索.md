大家好，我是星仔。

随着 2025 年即将画上句号，我想对”Agent 元年“根据个人这一年的实践和认知进行一次收敛。

**技术观点：Agent 架构之争已定，收敛至以 Claude Code 和 Deep Agent 为代表的「通用型 Agent」形态。**

Claude Code 虽然在 2025 年 3 月作为“智能终端编程助手”推出，但其不止于编程。

**社区里“不务正业”的玩法**：社区的开发者迅速挖掘了它的潜力，将其用于整理知识库、辅助博客创作、项目管理：

- • 案例：Claude Code 「全球“薅羊毛”第一人」刘小排（曾用 200 美元套餐消耗 5 万美元 Token）曾断言：**“只要有 SOP，就没有 Claude Code 执行不了的任务。”**

**官方的战略转向**：Anthropic 官方也注意到这种转变，2025 年 9 月，官方发布博文《Building agents with the Claude Agent SDK》[1]，正式将 “Claude Code SDK” 更名为 “Claude Agent SDK”。

- • **背后的逻辑**：Anthropic 意识到 Claude Code 核心的 Plan（规划）能力、上下文自动压缩、文件系统访问 等机制，不仅适用于编程，同样完美适配深度研究、视频制作等非编程任务。因此赶紧改名，防止大家从命名上认为它们只能做代码。

**不是计划出来的，是演化出来的**：也许 Anthropic 一开始也不知道 claude code 能做这么多事情，随着社区里更多更多的玩法，才逐渐清晰。

这也引出了一个关键问题：**它的核心架构究竟有何特点？我们又该如何对其进行修改适配，将其从“通用型”转化为特定领域的“垂类 Agent”？，将在后文详细展开**。

行业认知: 2025 年作为 Agent 元年，既没有悲观者眼中的“名不副实”，也未完全达到乐观者预期的“全面替代”，而是处于稳步落地的中间态。

作为一线从业者，我的评价是：**技术已就绪，爆发在局部**。

**验证过的成功**： Deep Research 和 Claude Code 已经完全融入日常工作流，成为了稳定可靠的生产力工具。

**看不见的繁荣**： 在招聘、市场营销、医疗等垂直领域，许多 Agent 产品早已实现百万美元营收。但由于大量业务集中在出海方向，导致国内体感不强。

**核心瓶颈的变化**： 年中时我们还在纠结技术架构，但现在架构已趋于统一。当前的真正挑战在于“业务重塑”——即依然需要懂技术的一线从业者，将传统 SOP（标准作业程序）解构和把行业知识提炼出来，以 Agent 友好的方式沉淀为新的工作流。

**基于以上背景，本文将从 Deep Agent 为切入点，分享我作为一线开发者在 2025 年的实战感悟**。

主要参考资料： Anthropic[2]、LangGraph[3]、Manus[4]、Philipp[5]。

关于参考资料的说明：在 Agent 领域，这些一线头部企业（特别是 Anthropic）对技术落地和架构的理解属于 T0 版本，其认知深度和实效性目前远超学术论文。如果你想真正研究 Agent，建议暂时放下学术论文，直接关注一线企业的落地实践和思考。

# 先来下个定义，什么是”Deep Agent“ ？

首先，它是“Deep”的

个人认为有两点需要做到

### 特征一：够“垂”（行业性）

具体示例如下：

1.招聘 Agent 示例

- • **输入**： 一位 AI 芯片架构师的姓名。
- • **任务**： 一份专业背景报告。
- • **衡量标准（如何才算“够垂”）**：报告内容（研究方向、核心项目、融资历史等）逻辑严谨、信息全面、专业性强，无任何重要信息遗漏和事实错误，达到高级招聘经理的水准。观感上，让老板无法分辨是人工还是 AI 生成。

2.市场营销 Agent 示例

- • **输入**：某品牌的产品信息和市场定位。
- • **任务**：筛选符合品牌调性的网红（KOL/KOC）并给出市场报价。
- • **衡量标准（如何才算“够垂”）**：最终筛选出的名单和报价，与公司市场部人工筛选的结果高度重合（例如 70% 以上重合），且报价在人工测算的合理区间内。

这些就是你的 agent 够“垂”的表现。假如你的 Agent 输出与通用型工具（如 Manus）一样，那就是不合格的。

行业性指的是什么呢？所谓的行业性，是指 Agent 的知识和能力必须源于该行业的**深度实践和共识**，包括但不限于：

- • **业务定义的理想态**：如高级招聘专家定义的标准流程、评分标准或成功方法论。
- • **过往案例积累**： 行业内成功的或失败的关键案例（如一次成功的招聘、一次失败的市场活动）。
- • **行业潜规则/默契**： 仅在特定圈子（如猎头行业）流传的专业共识、价格默契、资源倾向或风险偏好。

### 特征二：Long-running（稳定性）

**2025 年 2 月 24 日，Claude 3.7 Sonnet 发布**。Anthropic 为了证明 claude 3.7 Sonnet 能在在复杂任务中的规划和长期连贯性。在 Twitch 平台上开启了 “Claude Plays Pokemon” 的直播，让 claude 自己连续玩好几个小时的宠物小精灵。Claude Plays 宠物小精灵[6]

**2025 年 11 月 18 日，Gemini3 发布**：Blog 里提到 Plan anything[7]。Gemini 3 提升了其跨越长周期可靠规划的能力。例如，用户要求规划并预订下月初（1 月 6 日、7 日）从兰州到法兰克福的往返行程和酒店。规划流程涉及多步骤的操作，如：

- • 检查 Google 日历，确保出发时间不与标记为“重要”的会议冲突。
- • 如果发现冲突，自动将会议重新安排到会议周内最接近的空闲时间。
- • 在 Google Keep 中创建包含法兰克福一月平均气温信息的打包清单。 这个例子展示了 Agent 必须具备跨应用、多步骤、具有决策和修正能力的长时间任务执行能力。
- • 发送行程安排到你的 Google email。

**2025 年 12 月 1 日，豆包手机发布**。Agent 能够通过感受图形界面和仿人化的操作，例如点击屏幕完成一系列任务。例如：“帮我查一下从 [城市 A] 到 [城市 B] 最便宜的机票，然后预订下来，并给我订一个 [城市 B] 附近评价最好的酒店。”

以上案例共同证明，一个 Deep 的 Agent 必须能够实现 “Long Time Run”，这涵盖了两个关键维度：

1.**Agent 必须能够长时间持续运行而不崩溃**（例如，连续玩 24 小时宠物小精灵直至通关），确保任务不会因系统不稳定而中断。

2.**Agent 必须能连续、保质保量地执行多步骤任务，涉及到大量调用工具（Tools）和外部服务（APIs）**。例如，相比于简单的“发微信告诉妈妈今晚我晚点回家”，更复杂的任务是“找一款 500 元的大品牌秋冬大衣，并在京东、淘宝、拼多多比较，综合所有评论，找到推荐的 3 件，并发到我邮箱”。后一任务可能涉及多达 50 个 tool 或 API 的连续调用。

#### 其次，它是“Agent”

Deep Agent，它是一个 Agent。

以下相信已经是公认的对 Agent 的定义

An LLM agent runs tools in a loop to achieve a goal.

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdrUQJmvibTlIylxEzV8Za8co68TNHAiaqH3RH1XLicfdFAm4icHTXglry4K4kWrgickklibAeyEwWx1yVA/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=1)

这是一个老生常谈的故事。Workflow 胜在稳定，Agent 胜在上限高。传统做业务开发的同事，往往追求稳定，包括我自己。但最近，本人又有一些新的思考，“We are managing risk, not eliminating variance”。

甚至有人戏称

拉投资用 Agent 讲故事，做业务踏踏实实用 Workflow 。

这句玩笑背后折射出现实的考量：Workflow 胜在确定性，而 Agent 胜在上限。投资人或许能容忍 Agent 偶尔的“幻觉”甚至将其视为智能的体现，但业务交付更看重从 A 到 B 的稳定达标。

如果用一句话概括二者的本质区别，我认为是**复杂度的转移**：

Workflow 将错综复杂的业务逻辑显式地构建为“有向图”；而 Agent 则将这些逻辑抽象为自然语言。在我们将架构简化为“Prompt + Tool”的同时，并没有消除复杂度，仅仅是将复杂度从“流程编排”转移到了“Prompt 设计”之中。

但跳出形态之争，无论你选择 Workflow 还是 Agent，核心逻辑是一致的：**我们都在实践 Test-Time Scaling Law**。 即通过良好的上下文工程（Context Engineering），让模型“合理”地消耗更多 Token，以换取解决更难题目的能力或更高的任务准确率。

我们可以设想一场算法比赛：给定一个复杂的业务场景、5 个不同模型厂商的 api、 单次 20 万 Token 的消耗上限，比拼业务准确率。我相信 100 个开发者会给出 100 种方案：有人会构建不同的 Workflow，有人会打磨 Agent 的 抽象，实现的路径本身就是充满了多样性。

本文重点还是讲 Agent，但在后续的实践部分，会演示如何将一个 Workflow 变成 Agent。

# 围绕上述特点，如何构建 Deep Agent？

### 维度一：把业务知识丝滑地融入到 Agent

目前的常见做法

1.**融入 Prompt**：绞尽脑汁地编写 prompt，试图把业务逻辑“翻译”成模型能懂的口吻。这种方式往往僵化且死板，难以灵活应对复杂场景。

2.**企业知识库 (RAG)**：虽然能解决知识体量问题。但需要定义 Index、处理向量化、精心切分文档……整个过程笨重。

这些做法都不够“丝滑”。直到 Anthropic 在 2025 年 10 月提出了 Agent Skills，我看到了一种优雅的解法。

```
Blog: 《Equipping agents for the real world with Agent Skills》
https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

Youtube: 《Don’t Build Agents, Build Skills Instead – Barry Zhang & Mahesh Murag, Anthropic》
https://www.youtube.com/@aiDotEngineer
```

Skill 本质上是一个多层级的文件系统。

这个文件系统里封装了指令、脚本和相关资源，旨在让 Agent 可以**动态地发现和加载这些内容**，以便更好地执行特定任务。技能通过将您的专业知识打包成可组合的资源提供给 Claude，从而扩展了 Claude 的能力，将通用代理转化为适合您需求的**专业化代理**。

用官网 Blog 的例子来说明

例子：Claude 对理解 PDF 已经很强了，但在直接操作它们（例如填写表格）的能力上受到限制。因此，Claude 抽象出一个 pdf 的 skill。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdrUQJmvibTlIylxEzV8Za8cCnN4ibgwsRYff3VD560b5pllM4aicIptibd9vXtz5bSLiczjIMFDIWtPtQ/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=2)

最简单地说，技能是一个包含 SKILL.md 文件的目录。该文件必须以 YAML Frontmatter 开头，其中包含一些**必需的元数据**：name 和 description。在启动时，代理会将所有已安装技能的 name 和 description **预加载到其系统提示中**。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdrUQJmvibTlIylxEzV8Za8cxCT5jpiamHk50xHk75A1FRDaQMDF6icbsIfEMhc5Rsic9SXBtW6n6snTg/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=3)

这些元数据是**渐进式披露**（progressive disclosure）的**第一级**：它提供了刚好足够的信息，让 Claude 知道何时应该使用每个技能，而无需将所有内容都加载到上下文（context）中。

该文件**实际的正文是第二级细节**。如果 Claude 认为该技能与当前任务相关，它将通过读取完整的 SKILL.md 文件到上下文（context）中来加载该技能。

一个 SKILL.md 文件必须以包含文件名和描述的 YAML Frontmatter 开头，这些内容会在启动时加载到其系统提示中。

随着技能复杂性的增加，它们可能包含太多上下文而无法放入单个 SKILL.md 中，或者包含仅在特定场景下才相关的上下文。

在这些情况下，技能可以在其目录内捆绑额外的文件，并从 SKILL.md 中按名称引用它们。这些**额外的链接文件是第三级**（及更深层次）的细节，Claude 可以选择**仅在需要**时导航和发现它们。

在下面所示的 PDF 技能中，SKILL.md 引用了两个额外的文件（reference.md 和 forms.md），技能作者选择将它们与核心的 SKILL.md 捆绑在一起。

通过将填写表格的指令移动到一个单独的文件（forms.md）中，技能作者能够保持核心技能的精简，**相信 Claude 只有在填写表格时才会读取 forms.md**。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdrUQJmvibTlIylxEzV8Za8c7LUqUjTFghGrBib5mib7DhRk20G5tYb9plXJkU8lBiaiaFElly0ibHqzoAA/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=4)

**渐进式披露**是使 Agent Skills 灵活和可扩展的**核心设计原则**。就像一本组织良好的手册，从目录开始，接着是特定的章节，最后是详细的附录，**技能允许 Claude 仅在需要时加载信息**：

- • 技能元数据（name 和 description）→ 预加载到系统提示 (System Prompt) 中。
- • SKILL.md 的全部内容 → 仅在相关时加载到上下文（context）中。
- • 附加文件 (如 forms.md) → 仅在需要时被发现和加载到上下文（context）中。

以下图表展示了当用户消息触发技能时，上下文窗口是如何变化的。

技能通过您的系统提示在上下文窗口中被触发。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdrUQJmvibTlIylxEzV8Za8clNgpU052J9e6V0vRjUy5NppoJpSFIEuyx2ky3wgf0koVUoTkMn4jdA/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=5)

所示的操作序列：

1.开始时，上下文窗口包含核心系统提示和所有已安装技能的元数据，以及用户的初始消息；

2.Claude 通过调用 Bash 工具来读取 pdf/SKILL.md 的内容，从而触发 PDF 技能；

3.Claude 选择读取技能中捆绑的 forms.md 文件；

4.最后，Claude 在加载了 PDF 技能中的相关指令后，继续执行用户任务。

#### Skills 还可以包含代码

官网示例中，PDF 技能包含一个预先编写的 Python 脚本，该脚本可以读取 PDF 并提取所有表单字段。Claude 可以运行此脚本，而无需将脚本或 PDF 加载到上下文环境中。而且由于代码具有确定性，因此这个工作流程是一致且可重复的。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdriaBDriaWqZGLxrHq8kG4XHOpwoVpx9SpM0K9QcxiadK3AaNVWHjicvTz7Nic0LhP63TFQO5icJmPSm1g/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=6)

从这个角度来看，skills 多多少少还有取代 tools 或 mcp 的作用。假如你的场景因为外部编写的 mcp 字段定义得不好，其实你可以是可以把它变成 skills，写一些 case，来提升提升调用的准确率的，这样子，从外部的不可控变成自己掌控。

为什么好？

1.**渐进式披露和加载，带来更好的 Context 管理**：彻底告别把所有背景信息一次性塞进 Prompt 的暴力做法。通过分级加载，大模型变得更轻快、更专注。

2.**能让工程师进入“业务心流”状态**：这种文件结构迫使工程师必须梳理清楚业务逻辑。编写 Skill 的过程，本质上就是对业务进行高内聚、低耦合的抽象过程。这感觉是 AI 时代，更好的人机协作方式，人来做高层的业务抽象，AI 来完成具体的事情。

3.**高度可复用**：Skill 是独立的文件夹。同事想了解和复用你的业务逻辑？直接把文件夹 Copy 给他即可，觉得好用的，直接加入到自己的 skills 就好了。

4.**部分代码更稳定**：想想，调用代码更加稳定，假如我们是用 mcp_hub tools 时，假如有 50 个 tools，都需加载到 system prompt，但假如用 Agents skills，它是按需加载的。同 1，但更针对工具和代码调用。

有一大堆开源的 skill 可以参考。

```
HTTPS://GitHub.com/anthropics/skills/tree/main/skills
```

#### 不过，思想虽美，落地时仍需“祛魅”。

在实际工程中，你会发现一个残酷的现实：**Claude 模型**：能以 98% 的概率稳定触发和调用这些 Skills；**非 Claude 模型**（如豆包、DeepSeek 等）：触发成功率可能仅维持在 80% 左右甚至更低，

无论如何， Claude Skill 是 2025 年 AI 应用我认为的最佳工作。如此简单而美的工作，用最直观、清晰、简练的方式，解决了 Agent 复杂能力的封装与扩展问题。

#### 维度二：怎么 Long-Running

langgraph 提出来 4 种方法，让你的 agent 在长时间运行不崩溃，甚至 langgraph 开发了一个包，就叫 Deep Agent[8]。里面提到了 4 种方法。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdrUQJmvibTlIylxEzV8Za8cAGTQ5wQv2BIFhN5Y2B85EYelPgMuvfC10OTxmpkngSQvYicaqBP1oTQ/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=7)

#### Planning

规划是深度代理能够在其目标上执行**更长时间跨度任务**的重要组成部分。

• **任务分解**： 规划工具（例如内置的 write_todos 工具）使得代理可以将复杂的任务分解为离散的步骤，跟踪进度，并根据新信息调整计划。

• **保持焦点**： 规划工具通过在模型的上下文（context）中创建待办事项列表等消息，帮助代理在执行过程中保持正确的轨道。

#### Sub-Agents

子代理的目的是允许代理将任务拆分，**并实现上下文隔离**。

1. 1. **上下文隔离**: 子任务的执行过程不会污染主智能体的上下文。
2. 2. **并行执行**: 多个子任务可以同时进行，大幅提升效率。
3. 3. **专业化分工**: 可以为不同的子智能体配置专属的工具和指令。
4. 4. **Token 效率**: 子智能体完成任务后，只将最终的、高度综合的结果返回给主智能体，极大地压缩了上下文。

但 Sub-Agents 的架构已经收敛到一个超强的 main-agent，必要时再按需调用 sub agent 的架构。例如下图的 supervisor。这种架构还有个好处，KV cache 能很好地利用上，省钱+跑得快。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdrUQJmvibTlIylxEzV8Za8ceQQcBtjC3qu1rFpVETIczICRva8voMwe0NyuGNsQJFvu9fAlbibgUQw/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=8)

#### File System

• **上下文卸载**： 文件系统（如 ls、read_file、write_file、edit_file 等工具）允许代理将大量的上下文卸载到文件中。这有助于防止上下文窗口溢出，并避免由于上下文过多导致的大语言模型性能下降。
• **共享工作区**： 文件系统可用作所有代理（包括子代理）协作的共享工作区。
• **长期记忆**： 代理可以通过文件系统存储（然后稍后读取）笔记或信息，充当“记忆”功能。此外，文件系统也可以用于存储代理可执行的脚本或“技能”，并通过命令行工具（如 Bash 工具）调用。

#### SyStem Prompt

系统提示在深度代理的实现中至关重要。最优秀的 code cli 或 deep research 往往拥有**非常复杂和详细的系统提示**。例如 claude deep research 的 prompt。

• **详细指导**： 系统提示通常很长，包含关于如何使用各种工具的详细说明。

• **示例学习**： 它们可能包含少量示例（few-shot prompts），指导代理在特定情况下如何行动。

• **复杂性承载**： 尽管模型能力强大，但依然需要提供数百甚至数千行的详细指令，这是因为提示工程仍然非常重要。**通过细致的提示，可以将应用的复杂性转移到提示本身**。

这些详细指令通常会定义：

1.何时应该暂停执行并进行规划的识别标准。
2.何时应该生成子**智能体**，以及何时应该自己完成工作的决策协议。
3.所有可用**工具**的详细定义、使用方法和最佳实践示例。
4.文件命名和目录结构的标准规范，以保证工作空间的整洁。

这四大支柱并非孤立存在，它们相辅相成，共同构成了 Deep Agent 的核心运作机制。而将这一切串联起来的底层技术，正是“上下文工程”。

# Agent 技术形态的收敛

在 10 月份前，我觉得 Agent 的技术发展还没收敛的。

- • 证据一：自 Manus 于三月份推出到十月份，他们已经重构了 Manus 的架构五次[9]。
- • 证据二：LangChain 在 2025 年 10 月 才正式上线 1.0 正式版本（v1.0），并同时推出了 DeepAgent[10]。

但 2025 年 10 月份后，我认为已经收敛，收敛到以 Claude Agent SDK[11] 和 Deep Agent[12] 为代表的架构。

这种架构有什么特点呢？

上面已经介绍了一部分，它是 **Main Agent - Sub Agent（主从架构），还具备自主规划（Planning）能力和独立的文件系统概念**。

还有些没提到，包括

**上下文自动压缩 (Context Compression)**：当 Token 使用量达到上限（如 200k）的 80% 时，自动调用总结模型对前文进行摘要压缩，释放空间。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdrUQJmvibTlIylxEzV8Za8cWUKB6iaYBHydB2H11of4B6rQqwu16189KkAbUVx9GtuXMmBIzNRhnMg/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=9)

#### 分层的工具调用：解决上下文拥挤的问题

向 LLM 一次性灌输超过 100 个工具会导致 **上下文混淆** (Context Confusion)，极易引发幻觉或参数错误。Manus 等先进架构通过**三层分层**设计缓解了这一问题：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdriaBDriaWqZGLxrHq8kG4XHJokmkQFDfzoJWkCNOq6aPx81yZMnF11gAaiaxGTeqFtwrTmuEArmPtg/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=10)

#### 第 1 层：原子层 (Atomic Layer)

- • **特点**： 仅保留约 20 个核心、高频、正交的工具。
- • **内容**：read file, edit file,browser_navigate, bash, ls、task 等。
- • **目的**： 确保模型最基础的交互能力稳定可靠。

#### 第 2 层：沙箱工具层 (Sandbox Utilities)

- • **核心思想**： 去工具化。不再为每个程序（如 ffmpeg）封装独立的 Function Call 定义，而是直接让 LLM 使用 bash 工具在命令行中调用预装程序。
- • **优势**： 将工具的具体定义排除在 Context 之外，极大节省 Token 并降低混淆。
- • **案例对比**：视频处理 (FFmpeg)

```
❌ 传统模式（API 堆砌）： 开发者必须预定义 convert_video 等大量专用工具及其繁杂参数（分辨率、码率等）。
结果： LLM 面对的是一个冗长且受限的工具列表 [file_read, convert_video, resize_image...]，消耗大量 Token 且缺乏灵活性。

✅ Manus 模式（通用沙箱）： 开发者仅提供 bash 工具，并写入提示词：“如果你发现当前没有合适的工具，请使用 /help 命令探测系统环境。” 执行流程：
判断：用户请求处理视频，LLM 扫描工具列表 [file_read, bash]，发现没有视频工具。
探测：LLM 遵循预设提示，通过 bash 执行 /help，系统返回可用命令列表 (如 ffmpeg)。
执行：LLM 随即构建并执行 ffmpeg -i video.mov... 完成任务。
```

底层还是**渐进式披露**的思想。

#### 第 3 层：代码/包层 (Code/Packages)

- • **核心思想**：逻辑封装。类似 Huggingface Smolagents 的理念。
  场景： 针对复杂的串行逻辑。
- • **解决方案**： 不再进行 3 次 LLM 往返交互 (Roundtrips)，而是直接提供 Python 库，让 Agent 编写一段动态脚本一次性执行所有步骤。如下图，假如用 tool，可能一个简单的问题“帮我查看每个国家换算成美元后的手机价格，找过最便宜的国家”需要上百次的 tool 调用，但用代码其实只是十几行代码的循环。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdrUQJmvibTlIylxEzV8Za8cwfibOXmgHu9S8LbKHd2DjicZQgB9rnSNxsHSPPhODE3MQ0UOWsfeqKUQ/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=11)

**既然通用型 Agent 的架构已经如此强大，我们如何将其适配到特定的垂直业务场景中？**

1.**业务知识技能化 (Skills via File System)**： 将业务文档、SOP（标准作业程序）抽象为 Skills，存储在 Agent 的文件系统中。模型根据任务需求，按需动态加载（Load on Demand），而非一次性塞入。

2.**业务接口 MCP 化 (MCP)**： 将企业的业务 API 封装为 MCP (Model Context Protocol) 服务。Agent 可以像连接外设一样，按需连接和调用这些 Server。

3.**提示词精细化 (Fine-grained System Prompts)**： 分别针对 Main Agent（负责调度）和 Sub Agent（负责执行）编写极度详细的 System Prompt，约束其行为边界。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdrUQJmvibTlIylxEzV8Za8c9n3Poj6pUNBic5d3AHZE24vzbsTPGpgAny5eC0rYbZMEdNBmQtH2lww/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=12)

# 业务中的思考

### 如何将现有 Workflow 升级为 Agent

其实很简单，仿照 claude 的 deep research prompt[13] 就好了。

claude deep research 就是一个很典型的 main-agent/sub-agent 架构，只有三个 prompt，一个 main agent（lead agent），一个 subagent，一个是生成文章后处理引用信息的 agent 最重要的就是 main-agent/sub-agent 。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/HrMQ8SF1ApdriaBDriaWqZGLxrHq8kG4XH2Zx0ukSN7bhQACNEwTv1f5dpARHwwT84g3zyoniaHeoAwS5Za6Bb8iaQ/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=13)

模仿 Claude Deep Research 的 Prompt 架构。我们可以将大量复杂的业务流程和决策逻辑，通过极度详尽的 System Prompt 沉淀到 Main Agent 的认知体系中。

**很多人之所以不相信这种方式有效，往往是因为他们没有使用最 SOTA 的模型（claude4.5、 gemeni3 、 gpt5.2）**。

假如确实没有拿到最 SOTA 的模型，那就把任务难度降一层级吧。在那些没那么复杂的业务上做尝试。

相较于传统微调（SFT）动辄两周的长周期 —— 在此期间需要投入大量时间进行数据清洗、人工标注和反复训练。Agent 模式的开发路径直接跳过了最耗时的数据准备环节，将迭代周期从 “周级” 压缩至 “天级”。其核心逻辑，本质是通过消耗 token 的方式来换取效果的快速迭代与提升。

个人感觉，26 年要多尝试这种开发姿势了。

# 25 年，我的 Agent 探索新路

25 年过去了，随着更强的模型，现在新发布的模型，例如 deepseekv3.2、kimi 2 thinking、gemini3 它们都一定会宣称自己是一个 agent native model，用了大量 agent 的数据来做训练。

回顾这一年，思考路径随着技术演进而不断深化：

- • 2025 年 2 月， 受 OpenAI 发布 DeepResearch 的启发，我思考了 Agent 的形态，写下《25 年什么样的 Agent 会脱颖而出：简单胜于复杂》[14]。
- • 2025 年 4 月，深入业务场景实践，围绕“端到端复现 Deep Research”撰写了三部曲：
  《端到端的训练，怎么复现 Deep ReSearch（上） ：先从 Deep Search 做起》[15]
  《端到端的训练，怎么复现 Deep ReSearch（中） ：围绕着”Deep”，解构 Jina 项目的实现》[16]
  《端到端的训练，怎么复现 Deep ReSearch（下） ：前沿的产品形态》[17]
- • 2025 年 8 月，上下文工程是本质，写下《为什么我们需要 Context Engineering？》[18]
- • 期间，紧跟 Anthropic 等厂商的最佳实践实践，看到有感触的就写《Anthropic：为 Agent 编写高效的工具》[19]《Anthropic：如何建设有效的上下文》[20]《我看懂了通义 Deep Research 的进化史》[21]《Skills 让你的 Agent 从”可用”变”好用”》[22]《Sub Agent As Tool 的 Agent 设计思想》[23]