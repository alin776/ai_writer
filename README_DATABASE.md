# 数据库管理说明

## 🚀 快速开始（新开发者）

### 方式1：一键初始化脚本（推荐）

```bash
# Windows
cd backend
setup_for_new_dev.bat

# Linux/Mac
cd backend
chmod +x setup_for_new_dev.sh
./setup_for_new_dev.sh
```

### 方式2：手动执行

```bash
cd backend

# 1. 激活虚拟环境（如果使用）
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. 执行数据库迁移
alembic upgrade head

# 3. 验证
alembic current
```

---

## 📋 常用命令

```bash
# 查看当前版本
alembic current

# 升级到最新
alembic upgrade head

# 查看历史
alembic history

# 回滚（慎用）
alembic downgrade -1
```

---

## ⚠️ 常见问题

### Q1: 报错"表已存在"
**原因**：表已通过其他方式创建，但迁移记录未更新

**解决**：
```bash
alembic stamp head
```

### Q2: 数据库连接失败
检查 `.env` 文件中的 `DATABASE_URL`：
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
```

### Q3: 不清楚数据库状态
运行诊断脚本：
```bash
python check_tables.py
```

---

## 📚 详细文档

完整文档请查看：`backend/docs/数据库迁移指南.md`

---

## 🔄 工作流程

### 开发者A（创建新模型）
```bash
1. 修改 models/*.py
2. alembic revision --autogenerate -m "描述"
3. alembic upgrade head
4. git add . && git commit -m "feat: 添加新模型"
5. git push
```

### 开发者B（拉取更新）
```bash
1. git pull
2. alembic upgrade head  # ← 自动同步数据库
3. 完成！
```

---

## 📊 当前数据库版本

**最新版本**: `add_ai_guidelines_001` (2025-10-18)

**包含的表**：
- users（用户）
- works（作品）
- chapters（章节）
- characters（角色）
- locations（地点）
- settings（设定）
- work_guidelines（作品规范）
- ai_guidelines（AI创作规范）✨ 新增
