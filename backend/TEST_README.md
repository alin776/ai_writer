# AI 改写助手自动化测试

## 📋 功能说明

这个测试脚本会自动测试 AI 改写助手的所有 API 接口：

1. ✅ 用户登录认证
2. ✅ 获取可用模型列表
3. ✅ 智能分析文本质量
4. ✅ 多模型并发改写
5. ✅ 保存改写历史记录
6. ✅ 获取历史记录列表（分页）
7. ✅ 获取会话详情
8. ✅ 删除历史记录

## 🚀 快速开始

### 1. 安装依赖

```bash
cd backend
pip install httpx
```

### 2. 启动后端服务

```bash
# 方式1: 使用 uvicorn
cd backend
python -m uvicorn app.main:app --reload

# 方式2: 使用开发服务器
python -m app.main
```

### 3. 运行测试

```bash
# 使用默认配置
python test_rewrite_arena.py

# 使用自定义配置
API_BASE_URL=http://localhost:8000 python test_rewrite_arena.py
```

## ⚙️ 配置选项

### 环境变量

| 变量名 | 说明 | 默认值 |
|-------|------|--------|
| `API_BASE_URL` | API 服务器地址 | `http://localhost:8000` |
| `TEST_USERNAME` | 测试用户名 | `test@example.com` |
| `TEST_PASSWORD` | 测试密码 | `password123` |

### 示例配置

创建 `.env` 文件：

```bash
API_BASE_URL=http://localhost:8000
TEST_USERNAME=your_username@example.com
TEST_PASSWORD=your_password
```

然后运行：

```bash
# Linux/Mac
export $(cat .env | xargs) && python test_rewrite_arena.py

# Windows (PowerShell)
Get-Content .env | ForEach-Object { $name, $value = $_ -split '=', 2; Set-Item "env:$name" $value }
python test_rewrite_arena.py
```

## 📊 测试输出示例

```
============================================================
AI 改写助手自动化测试
============================================================

测试环境:
  API URL: http://localhost:8000
  用户名: test@example.com
  开始时间: 2025-10-25 22:30:00

▶ 1. 用户登录
✓ 登录成功
  用户名: test@example.com
  Token: eyJhbGciOiJIUzI1NiIs...

▶ 2. 获取可用模型列表
✓ 成功获取 4 个模型
  默认模型: gemini-2.5-pro, gpt-5
  最大模型数: 4
  ✓ Gemini 2.5 Pro - 擅长创意和细节描写
  ✓ GPT-5 - 平衡全能，表现稳定
  ✗ Claude 3 Opus - 擅长深度思考和逻辑
  ✗ GPT-4 Turbo - 快速高效

▶ 3. 智能分析文本
✓ 文本分析完成
  质量评分: 45/100
  推荐模式: expand
  推荐理由: 建议增加细节和情感描写，使画面更生动
  检测问题: 2
  • 描写过于简单 (high)
  • 缺少情感渲染 (medium)

▶ 4. 多模型改写文本
✓ 改写完成，共 2 个结果
  改写模式: expand
  原文: 主角走进房间，看到了桌子上的剑。

  模型 1: gemini-2.5-pro
  改写文本: 主角推开那扇厚重的木门，昏暗的房间中唯有一柄长剑泛着幽冷的寒光...
  字数: 156
  耗时: 2.3s

  模型 2: gpt-5
  改写文本: 房门缓缓开启，主角的视线立刻被桌上那柄寒光闪烁的长剑锁定...
  字数: 142
  耗时: 1.8s

▶ 5. 保存改写历史
✓ 历史记录保存成功
  会话ID: 8a3f7b2c-4d1e-5f6a-7b8c-9d0e1f2a3b4c
  结果数量: 2

... (更多测试输出)

============================================================
测试总结
============================================================
总测试数: 8
通过: 8
失败: 0
============================================================

✅ 所有测试通过！
```

## 🐛 故障排查

### 问题1: 连接失败

```
✗ 登录异常: ConnectError: Connection refused
```

**解决方案:**
- 确认后端服务已启动
- 检查 API_BASE_URL 是否正确
- 检查防火墙设置

### 问题2: 认证失败

```
✗ 登录失败: 401 - Unauthorized
```

**解决方案:**
- 检查用户名和密码是否正确
- 确认用户账号已在数据库中创建
- 检查数据库连接是否正常

### 问题3: 数据库表不存在

```
✗ 保存历史失败: 500 - Internal Server Error
```

**解决方案:**
```bash
cd backend
python -m alembic upgrade head
```

### 问题4: AI 调用失败

```
模型 1: gemini-2.5-pro - 失败
错误: API 请求失败: 401
```

**解决方案:**
- 检查 `.env` 文件中的 `OPENAI_API_KEY`
- 确认 API key 有效且有余额
- 检查网络连接

## 📝 测试说明

### 测试覆盖

- ✅ **功能测试**: 所有 API 接口功能正常
- ✅ **集成测试**: 完整的工作流从分析到保存
- ✅ **性能观察**: 记录改写耗时和响应时间
- ✅ **错误处理**: 测试异常情况和错误响应

### 测试流程

1. **认证阶段**: 用户登录获取 JWT token
2. **准备阶段**: 获取可用模型列表
3. **分析阶段**: AI 智能分析文本质量
4. **改写阶段**: 多模型并发改写文本
5. **保存阶段**: 保存改写结果到数据库
6. **查询阶段**: 测试历史记录查询功能
7. **清理阶段**: 删除测试数据

## 🔧 开发说明

### 添加新测试

在 `RewriteArenaAPITester` 类中添加新方法：

```python
async def test_new_feature(self) -> bool:
    """测试新功能"""
    self.print_step("N. 测试新功能")

    try:
        response = await self.client.get(
            f"{self.base_url}/api/v1/your-endpoint",
            headers=self.get_headers()
        )

        if response.status_code == 200:
            self.print_success("测试成功")
            self.result.add_pass()
            return True
        else:
            error_msg = f"测试失败: {response.status_code}"
            self.print_error(error_msg)
            self.result.add_fail(error_msg)
            return False

    except Exception as e:
        error_msg = f"测试异常: {str(e)}"
        self.print_error(error_msg)
        self.result.add_fail(error_msg)
        return False
```

然后在 `run_all_tests()` 中调用：

```python
await self.test_new_feature()
```

### 自定义输出

可以使用 `Colors` 类自定义输出颜色：

```python
print(f"{Colors.GREEN}成功{Colors.RESET}")
print(f"{Colors.RED}失败{Colors.RESET}")
print(f"{Colors.YELLOW}警告{Colors.RESET}")
print(f"{Colors.BLUE}信息{Colors.RESET}")
```

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！
