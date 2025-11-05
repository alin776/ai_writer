# WSL中安装Redis Stack完整指南

## 环境说明
- **系统**: Windows 10/11 + WSL2 (Ubuntu 24.04)
- **Redis版本**: Redis Stack (包含RedisJSON + RediSearch)
- **部署方式**: Docker容器

---

## 零、安装WSL（Windows Subsystem for Linux）

### 0.1 检查Windows版本
- **Windows 10**: 需要版本 2004 及更高版本（内部版本 19041 及更高版本）
- **Windows 11**: 所有版本均支持

### 0.2 启用WSL功能
打开 **PowerShell（管理员）**，执行：

```powershell
# 一键安装WSL2 + Ubuntu（推荐，Windows 10 2004+）
wsl --install
```

**该命令会自动完成：**
1. 启用"适用于 Linux 的 Windows 子系统"功能
2. 启用"虚拟机平台"功能
3. 下载并安装 WSL2 Linux 内核
4. 设置 WSL2 为默认版本
5. 安装 Ubuntu 发行版

### 0.3 重启计算机
**必须重启才能完成安装！**

```powershell
# 执行后重启
Restart-Computer
```

### 0.4 设置Ubuntu用户名和密码
重启后，Ubuntu会自动启动，按提示设置：
```
Enter new UNIX username: your_username
New password: ********
Retype new password: ********
```

### 0.5 验证WSL安装
在PowerShell中执行：
```powershell
# 查看WSL版本
wsl --version

# 查看已安装的Linux发行版
wsl -l -v

# 预期输出：
#   NAME      STATE           VERSION
# * Ubuntu    Running         2
```

### 0.6 进入WSL
```powershell
# 方法1: 在PowerShell中执行
wsl

# 方法2: 在开始菜单搜索"Ubuntu"并打开
```

---

## 一、在WSL中安装Docker

### 1.1 更新系统包
在WSL终端中执行：
```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2 安装Docker依赖
```bash
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

### 1.3 添加Docker官方GPG密钥
```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

### 1.4 配置Docker APT源
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 1.5 安装Docker Engine
```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 1.6 启动Docker服务
```bash
sudo service docker start
```

### 1.7 验证Docker安装
```bash
sudo docker --version
# 输出: Docker version 27.x.x, build xxxxx

sudo docker run hello-world
# 输出: Hello from Docker! ...
```

### 1.8 配置Docker权限（可选，避免每次使用sudo）
```bash
# 将当前用户添加到docker组
sudo usermod -aG docker $USER

# 重新加载用户组（或重新登录WSL）
newgrp docker

# 验证（不需要sudo）
docker --version
```

---

## 二、配置Docker国内镜像源（中国大陆用户）

### 2.1 创建Docker配置目录
```bash
sudo mkdir -p /etc/docker
```

### 2.2 编辑配置文件
```bash
sudo nano /etc/docker/daemon.json
```

### 2.3 写入镜像源配置
复制以下内容到文件中：
```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.nju.edu.cn"
  ]
}
```

**保存方式**:
- 按 `Ctrl + O` 保存
- 按 `Enter` 确认
- 按 `Ctrl + X` 退出

### 2.4 重启Docker服务
```bash
sudo service docker restart
```

### 2.5 验证镜像源配置
```bash
sudo docker info | grep -A 5 "Registry Mirrors"
# 输出:
#  Registry Mirrors:
#   https://docker.m.daocloud.io/
#   https://docker.nju.edu.cn/
```

---

## 三、拉取Redis Stack镜像

### 3.1 拉取最新版镜像
```bash
sudo docker pull redis/redis-stack:latest
```

**输出示例**:
```
latest: Pulling from redis/redis-stack
a2abf6c4d29d: Pull complete
...
Status: Downloaded newer image for redis/redis-stack:latest
```

### 3.2 验证镜像下载成功
```bash
sudo docker images | grep redis-stack

# 输出:
# redis/redis-stack   latest    abc123def456   2 weeks ago   500MB
```

---

## 四、运行Redis Stack容器

### 4.1 基础运行（开发环境）
```bash
sudo docker run -d \
  --name redis-stack \
  -p 127.0.0.1:6379:6379 \
  -p 127.0.0.1:8001:8001 \
  --restart unless-stopped \
  redis/redis-stack:latest
```

**参数说明**:
- `-d`: 后台运行
- `--name redis-stack`: 容器名称
- `-p 127.0.0.1:6379:6379`: Redis端口（仅本地访问）
- `-p 127.0.0.1:8001:8001`: RedisInsight管理界面端口
- `--restart unless-stopped`: 自动重启策略（Docker启动时自动启动容器）

### 4.2 生产环境运行（带数据持久化和密码）
```bash
# 创建数据持久化目录
mkdir -p ~/redis-data

# 运行容器
sudo docker run -d \
  --name redis-stack \
  -p 127.0.0.1:6379:6379 \
  -p 127.0.0.1:8001:8001 \
  -v ~/redis-data:/data \
  -e REDIS_ARGS="--requirepass your_strong_password --save 60 1000" \
  --restart unless-stopped \
  redis/redis-stack:latest
```

**新增参数说明**:
- `-v ~/redis-data:/data`: 挂载数据卷（持久化到宿主机）
- `-e REDIS_ARGS="..."`: 传递Redis配置参数
  - `--requirepass your_strong_password`: 设置Redis密码
  - `--save 60 1000`: 每60秒内有1000次写入时保存快照

### 4.3 验证容器运行状态
```bash
sudo docker ps

# 输出:
# CONTAINER ID   IMAGE                     STATUS        PORTS
# abc123def456   redis/redis-stack:latest  Up 2 minutes  127.0.0.1:6379->6379/tcp, 127.0.0.1:8001->8001/tcp
```

### 4.4 验证Redis模块
```bash
sudo docker exec redis-stack redis-cli MODULE LIST
```

**预期输出**:
```
1) 1) "name"
   2) "ReJSON"
   3) "ver"
   4) 999999
2) 1) "name"
   2) "search"
   3) "ver"
   4) 20812
```

### 4.5 测试Redis连接
```bash
# 无密码连接
sudo docker exec redis-stack redis-cli PING
# 输出: PONG

# 有密码连接
sudo docker exec redis-stack redis-cli -a your_strong_password PING
# 输出: PONG
```

---

## 五、Redis配置详解

### 5.1 连接配置

**无密码连接（开发环境）**:
```bash
# 命令行连接
sudo docker exec -it redis-stack redis-cli

# Python连接
redis_url = "redis://localhost:6379/0"
```

**有密码连接（生产环境）**:
```bash
# 命令行连接
sudo docker exec -it redis-stack redis-cli -a your_strong_password

# Python连接
redis_url = "redis://:your_strong_password@localhost:6379/0"
```

### 5.2 持久化配置

Redis Stack支持两种持久化方式：

**RDB快照（已配置 `--save 60 1000`）**:
```bash
# 手动触发快照
sudo docker exec redis-stack redis-cli BGSAVE

# 查看上次快照时间
sudo docker exec redis-stack redis-cli LASTSAVE
```

**AOF持久化（可选，更安全但性能稍低）**:
```bash
# 运行容器时添加AOF配置
sudo docker run -d \
  --name redis-stack \
  -v ~/redis-data:/data \
  -e REDIS_ARGS="--appendonly yes --appendfsync everysec" \
  redis/redis-stack:latest
```

### 5.3 内存限制配置
```bash
# 限制最大内存为2GB，超出后使用LRU淘汰策略
sudo docker run -d \
  --name redis-stack \
  -e REDIS_ARGS="--maxmemory 2gb --maxmemory-policy allkeys-lru" \
  redis/redis-stack:latest
```

### 5.4 数据库选择
Redis默认有16个数据库（db0 - db15）

**重要限制**: RediSearch索引只能在db0创建！

```bash
# 切换到db0（推荐用于LangGraph AsyncRedisSaver）
SELECT 0

# 切换到db3（其他用途）
SELECT 3
```

---

## 六、项目集成配置

### 6.1 Python连接配置（AsyncRedisSaver）

**文件**: `backend/app/services/agent/langgraph_agent.py`

```python
from langgraph.checkpoint.redis import AsyncRedisSaver

# Redis连接URL（必须使用db0，RediSearch索引限制）
redis_url = "redis://localhost:6379/0"  # 无密码
# redis_url = "redis://:your_password@localhost:6379/0"  # 有密码

# 配置TTL自动清理（7天）
ttl_config = {
    "default_ttl": 10080,       # 7天 = 7×24×60分钟
    "refresh_on_read": True     # 活跃对话自动续期
}

# 创建AsyncRedisSaver
checkpointer = AsyncRedisSaver(redis_url=redis_url, ttl=ttl_config)

# 初始化索引（必须在async函数中调用）
await checkpointer.asetup()
```

### 6.2 环境变量配置

**文件**: `backend/.env`

```env
# 无密码
REDIS_URL=redis://localhost:6379/0

# 有密码
# REDIS_URL=redis://:your_strong_password@localhost:6379/0
```

### 6.3 访问RedisInsight管理界面
在Windows浏览器中打开：
```
http://localhost:8001
```

**功能**:
- 可视化查看所有键值
- 执行Redis命令
- 监控性能指标
- 查看模块状态

---

## 七、常用Docker命令

### 7.1 容器管理
```bash
# 查看所有容器（运行中+停止）
sudo docker ps -a

# 查看运行中容器
sudo docker ps

# 启动容器
sudo docker start redis-stack

# 停止容器
sudo docker stop redis-stack

# 重启容器
sudo docker restart redis-stack

# 删除容器（需先停止）
sudo docker stop redis-stack
sudo docker rm redis-stack

# 查看容器日志
sudo docker logs redis-stack

# 实时查看日志
sudo docker logs -f redis-stack

# 查看容器资源使用
sudo docker stats redis-stack
```

### 7.2 进入容器
```bash
# 进入容器bash
sudo docker exec -it redis-stack bash

# 直接执行redis-cli
sudo docker exec -it redis-stack redis-cli

# 执行单条Redis命令
sudo docker exec redis-stack redis-cli KEYS "*"
```

---

## 八、常用Redis命令

### 8.1 Redis基础操作
```bash
# 进入Redis CLI
sudo docker exec -it redis-stack redis-cli

# 查看Redis信息
INFO

# 查看所有配置
CONFIG GET *

# 查看特定配置
CONFIG GET maxmemory
CONFIG GET requirepass

# 查看数据库大小
DBSIZE

# 查看所有键（谨慎使用，键多时很慢）
KEYS *

# 扫描键（推荐，不阻塞）
SCAN 0 MATCH checkpoint:* COUNT 100

# 查看键的过期时间（秒）
TTL key_name

# 设置键的过期时间（秒）
EXPIRE key_name 3600

# 删除键
DEL key_name

# 清空当前数据库
FLUSHDB

# 清空所有数据库
FLUSHALL
```

### 8.2 数据库切换
```bash
# 切换到db0
SELECT 0

# 切换到db3
SELECT 3

# 查看当前数据库
CLIENT LIST
```

### 8.3 RedisJSON操作
```bash
# 设置JSON数据
JSON.SET user:1 $ '{"name":"张三","age":25}'

# 获取JSON数据
JSON.GET user:1

# 获取JSON字段
JSON.GET user:1 $.name

# 修改JSON字段
JSON.SET user:1 $.age 26

# 删除JSON字段
JSON.DEL user:1 $.age

# 查看JSON类型
JSON.TYPE user:1
```

### 8.4 RediSearch操作
```bash
# 查看所有索引
FT._LIST

# 查看索引信息
FT.INFO checkpoint_writes

# 搜索示例
FT.SEARCH checkpoint_writes "*"

# 删除索引（不删除数据）
FT.DROPINDEX checkpoint_writes

# 删除索引并删除数据
FT.DROPINDEX checkpoint_writes DD
```

---

## 九、监控与维护

### 9.1 查看checkpoint数据量
```bash
sudo docker exec redis-stack redis-cli --scan --pattern "checkpoint:*" | wc -l
```

### 9.2 查看内存使用
```bash
sudo docker exec redis-stack redis-cli INFO memory | grep used_memory_human
```

### 9.3 查看键的TTL分布
```bash
# 查看特定会话的TTL
sudo docker exec redis-stack redis-cli TTL "checkpoint:test_session:..."
```

### 9.4 手动清理过期数据
```bash
# Redis会自动清理过期键，但可以手动触发
sudo docker exec redis-stack redis-cli --scan --pattern "checkpoint:*" | \
while read key; do
    ttl=$(sudo docker exec redis-stack redis-cli TTL "$key")
    if [ "$ttl" -eq -1 ]; then
        echo "发现未设置TTL的键: $key"
    fi
done
```

### 9.5 性能监控
```bash
# 实时监控Redis操作
sudo docker exec redis-stack redis-cli MONITOR

# 查看慢查询日志
sudo docker exec redis-stack redis-cli SLOWLOG GET 10
```

---

## 十、数据备份与恢复

### 10.1 备份数据
```bash
# 创建RDB快照
sudo docker exec redis-stack redis-cli BGSAVE

# 查看快照状态
sudo docker exec redis-stack redis-cli LASTSAVE

# 复制快照文件到宿主机
mkdir -p ~/backup
sudo docker cp redis-stack:/data/dump.rdb ~/backup/dump_$(date +%Y%m%d).rdb
```

### 10.2 恢复数据
```bash
# 停止容器
sudo docker stop redis-stack

# 复制快照到容器数据目录
sudo docker cp ~/backup/dump_20250105.rdb redis-stack:/data/dump.rdb

# 启动容器
sudo docker start redis-stack
```

### 10.3 定期备份脚本
创建文件 `~/backup_redis.sh`:
```bash
#!/bin/bash
# Redis自动备份脚本

BACKUP_DIR=~/backup/redis
mkdir -p $BACKUP_DIR

# 触发快照
sudo docker exec redis-stack redis-cli BGSAVE

# 等待快照完成
sleep 5

# 复制快照
sudo docker cp redis-stack:/data/dump.rdb $BACKUP_DIR/dump_$(date +%Y%m%d_%H%M%S).rdb

# 删除7天前的备份
find $BACKUP_DIR -name "dump_*.rdb" -mtime +7 -delete

echo "备份完成: $BACKUP_DIR"
```

**设置定时备份（每天凌晨3点）**:
```bash
# 添加执行权限
chmod +x ~/backup_redis.sh

# 编辑crontab
crontab -e

# 添加以下行
0 3 * * * ~/backup_redis.sh >> ~/backup/redis_backup.log 2>&1
```

---

## 十一、故障排查

### 11.1 Redis连接失败
```bash
# 检查容器状态
sudo docker ps -a | grep redis-stack

# 检查容器日志
sudo docker logs redis-stack

# 检查端口占用
sudo netstat -tulnp | grep 6379

# 测试连接
sudo docker exec redis-stack redis-cli PING
```

### 11.2 索引创建失败
**错误**: `Cannot create index on db != 0`

**解决**: RediSearch索引只能在db0创建，必须使用:
```python
redis_url = "redis://localhost:6379/0"  # 必须是/0
```

### 11.3 JSON.SET失败
**错误**: `Command # 1 (JSON.SET ...) of pipeline caused error`

**解决**: 确认RedisJSON模块已加载
```bash
sudo docker exec redis-stack redis-cli MODULE LIST | grep -i json
```

### 11.4 Docker服务未启动
**错误**: `Cannot connect to the Docker daemon`

**解决**:
```bash
# 启动Docker服务
sudo service docker start

# 检查Docker状态
sudo service docker status
```

### 11.5 WSL中Docker权限问题
**错误**: `permission denied while trying to connect to the Docker daemon socket`

**解决**:
```bash
# 方案1: 使用sudo
sudo docker ps

# 方案2: 添加当前用户到docker组
sudo usermod -aG docker $USER
newgrp docker
```

---

## 十二、开机自动启动配置

### 12.1 Docker自动启动（推荐）
编辑 `~/.bashrc`:
```bash
nano ~/.bashrc
```

添加以下内容到文件末尾:
```bash
# 自动启动Docker服务
if ! service docker status > /dev/null 2>&1; then
    sudo service docker start > /dev/null 2>&1
fi
```

配置sudo免密启动Docker:
```bash
# 编辑sudoers
sudo visudo

# 添加以下行（替换your_username为你的用户名）
your_username ALL=(ALL) NOPASSWD: /usr/sbin/service docker start
```

### 12.2 Windows启动时自动启动WSL和Docker
创建文件 `C:\Users\你的用户名\start_wsl_docker.bat`:
```bat
@echo off
wsl -e bash -c "sudo service docker start"
```

**设置开机启动**:
1. 按 `Win + R`，输入 `shell:startup`
2. 将 `start_wsl_docker.bat` 快捷方式放入启动文件夹

---

## 十三、卸载Redis Stack

### 13.1 完整卸载步骤
```bash
# 1. 停止容器
sudo docker stop redis-stack

# 2. 删除容器
sudo docker rm redis-stack

# 3. 删除镜像
sudo docker rmi redis/redis-stack:latest

# 4. 删除数据（谨慎！）
rm -rf ~/redis-data

# 5. 删除备份（可选）
rm -rf ~/backup/redis
```

### 13.2 仅清空数据（保留容器）
```bash
# 进入Redis CLI
sudo docker exec -it redis-stack redis-cli

# 清空所有数据库
FLUSHALL

# 或清空当前数据库
FLUSHDB
```

---

## 附录：Redis Stack特性对比

| 模块 | 功能 | 适用场景 | 性能影响 |
|------|------|----------|---------|
| **RedisJSON** | 原生JSON数据类型 | 复杂对象存储、嵌套数据 | 低 |
| **RediSearch** | 全文搜索+索引 | 文本搜索、范围查询、聚合 | 中（需要db0） |
| **RedisGraph** | 图数据库 | 社交网络、知识图谱 | 高 |
| **RedisTimeSeries** | 时序数据 | 监控指标、IoT数据 | 低 |
| **RedisBloom** | 概率数据结构 | 去重、缓存判断 | 极低 |

---

## 参考文档

- [WSL官方文档](https://docs.microsoft.com/zh-cn/windows/wsl/)
- [Docker官方文档](https://docs.docker.com/)
- [Redis Stack官方文档](https://redis.io/docs/stack/)
- [LangGraph AsyncRedisSaver文档](https://langchain-ai.github.io/langgraph/reference/checkpoints/#langgraph.checkpoint.redis.AsyncRedisSaver)

---

**文档版本**: v2.0
**最后更新**: 2025-01-05
**适用环境**: Windows 10/11 + WSL2 + Ubuntu 24.04
