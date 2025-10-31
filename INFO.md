(venv) PS D:\Java\ai_writer\backend> python tests/test_memory_system.py
19:03:13 [INFO] __main__ - ================================================================================
19:03:13 [INFO] __main__ - 🧪 增强记忆管理系统自动化测试
19:03:13 [INFO] __main__ - 🌐 后端地址: http://localhost:8000
19:03:13 [INFO] __main__ - 📧 测试账号: 2072855200@qq.com
19:03:13 [INFO] __main__ - ================================================================================
19:03:13 [INFO] __main__ -
================================================================================
19:03:13 [INFO] __main__ - 📝 测试1: 用户登录 (OAuth2 form data)
19:03:13 [INFO] __main__ - ================================================================================
19:03:13 [INFO] __main__ - ➤ 发送登录请求...
19:03:14 [INFO] httpx - HTTP Request: POST http://localhost:8000/api/v1/auth/login "HTTP/1.1 200 OK"
19:03:14 [INFO] __main__ - ✓ 响应时间: 0.291s
19:03:14 [INFO] __main__ - ✓ 状态码: 200
19:03:14 [INFO] __main__ - ✓ 获取到 Token: eyJhbGciOiJIUzI1NiIs...
19:03:14 [INFO] __main__ - ✓ User ID: 2072855200@qq.com
19:03:14 [INFO] __main__ - ✅ 测试1通过: 登录成功
19:03:14 [INFO] __main__ -
➤ 连接Redis...
19:03:14 [INFO] __main__ - ✓ Redis连接成功
19:03:14 [INFO] __main__ -
================================================================================
19:03:14 [INFO] __main__ - 📝 测试0: 清理测试数据
19:03:14 [INFO] __main__ - ================================================================================
19:03:14 [INFO] __main__ - ➤ 清理用户 2072855200@qq.com 的记忆数据...
19:03:16 [INFO] __main__ - ✓ 清理完成,删除了 0 个key
19:03:16 [INFO] __main__ - ✅ 测试0通过: 数据清理成功
19:03:16 [INFO] __main__ -
➤ 初始化EnhancedMemoryManager...
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1
19:03:16 [INFO] __main__ - ✓ MemoryManager初始化成功
19:03:16 [INFO] __main__ -
================================================================================
19:03:16 [INFO] __main__ - 📝 测试2: 添加记忆
19:03:16 [INFO] __main__ - ================================================================================
19:03:16 [INFO] __main__ - ➤ 准备添加 10 条记忆...
D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py:417: RuntimeWarning: coroutine 'Redis.execute_command' was never awaited
  self.redis.lpush(key, memory.model_dump_json())
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py:419: RuntimeWarning: coroutine 'Redis.execute_command' was never awaited
  self.redis.ltrim(key, 0, self.short_term_size - 1)
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py:421: RuntimeWarning: coroutine 'Redis.execute_command' was never awaited
  self.redis.expire(key, 3600)  # 1小时
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - Memory mem_ce02cac37475 added to short-term for user 2072855200@qq.com
19:03:16 [WARNING] app.services.agent.memory.enhanced_memory_manager - Forgetting failed for user 2072855200@qq.com: 'coroutine' object is not iterable
D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py:141: RuntimeWarning: coroutine 'Redis.execute_command' was never awaited
  logger.warning(f"Forgetting failed for user {user_id}: {e}")
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
19:03:16 [INFO] __main__ -   1. [user] 我想写一部玄幻小说... (importance=0.9)
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - Memory mem_501d94d2ae7c added to short-term for user 2072855200@qq.com
19:03:16 [WARNING] app.services.agent.memory.enhanced_memory_manager - Forgetting failed for user 2072855200@qq.com: 'coroutine' object is not iterable
19:03:16 [INFO] __main__ -   2. [assistant] 好的,我可以帮您创作玄幻小说... (importance=0.7)
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - Memory mem_8c623de027ff added to short-term for user 2072855200@qq.com
19:03:16 [WARNING] app.services.agent.memory.enhanced_memory_manager - Forgetting failed for user 2072855200@qq.com: 'coroutine' object is not iterable
19:03:16 [INFO] __main__ -   3. [user] 主角叫李云天,是一个天才修士... (importance=0.95)
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - Memory mem_02142f2eb270 added to short-term for user 2072855200@qq.com
19:03:16 [WARNING] app.services.agent.memory.enhanced_memory_manager - Forgetting failed for user 2072855200@qq.com: 'coroutine' object is not iterable
19:03:16 [INFO] __main__ -   4. [assistant] 李云天这个名字不错,很有仙侠风格... (importance=0.6)
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - Memory mem_391ab8daf9b4 added to short-term for user 2072855200@qq.com
19:03:16 [WARNING] app.services.agent.memory.enhanced_memory_manager - Forgetting failed for user 2072855200@qq.com: 'coroutine' object is not iterable
19:03:16 [INFO] __main__ -   5. [user] 世界观设定在九州大陆... (importance=0.85)
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - Memory mem_eaf7cee0cae4 added to short-term for user 2072855200@qq.com
19:03:16 [WARNING] app.services.agent.memory.enhanced_memory_manager - Forgetting failed for user 2072855200@qq.com: 'coroutine' object is not iterable
19:03:16 [INFO] __main__ -   6. [assistant] 九州大陆可以分为中州、东域、西荒等区域... (importance=0.7)
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - Memory mem_eda657cf9746 added to short-term for user 2072855200@qq.com
19:03:16 [WARNING] app.services.agent.memory.enhanced_memory_manager - Forgetting failed for user 2072855200@qq.com: 'coroutine' object is not iterable
19:03:16 [INFO] __main__ -   7. [user] 修炼体系分为炼气、筑基、金丹、元婴... (importance=0.9)
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - Memory mem_4c2d04d604b7 added to short-term for user 2072855200@qq.com
19:03:16 [WARNING] app.services.agent.memory.enhanced_memory_manager - Forgetting failed for user 2072855200@qq.com: 'coroutine' object is not iterable
19:03:16 [INFO] __main__ -   8. [assistant] 这是经典的修仙体系... (importance=0.5)
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - Memory mem_4e03f0169641 added to short-term for user 2072855200@qq.com
19:03:16 [WARNING] app.services.agent.memory.enhanced_memory_manager - Forgetting failed for user 2072855200@qq.com: 'coroutine' object is not iterable
19:03:16 [INFO] __main__ -   9. [user] 第一章从李云天被逐出家族开始... (importance=0.8)
19:03:16 [INFO] app.services.agent.memory.enhanced_memory_manager - Memory mem_de75fd8a5d68 added to short-term for user 2072855200@qq.com
19:03:16 [WARNING] app.services.agent.memory.enhanced_memory_manager - Forgetting failed for user 2072855200@qq.com: 'coroutine' object is not iterable
19:03:16 [INFO] __main__ -   10. [assistant] 废材逆袭的开局很吸引人... (importance=0.6)
19:03:16 [INFO] __main__ - ✓ 成功添加 10 条记忆
19:03:16 [INFO] __main__ - ✓ 所有记忆ID唯一
19:03:16 [INFO] __main__ - ✅ 测试2通过: 记忆添加成功
19:03:16 [INFO] __main__ -
================================================================================
19:03:16 [INFO] __main__ - 📝 测试3: 获取最近记忆
19:03:16 [INFO] __main__ - ================================================================================
19:03:16 [INFO] __main__ - ➤ 获取最近5条短期记忆...
19:03:16 [ERROR] __main__ - ✗ 测试3失败: 'coroutine' object is not iterable
19:03:16 [ERROR] __main__ - Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\tests\test_memory_system.py", line 273, in test_3_get_recent_memories
    recent = memory_manager.get_recent_memories(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py", line 176, in get_recent_memories
    return self._get_short_term_memories(user_id, limit)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py", line 429, in _get_short_term_memories
    for data in data_list:
TypeError: 'coroutine' object is not iterable

D:\Java\ai_writer\backend\tests\test_memory_system.py:325: RuntimeWarning: coroutine 'Redis.execute_command' was never awaited
  return False
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
19:03:16 [INFO] __main__ -
================================================================================
19:03:16 [INFO] __main__ - 📝 测试4: 关键词搜索
19:03:16 [INFO] __main__ - ================================================================================
19:03:16 [INFO] __main__ - ➤ 搜索关键词: ['主角', '李云天']
19:03:16 [ERROR] __main__ - ✗ 测试4失败: 'coroutine' object is not iterable
19:03:16 [ERROR] __main__ - Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\tests\test_memory_system.py", line 343, in test_4_search_keywords
    results = memory_manager.search_memories(
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py", line 224, in search_memories
    self._get_short_term_memories(user_id, self.short_term_size)
  File "D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py", line 429, in _get_short_term_memories
    for data in data_list:
TypeError: 'coroutine' object is not iterable

D:\Java\ai_writer\backend\tests\test_memory_system.py:371: RuntimeWarning: coroutine 'Redis.execute_command' was never awaited
  return False
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
19:03:16 [INFO] __main__ -
================================================================================
19:03:16 [INFO] __main__ - 📝 测试5: 智能遗忘策略
19:03:16 [INFO] __main__ - ================================================================================
19:03:16 [INFO] __main__ - ➤ 获取遗忘前的统计信息...
19:03:16 [ERROR] __main__ - ✗ 测试5失败: 'coroutine' object is not iterable
19:03:16 [ERROR] __main__ - Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\tests\test_memory_system.py", line 388, in test_5_smart_forgetting
    stats_before = memory_manager.get_stats(self.user_id)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py", line 543, in get_stats
    short_memories = self._get_short_term_memories(user_id, self.short_term_size)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py", line 429, in _get_short_term_memories
    for data in data_list:
TypeError: 'coroutine' object is not iterable

D:\Java\ai_writer\backend\tests\test_memory_system.py:414: RuntimeWarning: coroutine 'Redis.execute_command' was never awaited
  return False
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
19:03:16 [INFO] __main__ -
================================================================================
19:03:16 [INFO] __main__ - 📝 测试6: 快照创建和恢复
19:03:16 [INFO] __main__ - ================================================================================
19:03:16 [INFO] __main__ - ➤ 创建记忆快照...
19:03:16 [ERROR] __main__ - ✗ 测试6失败: 'coroutine' object is not iterable
19:03:16 [ERROR] __main__ - Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\tests\test_memory_system.py", line 432, in test_6_snapshot
    snapshot_id = memory_manager.create_snapshot(
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py", line 361, in create_snapshot
    short_term_memories=self._get_short_term_memories(user_id, self.short_term_size),
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py", line 429, in _get_short_term_memories
    for data in data_list:
TypeError: 'coroutine' object is not iterable

D:\Java\ai_writer\backend\tests\test_memory_system.py:475: RuntimeWarning: coroutine 'Redis.execute_command' was never awaited
  return False
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
19:03:16 [INFO] __main__ -
================================================================================
19:03:16 [INFO] __main__ - 📝 测试7: 统计信息
19:03:16 [INFO] __main__ - ================================================================================
19:03:16 [INFO] __main__ - ➤ 获取记忆统计信息...
19:03:16 [ERROR] __main__ - ✗ 测试7失败: 'coroutine' object is not iterable
19:03:16 [ERROR] __main__ - Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\tests\test_memory_system.py", line 492, in test_7_stats
    stats = memory_manager.get_stats(self.user_id)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py", line 543, in get_stats
    short_memories = self._get_short_term_memories(user_id, self.short_term_size)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\memory\enhanced_memory_manager.py", line 429, in _get_short_term_memories
    for data in data_list:
TypeError: 'coroutine' object is not iterable

D:\Java\ai_writer\backend\tests\test_memory_system.py:512: RuntimeWarning: coroutine 'Redis.execute_command' was never awaited
  return False
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
D:\Java\ai_writer\backend\tests\test_memory_system.py:590: DeprecationWarning: Call to deprecated close. (Use aclose() instead) -- Deprecated since version 5.0.0.
  await redis_client.close()
19:03:16 [INFO] __main__ -
✓ Redis连接已关闭
19:03:16 [INFO] __main__ -
================================================================================
19:03:16 [INFO] __main__ - 📊 测试结果总结
19:03:16 [INFO] __main__ - ================================================================================
19:03:16 [INFO] __main__ -
总测试数: 8
19:03:16 [INFO] __main__ - ✅ 通过: 3
19:03:16 [INFO] __main__ - ✗ 失败: 5
19:03:16 [INFO] __main__ - ⊘ 跳过: 0
19:03:16 [INFO] __main__ -
详细结果:
19:03:16 [INFO] __main__ -   login: ✅ 通过
19:03:16 [INFO] __main__ -   cleanup: ✅ 通过
19:03:16 [INFO] __main__ -   add_memory: ✅ 通过
19:03:16 [INFO] __main__ -   get_recent: ✗ 失败
19:03:16 [INFO] __main__ -   search_keywords: ✗ 失败
19:03:16 [INFO] __main__ -   smart_forgetting: ✗ 失败
19:03:16 [INFO] __main__ -   snapshot: ✗ 失败
19:03:16 [INFO] __main__ -   stats: ✗ 失败
19:03:16 [INFO] __main__ -
成功率: 37.5%
19:03:16 [WARNING] __main__ -
⚠ 有 5 个测试失败,请检查日志
19:03:16 [INFO] __main__ - ================================================================================
(venv) PS D:\Java\ai_writer\backend>