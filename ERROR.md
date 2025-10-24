PS C:\Users\姚东名> cd D:\Java\ai_writer\backend
PS D:\Java\ai_writer\backend> alembic upgrade head
alembic : 无法将“alembic”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请
确保路径正确，然后再试一次。
所在位置 行:1 字符: 1
+ alembic upgrade head
+ ~~~~~~~
    + CategoryInfo          : ObjectNotFound: (alembic:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException

PS D:\Java\ai_writer\backend> .\venv\Scripts\python.exe -m uvicorn app.main:app --reload
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [25640] using WatchFiles
Process SpawnProcess-1:
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
    from app.api.v1 import auth, users, works, chapters, ai, worldview, novel_analysis, admin, search, relationships, timeline, groups
  File "D:\Java\ai_writer\backend\app\api\v1\auth.py", line 10, in <module>
    from app.schemas.user import UserCreate, UserResponse, Token, AuthResponse
  File "D:\Java\ai_writer\backend\app\schemas\__init__.py", line 9, in <module>
    from app.schemas.work import (
  File "D:\Java\ai_writer\backend\app\schemas\work.py", line 5, in <module>
    from app.models.work import WorkStatus, WorkGenre
  File "D:\Java\ai_writer\backend\app\models\__init__.py", line 15, in <module>
    from app.models.ai_call_log import AICallLog
  File "D:\Java\ai_writer\backend\app\models\ai_call_log.py", line 16, in <module>
    class AICallLog(Base):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\decl_api.py", line 196, in __init__
    _as_declarative(reg, cls, dict_)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 247, in _as_declarative
    return _MapperConfig.setup_mapping(registry, cls, dict_, None, {})
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 328, in setup_mapping
    return _ClassScanMapperConfig(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 574, in __init__
    self._extract_mappable_attributes()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 1507, in _extract_mappable_attributes
    raise exc.InvalidRequestError(
sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved when using the Declarative API.
