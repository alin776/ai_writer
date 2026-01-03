INFO:     127.0.0.1:49957 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/messages/around/a1b34164-a44e-4269-8f7f-e90b5aa8e83c?params%5Blimit%5D=50 HTTP/1.1" 500 Internal Server Error
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
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 299, in app
    |     raise e
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 294, in app
    |     raw_response = await run_endpoint_function(
    |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 191, in run_endpoint_function
    |     return await dependant.call(**values)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\api\v1\channels.py", line 1461, in get_messages_around
    |     message_type=msg.message_type,
    |                  ^^^^^^^^^^^^^^^^
    | AttributeError: 'ChannelMessage' object has no attribute 'message_type'
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
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 299, in app
    raise e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 294, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\fastapi\routing.py", line 191, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\api\v1\channels.py", line 1461, in get_messages_around
    message_type=msg.message_type,
                 ^^^^^^^^^^^^^^^^
AttributeError: 'ChannelMessage' object has no attribute 'message_type'