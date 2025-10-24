# 技术栈规划

> **文档版本**: v2.12
> **最后更新**: 2025-10-24

## 📑 导航
- [⬅️ 上一章: 项目概述](./01-overview.md)
- [➡️ 下一章: 当前项目状态](./03-current-status.md)
- [🏠 返回文档导航](./README.md)

---

## ⚙️ 技术栈规划
### 技术选型说明
**最终确定方案**：React 19 + Vite + FastAPI + PostgreSQL
**前端状态**：✅ 核心功能已完成（编辑器、世界观、导入导出、搜索）
**后端状态**：✅ 核心API已完成（用户、作品、章节、世界观、AI服务）
**优势**：快速迭代、灵活可控、生态成熟

### 一、前端技术栈
#### 核心框架 ✅ 已确定
+ **框架**: React 19.1.1
+ **语言**: TypeScript 5.x
+ **包管理**: npm / pnpm
+ **构建工具**: Vite 5.x

#### 编辑器方案 ✅ **已完成**
+ **最终方案**: Tiptap 3.7.0 (自定义实现)
+ **已实现功能**:
    - ✅ 富文本编辑（粗体、斜体、标题、列表等）
    - ✅ Slash命令系统（11个命令 + 搜索）
    - ✅ AI功能菜单（续写/扩写/总结/润色/翻译）
    - ✅ 气泡菜单（9个格式化工具）
    - ✅ 代码块语法高亮（37种语言）
    - ✅ Markdown支持
    - ✅ 字数统计实时显示
    - ✅ 自动保存功能
    - ✅ 拖拽手柄
+ **核心组件**:
    - `NovelEditor.tsx` - 主编辑器 (312行)
    - `SlashCommands.tsx` - Slash命令
    - `AIMenu.tsx` - AI功能菜单 (20KB)
    - `BubbleMenu.tsx` - 气泡菜单
+ **实现状态**: 85% (图片上传非必需功能未实现)

#### AI集成 ⭐
+ **AI提供商**: 第三方OpenAI兼容接口
    - **Base URL**: `https://204992.xyz`
    - **API Key**: 环境变量配置 `{:LOCAL_API_KEY}`
+ **优势**:
    - ✅ 无需申请OpenAI官方账号
    - ✅ 成本可控，统一管理
    - ✅ 完全兼容OpenAI SDK
    - ✅ 支持GPT-4、GPT-3.5等主流模型
+ **前端SDK**: Vercel AI SDK (ai)
+ **流式处理**: EventSource / SSE
+ 后续使用Gemini的模型，好处上下文够长、语言有温度，对中文理解比模型要好

#### UI框架与组件
+ **实际使用**: 自定义组件 + 部分Radix UI
+ **样式方案**: Tailwind CSS 4.1.8 ✅
+ **图标**: Lucide React ✅
+ **特殊组件**:
  - ✅ ConfirmDialog - 专业确认对话框
  - ✅ Toast - 通知系统
  - ✅ Modal - 弹窗组件
+ **建议**: 后续可考虑迁移到Shadcn/ui（非必需）

#### 状态管理
+ **全局状态**: Zustand ✅ (已实现authStore、workStore)
+ **服务端状态**: 直接使用DataService + 组件状态（简单有效）
+ **表单状态**: React原生useState（已足够）
+ **建议**: 后续可引入React Query优化缓存（非必需）

#### 数据验证
+ **前端验证**: TypeScript类型系统 + 手动验证
+ **后端验证**: Pydantic Schema ✅ (完善)
+ **建议**: 前端可引入Zod增强验证（非必需）

#### 图表与可视化
+ **图表库**: Recharts ✅ (管理后台统计图表)
+ **关系图**: ReactFlow 12 ✅ (世界观关系图可视化已完成)
  - ✅ WorldviewGraph组件 (380行)
  - ✅ 三种自定义节点（角色/地点/设定）
  - ✅ 自动布局和交互

---

### 二、后端技术栈（Python）
#### 核心框架
+ **Web框架**: FastAPI 0.109+
+ **异步服务器**: Uvicorn
+ **ASGI服务器**: Gunicorn（生产环境）
+ **Python版本**: 3.11+

#### 数据库
+ **主数据库**: PostgreSQL 15+
+ **ORM**: SQLAlchemy 2.0 (Async)
+ **数据库驱动**: asyncpg
+ **数据库迁移**: Alembic
+ **缓存**: Redis 7.x
+ **Redis客户端**: redis-py + aioredis

#### AI核心 ⭐
+ **主要AI提供商**: 第三方OpenAI兼容API ([https://204992.xyz](https://204992.xyz))
+ **AI框架**: LangChain 0.1+ （可选，见下方选型讨论）
+ **AI集成**:
    - `openai` - OpenAI SDK（配置自定义base_url）
    - `langchain-openai` - LangChain OpenAI集成（可选）
+ **Token计数**: tiktoken
+ **向量数据库**: ChromaDB/PGSQL
+ **Embeddings**: sentence-transformers

#### AI框架选型讨论 ⭐⭐ **重要决策**

> **背景**: 项目已完成Milestone 1（基础AI调用），现规划Milestone 2的4大AI增强功能。团队讨论是否引入LangChain/LangGraph框架。

##### 当前状态
+ ✅ **已有实现**: `HTTPAIService` - 简单的OpenAI API调用封装
+ ✅ **提示词管理**: JSON配置文件 (`backend/app/services/ai/prompts/default.json`)
+ ⚠️ **复杂度增长**: Milestone 2需要多步骤AI Pipeline（反馈系统、去痕迹、评审）

##### 适合使用LangChain的场景

**🟢 强烈推荐使用的功能**:

1. **AI交互式反馈系统**（P0）
   - 需求：生成内容 → 自我评价 → 改进建议 → 重新生成
   - LangChain方案：`SequentialChain` 串联多步骤
   - 优势：清晰的Pipeline管理，易于调试

2. **去AI痕迹功能**（P0）
   - 需求：检测痕迹 → 规则处理 → AI润色 → 验证
   - LangChain方案：`TransformChain` + `LLMChain` 组合
   - 优势：规则引擎与AI调用统一管理

3. **小说评审增强**（P1）
   - 需求：分析 → 评分 → 诊断 → 生成任务清单
   - LangChain方案：`SequentialChain` + `TransformChain`
   - 优势：多维度分析的模块化组合

4. **提示词管理系统**
   - 需求：模板管理、变量替换、Few-shot示例
   - LangChain方案：`PromptTemplate` + `FewShotPromptTemplate`
   - 优势：内置强大的模板引擎，支持变量和条件逻辑

**🟡 可选使用的功能**:

5. **AI写作竞技场**（P1 - 明星功能）⭐⭐
   - 需求：当用户不满意AI生成时，同时调用4-6个模型对比选择最佳
   - 当前方案：`asyncio.gather` 并发调用，足够简单高效
   - LangChain优势：不明显（反而增加复杂度）
   - 备注：独立页面设计，作为产品差异化核心卖点

**🔴 不建议使用LangGraph的场景**:

- 当前所有功能都是**线性Pipeline**，不需要复杂的状态机
- LangGraph适合：Agent应用、条件分支、循环迭代
- 建议：6个月后，产品成熟后再考虑LangGraph

##### 推荐方案：逐步引入LangChain ⭐⭐⭐⭐⭐

**实施策略**:

```python
# Week 1: 为"去AI痕迹"试用LangChain
from langchain.chains import SequentialChain, TransformChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class HumanizeServiceV2:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url="https://204992.xyz",
            api_key=settings.OPENAI_API_KEY
        )

        # Prompt模板
        self.detect_prompt = PromptTemplate(
            input_variables=["text"],
            template="检测以下文本的AI痕迹（0-100分）：\n{text}"
        )

        self.humanize_prompt = PromptTemplate(
            input_variables=["text", "intensity"],
            template="去除AI痕迹（强度{intensity}/10）：\n{text}"
        )

        # 构建Pipeline
        detect_chain = LLMChain(llm=self.llm, prompt=self.detect_prompt)
        humanize_chain = LLMChain(llm=self.llm, prompt=self.humanize_prompt)

        self.pipeline = SequentialChain(
            chains=[detect_chain, humanize_chain],
            input_variables=["text", "intensity"],
            output_variables=["trace_score", "humanized_text"]
        )

    async def humanize(self, text: str, intensity: int):
        result = await self.pipeline.arun(text=text, intensity=intensity)
        return result
```

**优点**:
- ✅ 代码更清晰（Chain组合 vs 手动串联）
- ✅ Prompt管理更强（变量、条件、Few-shot）
- ✅ 可观测性更好（LangSmith调试工具）
- ✅ 与现有代码共存（无需重构）

**实施路径**:

1. **Week 1（本周）**: 为"去AI痕迹"功能试用LangChain
2. **Week 2-3**: 评估效果，决定是否扩大使用
3. **如果效果好**: 迁移"AI反馈"、"评审"到LangChain
4. **如果效果一般**: 保持现状，仅在复杂场景使用

##### 对比分析表

| 方案 | 适用场景 | 学习成本 | 开发效率 | 代码复杂度 | 推荐度 |
|------|---------|---------|---------|-----------|--------|
| **逐步引入LangChain** | Milestone 2核心功能 | 中等 | ⬆️ 提升30% | 适中 | ⭐⭐⭐⭐⭐ |
| **保持现状（简单调用）** | 简单AI调用 | 低 | → 不变 | 低 | ⭐⭐⭐ |
| **直接用LangGraph** | 复杂Agent | 高 | ⬇️ 初期降低 | 高 | ⭐ 不推荐 |

##### 风险评估

**引入LangChain的风险**:
- 🟡 增加依赖包大小（~50MB）
- 🟡 团队学习成本（2-3天熟悉）
- 🟢 生态成熟，社区活跃，风险可控

**不引入的风险**:
- 🔴 手动管理复杂Pipeline易出错
- 🔴 Prompt模板管理混乱（JSON文件不够用）
- 🔴 后期重构成本更高

##### 最终建议 ⭐

**决策**: ✅ **推荐逐步引入LangChain**

**理由**:
1. Milestone 2的4个核心功能都能从中受益
2. 可与现有代码共存，风险低
3. 提升开发效率和代码可维护性
4. 为未来的复杂AI功能打好基础

**下一步行动**:
- [ ] 安装LangChain依赖: `pip install langchain langchain-openai`
- [ ] 为"去AI痕迹"功能创建LangChain版本
- [ ] 对比效果，评估是否继续使用
- [ ] 1周后团队评审决策

##### 参考资源
+ **LangChain官方文档**: [https://python.langchain.com](https://python.langchain.com)
+ **LangChain中文教程**: [https://www.langchain.com.cn](https://www.langchain.com.cn)
+ **LangSmith调试工具**: [https://smith.langchain.com](https://smith.langchain.com)
+ **LangGraph文档**: [https://langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph)

---

#### 认证与安全
+ **JWT**: python-jose[cryptography]
+ **密码加密**: passlib[bcrypt]
+ **CORS**: fastapi.middleware.cors

#### 异步任务
+ **任务队列**: Celery 5.3+
+ **消息代理**: Redis (Celery Broker)
+ **任务监控**: Flower

#### 数据验证
+ **Schema**: Pydantic 2.5+
+ **Email验证**: email-validator

#### 文件存储
+ **对象存储**: 阿里云OSS
+ **本地存储**: aiofiles

#### 日志与监控
+ **日志**: loguru
+ **性能监控**: prometheus-client
+ **错误追踪**: sentry-sdk

---

### 三、数据库设计
#### 核心表结构
**用户系统**:

+ `users` - 用户表
+ `user_profiles` - 用户资料
+ `user_subscriptions` - 订阅信息
+ `user_credits` - 积分账户
+ `roles` - 角色表
+ `permissions` - 权限表

**小说系统**:

+ `works` / `novels` - 小说作品
+ `volumes` - 卷
+ `chapters` - 章节
+ `scenes` - 场景
+ `novel_tags` - 标签
+ `novel_statistics` - 统计数据

**世界观系统**:

+ `settings` - 设定条目
+ `setting_relations` - 设定关系
+ `setting_snapshots` - 历史快照
+ `characters` - 角色设定
+ `locations` - 地点设定
+ `factions` - 势力设定

**AI系统**:

+ `ai_requests` - AI请求日志
+ `ai_models` - AI模型配置
+ `user_api_keys` - 用户API密钥
+ `prompts` - 提示词
+ `prompt_presets` - 提示词预设
+ `ai_templates` - AI模板

**内容管理**:

+ `snippets` - 片段/灵感
+ `outlines` - 大纲
+ `notes` - 笔记
+ `bookmarks` - 书签

---

### 四、开发工具链
#### 版本控制
+ **VCS**: Git
+ **代码托管**: GitHub
+ **分支策略**: Git Flow

#### 容器化
+ **容器引擎**: Docker 24+
+ **编排工具**: Docker Compose
+ **镜像仓库**: Docker Hub / 私有Registry

#### CI/CD
+ **CI平台**: GitHub Actions
+ **自动化测试**: pytest + Vitest/Jest
+ **部署方式**: Docker + Nginx

#### 代码质量
**前端**:

+ ESLint + Prettier
+ TypeScript strict mode
+ Husky pre-commit hooks

**后端**:

+ black (代码格式化)
+ isort (导入排序)
+ flake8 (代码检查)
+ mypy (类型检查)
+ pre-commit

---

### 五、基础设施
#### 云服务提供商
**选项1 - 阿里云**:

+ **计算**: ECS / SAE
+ **数据库**: RDS PostgreSQL
+ **缓存**: Redis
+ **存储**: OSS
+ **CDN**: CDN
+ **负载均衡**: SLB

#### 监控与日志
+ **应用监控**: Prometheus + Grafana
+ **错误追踪**: Sentry
+ **日志聚合**: ELK Stack（可选）

---

### 六、第三方服务
#### AI服务 ⭐ 主力方案
**推荐：第三方OpenAI兼容API**

+ **服务地址**: `https://204992.xyz`
+ **API密钥**: `{:LOCAL_API_KEY}`（环境变量配置）
+ **兼容性**: 完全兼容OpenAI API规范
+ **优势**:
    - ✅ 无需注册OpenAI官方账号
    - ✅ 无需信用卡和海外手机号
    - ✅ 成本统一管理，预算可控
    - ✅ 国内访问稳定，无需代理
    - ✅ 完全兼容现有OpenAI SDK

#### 对象存储
+ 阿里云OSS

#### CDN
+ Cloudflare（推荐，免费）
+ 阿里云CDN

---

## 🔗 相关链接

- **上一章**: [项目概述](./01-overview.md)
- **下一章**: [当前项目状态](./03-current-status.md)
- **返回**: [文档导航](./README.md)
- **完整文档**: [NovelAIde 项目文档 v2.12.md](../NovelAIde%20项目文档%20v2.12.md)

---

**最后更新**: 2025-10-24
**文档版本**: v2.12
