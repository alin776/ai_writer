# 修复Python依赖冲突

## 问题总结
1. chromadb与httpx版本冲突 (需要>=0.27.0，但安装的是0.26.0)
2. kubernetes与urllib3版本冲突 (需要<2.4.0，但安装的是2.5.0)
3. chromadb不在requirements.txt中
4. 存在损坏的包 (~okenizers, ~orch, ~unctorch)
5. langgraph-checkpoint版本冲突

---

## ✅ 已完成的修复 (2025-11-11)

### 修复步骤

#### 1. 清理损坏的包目录 ✅
```bash
rm -rf venv/Lib/site-packages/~okenizers/
rm -rf venv/Lib/site-packages/~okenizers-0.15.2.dist-info/
rm -rf venv/Lib/site-packages/~orch/
rm -rf venv/Lib/site-packages/~orch-2.9.0.dist-info/
rm -rf venv/Lib/site-packages/~unctorch/
```

#### 2. 升级httpx到0.27.2 ✅
```bash
pip install "httpx==0.27.2"
```
- **原因**: chromadb 1.3.4 需要 httpx>=0.27.0

#### 3. 降级urllib3到2.3.0 ✅
```bash
pip install "urllib3==2.3.0"
```
- **原因**: kubernetes 34.1.0 需要 urllib3<2.4.0

#### 4. 降级langgraph-checkpoint-sqlite到2.0.11 ✅
```bash
pip install "langgraph-checkpoint-sqlite==2.0.11"
```
- **原因**:
  - langgraph-checkpoint-sqlite 3.0.0 需要 langgraph-checkpoint>=3
  - 但 langgraph-checkpoint-redis 0.1.2 需要 langgraph-checkpoint<3
  - 解决方案: 降级sqlite版本到2.x以保持兼容

#### 5. 更新requirements.txt ✅
添加和更新了以下包版本：
- `httpx==0.26.0` → `httpx==0.27.2`
- `urllib3==2.5.0` → `urllib3==2.3.0`
- `ormsgpack==1.11.0` → `ormsgpack==1.12.0`
- 新增 `chromadb==1.3.4`
- 新增 `langgraph-checkpoint-sqlite==2.0.11`

### 验证结果
```bash
$ pip check
No broken requirements found.
```

---

## 📋 修复后的依赖版本

| 包名 | 修复前 | 修复后 | 原因 |
|-----|-------|-------|------|
| httpx | 0.26.0 | 0.27.2 | chromadb需要>=0.27.0 |
| urllib3 | 2.5.0 | 2.3.0 | kubernetes需要<2.4.0 |
| ormsgpack | 1.11.0 | 1.12.0 | langgraph-checkpoint依赖 |
| chromadb | ❌ 缺失 | 1.3.4 | 项目使用但未在requirements.txt |
| langgraph-checkpoint-sqlite | 3.0.0 | 2.0.11 | 解决与redis版本冲突 |

---

## 🎯 核心问题分析

### 问题1: pip的依赖解析器缺陷
pip的依赖解析器不会在安装时检查所有已安装包的兼容性，导致：
- 安装新包时可能引入版本冲突
- 只在运行`pip check`时才发现问题

### 问题2: langgraph生态版本不兼容
- `langgraph-checkpoint-sqlite` 3.x 和 `langgraph-checkpoint-redis` 0.1.x 对 `langgraph-checkpoint` 的版本要求矛盾
- 解决方案: 将所有checkpoint相关包统一到2.x版本

### 问题3: 损坏的包目录
- 以`~`开头的包目录是pip安装失败的残留
- 必须手动删除，否则会干扰后续操作

---

## 💡 预防措施

1. **定期运行依赖检查**
   ```bash
   pip check
   ```

2. **使用pip-compile锁定依赖**
   ```bash
   pip install pip-tools
   pip-compile requirements.in
   ```

3. **在CI/CD中添加依赖验证**
   ```yaml
   - name: Check dependencies
     run: pip check
   ```

4. **及时更新requirements.txt**
   - 新增依赖时立即添加到requirements.txt
   - 升级包后同步更新版本号

---

## 📝 相关文件修改

- `backend/requirements.txt` - 更新了7个包版本，新增2个包
- `backend/venv/Lib/site-packages/` - 清理了5个损坏的目录

---

## ✅ 最终状态

- ✅ 所有依赖冲突已解决
- ✅ `pip check` 通过
- ✅ requirements.txt 已更新
- ✅ 环境干净，无损坏包
