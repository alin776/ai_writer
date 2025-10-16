# NovelAIde 团队协作开发工作流程

## 📋 目录
- [团队组成](#团队组成)
- [开发环境配置](#开发环境配置)
- [Git 工作流程](#git-工作流程)
- [分支管理策略](#分支管理策略)
- [代码提交规范](#代码提交规范)
- [代码审查流程](#代码审查流程)
- [任务分配与协作](#任务分配与协作)
- [测试与部署](#测试与部署)
- [沟通协作机制](#沟通协作机制)

---

## 👥 团队组成

### 3人团队角色分工

**成员 A - 全栈负责人（Tech Lead）**
- 负责：架构设计、代码审查、技术选型
- 主要工作：
  - 核心功能开发（用户认证、AI 集成）
  - 数据库设计和优化
  - 技术难点攻坚
  - Code Review 最终把关

**成员 B - 前端工程师**
- 负责：前端界面和交互
- 主要工作：
  - React 组件开发
  - UI/UX 实现
  - 编辑器集成（Tiptap/Novel）
  - 前端状态管理（Zustand + React Query）
  - 前端路由和页面

**成员 C - 后端工程师**
- 负责：后端 API 和数据处理
- 主要工作：
  - FastAPI 接口开发
  - 数据库模型和迁移
  - Service 层业务逻辑
  - AI 服务封装（OpenAI API）
  - 性能优化和缓存

---

## 💻 开发环境配置

### 统一开发环境

**必装工具：**
```bash
# 1. 版本控制
Git 2.40+

# 2. Node.js 和包管理器
Node.js 18+ / 20+
npm 或 pnpm

# 3. Python 环境
Python 3.11+
pip

# 4. 数据库（选其一）
PostgreSQL 15+ (推荐)
或 SQLite（本地开发）

# 5. Redis（可选，用于缓存）
Redis 7+ 或 Memurai (Windows)

# 6. 编辑器
VS Code（推荐）+ 必装插件：
  - ESLint
  - Prettier
  - Python
  - GitLens
  - Tailwind CSS IntelliSense
```

### 环境配置步骤

**初次克隆项目后：**

```bash
# 1. 克隆仓库
git clone <repository-url>
cd ai_writer

# 2. 前端工程师配置前端环境
cd frontend  # (假设前端在 frontend 目录)
npm install
cp .env.example .env
# 编辑 .env 配置前端环境变量

# 3. 后端工程师配置后端环境
cd ../backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 配置后端环境变量

# 4. 创建数据库（如果使用 PostgreSQL）
# 执行 setup_db.sql 或手动创建

# 5. 初始化数据库
alembic upgrade head
```

---

## 🌿 Git 工作流程

### 采用 Git Flow 简化版

**主要分支：**

```
main (生产环境)
  ↑
develop (开发环境)
  ↑
feature/* (功能分支)
fix/* (修复分支)
hotfix/* (紧急修复)
```

### 分支说明

| 分支类型 | 命名规则 | 说明 | 生命周期 |
|---------|---------|------|---------|
| `main` | - | 生产环境分支，随时可发布 | 永久 |
| `develop` | - | 开发分支，集成最新功能 | 永久 |
| `feature/*` | `feature/功能名` | 新功能开发 | 临时 |
| `fix/*` | `fix/bug描述` | Bug 修复 | 临时 |
| `hotfix/*` | `hotfix/紧急问题` | 生产环境紧急修复 | 临时 |

---

## 📝 分支管理策略

### 日常开发流程

**1. 开始新功能**

```bash
# 1. 确保 develop 是最新的
git checkout develop
git pull origin develop

# 2. 创建功能分支
git checkout -b feature/user-authentication

# 3. 开发功能
# ... 编码 ...

# 4. 提交代码
git add .
git commit -m "feat(auth): 实现用户登录功能"

# 5. 推送到远程
git push -u origin feature/user-authentication

# 6. 创建 Pull Request (PR)
# 在 GitHub/GitLab 上创建 PR，请求合并到 develop
```

**2. 代码审查后合并**

```bash
# PR 审查通过后，由 Tech Lead 合并到 develop

# 删除本地和远程的功能分支
git checkout develop
git pull origin develop
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

**3. 发布到生产环境**

```bash
# 从 develop 合并到 main
git checkout main
git pull origin main
git merge develop
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

---

## 📋 代码提交规范

### Commit Message 格式

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型：**

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(editor): 添加 AI 续写按钮` |
| `fix` | Bug 修复 | `fix(auth): 修复 token 刷新失败问题` |
| `docs` | 文档更新 | `docs(readme): 更新安装步骤` |
| `style` | 代码格式（不影响功能） | `style(api): 格式化代码` |
| `refactor` | 重构 | `refactor(service): 优化用户服务层` |
| `perf` | 性能优化 | `perf(db): 添加数据库索引` |
| `test` | 测试 | `test(auth): 添加登录单元测试` |
| `chore` | 构建/工具变动 | `chore(deps): 升级依赖版本` |
| `ci` | CI/CD 配置 | `ci(github): 添加自动化测试` |

**Scope 范围：**

- 前端：`editor`, `ui`, `auth`, `works`, `chapters`
- 后端：`api`, `service`, `db`, `model`, `security`
- 通用：`config`, `docs`, `deps`

**示例：**

```bash
# 好的提交
git commit -m "feat(editor): 集成 Tiptap 编辑器

- 安装 Tiptap 核心依赖
- 创建 Editor 组件
- 添加基础工具栏
- 实现自动保存功能

Closes #12"

# 不好的提交
git commit -m "更新代码"  # ❌ 太模糊
git commit -m "fix bug"    # ❌ 没说明修了什么
```

---

## 🔍 代码审查流程

### Pull Request (PR) 规范

**1. PR 标题格式**

```
[类型] 功能描述

示例：
[Feature] 实现用户注册和登录功能
[Fix] 修复章节删除后排序错误
[Refactor] 优化 AI 服务调用逻辑
```

**2. PR 描述模板**

```markdown
## 📝 变更说明
简要描述本次 PR 的目的和改动内容

## 🎯 关联 Issue
Closes #123

## 📋 变更清单
- [ ] 功能点 1
- [ ] 功能点 2
- [ ] 功能点 3

## 🧪 测试说明
- [ ] 单元测试已通过
- [ ] 手动测试已完成
- [ ] 浏览器兼容性测试（前端）

## 📸 截图/视频（可选）
如果是 UI 相关，请附上截图

## 🔗 相关链接
- 设计稿：[链接]
- 技术文档：[链接]

## ⚠️ 注意事项
列出需要注意的地方（如数据库迁移、环境变量等）
```

### 代码审查清单

**审查者（Tech Lead）检查项：**

- [ ] **代码质量**
  - [ ] 符合项目代码规范
  - [ ] 没有明显的性能问题
  - [ ] 没有安全隐患
  - [ ] 错误处理完善

- [ ] **功能实现**
  - [ ] 功能符合需求
  - [ ] 边界情况处理
  - [ ] 用户体验良好

- [ ] **测试覆盖**
  - [ ] 有相应的测试
  - [ ] 测试通过
  - [ ] 测试覆盖率达标

- [ ] **文档更新**
  - [ ] API 文档更新
  - [ ] README 更新（如需要）
  - [ ] 代码注释清晰

- [ ] **数据库变更**
  - [ ] 数据库迁移脚本正确
  - [ ] 不会丢失数据
  - [ ] 索引合理

### 审查流程

```
1. 开发者提交 PR
   ↓
2. 自动化测试（CI）
   ↓
3. 至少 1 人审查（Tech Lead 必审）
   ↓
4. 审查意见修改
   ↓
5. 审查通过，合并到 develop
   ↓
6. 删除功能分支
```

---

## 📊 任务分配与协作

### 基于 todo.md 的任务分配

根据项目当前状态，任务分配建议：

**第一阶段：核心功能开发（2-3周）**

| 任务 | 负责人 | 优先级 | 预计时间 |
|------|--------|--------|---------|
| 后端基础架构搭建 | 成员 C | P0 | 3天 |
| 用户认证系统 | 成员 A | P0 | 3天 |
| 编辑器集成（Tiptap） | 成员 B | P0 | 5天 |
| 作品和章节 CRUD | 成员 C | P1 | 5天 |
| AI 服务集成 | 成员 A | P0 | 5天 |
| 前端状态管理完善 | 成员 B | P1 | 3天 |

**第二阶段：AI 增强功能（2周）**

| 任务 | 负责人 | 优先级 | 预计时间 |
|------|--------|--------|---------|
| 提示词管理系统 | 成员 C | P2 | 3天 |
| 大纲生成功能 | 成员 A | P2 | 5天 |
| AI 续写优化 | 成员 A | P1 | 3天 |
| 管理后台数据对接 | 成员 B | P1 | 3天 |

**第三阶段：世界观和组织工具（3周）**

| 任务 | 负责人 | 优先级 | 预计时间 |
|------|--------|--------|---------|
| 世界观构建系统 | 成员 B + C | P2 | 1周 |
| 数据统计和可视化 | 成员 B | P2 | 3天 |
| 搜索功能 | 成员 C | P3 | 3天 |
| 文件导入导出 | 成员 A | P3 | 5天 |

### 每日协作流程

**上午（9:00-12:00）**
- 9:00 - 每日站会（15分钟）
  - 昨天完成了什么
  - 今天计划做什么
  - 遇到什么阻碍
- 9:15 - 集中开发时间

**下午（14:00-18:00）**
- 集中开发时间
- 遇到问题随时沟通
- 16:00 - Code Review 时间（可选）

**每周例会（周一或周五）**
- 回顾本周进度
- 计划下周任务
- 技术分享（可选）

---

## 🧪 测试与部署

### 测试策略

**前端测试：**
```bash
# 单元测试
npm run test

# 覆盖率测试
npm run test:coverage

# E2E 测试
npm run test:e2e
```

**后端测试：**
```bash
# 单元测试
pytest

# 覆盖率测试
pytest --cov=app tests/

# 特定测试
pytest tests/test_users.py
```

**测试覆盖率要求：**
- 核心功能：80%+
- UI 组件：60%+
- 工具函数：90%+

### CI/CD 流程

**GitHub Actions 配置：**

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [develop, main]
  push:
    branches: [develop, main]

jobs:
  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm run lint
      - run: npm run test
      - run: npm run build

  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: black --check .
      - run: flake8
      - run: pytest
```

### 部署流程

**开发环境（自动部署）：**
- 合并到 `develop` → 自动部署到开发服务器

**生产环境（手动部署）：**
- 合并到 `main` → 打标签 → 手动触发部署

---

## 💬 沟通协作机制

### 沟通工具

**推荐工具栈：**

1. **即时通讯**
   - 钉钉 / 飞书 / 微信群
   - 紧急问题 @所有人

2. **项目管理**
   - GitHub Issues / Projects
   - 或 Jira / Trello

3. **文档协作**
   - 语雀 / Notion
   - 技术文档和会议记录

4. **代码托管**
   - GitHub / GitLab
   - Code Review 和 PR 讨论

### 沟通规范

**什么时候同步沟通（即时消息/语音）：**
- ✅ 紧急 Bug 需要立即修复
- ✅ 技术方案需要快速决策
- ✅ 遇到阻塞性问题
- ✅ 需要结对编程

**什么时候异步沟通（Issue/PR 评论）：**
- ✅ 非紧急的功能讨论
- ✅ 代码审查意见
- ✅ 文档更新建议
- ✅ 长期规划讨论

---

## 📚 最佳实践

### 开发建议

**1. 频繁提交，小步快跑**
```bash
# 好的做法
git commit -m "feat(auth): 添加用户模型"
git commit -m "feat(auth): 实现注册接口"
git commit -m "feat(auth): 添加登录验证"

# 不好的做法
# 一次性提交几百行代码
git commit -m "完成用户系统"
```

**2. 每天至少同步一次代码**
```bash
# 每天开始工作前
git checkout develop
git pull origin develop
git checkout feature/my-feature
git merge develop  # 或 git rebase develop
```

**3. PR 尽量小而专注**
- 一个 PR 只做一件事
- 代码行数建议 < 500 行
- 便于审查和回滚

**4. 重要变更提前沟通**
- 数据库 Schema 变更
- API 接口变更
- 重要架构调整

### 冲突处理

**遇到代码冲突：**

```bash
# 1. 拉取最新代码
git checkout develop
git pull origin develop

# 2. 合并到你的分支
git checkout feature/my-feature
git merge develop

# 3. 解决冲突
# 打开冲突文件，手动解决

# 4. 提交解决后的代码
git add .
git commit -m "merge: 解决与 develop 的冲突"
git push
```

**如果不确定如何解决冲突：**
- 先暂停，找 Tech Lead 讨论
- 可以使用 VS Code 的 Git 工具
- 或使用可视化工具（GitKraken、SourceTree）

---

## 🚨 紧急情况处理

### 生产环境 Bug

**流程：**

```bash
# 1. 从 main 创建 hotfix 分支
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. 修复 Bug
# ... 编码 ...

# 3. 提交并推送
git commit -m "fix(critical): 修复生产环境崩溃问题"
git push -u origin hotfix/critical-bug

# 4. 创建 PR 到 main（紧急审查）

# 5. 合并后同时合并回 develop
git checkout develop
git merge hotfix/critical-bug
git push origin develop

# 6. 部署到生产环境

# 7. 删除 hotfix 分支
```

---

## 📋 检查清单

### 提交代码前检查

- [ ] 代码符合规范（ESLint/Black 无警告）
- [ ] 删除了 `console.log` 和调试代码
- [ ] 添加了必要的注释
- [ ] 测试通过
- [ ] Commit message 符合规范
- [ ] 更新了相关文档

### 创建 PR 前检查

- [ ] 功能已完整实现
- [ ] 已在本地测试
- [ ] 已解决所有冲突
- [ ] PR 描述清晰
- [ ] 关联了相关 Issue

### 合并 PR 前检查

- [ ] CI 测试通过
- [ ] 至少 1 人审查通过
- [ ] 所有审查意见已处理
- [ ] 无未解决的讨论
- [ ] 确认可以合并

---

## 🎯 总结

**团队协作的关键：**

1. ✅ **清晰的分工** - 每个人知道自己负责什么
2. ✅ **规范的流程** - Git Flow + Code Review
3. ✅ **频繁的沟通** - 每日站会 + 随时讨论
4. ✅ **小步快跑** - 小功能、频繁提交、快速迭代
5. ✅ **互相帮助** - 遇到问题及时求助

**记住：**
- 没有愚蠢的问题，随时问
- 代码审查是学习的机会，不是批评
- 团队的成功比个人的完美更重要

---

## 📞 联系方式

- **Tech Lead（成员 A）**: [联系方式]
- **前端（成员 B）**: [联系方式]
- **后端（成员 C）**: [联系方式]

**项目相关链接：**
- 项目仓库：[GitHub 链接]
- 项目文档：[语雀/Notion 链接]
- 在线演示：[Demo 链接]

---

**最后更新时间：** 2025-10-15
**文档维护者：** Tech Lead
