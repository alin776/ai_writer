2026-01-19 00:43:29,459 - app.main - ERROR - Global exception handler caught: InterfaceError
2026-01-19 00:43:29,460 - app.main - ERROR - Exception: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot call Transaction.rollback(): the underlying connection is closed
(Background on this error at: https://sqlalche.me/e/20/rvf5)
2026-01-19 00:43:31,045 - app.main - ERROR - Traceback: Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 863, in rollback
    self.await_(self._transaction.rollback())
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connresource.py", line 19, in _check
    self._check_conn_validity(meth.__name__)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connresource.py", line 41, in _check_conn_validity
    raise exceptions.InterfaceError(
asyncpg.exceptions._base.InterfaceError: cannot call Transaction.rollback(): the underlying connection is closed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1119, in _rollback_impl
    self.engine.dialect.do_rollback(self.connection)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 692, in do_rollback
    dbapi_connection.rollback()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 865, in rollback
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot call Transaction.rollback(): the underlying connection is closed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    with collapse_excgroups():
  File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    raise exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\responses.py", line 257, in wrap
    await func()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 217, in stream_response
    return await super().stream_response(send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\responses.py", line 246, in stream_response
    async for chunk in self.body_iterator:
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 181, in body_stream
    raise app_exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    with collapse_excgroups():
  File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    raise exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\responses.py", line 257, in wrap
    await func()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\responses.py", line 246, in stream_response
    async for chunk in self.body_iterator:
  File "D:\Java\ai_writer\backend\app\api\v1\agent.py", line 1012, in event_generator
    async with create_db_session() as db:
  File "C:\Program Files\Python312\Lib\contextlib.py", line 217, in __aexit__
    await anext(self.gen)
  File "D:\Java\ai_writer\backend\app\core\database.py", line 90, in create_db_session
    await session.close()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 1027, in close
    await greenlet_spawn(self.sync_session.close)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 202, in greenlet_spawn
    result = context.switch(value)
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2468, in close
    self._close_impl(invalidate=False)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2537, in _close_impl
    transaction.close(invalidate)
  File "<string>", line 2, in close
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1362, in close
    transaction.close()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2577, in close
    self._do_close()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2715, in _do_close
    self._close_impl()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2701, in _close_impl
    self._connection_rollback_impl()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2693, in _connection_rollback_impl
    self.connection._rollback_impl()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1121, in _rollback_impl
    self._handle_dbapi_exception(e, None, None, None, None)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2344, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1119, in _rollback_impl
    self.engine.dialect.do_rollback(self.connection)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 692, in do_rollback
    dbapi_connection.rollback()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 865, in rollback
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot call Transaction.rollback(): the underlying connection is closed
(Background on this error at: https://sqlalche.me/e/20/rvf5)

ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 863, in rollback
    self.await_(self._transaction.rollback())
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connresource.py", line 19, in _check
    self._check_conn_validity(meth.__name__)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connresource.py", line 41, in _check_conn_validity
    raise exceptions.InterfaceError(
asyncpg.exceptions._base.InterfaceError: cannot call Transaction.rollback(): the underlying connection is closed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1119, in _rollback_impl
    self.engine.dialect.do_rollback(self.connection)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 692, in do_rollback
    dbapi_connection.rollback()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 865, in rollback
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot call Transaction.rollback(): the underlying connection is closed

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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\responses.py", line 257, in wrap
    await func()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 217, in stream_response
    return await super().stream_response(send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\responses.py", line 246, in stream_response
    async for chunk in self.body_iterator:
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 181, in body_stream
    raise app_exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    with collapse_excgroups():
  File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    raise exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\responses.py", line 257, in wrap
    await func()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\responses.py", line 246, in stream_response
    async for chunk in self.body_iterator:
  File "D:\Java\ai_writer\backend\app\api\v1\agent.py", line 1012, in event_generator
    async with create_db_session() as db:
  File "C:\Program Files\Python312\Lib\contextlib.py", line 217, in __aexit__
    await anext(self.gen)
  File "D:\Java\ai_writer\backend\app\core\database.py", line 90, in create_db_session
    await session.close()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 1027, in close
    await greenlet_spawn(self.sync_session.close)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 202, in greenlet_spawn
    result = context.switch(value)
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2468, in close
    self._close_impl(invalidate=False)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2537, in _close_impl
    transaction.close(invalidate)
  File "<string>", line 2, in close
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1362, in close
    transaction.close()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2577, in close
    self._do_close()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2715, in _do_close
    self._close_impl()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2701, in _close_impl
    self._connection_rollback_impl()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2693, in _connection_rollback_impl
    self.connection._rollback_impl()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1121, in _rollback_impl
    self._handle_dbapi_exception(e, None, None, None, None)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2344, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1119, in _rollback_impl
    self.engine.dialect.do_rollback(self.connection)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 692, in do_rollback
    dbapi_connection.rollback()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 865, in rollback
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot call Transaction.rollback(): the underlying connection is closed
(Background on this error at: https://sqlalche.me/e/20/rvf5)
2026-01-19 00:43:53,589 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/0164eaf3-eba3-4897-bbc7-ef4dce7567e0