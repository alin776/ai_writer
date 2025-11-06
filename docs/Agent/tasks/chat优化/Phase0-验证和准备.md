# Phase 0: 验证和准备

**阶段**: Phase 0
**预计时间**: 1天
**状态**: ⏸️ 待开始

---

## 🎯 阶段目标

验证当前系统状态，确保技术基础满足后续开发需求，完成必要的准备工作。

### 核心任务
1. 验证chat_stream()方法功能完整性
2. 检查依赖版本是否满足要求
3. 检查现有API端点和前端支持
4. 创建开发分支和备份配置

---

## 📋 详细任务清单

### 任务1: 验证chat_stream()方法 (2小时)

#### 1.1 代码位置确认
- [ ] 确认方法位置: `backend/app/services/agent/langgraph_agent.py:1836-1953`
- [ ] 确认代码行数: 约118行
- [ ] 确认方法签名完整

**检查命令**:
```bash
# 查看chat_stream方法
cd D:\Java\ai_writer
grep -n "async def chat_stream" backend/app/services/agent/langgraph_agent.py

# 查看方法定义
sed -n '1836,1900p' backend/app/services/agent/langgraph_agent.py
```

#### 1.2 核心功能验证
- [ ] **流式执行**: 验证使用astream()机制
  ```python
  # 应该包含类似代码
  async for event in self.graph.astream(...)
  ```

- [ ] **回调机制**: 验证三个回调函数
  - on_progress: 进度回调
  - on_tool_call: 工具调用回调
  - on_content: 内容生成回调

- [ ] **异常处理**: 验证try-except块
  ```python
  try:
      # 主逻辑
  except Exception as e:
      logger.error(...)
  ```

- [ ] **状态管理**: 验证checkpointer使用
  - AsyncRedisSaver初始化
  - asetup()调用

#### 1.3 功能测试
- [ ] 编写简单测试脚本
  ```python
  # tests/test_chat_stream.py
  async def test_chat_stream_basic():
      agent = LangGraphAgent()

      progress_events = []
      async def on_progress(event):
          progress_events.append(event)

      result = await agent.chat_stream(
          message="测试消息",
          on_progress=on_progress
      )

      assert result is not None
      assert len(progress_events) > 0
  ```

- [ ] 运行测试
  ```bash
  cd backend
  python -m pytest tests/test_chat_stream.py -v
  ```

**验收标准**:
- [ ] chat_stream()方法存在且完整
- [ ] 包含astream()流式执行
- [ ] 三个回调函数都正常工作
- [ ] 异常处理完善
- [ ] 简单测试通过

---

### 任务2: 检查依赖版本 (30分钟)

#### 2.1 检查Python包版本
```bash
cd D:\Java\ai_writer\backend

# 检查核心依赖
pip show langgraph
pip show langchain
pip show langchain-core
pip show langchain-google-genai
```

#### 2.2 版本要求
- [ ] **langgraph**: >= 0.2.0 (必需)
- [ ] **langchain**: >= 0.3.0 (必需)
- [ ] **langchain-core**: >= 0.3.0 (必需)
- [ ] **langchain-google-genai**: 最新稳定版

#### 2.3 版本不满足时的升级
```bash
# 备份当前环境
pip freeze > requirements_backup_$(date +%Y%m%d).txt

# 升级依赖
pip install --upgrade langgraph>=0.2.0
pip install --upgrade langchain>=0.3.0
pip install --upgrade langchain-core>=0.3.0

# 验证升级后的版本
pip show langgraph langchain langchain-core
```

#### 2.4 兼容性测试
- [ ] 运行现有测试套件
  ```bash
  python -m pytest tests/ -v --tb=short
  ```

- [ ] 确认现有功能不受影响
  - Planning模式正常工作
  - ReAct Stream端点正常

**验收标准**:
- [ ] 所有必需依赖版本满足要求
- [ ] 现有测试全部通过
- [ ] 无兼容性问题

---

### 任务3: 检查现有API端点 (1小时)

#### 3.1 检查ReAct Stream端点
- [ ] 确认文件存在: `backend/app/api/v1/agent_react_stream.py`
- [ ] 检查是否使用chat_stream()

```bash
# 查看文件内容
cat backend/app/api/v1/agent_react_stream.py | grep -A 20 "chat_stream"
```

#### 3.2 分析现有实现
- [ ] 记录现有API路由
  - 路径: `/api/v1/agent/react-stream` 或类似
  - 方法: POST
  - 参数: message, work_id, chapter_id等

- [ ] 记录事件格式
  - 使用SSE (Server-Sent Events)
  - 事件类型: progress, tool_call, content等

- [ ] 检查是否可以复用
  - 评估现有代码质量
  - 确定是否需要重构

#### 3.3 检查前端支持
- [ ] 确认前端文件存在
  - `src/hooks/useAgentChatStream.ts`
  - `src/components/agent/AgentStreamDemo.tsx`

- [ ] 检查前端是否支持ReAct事件
  ```bash
  cd src
  grep -r "react-stream" .
  grep -r "useAgentChatStream" .
  ```

**验收标准**:
- [ ] ReAct Stream端点存在
- [ ] 确认是否使用chat_stream()
- [ ] 前端已有基础支持
- [ ] 明确复用或重构策略

---

### 任务4: 准备开发环境 (30分钟)

#### 4.1 创建功能分支
```bash
cd D:\Java\ai_writer

# 确保当前在main分支
git checkout main

# 拉取最新代码
git pull origin main

# 创建功能分支
git checkout -b feature/chat-optimization

# 推送到远程
git push -u origin feature/chat-optimization
```

#### 4.2 备份配置文件
```bash
# 备份配置
cd backend/app
cp -r config config.backup.$(date +%Y%m%d)

# 备份关键文件
cd D:\Java\ai_writer
mkdir -p backups/phase0
cp backend/app/services/agent/langgraph_agent.py backups/phase0/
cp backend/app/api/v1/*.py backups/phase0/
```

#### 4.3 创建工作目录
```bash
# 创建新的配置目录（如果需要）
mkdir -p backend/app/config/chat_modes
mkdir -p backend/app/config/context
mkdir -p backend/app/config/prompts

# 创建Prompt模板目录
mkdir -p backend/app/prompts/templates

# 创建测试目录
mkdir -p backend/tests/integration/chat_optimization
```

**验收标准**:
- [ ] 功能分支创建成功
- [ ] 配置文件已备份
- [ ] 工作目录结构就绪

---

## 📊 验证检查表

### 代码验证
- [ ] chat_stream()方法完整且功能正常
- [ ] astream()流式机制工作
- [ ] 回调函数支持完善
- [ ] 异常处理健壮

### 依赖验证
- [ ] langgraph >= 0.2.0
- [ ] langchain >= 0.3.0
- [ ] langchain-core >= 0.3.0
- [ ] 所有现有测试通过

### 环境验证
- [ ] ReAct Stream端点存在
- [ ] 前端基础支持就绪
- [ ] 功能分支创建
- [ ] 配置文件备份

---

## 🎯 Phase 0完成标准

### 必须完成 ✅
- [ ] chat_stream()方法验证通过
- [ ] 所有依赖版本满足要求
- [ ] 现有功能不受影响
- [ ] 开发环境准备就绪

### 输出产物 📦
- [ ] Phase 0验证报告 (记录所有检查结果)
- [ ] 依赖版本清单
- [ ] 现有API分析文档
- [ ] 配置备份文件

---

## ⏭️ 下一步

**Phase 0完成后**:
1. 召开评审会议
2. 确认是否继续Phase 1
3. 如果通过，开始P1-02: API端点适配

**如果未通过**:
1. 识别阻塞问题
2. 制定解决方案
3. 重新评估时间表

---

## 📝 实施记录

### 检查项记录

#### chat_stream()验证
- **检查时间**: _____
- **方法位置**: _____
- **代码行数**: _____
- **功能完整性**: [ ] 是 [ ] 否
- **问题记录**: _____

#### 依赖版本检查
- **检查时间**: _____
- **langgraph版本**: _____
- **langchain版本**: _____
- **langchain-core版本**: _____
- **是否需要升级**: [ ] 是 [ ] 否
- **升级后测试结果**: _____

#### API端点检查
- **检查时间**: _____
- **ReAct Stream端点**: [ ] 存在 [ ] 不存在
- **是否使用chat_stream()**: [ ] 是 [ ] 否
- **前端支持情况**: _____
- **复用策略**: _____

### 决策记录
- **决策时间**: _____
- **是否继续Phase 1**: [ ] 是 [ ] 否
- **决策理由**: _____
- **特殊注意事项**: _____

---

**负责人**: _____
**开始时间**: _____
**完成时间**: _____
**状态**: ⏸️ 待开始 → 🔄 进行中 → ✅ 已完成
