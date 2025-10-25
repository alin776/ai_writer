# 🧪 AI 改写助手测试指南

> 本文档提供 AI 改写助手功能的完整测试指南，包括手动测试和自动化测试。

## 📋 目录

- [测试环境准备](#测试环境准备)
- [手动测试步骤](#手动测试步骤)
- [自动化测试](#自动化测试)
- [故障排查](#故障排查)
- [测试检查清单](#测试检查清单)

---

## 测试环境准备

### 1. 确保后端服务运行

**重要提示**：修改代码后必须重启服务！

#### 方法 A：重启现有服务

```bash
# 1. 按 Ctrl+C 停止服务
# 2. 重新启动
cd backend
python -m uvicorn app.main:app --reload
```

#### 方法 B：新开终端启动

```bash
cd D:\Java\ai_writer\backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

**验证服务启动成功**：
- ✅ 看到 `Application startup complete` 消息
- ✅ 访问 http://localhost:8000/docs 能正常打开
- ✅ 日志中没有错误信息

### 2. 确认虚拟环境激活

```bash
# Windows
cd backend
venv\Scripts\activate

# Linux/Mac
cd backend
source venv/bin/activate
```

### 3. 检查依赖安装

```bash
# 确认 langchain-core 已安装
pip list | findstr langchain-core
# 应该看到: langchain-core==0.3.0
```

---

## 手动测试步骤

### 方式一：使用 Swagger UI（推荐）

1. **打开 Swagger UI**
   - 访问：http://localhost:8000/docs

2. **登录获取 Token**
   - 找到 `POST /api/v1/auth/login`
   - 点击 "Try it out"
   - 输入测试账号：
     - username: `test@example.com`
     - password: `password123`
   - 点击 "Execute"
   - 复制返回的 `access_token`

3. **设置认证**
   - 点击页面右上角的 "Authorize" 按钮
   - 输入：`Bearer <access_token>`
   - 点击 "Authorize"

4. **测试各个接口**

#### 测试 1：获取可用模型列表
- 接口：`GET /api/v1/ai/rewrite-arena/models`
- 预期结果：返回模型列表，至少包含 gemini-2.5-pro 和 gpt-5

#### 测试 2：智能分析文本
- 接口：`POST /api/v1/ai/rewrite-arena/analyze`
- 请求体：
  ```json
  {
    "text": "主角走进房间，看到了桌子上的剑。",
    "context_before": null,
    "context_after": null
  }
  ```
- 预期结果：
  - 返回 `quality_score`（0-100）
  - 返回 `issues` 列表
  - 返回 `suggested_mode`
  - 耗时 1-3 秒

#### 测试 3：多模型改写文本
- 接口：`POST /api/v1/ai/rewrite-arena/rewrite`
- 请求体：
  ```json
  {
    "text": "主角走进房间，看到了桌子上的剑。",
    "mode": "expand",
    "context_before": null,
    "context_after": null,
    "custom_requirement": null,
    "model_ids": ["gemini-2.5-pro", "gpt-5"]
  }
  ```
- 预期结果：
  - 返回 2 个改写结果
  - 每个结果包含 `rewritten_text`、`word_count`、`elapsed_time`
  - 所有结果的 `success` 都为 `true`
  - 总耗时 2-5 秒

#### 测试 4：保存改写记录
- 接口：`POST /api/v1/rewrite-history/sessions`
- 请求体：
  ```json
  {
    "original_text": "主角走进房间，看到了桌子上的剑。",
    "mode": "expand",
    "context_before": null,
    "context_after": null,
    "custom_requirement": null,
    "results": [
      {
        "model_name": "gemini-2.5-pro",
        "rewritten_text": "主角推开那扇厚重的木门，缓缓走进了这间房间...",
        "word_count": 156,
        "elapsed_time": 2.3,
        "error": null,
        "is_selected": true
      },
      {
        "model_name": "gpt-5",
        "rewritten_text": "房门在主角的推动下缓缓打开...",
        "word_count": 142,
        "elapsed_time": 1.8,
        "error": null,
        "is_selected": false
      }
    ]
  }
  ```
- 预期结果：
  - 返回 200 状态码
  - 返回完整的会话信息，包含 `id` 和 `results`

#### 测试 5：获取历史记录列表
- 接口：`GET /api/v1/rewrite-history/sessions?page=1&page_size=20`
- 预期结果：
  - 返回会话列表
  - 包含 `total`、`page`、`page_size` 字段

#### 测试 6：获取会话详情
- 接口：`GET /api/v1/rewrite-history/sessions/{session_id}`
- 使用上一步保存返回的 session_id
- 预期结果：返回完整的会话信息和所有结果

#### 测试 7：删除会话
- 接口：`DELETE /api/v1/rewrite-history/sessions/{session_id}`
- 预期结果：返回删除成功消息

---

## 自动化测试

### 快速测试（推荐）

**测试内容**：保存改写历史功能

```bash
cd D:\Java\ai_writer\backend
venv\Scripts\activate
python quick_test_save.py
```

**预期输出**：
```
============================================================
快速验证：保存改写历史功能
============================================================

▶ 1. 登录...
✓ 登录成功

▶ 2. 保存改写历史...
✓ 保存成功！
  会话ID: [UUID]
  结果数量: 2

============================================================
✅ 测试通过！修复成功！
============================================================
```

### 完整测试

**测试内容**：所有 8 个 API 接口

```bash
cd D:\Java\ai_writer\backend
venv\Scripts\activate
python test_rewrite_arena.py
```

**预期输出**：
```
============================================================
AI 改写助手自动化测试
============================================================

▶ 1. 用户登录
✓ 登录成功

▶ 2. 获取可用模型列表
✓ 成功获取 4 个模型

▶ 3. 智能分析文本
✓ 文本分析完成

▶ 4. 多模型改写文本
✓ 改写完成，共 2 个结果

▶ 5. 保存改写历史
✓ 历史记录保存成功

▶ 6. 获取改写历史列表
✓ 成功获取历史记录

▶ 7. 获取会话详情
✓ 成功获取会话详情

▶ 8. 删除会话
✓ 成功删除会话

============================================================
测试总结
============================================================
总测试数: 8
通过: 8
失败: 0
============================================================

✅ 所有测试通过！
============================================================
```

### 自定义测试参数

可以通过环境变量自定义测试参数：

```bash
# Windows PowerShell
$env:API_BASE_URL="http://localhost:8001"
$env:TEST_USERNAME="myuser@example.com"
$env:TEST_PASSWORD="mypassword"
python quick_test_save.py

# Linux/Mac
export API_BASE_URL=http://localhost:8001
export TEST_USERNAME=myuser@example.com
export TEST_PASSWORD=mypassword
python quick_test_save.py
```

---

## 故障排查

### 问题 1：后端服务未启动

**错误**：`Connection refused` 或 `ConnectError`

**症状**：
```
httpcore._exceptions.ConnectError: [WinError 10061] 由于目标计算机积极拒绝，无法连接。
```

**解决**：
```bash
# 启动后端服务
cd backend
python -m uvicorn app.main:app --reload
```

**验证**：访问 http://localhost:8000/docs

---

### 问题 2：端口被占用

**错误**：`Address already in use`

**解决方案 A**：更改端口
```bash
python -m uvicorn app.main:app --reload --port 8001
```

然后修改测试脚本：
```bash
$env:API_BASE_URL="http://localhost:8001"
python quick_test_save.py
```

**解决方案 B**：关闭占用端口的进程
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [进程ID] /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

---

### 问题 3：代码未更新

**错误**：仍然出现 `MissingGreenlet` 错误或其他已修复的错误

**原因**：修改代码后未重启服务

**解决**：
1. 确认所有代码修改都已保存
2. **重启后端服务**（Ctrl+C 停止，然后重新启动）
3. 如果使用 `--reload`，等待 2-3 秒让服务重新加载
4. 检查日志确认服务已重新加载

**验证**：
```bash
# 检查日志，应该看到：
# Watching for file changes with StatReload
# Started reloader process...
# Application startup complete.
```

---

### 问题 4：虚拟环境未激活

**错误**：`ModuleNotFoundError: No module named 'httpx'`

**解决**：
```bash
# Windows
cd backend
venv\Scripts\activate

# Linux/Mac
cd backend
source venv/bin/activate
```

**验证**：
```bash
# 命令提示符应该有 (venv) 前缀
(venv) PS D:\Java\ai_writer\backend>
```

---

### 问题 5：httpx.ReadTimeout

**错误**：请求 30 秒后超时

**可能原因**：
1. AI 服务响应慢
2. 网络问题
3. API 密钥未配置或无效

**解决**：
1. 检查 `.env` 文件中的 API 密钥配置
2. 检查网络连接
3. 增加超时时间（如果需要）
4. 查看后端服务日志了解具体错误

---

### 问题 6：MissingGreenlet 错误

**错误**：`sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called`

**状态**：✅ **已修复**

**如果仍然出现**：
1. 确认使用的是最新代码
2. 重启后端服务
3. 查看 `backend/docs/TROUBLESHOOTING.md` 了解详细解决方案

---

## 测试检查清单

使用此清单确保所有测试步骤都已完成：

### 环境检查
- [ ] 后端服务已启动
- [ ] 能访问 http://localhost:8000/docs
- [ ] 虚拟环境已激活
- [ ] 依赖包已安装（langchain-core==0.3.0）

### 功能测试
- [ ] 能获取可用模型列表
- [ ] 能智能分析文本（返回质量评分和建议）
- [ ] 能多模型改写文本（至少 2 个模型）
- [ ] 能保存改写历史到数据库
- [ ] 能获取改写历史列表（分页）
- [ ] 能获取会话详情
- [ ] 能删除会话

### 性能测试
- [ ] 智能分析耗时 < 3 秒
- [ ] 双模型改写耗时 < 5 秒
- [ ] 保存历史耗时 < 1 秒
- [ ] 获取列表耗时 < 500ms

### 错误处理
- [ ] 未登录时返回 401
- [ ] 文本过长时返回 400
- [ ] 访问他人会话时返回 403
- [ ] 访问不存在的会话时返回 404

---

## 快速测试命令（复制粘贴）

### 终端 1 - 启动服务
```bash
cd D:\Java\ai_writer\backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

### 终端 2 - 运行快速测试
```bash
cd D:\Java\ai_writer\backend
venv\Scripts\activate
python quick_test_save.py
```

### 终端 2 - 运行完整测试
```bash
cd D:\Java\ai_writer\backend
venv\Scripts\activate
python test_rewrite_arena.py
```

---

## 成功标志

### 快速测试成功
```
✓ 保存成功！
  会话ID: [UUID]
  结果数量: 2
```

### 完整测试成功
```
============================================================
测试总结
============================================================
总测试数: 8
通过: 8
失败: 0
============================================================

✅ 所有测试通过！
============================================================
```

---

## 下一步

测试通过后：
1. ✅ 确认所有功能正常
2. ✅ Phase 1（后端开发）完成
3. ⏭️ 开始 Phase 2（前端开发）

---

## 相关文档

- **TROUBLESHOOTING.md** - 常见问题和解决方案
- **API_REFERENCE.md** - API 接口详细文档
- **DATABASE_SCHEMA.md** - 数据库表结构
- **HOW_TO_TEST.md** - 简化版测试指南

---

**祝测试顺利！** 🚀

如果遇到问题，请查看 TROUBLESHOOTING.md 或联系开发团队。
