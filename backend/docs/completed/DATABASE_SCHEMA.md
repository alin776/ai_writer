# 数据库表结构说明

> 本文档详细说明 NovelAIde 项目的数据库表结构

## 📊 数据库概览

- **数据库**: PostgreSQL 15+
- **表数量**: 5 个主表 ⭐️ **更新**
- **ORM**: SQLAlchemy (异步)
- **迁移工具**: Alembic

## 📋 表结构

### 1. users（用户表）

存储用户账号和个人信息。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 用户ID（自动生成） |
| username | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | 用户名 |
| hashed_password | VARCHAR(255) | NOT NULL | 密码哈希值 |
| email | VARCHAR(255) | UNIQUE, INDEX | 邮箱（可选） |
| full_name | VARCHAR(100) | | 真实姓名 |
| avatar | VARCHAR(500) | | 头像URL |
| bio | TEXT | | 个人简介 |
| is_active | BOOLEAN | NOT NULL, DEFAULT true | 是否激活 |
| is_admin | BOOLEAN | NOT NULL, DEFAULT false | 是否管理员 |
| is_verified | BOOLEAN | NOT NULL, DEFAULT false | 是否验证邮箱 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT now() | 更新时间 |
| last_login_at | TIMESTAMP | | 最后登录时间 |

**索引**:
- PRIMARY KEY: id
- UNIQUE INDEX: username
- UNIQUE INDEX: email
- INDEX: username
- INDEX: email

**关系**:
- 一对多关系：一个用户可以有多个作品（works）

---

### 2. works（作品表）

存储小说作品信息。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 作品ID（自动生成） |
| author_id | UUID | FOREIGN KEY, NOT NULL, INDEX | 作者ID（关联users.id） |
| title | VARCHAR(200) | NOT NULL, INDEX | 作品标题 |
| description | TEXT | | 作品简介 |
| cover_image | VARCHAR(500) | | 封面图片URL |
| genre | ENUM | NOT NULL, DEFAULT 'other' | 作品类型 |
| status | ENUM | NOT NULL, DEFAULT 'draft' | 作品状态 |
| total_words | INTEGER | NOT NULL, DEFAULT 0 | 总字数 |
| total_chapters | INTEGER | NOT NULL, DEFAULT 0 | 总章节数 |
| view_count | INTEGER | NOT NULL, DEFAULT 0 | 浏览次数 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT now() | 更新时间 |
| published_at | TIMESTAMP | | 发布时间 |

**枚举类型**:

**genre（作品类型）**:
- `fantasy` - 玄幻
- `urban` - 都市
- `romance` - 言情
- `scifi` - 科幻
- `wuxia` - 武侠
- `game` - 游戏
- `history` - 历史
- `military` - 军事
- `other` - 其他

**status（作品状态）**:
- `draft` - 草稿
- `writing` - 连载中
- `completed` - 已完结
- `abandoned` - 已弃坑

**索引**:
- PRIMARY KEY: id
- INDEX: author_id
- INDEX: title

**外键**:
- author_id → users(id) ON DELETE CASCADE

**关系**:
- 多对一关系：多个作品属于一个作者（author）
- 一对多关系：一个作品有多个章节（chapters）

---

### 3. chapters（章节表）

存储作品的章节内容。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 章节ID（自动生成） |
| work_id | UUID | FOREIGN KEY, NOT NULL, INDEX | 作品ID（关联works.id） |
| title | VARCHAR(200) | NOT NULL | 章节标题 |
| content | TEXT | DEFAULT '' | 章节内容 |
| order | INTEGER | NOT NULL, INDEX | 章节排序 |
| is_published | BOOLEAN | NOT NULL, DEFAULT false | 是否发布 |
| word_count | INTEGER | NOT NULL, DEFAULT 0 | 章节字数 |
| view_count | INTEGER | NOT NULL, DEFAULT 0 | 浏览次数 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT now() | 更新时间 |
| published_at | TIMESTAMP | | 发布时间 |

**索引**:
- PRIMARY KEY: id
- INDEX: work_id
- INDEX: order

**外键**:
- work_id → works(id) ON DELETE CASCADE

**关系**:
- 多对一关系：多个章节属于一个作品（work）

---

### 4. rewrite_sessions（改写会话表）⭐️ **NEW**

存储 AI 改写助手的改写会话记录。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 会话ID（自动生成） |
| user_id | UUID | FOREIGN KEY, NOT NULL, INDEX | 用户ID（关联users.id） |
| original_text | TEXT | NOT NULL | 原文 |
| context_before | TEXT | | 前文上下文 |
| context_after | TEXT | | 后文上下文 |
| mode | VARCHAR(50) | NOT NULL | 改写模式（optimize/expand/compress/custom） |
| custom_requirement | TEXT | | 自定义要求（mode=custom时） |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | 创建时间 |

**索引**:
- PRIMARY KEY: id
- INDEX: user_id
- INDEX: created_at（用于按时间排序）

**外键**:
- user_id → users(id) ON DELETE CASCADE

**关系**:
- 多对一关系：多个会话属于一个用户（user）
- 一对多关系：一个会话有多个改写结果（rewrite_results）

**说明**:
- 记录每次使用 AI 改写助手的会话
- 保存原文、上下文和改写模式
- 支持按用户和时间查询

---

### 5. rewrite_results（改写结果表）⭐️ **NEW**

存储每个模型的改写结果。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 结果ID（自动生成） |
| session_id | UUID | FOREIGN KEY, NOT NULL, INDEX | 会话ID（关联rewrite_sessions.id） |
| model_name | VARCHAR(100) | NOT NULL | 模型名称 |
| rewritten_text | TEXT | NOT NULL | 改写后的文本 |
| word_count | INTEGER | NOT NULL, DEFAULT 0 | 改写后的字数 |
| elapsed_time | FLOAT | NOT NULL | 改写耗时（秒） |
| error | TEXT | | 错误信息（失败时） |
| is_selected | BOOLEAN | NOT NULL, DEFAULT false | 用户是否选中这个结果 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | 创建时间 |

**索引**:
- PRIMARY KEY: id
- INDEX: session_id
- INDEX: created_at

**外键**:
- session_id → rewrite_sessions(id) ON DELETE CASCADE

**关系**:
- 多对一关系：多个结果属于一个会话（session）

**说明**:
- 存储每个 AI 模型的改写结果
- 支持保存多个模型的对比结果
- 记录性能数据（字数、耗时）
- 标记用户最终选择的结果

---

## 🔗 关系图

```
users (1) ──────< (N) works (1) ──────< (N) chapters
  |                    |                      |
  id                   author_id              work_id
                       work.author            chapter.work

users (1) ──────< (N) rewrite_sessions (1) ──────< (N) rewrite_results
  |                          |                              |
  id                         user_id                        session_id
                             session.user                   result.session
```

**说明**:
- 一个用户（User）可以有多个作品（Works）
- 一个作品（Work）属于一个用户（User）
- 一个作品（Work）可以有多个章节（Chapters）
- 一个章节（Chapter）属于一个作品（Work）
- **NEW** 一个用户（User）可以有多个改写会话（RewriteSessions）
- **NEW** 一个改写会话（RewriteSession）属于一个用户（User）
- **NEW** 一个改写会话（RewriteSession）可以有多个改写结果（RewriteResults）
- **NEW** 一个改写结果（RewriteResult）属于一个改写会话（RewriteSession）

**级联删除**:
- 删除用户时，自动删除其所有作品和改写会话
- 删除作品时，自动删除其所有章节
- 删除改写会话时，自动删除其所有改写结果

---

## 🛠️ 数据库初始化

### 方式一：自动创建（推荐）

启动应用时会自动创建所有表：

```python
# 在 app/core/database.py 中
async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

运行 `quick_start.bat` 会自动调用此函数。

### 方式二：使用 Alembic 迁移

```bash
# 升级到最新版本
alembic upgrade head

# 查看当前版本
alembic current

# 查看历史
alembic history
```

### 方式三：手动创建

可以使用 SQL 创建表，但不推荐（ORM 会自动处理）。

---

## 📝 现有迁移记录

1. **initial_migration** (c02326821f1e)
   - 创建初始表结构（users, works, chapters）
   - 日期：2025-10-15 23:03

2. **make_email_optional** (dfef30e5f344)
   - 将 email 字段改为可选
   - 日期：2025-10-16 09:23

3. **add_rewrite_history_tables** (f1g2h3i4j5k6) ⭐️ **NEW**
   - 创建 rewrite_sessions 表
   - 创建 rewrite_results 表
   - 添加外键和索引
   - 日期：2025-10-25 22:00
   - 文件：`backend/alembic/versions/20251025_2200_add_rewrite_history_tables.py`

---

## 💾 数据类型说明

### UUID
- 使用 PostgreSQL 的 UUID 类型
- 自动生成（uuid.uuid4）
- 作为主键和外键
- Python 中使用 `uuid.UUID` 类型

### TIMESTAMP
- 带时区的时间戳
- 默认值：`func.now()`（数据库当前时间）
- 自动更新：`onupdate=func.now()`

### ENUM
- PostgreSQL 原生枚举类型
- Python 中使用 `enum.Enum`
- 类型安全

### VARCHAR vs TEXT
- VARCHAR: 固定最大长度的字符串
- TEXT: 无限长度的文本

---

## 🔍 查询示例

### 查看所有表

```sql
\dt
```

### 查看表结构

```sql
-- 用户表
\d users

-- 作品表
\d works

-- 章节表
\d chapters
```

### 查看索引

```sql
\di
```

### 查看外键

```sql
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```

---

## 📊 数据统计示例

### 用户统计

```sql
-- 总用户数
SELECT COUNT(*) FROM users;

-- 活跃用户数
SELECT COUNT(*) FROM users WHERE is_active = true;

-- 管理员用户
SELECT username, email FROM users WHERE is_admin = true;
```

### 作品统计

```sql
-- 总作品数
SELECT COUNT(*) FROM works;

-- 按类型统计
SELECT genre, COUNT(*) as count 
FROM works 
GROUP BY genre 
ORDER BY count DESC;

-- 按状态统计
SELECT status, COUNT(*) as count 
FROM works 
GROUP BY status;

-- 总字数
SELECT SUM(total_words) as total_words FROM works;
```

### 章节统计

```sql
-- 总章节数
SELECT COUNT(*) FROM chapters;

-- 已发布章节数
SELECT COUNT(*) FROM chapters WHERE is_published = true;

-- 平均章节字数
SELECT AVG(word_count) as avg_word_count FROM chapters;
```

---

## 🔐 权限说明

### 数据库用户权限

数据库用户 `novelaide` 拥有以下权限：
- 对 `novelaide` 数据库的所有权限
- 对 `public` schema 的所有权限
- 可以创建、读取、更新、删除所有表的数据

### 应用层权限

应用通过业务逻辑控制权限：
- 用户只能操作自己的作品和章节
- 管理员可以查看所有数据（未实现）

---

## 🧪 测试数据

### 创建测试用户

```sql
INSERT INTO users (id, username, hashed_password, email, is_active) 
VALUES (
  gen_random_uuid(), 
  'testuser', 
  '$2b$12$...', -- 需要使用 bcrypt 哈希
  'test@example.com', 
  true
);
```

### 创建测试作品

```sql
INSERT INTO works (id, author_id, title, description, genre, status) 
VALUES (
  gen_random_uuid(),
  (SELECT id FROM users WHERE username = 'testuser'),
  '测试小说',
  '这是一部测试小说',
  'fantasy',
  'draft'
);
```

---

## 📚 相关文档

- **POSTGRESQL_SETUP.md** - PostgreSQL 安装指南
- **数据库配置说明.md** - 数据库配置
- **app/models/** - 数据模型定义
- **alembic/** - 数据库迁移文件

---

## 🔄 数据库维护

### 备份数据库

```bash
# 完整备份
pg_dump -U novelaide -d novelaide > backup_$(date +%Y%m%d).sql

# 仅备份数据
pg_dump -U novelaide -d novelaide --data-only > data_backup.sql

# 仅备份结构
pg_dump -U novelaide -d novelaide --schema-only > schema_backup.sql
```

### 恢复数据库

```bash
# 恢复完整备份
psql -U novelaide -d novelaide < backup.sql

# 恢复数据
psql -U novelaide -d novelaide < data_backup.sql
```

### 清空数据

```sql
-- 清空所有表（保留结构）
TRUNCATE TABLE chapters CASCADE;
TRUNCATE TABLE works CASCADE;
TRUNCATE TABLE users CASCADE;
```

### 重建数据库

```bash
# 删除数据库
dropdb -U postgres novelaide

# 重新创建
createdb -U postgres novelaide -O novelaide

# 运行初始化
psql -U postgres -d novelaide -f setup_db.sql
```

---

## 💡 开发建议

1. **使用 ORM**：通过 SQLAlchemy 操作数据库，不要直接写 SQL
2. **使用迁移**：数据库结构变更使用 Alembic 迁移
3. **使用事务**：保证数据一致性
4. **添加索引**：为常用查询字段添加索引
5. **定期备份**：生产环境定期备份数据

---

## 🎯 总结

✅ 数据库表已完整定义
✅ 使用 PostgreSQL 的特性（UUID、ENUM、CASCADE）
✅ 建立了完整的关系模型
✅ 支持自动创建和迁移
✅ 包含必要的索引和约束

数据库已经准备就绪，可以直接使用！🎉
