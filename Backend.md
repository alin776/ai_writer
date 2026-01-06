INFO:     127.0.0.1:61690 - "POST /api/v1/relationships/ HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
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
  File "asyncpg\protocol\protocol.pyx", line 207, in bind_execute
asyncpg.exceptions.NotNullViolationError: null value in column "created_at" of relation "entity_relationships" violates not-null constraint
DETAIL:  失败, 行包含(5d8af651-24ce-4d6f-aaf6-f63d5ea79e63, 9be29f66-b4b2-4a3a-8b6b-0fe2efc096a1, b7dd607e-2eb8-473b-994c-82a55462da1d, character, dd32ccda-29e2-48ff-b42b-6c661706295b, character, 好友关系, 好友, 从小就好哥们，以后也是好哥们，属于男二的角..., 5, two-way, null, null, null, null, #450dc9, dashed, null, null, null, null).

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
sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.IntegrityError: <class 'asyncpg.exceptions.NotNullViolationError'>: null value in column "created_at" of relation "entity_relationships" violates not-null constraint
DETAIL:  失败, 行包含(5d8af651-24ce-4d6f-aaf6-f63d5ea79e63, 9be29f66-b4b2-4a3a-8b6b-0fe2efc096a1, b7dd607e-2eb8-473b-994c-82a55462da1d, character, dd32ccda-29e2-48ff-b42b-6c661706295b, character, 好友关系, 好友, 从小就好哥们，以后也是好哥们，属于男二的角..., 5, two-way, null, null, null, null, #450dc9, dashed, null, null, null, null).

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\http\httptools_impl.py", line 419, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 84, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\applications.py", line 123, in __call__
    await self.middleware_stack(scope, receive, send)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    raise exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    with collapse_excgroups():
  File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    raise exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    response = await self.dispatch_func(request, call_next)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\api\middleware\trace_middleware.py", line 48, in dispatch
    response = await call_next(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    raise app_exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    with collapse_excgroups():
  File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    raise exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    response = await self.dispatch_func(request, call_next)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\api\middleware\monitoring_middleware.py", line 68, in dispatch
    response = await call_next(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    raise app_exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 91, in __call__
    await self.simple_response(scope, receive, send, request_headers=headers)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 146, in simple_response
    await self.app(scope, receive, send)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\exceptions.py", line 62, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 64, in wrapped_app
    raise exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 762, in __call__
    await self.middleware_stack(scope, receive, send)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 782, in app
    await route.handle(scope, receive, send)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 297, in handle
    await self.app(scope, receive, send)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 77, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 64, in wrapped_app
    raise exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 72, in app
    response = await func(request)
               ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 299, in app
    raise e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 294, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 191, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\api\v1\relationships.py", line 61, in create_relationship
    await db.commit()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 1011, in commit
    await greenlet_spawn(self.sync_session.commit)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 202, in greenlet_spawn
    result = context.switch(value)
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1969, in commit
    trans.commit(_to_root=True)
  File "<string>", line 2, in commit
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1256, in commit
    self._prepare_impl()
  File "<string>", line 2, in _prepare_impl
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1231, in _prepare_impl
    self.session.flush()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4312, in flush
    self._flush(objects)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4447, in _flush
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4408, in _flush
    flush_context.execute()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 466, in execute
    rec.execute(self)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 642, in execute
    util.preloaded.orm_persistence.save_obj(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 93, in save_obj
    _emit_insert_statements(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 1227, in _emit_insert_statements
    result = connection.execute(
             ^^^^^^^^^^^^^^^^^^^
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
sqlalchemy.exc.IntegrityError: (sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.NotNullViolationError'>: null value in column "created_at" of relation "entity_relationships" violates not-null constraint
DETAIL:  失败, 行包含(5d8af651-24ce-4d6f-aaf6-f63d5ea79e63, 9be29f66-b4b2-4a3a-8b6b-0fe2efc096a1, b7dd607e-2eb8-473b-994c-82a55462da1d, character, dd32ccda-29e2-48ff-b42b-6c661706295b, character, 好友关系, 好友, 从小就好哥们，以后也是好哥们，属于男二的角..., 5, two-way, null, null, null, null, #450dc9, dashed, null, null, null, null).
[SQL: INSERT INTO entity_relationships (id, work_id, source_id, source_type, target_id, target_type, relationship_type, label, description, strength, direction, start_chapter_id, end_chapter_id, start_time, end_time, color, line_style, tags, category) VALUES ($1::UUID, $2::UUID, $3::UUID, $4::VARCHAR, $5::UUID, $6::VARCHAR, $7::VARCHAR, $8::VARCHAR, $9::VARCHAR, $10::INTEGER, $11::VARCHAR, $12::UUID, $13::UUID, $14::TIMESTAMP WITHOUT TIME ZONE, $15::TIMESTAMP WITHOUT TIME ZONE, $16::VARCHAR, $17::VARCHAR, $18::TEXT[], $19::VARCHAR) RETURNING entity_relationships.created_at, entity_relationships.updated_at]
[parameters: (UUID('5d8af651-24ce-4d6f-aaf6-f63d5ea79e63'), UUID('9be29f66-b4b2-4a3a-8b6b-0fe2efc096a1'), UUID('b7dd607e-2eb8-473b-994c-82a55462da1d'), 'character', UUID('dd32ccda-29e2-48ff-b42b-6c661706295b'), 'character', '好友关系', '好友', '从小就好哥们，以后也是好哥们，属于男二的角色', 5, 'two-way', None, None, None, None, '#450dc9', 'dashed', None, None)]
(Background on this error at: https://sqlalche.me/e/20/gkpj)