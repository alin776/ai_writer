INFO:     Finished server process [25424]
WARNING:  WatchFiles detected changes in 'app\services\agent\tools\style_learning.py', 'app\services\agent\utils\concurrent_memory_manager.py', 'app\services\agent\utils\monitoring.py', 'app\services\agent\utils\performance.py', 'app\services\agent\langgraph_agent.py', 'app\services\agent\utils\advanced_task_queue.py', 'app\services\agent\tools\hitl.py', 'app\services\agent\memory\memory_manager.py', 'app\services\ai\http_ai_service.py', 'app\services\agent\tools\tool_registry.py', 'app\services\review\book_review_analyzer.py', 'app\services\agent\actions\base_action.py', 'app\services\agent\utils\concurrent_tool_optimizer.py', 'app\services\agent\memory\import_export.py', 'app\services\credits\credit_service.py', 'app\services\agent\utils\business_metrics.py', 'app\services\export_service.py', 'app\services\agent\tools\consistency_checker.py', 'fix_datetime_now.py', 'app\utils\file_storage.py', 'app\services\agent\tools\tool_monitor.py', 'app\prompts\version_manager.py', 'app\services\ai\fast_ai_service.py', 'app\services\agent\actions\action_registry.py', 'app\services\credits\redeem_code_service.py', 'app\services\agent\utils\monitoring_dashboard.py', 'app\services\agent\environment\state_manager.py', 'app\services\agent\agents\planning_agent.py', 'app\services\agent\agents\parallel_executor.py', 'app\services\agent\memory\memory_strategy.py', 'app\services\agent\utils\monitoring_reports.py', 'app\services\agent\memory\version_control.py', 'app\services\agent\cost_tracker.py', 'app\services\agent\prompt_library.py', 'app\services\agent\memory\long_term_memory.py', 'app\services\agent\tools\tool_types.py', 'app\services\agent\utils\error_handler.py', 'app\services\agent\chat_stream_extension.py', 'app\services\agent\version_control.py', 'app\services\agent\utils\llm_optimizer.py', 'app\services\agent\memory\user_profile.py', 'app\services\agent\agents\reflection_agent.py'. Reloading...
Process SpawnProcess-49:
Traceback (most recent call last):
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\_subprocess.py", line 78, in subprocess_started
    target(sockets=sockets)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\server.py", line 62, in run
    return asyncio.run(self.serve(sockets=sockets))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 687, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\server.py", line 69, in serve
    config.load()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\config.py", line 458, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\importlib\__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "D:\Java\ai_writer\backend\app\main.py", line 12, in <module>
    from app.api import api_router
  File "D:\Java\ai_writer\backend\app\api\__init__.py", line 2, in <module>
    from app.api.v1 import auth, users, works, chapters, ai, worldview, novel_analysis, admin, search, relationships, timeline, groups, rewrite_history, humanize, review, ws, knowledge, agent, agent_react_stream, monitoring, credits, invitations, admin_credits
  File "D:\Java\ai_writer\backend\app\api\v1\agent.py", line 30, in <module>
    from app.services.agent.langgraph_agent import WritingAgentGraph
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 41
    from app.utils.datetime_utils import get_utc_now
    ^^^^
SyntaxError: invalid syntax
Process SpawnProcess-50:
Traceback (most recent call last):
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\_subprocess.py", line 78, in subprocess_started
    target(sockets=sockets)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\server.py", line 62, in run
    return asyncio.run(self.serve(sockets=sockets))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 687, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\server.py", line 69, in serve
    config.load()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\config.py", line 458, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\importlib\__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "D:\Java\ai_writer\backend\app\main.py", line 12, in <module>
    from app.api import api_router
  File "D:\Java\ai_writer\backend\app\api\__init__.py", line 2, in <module>
    from app.api.v1 import auth, users, works, chapters, ai, worldview, novel_analysis, admin, search, relationships, timeline, groups, rewrite_history, humanize, review, ws, knowledge, agent, agent_react_stream, monitoring, credits, invitations, admin_credits
  File "D:\Java\ai_writer\backend\app\api\v1\agent.py", line 30, in <module>
    from app.services.agent.langgraph_agent import WritingAgentGraph
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 41
    from app.utils.datetime_utils import get_utc_now
    ^^^^
SyntaxError: invalid syntax