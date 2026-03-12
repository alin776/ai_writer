# Redis LOADING 阻塞全站修复小结

**日期**: 2026-03-12
**影响范围**: 全站不可用（前端弹出 "Redis is loading the dataset in memory"）

---

## 问题现象

Redis 容器重启后，前端弹出红色错误 "Redis is loading the dataset in memory"，所有 API 请求失败，WebSocket/SSE 连接反复断开重连，整站不可用持续数分钟。

## 根因分析

Redis 未设置 `maxmemory` 上限（值为 0），同时多处缓存 TTL 过长（会话缓存 30 天、LangGraph 检查点 7 天、分析结果 7 天、用户偏好 90 天），导致数据膨胀至 3.8 GB 内存 / 13.8 GB 磁盘持久化文件；每次 Redis 重启需从磁盘加载全部数据，期间拒绝一切读写请求，后端全局异常处理器又将原始错误信息直接透传给了前端。

## 讨论过的方案

| 方案 | 结论 |
|------|------|
| 仅加 `maxmemory` + LRU 淘汰 | 能控增量，但存量已膨胀，重启仍慢 |
| 后端降级 + 前端友好提示 | 治标不治本，数据继续膨胀 |
| 关闭持久化（纯缓存模式） | LangGraph 检查点依赖持久化保障对话连续性，不宜一刀切 |
| **maxmemory 上限 + 缩减 TTL**（采用） | 最小改动、从源头控制数据量，兼顾持久化需求 |

## 最终修复（8 处改动）

**短期 — Redis 容量管控（docker-compose.prod.yml）**:
```yaml
command: redis-stack-server --appendonly yes --maxmemory 1gb --maxmemory-policy allkeys-lru
```

**中期 — TTL 瘦身（7 处代码）**:

| 位置 | 原值 | 新值 |
|------|------|------|
| `backend/app/api/v1/agent.py:180` SESSION_CACHE_TTL_SECONDS | 30 天 | 2 天 |
| `backend/app/api/v1/agent.py:722` LangGraph checkpoint TTL | 7 天 | 3 天 |
| `backend/app/services/redis_cache_service.py:138` 分析结果默认 TTL | 7 天 | 2 天 |
| `backend/app/services/redis_cache_service.py:238` 向量缓存 TTL | 7 天 | 2 天 |
| `backend/app/services/redis_cache_service.py:311` 章节解析缓存 TTL | 7 天 | 2 天 |
| `backend/app/services/ai/novel_micro_analysis.py:172` 微分析调用处 TTL | 7 天 | 2 天 |
| `backend/app/services/agent/memory/long_term_memory.py:93` 用户偏好/记忆 TTL | 90 天 | 14 天 |

**部署**: 重建 Redis 容器（清除 13.8 GB 旧持久化数据，空库启动 < 1 秒）+ 重建 Backend 容器。

## 回归测试点

- [ ] AI 对话功能正常，多轮上下文保持连贯（LangGraph 检查点仍工作）
- [ ] 切换章节/作品时缓存命中正常，无明显延迟
- [ ] 用户偏好和写作风格在 14 天内持续生效
- [ ] 小说分析结果在 2 天内可复用，过期后按需重新分析
- [ ] Redis 内存稳态控制在 1 GB 以内（`redis-cli INFO memory` 监控）
- [ ] 模拟 Redis 重启后，启动耗时应在秒级，无 LOADING 阻塞

## 后续可优化项（按优先级排序）

1. **[高] 修复 Redis 持久化路径**: 当前 docker-compose 卷挂载在 `/data`，但 redis-stack-server 实际写入 `/var/lib/redis-stack/`，持久化文件存于容器层而非卷中，容器重建即丢失——需在 command 中加 `--dir /data` 或改卷挂载路径
2. **[高] 全局异常处理器脱敏**: `main.py` 的 `global_exception_handler` 将 `str(exc)` 直接返回前端，应替换为友好提示，技术细节仅写日志
3. **[中] 前端 SessionManager 循环风暴**: 浏览器日志中 "创建会话 → 内存限制删除 → 断开SSE" 无限循环，浪费后端资源，需排查 session 池上限逻辑
4. **[中] LangGraph 检查点迁移至 PostgreSQL**: `agent_session_messages` 表已存完整对话记录，检查点数据冗余，迁移后 Redis 可彻底作为纯缓存运行
5. **[低] 添加 Redis 内存监控告警**: 在内存使用超过 maxmemory 80% 时触发告警，提前预警
