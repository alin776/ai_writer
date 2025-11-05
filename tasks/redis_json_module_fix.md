# Redis JSON 模块缺失问题修复

## 问题分析

错误信息：
```
unknown command `JSON.SET`
```

**原因**: AsyncRedisSaver 需要 RedisJSON 模块，但当前连接的 Redis 实例不支持该模块。

## 待办任务

- [x] 验证 WSL Redis Stack 是否正在运行
- [x] 检查 Redis Stack 是否加载了 RedisJSON 模块
- [x] 停止 Windows Redis，启动 Redis Stack
- [x] 验证 JSON.SET 命令功能

## 解决方案

### 1. 检查 Redis Stack 状态（WSL）

```bash
# 在 WSL 中执行
docker ps | grep redis
redis-cli ping
redis-cli MODULE LIST
```

### 2. 验证 RedisJSON 模块

```bash
# 应该看到类似输出：
# 1) 1) "name"
#    2) "ReJSON"
#    3) "ver"
#    4) ...
```

### 3. 检查应用配置

查看 `.env` 或配置文件中的 Redis URL，确保连接到 localhost:6379（Redis Stack）

## 审查

### 问题根因

1. **Windows Redis 占用端口**: Windows 上运行的 `redis-server.exe`（PID 8508）占用了 6379 端口
2. **缺少 RedisJSON 模块**: Windows Redis 没有加载任何模块，不支持 `JSON.SET` 命令
3. **Redis Stack 未运行**: WSL Docker 中的 Redis Stack 处于 Exited 状态

### 解决步骤

1. **停止 Windows Redis**:
   ```powershell
   Stop-Process -Id 8508 -Force
   ```

2. **启动 Redis Stack**:
   ```bash
   docker start redis-stack
   ```

3. **验证模块加载**:
   - ✓ ReJSON（支持 JSON.SET）
   - ✓ search（RediSearch）
   - ✓ timeseries
   - ✓ redisgears_2
   - ✓ bf（Bloom filter）

4. **测试 JSON.SET**:
   ```python
   JSON.SET test:key $ '{"status": "ok"}'  # 成功！
   ```

### 当前状态

- ✓ Redis Stack 正在运行（localhost:6379）
- ✓ RedisJSON 模块已加载
- ✓ JSON.SET 命令测试通过
- ✓ AsyncRedisSaver 现在可以正常工作

### 注意事项

**重要**: 每次重启系统后，需要确保：
1. Windows Redis 不会自动启动
2. 启动 WSL Docker 中的 Redis Stack：
   ```bash
   wsl docker start redis-stack
   ```

### 建议

可以创建启动脚本自动化这个过程：
```bash
# start-redis-stack.bat
@echo off
wsl docker start redis-stack
echo Redis Stack started successfully!
```
