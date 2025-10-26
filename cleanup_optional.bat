@echo off
chcp 65001 > nul
echo ============================================================
echo 可选文件清理脚本 - 历史文档
echo ============================================================
echo.
echo 此脚本将删除【小说分析系统】相关的历史文档：
echo.
echo [项目根目录 - 小说分析系统历史文档]
echo   - AI辅助写小说的几个角度.md
echo   - 测试和加固计划.md
echo   - 前端查看分析结果指南.md
echo   - 如何运行压力测试.md
echo   - 世界观图终极升级工程文档.md
echo   - 项目交接文档-小说分析系统.md
echo   - 小说创作提示词.md
echo   - 小说分析系统设计规范.md
echo   - 小说分析系统实施进度.md
echo   - 小说分析系统完成报告.md
echo   - 小说分析性能优化完成报告.md
echo   - 新增依赖清单.md
echo.
echo [项目根目录 - 可能过时的文档]
echo   - NovelAIde 项目架构图.md
echo   - NovelAIde 项目文档 v2.12.md (旧版本)
echo.
echo ⚠️  警告：这些可能是历史记录，删除前请确认不再需要！
echo.
echo ============================================================
echo.
set /p confirm="确认删除以上历史文档？(y/N): "

if /i not "%confirm%"=="y" (
    echo 已取消删除
    pause
    exit /b 0
)

echo.
echo 开始删除...
echo.

REM 小说分析系统相关
if exist "AI辅助写小说的几个角度.md" (
    del "AI辅助写小说的几个角度.md"
    echo [✓] 删除 AI辅助写小说的几个角度.md
)

if exist "测试和加固计划.md" (
    del "测试和加固计划.md"
    echo [✓] 删除 测试和加固计划.md
)

if exist "前端查看分析结果指南.md" (
    del "前端查看分析结果指南.md"
    echo [✓] 删除 前端查看分析结果指南.md
)

if exist "如何运行压力测试.md" (
    del "如何运行压力测试.md"
    echo [✓] 删除 如何运行压力测试.md
)

if exist "世界观图终极升级工程文档.md" (
    del "世界观图终极升级工程文档.md"
    echo [✓] 删除 世界观图终极升级工程文档.md
)

if exist "项目交接文档-小说分析系统.md" (
    del "项目交接文档-小说分析系统.md"
    echo [✓] 删除 项目交接文档-小说分析系统.md
)

if exist "小说创作提示词.md" (
    del "小说创作提示词.md"
    echo [✓] 删除 小说创作提示词.md
)

if exist "小说分析系统设计规范.md" (
    del "小说分析系统设计规范.md"
    echo [✓] 删除 小说分析系统设计规范.md
)

if exist "小说分析系统实施进度.md" (
    del "小说分析系统实施进度.md"
    echo [✓] 删除 小说分析系统实施进度.md
)

if exist "小说分析系统完成报告.md" (
    del "小说分析系统完成报告.md"
    echo [✓] 删除 小说分析系统完成报告.md
)

if exist "小说分析性能优化完成报告.md" (
    del "小说分析性能优化完成报告.md"
    echo [✓] 删除 小说分析性能优化完成报告.md
)

if exist "新增依赖清单.md" (
    del "新增依赖清单.md"
    echo [✓] 删除 新增依赖清单.md
)

REM 可能过时的文档
if exist "NovelAIde 项目架构图.md" (
    del "NovelAIde 项目架构图.md"
    echo [✓] 删除 NovelAIde 项目架构图.md
)

if exist "NovelAIde 项目文档 v2.12.md" (
    del "NovelAIde 项目文档 v2.12.md"
    echo [✓] 删除 NovelAIde 项目文档 v2.12.md
)

echo.
echo ============================================================
echo 历史文档清理完成！
echo ============================================================
echo.
pause
