# 配置和FAQ 📖

> ⚠️ **文档性质：规划性参考文档**
>
> - 📋 **文档用途**: 描述计划实施后的配置和FAQ
> - ❌ **当前适用性**: 仅20%的基础配置适用
> - ✅ **适用部分**: Redis、OpenAI API等基础环境配置
> - ❌ **不适用部分**: 大部分功能配置（因功能未实现）
> - 💡 **使用建议**: 作为实施完成后的配置参考

---

> 配置参数说明和常见问题解答
>
> **用途**: 部署配置和故障排除
> **维护**: 随项目更新

---

## 📑 目录

- [环境配置](#环境配置)
- [配置参数](#配置参数)
- [部署指南](#部署指南)
- [常见问题FAQ](#常见问题faq)
- [故障排除](#故障排除)
- [回滚方案](#回滚方案)

---

## 环境配置

### 基础环境

```bash
# Python版本
Python >= 3.9

# 必需依赖
pip install tiktoken>=0.5.0          # Token精确计数
pip install pytest>=7.0.0            # 测试框架
pip install pytest-asyncio>=0.21.0   # 异步测试支持
pip install redis>=4.0.0             # Redis客户端

# 可选依赖（长期记忆）
pip install chromadb>=0.4.0          # 向量数据库
pip install sentence-transformers   # 本地Embedding（可选）
```

### 环境变量

**创建文件**：`.env`

```bash
# ===== 基础配置 =====
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-...

# ===== Token计数配置 =====
# 无需配置，自动使用tiktoken

# ===== 摘要生成配置 =====
ENABLE_LLM_SUMMARY=true              # 启用LLM摘要（默认true）
SUMMARY_MODEL=gpt-4o-mini            # 摘要模型
SUMMARY_TIMEOUT=10.0                 # 摘要超时时间（秒）
SUMMARY_MAX_RETRIES=2                # 摘要最大重试次数

# ===== 监控配置 =====
# 使用现有的monitoring.py，无需额外配置

# ===== 长期记忆配置（可选）=====
ENABLE_LONG_TERM_MEMORY=false        # 启用长期记忆（默认false）
VECTOR_STORE_PROVIDER=openai         # openai | local
CHROMA_PERSIST_DIR=./data/chroma_db  # ChromaDB持久化目录

# ===== 自适应预算配置（可选）=====
ENABLE_ADAPTIVE_BUDGET=false         # 启用自适应分配（默认false）
TOKEN_BUDGET_TOTAL=8000              # 总Token预算

# ===== 智能提取配置（可选）=====
ENABLE_SMART_EXTRACTION=false        # 启用智能提取（默认false）
ENABLE_NER=false                     # 命名实体识别
ENABLE_SEMANTIC_EXTRACTION=false     # 语义分析

# ===== 调试配置 =====
LOG_LEVEL=INFO                       # DEBUG | INFO | WARNING | ERROR
```

---

## 配置参数

### TokenCounter 配置

```python
from app.services.context.token_counter import TokenCounter

# 默认配置（推荐）
counter = TokenCounter(
    model="gpt-4",           # 模型名称
    fallback_enabled=True    # 启用降级策略
)

# 自定义配置
counter = TokenCounter(
    model="gpt-4o-mini",
    fallback_enabled=False  # 禁用降级（不推荐）
)
```

### SummaryService 配置

```python
from app.services.context.summary_service import SummaryService

# 默认配置
service = SummaryService(
    ai_service=ai_service,
    model="gpt-4o-mini",     # 摘要模型
    max_retries=2            # 最大重试次数
)

# 自定义配置
service = SummaryService(
    ai_service=ai_service,
    model="gpt-4o",          # 使用更强的模型
    max_retries=3,           # 增加重试次数
    timeout=15.0             # 自定义超时
)
```

### ContextManager 配置

```python
from app.services.context.manager import ContextManager
from app.services.context.models import TokenBudget

# 基础配置
manager = ContextManager(
    ai_service=ai_service
)

# 完整配置
manager = ContextManager(
    store=RedisContextStore(),
    token_budget=TokenBudget(
        total=8000,
        system_prompt=0.20,
        summary=0.25,
        short_memory=0.35,
        tools=0.15,
        reserved=0.05
    ),
    ai_service=ai_service,
    enable_long_term_memory=False,    # 长期记忆
    enable_adaptive_budget=False,     # 自适应分配
    enable_smart_extraction=False     # 智能提取
)
```

### VectorMemoryStore 配置

```python
from app.services.context.vector_memory_store import VectorMemoryStore

# 使用OpenAI Embedding（推荐）
store = VectorMemoryStore(
    persist_directory="./data/chroma_db",
    embedding_provider="openai"
)

# 使用本地Embedding（免费）
store = VectorMemoryStore(
    persist_directory="./data/chroma_db",
    embedding_provider="local"
)
```

---

## 部署指南

### 本地开发部署

```bash
# 1. 克隆项目
git checkout alin3.0  # 或对应分支

# 2. 安装依赖
cd backend
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 4. 启动Redis
redis-server

# 5. 运行测试
pytest tests/integration/ -v

# 6. 启动服务
python main.py
```

### 生产环境部署

```bash
# 1. 准备环境
# 确保Python 3.9+, Redis已安装

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
# 编辑 /etc/environment 或使用systemd环境文件

# 4. 启动服务（使用systemd）
sudo systemctl start ai-writer-backend
sudo systemctl enable ai-writer-backend

# 5. 验证服务
curl http://localhost:8000/health
```

### Docker部署

```bash
# 构建镜像
docker build -t ai-writer-backend .

# 运行容器
docker run -d \
  --name ai-writer \
  -p 8000:8000 \
  -e REDIS_URL=redis://redis:6379/0 \
  -e OPENAI_API_KEY=sk-... \
  -v ./data:/app/data \
  ai-writer-backend

# 查看日志
docker logs -f ai-writer
```

---

## 常见问题FAQ

### Q1: 为什么使用gpt-4o-mini而不是gpt-4？

**A**: 摘要生成是高频操作，gpt-4o-mini可以：
- **降低成本**：约1/10的价格（$0.15/1M tokens vs $30/1M tokens）
- **提高速度**：响应更快，减少用户等待时间
- **质量足够**：对于摘要任务，gpt-4o-mini的质量已经足够（8/10）

**何时使用gpt-4**：
- 需要极高质量的摘要（9+/10）
- 预算充足
- 用户明确要求

---

### Q2: 降级策略会不会导致质量下降？

**A**: 降级策略设计原则：
- **触发条件**：只在LLM失败时触发（如API超时、网络错误）
- **质量保障**：简单提取好于完全失败（3/10 vs 0/10）
- **监控记录**：所有降级会被监控系统记录
- **优化路径**：根据降级数据优化降级逻辑

**降级率指标**：
- 正常情况：< 5%
- 需要关注：5-10%
- 需要处理：> 10%

---

### Q3: 自适应分配是否适合所有场景？

**A**: 不是，建议：
- **初期默认禁用**：先使用固定分配，收集数据
- **稳定场景启用**：系统稳定后，在特定场景启用
- **A/B测试验证**：对比启用前后的效果
- **根据反馈调整**：根据用户反馈调整分配比例

**适合场景**：
- 创作型应用（小说、剧本）
- 分析型应用（代码分析、数据分析）
- 有明确任务类型的应用

**不适合场景**：
- 任务类型混杂的应用
- 对话模式不固定的应用

---

### Q4: 如何判断实施是否成功？

**A**: 关键指标：

| 指标 | 目标值 | 测量方式 |
|------|--------|----------|
| Token估算准确率 | > 95% | 对比tiktoken结果 |
| 摘要质量评分 | > 8/10 | 人工评估 |
| 压缩率 | 60-70% | 监控指标 |
| 系统稳定性 | 100% | 无崩溃、无数据丢失 |
| LLM成功率 | > 90% | 监控降级率 |

**验证步骤**：
```bash
# 1. 运行测试套件
pytest tests/integration/ -v

# 2. 检查监控指标
python -c "
from app.services.context.monitoring_integration import get_metrics_summary
print(get_metrics_summary())
"

# 3. 人工验证摘要质量
# 创建20轮对话，检查摘要是否保留关键信息
```

---

### Q5: 出现问题如何快速回滚？

**A**: 回滚步骤见下方 [回滚方案](#回滚方案)。

---

### Q6: tiktoken安装失败怎么办？

**A**: 解决步骤：
```bash
# 1. 更新pip
python -m pip install --upgrade pip

# 2. 使用国内镜像源
pip install tiktoken -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 如果仍失败，使用降级策略
# 系统会自动使用中文优化估算，无需tiktoken
```

---

### Q7: 长期记忆的成本如何？

**A**: 成本分析：

**使用OpenAI Embedding**：
- Embedding成本：$0.02/1M tokens
- 100万条记忆 × 200 tokens = $4/月
- 推荐：适合生产环境

**使用本地Embedding**：
- Embedding成本：$0（免费）
- 需要GPU资源（可选）
- 推荐：适合开发/测试环境

**存储成本**：
- 本地ChromaDB：免费
- 云端Chroma：$20/月（10万条）

**总成本**：< $10/月（推荐配置）

---

### Q8: Redis连接数过多怎么办？

**A**: 解决方案：
```python
# 在config.py中增加连接池大小
REDIS_MAX_CONNECTIONS = 50  # 默认10

# 或者使用连接池
from redis import ConnectionPool

pool = ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=50
)
```

---

## 故障排除

### 问题1: Token计数不准确

**症状**：Token数量与预期差异 > 10%

**排查步骤**：
```python
# 1. 检查tiktoken是否正常
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
print(enc.encode("测试文本"))

# 2. 检查使用的策略
from app.services.context.token_counter import TokenCounter
counter = TokenCounter()
stats = counter.get_stats()
print(f"当前策略: {stats['current_strategy']}")

# 3. 如果是降级策略，尝试重新安装tiktoken
pip uninstall tiktoken -y
pip install tiktoken
```

---

### 问题2: 摘要生成频繁失败

**症状**：监控显示降级率 > 10%

**排查步骤**：
```python
# 1. 检查AI服务可用性
from app.services.ai.http_ai_service import HTTPAIService
ai_service = HTTPAIService()
result = await ai_service.health_check()
print(f"AI服务健康: {result}")

# 2. 检查超时设置
# 在config.py中增加超时时间
SUMMARY_TIMEOUT = 15.0  # 增加到15秒

# 3. 检查网络连接
curl https://api.openai.com
```

---

### 问题3: Redis连接失败

**症状**：`redis.exceptions.ConnectionError`

**解决方案**：
```bash
# 1. 检查Redis是否运行
redis-cli ping
# 应该返回 PONG

# 2. 检查Redis配置
redis-cli config get bind
redis-cli config get port

# 3. 检查防火墙
sudo ufw status
sudo ufw allow 6379

# 4. 重启Redis
sudo systemctl restart redis
```

---

### 问题4: 内存占用过高

**症状**：内存使用 > 2GB

**排查步骤**：
```bash
# 1. 检查Redis内存
redis-cli info memory

# 2. 清理过期会话
redis-cli --scan --pattern "context:*" | xargs redis-cli del

# 3. 限制Redis最大内存
redis-cli config set maxmemory 1gb
redis-cli config set maxmemory-policy allkeys-lru
```

---

## 回滚方案

### 紧急回滚（5分钟内）

```bash
# 1. 修改配置，禁用新功能
# 在 .env 或 config.py 中：
ENABLE_ADAPTIVE_BUDGET=false
ENABLE_LLM_SUMMARY=false
ENABLE_LONG_TERM_MEMORY=false
ENABLE_SMART_EXTRACTION=false

# 2. 重启服务
sudo systemctl restart ai-writer-backend

# 3. 验证系统恢复
curl http://localhost:8000/health

# 4. 检查监控指标
python -c "
from app.services.context.monitoring_integration import get_metrics_summary
print(get_metrics_summary())
"
```

---

### 完全回滚（30分钟内）

```bash
# 1. 切换到稳定分支
git checkout main

# 2. 重新部署
cd backend
pip install -r requirements.txt

# 3. 重启服务
sudo systemctl restart ai-writer-backend

# 4. 验证功能
pytest tests/test_basic.py -v

# 5. 监控运行状态
tail -f logs/app.log
```

---

### 分步回滚

如果只某个功能有问题，可分步回滚：

#### 只回滚自适应分配

```python
# 在代码中禁用
manager = ContextManager(
    enable_adaptive_budget=False  # 禁用自适应
)
```

#### 只回滚LLM摘要

```python
# 方式1: 不传AI服务
manager = ContextManager(
    ai_service=None  # 使用降级策略
)

# 方式2: 环境变量
ENABLE_LLM_SUMMARY=false
```

#### 只回滚Token精确计数

```bash
# 卸载tiktoken
pip uninstall tiktoken -y

# 系统会自动使用降级策略（中文优化估算）
```

#### 只回滚长期记忆

```python
# 禁用长期记忆
manager = ContextManager(
    enable_long_term_memory=False
)

# 或删除向量数据
rm -rf ./data/chroma_db
```

---

## 监控和维护

### 日常监控

```bash
# 查看应用日志
tail -f logs/app.log | grep ERROR

# 查看监控指标
python -c "
from app.services.context.monitoring_integration import get_metrics_summary
import json
print(json.dumps(get_metrics_summary(), indent=2))
"

# 检查Redis状态
redis-cli info stats
```

### 定期维护

```bash
# 每周：清理过期数据
redis-cli --scan --pattern "context:*" | \
  while read key; do
    ttl=$(redis-cli ttl $key)
    if [ $ttl -eq -1 ]; then
      redis-cli del $key
    fi
  done

# 每月：备份向量数据库
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz ./data/chroma_db

# 每季度：性能基准测试
pytest tests/integration/test_performance_benchmark_e2e.py -v
```

---

**最后更新**: 2025-01-08

**下一步**: 开始实施 [01_Day1-2_Token估算改进.md](./01_Day1-2_Token估算改进.md) 🚀
