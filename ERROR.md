(venv) PS D:\Java\ai_writer\backend> python quick_test_save.py

============================================================
快速验证：保存改写历史功能
============================================================

▶ 1. 登录...
✓ 登录成功

▶ 2. 保存改写历史...
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_transports\default.py", line 67, in map_httpcore_exceptions
    yield
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_transports\default.py", line 371, in handle_async_request
    resp = await self._pool.handle_async_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpcore\_async\connection_pool.py", line 256, in handle_async_request
    raise exc from None
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpcore\_async\connection_pool.py", line 236, in handle_async_request
    response = await connection.handle_async_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpcore\_async\http_proxy.py", line 206, in handle_async_request
    return await self._connection.handle_async_request(proxy_request)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpcore\_async\connection.py", line 103, in handle_async_request
    return await self._connection.handle_async_request(request)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpcore\_async\http11.py", line 136, in handle_async_request
    raise exc
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpcore\_async\http11.py", line 106, in handle_async_request
    ) = await self._receive_response_headers(**kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpcore\_async\http11.py", line 177, in _receive_response_headers
    event = await self._receive_event(timeout=timeout)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpcore\_async\http11.py", line 217, in _receive_event
    data = await self._network_stream.read(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpcore\_backends\anyio.py", line 32, in read
    with map_exceptions(exc_map):
  File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpcore\_exceptions.py", line 14, in map_exceptions
    raise to_exc(exc) from exc
httpcore.ReadTimeout

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\quick_test_save.py", line 97, in <module>
    asyncio.run(main())
  File "C:\Program Files\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 687, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\quick_test_save.py", line 86, in main
    success = await test_save_history()
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\quick_test_save.py", line 39, in test_save_history
    response = await client.post(
               ^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_client.py", line 1877, in post
    return await self.request(
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_client.py", line 1559, in request
    return await self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_client.py", line 1646, in send
    response = await self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_client.py", line 1674, in _send_handling_auth
    response = await self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_client.py", line 1711, in _send_handling_redirects
    response = await self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_client.py", line 1748, in _send_single_request
    response = await transport.handle_async_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_transports\default.py", line 370, in handle_async_request
    with map_httpcore_exceptions():
  File "C:\Program Files\Python312\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_transports\default.py", line 84, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ReadTimeout
(venv) PS D:\Java\ai_writer\backend>