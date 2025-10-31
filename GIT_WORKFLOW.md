# Git 协作工作流程

> **版本**: v1.0
> **创建日期**: 2025-10-31
> **适用团队**: 前后端2人协作开发

---

## 📋 分支结构

```
main (生产分支，可部署)
 │
 ├─── dev (开发主分支，每日集成)
 │     │
 │     ├─── alin_qianduan (前端功能分支)
 │     └─── alin3.0 (后端功能分支)
```

### 分支说明

| 分支 | 用途 | 谁使用 | 何时合并 |
|------|------|--------|----------|
| **main** | 生产环境代码 | 项目负责人 | 功能稳定后 |
| **dev** | 开发主线，联调测试 | 前后端共同 | 每1-2天 |
| **alin_qianduan** | 前端功能开发 | 前端开发者 | 功能完成后 |
| **alin3.0** | 后端功能开发 | 后端开发者 | 功能完成后 |

---

## 🔄 日常工作流程

### 前端开发者工作流

#### 1. 每天开始工作
```bash
# 切换到前端分支
git checkout alin_qianduan

# 拉取 dev 最新代码（获取后端的更新）
git pull origin dev

# 如果有冲突，解决冲突后
git add .
git commit -m "merge: 同步dev分支"
```

#### 2. 开发功能
```bash
# 编写代码...

# 提交代码（小步提交，频繁commit）
git add .
git commit -m "feat(frontend): 完成登录页面优化"
git push origin alin_qianduan
```

#### 3. 功能完成后（1-2天一次）
```bash
# 切换到 dev 分支
git checkout dev

# 拉取最新代码
git pull origin dev

# 合并前端代码
git merge alin_qianduan --no-ff -m "merge: 合并前端xxx功能"

# 推送到远程
git push origin dev

# 切回前端分支继续开发
git checkout alin_qianduan

# 🔔 通知后端开发者：前端代码已合并到 dev
```

---

### 后端开发者工作流

#### 1. 每天开始工作
```bash
# 切换到后端分支
git checkout alin3.0

# 拉取 dev 最新代码（获取前端的更新）
git pull origin dev

# 如果有冲突，解决冲突后
git add .
git commit -m "merge: 同步dev分支"
```

#### 2. 开发功能
```bash
# 编写代码...

# 提交代码（小步提交，频繁commit）
git add .
git commit -m "feat(backend): 实现Agent API"
git push origin alin3.0
```

#### 3. 功能完成后（1-2天一次）
```bash
# 切换到 dev 分支
git checkout dev

# 拉取最新代码
git pull origin dev

# 合并后端代码
git merge alin3.0 --no-ff -m "merge: 合并后端xxx功能"

# 推送到远程
git push origin dev

# 切回后端分支继续开发
git checkout alin3.0

# 🔔 通知前端开发者：后端代码已合并到 dev
```

---

## 🧪 联调测试流程

当需要前后端联调时：

```bash
# 两人都切换到 dev 分支
git checkout dev
git pull origin dev

# 启动前后端服务进行联调
# 前端: npm run dev
# 后端: cd backend && python run.py

# 发现问题 → 切回各自分支修复 → 重新合并到 dev
```

---

## 📝 Commit 规范

### 格式
```
<type>(<scope>): <subject>

<body>
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(frontend): 添加登录页面` |
| `fix` | Bug修复 | `fix(backend): 修复Agent调用失败` |
| `docs` | 文档更新 | `docs: 更新API文档` |
| `style` | 代码格式 | `style: 格式化代码` |
| `refactor` | 重构 | `refactor: 重构Memory模块` |
| `test` | 测试 | `test: 添加单元测试` |
| `chore` | 构建/工具 | `chore: 更新依赖` |
| `merge` | 合并分支 | `merge: 合并dev分支` |

### Scope 范围

- `frontend` - 前端相关
- `backend` - 后端相关
- `ui` - UI组件
- `api` - API接口
- `agent` - Agent系统
- `docs` - 文档

### 示例

```bash
# 前端
git commit -m "feat(frontend): 优化编辑器交互体验"
git commit -m "fix(ui): 修复按钮样式问题"

# 后端
git commit -m "feat(backend): 实现质量循环评估"
git commit -m "fix(api): 修复续写接口超时"

# 文档
git commit -m "docs: 更新协作流程文档"
```

---

## ⚠️ 冲突处理

### 避免冲突的原则

1. **文件职责划分**
   ```
   前端主要负责:
   ├─ src/              # 前端代码
   ├─ public/           # 静态资源
   └─ package.json      # 前端依赖

   后端主要负责:
   ├─ backend/          # 后端代码
   ├─ docs/Agent/       # Agent文档
   └─ requirements.txt  # 后端依赖

   共同修改需协商:
   ├─ README.md
   ├─ .env
   └─ docker-compose.yml
   ```

2. **修改共享文件前沟通**
   - 修改前在群里说一声
   - 说明修改内容和原因
   - 等对方确认后再修改

3. **每天同步 dev 代码**
   - 早上开始工作前必做
   - 及时发现冲突，及时解决

### 冲突解决流程

如果遇到冲突：

```bash
# 1. 拉取代码时发现冲突
git pull origin dev
# Auto-merging xxx.py
# CONFLICT (content): Merge conflict in xxx.py

# 2. 查看冲突文件
git status

# 3. 打开冲突文件，会看到
<<<<<<< HEAD
你的代码
=======
别人的代码
>>>>>>> origin/dev

# 4. 手动解决冲突（保留需要的部分）

# 5. 标记为已解决
git add xxx.py

# 6. 完成合并
git commit -m "merge: 解决与dev的冲突"

# 7. 推送
git push origin alin_qianduan  # 或 alin3.0
```

### 紧急情况：放弃本地修改

```bash
# 如果本地改动不重要，直接用远程覆盖
git fetch origin
git reset --hard origin/dev
```

---

## 🚀 发布上线流程

当功能开发完成，需要上线时：

```bash
# 1. 确保 dev 分支稳定（前后端都已测试通过）
git checkout dev
git pull origin dev

# 2. 合并到 main
git checkout main
git pull origin main
git merge dev --no-ff -m "release: v1.x.x 版本发布"

# 3. 打标签
git tag -a v1.0.0 -m "版本 v1.0.0: 完成xxx功能"

# 4. 推送
git push origin main
git push origin v1.0.0

# 5. 部署生产环境
# ... 部署脚本 ...
```

---

## 📊 分支状态查看

### 查看分支关系
```bash
git log --oneline --graph --all --decorate
```

### 查看未合并的提交
```bash
# 查看 alin_qianduan 有哪些未合并到 dev
git log dev..alin_qianduan --oneline

# 查看 alin3.0 有哪些未合并到 dev
git log dev..alin3.0 --oneline
```

### 查看文件改动
```bash
# 查看工作区状态
git status

# 查看具体改动
git diff

# 查看已暂存的改动
git diff --staged
```

---

## 🛠️ 常用命令速查

### 基本操作
```bash
# 切换分支
git checkout <branch-name>

# 创建并切换新分支
git checkout -b <new-branch>

# 查看所有分支
git branch -a

# 拉取远程代码
git pull origin <branch>

# 推送到远程
git push origin <branch>
```

### 合并操作
```bash
# 合并分支（保留合并记录）
git merge <branch> --no-ff -m "merge: 合并xxx"

# 合并分支（快进合并）
git merge <branch>

# 取消合并
git merge --abort
```

### 回滚操作
```bash
# 撤销工作区修改
git checkout -- <file>

# 撤销暂存区
git reset HEAD <file>

# 回退到上一个提交
git reset --soft HEAD^

# 强制回退（危险！会丢失代码）
git reset --hard HEAD^
```

---

## 💡 最佳实践

### 1. 提交频率
- ✅ **推荐**: 小步提交，一个功能点一个 commit
- ❌ **避免**: 一天只提交一次，一次改动几百行

### 2. 同步频率
- ✅ **推荐**: 每天早上拉取 dev，每完成一个功能合并到 dev
- ❌ **避免**: 一周才同步一次，导致大量冲突

### 3. Commit 消息
- ✅ **推荐**: 清晰描述改了什么，为什么改
- ❌ **避免**: "update", "fix bug", "修改"

### 4. 代码审查
- ✅ **推荐**: 合并前互相 review 代码
- ❌ **避免**: 直接合并，不看对方的代码

### 5. 测试
- ✅ **推荐**: 本地测试通过再推送
- ❌ **避免**: 推送后才发现代码报错

---

## 📞 沟通机制

### 日常沟通
- 每天下班前，在群里说明自己改了哪些模块
- 遇到需要改共享文件，提前沟通
- 发现对方代码有问题，及时反馈

### 紧急情况
- 发现严重 Bug 立即告知
- 需要紧急发布提前规划
- 遇到复杂冲突两人一起解决

### 定期会议
- 每周一次代码 Review 会议
- 每两周一次技术分享
- 遇到问题及时讨论

---

## 🎯 检查清单

### 每天开始工作
- [ ] 切换到自己的分支
- [ ] 拉取 dev 最新代码
- [ ] 解决冲突（如果有）

### 提交代码前
- [ ] 代码已测试通过
- [ ] Commit 消息符合规范
- [ ] 没有提交调试代码
- [ ] 没有提交敏感信息

### 合并到 dev 前
- [ ] 自己分支已同步 dev
- [ ] 代码已在本地测试
- [ ] 已告知另一个开发者
- [ ] 合并后推送到远程

### 发布上线前
- [ ] dev 分支已充分测试
- [ ] 前后端联调通过
- [ ] 文档已更新
- [ ] 备份已完成

---

## 📚 相关资源

- [Git 官方文档](https://git-scm.com/doc)
- [Git Flow 工作流](https://nvie.com/posts/a-successful-git-branching-model/)
- [Commit 规范参考](https://www.conventionalcommits.org/)

---

## 🆘 遇到问题？

1. 先查看本文档的"冲突处理"章节
2. 使用 `git status` 查看当前状态
3. 不确定的操作先在测试分支尝试
4. 实在不会就找对方一起解决
5. 重要操作前先备份代码

---

**记住**: Git 的核心是**沟通和同步**，不是技术本身！

**祝开发顺利！** 🎉
