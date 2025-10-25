# 🔧 AI 改写助手故障排查手册

> 本文档记录 AI 改写助手开发过程中遇到的问题和解决方案，帮助快速定位和解决类似问题。

## 📋 目录

- [数据库问题](#数据库问题)
- [SQLAlchemy 异步问题](#sqlalchemy-异步问题)
- [性能优化问题](#性能优化问题)
- [依赖包问题](#依赖包问题)
- [服务启动问题](#服务启动问题)
- [API 测试问题](#api-测试问题)

---

## 数据库问题

### 问题 1：数据库迁移文件内容错误 ⚠️ **严重**

#### 问题描述

**现象**：
- 迁移文件 `20251025_2157_97b2fcd8fdd6_add_rewrite_history_tables.py` 存在
- 执行 `alembic upgrade head` 无错误
- 但数据库中没有 `rewrite_sessions` 和 `rewrite_results` 表

**影响**：
- 所有改写历史相关的 API 都无法使用
- 返回 500 错误：`relation "rewrite_sessions" does not exist`

#### 根本原因

自动生成的迁移文件内容不正确，只包含索引修改，没有 CREATE TABLE 语句：

```python
# ❌ 错误的迁移文件
def upgrade() -> None:
    op.create_index(...)  # 只有索引操作
    op.drop_index(...)

def downgrade() -> None:
    pass
```

正确的迁移文件应该包含：

```python
# ✅ 正确的迁移文件
def upgrade() -> None:
    # 创建表
    op.create_table(
        'rewrite_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        # ... 其他列
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_table('rewrite_results', ...)
    # 创建索引
    op.create_index(...)
```

#### 解决步骤

1. **删除错误的迁移文件**
   ```bash
   rm backend/alembic/versions/20251025_2157_97b2fcd8fdd6_add_rewrite_history_tables.py
   ```

2. **手动创建正确的迁移文件**
   - 文件名：`20251025_2200_add_rewrite_history_tables.py`
   - 包含完整的 CREATE TABLE 语句
   - 包含所有索引和外键

3. **更新数据库版本指针**
   ```bash
   # 修改 alembic_version 表
   psql -U novelaide -d novelaide -c "UPDATE alembic_version SET version_num='f1g2h3i4j5k6';"
   ```

4. **应用迁移**
   ```bash
   cd backend
   alembic upgrade head
   ```

5. **验证表已创建**
   ```bash
   psql -U novelaide -d novelaide -c "\dt"
   # 应该看到 rewrite_sessions 和 rewrite_results 表
   ```

#### 预防措施

- 生成迁移后，**务必检查迁移文件内容**
- 确认包含了所有必要的 CREATE TABLE 语句
- 在测试环境先验证迁移

#### 相关文件

- `backend/alembic/versions/20251025_2200_add_rewrite_history_tables.py`
- `backend/app/models/rewrite_history.py`

---

## SQLAlchemy 异步问题

### 问题 2：MissingGreenlet 错误 ⚠️ **严重**

#### 问题描述

**错误信息**：
```python
sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called;
can't call await_only() here. Was IO attempted in an unexpected place?
```

**错误位置**：
- `backend/app/api/v1/rewrite_history.py:171`
- 在保存改写历史时发生

**影响**：
- 保存改写历史功能完全失效
- API 返回 500 错误

#### 根本原因

在 SQLAlchemy 异步环境中，手动设置关系属性会触发**懒加载（lazy loading）**机制：

```python
# ❌ 错误代码 - 触发懒加载
session.results = result.scalars().all()  # 手动设置关系属性
```

懒加载需要在 greenlet 上下文中运行，但在 FastAPI 的 async/await 中没有这个上下文。

#### 技术细节

**SQLAlchemy 的关系属性默认使用懒加载策略**：
- 当访问 `session.results` 时，如果数据还没加载
- SQLAlchemy 会自动发起数据库查询
- 在异步环境中，这需要 greenlet 支持
- 但 FastAPI 的 async/await 不提供 greenlet

#### 解决方案

**方案 1：使用显式查询，不依赖关系属性** ✅ **推荐**

```python
# ✅ 正确代码
# 查询结果列表（不要手动设置关系属性）
stmt = select(RewriteResult).where(
    RewriteResult.session_id == session.id
).order_by(RewriteResult.created_at)
result = await db.execute(stmt)
results_list = result.scalars().all()

# 转换为响应模型（直接使用查询到的 results_list）
return RewriteSessionResponse(
    ...
    results=[
        RewriteResultResponse(...)
        for r in results_list  # ✅ 使用独立查询的结果
    ]
)
```

**方案 2：使用预加载** ⚠️ **不推荐**

```python
from sqlalchemy.orm import selectinload

stmt = select(RewriteSession).options(
    selectinload(RewriteSession.results)
).where(...)
```

此方案增加复杂度，且不如方案 1 清晰。

#### 修复范围

需要修复 `rewrite_history.py` 中的 4 个函数：

1. **create_rewrite_session** - 创建会话
2. **get_rewrite_sessions** - 获取列表
3. **get_rewrite_session** - 获取详情
4. **delete_rewrite_session** - 删除会话

每个函数都需要：
1. 在函数开始时提取用户信息
2. 使用显式查询获取关系数据
3. 避免在异常处理中访问关系属性

#### 代码模式

**修复模式**：

```python
async def api_function(
    request: ...,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # ✅ 1. 提前提取用户信息
    user_id = current_user.id
    username = getattr(current_user, 'username', str(user_id))

    try:
        # ✅ 2. 使用显式查询
        stmt = select(Model).where(...)
        result = await db.execute(stmt)
        data = result.scalars().all()

        # ✅ 3. 直接使用查询结果
        return Response(items=[item for item in data])

    except Exception as e:
        # ✅ 4. 异常处理中使用提取的变量
        logger.error(f"用户 {username} 操作失败: {str(e)}")
```

#### 验证修复

```bash
# 1. 重启后端服务
python -m uvicorn app.main:app --reload

# 2. 运行测试
python quick_test_save.py
```

预期结果：
```
✓ 保存成功！
  会话ID: [UUID]
  结果数量: 2
```

#### 相关文档

- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Understanding Lazy Loading](https://docs.sqlalchemy.org/en/20/orm/loading_relationships.html)
- `backend/FIX_ASYNC_ISSUE.md` - 详细技术说明

---

### 问题 3：异常处理中访问关系属性

#### 问题描述

**错误信息**：
```python
sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called
```

**错误位置**：异常处理块中访问 `current_user.username`

**代码示例**：
```python
except Exception as e:
    # ❌ 错误 - username 可能触发懒加载
    logger.error(f"用户 {current_user.username} 保存失败: {str(e)}")
```

#### 解决方案

在函数开始时提取所需的用户信息：

```python
async def api_function(...):
    # ✅ 在函数开始时提取
    user_id = current_user.id
    username = getattr(current_user, 'username', str(user_id))

    try:
        # ... 业务逻辑
    except Exception as e:
        # ✅ 使用提取的变量
        logger.error(f"用户 {username}({user_id}) 保存失败: {str(e)}")
```

#### 应用范围

这个模式应用到所有需要记录用户信息的地方：
- 日志记录
- 错误提示
- 审计记录

---

## 性能优化问题

### 问题 4：N+1 查询问题

#### 问题描述

**现象**：
- 获取改写历史列表时，循环查询每个会话的结果数量
- 当历史记录多时，性能明显下降
- 数据库查询次数 = 1 + N（N 为会话数量）

**代码示例**：
```python
# ❌ N+1 查询问题
sessions = await db.execute(select(RewriteSession).where(...))
for session in sessions:
    # 每个会话都执行一次查询！
    count = await db.execute(
        select(func.count()).where(RewriteResult.session_id == session.id)
    )
```

#### 解决方案

使用子查询 + LEFT JOIN，一次查询获取所有数据：

```python
# ✅ 优化后 - 只执行一次查询
# 创建子查询统计每个会话的结果数量
result_count_subq = (
    select(
        RewriteResult.session_id,
        func.count(RewriteResult.id).label('result_count')
    )
    .group_by(RewriteResult.session_id)
    .subquery()
)

# 主查询 LEFT JOIN 子查询
stmt = (
    select(RewriteSession, result_count_subq.c.result_count)
    .outerjoin(
        result_count_subq,
        RewriteSession.id == result_count_subq.c.session_id
    )
    .where(RewriteSession.user_id == user_id)
    .order_by(desc(RewriteSession.created_at))
    .offset(offset)
    .limit(page_size)
)

result = await db.execute(stmt)
rows = result.all()

# 构建响应
for session, result_count in rows:
    items.append(
        RewriteSessionListItem(
            id=str(session.id),
            result_count=result_count or 0,  # 处理 NULL
            ...
        )
    )
```

#### 性能对比

**优化前**：
- 100 个会话 = 101 次查询（1 次主查询 + 100 次计数查询）
- 响应时间：~500ms

**优化后**：
- 100 个会话 = 1 次查询
- 响应时间：~50ms
- **性能提升 10 倍**

#### 相关位置

- `backend/app/api/v1/rewrite_history.py` 的 `get_rewrite_sessions` 函数

---

### 问题 5：低效的计数查询

#### 问题描述

**错误代码**：
```python
# ❌ 加载所有记录再计数
count_result = await db.execute(select(RewriteSession).where(...))
total = len(count_result.scalars().all())  # 低效！
```

**问题**：
- 加载所有记录到内存
- 浪费内存和网络带宽
- 慢！

#### 解决方案

使用数据库层面的 COUNT：

```python
# ✅ 数据库层面计数
count_stmt = select(func.count()).select_from(RewriteSession).where(
    RewriteSession.user_id == user_id
)
count_result = await db.execute(count_stmt)
total = count_result.scalar()  # 快！
```

#### 性能对比

**优化前**：
- 10000 条记录：~2s，内存占用 ~50MB

**优化后**：
- 10000 条记录：~10ms，内存占用 <1KB
- **性能提升 200 倍**

---

## 依赖包问题

### 问题 6：langchain 版本冲突

#### 问题描述

**错误**：
- 安装 `langchain==0.1.5` 导致依赖冲突
- 与项目中的其他包版本不兼容

#### 解决方案

只安装需要的核心包：

```bash
# ❌ 不要安装完整的 langchain
pip uninstall langchain

# ✅ 只安装 langchain-core
pip install langchain-core==0.3.0
```

#### 原因

- `langchain` 是完整包，包含很多不需要的依赖
- `langchain-core` 是核心包，轻量级
- 我们只使用 `PydanticOutputParser`，只需要 core

#### requirements.txt

```txt
langchain-core==0.3.0  # ✅ 只保留这一行
# langchain==0.1.5     # ❌ 删除这一行
```

---

### 问题 7：pydantic 版本不匹配

#### 问题描述

**错误**：
```
ImportError: cannot import name 'BaseModel' from 'pydantic'
```

**原因**：
- alembic 依赖 pydantic 2.x
- 但安装了 pydantic 1.x

#### 解决方案

```bash
# 强制重装正确版本
pip uninstall pydantic pydantic-core
pip install pydantic==2.12.3 pydantic-core==2.41.4
```

---

## 服务启动问题

### 问题 8：代码修改后未生效

#### 问题描述

**现象**：
- 修改了代码
- 测试时仍然出现旧的错误
- 或者新功能没有生效

#### 原因

修改代码后没有重启后端服务。

#### 解决方案

**方法 1：重启服务**（如果服务正在运行）
```bash
# 1. 按 Ctrl+C 停止服务
# 2. 重新启动
python -m uvicorn app.main:app --reload
```

**方法 2：等待自动重载**（如果使用了 --reload）
- 保存文件后
- 等待 2-3 秒
- 查看日志确认重新加载：`Watching for file changes with StatReload`

#### 验证

```bash
# 检查日志，应该看到：
# Application startup complete.
# INFO:     Started server process [PID]
```

---

### 问题 9：端口被占用

#### 问题描述

**错误**：`Address already in use`

**原因**：
- 8000 端口已被其他程序占用
- 或者之前的服务没有正常关闭

#### 解决方案

**方法 A：使用其他端口**
```bash
python -m uvicorn app.main:app --reload --port 8001
```

**方法 B：关闭占用端口的进程**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [进程ID] /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

---

## API 测试问题

### 问题 10：httpx.ReadTimeout

#### 问题描述

**错误**：
```python
httpx.ReadTimeout
```

**现象**：
- 测试脚本调用 API 30 秒后超时
- 没有返回结果

#### 可能原因

1. **后端服务未运行** ✅ **最常见**
   - 解决：启动后端服务

2. **AI API 响应慢**
   - 解决：检查网络连接，增加超时时间

3. **代码有 bug 导致卡住**
   - 解决：查看后端日志，定位问题

4. **API 密钥无效**
   - 解决：检查 `.env` 文件中的配置

#### 排查步骤

1. **检查后端服务**
   ```bash
   # 访问健康检查
   curl http://localhost:8000/
   ```

2. **查看后端日志**
   ```bash
   # 查看终端输出的日志
   ```

3. **检查 API 配置**
   ```bash
   # 查看 .env 文件
   cat backend/.env
   ```

4. **增加超时时间**（临时）
   ```python
   # 修改测试脚本
   client = httpx.AsyncClient(timeout=60.0)  # 增加到 60 秒
   ```

---

### 问题 11：401 Unauthorized

#### 问题描述

**错误**：API 返回 401 状态码

**原因**：
1. 没有登录
2. Token 已过期
3. Token 格式错误

#### 解决方案

```python
# 1. 确保先登录
response = await client.post("/api/v1/auth/login", ...)
token = response.json()["access_token"]

# 2. 正确设置 Header
headers = {
    "Authorization": f"Bearer {token}",  # 注意 Bearer 和空格
    "Content-Type": "application/json"
}

# 3. 使用 Header
response = await client.post("/api/v1/...", headers=headers, ...)
```

---

## 快速参考

### 常见错误速查

| 错误 | 可能原因 | 解决方案 |
|------|---------|---------|
| `relation does not exist` | 表未创建 | 检查并重新运行迁移 |
| `MissingGreenlet` | 异步懒加载 | 使用显式查询 |
| `Connection refused` | 服务未启动 | 启动后端服务 |
| `ReadTimeout` | 请求超时 | 检查服务和网络 |
| `401 Unauthorized` | 未登录或 Token 无效 | 重新登录获取 Token |
| `ModuleNotFoundError` | 虚拟环境未激活 | 激活虚拟环境 |

### 故障排查流程

```
遇到问题
  ↓
查看错误信息
  ↓
在本文档中搜索相关关键词
  ↓
按照解决方案操作
  ↓
验证问题是否解决
  ↓
如果未解决 → 查看后端日志 → 联系开发团队
```

---

## 相关文档

- **TESTING_GUIDE.md** - 完整测试指南
- **API_REFERENCE.md** - API 接口文档
- **DATABASE_SCHEMA.md** - 数据库结构
- **FIX_ASYNC_ISSUE.md** - SQLAlchemy 异步问题详细说明
- **HOW_TO_TEST.md** - 快速测试指南

---

**持续更新中...**

如果遇到新问题，请记录到此文档，帮助他人快速解决！🚀
