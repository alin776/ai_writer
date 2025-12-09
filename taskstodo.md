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
| 问题 | 描述 |
|---|---|
| Prompt 分散存储 | 分布于 backend/app/prompts/*、backend/app/services/agent/prompts/*、backend/app/prompts/templates/* 等，难以维护 |
| 缺乏 Prompt 版本管理 | 目前无版本元数据，无法追踪演变 |
| langgraph_agent.py 过大 | 4500+ 行，建议按节点/工具拆分 |
| 记忆系统复杂度高 | 跨 context/memory/agent，多处逻辑缺统一接口和测试 |

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
└── memory_config.py     # Memory 模块配置（新增）
    ├── TTL 配置
    ├── 容量限制
    ├── 锁超时配置
    └── 遗忘策略参数
```
