@echo off
REM 停止服务快捷方式 - 从根目录调用
cd /d "%~dp0一键部署"
call "stop-services.bat"
