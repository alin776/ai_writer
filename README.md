# 文枢AI —— 智能小说创作平台

**文枢AI** 是一个面向网文作者的 AI 驱动创作平台，集智能写作辅助、世界观构建、社区互动于一体，帮助作者更高效地完成从构思到成稿的全流程。

## 演示与体验

- **视频介绍**：[市场上AI写作工具这么多，为什么我只推荐文枢AI？](https://www.bilibili.com/video/BV1xCXwBjEnL?vd_source=781968bc261a09d62bcfb19c6dbd5102)
- **在线体验**（需注册）：[https://wenshuai.online](https://wenshuai.online/register?code=BJ7X9ZCP)

## 核心功能

### AI 写作助手
- 基于 DeepAgents 框架的多轮对话写作代理，支持 SSE 实时流式输出
- **25+ 专业写作技能**，覆盖故事诊断、角色塑造、结构设计、写作技法、世界构建等 7 大类别
- 内置 RAG 语义检索，自动关联作品上下文，生成更连贯的内容

### 小说管理
- 作品与章节的完整 CRUD 管理
- 富文本编辑器（Lexical / Milkdown）
- 章节导入导出、批量操作

### 世界观构建
- 可视化知识图谱（角色关系、势力分布、时间线）
- 世界设定的语义向量分析与一致性检查
- 术语表与世界规则库

### 社区与频道
- 粉丝频道系统：实时消息（WebSocket）、表情反应、消息转发与置顶
- 好友系统、评论互动、活动动态
- 作品广场与个人书架

### 积分与任务
- 每日/每周任务奖励积分
- 积分兑换 AI 服务额度
- 邀请码系统与邀请奖励

### 管理后台
- 用户管理、作品审核、频道管理
- API 调用成本追踪与数据分析面板

## 技术栈

| 层级 | 技术 |
|------|------|
| **前端** | React 19 + TypeScript、Vite、Tailwind CSS、Radix UI、Zustand、React Query |
| **后端** | FastAPI（Python）、SQLAlchemy 2.0、Uvicorn |
| **数据库** | PostgreSQL + pgvector（向量检索） |
| **缓存/队列** | Redis Stack、Celery |
| **AI/LLM** | DeepAgents、LangChain、OpenAI / Gemini / Anthropic 多模型支持 |
| **部署** | Docker Compose、Nginx 反向代理 |

## 项目结构

```
ai_writer/
├── src/                # 前端源码（React）
│   ├── components/     # 通用组件
│   ├── pages/          # 页面
│   ├── stores/         # Zustand 状态管理
│   ├── services/       # API 调用层
│   └── router/         # 路由配置
├── backend/            # 后端源码（FastAPI）
│   ├── app/            # 应用主目录
│   │   ├── api/        # API 路由
│   │   ├── models/     # 数据库模型（57 个实体）
│   │   ├── services/   # 业务逻辑
│   │   └── core/       # 核心配置与中间件
│   └── alembic/        # 数据库迁移
├── config/             # 配置文件
├── docker-compose.prod.yml
└── nginx.conf
```

## 快速开始

### 环境要求
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+（需安装 pgvector 扩展）
- Redis

### 前端

```bash
npm install
npm run dev
```

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker 部署

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 许可证

本项目仅供学习和参考，未经授权不得用于商业用途。
