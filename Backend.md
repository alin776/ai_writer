INFO:     127.0.0.1:51413 - "GET /api/v1/channels/unread-summary HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
  + Exception Group Traceback (most recent call last):
  |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 85, in collapse_excgroups
  |     yield
  |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 190, in __call__
  |     async with anyio.create_task_group() as task_group:
  |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 781, in __aexit__
  |     raise BaseExceptionGroup(
  | ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
  +-+---------------- 1 ----------------
    | Traceback (most recent call last):
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\http\httptools_impl.py", line 419, in run_asgi
    |     result = await app(  # type: ignore[func-returns-value]
    |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 84, in __call__
    |     return await self.app(scope, receive, send)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\applications.py", line 1054, in __call__
    |     await super().__call__(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\applications.py", line 123, in __call__
    |     await self.middleware_stack(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    |     await self.app(scope, receive, _send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    |     with collapse_excgroups():
    |   File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    |     self.gen.throw(value)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    |     response = await self.dispatch_func(request, call_next)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\api\middleware\trace_middleware.py", line 48, in dispatch
    |     response = await call_next(request)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    |     raise app_exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    |     await self.app(scope, receive_or_disconnect, send_no_error)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    |     with collapse_excgroups():
    |   File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    |     self.gen.throw(value)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    |     response = await self.dispatch_func(request, call_next)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\api\middleware\monitoring_middleware.py", line 68, in dispatch
    |     response = await call_next(request)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    |     raise app_exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    |     await self.app(scope, receive_or_disconnect, send_no_error)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 83, in __call__
    |     await self.app(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\exceptions.py", line 62, in __call__
    |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 64, in wrapped_app
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    |     await app(scope, receive, sender)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 762, in __call__
    |     await self.middleware_stack(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 782, in app
    |     await route.handle(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 297, in handle
    |     await self.app(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 77, in app
    |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 64, in wrapped_app
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    |     await app(scope, receive, sender)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 72, in app
    |     response = await func(request)
    |                ^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 285, in app
    |     raise e
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 275, in app
    |     solved_result = await solve_dependencies(
    |                     ^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 570, in solve_dependencies
    |     solved_result = await solve_dependencies(
    |                     ^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 598, in solve_dependencies
    |     solved = await call(**sub_values)
    |              ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\core\security.py", line 135, in get_current_user
    |     user = await user_service.get_user_by_id(user_id)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\services\user_service.py", line 28, in get_user_by_id
    |     result = await self.db.execute(
    |              ^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    |     result = await greenlet_spawn(
    |              ^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 202, in greenlet_spawn
    |     result = context.switch(value)
    |              ^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    |     return self._execute_internal(
    |            ^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
    |     result: Result[Any] = compile_state_cls.orm_execute_statement(
    |                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
    |     result = conn.execute(
    |              ^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
    |     return meth(
    |            ^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
    |     return connection._execute_clauseelement(
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1631, in _execute_clauseelement
    |     compiled_sql, extracted_params, cache_hit = elem._compile_w_cache(
    |                                                 ^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 705, in _compile_w_cache
    |     compiled_sql = self._compiler(
    |                    ^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 317, in _compiler
    |     return dialect.statement_compiler(dialect, self, **kw)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 1427, in __init__
    |     Compiled.__init__(self, dialect, statement, **kwargs)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 867, in __init__
    |     self.string = self.process(self.statement, **compile_kwargs)
    |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 912, in process
    |     return obj._compiler_dispatch(self, **kwargs)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\visitors.py", line 143, in _compiler_dispatch
    |     return meth(self, **kw)  # type: ignore  # noqa: E501
    |            ^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 4609, in visit_select
    |     compile_state = select_stmt._compile_state_factory(
    |                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\base.py", line 687, in create_for_statement
    |     return klass.create_for_statement(statement, compiler, **kw)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 1091, in create_for_statement
    |     _QueryEntity.to_compile_state(
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2537, in to_compile_state
    |     _MapperEntity(
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2617, in __init__
    |     entity._post_inspect
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 1260, in __get__
    |     obj.__dict__[self.__name__] = result = self.fget(obj)
    |                                            ^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2707, in _post_inspect
    |     self._check_configure()
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2386, in _check_configure
    |     _configure_registries({self.registry}, cascade=True)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4199, in _configure_registries
    |     _do_configure_registries(registries, cascade)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4236, in _do_configure_registries
    |     raise e
    | sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[User(users)]'. Original exception was: Could not determine join condition between parent/child tables on relationship User.channel_messages - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.
    +------------------------------------

During handling of the above exception, another exception occurred:

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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 83, in __call__
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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 285, in app
    raise e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 275, in app
    solved_result = await solve_dependencies(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 570, in solve_dependencies
    solved_result = await solve_dependencies(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 598, in solve_dependencies
    solved = await call(**sub_values)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\core\security.py", line 135, in get_current_user
    user = await user_service.get_user_by_id(user_id)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\user_service.py", line 28, in get_user_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 202, in greenlet_spawn
    result = context.switch(value)
             ^^^^^^^^^^^^^^^^^^^^^
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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1631, in _execute_clauseelement
    compiled_sql, extracted_params, cache_hit = elem._compile_w_cache(
                                                ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 705, in _compile_w_cache
    compiled_sql = self._compiler(
                   ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 317, in _compiler
    return dialect.statement_compiler(dialect, self, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 1427, in __init__
    Compiled.__init__(self, dialect, statement, **kwargs)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 867, in __init__
    self.string = self.process(self.statement, **compile_kwargs)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 912, in process
    return obj._compiler_dispatch(self, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\visitors.py", line 143, in _compiler_dispatch
    return meth(self, **kw)  # type: ignore  # noqa: E501
           ^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 4609, in visit_select
    compile_state = select_stmt._compile_state_factory(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\base.py", line 687, in create_for_statement
    return klass.create_for_statement(statement, compiler, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 1091, in create_for_statement
    _QueryEntity.to_compile_state(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2537, in to_compile_state
    _MapperEntity(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2617, in __init__
    entity._post_inspect
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 1260, in __get__
    obj.__dict__[self.__name__] = result = self.fget(obj)
                                           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2707, in _post_inspect
    self._check_configure()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2386, in _check_configure
    _configure_registries({self.registry}, cascade=True)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4199, in _configure_registries
    _do_configure_registries(registries, cascade)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4236, in _do_configure_registries
    raise e
sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[User(users)]'. Original exception was: Could not determine join condition between parent/child tables on relationship User.channel_messages - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.
2025-12-30 19:40:04,156 - app.api.middleware.monitoring_middleware - ERROR - API请求失败: GET /api/v1/channels/unread-summary
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 159, in call_next
    message = await recv_stream.receive()
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\anyio\streams\memory.py", line 126, in receive
    raise EndOfStream from None
anyio.EndOfStream

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\api\middleware\monitoring_middleware.py", line 68, in dispatch
    response = await call_next(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    raise app_exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 83, in __call__
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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 285, in app
    raise e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 275, in app
    solved_result = await solve_dependencies(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 570, in solve_dependencies
    solved_result = await solve_dependencies(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 598, in solve_dependencies
    solved = await call(**sub_values)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\core\security.py", line 135, in get_current_user
    user = await user_service.get_user_by_id(user_id)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\user_service.py", line 28, in get_user_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 202, in greenlet_spawn
    result = context.switch(value)
             ^^^^^^^^^^^^^^^^^^^^^
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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1631, in _execute_clauseelement
    compiled_sql, extracted_params, cache_hit = elem._compile_w_cache(
                                                ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 705, in _compile_w_cache
    compiled_sql = self._compiler(
                   ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 317, in _compiler
    return dialect.statement_compiler(dialect, self, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 1427, in __init__
    Compiled.__init__(self, dialect, statement, **kwargs)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 867, in __init__
    self.string = self.process(self.statement, **compile_kwargs)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 912, in process
    return obj._compiler_dispatch(self, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\visitors.py", line 143, in _compiler_dispatch
    return meth(self, **kw)  # type: ignore  # noqa: E501
           ^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 4609, in visit_select
    compile_state = select_stmt._compile_state_factory(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\base.py", line 687, in create_for_statement
    return klass.create_for_statement(statement, compiler, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 1091, in create_for_statement
    _QueryEntity.to_compile_state(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2537, in to_compile_state
    _MapperEntity(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2617, in __init__
    entity._post_inspect
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 1260, in __get__
    obj.__dict__[self.__name__] = result = self.fget(obj)
                                           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2707, in _post_inspect
    self._check_configure()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2386, in _check_configure
    _configure_registries({self.registry}, cascade=True)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4199, in _configure_registries
    _do_configure_registries(registries, cascade)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4236, in _do_configure_registries
    raise e
sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[User(users)]'. Original exception was: Could not determine join condition between parent/child tables on relationship User.channel_messages - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.
2025-12-30 19:40:04,161 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
2025-12-30 19:40:04,161 - app.main - ERROR - Global exception handler caught: InvalidRequestError
2025-12-30 19:40:04,161 - app.main - ERROR - Exception: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[User(users)]'. Original exception was: Could not determine join condition between parent/child tables on relationship User.channel_messages - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.
2025-12-30 19:40:04,166 - app.main - ERROR - Traceback:   + Exception Group Traceback (most recent call last):
  |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 85, in collapse_excgroups
  |     yield
  |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 190, in __call__
  |     async with anyio.create_task_group() as task_group:
  |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 781, in __aexit__
  |     raise BaseExceptionGroup(
  | ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
  +-+---------------- 1 ----------------
    | Traceback (most recent call last):
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    |     await self.app(scope, receive, _send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    |     with collapse_excgroups():
    |   File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    |     self.gen.throw(value)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    |     response = await self.dispatch_func(request, call_next)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\api\middleware\trace_middleware.py", line 48, in dispatch
    |     response = await call_next(request)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    |     raise app_exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    |     await self.app(scope, receive_or_disconnect, send_no_error)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    |     with collapse_excgroups():
    |   File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    |     self.gen.throw(value)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    |     response = await self.dispatch_func(request, call_next)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\api\middleware\monitoring_middleware.py", line 68, in dispatch
    |     response = await call_next(request)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    |     raise app_exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    |     await self.app(scope, receive_or_disconnect, send_no_error)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 83, in __call__
    |     await self.app(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\exceptions.py", line 62, in __call__
    |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 64, in wrapped_app
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    |     await app(scope, receive, sender)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 762, in __call__
    |     await self.middleware_stack(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 782, in app
    |     await route.handle(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 297, in handle
    |     await self.app(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 77, in app
    |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 64, in wrapped_app
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    |     await app(scope, receive, sender)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 72, in app
    |     response = await func(request)
    |                ^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 285, in app
    |     raise e
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 275, in app
    |     solved_result = await solve_dependencies(
    |                     ^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 570, in solve_dependencies
    |     solved_result = await solve_dependencies(
    |                     ^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 598, in solve_dependencies
    |     solved = await call(**sub_values)
    |              ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\core\security.py", line 135, in get_current_user
    |     user = await user_service.get_user_by_id(user_id)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\services\user_service.py", line 28, in get_user_by_id
    |     result = await self.db.execute(
    |              ^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    |     result = await greenlet_spawn(
    |              ^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 202, in greenlet_spawn
    |     result = context.switch(value)
    |              ^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    |     return self._execute_internal(
    |            ^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
    |     result: Result[Any] = compile_state_cls.orm_execute_statement(
    |                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
    |     result = conn.execute(
    |              ^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
    |     return meth(
    |            ^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
    |     return connection._execute_clauseelement(
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1631, in _execute_clauseelement
    |     compiled_sql, extracted_params, cache_hit = elem._compile_w_cache(
    |                                                 ^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 705, in _compile_w_cache
    |     compiled_sql = self._compiler(
    |                    ^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 317, in _compiler
    |     return dialect.statement_compiler(dialect, self, **kw)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 1427, in __init__
    |     Compiled.__init__(self, dialect, statement, **kwargs)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 867, in __init__
    |     self.string = self.process(self.statement, **compile_kwargs)
    |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 912, in process
    |     return obj._compiler_dispatch(self, **kwargs)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\visitors.py", line 143, in _compiler_dispatch
    |     return meth(self, **kw)  # type: ignore  # noqa: E501
    |            ^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 4609, in visit_select
    |     compile_state = select_stmt._compile_state_factory(
    |                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\base.py", line 687, in create_for_statement
    |     return klass.create_for_statement(statement, compiler, **kw)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 1091, in create_for_statement
    |     _QueryEntity.to_compile_state(
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2537, in to_compile_state
    |     _MapperEntity(
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2617, in __init__
    |     entity._post_inspect
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 1260, in __get__
    |     obj.__dict__[self.__name__] = result = self.fget(obj)
    |                                            ^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2707, in _post_inspect
    |     self._check_configure()
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2386, in _check_configure
    |     _configure_registries({self.registry}, cascade=True)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4199, in _configure_registries
    |     _do_configure_registries(registries, cascade)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4236, in _do_configure_registries
    |     raise e
    | sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[User(users)]'. Original exception was: Could not determine join condition between parent/child tables on relationship User.channel_messages - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.
    +------------------------------------

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 83, in __call__
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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 285, in app
    raise e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 275, in app
    solved_result = await solve_dependencies(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 570, in solve_dependencies
    solved_result = await solve_dependencies(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 598, in solve_dependencies
    solved = await call(**sub_values)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\core\security.py", line 135, in get_current_user
    user = await user_service.get_user_by_id(user_id)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\user_service.py", line 28, in get_user_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 202, in greenlet_spawn
    result = context.switch(value)
             ^^^^^^^^^^^^^^^^^^^^^
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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1631, in _execute_clauseelement
    compiled_sql, extracted_params, cache_hit = elem._compile_w_cache(
                                                ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 705, in _compile_w_cache
    compiled_sql = self._compiler(
                   ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 317, in _compiler
    return dialect.statement_compiler(dialect, self, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 1427, in __init__
    Compiled.__init__(self, dialect, statement, **kwargs)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 867, in __init__
    self.string = self.process(self.statement, **compile_kwargs)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 912, in process
    return obj._compiler_dispatch(self, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\visitors.py", line 143, in _compiler_dispatch
    return meth(self, **kw)  # type: ignore  # noqa: E501
           ^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 4609, in visit_select
    compile_state = select_stmt._compile_state_factory(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\base.py", line 687, in create_for_statement
    return klass.create_for_statement(statement, compiler, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 1091, in create_for_statement
    _QueryEntity.to_compile_state(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2537, in to_compile_state
    _MapperEntity(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2617, in __init__
    entity._post_inspect
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 1260, in __get__
    obj.__dict__[self.__name__] = result = self.fget(obj)
                                           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2707, in _post_inspect
    self._check_configure()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2386, in _check_configure
    _configure_registries({self.registry}, cascade=True)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4199, in _configure_registries
    _do_configure_registries(registries, cascade)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4236, in _do_configure_registries
    raise e
sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[User(users)]'. Original exception was: Could not determine join condition between parent/child tables on relationship User.channel_messages - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.

INFO:     127.0.0.1:58988 - "GET /api/v1/channels/unread-summary HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
  + Exception Group Traceback (most recent call last):
  |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 85, in collapse_excgroups
  |     yield
  |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 190, in __call__
  |     async with anyio.create_task_group() as task_group:
  |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 781, in __aexit__
  |     raise BaseExceptionGroup(
  | ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
  +-+---------------- 1 ----------------
    | Traceback (most recent call last):
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\http\httptools_impl.py", line 419, in run_asgi
    |     result = await app(  # type: ignore[func-returns-value]
    |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 84, in __call__
    |     return await self.app(scope, receive, send)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\applications.py", line 1054, in __call__
    |     await super().__call__(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\applications.py", line 123, in __call__
    |     await self.middleware_stack(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    |     await self.app(scope, receive, _send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    |     with collapse_excgroups():
    |   File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    |     self.gen.throw(value)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    |     response = await self.dispatch_func(request, call_next)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\api\middleware\trace_middleware.py", line 48, in dispatch
    |     response = await call_next(request)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    |     raise app_exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    |     await self.app(scope, receive_or_disconnect, send_no_error)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    |     with collapse_excgroups():
    |   File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    |     self.gen.throw(value)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    |     response = await self.dispatch_func(request, call_next)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\api\middleware\monitoring_middleware.py", line 68, in dispatch
    |     response = await call_next(request)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    |     raise app_exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    |     await self.app(scope, receive_or_disconnect, send_no_error)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 83, in __call__
    |     await self.app(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\exceptions.py", line 62, in __call__
    |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 64, in wrapped_app
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    |     await app(scope, receive, sender)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 762, in __call__
    |     await self.middleware_stack(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 782, in app
    |     await route.handle(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 297, in handle
    |     await self.app(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 77, in app
    |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 64, in wrapped_app
    |     raise exc
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    |     await app(scope, receive, sender)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\routing.py", line 72, in app
    |     response = await func(request)
    |                ^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 285, in app
    |     raise e
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 275, in app
    |     solved_result = await solve_dependencies(
    |                     ^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 570, in solve_dependencies
    |     solved_result = await solve_dependencies(
    |                     ^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 598, in solve_dependencies
    |     solved = await call(**sub_values)
    |              ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\core\security.py", line 135, in get_current_user
    |     user = await user_service.get_user_by_id(user_id)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\services\user_service.py", line 28, in get_user_by_id
    |     result = await self.db.execute(
    |              ^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    |     result = await greenlet_spawn(
    |              ^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 202, in greenlet_spawn
    |     result = context.switch(value)
    |              ^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    |     return self._execute_internal(
    |            ^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
    |     result: Result[Any] = compile_state_cls.orm_execute_statement(
    |                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
    |     result = conn.execute(
    |              ^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
    |     return meth(
    |            ^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
    |     return connection._execute_clauseelement(
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1631, in _execute_clauseelement
    |     compiled_sql, extracted_params, cache_hit = elem._compile_w_cache(
    |                                                 ^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 705, in _compile_w_cache
    |     compiled_sql = self._compiler(
    |                    ^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 317, in _compiler
    |     return dialect.statement_compiler(dialect, self, **kw)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 1427, in __init__
    |     Compiled.__init__(self, dialect, statement, **kwargs)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 867, in __init__
    |     self.string = self.process(self.statement, **compile_kwargs)
    |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 912, in process
    |     return obj._compiler_dispatch(self, **kwargs)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\visitors.py", line 143, in _compiler_dispatch
    |     return meth(self, **kw)  # type: ignore  # noqa: E501
    |            ^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 4609, in visit_select
    |     compile_state = select_stmt._compile_state_factory(
    |                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\base.py", line 687, in create_for_statement
    |     return klass.create_for_statement(statement, compiler, **kw)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 1091, in create_for_statement
    |     _QueryEntity.to_compile_state(
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2537, in to_compile_state
    |     _MapperEntity(
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2617, in __init__
    |     entity._post_inspect
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 1260, in __get__
    |     obj.__dict__[self.__name__] = result = self.fget(obj)
    |                                            ^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2707, in _post_inspect
    |     self._check_configure()
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2386, in _check_configure
    |     _configure_registries({self.registry}, cascade=True)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4199, in _configure_registries
    |     _do_configure_registries(registries, cascade)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4236, in _do_configure_registries
    |     raise e
    | sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[User(users)]'. Original exception was: Could not determine join condition between parent/child tables on relationship User.channel_messages - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.
    +------------------------------------

During handling of the above exception, another exception occurred:

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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 83, in __call__
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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 285, in app
    raise e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 275, in app
    solved_result = await solve_dependencies(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 570, in solve_dependencies
    solved_result = await solve_dependencies(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\dependencies\utils.py", line 598, in solve_dependencies
    solved = await call(**sub_values)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\core\security.py", line 135, in get_current_user
    user = await user_service.get_user_by_id(user_id)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\user_service.py", line 28, in get_user_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 202, in greenlet_spawn
    result = context.switch(value)
             ^^^^^^^^^^^^^^^^^^^^^
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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1631, in _execute_clauseelement
    compiled_sql, extracted_params, cache_hit = elem._compile_w_cache(
                                                ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 705, in _compile_w_cache
    compiled_sql = self._compiler(
                   ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 317, in _compiler
    return dialect.statement_compiler(dialect, self, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 1427, in __init__
    Compiled.__init__(self, dialect, statement, **kwargs)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 867, in __init__
    self.string = self.process(self.statement, **compile_kwargs)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 912, in process
    return obj._compiler_dispatch(self, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\visitors.py", line 143, in _compiler_dispatch
    return meth(self, **kw)  # type: ignore  # noqa: E501
           ^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\compiler.py", line 4609, in visit_select
    compile_state = select_stmt._compile_state_factory(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\base.py", line 687, in create_for_statement
    return klass.create_for_statement(statement, compiler, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 1091, in create_for_statement
    _QueryEntity.to_compile_state(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2537, in to_compile_state
    _MapperEntity(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 2617, in __init__
    entity._post_inspect
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 1260, in __get__
    obj.__dict__[self.__name__] = result = self.fget(obj)
                                           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2707, in _post_inspect
    self._check_configure()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 2386, in _check_configure
    _configure_registries({self.registry}, cascade=True)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4199, in _configure_registries
    _do_configure_registries(registries, cascade)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 4236, in _do_configure_registries
    raise e
sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[User(users)]'. Original exception was: Could not determine join condition between parent/child tables on relationship User.channel_messages - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.