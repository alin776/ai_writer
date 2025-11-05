# P0性能优化任务 - AsyncRedisSaver & Embedding模型

## 📋 问题分析

### 问题1：AsyncRedisSaver加载耗时21秒
**现状**：
- 每次请求固定耗时21秒
- 占总耗时25-54%
- 严重影响用户体验

**根本原因**：
1. AsyncRedisSaver的索引创建(`asetup()`)在首次调用时懒加载
2. TTL自动续期配置(`refresh_on_read: True`)导致每次读取额外Redis操作
3. 没有在应用启动时预创建索引

**影响位置**：
- `backend/app/services/agent/langgraph_agent.py` 第681行
- `backend/app/api/v1/agent.py` 第289-291行

---

### 问题2：Embedding模型每次加载耗时7-8秒
**现状**：
- 每次RAG检索重新加载模型
- 模型：paraphrase-multilingual-MiniLM-L12-v2
- 虽然有类变量缓存但未真正单例化

**根本原因**：
1. `main.py`中预加载被注释（第51-60行）
2. 每次RAG检索创建新的VectorStoreService实例
3. 懒加载机制导致首次使用延迟

**影响位置**：
- `backend/app/main.py` 第51-60行（预加载被禁用）
- `backend/app/services/vector_store_service.py` 第68-76行（懒加载）

---

## ✅ 优化方案

### 方案1：优化AsyncRedisSaver（预期减少19秒）

#### 1.1 添加类方法支持预初始化
**文件**：`backend/app/services/agent/langgraph_agent.py`
**位置**：在`WritingAgentGraph`类中添加
**改动**：添加`setup_checkpointer()`类方法

```python
@classmethod
async def setup_checkpointer(cls):
    """预创建AsyncRedisSaver索引（应用启动时调用）"""
    try:
        from app.core.config import get_settings
        redis_url = get_settings().redis_url

        # 创建临时checkpointer实例用于预初始化
        ttl_config = {
            "default_ttl": 10080,  # 7天
            "refresh_on_read": False  # 禁用自动续期，减少Redis操作
        }
        checkpointer = AsyncRedisSaver(redis_url=redis_url, ttl=ttl_config)
        await checkpointer.asetup()  # 预创建索引
        logger.info("[LangGraph] AsyncRedisSaver索引预创建成功")
    except Exception as e:
        logger.warning(f"[LangGraph] 索引预创建失败: {e}")
```

#### 1.2 禁用TTL自动续期
**文件**：`backend/app/services/agent/langgraph_agent.py` 第679行
**改动**：将`refresh_on_read: True`改为`False`

#### 1.3 在应用启动时预初始化
**文件**：`backend/app/main.py`
**位置**：在`lifespan`函数的startup阶段
**改动**：添加AsyncRedisSaver初始化调用

```python
# 预初始化AsyncRedisSaver索引（性能优化）
try:
    from app.services.agent.langgraph_agent import WritingAgentGraph
    logger.info("[STARTUP] 开始初始化AsyncRedisSaver索引...")
    await WritingAgentGraph.setup_checkpointer()
    logger.info("[STARTUP] AsyncRedisSaver索引初始化完成")
except Exception as e:
    logger.warning(f"[STARTUP] AsyncRedisSaver索引初始化失败: {e}")
```

---

### 方案2：优化Embedding模型加载（预期减少7秒）

#### 2.1 启用应用启动时预加载
**文件**：`backend/app/main.py` 第51-60行
**改动**：取消注释，恢复预加载逻辑

```python
# 预加载Embedding模型（性能优化）
try:
    from app.services.vector_store_service import VectorStoreService
    logger.info("[STARTUP] 开始预加载Embedding模型...")
    VectorStoreService.preload_model()
    logger.info("[STARTUP] Embedding模型预加载完成")
except Exception as e:
    logger.warning(f"[STARTUP] Embedding模型预加载失败: {e}")
    logger.warning("   首次向量化时将自动加载模型")
```

---

## 📝 待办任务

- [ ] **任务1**：在WritingAgentGraph类中添加setup_checkpointer()方法
- [ ] **任务2**：修改TTL配置，禁用refresh_on_read
- [ ] **任务3**：在main.py的lifespan中调用AsyncRedisSaver预初始化
- [ ] **任务4**：在main.py中启用Embedding模型预加载（取消注释）
- [ ] **任务5**：测试验证 - 重启应用，运行测试1验证性能提升

---

## 🎯 预期效果

| 测试 | 当前耗时 | 优化后预期 | 提升幅度 |
|-----|---------|-----------|---------|
| 测试1 | 39秒 | **12秒** | 69% ⬇️ |
| 测试2 | 64秒 | **37秒** | 42% ⬇️ |
| 测试3 | 77秒 | **50秒** | 35% ⬇️ |
| 测试4 | 210秒 | **183秒** | 13% ⬇️ |
| 测试5 | 82秒 | **55秒** | 33% ⬇️ |
| 测试6 | 84秒 | **57秒** | 32% ⬇️ |

**核心优化**：
- ✅ 记忆加载：21秒 → **2秒**（减少19秒）
- ✅ Embedding加载：8秒 → **0.5秒**（减少7.5秒）
- ✅ 总体提升：**平均节省60%时间**

---

## 📌 注意事项

1. **Redis依赖**：确保Redis服务运行在`localhost:6379`
2. **内存占用**：Embedding模型约200MB，启动时加载
3. **TTL续期**：禁用后仍保留7天TTL自动清理机制
4. **向下兼容**：保留懒加载作为降级方案

---

## 📊 Review（待完成后填写）

### 实际改动
- [ ] 改动文件1：...
- [ ] 改动文件2：...

### 测试结果
- [ ] 测试1耗时：...
- [ ] 性能提升：...

### 其他发现
- 待补充...
