# Git 忽略文件说明

> 本文档说明哪些文件不会提交到 Git 仓库，以及原因。

## 📋 被忽略的文件类别

### 1. Python 相关

#### 缓存和编译文件
```
__pycache__/          # Python 缓存目录
*.py[cod]             # 编译的 Python 文件
*$py.class            # Python 类文件
.mypy_cache/          # MyPy 类型检查缓存
```

**原因**：这些是自动生成的文件，每个人运行时都会重新生成。

#### 打包和安装文件
```
build/
dist/
*.egg-info/
*.egg
MANIFEST
```

**原因**：打包生成的临时文件，不需要版本控制。

---

### 2. 虚拟环境

```
venv/                 # 标准虚拟环境
ENV/
env/
.venv
pip/                  # pip 临时目录
```

**原因**：
- 虚拟环境很大（几百MB）
- 每个开发者应该自己创建虚拟环境
- 不同系统的虚拟环境不兼容

**如何重建**：运行 `setup.bat` 会自动创建虚拟环境

---

### 3. 环境变量（敏感信息）⚠️

```
.env                  # 包含密钥和密码
.env.local
.env.*.local
```

**原因**：
- 包含敏感信息（API Key、数据库密码等）
- 不同环境配置不同
- 泄露会有安全风险

**替代方案**：
- 提交 `.env.example` 作为模板
- 每个开发者复制并修改为自己的配置

---

### 4. 数据库文件

```
*.db
*.sqlite
*.sqlite3
novelaide.db
```

**原因**：
- 包含用户数据
- 文件很大
- 每个开发者应该有自己的测试数据

**如何重建**：启动服务时会自动创建表结构

---

### 5. 日志文件

```
logs/                 # 日志目录
*.log                 # 所有日志文件
```

**原因**：
- 日志文件会不断增长
- 包含运行时信息，不需要版本控制
- 每个环境的日志不同

---

### 6. 上传文件

```
uploads/              # 用户上传的文件
media/                # 媒体文件
```

**原因**：
- 用户上传的文件不是代码
- 可能很大
- 应该存储在文件服务器或云存储

---

### 7. IDE 和编辑器

```
.vscode/              # VS Code 配置
.idea/                # PyCharm 配置
*.swp, *.swo          # Vim 临时文件
.project              # Eclipse 配置
.settings/
```

**原因**：
- 每个开发者的 IDE 配置不同
- 不应该强制统一 IDE

---

### 8. 测试相关

#### 测试缓存
```
.pytest_cache/        # Pytest 缓存
.coverage             # 测试覆盖率数据
htmlcov/              # 覆盖率报告
.tox/                 # Tox 测试环境
```

**原因**：自动生成，每次运行测试都会重新生成。

#### 临时测试脚本 ⚠️
```
test_*.py             # 临时测试脚本
auto_test.py          # 自动测试工具
clear_users.py        # 清理用户数据
view_data.py          # 查看数据工具
```

**原因**：
- 开发过程中的临时测试脚本
- 可能包含调试代码
- 正式测试应该在 `tests/` 目录

**注意**：如果某个测试脚本需要保留，应该移到 `tests/` 目录。

---

### 9. 临时文档和笔记 ⚠️

```
API_TEST_LIST.md      # API 测试清单
FIX_SUMMARY.md        # 修复总结
HOW_TO_TEST.md        # 测试说明
NEXT_STEPS.md         # 下一步计划
README_TEST.md        # 测试文档
TEST_DATA.md          # 测试数据
PROGRESS_STATUS.md    # 进度状态
ARCHITECTURE_FIX_LOG.md  # 架构修复日志
```

**原因**：
- 开发过程中的临时笔记
- 内容可能过时
- 正式文档在 `docs/` 目录

**保留策略**：
- 如果内容有价值，整理后移到 `docs/` 目录
- 临时笔记不需要版本控制

---

### 10. 临时批处理脚本 ⚠️

```
run_tests.bat         # 运行测试
run_full_test.bat     # 完整测试
start_server.bat      # 启动服务器（已有 quick_start.bat）
VERIFY_FIX.bat        # 验证修复
```

**原因**：
- 临时调试脚本
- 已有正式的脚本（setup.bat, quick_start.bat）
- 可能包含硬编码路径

**保留策略**：
- 正式脚本：setup.bat, quick_start.bat, check_env.bat
- 临时脚本：不提交

---

### 11. 操作系统文件

```
.DS_Store             # macOS 文件夹配置
Thumbs.db             # Windows 缩略图缓存
Desktop.ini           # Windows 桌面配置
$RECYCLE.BIN/         # Windows 回收站
```

**原因**：操作系统自动生成，无意义。

---

### 12. 打包文件

```
*.tar.gz
*.zip
*.rar
```

**原因**：压缩包不需要版本控制。

---

### 13. Factory AI

```
.factory/             # Factory AI 工具目录
```

**原因**：本地开发工具配置，不需要提交。

---

## ✅ 应该提交的文件

### 源代码
- ✅ `app/` - 所有应用代码
- ✅ `tests/` - 正式的测试代码（不是临时测试脚本）
- ✅ `alembic/` - 数据库迁移文件

### 配置模板
- ✅ `.env.example` - 环境变量模板（不含敏感信息）
- ✅ `requirements.txt` - Python 依赖
- ✅ `pyproject.toml` - 项目配置
- ✅ `alembic.ini` - Alembic 配置

### 脚本
- ✅ `setup.bat` - 安装脚本
- ✅ `quick_start.bat` - 启动脚本
- ✅ `check_env.bat` - 环境检查脚本

### 数据库
- ✅ `setup_db.sql` - 数据库初始化脚本（SQL）

### 文档
- ✅ `docs/` - 所有正式文档
- ✅ `README.md` - 项目说明
- ✅ `START_HERE.md` - 快速开始

### Docker
- ✅ `Dockerfile`
- ✅ `docker-compose.yml`

### 其他配置
- ✅ `.gitignore` - Git 忽略规则
- ✅ `.flake8` - 代码检查配置

---

## 🔍 检查被忽略的文件

### 查看所有被忽略的文件

```bash
git status --ignored
```

### 查看某个文件是否被忽略

```bash
git check-ignore -v <文件名>
```

### 强制添加被忽略的文件（不推荐）

```bash
git add -f <文件名>
```

---

## ⚠️ 重要提醒

### 不要提交的内容

1. **敏感信息**：
   - ❌ 密码、API Key
   - ❌ 数据库凭证
   - ❌ 真实的用户数据

2. **临时文件**：
   - ❌ 缓存、日志
   - ❌ 编译文件
   - ❌ 临时测试脚本

3. **个人配置**：
   - ❌ IDE 配置
   - ❌ 个人的环境配置

### 如果不小心提交了敏感信息

```bash
# 从历史记录中删除文件（危险操作！）
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch <文件路径>" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送
git push origin --force --all
```

**建议**：如果泄露了 API Key，立即重新生成新的 Key！

---

## 📝 最佳实践

1. **提交前检查**：
   ```bash
   git status
   git diff --cached
   ```

2. **使用 .env.example**：
   - 提交模板文件
   - 注释说明每个配置项
   - 不包含真实值

3. **测试脚本管理**：
   - 临时测试 → 不提交
   - 正式测试 → 放在 `tests/` 目录

4. **文档管理**：
   - 临时笔记 → 不提交
   - 正式文档 → 放在 `docs/` 目录

5. **定期清理**：
   ```bash
   # 清理被忽略的文件
   git clean -Xn  # 预览
   git clean -Xf  # 执行删除
   ```

---

## 🔄 更新 .gitignore

如果需要添加新的忽略规则：

1. 编辑 `.gitignore` 文件
2. 添加文件或目录模式
3. 提交更改

如果文件已经被跟踪，需要先移除：

```bash
git rm --cached <文件名>
git commit -m "Remove tracked file"
```

---

## 📚 参考资源

- [Git 官方文档 - gitignore](https://git-scm.com/docs/gitignore)
- [GitHub - Python .gitignore 模板](https://github.com/github/gitignore/blob/main/Python.gitignore)
- [.gitignore 生成器](https://www.toptal.com/developers/gitignore)

---

## 💡 总结

✅ **提交**：源代码、配置模板、文档、脚本
❌ **不提交**：敏感信息、临时文件、缓存、日志、个人配置

遵循这些规则可以：
- 🔒 保护敏感信息
- 📦 减小仓库体积
- 🤝 避免团队冲突
- 🚀 提高克隆速度
