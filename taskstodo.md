● 根据 2025-12-09 代码巡检结果，更新问题状态（括号为验证位置）。

---
已解决的问题 ✅

P0 - 严重问题
| 序号 | 问题 | 状态 |
|---|---|---|
| 1 | 默认thread_id污染 | 已修复（三层隔离 + 长度保护，见 backend/app/services/agent/langgraph_agent.py:3358-3389,3529-3554,4266-4296） |
| 2 | 作品隔离不完整 | 已修复（向量检索/写入携带 work_id，见 backend/app/services/context/manager.py:73-146,1076-1145；backend/app/services/context/vector_memory_store.py:120-218） |
| 3 | 长期记忆偏好无隔离 | 已修复（会话摘要按 work_id 存取并二次过滤，见 backend/app/services/agent/memory/long_term_memory.py:389-491） |
| 4 | 反思解析歧义 | 已修复（改为 JSON 结构解析） |
| 5 | 重规划JSON解析脆弱 | 已修复（括号匹配 + 数据验证） |

P1 - 重要问题
| 序号 | 问题 | 状态 |
|---|---|---|
| 6 | 任务ID重复风险 | 已修复（去重逻辑） |
| 7 | Token截断策略粗糙 | 已修复（智能截断+摘要，集中配置，见 backend/app/services/context/manager.py:121-141,287-319；context_config.py） |
| 8 | 消息清理IndexError | 已修复（成对保留AI/Tool，见 backend/app/services/agent/langgraph_agent.py:2975-3045） |
| 9 | 消息去重阈值固定 | 已修复（自适应阈值集中配置，见 backend/app/services/context/manager.py:1337-1387；context_config.py） |
| 10 | 摘要生成阻塞 | 已修复（8s 超时 + 监控埋点，见 backend/app/services/context/manager.py:287-319；context_config.py） |
| 11 | 长期记忆检索阻塞 | 已修复（6s 超时 + 监控埋点，见 backend/app/services/context/manager.py:1128-1143；context_config.py） |
| 12 | 向量库无内容去重 | 已修复（hash 去重，见 backend/app/services/context/vector_memory_store.py:108-150） |
| 13 | 短期记忆数量不一致 | 已修复（压缩与max_turns对齐，见 backend/app/services/context/manager.py:287-319） |
| 14 | thread_id 截断碰撞风险 | 已修复（截断+哈希后缀集中配置，见 backend/app/services/agent/langgraph_agent.py:3358-3385,3529-3556,4287-4304；context_config.py） |
| 15 | checkpoint 依赖 planner 标记才反思，缺兜底/验证 | 已修复（间隔兜底 + 单元测试覆盖，见 reflection.py:222-233；test_should_reflect.py 17 个测试用例） |
| 16 | 阈值/监控集中仍需扩展到 agent/memory 侧 | 已修复（新增 memory_config.py 集中配置，见下方详情） |

---
未解决的问题 ⚠️

（暂无）

---
架构 / 代码质量
| 问题 | 描述 | 状态 |
|---|---|---|
| Prompt 分散存储 | 分布于多个目录，难以维护 | ✅ 已解决（新增 prompt_config.py 集中配置，见下方详情） |
| 缺乏 Prompt 版本管理 | 目前无版本元数据 | ✅ 已解决（PromptModuleInfo 包含版本字段） |
| langgraph_agent.py 过大 | 6156 行，需拆分 | 🔄 进行中 |
| 记忆系统复杂度高 | 跨模块，缺统一接口 | 待处理 |

---
## 拆分 langgraph_agent.py 计划（6156行 → ~800行）

### 当前结构分析

| 代码段 | 行号范围 | 行数 | 职责 |
|-------|---------|------|------|
| 导入和全局函数 | 1-120 | 120 | 导入、validate_uuid、全局AI服务 |
| _generate_text_helper | 210-268 | 60 | 文本生成辅助函数 |
| **工具函数** | 271-975 | **700** | 6个@tool装饰的工具 |
| 压缩/上下文辅助 | 976-1160 | 185 | _compress_task_result 等 |
| WritingAgentGraph.__init__ | 1163-1850 | 690 | 初始化 + 图构建 |
| Handler方法 | 1855-3310 | 1455 | _handle_writing/planning/analysis等 |
| chat/chat_stream | 3312-3860 | 550 | 主入口方法 |
| 流事件处理 | 3863-4230 | 370 | _handle_stream_event 等 |
| chat_with_planning | 4230-5210 | 980 | 规划执行入口 |
| 任务执行 | 5212-6156 | 945 | _execute_task/_execute_tasks_in_parallel |

### 拆分方案

```
backend/app/services/agent/
├── langgraph_agent.py          # 保留：主类 + 入口（~800行）
├── tools/
│   ├── __init__.py             # 新增
│   ├── writing_tools.py        # 新增：续写/润色/分析工具（~200行）
│   └── chapter_tools.py        # 新增：章节读取/检索工具（~500行）
├── handlers/
│   ├── __init__.py             # 新增
│   ├── base_handler.py         # 新增：Handler基类（~100行）
│   ├── writing_handler.py      # 新增：_handle_writing（~200行）
│   ├── planning_handler.py     # 新增：_handle_planning（~200行）
│   ├── analysis_handler.py     # 新增：_handle_analysis（~200行）
│   └── general_handler.py      # 新增：_handle_general + _handle_stuck（~300行）
├── execution/
│   ├── __init__.py             # 新增
│   ├── task_executor.py        # 新增：_execute_task（~600行）
│   └── parallel_executor.py    # 新增：_execute_tasks_in_parallel（~400行）
└── utils/
    ├── context_builder.py      # 新增：_build_knowledge_system_messages等（~200行）
    └── result_compressor.py    # 新增：_compress_task_result等（~150行）
```

### 拆分步骤（按依赖顺序）

- [ ] **Step 1**: 创建 `tools/writing_tools.py` - 拆出 continue_writing_tool, polish_text_tool, analyze_text_tool
- [ ] **Step 2**: 创建 `tools/chapter_tools.py` - 拆出 read_chapter_tool, get_chapter_by_order_tool, search_analysis_fragments_tool, get_context_tool
- [ ] **Step 3**: 创建 `utils/context_builder.py` - 拆出 _build_knowledge_system_messages, _build_summarization_context
- [ ] **Step 4**: 创建 `utils/result_compressor.py` - 拆出 _compress_task_result, _optimize_prompt_for_retry
- [ ] **Step 5**: 创建 `handlers/base_handler.py` - 抽取 Handler 公共逻辑
- [ ] **Step 6**: 创建 `handlers/writing_handler.py` - 拆出 _handle_writing
- [ ] **Step 7**: 创建 `handlers/planning_handler.py` - 拆出 _handle_planning
- [ ] **Step 8**: 创建 `handlers/analysis_handler.py` - 拆出 _handle_analysis
- [ ] **Step 9**: 创建 `handlers/general_handler.py` - 拆出 _handle_general, _handle_stuck
- [ ] **Step 10**: 创建 `execution/task_executor.py` - 拆出 _execute_task
- [ ] **Step 11**: 创建 `execution/parallel_executor.py` - 拆出 _execute_tasks_in_parallel, chat_with_planning
- [ ] **Step 12**: 清理 langgraph_agent.py - 删除已拆出代码，添加导入

### 拆分原则

1. **保持接口不变**：外部调用方式不变，只是内部重构
2. **最小依赖**：每个模块只依赖必要的内容
3. **逐步验证**：每拆一个模块就运行测试
4. **保留注释**：所有修复标记（✅ P0修复等）保留原位置

---
## Review: P2-16 阈值/监控集中扩展到 agent/memory 侧

### 修改内容

**新增文件：**
- `backend/app/services/agent/memory/memory_config.py` - Memory 模块集中配置

**修改文件：**
| 文件 | 修改内容 |
|---|---|
| `advanced_forget_strategy.py` | ForgetConfig dataclass 默认值改为引用 MemoryConfig |
| `enhanced_memory_manager.py` | TTL 常量、锁超时、long_term_max_size_kb 改为引用 MemoryConfig |
| `version_control.py` | VERSION_TTL、MAX_VERSIONS、COMPRESS_THRESHOLD 改为引用 MemoryConfig |

### 集中配置项清单

| 配置项 | 值 | 说明 |
|---|---|---|
| SHORT_TERM_TTL | 86400 | 短期记忆 24h |
| MEDIUM_TERM_TTL | 259200 | 中期记忆 3天 |
| SNAPSHOT_TTL | 604800 | 快照 7天 |
| VERSION_TTL | 2592000 | 版本保留 30天 |
| MAX_VERSIONS | 50 | 每用户最大版本数 |
| COMPRESS_THRESHOLD | 10000 | 压缩阈值（字符） |
| LONG_TERM_MAX_SIZE_KB | 50 | 长期记忆压缩阈值 |
| LOCK_TIMEOUT | 30 | 分布式锁超时 |
| LOCK_BLOCKING_TIMEOUT | 5 | 锁等待超时 |
| 遗忘策略相关 | 见 memory_config.py | 15+ 个参数 |

### 配置文件架构

```
配置集中管理
├── context_config.py    # Context 模块配置（已有）
│   ├── Token 硬限制
│   ├── 摘要/检索超时
│   ├── 去重阈值
│   └── thread_id 长度
│
├── memory_config.py     # Memory 模块配置（新增）
│   ├── TTL 配置
│   ├── 容量限制
│   ├── 锁超时配置
│   └── 遗忘策略参数
│
└── prompt_config.py     # Prompt 模块配置（新增）
    ├── 模块注册表
    ├── 缓存配置
    ├── 长度限制
    └── 版本控制配置
```

---
## Review: Prompt 统一存储

### 修改内容

**新增文件：**
- `backend/app/prompts/prompt_config.py` - Prompt 模块集中配置

**修改文件：**
| 文件 | 修改内容 |
|---|---|
| `app/prompts/__init__.py` | 导出 PromptConfig, PromptCategory, PromptFileType, PromptRegistry 等 |

### 索引统计

| 类型 | 数量 |
|---|---|
| Python 模块 | 16 |
| YAML 模板 | 8 |
| JSON 配置 | 2 |
| **总计** | **26** |

### 集中配置项清单

| 配置项 | 说明 |
|---|---|
| MODULES | Python Prompt 模块注册表 |
| YAML_TEMPLATES | YAML 模板文件注册表 |
| JSON_CONFIGS | JSON 配置文件注册表 |
| CACHE_ENABLED | 缓存开关 |
| CACHE_TTL | 缓存 TTL (3600s) |
| MAX_SYSTEM_PROMPT_LENGTH | 系统 Prompt 最大长度 (8000) |
| MAX_USER_PROMPT_LENGTH | 用户 Prompt 最大长度 (4000) |
| VERSION_TRACKING_ENABLED | 版本追踪开关 |

### Prompt 模块索引

**Python 模块 (16个)**
| 类别 | 模块 | 路径 |
|---|---|---|
| AI_SERVICE | ai_prompts | app.services.ai.prompts |
| EVALUATION | evaluation_prompts | app.services.ai.evaluation_prompts |
| HUMANIZE | humanize_prompts | app.services.ai.humanize_prompts |
| REVIEW | review_prompts | app.prompts.review_prompts |
| CONTENT_CREATION | content_creation_prompts | app.services.agent.prompts.content_creation_prompts |
| PLANNING | novel_planning_prompts | app.services.agent.prompts.novel_planning_prompts |
| AGENT | prompt_manager/optimizer/library/cache | app.prompts.*/app.services.agent.* |
| MULTI_AGENT | writer/outline/editor/character_guard/logic_auditor | app.services.agent.multi_agent.prompts.* |
| CONFIG | agent_config | app.core.agent_config |

**YAML 模板 (8个)**
| 模块 | 路径 |
|---|---|
| intent_classifier | app/prompts/templates/intent_classifier.yaml |
| writing_agent | app/prompts/templates/writing_agent.yaml |
| planning_agent | app/prompts/templates/planning_agent.yaml |
| tool_agent | app/prompts/templates/tool_agent.yaml |
| query_agent | app/prompts/templates/query_agent.yaml |
| system_agent_prompt | app/prompts/templates/system_agent_prompt.yaml |
| creative_writing_prompt | app/prompts/templates/creative_writing_prompt.yaml |
| analyze_text | app/prompts/templates/analyze_text.yaml |

**JSON 配置 (2个)**
| 模块 | 路径 |
|---|---|
| default_prompts | app/services/ai/prompts/default.json |
| novel_analysis | app/services/ai/prompts/novel_analysis.json |

### 使用示例

```python
from app.prompts import PromptConfig, PromptCategory, PromptFileType

# 获取所有模块（26个）
all_modules = PromptConfig.list_all_modules()

# 按类别获取
agent_prompts = PromptConfig.get_modules_by_category(PromptCategory.AGENT)

# 按文件类型获取
yaml_templates = PromptConfig.get_modules_by_file_type(PromptFileType.YAML)

# 获取模块路径
path = PromptConfig.get_module_path("content_creation_prompts")

# 统计各类别数量
summary = PromptConfig.get_category_summary()

# 统计各文件类型数量
file_summary = PromptConfig.get_file_type_summary()
```

### 遗留问题说明

本次修改创建了 **Prompt 统一索引**，解决了"难以找到 Prompt 位置"的问题。但以下问题仍需后续处理：

| 问题 | 说明 | 建议 |
|---|---|---|
| 内联 Prompt 未索引 | langgraph_agent.py 等文件中有内联 Prompt | 逐步迁移到独立模块 |
| 统一访问接口 | 目前只是索引，无统一访问 API | 可扩展 PromptRegistry |
| 版本控制实际应用 | version 字段仅存储，未实际使用 | 与 PromptVersionManager 集成 |

