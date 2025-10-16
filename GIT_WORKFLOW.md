# Git 前后端协作工作流程指南

## 📊 当前仓库状态

- **仓库地址**: https://github.com/alin776/ai_writer.git
- **当前分支**: main
- **协作人数**: 2人（前端 + 后端）
- **项目阶段**: 刚起步

---

## 🎯 推荐的协作方案

### 方案选择

由于项目刚起步，推荐使用 **GitHub Flow 简化版**：

```
main (主分支，保护分支)
  ↑
  ├── feature/frontend-xxx (前端功能分支)
  └── feature/backend-xxx (后端功能分支)
```

**优点：**
- ✅ 简单易用，适合小团队
- ✅ main 分支始终保持可部署状态
- ✅ 通过 PR 进行代码审查
- ✅ 避免代码冲突

---

## 📁 建议的目录结构

```
ai_writer/
├── .github/              # GitHub 配置
│   └── workflows/        # CI/CD 配置
├── frontend/             # 前端代码（前端负责）
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── backend/              # 后端代码（后端负责）
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── docs/                 # 文档（共同维护）
│   ├── api/              # API 文档
│   └── architecture/     # 架构文档
├── .gitignore            # Git 忽略文件
├── README.md             # 项目总README
└── docker-compose.yml    # Docker 配置
```

---

## 🔄 完整工作流程

### 场景：后端要提交代码，前端已经在 main

### 第1步：拉取最新代码

```bash
# 确保你在 main 分支
git checkout main

# 拉取前端刚提交的最新代码
git pull origin main
```

### 第2步：创建你的后端功能分支

```bash
# 从 main 创建新分支（命名规范）
git checkout -b feature/backend-api-setup

# 或者更具体的功能分支
git checkout -b feature/backend-user-auth
git checkout -b feature/backend-chapter-api
```

**命名规范：**
- `feature/backend-xxx` - 后端新功能
- `feature/frontend-xxx` - 前端新功能
- `fix/backend-xxx` - 后端bug修复
- `fix/frontend-xxx` - 前端bug修复

### 第3步：在自己的分支上工作

```bash
# 添加后端文件
git add backend/

# 也可以添加其他共享文件
git add ARCHITECTURE.md
git add PROGRESS_STATUS.md
git add todo.md
git add workflow.md

# 提交（写清楚的commit message）
git commit -m "feat(backend): 初始化后端项目结构

- 添加 FastAPI 基础框架
- 配置数据库连接
- 实现用户认证 API
- 添加测试脚本

Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>"
```

### 第4步：推送分支到远程

```bash
# 第一次推送使用 -u
git push -u origin feature/backend-api-setup

# 后续推送直接用
git push
```

### 第5步：在 GitHub 上创建 Pull Request

1. 访问 https://github.com/alin776/ai_writer
2. 会看到提示 "Compare & pull request" 按钮
3. 点击创建 PR：
   - **Base**: main
   - **Compare**: feature/backend-api-setup
   - **标题**: [Backend] 初始化后端项目结构
   - **描述**: 详细说明本次提交的内容

**PR 描述模板：**
```markdown
## 📝 变更说明
初始化后端项目结构，包括 FastAPI 框架和核心 API

## 📋 变更清单
- [x] FastAPI 项目初始化
- [x] 数据库配置
- [x] 用户认证 API
- [x] 作品管理 API
- [x] 章节管理 API
- [x] 测试脚本

## 🧪 测试情况
- [x] 所有测试通过（14/14）
- [x] API 文档：http://localhost:8000/docs

## 📸 截图
（如果有的话，贴上测试结果截图）

## ⚠️ 注意事项
- 需要安装 Python 依赖：`pip install -r backend/requirements.txt`
- 需要配置 `.env` 文件（参考 `.env.example`）

## 🔗 相关 Issue
Closes #1
```

### 第6步：前端同学审查代码

前端同学在 GitHub 上：
1. 查看 PR 的代码变更
2. 添加评论或建议
3. 点击 "Approve" 批准

###第7步：合并到 main

审查通过后：
1. 点击 "Merge pull request"
2. 选择 "Squash and merge" 或 "Create a merge commit"
3. 删除远程分支（可选）

### 第8步：同步本地 main

```bash
# 切换回 main
git checkout main

# 拉取最新合并的代码
git pull origin main

# 删除本地的功能分支（可选）
git branch -d feature/backend-api-setup
```

---

## 🔒 保护 main 分支（推荐设置）

在 GitHub 仓库设置中：

1. 进入 **Settings** → **Branches**
2. 点击 "Add rule"
3. 配置规则：
   - Branch name pattern: `main`
   - ✅ Require a pull request before merging
   - ✅ Require approvals (至少1个)
   - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require status checks to pass before merging

这样设置后，**任何人都不能直接推送到 main**，必须通过 PR。

---

## 🤝 日常协作流程

### 前端要提交代码

```bash
# 1. 更新 main
git checkout main
git pull origin main

# 2. 创建前端分支
git checkout -b feature/frontend-editor-integration

# 3. 开发前端功能
# ... 编码 ...

# 4. 提交
git add frontend/
git commit -m "feat(frontend): 集成 Tiptap 编辑器"

# 5. 推送
git push -u origin feature/frontend-editor-integration

# 6. 创建 PR 到 main
# 7. 后端审查通过后合并
```

### 后端要提交代码

```bash
# 1. 更新 main
git checkout main
git pull origin main

# 2. 创建后端分支
git checkout -b feature/backend-ai-service

# 3. 开发后端功能
# ... 编码 ...

# 4. 提交
git add backend/
git commit -m "feat(backend): 实现 AI 续写服务"

# 5. 推送
git push -u origin feature/backend-ai-service

# 6. 创建 PR 到 main
# 7. 前端审查通过后合并
```

### 如果两个人同时开发

```bash
# 前端在 feature/frontend-editor
# 后端在 feature/backend-ai

# 各自独立开发，互不影响
# 通过 PR 依次合并到 main
```

---

## ⚠️ 常见问题和解决方案

### Q1: 前端已经直接提交到 main 了怎么办？

**不要慌！现在开始规范就好：**

```bash
# 1. 拉取最新的 main（包含前端的提交）
git pull origin main

# 2. 从现在开始，你们都用分支开发
git checkout -b feature/backend-initial

# 3. 添加你的后端代码
git add backend/
git commit -m "feat(backend): 初始化后端项目"

# 4. 推送并创建 PR
git push -u origin feature/backend-initial
```

### Q2: 如何避免冲突？

**最佳实践：**

1. **目录隔离**：
   - 前端只修改 `frontend/` 目录
   - 后端只修改 `backend/` 目录
   - 共享文件（README、docs）协商修改

2. **频繁同步**：
   ```bash
   # 每天开始工作前
   git checkout main
   git pull origin main
   git checkout your-branch
   git merge main  # 合并最新的 main 到你的分支
   ```

3. **小步快跑**：
   - 功能完成就立即提 PR
   - 不要憋大招，一次提交太多代码

### Q3: 如果还是发生冲突了？

```bash
# 拉取最新 main 时发现冲突
git pull origin main

# Git 会提示哪些文件冲突
# 打开冲突的文件，会看到：
<<<<<<< HEAD
你的代码
=======
别人的代码
>>>>>>> origin/main

# 手动解决冲突（保留需要的代码）
# 然后：
git add 冲突文件
git commit -m "merge: 解决与 main 的冲突"
git push
```

### Q4: 不小心在 main 上做了修改怎么办？

```bash
# 如果还没提交
git stash  # 暂存修改
git checkout -b feature/backend-xxx  # 创建新分支
git stash pop  # 恢复修改

# 如果已经提交但没推送
git reset --soft HEAD~1  # 撤销commit但保留修改
git checkout -b feature/backend-xxx
git add .
git commit -m "feat(backend): xxx"

# 如果已经推送到 main（紧急情况）
# 联系前端同学，商量如何处理
```

### Q5: 如何查看前端提交了什么？

```bash
# 查看最近的提交历史
git log --oneline -10

# 查看某次提交的详细内容
git show <commit-hash>

# 查看前端目录的变更
git log --oneline -- frontend/

# 查看文件的修改历史
git log -p -- frontend/src/App.tsx
```

---

## 📝 Commit Message 规范

遵循约定式提交（Conventional Commits）：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具变动

**Scope 范围：**
- `frontend`: 前端相关
- `backend`: 后端相关
- `docs`: 文档
- `ci`: CI/CD

**示例：**
```bash
# 好的 commit
git commit -m "feat(backend): 实现用户认证 API

- 添加注册接口
- 添加登录接口
- 实现 JWT 认证
- 添加测试用例

Closes #123"

# 不好的 commit
git commit -m "更新代码"  # ❌ 太模糊
git commit -m "fix"        # ❌ 没说修了什么
```

---

## 🎯 快速参考命令

### 日常工作流

```bash
# 1. 开始新功能
git checkout main
git pull origin main
git checkout -b feature/backend-xxx

# 2. 开发中提交
git add .
git commit -m "feat(backend): xxx"

# 3. 推送到远程
git push -u origin feature/backend-xxx

# 4. 同步 main 的最新代码到你的分支
git checkout main
git pull origin main
git checkout feature/backend-xxx
git merge main

# 5. PR 合并后清理
git checkout main
git pull origin main
git branch -d feature/backend-xxx  # 删除本地分支
```

### 常用查询命令

```bash
# 查看状态
git status

# 查看历史
git log --oneline --graph --all

# 查看远程分支
git branch -a

# 查看某个文件的修改历史
git log --follow -- backend/app/main.py

# 查看当前分支与 main 的差异
git diff main..HEAD
```

---

## 📚 学习资源

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub Flow 指南](https://guides.github.com/introduction/flow/)
- [约定式提交规范](https://www.conventionalcommits.org/zh-hans/)

---

## 💡 总结

### ✅ 推荐做法

1. **永远不要直接在 main 上工作**
2. **每个功能创建独立分支**
3. **通过 PR 进行代码审查**
4. **频繁同步 main 的最新代码**
5. **写清晰的 commit message**

### ❌ 避免做法

1. ❌ 直接推送到 main
2. ❌ 长期不合并导致大冲突
3. ❌ commit message 写得模糊
4. ❌ 不经审查就合并
5. ❌ 修改不属于自己负责的代码

---

**协作的关键：沟通 + 规范 + 工具**

有任何问题随时在群里或 PR 评论中沟通！🎉
