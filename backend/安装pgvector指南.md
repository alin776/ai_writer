# pgvector 扩展安装指南

## ✅ 环境检查结果

- ✅ Git: 2.45.1（已安装）
- ✅ Visual Studio编译工具（已安装）
- ✅ PostgreSQL: 15.14（已安装）
- ✅ pgvector源码：已克隆到 `%TEMP%\pgvector`

---

## 🚀 安装步骤（必须以管理员身份运行）

### 方法1：使用准备好的批处理脚本 ⭐ 推荐

1. **右键点击** `D:\Java\ai_writer\backend\compile_pgvector.bat`

2. **选择"以管理员身份运行"**

3. 等待编译完成（约1-2分钟）

4. 如果看到"安装成功！"，继续下一步

---

### 方法2：手动编译（如果方法1失败）

1. **以管理员身份打开命令提示符**
   - 按 `Win + X`
   - 选择"Windows PowerShell (管理员)"或"命令提示符(管理员)"

2. **执行以下命令**：

```cmd
set "PGROOT=C:\Program Files\PostgreSQL\15"
cd %TEMP%\pgvector
nmake /F Makefile.win
nmake /F Makefile.win install
```

3. 如果看到文件被复制，说明成功

---

## 🔄 重启PostgreSQL服务

### 方法1：使用服务管理器

1. 按 `Win + R`，输入 `services.msc`，回车

2. 找到 `postgresql-x64-15` 服务

3. 右键 → 重新启动

### 方法2：使用命令行（管理员）

```powershell
Restart-Service postgresql-x64-15
```

---

## ✅ 在数据库中启用pgvector扩展

### 步骤1：连接到数据库

打开PowerShell，执行：

```powershell
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -d novelaide
```

如果提示输入密码，输入您的PostgreSQL密码。

### 步骤2：创建扩展

在psql命令行中执行：

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 步骤3：验证安装

```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

如果看到一行结果，说明成功！

输入 `\q` 退出psql。

---

## 🧪 验证项目迁移

回到项目目录，运行数据库迁移：

```powershell
cd D:\Java\ai_writer\backend
.\venv\Scripts\python.exe -m alembic upgrade head
```

如果没有报错，说明pgvector扩展已成功集成！

---

## ❌ 常见问题

### Q1: nmake命令不存在

**原因**: Visual Studio C++编译工具未正确安装

**解决**: 
1. 下载 Visual Studio Build Tools: https://aka.ms/vs/17/release/vs_BuildTools.exe
2. 运行安装，勾选"使用C++的桌面开发"
3. 重启电脑后再试

### Q2: 找不到PostgreSQL目录

**原因**: PostgreSQL版本或路径不匹配

**解决**: 
检查实际安装路径：
```powershell
Get-ChildItem "C:\Program Files\PostgreSQL" | Select-Object Name
```

如果版本不是15，修改脚本中的 `PGROOT` 路径。

### Q3: 权限不足

**原因**: 没有以管理员身份运行

**解决**: 
- 右键批处理文件，选择"以管理员身份运行"
- 或者以管理员打开PowerShell后再运行命令

### Q4: CREATE EXTENSION失败

**原因**: 
- PostgreSQL服务未重启
- 编译的文件未正确安装

**解决**: 
1. 检查文件是否存在：
```powershell
Test-Path "C:\Program Files\PostgreSQL\15\lib\vector.dll"
Test-Path "C:\Program Files\PostgreSQL\15\share\extension\vector.control"
```

2. 如果文件不存在，重新编译安装

3. 重启PostgreSQL服务

---

## 📝 手动清理（可选）

如果需要重新编译，先清理旧文件：

```powershell
cd $env:TEMP
Remove-Item -Recurse -Force pgvector -ErrorAction SilentlyContinue
git clone --branch v0.8.1 https://github.com/pgvector/pgvector.git
```

---

## 📚 参考资源

- pgvector GitHub: https://github.com/pgvector/pgvector
- PostgreSQL扩展文档: https://www.postgresql.org/docs/current/extend-extensions.html

---

## ✅ 完成后的检查清单

- [ ] 编译pgvector成功
- [ ] 安装pgvector到PostgreSQL目录
- [ ] 重启PostgreSQL服务
- [ ] 在数据库中创建vector扩展
- [ ] 验证扩展已安装
- [ ] 运行 `alembic upgrade head` 成功

---

**祝安装顺利！**如有问题，请检查上面的常见问题部分。
