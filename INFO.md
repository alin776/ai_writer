22:37:45 app.api.v1.auth ERROR   Unexpected error: UnboundLocalError: cannot access local variable 'reward_amount' where it is not associated with a value
22:37:45 app.api.v1.auth ERROR   Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\api\v1\auth.py", line 138, in register
    reward_info = await invitation_service.activate_invitation(
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\invitations\invitation_service.py", line 404, in activate_invitation
    "reward_credits": float(reward_amount),
                            ^^^^^^^^^^^^^
UnboundLocalError: cannot access local variable 'reward_amount' where it is not associated with a value

22:37:45 app.api.middleware.monitoring_middleware ERROR   API请求失败: POST /api/v1/auth/register
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
  File "D:\Java\ai_writer\backend\app\api\v1\auth.py", line 138, in register
    reward_info = await invitation_service.activate_invitation(
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\invitations\invitation_service.py", line 404, in activate_invitation
    "reward_credits": float(reward_amount),
                            ^^^^^^^^^^^^^
UnboundLocalError: cannot access local variable 'reward_amount' where it is not associated with a value
22:37:45 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/register
22:37:45 app.main ERROR   Global exception handler caught: UnboundLocalError
22:37:45 app.main ERROR   Exception: cannot access local variable 'reward_amount' where it is not associated with a value
22:37:45 app.main ERROR   Traceback:   + Exception Group Traceback (most recent call last):
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
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 91, in __call__
    |     await self.simple_response(scope, receive, send, request_headers=headers)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 146, in simple_response
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
    |   File "D:\Java\ai_writer\backend\app\api\v1\auth.py", line 138, in register
    |     reward_info = await invitation_service.activate_invitation(
    |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\services\invitations\invitation_service.py", line 404, in activate_invitation
    |     "reward_credits": float(reward_amount),
    |                             ^^^^^^^^^^^^^
    | UnboundLocalError: cannot access local variable 'reward_amount' where it is not associated with a value
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
  File "D:\Java\ai_writer\backend\app\api\v1\auth.py", line 138, in register
    reward_info = await invitation_service.activate_invitation(
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\invitations\invitation_service.py", line 404, in activate_invitation
    "reward_credits": float(reward_amount),
                            ^^^^^^^^^^^^^
UnboundLocalError: cannot access local variable 'reward_amount' where it is not associated with a value

INFO:     127.0.0.1:58058 - "POST /api/v1/auth/register HTTP/1.1" 500 Internal Server Error
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
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 91, in __call__
    |     await self.simple_response(scope, receive, send, request_headers=headers)
    |   File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 146, in simple_response
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
    |   File "D:\Java\ai_writer\backend\app\api\v1\auth.py", line 138, in register
    |     reward_info = await invitation_service.activate_invitation(
    |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "D:\Java\ai_writer\backend\app\services\invitations\invitation_service.py", line 404, in activate_invitation
    |     "reward_credits": float(reward_amount),
    |                             ^^^^^^^^^^^^^
    | UnboundLocalError: cannot access local variable 'reward_amount' where it is not associated with a value
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
  File "D:\Java\ai_writer\backend\app\api\v1\auth.py", line 138, in register
    reward_info = await invitation_service.activate_invitation(
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\invitations\invitation_service.py", line 404, in activate_invitation
    "reward_credits": float(reward_amount),
                            ^^^^^^^^^^^^^
UnboundLocalError: cannot access local variable 'reward_amount' where it is not associated with a value