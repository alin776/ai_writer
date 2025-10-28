(venv) PS D:\Java\ai_writer\backend> python test_book_cache.py

启动测试...
测试时间: 2025-10-28 15:25:56

############################################################
#  AI拆书Redis缓存功能测试
############################################################


============================================================
步骤 1: 用户登录
============================================================

用户名: 2072855200@qq.com
✅ 登录成功!
   Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2M...

============================================================
步骤 2: 首次分析 - 缓存未命中
============================================================

ℹ️  测试文件: test_cache_v1_1761636359.txt
ℹ️  ⏳ 正在上传并分析 (首次,应该调用AI)...
ℹ️  任务ID: 015e9e24-274b-4118-9a79-013f9f6cbfcc
✅ 首次分析完成! 耗时: 62.09秒
ℹ️  分析章节: 0
ℹ️  提取知识: 0

============================================================
步骤 3: 重复分析 - 缓存命中测试
============================================================

ℹ️  测试文件: test_cache_v1_1761636359.txt
ℹ️  ⏳ 正在上传并分析 (相同内容,应该命中缓存)...
ℹ️  任务ID: 807dd020-a35e-479c-b33b-a2324f7a2718
✅ 第二次分析完成! 耗时: 33.21秒
ℹ️  分析章节: 0

============================================================
步骤 4: 性能对比分析
============================================================

📊 首次分析 (缓存未命中): 62.09秒
📊 重复分析 (缓存命中):   33.21秒
⚡ 性能提升: 1.9x
⏱️  节省时间: 28.89秒

❌ ❌ 缓存未生效! 两次耗时相近

============================================================
步骤 5: 不同内容测试 - 验证缓存键隔离
============================================================

ℹ️  测试文件: test_cache_v2_1761636458.txt
ℹ️  ⏳ 正在分析不同内容 (应该重新调用AI)...
ℹ️  任务ID: f4a6520c-f6df-4f1b-a75a-da9c7f47bdd7

测试失败:
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
httpcore.ReadError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\test_book_cache.py", line 403, in main
    await runner.run_cache_test()
  File "D:\Java\ai_writer\backend\test_book_cache.py", line 362, in run_cache_test
    result3 = await self.upload_and_analyze(client, test_file3)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\test_book_cache.py", line 222, in upload_and_analyze
    status_resp = await client.get(
                  ^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\httpx\_client.py", line 1786, in get
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
httpx.ReadError
(venv) PS D:\Java\ai_writer\backend>