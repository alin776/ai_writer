@echo off
chcp 65001 >nul
echo ============================================
echo   Compiling pgvector for PostgreSQL 15
echo ============================================
echo.

REM Set VS Build Tools path
set "VSPATH=D:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools"

REM Initialize VS environment
echo Initializing Visual Studio environment...
call "%VSPATH%\VC\Auxiliary\Build\vcvars64.bat"

if errorlevel 1 (
    echo ERROR: Failed to initialize VS environment
    pause
    exit /b 1
)

echo.
echo VS Environment initialized successfully
echo.

REM Set PostgreSQL root
set "PGROOT=C:\Program Files\PostgreSQL\15"

echo PostgreSQL path: %PGROOT%
echo.

REM Navigate to pgvector source
cd /d %TEMP%\pgvector

if errorlevel 1 (
    echo ERROR: pgvector source not found in %TEMP%\pgvector
    pause
    exit /b 1
)

echo Current directory: %CD%
echo.

REM Compile
echo ============================================
echo Compiling pgvector...
echo ============================================
nmake /F Makefile.win

if errorlevel 1 (
    echo.
    echo ERROR: Compilation failed
    pause
    exit /b 1
)

echo.
echo Compilation successful!
echo.

REM Install
echo ============================================
echo Installing pgvector...
echo ============================================
nmake /F Makefile.win install

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed
    pause
    exit /b 1
)

echo.
echo ============================================
echo SUCCESS! pgvector installed successfully
echo ============================================
echo.
echo Next steps:
echo 1. Restart PostgreSQL service
echo 2. Connect to database
echo 3. Run: CREATE EXTENSION vector;
echo.
pause
