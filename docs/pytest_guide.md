# Pytest 自动化测试指南

## 📦 安装依赖

### 方法1: 安装测试依赖（推荐）

```bash
# 在项目根目录执行
./venv/Scripts/pip.exe install -r requirements-test.txt
```

### 方法2: 只安装核心依赖

```bash
./venv/Scripts/pip.exe install pytest pytest-asyncio httpx
```

---

## 🚀 运行测试

### 基础命令

```bash
# 运行所有测试（详细输出）
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v

# 运行所有测试（简洁输出）
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py
```

### 筛选测试

```bash
# 只运行Planning模式测试
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v -k "planning"

# 只运行chat()模式测试
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v -k "chat_mode"

# 只运行边界条件测试
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v -k "boundary"

# 排除某些测试
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v -k "not slow"
```

### 生成HTML报告

```bash
# 生成HTML测试报告
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --html=report.html --self-contained-html

# 报告会生成在: D:\Java\ai_writer\report.html
```

### 失败重试

```bash
# 失败的测试自动重试3次
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --reruns 3

# 失败重试，间隔2秒
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --reruns 3 --reruns-delay 2
```

### 并发执行

```bash
# 使用4个进程并发执行（需要pytest-xdist）
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v -n 4

# 自动检测CPU核心数并发执行
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v -n auto
```

### 覆盖率报告

```bash
# 生成代码覆盖率报告
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --cov=app --cov-report=html

# 报告会生成在: htmlcov/index.html
```

### 详细日志

```bash
# 显示详细日志
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v -s

# 显示所有print输出
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --capture=no
```

---

## 📊 测试用例说明

### chat() 模式测试（3个参数化用例）

```python
test_chat_mode[一般对话]
test_chat_mode[写作请求]
test_chat_mode[分析请求]
```

**验证内容**:
- HTTP状态码200
- 响应数据非空
- 响应文本长度 > 0
- 意图分类正确（可选）

### chat_stream() 模式测试（2个参数化用例）

```python
test_chat_stream_mode[创作任务]
test_chat_stream_mode[咨询对话]
```

**验证内容**:
- 接收到事件数量 > 0
- 响应内容非空
- ✅ React模式content正确解析（不包含字典字符串）
- 事件统计中content事件 > 0

### Planning 模式测试（4个参数化用例）

```python
test_planning_mode[小说大纲规划]
test_planning_mode[世界观构建]
test_planning_mode[角色设计]
test_planning_mode[复杂多任务]
```

**验证内容**:
- 检测到的阶段 ≥ 2
- 三个阶段（Planning, Execution, Response）
- 任务数量 ≥ 预期值的80%
- ✅ Planning模式content正确解析
- 响应内容非空

### 边界条件测试（2个参数化用例）

```python
test_boundary_conditions[超短消息]
test_boundary_conditions[超长消息]
```

**验证内容**:
- HTTP状态码200
- 响应数据非空

### 连接测试（2个独立用例）

```python
test_server_connection  # 服务器连接测试
test_login              # OAuth2登录测试
```

---

## 📈 预期测试结果

### 总测试数

- **chat() 模式**: 3个测试
- **chat_stream() 模式**: 2个测试
- **Planning 模式**: 4个测试
- **边界条件**: 2个测试
- **连接测试**: 2个测试

**总计**: 13个测试

### 预期通过率

- **Planning模式**: 100% (4/4) ✅
- **chat()模式**: 100% (3/3) ✅
- **chat_stream()模式**: 100% (2/2) ✅
- **边界条件**: 100% (2/2) ✅
- **连接测试**: 100% (2/2) ✅

**总体预期**: 100% (13/13) ✅

---

## 🎯 测试输出示例

### 成功示例

```
tests/test_chatgpt_fix_pytest.py::test_chat_mode[一般对话] PASSED        [  7%]
[一般对话] 意图: general, 响应长度: 156字符

tests/test_chatgpt_fix_pytest.py::test_planning_mode[小说大纲规划] PASSED [  38%]
[小说大纲规划] 阶段: 3/3 ✅
  Planning: ✅
  Execution: ✅
  Response: ✅
  任务数: 5个 (预期5+) ✅
  事件统计: {'plan': 1, 'task_start': 5, 'task_done': 5, 'content': 8}

========================= 13 passed in 234.56s =========================
```

### 失败示例

```
tests/test_chatgpt_fix_pytest.py::test_planning_mode[小说大纲规划] FAILED [  38%]

FAILED - AssertionError: 未检测到足够的阶段 (检测到1/3)

========================= 1 failed, 12 passed in 234.56s =========================
```

---

## 🔍 调试技巧

### 只运行失败的测试

```bash
# 第一次运行
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v

# 只重跑失败的测试
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --lf
```

### 在第一个失败时停止

```bash
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v -x
```

### 查看完整的错误堆栈

```bash
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --tb=long
```

### 进入调试模式（pdb）

```bash
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --pdb
```

---

## 📋 常见问题

### Q1: ImportError: cannot import name 'pytest_asyncio'

**解决方案**:
```bash
./venv/Scripts/pip.exe install pytest-asyncio
```

### Q2: 测试超时

**解决方案**:
```bash
# 增加超时时间（默认300秒）
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --timeout=600
```

### Q3: 服务器连接失败

**解决方案**:
1. 确认后端服务正在运行: `http://localhost:8000`
2. 检查防火墙设置
3. 使用 `test_server_connection` 测试连接

### Q4: 登录失败

**解决方案**:
1. 检查账号密码是否正确（test_chatgpt_fix_pytest.py:24-25）
2. 确认账号未被锁定
3. 检查后端日志

---

## 🎓 高级用法

### 生成JSON报告

```bash
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --json-report --json-report-file=report.json
```

### 生成JUnit XML报告（用于CI/CD）

```bash
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py -v --junit-xml=junit.xml
```

### 完整的CI/CD命令

```bash
./venv/Scripts/pytest.exe tests/test_chatgpt_fix_pytest.py \
    -v \
    --html=report.html \
    --self-contained-html \
    --junit-xml=junit.xml \
    --cov=app \
    --cov-report=html \
    --reruns 2
```

---

## 📊 Pytest vs 原版测试对比

| 特性 | 原版脚本 | Pytest版本 |
|------|---------|-----------|
| 参数化测试 | ❌ 手动循环 | ✅ @parametrize |
| 测试报告 | ❌ 无 | ✅ HTML/JSON/JUnit |
| 失败重试 | ❌ 无 | ✅ --reruns |
| 并发执行 | ❌ 无 | ✅ -n auto |
| 覆盖率 | ❌ 无 | ✅ --cov |
| CI/CD集成 | ⚠️ 困难 | ✅ 简单 |
| 筛选测试 | ❌ 无 | ✅ -k 关键字 |
| 调试模式 | ❌ 无 | ✅ --pdb |

---

**创建时间**: 2025-11-08
**作者**: Claude
**版本**: 1.0
