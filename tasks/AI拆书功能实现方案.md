# NovelAIde - AI拆书功能实现方案

> 生成时间: 2025-10-27
> 项目: Python/FastAPI 版本
> 基于: Java版参考文档 + 当前项目现状分析

---

## 📋 目录

1. [方案概述](#1-方案概述)
2. [技术架构设计](#2-技术架构设计)
3. [数据模型设计](#3-数据模型设计)
4. [实现步骤与时间表](#4-实现步骤与时间表)
5. [核心代码设计](#5-核心代码设计)
6. [API接口设计](#6-api接口设计)
7. [前端集成方案](#7-前端集成方案)
8. [测试方案](#8-测试方案)

---

## 1. 方案概述

### 1.1 功能定位

**AI拆书功能** = 智能图书分析 + 知识提取 + 自动入库

**核心价值**:
- 📚 自动解析图书内容(支持 .txt, .epub, .pdf)
- 🤖 AI提取核心观点、案例、技巧
- 💾 自动创建知识库条目
- 🔍 向量化存储支持语义搜索
- ✍️ 编辑器中智能引用

### 1.2 与Java参考文档的差异

| 维度 | Java参考版本 | 我们的Python版本 | 原因 |
|------|-------------|-----------------|------|
| **目标对象** | 网文小说(番茄/起点) | 非虚构图书(工具书/教程) | 符合知识库定位 |
| **输出结构** | 11维度树形设定节点 | 平面知识条目 | 简化MVP,快速上线 |
| **策略设计** | 多种策略(番茄/起点) | 通用图书分析策略 | 专注一个场景 |
| **存储方式** | MongoDB树形文档 | PostgreSQL平面表+向量 | 利用现有架构 |
| **实时推送** | SSE事件流 | WebSocket(可选) | 根据需求选择 |

### 1.3 功能边界

**Week 1 MVP范围** (本次实现):
- ✅ 支持 .txt 格式图书上传
- ✅ 逐章AI分析提取知识点
- ✅ 自动创建知识库条目
- ✅ 自动向量化存储
- ✅ 基础进度显示

**Week 2+ 扩展功能** (后续迭代):
- ⏳ 支持 .epub, .pdf 格式
- ⏳ 用户自定义提取规则
- ⏳ 多书对比分析
- ⏳ 知识图谱可视化

---

## 2. 技术架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    前端层 (React)                        │
│  - 图书上传组件 (BookUploadDialog)                       │
│  - 分析进度监控 (AnalysisProgressPanel)                  │
│  - 知识库列表 (KnowledgeLibraryView)                     │
└────────────────────┬────────────────────────────────────┘
                     │ REST API / WebSocket
┌────────────────────┴────────────────────────────────────┐
│                  后端服务层 (FastAPI)                     │
│  ┌────────────────────────────────────────────────┐     │
│  │ BookAnalysisService (核心拆书服务)              │     │
│  │  - parse_book()        解析图书文件             │     │
│  │  - analyze_chapter()   单章分析                 │     │
│  │  - extract_knowledge() 知识提取                 │     │
│  │  - create_items()      批量入库                 │     │
│  └────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────┐     │
│  │ KnowledgeService (现有服务复用)                 │     │
│  │  - create()           创建知识条目               │     │
│  │  - search()           语义搜索                   │     │
│  └────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────┐     │
│  │ VectorStoreService (现有向量服务)               │     │
│  │  - store_embedding()  存储向量                  │     │
│  │  - semantic_search()  相似度查询                │     │
│  └────────────────────────────────────────────────┘     │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────┐
│              数据持久层 (PostgreSQL)                      │
│  - knowledge_items 表 (现有)                             │
│  - book_analysis_jobs 表 (新增)                          │
│  - book_chapters 表 (新增,可选)                          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 技术栈选择

| 组件 | 技术选型 | 理由 |
|------|---------|------|
| **文件解析** | ebooklib (epub), PyPDF2 (pdf) | 成熟可靠 |
| **AI调用** | OpenAI API (现有) | 已集成,稳定 |
| **异步处理** | asyncio + Celery (可选) | 处理长时间任务 |
| **进度监控** | Redis Stream (推荐) 或 WebSocket | 实时性强 |
| **向量化** | sentence-transformers (现有) | 无需改动 |

### 2.3 核心工作流程

```
┌─────────────────────────────────────────────────────────┐
│ 步骤1: 用户上传图书文件                                   │
│  POST /api/v1/books/upload                              │
│  - 文件类型验证 (.txt/.epub/.pdf)                        │
│  - 文件大小限制 (< 50MB)                                 │
│  - 创建分析任务 (book_analysis_jobs表)                   │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ 步骤2: 解析图书结构                                       │
│  BookAnalysisService.parse_book()                       │
│  - .txt: 正则匹配章节标题                                │
│  - .epub: ebooklib提取章节                               │
│  - .pdf: PyPDF2逐页提取                                  │
│  输出: List[ChapterData]                                │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ 步骤3: 逐章AI分析 (异步)                                  │
│  BookAnalysisService.analyze_chapter()                  │
│  - 构建提示词 (见5.2节)                                  │
│  - 调用OpenAI API                                        │
│  - 解析返回的JSON                                        │
│  - 更新进度 (Redis/WebSocket)                            │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ 步骤4: 知识提取与分类                                     │
│  BookAnalysisService.extract_knowledge()                │
│  - 核心观点 → TECHNIQUE                                  │
│  - 实践案例 → REFERENCE                                  │
│  - 建议总结 → TECHNIQUE                                  │
│  - 金句摘录 → REFERENCE                                  │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ 步骤5: 批量创建知识条目                                   │
│  KnowledgeService.create_batch()                        │
│  - 填充 source_type = "BOOK_ANALYSIS"                   │
│  - 填充 source_reference = 章节标题                      │
│  - 自动生成 tags                                         │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ 步骤6: 自动向量化                                         │
│  VectorStoreService.store_embedding()                   │
│  - sentence-transformers生成384维向量                    │
│  - 存储到pgvector                                        │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ 完成: 返回分析结果                                        │
│  - 总知识条目数                                           │
│  - 各类别分布统计                                         │
│  - 跳转到知识库列表                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 数据模型设计

### 3.1 复用现有表: knowledge_items

**字段映射**:
```python
# AI拆书创建的知识条目特征
{
    "id": "uuid-xxx",
    "user_id": "用户ID",
    "title": "核心观点: XXX",  # AI生成的标题
    "content": "详细内容...",   # AI提取的完整内容
    "summary": "一句话总结",    # AI生成的摘要
    "category": "TECHNIQUE",   # 或 REFERENCE
    "tags": ["书名", "章节名", "关键词1", "关键词2"],
    "source_type": "BOOK_ANALYSIS",  # 标识来源
    "source_id": "book_id_xxx",      # 图书ID
    "source_reference": "第3章 项目管理实战",  # 章节信息
    "extra_data": {
        "book_title": "敏捷开发实战",
        "chapter_title": "第3章 项目管理实战",
        "chapter_index": 3,
        "analysis_timestamp": "2025-10-27T10:00:00Z",
        "confidence_score": 0.85,  # AI置信度
        "extraction_type": "core_concept"  # 提取类型
    }
}
```

### 3.2 新增表: book_analysis_jobs

**用途**: 追踪图书分析任务的状态

```sql
CREATE TABLE book_analysis_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- 图书信息
    book_title VARCHAR(500) NOT NULL,
    original_filename VARCHAR(500) NOT NULL,
    file_format VARCHAR(10) NOT NULL,  -- 'txt', 'epub', 'pdf'
    file_size_bytes INTEGER NOT NULL,
    file_hash VARCHAR(64) UNIQUE,  -- SHA256哈希,去重

    -- 任务状态
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- 状态: pending, parsing, analyzing, completed, failed
    progress INTEGER DEFAULT 0,  -- 0-100
    current_step VARCHAR(200),

    -- 分析结果
    total_chapters INTEGER,
    analyzed_chapters INTEGER DEFAULT 0,
    extracted_items_count INTEGER DEFAULT 0,

    -- 错误处理
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,

    -- 元数据
    extra_data JSONB DEFAULT '{}',  -- 灵活扩展

    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_book_analysis_user_status
    ON book_analysis_jobs(user_id, status);
CREATE INDEX idx_book_analysis_created
    ON book_analysis_jobs(created_at DESC);
CREATE INDEX idx_book_analysis_file_hash
    ON book_analysis_jobs(file_hash);
```

### 3.3 可选表: book_chapters (后续扩展)

**用途**: 缓存章节内容,支持重新分析

```sql
CREATE TABLE book_chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES book_analysis_jobs(id) ON DELETE CASCADE,

    chapter_index INTEGER NOT NULL,
    chapter_title VARCHAR(500),
    content TEXT NOT NULL,
    word_count INTEGER,

    -- 分析结果缓存
    analysis_result JSONB,  -- AI返回的原始JSON
    extracted_items UUID[],  -- 关联的knowledge_items ID数组

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    UNIQUE(job_id, chapter_index)
);

CREATE INDEX idx_book_chapters_job ON book_chapters(job_id);
```

---

## 4. 实现步骤与时间表

### 4.1 Day 1-2: 后端核心服务

**任务清单**:
- [x] 创建 `BookAnalysisService` 服务类
- [x] 实现 .txt 文件解析器
- [x] 实现章节标题正则匹配
- [x] 设计AI提示词模板
- [x] 实现单章分析逻辑
- [x] 实现知识提取逻辑
- [x] 创建数据库表 `book_analysis_jobs`
- [x] 编写单元测试

**关键文件**:
```
backend/app/services/book_analysis_service.py  (新建)
backend/app/api/v1/endpoints/books.py          (新建)
backend/app/models/book_analysis.py            (新建)
backend/tests/test_book_analysis.py            (新建)
```

### 4.2 Day 3: API接口开发

**任务清单**:
- [x] POST /api/v1/books/upload - 上传图书
- [x] GET /api/v1/books/jobs/{job_id} - 查询任务状态
- [x] GET /api/v1/books/jobs - 用户任务列表
- [x] POST /api/v1/books/jobs/{job_id}/cancel - 取消任务
- [x] DELETE /api/v1/books/jobs/{job_id} - 删除任务
- [x] 集成到 main.py 路由

### 4.3 Day 4-5: 前端集成

**任务清单**:
- [x] 创建 `BookUploadDialog.tsx` 上传对话框
- [x] 创建 `AnalysisJobList.tsx` 任务列表
- [x] 创建 `AnalysisProgress.tsx` 进度监控
- [x] 集成到知识库页面
- [x] 测试完整流程

**关键文件**:
```
frontend/src/components/knowledge/BookUploadDialog.tsx
frontend/src/components/knowledge/AnalysisJobList.tsx
frontend/src/components/knowledge/AnalysisProgress.tsx
frontend/src/api/bookAnalysis.ts
```

### 4.4 Day 6: 测试与优化

**任务清单**:
- [x] 端到端测试 (上传 → 分析 → 入库)
- [x] 性能测试 (处理500页图书)
- [x] 错误处理测试 (网络中断/API限流)
- [x] 用户体验优化
- [x] 文档编写

---

## 5. 核心代码设计

### 5.1 BookAnalysisService 服务类

```python
# backend/app/services/book_analysis_service.py

import re
import asyncio
from typing import List, Dict, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from app.models.book_analysis import BookAnalysisJob, JobStatus
from app.models.knowledge import KnowledgeItem, KnowledgeCategory
from app.services.knowledge_service import KnowledgeService
from app.services.vector_store_service import VectorStoreService


class ChapterData:
    """章节数据结构"""
    def __init__(self, index: int, title: str, content: str):
        self.index = index
        self.title = title
        self.content = content
        self.word_count = len(content)


class BookAnalysisService:
    """图书分析服务"""

    def __init__(
        self,
        db: AsyncSession,
        knowledge_service: KnowledgeService,
        vector_service: VectorStoreService
    ):
        self.db = db
        self.knowledge_service = knowledge_service
        self.vector_service = vector_service
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    # ========== 文件解析 ==========

    async def parse_txt_book(self, file_path: str) -> List[ChapterData]:
        """解析TXT格式图书"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 章节标题正则表达式 (参考Java版)
        chapter_pattern = re.compile(
            r'^(?:第[一二三四五六七八九十百千万\d]+[章节部]|Chapter\s+\d+|[IVXLCDM]+\.)\s*(.*)$',
            re.MULTILINE | re.IGNORECASE
        )

        chapters = []
        matches = list(chapter_pattern.finditer(content))

        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)

            title = match.group(0).strip()
            chapter_content = content[start:end].strip()

            chapters.append(ChapterData(
                index=i + 1,
                title=title,
                content=chapter_content
            ))

        # 备用策略: 如果没有匹配到章节,按空行分割
        if not chapters:
            parts = re.split(r'\n\s*\n', content)
            chapters = [
                ChapterData(i + 1, f"第{i + 1}部分", part.strip())
                for i, part in enumerate(parts) if part.strip()
            ]

        return chapters

    # ========== AI分析 ==========

    async def analyze_chapter(
        self,
        chapter: ChapterData,
        book_title: str
    ) -> Dict:
        """使用AI分析单个章节"""

        # 限制内容长度避免Token爆炸
        max_length = 3000
        content = chapter.content[:max_length]
        if len(chapter.content) > max_length:
            content += "\n...(内容过长已截断)"

        prompt = self._build_analysis_prompt(
            book_title=book_title,
            chapter_title=chapter.title,
            content=content
        )

        # 调用LLM
        response = await self.llm.ainvoke(prompt)

        # 解析JSON返回
        import json
        result = json.loads(response.content)

        return result

    def _build_analysis_prompt(
        self,
        book_title: str,
        chapter_title: str,
        content: str
    ) -> str:
        """构建分析提示词"""

        template = ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的图书分析助手,擅长从非虚构图书中提取核心知识点。

你的任务是分析给定章节,提取以下内容:
1. **核心观点** (3-5个): 本章的关键思想和理论
2. **实践案例** (2-3个): 具体的应用示例或真实案例
3. **行动建议** (3-5个): 可落地的实践技巧或方法论
4. **金句摘录** (2-3个): 值得收藏的精彩句子

输出格式必须是JSON:
{{
  "core_concepts": [
    {{"title": "观点标题", "content": "详细描述", "tags": ["标签1", "标签2"]}},
    ...
  ],
  "cases": [
    {{"title": "案例标题", "content": "案例详情", "tags": ["标签1"]}},
    ...
  ],
  "action_items": [
    {{"title": "建议标题", "content": "具体步骤", "tags": ["标签1"]}},
    ...
  ],
  "quotes": [
    {{"content": "金句原文", "context": "上下文说明"}},
    ...
  ]
}}

要求:
- 内容必须准确,不得编造
- 标题简洁(≤20字),内容详实(50-200字)
- 标签必须具体且相关
- 如果某个类别没有内容,返回空数组[]"""),
            ("user", """请分析以下章节:

图书名称: {book_title}
章节标题: {chapter_title}

章节内容:
{content}

请按JSON格式返回分析结果。""")
        ])

        return template.format_messages(
            book_title=book_title,
            chapter_title=chapter_title,
            content=content
        )

    # ========== 知识提取 ==========

    async def extract_knowledge_items(
        self,
        analysis_result: Dict,
        job: BookAnalysisJob,
        chapter: ChapterData,
        user_id: UUID
    ) -> List[KnowledgeItem]:
        """从分析结果提取知识条目"""

        items = []

        # 1. 核心观点 → TECHNIQUE
        for concept in analysis_result.get("core_concepts", []):
            item = await self.knowledge_service.create(
                user_id=user_id,
                title=f"💡 {concept['title']}",
                content=concept['content'],
                category=KnowledgeCategory.TECHNIQUE,
                tags=[job.book_title, chapter.title] + concept.get('tags', []),
                source_type="BOOK_ANALYSIS",
                source_id=str(job.id),
                source_reference=f"{job.book_title} - {chapter.title}",
                extra_data={
                    "book_title": job.book_title,
                    "chapter_title": chapter.title,
                    "chapter_index": chapter.index,
                    "extraction_type": "core_concept"
                }
            )
            items.append(item)

        # 2. 实践案例 → REFERENCE
        for case in analysis_result.get("cases", []):
            item = await self.knowledge_service.create(
                user_id=user_id,
                title=f"📚 {case['title']}",
                content=case['content'],
                category=KnowledgeCategory.REFERENCE,
                tags=[job.book_title, chapter.title] + case.get('tags', []),
                source_type="BOOK_ANALYSIS",
                source_id=str(job.id),
                source_reference=f"{job.book_title} - {chapter.title}",
                extra_data={
                    "book_title": job.book_title,
                    "chapter_title": chapter.title,
                    "chapter_index": chapter.index,
                    "extraction_type": "case_study"
                }
            )
            items.append(item)

        # 3. 行动建议 → TECHNIQUE
        for action in analysis_result.get("action_items", []):
            item = await self.knowledge_service.create(
                user_id=user_id,
                title=f"✅ {action['title']}",
                content=action['content'],
                category=KnowledgeCategory.TECHNIQUE,
                tags=[job.book_title, chapter.title] + action.get('tags', []),
                source_type="BOOK_ANALYSIS",
                source_id=str(job.id),
                source_reference=f"{job.book_title} - {chapter.title}",
                extra_data={
                    "book_title": job.book_title,
                    "chapter_title": chapter.title,
                    "chapter_index": chapter.index,
                    "extraction_type": "action_item"
                }
            )
            items.append(item)

        # 4. 金句摘录 → REFERENCE
        for quote in analysis_result.get("quotes", []):
            item = await self.knowledge_service.create(
                user_id=user_id,
                title=f"💬 {quote['content'][:30]}...",
                content=f"{quote['content']}\n\n上下文: {quote.get('context', '')}",
                category=KnowledgeCategory.REFERENCE,
                tags=[job.book_title, chapter.title, "金句"],
                source_type="BOOK_ANALYSIS",
                source_id=str(job.id),
                source_reference=f"{job.book_title} - {chapter.title}",
                extra_data={
                    "book_title": job.book_title,
                    "chapter_title": chapter.title,
                    "chapter_index": chapter.index,
                    "extraction_type": "quote"
                }
            )
            items.append(item)

        return items

    # ========== 完整流程 ==========

    async def analyze_book(
        self,
        job_id: UUID,
        file_path: str,
        user_id: UUID
    ):
        """完整的图书分析流程 (异步任务)"""

        # 1. 获取任务
        job = await self.db.get(BookAnalysisJob, job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")

        try:
            # 2. 更新状态为解析中
            job.status = JobStatus.PARSING
            job.current_step = "正在解析图书结构..."
            await self.db.commit()

            # 3. 解析图书
            chapters = await self.parse_txt_book(file_path)
            job.total_chapters = len(chapters)
            job.current_step = f"已识别 {len(chapters)} 个章节"
            await self.db.commit()

            # 4. 更新状态为分析中
            job.status = JobStatus.ANALYZING
            await self.db.commit()

            # 5. 逐章分析
            total_items = 0
            for chapter in chapters:
                job.current_step = f"正在分析: {chapter.title}"
                await self.db.commit()

                # AI分析
                analysis_result = await self.analyze_chapter(
                    chapter=chapter,
                    book_title=job.book_title
                )

                # 提取知识条目
                items = await self.extract_knowledge_items(
                    analysis_result=analysis_result,
                    job=job,
                    chapter=chapter,
                    user_id=user_id
                )

                # 更新进度
                job.analyzed_chapters += 1
                job.extracted_items_count += len(items)
                job.progress = int((job.analyzed_chapters / job.total_chapters) * 100)
                await self.db.commit()

                total_items += len(items)

                # 避免API限流
                await asyncio.sleep(1)

            # 6. 完成
            job.status = JobStatus.COMPLETED
            job.current_step = f"分析完成! 共提取 {total_items} 个知识点"
            job.progress = 100
            job.completed_at = datetime.utcnow()
            await self.db.commit()

        except Exception as e:
            # 错误处理
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.retry_count += 1
            await self.db.commit()
            raise
```

### 5.2 AI提示词设计

**参考Java版的番茄小说策略,我们设计通用图书分析提示词**:

```python
# 核心设计思路:
# 1. 明确角色定位 (专业图书分析助手)
# 2. 结构化输出 (JSON格式)
# 3. 4种提取类型 (观点/案例/建议/金句)
# 4. 质量要求 (准确性/完整性/可用性)

SYSTEM_PROMPT = """你是一位专业的图书分析助手,擅长从非虚构图书中提取核心知识点。

核心理念:
- **准确性**: 不编造内容,基于原文提取
- **实用性**: 提取可落地的知识和建议
- **结构化**: 按类别组织,便于后续应用

输出类别:
1. 核心观点: 本章的关键思想、理论框架、重要概念
2. 实践案例: 具体示例、真实案例、数据支撑
3. 行动建议: 可执行的方法、技巧、步骤
4. 金句摘录: 精彩句子、名言警句

质量标准:
- 标题: 简洁精准(≤20字)
- 内容: 详实完整(50-200字)
- 标签: 具体相关(3-5个)
- 格式: 严格JSON
"""

# 这个设计比Java版更聚焦,因为我们的目标是工具书而非网文
```

### 5.3 数据模型类

```python
# backend/app/models/book_analysis.py

from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, String, Integer, Text, DateTime, Enum as SQLEnum, ARRAY
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB

from app.db.base_class import Base


class JobStatus(str, Enum):
    PENDING = "pending"
    PARSING = "parsing"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BookAnalysisJob(Base):
    __tablename__ = "book_analysis_jobs"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(PGUUID(as_uuid=True), nullable=False)

    # 图书信息
    book_title = Column(String(500), nullable=False)
    original_filename = Column(String(500), nullable=False)
    file_format = Column(String(10), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    file_hash = Column(String(64), unique=True)

    # 任务状态
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING, nullable=False)
    progress = Column(Integer, default=0)
    current_step = Column(String(200))

    # 分析结果
    total_chapters = Column(Integer)
    analyzed_chapters = Column(Integer, default=0)
    extracted_items_count = Column(Integer, default=0)

    # 错误处理
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)

    # 元数据
    extra_data = Column(JSONB, default={})

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

## 6. API接口设计

### 6.1 上传图书

```python
# POST /api/v1/books/upload

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/upload")
async def upload_book(
    file: UploadFile = File(...),
    book_title: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传图书并启动分析任务"""

    # 1. 验证文件类型
    allowed_formats = ['.txt', '.epub', '.pdf']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_formats:
        raise HTTPException(400, f"不支持的文件格式,仅支持: {allowed_formats}")

    # 2. 验证文件大小
    max_size = 50 * 1024 * 1024  # 50MB
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(400, "文件过大,最大支持50MB")

    # 3. 计算文件哈希去重
    import hashlib
    file_hash = hashlib.sha256(content).hexdigest()

    existing_job = await db.execute(
        select(BookAnalysisJob).where(BookAnalysisJob.file_hash == file_hash)
    )
    if existing_job.scalar_one_or_none():
        raise HTTPException(400, "该图书已分析过,请在任务列表中查看")

    # 4. 保存文件
    upload_dir = Path("uploads/books")
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / f"{uuid4()}{file_ext}"

    with open(file_path, 'wb') as f:
        f.write(content)

    # 5. 创建分析任务
    job = BookAnalysisJob(
        user_id=current_user.id,
        book_title=book_title or file.filename,
        original_filename=file.filename,
        file_format=file_ext[1:],  # 去掉点号
        file_size_bytes=len(content),
        file_hash=file_hash,
        status=JobStatus.PENDING
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    # 6. 启动异步分析任务 (Celery或后台线程)
    from app.tasks import analyze_book_task
    analyze_book_task.delay(str(job.id), str(file_path), str(current_user.id))

    return {
        "job_id": str(job.id),
        "book_title": job.book_title,
        "status": job.status,
        "message": "分析任务已启动,请稍候查看进度"
    }
```

### 6.2 查询任务状态

```python
# GET /api/v1/books/jobs/{job_id}

@router.get("/jobs/{job_id}")
async def get_job_status(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """查询分析任务状态"""

    job = await db.get(BookAnalysisJob, job_id)
    if not job:
        raise HTTPException(404, "任务不存在")

    if job.user_id != current_user.id:
        raise HTTPException(403, "无权访问该任务")

    return {
        "job_id": str(job.id),
        "book_title": job.book_title,
        "status": job.status,
        "progress": job.progress,
        "current_step": job.current_step,
        "total_chapters": job.total_chapters,
        "analyzed_chapters": job.analyzed_chapters,
        "extracted_items_count": job.extracted_items_count,
        "error_message": job.error_message,
        "created_at": job.created_at.isoformat(),
        "completed_at": job.completed_at.isoformat() if job.completed_at else None
    }
```

### 6.3 任务列表

```python
# GET /api/v1/books/jobs

@router.get("/jobs")
async def list_jobs(
    status: Optional[JobStatus] = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的分析任务列表"""

    query = select(BookAnalysisJob).where(
        BookAnalysisJob.user_id == current_user.id
    )

    if status:
        query = query.where(BookAnalysisJob.status == status)

    query = query.order_by(BookAnalysisJob.created_at.desc())
    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    jobs = result.scalars().all()

    return {
        "jobs": [
            {
                "job_id": str(job.id),
                "book_title": job.book_title,
                "status": job.status,
                "progress": job.progress,
                "extracted_items_count": job.extracted_items_count,
                "created_at": job.created_at.isoformat()
            }
            for job in jobs
        ],
        "total": len(jobs)
    }
```

---

## 7. 前端集成方案

### 7.1 上传对话框组件

```tsx
// frontend/src/components/knowledge/BookUploadDialog.tsx

import React, { useState } from 'react';
import { Upload, message, Modal, Progress } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import { uploadBook, getJobStatus } from '@/api/bookAnalysis';

const { Dragger } = Upload;

export const BookUploadDialog: React.FC<{
  visible: boolean;
  onClose: () => void;
  onSuccess: (jobId: string) => void;
}> = ({ visible, onClose, onSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');

  const handleUpload = async (file: File) => {
    try {
      setUploading(true);

      // 上传文件
      const result = await uploadBook(file);

      message.success('上传成功,开始分析...');
      setUploading(false);
      setAnalyzing(true);

      // 轮询任务状态
      const jobId = result.job_id;
      const pollInterval = setInterval(async () => {
        const status = await getJobStatus(jobId);

        setProgress(status.progress);
        setCurrentStep(status.current_step);

        if (status.status === 'completed') {
          clearInterval(pollInterval);
          message.success(`分析完成! 提取了 ${status.extracted_items_count} 个知识点`);
          onSuccess(jobId);
          onClose();
        } else if (status.status === 'failed') {
          clearInterval(pollInterval);
          message.error(`分析失败: ${status.error_message}`);
          setAnalyzing(false);
        }
      }, 2000);

    } catch (error) {
      message.error('上传失败: ' + error.message);
      setUploading(false);
    }

    return false; // 阻止默认上传行为
  };

  return (
    <Modal
      title="上传图书进行AI分析"
      open={visible}
      onCancel={onClose}
      footer={null}
      width={600}
    >
      {!analyzing ? (
        <Dragger
          accept=".txt,.epub,.pdf"
          beforeUpload={handleUpload}
          showUploadList={false}
          disabled={uploading}
        >
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">
            点击或拖拽文件到此区域上传
          </p>
          <p className="ant-upload-hint">
            支持 .txt, .epub, .pdf 格式,最大50MB
          </p>
        </Dragger>
      ) : (
        <div style={{ padding: '20px' }}>
          <Progress percent={progress} status="active" />
          <p style={{ marginTop: '10px', textAlign: 'center' }}>
            {currentStep}
          </p>
        </div>
      )}
    </Modal>
  );
};
```

### 7.2 集成到知识库页面

```tsx
// frontend/src/pages/KnowledgeLibrary.tsx

import { BookUploadDialog } from '@/components/knowledge/BookUploadDialog';
import { Button } from 'antd';
import { BookOutlined } from '@ant-design/icons';

export const KnowledgeLibrary: React.FC = () => {
  const [uploadVisible, setUploadVisible] = useState(false);

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Button
          type="primary"
          icon={<BookOutlined />}
          onClick={() => setUploadVisible(true)}
        >
          AI拆书分析
        </Button>
      </div>

      {/* 知识库列表 */}
      <KnowledgeList />

      {/* 上传对话框 */}
      <BookUploadDialog
        visible={uploadVisible}
        onClose={() => setUploadVisible(false)}
        onSuccess={(jobId) => {
          // 跳转到知识库列表并筛选该书的知识点
          message.success('分析完成,已自动刷新知识库');
        }}
      />
    </div>
  );
};
```

---

## 8. 测试方案

### 8.1 单元测试

```python
# backend/tests/test_book_analysis.py

import pytest
from app.services.book_analysis_service import BookAnalysisService

@pytest.mark.asyncio
async def test_parse_txt_book():
    """测试TXT解析"""
    service = BookAnalysisService(...)

    # 创建测试文件
    test_content = """
第一章 项目管理基础

项目管理是...

第二章 敏捷开发实践

敏捷开发强调...
"""

    with open('/tmp/test_book.txt', 'w') as f:
        f.write(test_content)

    chapters = await service.parse_txt_book('/tmp/test_book.txt')

    assert len(chapters) == 2
    assert chapters[0].title == '第一章 项目管理基础'
    assert '项目管理' in chapters[0].content


@pytest.mark.asyncio
async def test_analyze_chapter():
    """测试AI分析"""
    service = BookAnalysisService(...)

    chapter = ChapterData(
        index=1,
        title="第一章 测试",
        content="核心观点: 测试驱动开发是..."
    )

    result = await service.analyze_chapter(chapter, "测试图书")

    assert 'core_concepts' in result
    assert len(result['core_concepts']) > 0
```

### 8.2 集成测试

```python
# backend/tests/test_book_api.py

@pytest.mark.asyncio
async def test_upload_and_analyze():
    """端到端测试"""

    # 1. 上传文件
    with open('test_data/sample_book.txt', 'rb') as f:
        response = await client.post(
            '/api/v1/books/upload',
            files={'file': f}
        )

    assert response.status_code == 200
    job_id = response.json()['job_id']

    # 2. 等待分析完成
    import asyncio
    for _ in range(30):  # 最多等待60秒
        await asyncio.sleep(2)

        status_response = await client.get(f'/api/v1/books/jobs/{job_id}')
        status = status_response.json()

        if status['status'] == 'completed':
            break

    assert status['status'] == 'completed'
    assert status['extracted_items_count'] > 0

    # 3. 验证知识库
    knowledge_response = await client.get('/api/v1/knowledge')
    items = knowledge_response.json()['items']

    book_items = [
        item for item in items
        if item['source_type'] == 'BOOK_ANALYSIS'
    ]

    assert len(book_items) > 0
```

---

## 📋 总结

### ✅ 本方案的优势

1. **复用现有架构**: 100% 基于当前的 FastAPI + PostgreSQL
2. **简化设计**: 平面知识条目,避免Java版的树形复杂度
3. **聚焦场景**: 针对工具书/教程,而非网文小说
4. **快速上线**: MVP仅需5天开发
5. **扩展性强**: 通过JSONB支持后续功能迭代

### 🎯 关键差异点

| 维度 | Java参考版 | 我们的实现 |
|------|-----------|----------|
| 目标类型 | 网文小说 | 非虚构图书 |
| 分析维度 | 11维度树形 | 4类平面条目 |
| 数据库 | MongoDB | PostgreSQL |
| 实时推送 | SSE | 轮询(可升级WebSocket) |
| 会话管理 | 内存Session | 数据库Job |

---

## 9. 最终确定方案 (基于讨论结果)

### 9.1 需求确认 (来自 INFO.md)

#### **1. 功能定位**
- ✅ **目标用户**: 小说作者,用来分析其他小说学习技巧
- ✅ **核心场景**: 长篇网文创作者分析爆款学习套路

#### **2. 输出内容需求**
原方案的4类不够用,需要扩展为网文专用的分析维度:
- 🎭 **角色设定模板**
- 🌍 **世界观要素**
- 📖 **情节结构分析**
- 🔥 **爽点设计技巧**

**→ 决策: 采用Java参考文档的11维度网文分析策略**

#### **3. 策略选择**
- ✅ **双策略支持,但先实现网文策略**
  - Phase 1 (Week 1-2): 网文11维度分析
  - Phase 2 (Week 3+): 通用图书分析

**理由**:
1. ✅ 差异化最强 (网文工具市场空白)
2. ✅ 技术难度最高 (攻克最难的,其他都简单)
3. ✅ 未来扩展性好 (策略模式架构)
4. ✅ 商业价值最大 (网文作者付费意愿强)

#### **4. 性能方案**
针对长篇网文 (100万字+, 500章) 的智能采样策略:
- ✅ 前30章深度分析 (建立核心设定)
- ✅ 关键章节识别 (正则+固定间隔)
- ✅ 增量分析提示词 (只提取新内容)
- ✅ 成本控制 (单次最大分析章节数限制)

**预期效果**:
- 分析时间: 15-20分钟
- 分析章节: 100-150章 (而非全部500章)
- API成本: $0.3-0.5
- 提取知识点: 200-300个

#### **5. 世界观关联方式**
- ✅ **Week 1 直接做智能建议版本**
  - AI自动识别可关联的世界观元素
  - 卡片式建议列表,批量选中交互
  - 采纳向导流程,预填充数据
  - 有"魔法感"的用户体验

**对比方案**:

| 维度 | 纯知识库模式 | 智能建议模式 (选定) |
|------|-------------|---------------------|
| 开发时间 | 3天 ⚡ | 5天 |
| 用户体验 | 😐 需要手动操作 | 🤩 AI主动建议 |
| 采纳率 | 20-30% | 60-80% |
| 差异化 | ⭐⭐ 知识库工具 | ⭐⭐⭐⭐⭐ 智能助手 |
| 产品价值 | 实用工具 | 魔法体验 |

**→ 决策: 多花2天,换来10倍用户价值**

---

## 10. 完整开发计划 (已确定)

### 10.1 Week 1: 网文11维度分析 MVP (Day 1-6)

#### **Day 1-2: 后端核心架构**

**任务清单**:
- [ ] 创建策略模式基础架构
  - [ ] `BookAnalysisStrategy` 抽象基类
  - [ ] `WebNovelStrategy` 实现类 (11维度)
  - [ ] `StrategyRegistry` 策略注册器

- [ ] 实现智能采样分析服务
  - [ ] `SmartSamplingAnalyzer` 类
  - [ ] 前30章深度分析逻辑
  - [ ] 关键章节识别算法
  - [ ] 增量分析提示词构建

- [ ] 数据模型创建
  - [ ] `book_analysis_jobs` 表 (任务管理)
  - [ ] `worldview_suggestions` 表 (智能建议)
  - [ ] SQLAlchemy模型类
  - [ ] Alembic迁移脚本

- [ ] 提示词工程
  - [ ] 11维度网文分析系统提示词
  - [ ] 增量分析提示词模板
  - [ ] 智能建议生成提示词

**关键文件**:
```
backend/app/services/book_analysis/
├── __init__.py
├── strategy.py              # 策略基类
├── web_novel_strategy.py    # 网文策略实现
├── smart_sampling.py         # 智能采样逻辑
└── suggestion_generator.py   # 建议生成器

backend/app/models/
├── book_analysis.py          # Job模型
└── worldview_suggestion.py   # Suggestion模型

backend/alembic/versions/
└── xxxx_add_book_analysis_tables.py
```

---

#### **Day 3: API接口开发**

**任务清单**:
- [ ] 创建API路由
  - [ ] `POST /api/v1/books/upload` - 上传图书并启动分析
  - [ ] `GET /api/v1/books/jobs/{job_id}` - 查询任务状态
  - [ ] `GET /api/v1/books/jobs` - 任务列表
  - [ ] `GET /api/v1/books/{job_id}/suggestions` - 获取智能建议
  - [ ] `POST /api/v1/books/{job_id}/adopt` - 批量采纳建议
  - [ ] `PATCH /api/v1/suggestions/{id}` - 修改单个建议
  - [ ] `DELETE /api/v1/books/jobs/{job_id}` - 删除任务

- [ ] 异步任务处理
  - [ ] Celery任务配置 (或后台线程)
  - [ ] 任务状态更新机制
  - [ ] 错误处理与重试逻辑

- [ ] API文档
  - [ ] FastAPI自动文档完善
  - [ ] 请求/响应示例

**关键文件**:
```
backend/app/api/v1/endpoints/
└── books.py                  # 图书分析API

backend/app/tasks/
└── book_analysis_task.py     # Celery异步任务
```

---

#### **Day 4-5: 前端集成**

**任务清单**:

**Day 4: 核心组件开发**
- [ ] 上传对话框
  - [ ] `BookUploadDialog.tsx` - 文件上传+意图选择
  - [ ] 策略选择UI (网文分析 vs 通用分析)
  - [ ] 作品关联选择器
  - [ ] 上传进度显示

- [ ] 分析进度监控
  - [ ] `AnalysisProgressPanel.tsx` - 实时进度条
  - [ ] 任务状态轮询逻辑
  - [ ] 阶段性进度文案 ("正在分析第XX章...")

**Day 5: 智能建议UI**
- [ ] 建议结果页面
  - [ ] `SuggestionResultModal.tsx` - 分析完成弹窗
  - [ ] `SuggestionCard.tsx` - 建议卡片组件
  - [ ] 卡片网格布局 (响应式)
  - [ ] 类型筛选标签 (角色/地点/设定/力量体系)

- [ ] 批量操作交互
  - [ ] 卡片多选交互 (点击卡片切换选中状态)
  - [ ] 全选/反选/按推荐度筛选
  - [ ] 底部操作栏 (采纳X个元素)

- [ ] 采纳向导
  - [ ] `AdoptionWizard.tsx` - 逐步确认流程
  - [ ] 表单预填充 (AI生成的数据)
  - [ ] 跳过/修改/保存按钮
  - [ ] 完成庆祝动画

**关键文件**:
```
frontend/src/components/knowledge/
├── BookUploadDialog.tsx
├── AnalysisProgressPanel.tsx
├── SuggestionResultModal.tsx
├── SuggestionCard.tsx
└── AdoptionWizard.tsx

frontend/src/api/
└── bookAnalysis.ts           # API调用封装

frontend/src/types/
└── bookAnalysis.ts           # TypeScript类型定义
```

---

#### **Day 6: 测试与优化**

**任务清单**:
- [ ] 后端单元测试
  - [ ] 测试TXT解析功能
  - [ ] 测试11维度分析提示词
  - [ ] 测试智能采样逻辑
  - [ ] 测试建议生成准确性

- [ ] 集成测试
  - [ ] 端到端测试 (上传→分析→入库)
  - [ ] 测试长篇网文 (100万字+)
  - [ ] 测试成本控制 (是否≤$0.5)
  - [ ] 测试错误处理 (网络中断/API限流)

- [ ] 前端测试
  - [ ] 组件单元测试
  - [ ] 用户流程测试
  - [ ] 响应式布局测试

- [ ] 性能优化
  - [ ] 数据库查询优化
  - [ ] API响应时间优化
  - [ ] 前端加载速度优化

- [ ] 文档编写
  - [ ] 用户使用指南
  - [ ] API接口文档
  - [ ] 开发者文档

**关键文件**:
```
backend/tests/
├── test_book_analysis_service.py
├── test_web_novel_strategy.py
├── test_smart_sampling.py
└── test_book_api.py

frontend/src/components/__tests__/
├── BookUploadDialog.test.tsx
└── SuggestionCard.test.tsx
```

---

### 10.2 Week 2-3: 扩展功能 (可选)

#### **Phase 2A: 通用图书分析策略**
- [ ] 创建 `GeneralBookStrategy` 类
- [ ] 4类通用提取 (观点/案例/建议/金句)
- [ ] 前端策略切换UI

#### **Phase 2B: 多格式支持**
- [ ] .epub 解析 (ebooklib)
- [ ] .pdf 解析 (PyPDF2)
- [ ] 格式自动识别

#### **Phase 2C: 进阶功能**
- [ ] 本地模型支持 (Ollama初筛)
- [ ] 用户自定义采样策略
- [ ] 断点续传 (分析中断可恢复)
- [ ] 知识图谱可视化
- [ ] 多书对比分析

---

## 11. 技术实现细节

### 11.1 11维度网文分析策略

#### **分析维度定义**

```python
# backend/app/services/book_analysis/web_novel_strategy.py

class WebNovelStrategy(BookAnalysisStrategy):
    """番茄小说网文分析策略 (11维度)"""

    DIMENSIONS = [
        {
            "id": "core_selling_point",
            "name": "核心卖点",
            "description": "一句话概括小说的最大吸引力点",
            "priority": 1,
            "output_length": "50-80字",
            "entity_type": "TECHNIQUE",
            "tags": ["卖点", "核心定位"]
        },
        {
            "id": "protagonist_setting",
            "name": "主角设定",
            "description": "主角的身份背景、性格标签、初始困境",
            "priority": 2,
            "output_length": "100-200字",
            "entity_type": "CHARACTER_TEMPLATE",
            "tags": ["角色", "主角"],
            "sub_elements": [
                {"id": "identity", "name": "身份背景"},
                {"id": "personality", "name": "性格标签"},
                {"id": "initial_crisis", "name": "初始困境"}
            ]
        },
        {
            "id": "cheat_system",
            "name": "金手指系统",
            "description": "主角的外挂、系统或核心优势",
            "priority": 3,
            "output_length": "150-250字",
            "entity_type": "POWER_SYSTEM",
            "tags": ["金手指", "系统"],
            "sub_elements": [
                {"id": "mechanism", "name": "核心机理"},
                {"id": "growth_path", "name": "成长路径"},
                {"id": "usage_examples", "name": "用法示例"}
            ]
        },
        {
            "id": "world_framework",
            "name": "世界观框架",
            "description": "故事发生的时代背景与底层规则",
            "priority": 4,
            "output_length": "100-200字",
            "entity_type": "SETTING",
            "tags": ["世界观", "背景设定"]
        },
        {
            "id": "power_system",
            "name": "等级力量体系",
            "description": "角色成长的分层体系与战力规则",
            "priority": 5,
            "output_length": "100-200字",
            "entity_type": "POWER_SYSTEM",
            "tags": ["力量体系", "等级"]
        },
        {
            "id": "antagonist_forces",
            "name": "反派势力",
            "description": "敌对体系,层级递进的反派设计",
            "priority": 6,
            "output_length": "100-200字",
            "entity_type": "CHARACTER_TEMPLATE",
            "tags": ["反派", "势力"],
            "sub_elements": [
                {"id": "tier_1", "name": "前期反派"},
                {"id": "tier_2", "name": "中期反派"},
                {"id": "tier_3", "name": "后期反派"}
            ]
        },
        {
            "id": "romance_line",
            "name": "情感线设定",
            "description": "情感关系的发展路径",
            "priority": 7,
            "output_length": "100-150字",
            "entity_type": "RELATIONSHIP",
            "tags": ["情感线", "感情"]
        },
        {
            "id": "satisfaction_points",
            "name": "爽点布局",
            "description": "打脸、反差、碾压、绝境翻盘等爽点设计",
            "priority": 8,
            "output_length": "150-250字",
            "entity_type": "TECHNIQUE",
            "tags": ["爽点", "节奏"],
            "sub_elements": [
                {"id": "chapter_1_10", "name": "前10章爽点"},
                {"id": "chapter_10_30", "name": "10-30章爽点"},
                {"id": "chapter_30_plus", "name": "30章后爽点"}
            ]
        },
        {
            "id": "anticipation_hooks",
            "name": "期待感钩子",
            "description": "悬念、伏笔、预告等拉期待的设计",
            "priority": 9,
            "output_length": "150-250字",
            "entity_type": "TECHNIQUE",
            "tags": ["悬念", "伏笔", "期待感"]
        },
        {
            "id": "sub_plots",
            "name": "支线剧情",
            "description": "增强可读性的副线",
            "priority": 10,
            "output_length": "100-200字",
            "entity_type": "PLOT_STRUCTURE",
            "tags": ["支线", "副线"]
        },
        {
            "id": "unique_features",
            "name": "特色设定",
            "description": "差异化卖点与母题",
            "priority": 11,
            "output_length": "100-150字",
            "entity_type": "TECHNIQUE",
            "tags": ["特色", "差异化"]
        }
    ]
```

#### **提示词模板**

```python
SYSTEM_PROMPT = """
你是一位在番茄小说平台孵化多本爆款的白金大神作家兼策划。

核心理念 (必须贯彻):
- **金手指**: 独特且具成长性的优势/系统,避免平庸或单纯数值堆砌
- **爽点**: 反差、打脸、扮猪吃虎、绝境翻盘、信息差等,每隔几章必须有一波"大爽"
- **期待感**: 悬念、伏笔、信息差形成闭环,每一章都让读者想看下一章
- **网感**: 始终围绕"读者体验"与"商业化结果"思考

输出要求:
1. 严格遵循JSON Schema结构
2. 根节点 (11个维度) 每个50-80字精炼概括
3. 叶子节点 (详细内容) 每个100-200字深度阐述
4. 必须体现"拉期待—给爽点—再拉期待"的循环结构
5. 所有内容必须可落地执行,避免空洞理论

禁止行为:
- 生成与网文商业逻辑脱节的"文学化"设定
- 使用模糊词汇 ("可能"、"也许"、"或许")
- 重复已有网文的套路而不加创新
- 忽略"爽点密度"与"期待感钩子"的布局
"""

USER_PROMPT_TEMPLATE = """
小说内容:
{novel_content}

{existing_settings_context}

根节点清单 (必须包含,顺序不可变):
{dimensions_list}

输出格式要求:
- 使用 JSON 格式
- 每个维度必须包含: id、name、description、children (如有)
- description 为核心内容,根节点50-80字,叶子节点100-200字
- 所有子节点必须在 children 数组中,不得遗漏
- 必须包含所有11个根节点,不得擅自合并或删减

特别提醒:
- 番茄小说读者偏好"快节奏+高爽点密度",前3章必须有至少2个爽点
- 金手指必须"独特+可成长+有具体用法"
- 反派必须有"层级递进"
- 情感线不能"无脑倒贴",必须有情感张力

{incremental_instruction}
"""

INCREMENTAL_INSTRUCTION = """
=== 增量分析模式 ===
当前章节: 第{chapter_num}章

已知设定 (请避免重复):
{existing_settings_summary}

你的任务:
ONLY 提取 **新增的** 或 **变化的** 设定元素:
1. 新角色出现?
2. 新技能/装备/系统功能?
3. 新反派/势力?
4. 新的爽点类型?
5. 世界观扩展?

如果本章没有新元素,返回: {{"no_new_content": true}}
"""
```

---

### 11.2 智能建议生成逻辑

```python
# backend/app/services/book_analysis/suggestion_generator.py

class SuggestionGenerator:
    """智能建议生成器"""

    async def generate_suggestions(
        self,
        analysis_result: Dict,
        target_work_id: Optional[UUID],
        user_id: UUID
    ) -> List[WorldviewSuggestion]:
        """
        从11维度分析结果生成可关联的世界观元素建议

        映射规则:
        - 核心卖点 → TECHNIQUE (知识库条目)
        - 主角设定 → CHARACTER (智能建议)
        - 金手指系统 → POWER_SYSTEM (智能建议)
        - 世界观框架 → SETTING (智能建议)
        - 等级力量体系 → POWER_SYSTEM (智能建议)
        - 反派势力 → CHARACTER (智能建议)
        - 情感线设定 → RELATIONSHIP (智能建议)
        - 爽点布局 → TECHNIQUE (知识库条目)
        - 期待感钩子 → TECHNIQUE (知识库条目)
        - 支线剧情 → PLOT_STRUCTURE (知识库条目)
        - 特色设定 → TECHNIQUE (知识库条目)
        """

        suggestions = []

        # 1. 主角设定 → 建议创建角色
        if "protagonist_setting" in analysis_result:
            protagonist = analysis_result["protagonist_setting"]

            # AI评估置信度
            confidence = await self._assess_confidence(
                element_type="character",
                data=protagonist,
                existing_world=await self._load_world(target_work_id)
            )

            if confidence > 0.6:  # 置信度阈值
                suggestions.append(WorldviewSuggestion(
                    user_id=user_id,
                    work_id=target_work_id,
                    suggestion_type="character",
                    action="create_new",
                    suggested_data={
                        "name": protagonist.get("name", "主角原型"),
                        "identity": protagonist.get("identity", ""),
                        "personality_tags": protagonist.get("personality", []),
                        "background": protagonist.get("description", "")
                    },
                    confidence_score=confidence,
                    reason=await self._generate_reason(protagonist, confidence),
                    status="pending"
                ))

        # 2. 金手指系统 → 建议创建力量体系
        if "cheat_system" in analysis_result:
            system = analysis_result["cheat_system"]
            confidence = await self._assess_confidence(
                element_type="power_system",
                data=system,
                existing_world=await self._load_world(target_work_id)
            )

            if confidence > 0.6:
                suggestions.append(WorldviewSuggestion(
                    suggestion_type="power_system",
                    suggested_data={
                        "name": system.get("name", ""),
                        "mechanism": system.get("mechanism", ""),
                        "growth_path": system.get("growth_path", [])
                    },
                    confidence_score=confidence,
                    # ...
                ))

        # 3-11. 其他维度的映射逻辑...

        return suggestions
```

---

## 12. 验收标准

### 12.1 功能验收

- [ ] ✅ 可上传.txt格式网文小说 (≤50MB)
- [ ] ✅ 自动识别章节结构 (正则匹配成功率≥90%)
- [ ] ✅ 智能采样分析 (前30章全分析 + 后期抽样)
- [ ] ✅ 11维度提取完整 (所有维度都有输出)
- [ ] ✅ 自动创建知识库条目 (≥150条)
- [ ] ✅ 生成智能建议 (15-30个可关联元素)
- [ ] ✅ 批量采纳功能正常
- [ ] ✅ 采纳向导预填充正确

### 12.2 性能验收

- [ ] ✅ 100万字网文分析时间 ≤ 20分钟
- [ ] ✅ API成本 ≤ $0.5/本
- [ ] ✅ 分析章节数 ≤ 150章 (而非全部500章)
- [ ] ✅ 前端响应时间 < 500ms
- [ ] ✅ 进度更新延迟 < 2秒

### 12.3 体验验收

- [ ] ✅ 上传流程顺畅 (≤3步)
- [ ] ✅ 进度显示清晰
- [ ] ✅ 建议卡片美观 (卡片布局/类型徽章)
- [ ] ✅ 批量选中交互流畅
- [ ] ✅ 采纳向导体验好 (有"魔法感")
- [ ] ✅ 完成时有庆祝动画

---

## 13. 风险与对策

### 13.1 技术风险

| 风险 | 影响 | 概率 | 对策 |
|------|------|------|------|
| AI提取不准确 | 高 | 中 | 迭代优化提示词;人工审核建议 |
| 长文本Token超限 | 中 | 中 | 智能采样;内容截断策略 |
| API限流 | 中 | 低 | 请求间隔控制;错误重试 |
| 前端性能问题 | 中 | 低 | 虚拟滚动;懒加载 |

### 13.2 产品风险

| 风险 | 影响 | 概率 | 对策 |
|------|------|------|------|
| 用户不理解11维度 | 中 | 中 | 添加维度说明tooltip;示例展示 |
| 采纳率低于预期 | 高 | 中 | A/B测试;用户访谈;优化推荐算法 |
| 成本超预算 | 高 | 低 | 严格的成本监控;单用户限额 |

---

## 14. 下一步行动

### ✅ 已完成
- [x] 需求讨论与确认
- [x] 方案设计与评审
- [x] 完整开发计划制定

### 🚀 立即开始 (Day 1)

1. **创建Git分支**
   ```bash
   git checkout -b feature/book-analysis
   ```

2. **创建项目结构**
   ```bash
   mkdir -p backend/app/services/book_analysis
   mkdir -p backend/app/models
   mkdir -p frontend/src/components/knowledge
   ```

3. **开始编码 (Day 1 任务)**
   - [ ] 创建策略基类
   - [ ] 实现WebNovelStrategy
   - [ ] 创建数据库表

### 📅 时间表总览

```
Week 1 (Day 1-6): 网文分析MVP
├─ Day 1-2: 后端核心 (策略+采样+提示词)
├─ Day 3:   API开发 (7个端点+异步任务)
├─ Day 4-5: 前端集成 (上传+进度+建议+采纳)
└─ Day 6:   测试优化 (单元+集成+性能)

Week 2-3 (可选): 扩展功能
├─ 通用图书分析策略
├─ .epub/.pdf格式支持
└─ 进阶功能 (本地模型/断点续传/知识图谱)
```

---

**文档版本**: v2.0 (最终确定版)
**创建时间**: 2025-10-27
**最后更新**: 2025-10-27
**作者**: Claude Code
**状态**: ✅ 已确认,准备开始实施
