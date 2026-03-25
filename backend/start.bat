@echo off
chcp 65001 >nul
cd /d D:\Java\ai_writer\backend
call venv\Scripts\activate.bat
set PYTHONUNBUFFERED=1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
