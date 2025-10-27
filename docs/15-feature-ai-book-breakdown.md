# AI拆书功能设计文档

> **功能名称**: AI智能拆书分析系统
> **优先级**: ⭐⭐⭐⭐
> **状态**: ✅ 已完成 (MVP版本)
> **完成日期**: 2025-10-27
> **测试通过率**: 100% (7/7)
> **依赖功能**: 个人知识库 (已实现)
> **最后更新**: 2025-10-27

---

## 📋 目录

**📢 重要**: AI拆书功能已完整实现! 查看 → [实施总结文档](./AI拆书功能实施总结_2025-10-27.md)

1. [功能概述](#功能概述)
2. [核心价值](#核心价值)
3. [使用场景](#使用场景)
4. [技术方案](#技术方案)
5. [数据模型设计](#数据模型设计)
6. [API接口设计](#api接口设计)
7. [开发计划](#开发计划) ✅ 已完成
8. [LangChain增强方案](#langchain增强方案)

---

## 🎯 功能概述

AI拆书功能允许用户上传书籍(PDF/TXT/EPUB)，通过AI自动分析提取:
- 📚 **结构分析**: 章节结构、叙事框架、剧情节奏
- 🎭 **写作技巧**: 描写手法、对话技巧、悬念设计
- 🌍 **内容提取**: 世界观设定、人物关系、情节要素
- 💡 **创作启发**: 可复用的素材、灵感点、金句摘录

拆书结果可直接保存到个人知识库，作为写作参考素材。

---

## 💎 核心价值

### 1. 学习优秀作品 (⭐⭐⭐⭐⭐)
- 快速理解经典小说的写作结构
- 学习成熟作家的叙事技巧
- 分析畅销书的爽点设计

### 2. 建立素材库 (⭐⭐⭐⭐⭐)
- 提取可复用的世界观设定
- 收集精彩的对话和描写
- 建立个人化的创作素材库

### 3. 差异化竞争 (⭐⭐⭐⭐)
- 市面上AI写作工具少有此功能
- 从"写作助手"升级为"写作教练"
- 吸引注重学习提升的作者用户

---

## 📖 使用场景

### 场景1: 新手作者学习写作
```
用户行为:
1. 上传《三体》PDF
2. 选择分析维度: "科幻设定构建" + "悬念铺垫技巧"
3. AI生成拆书报告

AI输出:
├── 科幻设定构建
│   ├── 三体文明的设定逻辑
│   ├── 黑暗森林法则的引入时机
│   └── 技术细节的真实感塑造
├── 悬念铺垫技巧
│   ├── 倒计时的多重解释
│   ├── 信息的逐步揭示
│   └── 反转的伏笔设计
└── 可复用素材
    └── [自动保存到知识库]
```

### 场景2: 老作者研究市场热书
```
用户行为:
1. 上传近期热门网文
2. 选择分析: "爽点设计" + "节奏控制" + "读者留存策略"

AI输出:
├── 爽点分析
│   ├── 每章爽点分布图
│   ├── 打脸/装逼/反转频率
│   └── 情绪曲线图
├── 节奏控制
│   ├── 章节长度分析
│   ├── 高潮低谷交替规律
│   └── 悬念扣设计密度
└── 商业化建议
    └── 可学习的商业写作技巧
```

### 场景3: 跨类型创作参考
```
用户行为:
1. 上传5本武侠小说
2. 批量提取"武功体系设定"

AI输出:
├── 《天龙八部》- 内力修炼体系
├── 《笑傲江湖》- 剑法招式设定
├── 《射雕英雄传》- 功法等级划分
├── 《神雕侠侣》- 独门绝技设计
└── 综合分析
    ├── 武侠体系的共性规律
    ├── 差异化设计要点
    └── [生成可复用模板]
```

---

## 🛠️ 技术方案

### 方案A: 简单MVP版本 (推荐先做)

**核心流程:**
```
上传书籍 → 解析文本 → AI分析 → 生成报告 → 保存到知识库
```

**技术栈:**
```python
# 1. 文件解析
- PDF: PyPDF2 / pdfplumber
- TXT: 原生支持
- EPUB: ebooklib

# 2. 文本处理
- 章节切分: 正则匹配 + 智能识别
- 去除噪音: 页眉页脚、目录等

# 3. AI分析
- 复用现有: NovelAnalysisOrchestrator
- 扩展分析维度:
  ├── 宏观: 结构、节奏、主题
  ├── 微观: 技巧、手法、细节
  └── 提取: 世界观、人物、情节

# 4. 结果存储
- book_analysis 表: 存储分析结果
- knowledge_items 表: 可复用素材
```

**改动文件列表:**
```
新增:
├── backend/app/models/book_analysis.py          (书籍分析模型)
├── backend/app/schemas/book_analysis.py         (Schema定义)
├── backend/app/api/v1/book_breakdown.py         (API路由)
├── backend/app/services/book_parser_service.py  (文件解析)
└── backend/app/services/ai/book_analyzer.py     (AI拆书分析器)

修改:
├── backend/app/services/ai/novel_analysis_orchestrator.py  (扩展支持外部书籍)
├── backend/app/services/vector_store_service.py            (增加书籍类型)
└── backend/requirements.txt  (添加: pdfplumber, ebooklib)
```

### 方案B: LangChain增强版 (中期扩展)

**增强能力:**
1. **对话式拆书**: 多轮问答深度分析
2. **对比分析**: 同时分析多本书的差异
3. **自动生成学习笔记**: 结构化输出

详见 [LangChain增强方案](#langchain增强方案)

---

## 📊 数据模型设计

### 1. BookAnalysis (书籍分析主表)

```python
# backend/app/models/book_analysis.py
from sqlalchemy import Column, String, Text, Integer, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum

class BookFormat(str, enum.Enum):
    """书籍格式"""
    PDF = "pdf"
    TXT = "txt"
    EPUB = "epub"
    OTHER = "other"

class AnalysisType(str, enum.Enum):
    """分析类型"""
    STRUCTURE = "structure"      # 结构分析
    TECHNIQUE = "technique"      # 技巧分析
    CONTENT = "content"          # 内容提取
    MARKET = "market"            # 市场分析
    FULL = "full"                # 全面分析

class BookAnalysis(Base):
    """书籍拆书分析"""
    __tablename__ = "book_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # 书籍信息
    book_title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=True)
    format = Column(Enum(BookFormat), nullable=False)
    file_path = Column(String(500), nullable=False)  # 存储路径

    # 文本内容
    total_words = Column(Integer, default=0)
    total_chapters = Column(Integer, default=0)
    full_text = Column(Text, nullable=True)  # 可选: 存储全文

    # 分析配置
    analysis_type = Column(Enum(AnalysisType), nullable=False)
    custom_prompts = Column(JSON, nullable=True)  # 自定义分析维度

    # 分析结果
    structure_analysis = Column(JSON, nullable=True)  # 结构分析
    technique_analysis = Column(JSON, nullable=True)  # 技巧分析
    content_extraction = Column(JSON, nullable=True)  # 内容提取
    market_analysis = Column(JSON, nullable=True)     # 市场分析

    # 元数据
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    # 关联
    user = relationship("User", back_populates="book_analyses")
    knowledge_items = relationship("KnowledgeItem", back_populates="source_analysis")
```

### 2. 分析结果JSON结构

```python
# structure_analysis 结构
{
    "narrative_framework": {
        "type": "三幕式结构",
        "acts": [
            {"act": 1, "chapters": [1, 5], "summary": "世界观建立"},
            {"act": 2, "chapters": [6, 15], "summary": "冲突升级"},
            {"act": 3, "chapters": [16, 20], "summary": "高潮与结局"}
        ]
    },
    "plot_rhythm": {
        "chapter_lengths": [2500, 3000, 2800, ...],
        "climax_positions": [5, 10, 18],
        "pace_analysis": "前慢后快，符合商业小说节奏"
    }
}

# technique_analysis 结构
{
    "writing_techniques": [
        {
            "technique": "悬念铺垫",
            "examples": [
                {"chapter": 3, "quote": "他转身离开，不知道身后的阴影正在逼近..."},
                {"chapter": 7, "quote": "这个秘密，只有一个人知道。"}
            ],
            "analysis": "多次使用伏笔暗示，增强读者期待"
        },
        {
            "technique": "对话推进情节",
            "examples": [...],
            "analysis": "通过对话揭示信息，避免旁白堆砌"
        }
    ],
    "description_style": {
        "character_description": "外貌+性格+行为三位一体",
        "scene_description": "视觉+听觉+嗅觉多感官描写"
    }
}

# content_extraction 结构
{
    "worldview": {
        "setting": "近未来地球 + 三体星系",
        "rules": ["黑暗森林法则", "技术爆炸理论"],
        "organizations": ["地球三体组织", "面壁计划"]
    },
    "characters": [
        {
            "name": "叶文洁",
            "role": "关键人物",
            "traits": ["理想主义", "绝望", "复仇"],
            "arc": "从科学家到三体联络员的转变"
        }
    ],
    "plot_elements": {
        "core_conflicts": ["人类与三体文明", "科学与信仰"],
        "turning_points": [
            {"chapter": 5, "event": "叶文洁发现信号"},
            {"chapter": 15, "event": "黑暗森林法则揭示"}
        ]
    }
}
```

---

## 🔌 API接口设计

### 1. 上传并分析书籍

```http
POST /api/v1/books/analyze
Content-Type: multipart/form-data

Request:
{
    "file": <binary>,
    "book_title": "三体",
    "author": "刘慈欣",
    "analysis_type": "full",  // structure/technique/content/market/full
    "custom_prompts": [
        "分析科幻设定的构建方式",
        "提取可复用的悬念技巧"
    ]
}

Response 200:
{
    "analysis_id": "uuid",
    "status": "processing",
    "message": "分析任务已创建，预计需要5-10分钟"
}
```

### 2. 查询分析状态

```http
GET /api/v1/books/analyze/{analysis_id}

Response 200:
{
    "id": "uuid",
    "status": "completed",  // pending/processing/completed/failed
    "progress": 100,
    "book_title": "三体",
    "completed_at": "2025-10-26T10:30:00Z",
    "result": {
        "structure_analysis": {...},
        "technique_analysis": {...},
        "content_extraction": {...}
    }
}
```

### 3. 获取拆书报告

```http
GET /api/v1/books/analyze/{analysis_id}/report

Response 200:
{
    "book_info": {
        "title": "三体",
        "author": "刘慈欣",
        "words": 150000,
        "chapters": 20
    },
    "analysis": {
        "structure": {...},
        "techniques": {...},
        "extractions": {...}
    },
    "knowledge_items": [  // 已保存到知识库的条目
        {
            "id": "uuid",
            "title": "黑暗森林法则",
            "category": "worldview"
        }
    ]
}
```

### 4. 保存到知识库

```http
POST /api/v1/books/analyze/{analysis_id}/save-to-knowledge

Request:
{
    "selections": [
        {
            "type": "worldview",
            "content": "黑暗森林法则: 宇宙就是一座黑暗森林...",
            "tags": ["科幻设定", "宇宙法则"]
        },
        {
            "type": "technique",
            "content": "悬念铺垫技巧: 在第3章埋下伏笔...",
            "tags": ["写作技巧", "悬念"]
        }
    ]
}

Response 200:
{
    "saved_count": 2,
    "knowledge_ids": ["uuid1", "uuid2"]
}
```

### 5. 批量分析书籍

```http
POST /api/v1/books/batch-analyze
Content-Type: multipart/form-data

Request:
{
    "files": [<binary1>, <binary2>, <binary3>],
    "analysis_type": "content",
    "extract_common": true  // 提取共性规律
}

Response 200:
{
    "batch_id": "uuid",
    "total_books": 3,
    "status": "processing"
}
```

---

## 📅 开发计划

### ✅ Phase 1: MVP基础版 (已完成 - 2025-10-27)

**Day 1-2: 数据模型 + 文件解析**
- ✅ 设计 `book_analysis` 表
- ✅ 实现 PDF/TXT 解析服务
- ✅ 章节切分算法

**Day 3-4: AI分析服务**
- ✅ 实现11维度网文分析策略 (`web_novel_11d`)
- ✅ 实现 `BookAnalyzerService`
- ✅ 设计分析Prompt模板
- ✅ 智能建议生成系统

**Day 5: API开发**
- ✅ 实现上传、查询、报告接口 (7个端点)
- ✅ 集成后台任务处理

**Day 6-7: 测试与优化**
- ✅ 自动化测试 (test_book_analysis_auto.py)
- ✅ 端到端测试 (100%通过)
- ✅ 调试日志输出

**完成状态**:
- ✅ 11维度分析策略完整实现
- ✅ 智能建议生成 (6种类型)
- ✅ 7个API端点全部可用
- ✅ 自动化测试100%通过
- ✅ 详细文档和实施总结

### 📋 Phase 2: 知识库集成 (进行中)

**Day 1: 数据打通**
- ✅ 拆书结果保存到 `knowledge_items`
- ✅ 自动分类和标签

**Day 2: 智能推荐**
- ✅ 基于拆书内容推荐相关素材
- ✅ 向量检索集成

**Day 3: 前端开发**
- ✅ 拆书报告展示页面
- ✅ 一键保存到知识库

### Phase 3: LangChain增强 (可选，3-5天)

详见下节

---

## 🚀 LangChain增强方案

### 场景1: 对话式拆书

**功能:**
```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# 用户上传《三体》后
user: "这本书的悬念是怎么设计的?"
ai: "《三体》主要使用了三层悬念: 1) 倒计时的真相..."

user: "第一层悬念在哪几章揭示?"
ai: "第一层悬念在第5章开始揭示，叶文洁发现了..."

user: "和《盗梦空间》的悬念手法有什么不同?"
ai: [对比分析两部作品]
```

**实现:**
```python
# backend/app/services/ai/conversational_book_analyzer.py
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma

class ConversationalBookAnalyzer:
    def __init__(self, book_analysis_id: str):
        # 1. 加载书籍文本到向量库
        self.vectorstore = self._load_book_to_vectorstore(book_analysis_id)

        # 2. 创建对话记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # 3. 创建对话链
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=openai_llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            memory=self.memory
        )

    async def ask(self, question: str) -> str:
        """多轮对话式分析"""
        response = await self.chain.ainvoke({"question": question})
        return response["answer"]
```

**API:**
```http
POST /api/v1/books/analyze/{analysis_id}/chat

Request:
{
    "question": "这本书的悬念是怎么设计的?"
}

Response:
{
    "answer": "《三体》主要使用了三层悬念...",
    "sources": [
        {"chapter": 3, "text": "..."},
        {"chapter": 5, "text": "..."}
    ]
}
```

### 场景2: 批量对比分析

**功能:**
```
用户上传5本武侠小说 → AI自动对比分析:
1. 武功体系设定的异同
2. 人物塑造手法的差异
3. 情节推进节奏的对比
4. 生成"武侠小说创作规律总结"
```

**实现:**
```python
from langchain.chains import MapReduceDocumentsChain

class BatchBookComparator:
    async def compare_books(self, book_ids: List[str], aspect: str):
        """批量对比分析"""
        # 1. 加载所有书籍
        docs = [self._load_book(id) for id in book_ids]

        # 2. Map阶段: 分析每本书
        map_results = await self._map_analyze(docs, aspect)

        # 3. Reduce阶段: 综合对比
        comparison = await self._reduce_compare(map_results)

        return comparison
```

### 场景3: 自动生成学习笔记

**功能:**
```
上传《三体》→ AI自动生成结构化学习笔记:

# 《三体》写作技法学习笔记

## 一、科幻设定构建
### 1.1 技术细节真实性
- 使用真实物理理论增强可信度
- 案例: 智子的二维展开 (第12章)

### 1.2 概念引入节奏
- 先引入现象，后解释原理
- 案例: 倒计时→三体游戏→真相揭示

## 二、悬念铺垫技巧
...
```

**实现:**
```python
from langchain.chains import LLMChain

async def generate_study_notes(book_analysis_id: str):
    prompt = PromptTemplate("""
    基于以下书籍分析结果，生成结构化学习笔记：

    书籍: {book_title}
    分析: {analysis}

    要求:
    1. Markdown格式
    2. 按技法分类
    3. 每个技法配案例
    4. 标注章节位置
    """)

    chain = LLMChain(llm=openai_llm, prompt=prompt)
    notes = await chain.ainvoke({...})
    return notes
```

---

## 📊 预期效果

### 用户价值
1. **学习效率提升**: 传统阅读一本书需要5-10小时，AI拆书15分钟出结果
2. **素材积累**: 自动提取可复用素材，建立个人创作资料库
3. **技能提升**: 快速掌握优秀作家的写作技法

### 商业价值
1. **差异化竞争**: 市面上少有AI拆书功能
2. **用户粘性**: 知识库沉淀用户资产
3. **付费转化**: 可设置拆书次数限制，引导付费

---

## 🔗 相关文档

- [个人知识库功能设计](./16-feature-knowledge-base.md)
- [向量存储服务](../backend/app/services/vector_store_service.py)
- [小说分析编排器](../backend/app/services/ai/novel_analysis_orchestrator.py)
- [LangChain引入时机分析](../LangChain加入的时机.md)

---

**维护者**: NovelAIde 开发团队
**最后更新**: 2025-10-27
**版本**: v2.0
**状态**: ✅ MVP版本已完成并测试通过

**相关文档**:
- [AI拆书功能实施总结](./AI拆书功能实施总结_2025-10-27.md) ⭐ 必读
- [自动化测试脚本](../backend/tests/test_book_analysis_auto.py)
- [测试日志](../INFO.md)
