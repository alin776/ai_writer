@echo off
REM 启动服务快捷方式 - 从根目录调用
cd /d "%~dp0一键部署"
call "start-services.bat"
