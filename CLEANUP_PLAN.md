# 文件清理计划 - 2025-10-26

## 📋 清理原则

1. **保留**: 有用的、当前使用的、文档化的文件
2. **删除**: 临时的、过时的、重复的文件
3. **归档**: 有历史价值但不常用的文件

---

## 🔧 脚本文件分析

### ❌ 可以删除的脚本 (11个)

#### 根目录脚本 (4个)
- `AUTO_TEST.bat` - 自动测试脚本 (临时)
- `GET_TOKEN.bat` - 获取token脚本 (临时调试)
- `TEST_COST_MONITOR.bat` - 成本监控测试 (临时)
- `cleanup_optional.bat` - 可选清理脚本 (一次性)

#### backend目录脚本 (7个)
- `backend/clear_cache.bat` - 清理缓存 (临时,已在.gitignore)
- `backend/check_env.bat` - 环境检查 (临时调试)
- `backend/compile_pgvector_final.bat` - pgvector编译 (一次性完成)
- `backend/run_performance_test.bat` - 性能测试 (已有pytest)
- `backend/setup_auto.bat` - 自动安装 (重复,有setup.bat)
- `backend/setup_for_new_dev.bat` - 新开发者安装 (重复)
- `backend/START_BACKEND.bat` - 启动后端 (临时,应用uvicorn命令)

### ✅ 必须保留的脚本 (1个)

- `backend/setup.bat` - 官方安装脚本 (首次部署必需)

**理由**: 这是标准的开发环境搭建脚本,新开发者需要

---

## 📄 文档文件分析

### ❌ backend/docs 可删除文档 (6个)

这些是**测试修复过程文档**,已被 TEST_FIX_SUMMARY.md 汇总:

1. `CONFTEST_FIX.md` - conftest修复详情 (已归档到TEST_FIX_SUMMARY.md)
2. `ERROR.md` - 错误记录 (临时调试文档)
3. `ERROR_FIX_COMPLETE.md` - 错误修复完成 (临时文档)
4. `ERROR_FIX_ROUND2.md` - 第二轮修复 (临时文档)
5. `INFO.md` - 测试信息 (已被TEST_RESULTS.md替代)
6. `TESTING_FIX.md` - 测试修复详情 (已归档到TEST_FIX_SUMMARY.md)

**理由**: 这些都是调试过程记录,最终结果已汇总到 TEST_FIX_SUMMARY.md 和 TEST_RESULTS.md

### ✅ backend/docs 必须保留文档 (18个)

#### API文档 (3个)
- `AI_REWRITE_ASSISTANT_API.md` - AI改写API完整文档 ⭐
- `AI_REWRITE_ASSISTANT_API_QUICK_REFERENCE.md` - API快速参考 ⭐
- `API_REFERENCE.md` - 后端API参考

#### 配置部署 (4个)
- `CONFIG_GUIDE.md` - 配置指南
- `POSTGRESQL_SETUP.md` - 数据库安装
- `QUICKSTART_SETUP.md` - 快速开始
- `一键部署包说明.md` - 部署说明

#### 数据库文档 (3个)
- `DATABASE_SCHEMA.md` - 数据库Schema
- `数据库配置说明.md` - 数据库配置
- `数据库迁移指南.md` - 迁移指南

#### 测试文档 (4个)
- `TEST_FIX_SUMMARY.md` - 测试修复总结 ⭐⭐
- `TEST_RESULTS.md` - 测试结果报告 ⭐
- `TEST_ACCOUNT_CONFIG.md` - 测试账号配置
- `TESTING_GUIDE.md` - 测试指南

#### 其他文档 (4个)
- `TROUBLESHOOTING.md` - 故障排除
- `MIGRATION_FIX.md` - 数据库迁移修复记录
- `前端开发者指南.md` - 前端快速上手

---

### ❌ docs 目录可删除文档 (1个)

- `docs/README.md.backup` - 备份文件 (临时备份)

### ✅ docs 目录必须保留文档 (24个)

**全部保留** - 这些都是项目核心文档,已在 DOCS_INDEX.md 中索引

---

### ❌ 根目录可删除文档 (11个)

#### 过时的实施文档 (6个)
- `小说分析系统设计规范.md` - 已实施完成
- `小说分析系统实施进度.md` - 已实施完成
- `小说分析系统完成报告.md` - 已归档到 docs/
- `小说分析性能优化完成报告.md` - 已归档到 docs/
- `项目交接文档-小说分析系统.md` - 已归档到 docs/
- `世界观图终极升级工程文档.md` - 已实施完成

#### 临时指南 (3个)
- `前端查看分析结果指南.md` - 临时指南,已归档到 docs/
- `如何运行压力测试.md` - 临时指南,已归档到 docs/
- `新增依赖清单.md` - 临时记录,已过时

#### 临时清理指南 (1个)
- `CLEANUP_GUIDE.md` - 之前的清理指南,将被本次替代

#### 临时记录 (1个)
- `测试和加固计划.md` - 已完成,可删除

### ⚠️ 根目录需要评估的文档 (6个)

#### 可能保留
- `NovelAIde 项目文档 v2.12.md` - **老版本文档** (已有 docs/README.md v2.14)
  - **建议**: 删除 (内容已整合到 docs/ 目录)
  
- `NovelAIde 项目架构图.md` - **架构图** 
  - **建议**: **保留** (仍然有参考价值)

- `CHANGELOG.md` - **变更日志**
  - **建议**: **保留** (已在 docs/12-changelog.md,但根目录的更全面)

- `rules.md` - **开发规范**
  - **建议**: **保留** (开发团队协作规范)

- `workflow.md` - **工作流程**
  - **建议**: **保留** (开发流程文档)

- `AI辅助写小说的几个角度.md` - **产品思考文档**
  - **建议**: **保留** (产品设计参考)

- `小说创作提示词.md` - **Prompt库**
  - **建议**: **保留** (AI prompt参考)

---

## 📊 清理统计

| 类型 | 可删除 | 必须保留 | 需评估 |
|------|--------|---------|--------|
| 脚本 | 11个 | 1个 | 0个 |
| backend/docs | 6个 | 18个 | 0个 |
| docs | 1个 | 24个 | 0个 |
| 根目录md | 11个 | 7个 | 0个 |
| **总计** | **29个** | **50个** | **0个** |

---

## ✅ 最终清理清单

### 立即删除 (29个)

#### 脚本 (11个)
```bash
# 根目录
AUTO_TEST.bat
GET_TOKEN.bat
TEST_COST_MONITOR.bat
cleanup_optional.bat

# backend
backend/clear_cache.bat
backend/check_env.bat
backend/compile_pgvector_final.bat
backend/run_performance_test.bat
backend/setup_auto.bat
backend/setup_for_new_dev.bat
backend/START_BACKEND.bat
```

#### 文档 (18个)
```bash
# backend/docs (6个)
backend/docs/CONFTEST_FIX.md
backend/docs/ERROR.md
backend/docs/ERROR_FIX_COMPLETE.md
backend/docs/ERROR_FIX_ROUND2.md
backend/docs/INFO.md
backend/docs/TESTING_FIX.md

# docs (1个)
docs/README.md.backup

# 根目录 (11个)
NovelAIde\ 项目文档\ v2.12.md
小说分析系统设计规范.md
小说分析系统实施进度.md
小说分析系统完成报告.md
小说分析性能优化完成报告.md
项目交接文档-小说分析系统.md
世界观图终极升级工程文档.md
前端查看分析结果指南.md
如何运行压力测试.md
新增依赖清单.md
CLEANUP_GUIDE.md
测试和加固计划.md
```

### 必须保留 (50个)

#### 脚本 (1个)
- `backend/setup.bat` - 官方安装脚本

#### backend/docs (18个) - 全部保留
#### docs (24个) - 全部保留  
#### 根目录 (7个)
- NovelAIde 项目架构图.md
- CHANGELOG.md
- rules.md
- workflow.md
- AI辅助写小说的几个角度.md
- 小说创作提示词.md

---

## 🎯 执行建议

### 方案1: 全部删除 (推荐)
一次性删除所有29个临时文件

### 方案2: 分批删除
1. 第一批: 删除所有脚本 (11个)
2. 第二批: 删除 backend/docs 临时文档 (6个)
3. 第三批: 删除根目录过时文档 (12个)

---

**创建时间**: 2025-10-26
**状态**: 待执行
