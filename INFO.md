INFO:     127.0.0.1:63175 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
20:22:00 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和心理变化 2. 能力体系和成长轨迹 3....
20:22:00 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和心理变化 2. 能力体系和成长轨迹 3....
20:22:00 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
20:22:00 app.services.agent.langgraph_agent INFO   [Intent] 开始识别意图: 请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和心理变化 2. 能力体系和成长轨迹 3....
20:22:18 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
20:22:18 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=bd3a71a2-cfda-4bad-9834-8eca4f151f6e, model=gemini-2.5-pro, duration=18.79s, tokens=2209 (prompt=2124, completion=85)
20:22:18 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=2209
20:22:18 app.services.agent.langgraph_agent INFO   [Intent] 识别结果: tool, 置信度: 0.95
20:22:18 app.services.agent.langgraph_agent INFO   [Intent] 用户意图: tool, 置信度: 0.95, 原因: 用户要求对已有的小说内容（特定角色）进行深度分析和信息提取，这属于查询小说内容和信息的范畴，符合tool意图的定义。
20:22:18 app.services.agent.langgraph_agent INFO   [Intent] 选择 Prompt 模板: tool_agent, 版本: 2.0.0
20:22:18 app.services.context.manager INFO   [ContextManager] 创建新上下文: e7803789-de9d-4f64-ad8f-34713d465b11
20:22:18 app.services.context.manager INFO   [ContextManager] Session e7803789-de9d-4f64-ad8f-34713d465b11: 1078/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 14.57it/s]
20:22:19 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
20:22:19 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和...' | 找到=3条 | 阈值=0.3
20:22:19 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 2条消息, 1078 tokens, 耗时 77.83ms
20:22:19 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': 'e7803789-de9d-4f64-ad8f-34713d465b11', 'token_count': 1078, 'short_memory_size': 0, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
20:22:19 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类
20:22:35 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
20:22:35 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=44cbdbb9-9ad4-48de-90bf-a9141f6732bd, model=gemini-2.5-pro, duration=16.55s, tokens=699 (prompt=698, completion=1)
20:22:35 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=699
20:22:35 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: analysis
20:22:35 app.services.agent.langgraph_agent INFO   [LangGraph] 处理分析请求（新架构）
20:22:35 Action.analysis INFO   [analysis] PromptManager已初始化
20:22:35 Action.analysis INFO   [analysis] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
20:22:35 app.services.agent.langgraph_agent INFO   [LangGraph] AnalysisAction准备完成: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
20:22:35 app.services.agent.langgraph_agent INFO   [LangGraph] 处理analysis场景 (use_chatgpt=True)
20:23:04 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
20:23:04 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=d40de403-f0fa-4eb6-923d-9736cf9ee683, model=gemini-2.5-pro, duration=28.98s, tokens=3168 (prompt=2984, completion=184)
20:23:04 app.services.agent.langgraph_agent INFO   [LangGraph] 检测到工具调用: 5 个工具
20:23:04 app.services.vector_store_service INFO   RAG检索: work_id=YXTW_001, query=对《一夕千悟》主角段融的性格特征、心理变化、能力体系、成长轨迹、人际关系、社交网络、主要挑战和困境、...
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 19.82it/s]
20:23:04 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] 读取章节失败: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_2' (invalid UUID 'ch_2': length must be between 32..36 characters, got 4)
[SQL: SELECT chapters.id, chapters.work_id, chapters.title, chapters.content, chapters.summary, chapters.status, chapters."order", chapters.is_published, chapters.word_count, chapters.view_count, chapters.created_at, chapters.updated_at, chapters.published_at
FROM chapters
WHERE chapters.id = $1::UUID]
[parameters: ('ch_2',)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
Traceback (most recent call last):
  File "asyncpg\protocol\prepared_stmt.pyx", line 175, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
  File "asyncpg\protocol\codecs/base.pyx", line 227, in asyncpg.protocol.protocol.Codec.encode
  File "asyncpg\protocol\codecs/base.pyx", line 129, in asyncpg.protocol.protocol.Codec.encode_scalar
  File "asyncpg\pgproto\./codecs/uuid.pyx", line 16, in asyncpg.pgproto.pgproto.uuid_encode
  File "asyncpg\pgproto\./uuid.pyx", line 88, in asyncpg.pgproto.pgproto.pg_uuid_bytes_from_str
ValueError: invalid UUID 'ch_2': length must be between 32..36 characters, got 4

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 546, in _prepare_and_execute
    self._rows = await prepared_stmt.fetch(*parameters)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 176, in fetch
    data = await self.__bind_execute(args, 0, timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 241, in __bind_execute
    data, status, _ = await self.__do_execute(
                      ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 230, in __do_execute
    return await executor(protocol)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "asyncpg\protocol\protocol.pyx", line 186, in bind_execute
  File "asyncpg\protocol\prepared_stmt.pyx", line 204, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
asyncpg.exceptions.DataError: invalid input for query argument $1: 'ch_2' (invalid UUID 'ch_2': length must be between 32..36 characters, got 4)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.Error: <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_2' (invalid UUID 'ch_2': length must be between 32..36 characters, got 4)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 387, in read_chapter_tool
    chapter = await chapter_service.get_chapter_by_id(chapter_id)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
    return meth(
           ^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1639, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2344, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_2' (invalid UUID 'ch_2': length must be between 32..36 characters, got 4)
[SQL: SELECT chapters.id, chapters.work_id, chapters.title, chapters.content, chapters.summary, chapters.status, chapters."order", chapters.is_published, chapters.word_count, chapters.view_count, chapters.created_at, chapters.updated_at, chapters.published_at
FROM chapters
WHERE chapters.id = $1::UUID]
[parameters: ('ch_2',)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
20:23:04 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] 读取章节失败: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_4' (invalid UUID 'ch_4': length must be between 32..36 characters, got 4)
[SQL: SELECT chapters.id, chapters.work_id, chapters.title, chapters.content, chapters.summary, chapters.status, chapters."order", chapters.is_published, chapters.word_count, chapters.view_count, chapters.created_at, chapters.updated_at, chapters.published_at
FROM chapters
WHERE chapters.id = $1::UUID]
[parameters: ('ch_4',)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
Traceback (most recent call last):
  File "asyncpg\protocol\prepared_stmt.pyx", line 175, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
  File "asyncpg\protocol\codecs/base.pyx", line 227, in asyncpg.protocol.protocol.Codec.encode
  File "asyncpg\protocol\codecs/base.pyx", line 129, in asyncpg.protocol.protocol.Codec.encode_scalar
  File "asyncpg\pgproto\./codecs/uuid.pyx", line 16, in asyncpg.pgproto.pgproto.uuid_encode
  File "asyncpg\pgproto\./uuid.pyx", line 88, in asyncpg.pgproto.pgproto.pg_uuid_bytes_from_str
ValueError: invalid UUID 'ch_4': length must be between 32..36 characters, got 4

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 546, in _prepare_and_execute
    self._rows = await prepared_stmt.fetch(*parameters)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 176, in fetch
    data = await self.__bind_execute(args, 0, timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 241, in __bind_execute
    data, status, _ = await self.__do_execute(
                      ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 230, in __do_execute
    return await executor(protocol)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "asyncpg\protocol\protocol.pyx", line 186, in bind_execute
  File "asyncpg\protocol\prepared_stmt.pyx", line 204, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
asyncpg.exceptions.DataError: invalid input for query argument $1: 'ch_4' (invalid UUID 'ch_4': length must be between 32..36 characters, got 4)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.Error: <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_4' (invalid UUID 'ch_4': length must be between 32..36 characters, got 4)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 387, in read_chapter_tool
    chapter = await chapter_service.get_chapter_by_id(chapter_id)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
    return meth(
           ^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1639, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2344, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_4' (invalid UUID 'ch_4': length must be between 32..36 characters, got 4)
[SQL: SELECT chapters.id, chapters.work_id, chapters.title, chapters.content, chapters.summary, chapters.status, chapters."order", chapters.is_published, chapters.word_count, chapters.view_count, chapters.created_at, chapters.updated_at, chapters.published_at
FROM chapters
WHERE chapters.id = $1::UUID]
[parameters: ('ch_4',)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
20:23:04 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] 读取章节失败: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_1' (invalid UUID 'ch_1': length must be between 32..36 characters, got 4)
[SQL: SELECT chapters.id, chapters.work_id, chapters.title, chapters.content, chapters.summary, chapters.status, chapters."order", chapters.is_published, chapters.word_count, chapters.view_count, chapters.created_at, chapters.updated_at, chapters.published_at
FROM chapters
WHERE chapters.id = $1::UUID]
[parameters: ('ch_1',)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
Traceback (most recent call last):
  File "asyncpg\protocol\prepared_stmt.pyx", line 175, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
  File "asyncpg\protocol\codecs/base.pyx", line 227, in asyncpg.protocol.protocol.Codec.encode
  File "asyncpg\protocol\codecs/base.pyx", line 129, in asyncpg.protocol.protocol.Codec.encode_scalar
  File "asyncpg\pgproto\./codecs/uuid.pyx", line 16, in asyncpg.pgproto.pgproto.uuid_encode
  File "asyncpg\pgproto\./uuid.pyx", line 88, in asyncpg.pgproto.pgproto.pg_uuid_bytes_from_str
ValueError: invalid UUID 'ch_1': length must be between 32..36 characters, got 4

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 546, in _prepare_and_execute
    self._rows = await prepared_stmt.fetch(*parameters)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 176, in fetch
    data = await self.__bind_execute(args, 0, timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 241, in __bind_execute
    data, status, _ = await self.__do_execute(
                      ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 230, in __do_execute
    return await executor(protocol)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "asyncpg\protocol\protocol.pyx", line 186, in bind_execute
  File "asyncpg\protocol\prepared_stmt.pyx", line 204, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
asyncpg.exceptions.DataError: invalid input for query argument $1: 'ch_1' (invalid UUID 'ch_1': length must be between 32..36 characters, got 4)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.Error: <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_1' (invalid UUID 'ch_1': length must be between 32..36 characters, got 4)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 387, in read_chapter_tool
    chapter = await chapter_service.get_chapter_by_id(chapter_id)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
    return meth(
           ^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1639, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2344, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_1' (invalid UUID 'ch_1': length must be between 32..36 characters, got 4)
[SQL: SELECT chapters.id, chapters.work_id, chapters.title, chapters.content, chapters.summary, chapters.status, chapters."order", chapters.is_published, chapters.word_count, chapters.view_count, chapters.created_at, chapters.updated_at, chapters.published_at
FROM chapters
WHERE chapters.id = $1::UUID]
[parameters: ('ch_1',)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
20:23:04 app.services.vector_store_service ERROR   RAG检索失败: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $3: 'YXTW_001' (invalid UUID 'YXTW_001': length must be between 32..36 characters, got 8)
[SQL: SELECT novel_analysis_vectors.id, novel_analysis_vectors.work_id, novel_analysis_vectors.chapter_id, novel_analysis_vectors.analysis_id, novel_analysis_vectors.user_id, novel_analysis_vectors.source_type, novel_analysis_vectors.source_id, novel_analysis_vectors.embedding, novel_analysis_vectors.content_text, novel_analysis_vectors.micro_data, novel_analysis_vectors.chunk_index, $1::INTEGER - (novel_analysis_vectors.embedding <=> $2) AS similarity
FROM novel_analysis_vectors
WHERE novel_analysis_vectors.work_id = $3::UUID ORDER BY novel_analysis_vectors.embedding <=> $4
 LIMIT $5::INTEGER]
[parameters: (1, '[-0.020042935386300087,-0.02332240901887417,-0.028026368468999863,0.036418940871953964,-0.02128913812339306,0.0029744270723313093,0.04579425603151321 ... (7747 characters truncated) ... 19,0.09471321851015091,-0.029775777831673622,-0.023853668943047523,0.052219707518815994,0.07330196350812912,-0.1055447906255722,-0.05414644628763199]', 'YXTW_001', '[-0.020042935386300087,-0.02332240901887417,-0.028026368468999863,0.036418940871953964,-0.02128913812339306,0.0029744270723313093,0.04579425603151321 ... (7747 characters truncated) ... 19,0.09471321851015091,-0.029775777831673622,-0.023853668943047523,0.052219707518815994,0.07330196350812912,-0.1055447906255722,-0.05414644628763199]', 5)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
Traceback (most recent call last):
  File "asyncpg\protocol\prepared_stmt.pyx", line 175, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
  File "asyncpg\protocol\codecs/base.pyx", line 227, in asyncpg.protocol.protocol.Codec.encode
  File "asyncpg\protocol\codecs/base.pyx", line 129, in asyncpg.protocol.protocol.Codec.encode_scalar
  File "asyncpg\pgproto\./codecs/uuid.pyx", line 16, in asyncpg.pgproto.pgproto.uuid_encode
  File "asyncpg\pgproto\./uuid.pyx", line 88, in asyncpg.pgproto.pgproto.pg_uuid_bytes_from_str
ValueError: invalid UUID 'YXTW_001': length must be between 32..36 characters, got 8

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 546, in _prepare_and_execute
    self._rows = await prepared_stmt.fetch(*parameters)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 176, in fetch
    data = await self.__bind_execute(args, 0, timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 241, in __bind_execute
    data, status, _ = await self.__do_execute(
                      ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 230, in __do_execute
    return await executor(protocol)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "asyncpg\protocol\protocol.pyx", line 186, in bind_execute
  File "asyncpg\protocol\prepared_stmt.pyx", line 204, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
asyncpg.exceptions.DataError: invalid input for query argument $3: 'YXTW_001' (invalid UUID 'YXTW_001': length must be between 32..36 characters, got 8)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.Error: <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $3: 'YXTW_001' (invalid UUID 'YXTW_001': length must be between 32..36 characters, got 8)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
    return meth(
           ^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1639, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2344, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $3: 'YXTW_001' (invalid UUID 'YXTW_001': length must be between 32..36 characters, got 8)
[SQL: SELECT novel_analysis_vectors.id, novel_analysis_vectors.work_id, novel_analysis_vectors.chapter_id, novel_analysis_vectors.analysis_id, novel_analysis_vectors.user_id, novel_analysis_vectors.source_type, novel_analysis_vectors.source_id, novel_analysis_vectors.embedding, novel_analysis_vectors.content_text, novel_analysis_vectors.micro_data, novel_analysis_vectors.chunk_index, $1::INTEGER - (novel_analysis_vectors.embedding <=> $2) AS similarity
FROM novel_analysis_vectors
WHERE novel_analysis_vectors.work_id = $3::UUID ORDER BY novel_analysis_vectors.embedding <=> $4
 LIMIT $5::INTEGER]
[parameters: (1, '[-0.020042935386300087,-0.02332240901887417,-0.028026368468999863,0.036418940871953964,-0.02128913812339306,0.0029744270723313093,0.04579425603151321 ... (7747 characters truncated) ... 19,0.09471321851015091,-0.029775777831673622,-0.023853668943047523,0.052219707518815994,0.07330196350812912,-0.1055447906255722,-0.05414644628763199]', 'YXTW_001', '[-0.020042935386300087,-0.02332240901887417,-0.028026368468999863,0.036418940871953964,-0.02128913812339306,0.0029744270723313093,0.04579425603151321 ... (7747 characters truncated) ... 19,0.09471321851015091,-0.029775777831673622,-0.023853668943047523,0.052219707518815994,0.07330196350812912,-0.1055447906255722,-0.05414644628763199]', 5)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
20:23:04 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] 读取章节失败: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_3' (invalid UUID 'ch_3': length must be between 32..36 characters, got 4)
[SQL: SELECT chapters.id, chapters.work_id, chapters.title, chapters.content, chapters.summary, chapters.status, chapters."order", chapters.is_published, chapters.word_count, chapters.view_count, chapters.created_at, chapters.updated_at, chapters.published_at
FROM chapters
WHERE chapters.id = $1::UUID]
[parameters: ('ch_3',)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
Traceback (most recent call last):
  File "asyncpg\protocol\prepared_stmt.pyx", line 175, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
  File "asyncpg\protocol\codecs/base.pyx", line 227, in asyncpg.protocol.protocol.Codec.encode
  File "asyncpg\protocol\codecs/base.pyx", line 129, in asyncpg.protocol.protocol.Codec.encode_scalar
  File "asyncpg\pgproto\./codecs/uuid.pyx", line 16, in asyncpg.pgproto.pgproto.uuid_encode
  File "asyncpg\pgproto\./uuid.pyx", line 88, in asyncpg.pgproto.pgproto.pg_uuid_bytes_from_str
ValueError: invalid UUID 'ch_3': length must be between 32..36 characters, got 4

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 546, in _prepare_and_execute
    self._rows = await prepared_stmt.fetch(*parameters)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 176, in fetch
    data = await self.__bind_execute(args, 0, timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 241, in __bind_execute
    data, status, _ = await self.__do_execute(
                      ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 230, in __do_execute
    return await executor(protocol)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "asyncpg\protocol\protocol.pyx", line 186, in bind_execute
  File "asyncpg\protocol\prepared_stmt.pyx", line 204, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
asyncpg.exceptions.DataError: invalid input for query argument $1: 'ch_3' (invalid UUID 'ch_3': length must be between 32..36 characters, got 4)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.Error: <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_3' (invalid UUID 'ch_3': length must be between 32..36 characters, got 4)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 387, in read_chapter_tool
    chapter = await chapter_service.get_chapter_by_id(chapter_id)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
    return meth(
           ^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1639, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2344, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 'ch_3' (invalid UUID 'ch_3': length must be between 32..36 characters, got 4)
[SQL: SELECT chapters.id, chapters.work_id, chapters.title, chapters.content, chapters.summary, chapters.status, chapters."order", chapters.is_published, chapters.word_count, chapters.view_count, chapters.created_at, chapters.updated_at, chapters.published_at
FROM chapters
WHERE chapters.id = $1::UUID]
[parameters: ('ch_3',)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
20:23:04 app.services.agent.langgraph_agent INFO   [LangGraph] 工具执行完毕，路由回: analysis_agent
20:23:04 app.services.agent.langgraph_agent INFO   [LangGraph] 处理分析请求（新架构）
20:23:04 Action.analysis INFO   [analysis] PromptManager已初始化
20:23:04 Action.analysis INFO   [analysis] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
20:23:04 app.services.agent.langgraph_agent INFO   [LangGraph] AnalysisAction准备完成: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
20:23:04 app.services.agent.langgraph_agent INFO   [LangGraph] 处理analysis场景 (use_chatgpt=True)
20:23:04 app.services.agent.langgraph_agent INFO   [LangGraph] analysis - 处理工具执行结果 (ChatOpenAI)
20:23:42 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
20:23:42 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=d2dff955-c9c7-43db-b067-80aa27b78e84, model=gemini-2.5-pro, duration=38.27s, tokens=3121 (prompt=529, completion=2592)
20:23:42 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
20:23:42 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共4个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.47it/s]
20:23:43 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=3838
20:23:43 app.services.context.store INFO   [ContextStore] 保存上下文: e7803789-de9d-4f64-ad8f-34713d465b11, token=5475
20:23:43 app.services.context.manager INFO   [ContextManager] 更新上下文: e7803789-de9d-4f64-ad8f-34713d465b11, 消息数=2, Token=5475
20:23:43 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: e7803789-de9d-4f64-ad8f-34713d465b11
20:23:43 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
