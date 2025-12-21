@echo off
echo ======================================
echo    AI Writer - Stop Services
echo ======================================
echo.

echo Stopping Frontend Server...
taskkill /F /FI "WINDOWTITLE eq AI-Writer-Frontend*" 2>NUL
if "%ERRORLEVEL%"=="0" (
    echo Frontend stopped
) else (
    echo Frontend not running
)
echo.

echo Stopping Backend Server...
taskkill /F /FI "WINDOWTITLE eq AI-Writer-Backend*" 2>NUL
if "%ERRORLEVEL%"=="0" (
    echo Backend stopped
) else (
    echo Backend not running
)
echo.

echo ======================================
echo   All services stopped!
echo ======================================
echo.
pause
