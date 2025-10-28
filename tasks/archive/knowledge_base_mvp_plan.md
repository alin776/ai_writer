# 个人知识库 MVP - 开发计划

> **创建时间**: 2025-10-26
> **优先级**: ⭐⭐⭐⭐⭐ (最高优先级，基础设施)
> **预计工期**: 5天 (MVP版本)
> **状态**: 规划中 → 待确认

---

## 📋 功能概述

### 核心定位

个人知识库是一个**AI增强的写作素材管理系统**，帮助作者：
- 📝 收集管理灵感、金句、设定、人物卡等写作素材
- 🔍 基于RAG的语义搜索，快速找到需要的内容
- 🔗 自动发现素材间的关联，激发创意组合
- 🎨 跨作品复用世界观和设定

### 战略意义

- 🎯 **用户粘性最强的功能** - 数据积累越多，迁移成本越高
- 🚀 **差异化竞争力** - 市面上少有的AI增强知识库
- 💎 **长期价值沉淀** - 帮助用户建立个人创作资产库
- 🔗 **功能协同效应** - 为AI拆书功能提供存储基础

---

## 🎯 MVP 功能范围

### ✅ MVP 包含功能 (Week 1)

#### 1. 基础CRUD (Day 1-2)
- ✅ 创建知识条目 (标题/内容/分类/标签)
- ✅ 查看知识条目详情
- ✅ 编辑知识条目
- ✅ 删除知识条目
- ✅ 列表查询 (分页/排序/过滤)

#### 2. 分类管理 (Day 1)
- ✅ 7大分类系统：
  - CHARACTER (人物设定)
  - WORLDVIEW (世界观)
  - PLOT (情节灵感)
  - DIALOGUE (对话金句)
  - DESCRIPTION (场景描写)
  - TECHNIQUE (写作技巧)
  - REFERENCE (参考资料)
  - OTHER (其他)

#### 3. 标签系统 (Day 2)
- ✅ 手动添加标签
- ✅ 标签数组存储
- ✅ 按标签过滤

#### 4. 来源追踪 (Day 2)
- ✅ 4种来源类型：
  - MANUAL (手动创建)
  - BOOK_ANALYSIS (AI拆书)
  - AI_GENERATED (AI生成)
  - IMPORTED (导入)
- ✅ 来源引用字段 (书名/网址等)

#### 5. 关联作品 (Day 2)
- ✅ 可选关联到作品 (work_id)
- ✅ 可选关联到章节 (chapter_id)
- ✅ 支持不关联任何作品 (通用素材库)

#### 6. 语义搜索 (Day 3-4) ⭐核心功能
- ✅ RAG向量检索 (基于pgvector)
- ✅ 混合检索 (关键词 + 语义)
- ✅ 多维过滤 (分类/标签/时间/作品)
- ✅ Top-K结果返回
- ✅ 相关性评分

#### 7. 前端UI (Day 5)
- ✅ 知识库列表页 (卡片/列表视图切换)
- ✅ 创建/编辑表单
- ✅ 智能搜索界面
- ✅ 详情展示页
- ✅ 分类/标签过滤器

### ⏳ 延后功能 (Week 2)

#### AI增强功能
- ⏳ AI自动摘要生成
- ⏳ AI智能标签提取
- ⏳ AI自动分类建议
- ⏳ 相关素材推荐
- ⏳ 创意组合建议

#### 高级功能
- ⏳ 批量导入 (CSV/JSON/Markdown)
- ⏳ 统计仪表板
- ⏳ 编辑器快速引用 (Slash命令/AI菜单)
- ⏳ 可视化关联图

---

## 🗂️ 数据模型设计

### 核心表: knowledge_items

```python
class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"

    # 主键
    id = UUID(primary_key=True, default=uuid4)
    user_id = UUID(ForeignKey("users.id"), nullable=False, index=True)

    # 基本信息
    title = String(200, nullable=False, index=True)
    content = Text(nullable=False)
    summary = Text(nullable=True)  # MVP可为空，Week 2 AI生成

    # 分类和标签
    category = Enum(KnowledgeCategory, nullable=False, index=True)
    tags = ARRAY(String, default=[], nullable=False)

    # 来源信息
    source_type = Enum(KnowledgeSource, default=KnowledgeSource.MANUAL)
    source_id = UUID(nullable=True)  # 来源ID (如book_analysis_id)
    source_reference = String(500, nullable=True)  # 来源描述

    # 关联作品 (可选)
    work_id = UUID(ForeignKey("works.id"), nullable=True)
    chapter_id = UUID(ForeignKey("chapters.id"), nullable=True)

    # 扩展信息
    metadata = JSONB(default={})  # 灵活存储额外信息

    # 使用统计
    view_count = Integer(default=0)
    reference_count = Integer(default=0)

    # 时间戳
    created_at = DateTime(timezone=True, server_default=func.now())
    updated_at = DateTime(timezone=True, onupdate=func.now())
    last_accessed_at = DateTime(timezone=True, nullable=True)
```

### 向量存储 (复用现有)

```python
# 扩展现有的 novel_analysis_vectors 表
# source_type 新增支持: "knowledge"
# source_id 指向: knowledge_item.id
```

---

## 🔌 API 接口设计

### 核心接口 (MVP必需)

#### 1. 创建知识条目
```http
POST /api/v1/knowledge
Authorization: Bearer <token>

Request:
{
    "title": "修仙境界体系",
    "content": "练气 → 筑基 → 金丹 → 元婴...",
    "category": "worldview",
    "tags": ["修仙", "境界体系"],
    "source_reference": "参考《凡人修仙传》",
    "work_id": "uuid",  // 可选
    "metadata": {}      // 可选
}

Response 201:
{
    "id": "uuid",
    "title": "修仙境界体系",
    "category": "worldview",
    "tags": ["修仙", "境界体系"],
    "created_at": "2025-10-26T10:00:00Z"
}
```

#### 2. 列表查询 (支持过滤)
```http
GET /api/v1/knowledge?category=worldview&tags=修仙&page=1&page_size=20

Response 200:
{
    "items": [
        {
            "id": "uuid",
            "title": "修仙境界体系",
            "summary": "完整的修仙境界划分...",
            "category": "worldview",
            "tags": ["修仙", "境界体系"],
            "created_at": "2025-10-26T10:00:00Z",
            "reference_count": 5
        }
    ],
    "total": 100,
    "page": 1,
    "page_size": 20
}
```

#### 3. 语义搜索 (RAG核心)
```http
POST /api/v1/knowledge/search

Request:
{
    "query": "帮我找修仙境界的设定",
    "category": "worldview",  // 可选
    "tags": ["修仙"],         // 可选
    "work_id": "uuid",        // 可选
    "top_k": 10
}

Response 200:
{
    "results": [
        {
            "item": {
                "id": "uuid",
                "title": "修仙境界体系",
                "content": "...",
                "category": "worldview",
                "tags": ["修仙", "境界体系"]
            },
            "relevance_score": 0.95,
            "highlight": "...境界划分为九重天..."
        }
    ]
}
```

#### 4. 获取详情
```http
GET /api/v1/knowledge/{id}

Response 200:
{
    "id": "uuid",
    "title": "修仙境界体系",
    "content": "完整内容...",
    "category": "worldview",
    "tags": ["修仙", "境界体系"],
    "source_reference": "参考《凡人修仙传》",
    "created_at": "2025-10-26T10:00:00Z",
    "updated_at": "2025-10-26T11:00:00Z",
    "view_count": 10,
    "reference_count": 5
}
```

#### 5. 更新知识条目
```http
PUT /api/v1/knowledge/{id}

Request:
{
    "title": "更新后的标题",
    "content": "更新后的内容",
    "tags": ["新标签"]
}

Response 200:
{
    "id": "uuid",
    "updated_at": "2025-10-26T12:00:00Z"
}
```

#### 6. 删除知识条目
```http
DELETE /api/v1/knowledge/{id}

Response 204: No Content
```

---

## 📅 5天开发计划

### Day 1: 数据模型与数据库迁移 (2025-10-27)

#### 任务清单
- [ ] 创建 `backend/app/models/knowledge_item.py`
  - [ ] 定义 `KnowledgeCategory` 枚举
  - [ ] 定义 `KnowledgeSource` 枚举
  - [ ] 定义 `KnowledgeItem` 模型
- [ ] 更新 `backend/app/models/__init__.py` (导入新模型)
- [ ] 更新关联模型的反向关系
  - [ ] `User.knowledge_items`
  - [ ] `Work.knowledge_items`
  - [ ] `Chapter.knowledge_items`
- [ ] 生成 Alembic 迁移文件
  ```bash
  python -m alembic revision --autogenerate -m "add_knowledge_items_table"
  ```
- [ ] 检查生成的迁移文件
- [ ] 执行数据库迁移
  ```bash
  python -m alembic upgrade head
  ```
- [ ] 验证表创建成功

#### 交付物
- ✅ `knowledge_items` 表创建成功
- ✅ 枚举类型创建成功
- ✅ 外键关系正确

---

### Day 2: Schema与向量服务扩展 (2025-10-28)

#### 任务清单
- [ ] 创建 `backend/app/schemas/knowledge.py`
  - [ ] `KnowledgeItemCreate` (创建请求)
  - [ ] `KnowledgeItemUpdate` (更新请求)
  - [ ] `KnowledgeItemResponse` (响应)
  - [ ] `KnowledgeItemList` (列表响应)
  - [ ] `KnowledgeSearchRequest` (搜索请求)
  - [ ] `KnowledgeSearchResponse` (搜索响应)
- [ ] 扩展 `backend/app/services/vector_store_service.py`
  - [ ] `add_knowledge(item: KnowledgeItem)` - 添加向量
  - [ ] `search_knowledge(query: str, user_id: str, top_k: int)` - 搜索向量
  - [ ] `update_knowledge_vector(item_id: str)` - 更新向量
  - [ ] `delete_knowledge_vector(item_id: str)` - 删除向量
- [ ] 单元测试
  - [ ] 测试向量生成
  - [ ] 测试向量检索准确性

#### 交付物
- ✅ Schema定义完整
- ✅ 向量服务扩展完成
- ✅ 向量检索功能正常

---

### Day 3: 后端服务层 CRUD (2025-10-29)

#### 任务清单
- [ ] 创建 `backend/app/services/knowledge_service.py`
  - [ ] `create_item()` - 创建条目 + 生成向量
  - [ ] `get_item()` - 获取单个条目
  - [ ] `get_items()` - 列表查询 (支持过滤/分页/排序)
  - [ ] `update_item()` - 更新条目 + 更新向量
  - [ ] `delete_item()` - 删除条目 + 删除向量
  - [ ] `search_by_semantic()` - 语义搜索
  - [ ] `increment_view_count()` - 增加查看次数
  - [ ] `increment_reference_count()` - 增加引用次数
- [ ] 单元测试
  - [ ] 测试CRUD操作
  - [ ] 测试过滤/排序
  - [ ] 测试语义搜索

#### 交付物
- ✅ KnowledgeService 完整实现
- ✅ 单元测试通过 (覆盖率 > 80%)

---

### Day 4: 后端API层与测试数据 (2025-10-30)

#### 任务清单
- [ ] 创建 `backend/app/api/v1/knowledge.py`
  - [ ] `POST /api/v1/knowledge` - 创建
  - [ ] `GET /api/v1/knowledge` - 列表查询
  - [ ] `GET /api/v1/knowledge/{id}` - 详情
  - [ ] `PUT /api/v1/knowledge/{id}` - 更新
  - [ ] `DELETE /api/v1/knowledge/{id}` - 删除
  - [ ] `POST /api/v1/knowledge/search` - 语义搜索
- [ ] 更新 `backend/app/api/__init__.py` (注册路由)
- [ ] 创建测试数据
  - [ ] 更新 `backend/tests/conftest.py` (添加 `create_test_knowledge_item`)
  - [ ] 创建 `backend/scripts/seed_knowledge_data.py` (8条示例数据)
- [ ] API测试
  - [ ] 测试所有端点
  - [ ] 测试权限验证
  - [ ] 测试错误处理

#### 交付物
- ✅ 6个API端点完整实现
- ✅ API测试通过
- ✅ 测试数据脚本可用

---

### Day 5: 前端开发 (2025-10-31)

#### 任务清单
- [ ] 创建前端组件
  - [ ] `KnowledgeList.tsx` - 列表页
  - [ ] `KnowledgeCard.tsx` - 卡片组件
  - [ ] `KnowledgeForm.tsx` - 创建/编辑表单
  - [ ] `KnowledgeDetail.tsx` - 详情页
  - [ ] `KnowledgeSearch.tsx` - 搜索界面
  - [ ] `KnowledgeFilters.tsx` - 过滤器
- [ ] 前端路由
  - [ ] `/knowledge` - 列表页
  - [ ] `/knowledge/new` - 创建页
  - [ ] `/knowledge/:id` - 详情页
  - [ ] `/knowledge/:id/edit` - 编辑页
- [ ] 侧边栏导航
  - [ ] 添加"📚 知识库"一级导航
- [ ] 状态管理
  - [ ] `useKnowledgeStore` (Zustand)
- [ ] API集成
  - [ ] 调用后端API
  - [ ] 错误处理
  - [ ] 加载状态
- [ ] 端到端测试
  - [ ] 测试完整流程

#### 交付物
- ✅ 前端UI完整实现
- ✅ CRUD操作正常
- ✅ 搜索功能正常
- ✅ 端到端测试通过

---

## 🎨 前端UI设计

### 入口位置

```
侧边栏 (一级导航):
├── 📝 作品列表
├── 🌍 世界观
├── 📚 知识库 (新增) ← MVP入口
└── ⚙️ 设置
```

### 页面结构

#### 1. 知识库列表页 `/knowledge`

```
┌─────────────────────────────────────────────────┐
│ 📚 个人知识库                          [+ 新建]  │
├─────────────────────────────────────────────────┤
│ 🔍 [搜索框: 语义搜索...]         [过滤器 ▼]     │
├─────────────────────────────────────────────────┤
│ 分类: [全部] [人物] [世界观] [情节] ...         │
│ 标签: [修仙] [武侠] [科幻] ...                  │
├─────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────┐     │
│ │ 📖 修仙境界体系                          │     │
│ │ 世界观 | 修仙, 境界体系                   │     │
│ │ 练气 → 筑基 → 金丹 → 元婴...            │     │
│ │ 2025-10-26 | 引用 5次                    │     │
│ └─────────────────────────────────────────┘     │
│                                                  │
│ ┌─────────────────────────────────────────┐     │
│ │ ⚔️ 剑法描写 - 一剑光寒                   │     │
│ │ 场景描写 | 武侠, 剑法, 动作戏            │     │
│ │ 他缓缓拔剑，剑身未出鞘...                │     │
│ │ 2025-10-26 | 引用 3次                    │     │
│ └─────────────────────────────────────────┘     │
│                                                  │
│ [分页: 1 2 3 ... 10]                            │
└─────────────────────────────────────────────────┘
```

#### 2. 创建/编辑页 `/knowledge/new`

```
┌─────────────────────────────────────────────────┐
│ [← 返回] 新建知识条目                            │
├─────────────────────────────────────────────────┤
│ 标题: [________________]                         │
│                                                  │
│ 分类: [世界观 ▼]                                 │
│                                                  │
│ 标签: [修仙] [境界体系] + 添加标签               │
│                                                  │
│ 内容:                                            │
│ ┌──────────────────────────────────────────┐    │
│ │ [富文本编辑器]                            │    │
│ │                                           │    │
│ │                                           │    │
│ │                                           │    │
│ └──────────────────────────────────────────┘    │
│                                                  │
│ 来源: [手动创建 ▼]                               │
│ 来源说明: [可选: 书名/网址/...]                  │
│                                                  │
│ 关联作品: [可选: 选择作品 ▼]                     │
│                                                  │
│ [取消]                             [保存]        │
└─────────────────────────────────────────────────┘
```

#### 3. 搜索界面 (语义搜索)

```
┌─────────────────────────────────────────────────┐
│ 🔍 智能搜索                                      │
├─────────────────────────────────────────────────┤
│ [帮我找修仙境界的设定___________] [搜索]         │
│                                                  │
│ 筛选: □ 仅搜索当前作品                           │
│       分类: [世界观 ▼]  标签: [修仙 ▼]          │
├─────────────────────────────────────────────────┤
│ 找到 3 个相关结果:                               │
│                                                  │
│ ┌─────────────────────────────────────────┐     │
│ │ 📖 修仙境界体系         相关度: 95%      │     │
│ │ 世界观 | 修仙, 境界体系                   │     │
│ │ "...境界划分为九重天..."                 │     │
│ │ [查看详情] [引用到编辑器]                │     │
│ └─────────────────────────────────────────┘     │
│                                                  │
│ ┌─────────────────────────────────────────┐     │
│ │ 📖 灵气等级划分         相关度: 88%      │     │
│ │ 世界观 | 修仙, 灵气                       │     │
│ │ "...灵气浓度决定修炼速度..."             │     │
│ │ [查看详情] [引用到编辑器]                │     │
│ └─────────────────────────────────────────┘     │
└─────────────────────────────────────────────────┘
```

---

## 🔧 技术实现细节

### 1. 向量服务扩展

```python
# backend/app/services/vector_store_service.py

class VectorStoreService:
    # ... 现有代码 ...

    async def add_knowledge(self, item: KnowledgeItem):
        """添加知识到向量库"""
        # 生成文本表示 (标题 + 内容 + 标签)
        text = f"{item.title}\n{item.content}\n标签:{','.join(item.tags)}"

        # 生成embedding
        embedding = self._get_model().encode(text).tolist()

        # 存储向量
        vector = NovelAnalysisVector(
            user_id=item.user_id,
            source_type="knowledge",  # 新增类型
            source_id=str(item.id),
            content_text=text,
            embedding=embedding
        )
        self.db.add(vector)
        await self.db.commit()

    async def search_knowledge(
        self,
        query: str,
        user_id: str,
        top_k: int = 10
    ) -> List[dict]:
        """搜索知识库"""
        # 1. 生成查询向量
        query_embedding = self._get_model().encode(query).tolist()

        # 2. 向量相似度搜索 (pgvector)
        stmt = select(
            NovelAnalysisVector,
            func.cosine_similarity(
                NovelAnalysisVector.embedding,
                query_embedding
            ).label('similarity')
        ).where(
            and_(
                NovelAnalysisVector.user_id == user_id,
                NovelAnalysisVector.source_type == "knowledge"
            )
        ).order_by(
            desc('similarity')
        ).limit(top_k)

        results = await self.db.execute(stmt)

        return [
            {
                'source_id': row.NovelAnalysisVector.source_id,
                'similarity': row.similarity,
                'text': row.NovelAnalysisVector.content_text
            }
            for row in results
        ]
```

### 2. CRUD服务

```python
# backend/app/services/knowledge_service.py

class KnowledgeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vector_service = VectorStoreService(db)

    async def create_item(
        self,
        user_id: str,
        data: KnowledgeItemCreate
    ) -> KnowledgeItem:
        """创建知识条目"""
        # 1. 创建条目
        item = KnowledgeItem(
            user_id=user_id,
            **data.dict()
        )
        self.db.add(item)
        await self.db.flush()

        # 2. 生成并存储向量
        await self.vector_service.add_knowledge(item)

        await self.db.commit()
        return item

    async def search_by_semantic(
        self,
        user_id: str,
        query: str,
        category: Optional[KnowledgeCategory] = None,
        tags: Optional[List[str]] = None,
        top_k: int = 10
    ) -> List[dict]:
        """语义搜索"""
        # 1. 向量检索
        vector_results = await self.vector_service.search_knowledge(
            query=query,
            user_id=user_id,
            top_k=top_k * 2  # 多取一些，过滤后再截断
        )

        # 2. 加载完整条目 + 过滤
        items = []
        for result in vector_results:
            item = await self.get_by_id(result['source_id'])

            # 分类过滤
            if category and item.category != category:
                continue

            # 标签过滤
            if tags and not any(tag in item.tags for tag in tags):
                continue

            items.append({
                'item': item,
                'relevance_score': result['similarity'],
                'highlight': self._extract_highlight(item.content, query)
            })

            if len(items) >= top_k:
                break

        return items

    def _extract_highlight(self, content: str, query: str) -> str:
        """提取相关片段 (简单实现)"""
        # TODO: 可以用更智能的方式提取
        return content[:100] + "..."
```

---

## ✅ 验收标准

### 后端验收

- [ ] 所有API端点返回正确的状态码
- [ ] 数据模型字段验证正确
- [ ] 向量检索准确率 > 80%
- [ ] 单元测试覆盖率 > 80%
- [ ] API性能: 列表查询 < 200ms, 搜索 < 500ms

### 前端验收

- [ ] UI符合设计规范
- [ ] CRUD操作流畅无卡顿
- [ ] 搜索结果实时展示
- [ ] 响应式布局 (桌面端)
- [ ] 错误提示友好

### 功能验收

- [ ] 用户可以创建/编辑/删除知识条目
- [ ] 分类和标签系统正常工作
- [ ] 语义搜索能找到相关内容
- [ ] 列表过滤和排序正常
- [ ] 测试数据脚本可用

---

## 🚀 后续规划 (Week 2)

### AI增强功能
- AI自动摘要生成
- AI智能标签提取
- AI自动分类建议
- 相关素材推荐
- 创意组合建议

### 高级功能
- 批量导入/导出
- 统计仪表板
- 编辑器快速引用集成
- 可视化关联图

### 性能优化
- 向量检索缓存
- 列表查询优化
- 前端虚拟滚动

---

## 📝 风险与应对

### 风险1: 向量检索准确率不高
**应对**:
- 优化文本预处理 (去除标点、分词)
- 调整向量相似度阈值
- 增加混合检索 (关键词 + 向量)

### 风险2: 开发进度延期
**应对**:
- 严格按MVP范围开发
- AI增强功能可延后
- 前端UI可简化

### 风险3: 用户不理解语义搜索
**应对**:
- 添加使用提示
- 提供示例查询
- 同时支持关键词搜索

---

## 📚 相关文档

- [个人知识库功能设计](../docs/16-feature-knowledge-base.md)
- [开发路线图 - Milestone 2.5](../docs/04-milestones.md)
- [向量存储服务](../backend/app/services/vector_store_service.py)

---

**创建者**: AI Assistant
**最后更新**: 2025-10-26
**版本**: v1.0
**状态**: 等待用户确认 ✋
