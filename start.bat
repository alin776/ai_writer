@echo off
echo ======================================
echo    AI Writer - Start Services
echo ======================================
echo.

echo [1/2] Starting Backend Server...
cd /d "%~dp0backend"
start "AI-Writer-Backend" cmd /k "venv\Scripts\activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo Backend started at http://localhost:8000
echo.

timeout /t 2 /nobreak >nul

echo [2/2] Starting Frontend Server...
cd /d "%~dp0"
start "AI-Writer-Frontend" cmd /k "npm run dev"
echo Frontend started at http://localhost:5173
echo.

echo ======================================
echo   All services started!
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/docs
echo ======================================
echo.
echo Press any key to close this window...
pause >nul
