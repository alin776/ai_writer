# Context-Aware 自动补全设计方案

## 📋 目标

将自动补全从"盲目续写"升级为"智能创作助手"，利用项目已有的丰富元数据资源，提供上下文感知的智能补全。

---

## 🎯 核心思路

### 当前问题
- 自动补全只使用最近 200 字符的上下文
- 不了解小说的世界观、人物、力量体系等设定
- 容易出现与设定冲突的内容
- 无法保持人物性格一致性

### 解决方案
利用项目已有的 3 层元数据资源：
1. **作品级元数据**：AI创作规范、世界观、力量体系
2. **章节级元数据**：章节概要、剧情发展
3. **实时 RAG 检索**：相关人物、场景、事件信息

---

## 🗂️ 可用资源清单

### 1. AI Guidelines（创作规范）
**数据表**: `ai_guidelines`
**关联**: Work (一对一)

**包含字段**（32个）：
```python
# 创作规范部分
- business_goal          # 商业目标
- target_audience        # 目标读者
- high_concept          # 高概念卖点
- core_paradox          # 核心悖论/设定
- dominant_emotion      # 主导情感
- protagonist_arc       # 主角弧光
- core_conflict         # 核心关系冲突
- narrative_rhythm      # 叙事节奏
- writing_style         # 文笔风格
- style_notes           # 文风注意事项
- chapter_length        # 章节长度
- content_taboos        # 内容禁忌

# 核心设定部分
- primary_genre         # 一级类型（玄幻/都市/科幻等）
- secondary_tags        # 二级标签
- creative_tone         # 创作基调
- world_intro           # 核心世界观简介
- main_locations        # 主要场景/地点
- world_rules           # 世界规则
- power_system_name     # 力量体系名称与原理
- power_levels          # 等级划分
- power_cost            # 能力获取与代价
- protagonist_name      # 主角姓名/代号
- protagonist_identity  # 核心身份
- protagonist_traits    # 强化缺陷与能力
- protagonist_goal      # 核心目标与动机
- conflict_design       # 冲突点设计
- act_one/two/three     # 三幕剧情
```

### 2. 章节元数据
**数据表**: `chapters`

```python
- title          # 章节标题
- summary        # 章节剧情概括（AI生成）
- order          # 章节顺序
- content        # 章节正文
```

### 3. 人物数据
**数据表**: `characters`

```python
- name           # 人物姓名
- description    # 人物描述
- role           # 角色定位（主角/配角/反派）
- tags           # 标签（JSON）
- relationships  # 关系（JSON）
```

### 4. RAG 向量检索系统
**服务**: `VectorStoreService`
**数据表**: `novel_analysis_vectors`

**功能**：
- 存储章节的微观分析向量（384维）
- 支持语义检索相关内容
- 自动提取人物、场景、事件信息

**检索方法**：
```python
async def retrieve_relevant_analysis(
    work_id: str,
    query: str,           # 查询文本
    top_k: int = 5,       # 返回前K个结果
    similarity_threshold: float = 0.5
) -> List[Dict]:          # 返回相关分析结果
```

---

## 🏗️ 技术架构设计

### 方案架构图

```
用户输入 → 前端编辑器
    ↓
触发自动补全 (6秒停顿 + 句末)
    ↓
前端发送请求 {
    context: "最近500字",
    work_id: "作品ID",
    chapter_id: "当前章节ID"
}
    ↓
后端 AI Service
    ↓
┌─────────────────────────────────────┐
│  Context Enhancement Layer          │
│  (上下文增强层 - 新增)               │
├─────────────────────────────────────┤
│ 1. 加载 AI Guidelines               │
│    ✓ 写作风格、叙事节奏              │
│    ✓ 主角设定、力量体系              │
│    ✓ 世界观规则                     │
│                                     │
│ 2. 加载章节元数据                   │
│    ✓ 当前章节概要                   │
│    ✓ 前1-2章概要（上下文）           │
│                                     │
│ 3. RAG 智能检索 (可选)              │
│    ✓ 提取人物名                     │
│    ✓ 检索人物设定                   │
│    ✓ 检索相关场景/事件              │
└─────────────────────────────────────┘
    ↓
构建增强 System Prompt
    ↓
调用 LLM (max_tokens=100)
    ↓
返回补全建议
```

---

## 💡 实现方案

### 阶段一：基础元数据注入（优先级 ⭐⭐⭐）

**改动最小，效果最明显**

#### 1.1 修改 AI Service

**文件**: `backend/app/services/ai/http_ai_service.py`

```python
async def stream_complete(
    self,
    context: str,
    prompt: str = "续写",
    style: str = "",
    max_tokens: int = 500,
    temperature: float = 0.7,
    # ===== 新增参数 =====
    work_id: str = None,
    chapter_id: str = None,
    enable_rag: bool = False  # 是否启用RAG检索
) -> AsyncGenerator[tuple[str, dict | None], None]:
    """AI 续写（流式响应）"""

    is_autocomplete = max_tokens <= 150

    # ===== 构建增强的 system prompt =====
    if is_autocomplete:
        system_prompt = await self._build_enhanced_autocomplete_prompt(
            work_id, chapter_id, context, enable_rag
        )
    else:
        system_prompt = self._build_complete_system_prompt(prompt, style)

    # ... 继续原有逻辑
```

#### 1.2 新增方法：构建增强提示词

```python
async def _build_enhanced_autocomplete_prompt(
    self,
    work_id: str,
    chapter_id: str,
    context: str,
    enable_rag: bool = False
) -> str:
    """构建增强的自动补全提示词"""

    # 基础提示词
    base_prompt = self._build_autocomplete_system_prompt()

    # 如果没有work_id，返回基础版本
    if not work_id:
        return base_prompt

    enhancements = []

    # ===== 1. 加载 AI Guidelines（最重要） =====
    try:
        from app.services.ai_guidelines_service import AIGuidelinesService
        guidelines_service = AIGuidelinesService(self.db)
        guidelines = await guidelines_service.get_by_work_id(work_id)

        if guidelines:
            # 提取关键元数据
            metadata_parts = []

            # 文笔风格（最重要）
            if guidelines.writing_style:
                metadata_parts.append(f"文笔风格: {guidelines.writing_style}")

            # 叙事节奏
            if guidelines.narrative_rhythm:
                metadata_parts.append(f"叙事节奏: {guidelines.narrative_rhythm}")

            # 主角基本信息
            if guidelines.protagonist_name:
                protag_info = f"主角: {guidelines.protagonist_name}"
                if guidelines.protagonist_traits:
                    protag_info += f"({guidelines.protagonist_traits})"
                metadata_parts.append(protag_info)

            # 力量体系
            if guidelines.power_system_name:
                metadata_parts.append(f"力量体系: {guidelines.power_system_name}")

            # 世界规则
            if guidelines.world_rules:
                metadata_parts.append(f"世界规则: {guidelines.world_rules}")

            # 内容禁忌
            if guidelines.content_taboos:
                metadata_parts.append(f"禁忌: {guidelines.content_taboos}")

            if metadata_parts:
                enhancements.append("【作品设定】\n" + "\n".join(metadata_parts))

    except Exception as e:
        logger.warning(f"加载AI Guidelines失败: {e}")

    # ===== 2. 加载章节概要（提供剧情上下文） =====
    if chapter_id:
        try:
            from app.services.chapter_service import ChapterService
            chapter_service = ChapterService(self.db)

            # 当前章节概要
            current_chapter = await chapter_service.get_chapter(chapter_id)
            if current_chapter and current_chapter.summary:
                enhancements.append(f"【本章剧情】\n{current_chapter.summary}")

            # 获取前一章概要（可选）
            if current_chapter and current_chapter.order > 1:
                previous_chapter = await chapter_service.get_chapter_by_order(
                    work_id, current_chapter.order - 1
                )
                if previous_chapter and previous_chapter.summary:
                    enhancements.append(f"【上章剧情】\n{previous_chapter.summary}")

        except Exception as e:
            logger.warning(f"加载章节概要失败: {e}")

    # ===== 3. RAG 检索（可选，默认关闭） =====
    if enable_rag and work_id:
        try:
            # 提取人物名（简单正则）
            import re
            # 匹配中文人名（2-4个字）
            names = re.findall(r'[\u4e00-\u9fa5]{2,4}(?:说|道|想|看|听|笑)', context)

            if names:
                from app.services.vector_store_service import VectorStoreService
                vector_service = VectorStoreService(self.db)

                # 检索相关人物设定
                query = f"人物 {' '.join(set(names[:3]))}"  # 取前3个不重复的人名
                relevant_info = await vector_service.retrieve_relevant_analysis(
                    work_id=work_id,
                    query=query,
                    top_k=2,
                    similarity_threshold=0.6
                )

                if relevant_info:
                    rag_parts = []
                    for item in relevant_info:
                        if 'content_text' in item:
                            rag_parts.append(item['content_text'][:200])  # 限制长度

                    if rag_parts:
                        enhancements.append("【相关设定】\n" + "\n".join(rag_parts))

        except Exception as e:
            logger.warning(f"RAG检索失败: {e}")

    # ===== 组装最终提示词 =====
    if not enhancements:
        return base_prompt

    # 限制元数据总长度（避免超过token限制）
    enhanced_context = "\n\n".join(enhancements)
    if len(enhanced_context) > 800:
        enhanced_context = enhanced_context[:800] + "..."

    return f"{base_prompt}\n\n{enhanced_context}"
```

#### 1.3 修改 API 接口

**文件**: `backend/app/api/v1/ai.py`

找到 `/api/v1/ai/complete` 端点，修改为：

```python
@router.post("/complete")
async def ai_complete(
    request: AICompleteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """AI续写（流式响应）"""

    ai_service = HTTPAIService(db=db)

    async def event_generator():
        try:
            async for chunk, usage in ai_service.stream_complete(
                context=request.context,
                prompt=request.prompt,
                style=request.style or "",
                max_tokens=request.max_tokens,
                temperature=request.temperature or 0.7,
                # ===== 新增参数 =====
                work_id=request.work_id,      # 从请求体获取
                chapter_id=request.chapter_id, # 从请求体获取
                enable_rag=request.enable_rag or False
            ):
                # ... 原有SSE逻辑
```

**Schema 更新** (`backend/app/schemas/ai.py`):

```python
class AICompleteRequest(BaseModel):
    context: str
    prompt: str = "续写"
    style: str = ""
    max_tokens: int = 500
    temperature: float = 0.7
    # ===== 新增 =====
    work_id: Optional[str] = None
    chapter_id: Optional[str] = None
    enable_rag: bool = False  # 默认关闭RAG（性能考虑）
```

#### 1.4 修改前端调用

**文件**: `src/services/AIService.ts`

修改 `quickComplete` 方法：

```typescript
/**
 * 快速 AI 补全（用于实时自动补全）
 * @param context - 上下文文本
 * @param workId - 作品ID（可选）
 * @param chapterId - 章节ID（可选）
 */
async quickComplete(
  context: string,
  workId?: string,
  chapterId?: string
): Promise<string> {
  try {
    const result = await this.complete({
      prompt: context,
      context,
      maxTokens: 100,
      // ===== 新增 =====
      workId,
      chapterId,
      enableRag: false  // 自动补全场景默认关闭RAG（速度优先）
    });
    return result.trim();
  } catch (error) {
    console.error('快速补全失败:', error);
    return '';
  }
}
```

修改接口类型定义：

```typescript
export interface AICompletionRequest {
  prompt: string;
  context?: string;
  maxTokens?: number;
  temperature?: number;
  model?: string;
  // ===== 新增 =====
  workId?: string;
  chapterId?: string;
  enableRag?: boolean;
}
```

#### 1.5 在编辑器中传递 work_id 和 chapter_id

**文件**: `src/components/editor/NovelEditor.tsx`

找到 AIAutoCompleteExtension 配置，修改 onTrigger：

```typescript
AIAutoCompleteExtension.configure({
  delay: 6000,
  minChars: 50,
  enabled: true,
  onTrigger: async (text: string) => {
    try {
      // ===== 获取当前作品和章节ID =====
      const workId = /* 从组件props或context获取 */;
      const chapterId = /* 从组件props或context获取 */;

      // 调用带元数据的补全API
      const suggestion = await AIService.quickComplete(
        text,
        workId,
        chapterId
      );

      return suggestion;
    } catch (error) {
      console.error('[AI自动补全] 失败:', error);
      return '';
    }
  },
})
```

---

### 阶段二：智能 RAG 检索（优先级 ⭐⭐）

**进阶功能，性能开销较大**

#### 2.1 优化人物名提取

使用更智能的 NER（命名实体识别）或规则：

```python
def extract_character_names(context: str, guidelines) -> List[str]:
    """从上下文中智能提取人物名"""
    names = []

    # 1. 优先使用主角名（从 guidelines 获取）
    if guidelines and guidelines.protagonist_name:
        protag_name = guidelines.protagonist_name.split('/')[0]  # 处理"张三/小张"格式
        if protag_name in context:
            names.append(protag_name)

    # 2. 正则匹配人名模式
    import re
    # 中文人名 + 动作词
    pattern = r'([\u4e00-\u9fa5]{2,4})(?:说|道|想|看|听|笑|问|答|走|跑|站|坐)'
    matches = re.findall(pattern, context)
    names.extend(matches)

    # 3. 去重并限制数量
    return list(set(names))[:3]
```

#### 2.2 条件化 RAG 触发

只在特定场景下触发 RAG：

```python
def should_trigger_rag(context: str, chapter_summary: str = None) -> bool:
    """判断是否需要触发RAG检索"""

    # 1. 如果出现对话（引号），可能需要人物设定
    if '"' in context or '"' in context or '「' in context:
        return True

    # 2. 如果出现动作描写，可能需要场景信息
    action_keywords = ['走', '进', '来到', '看到', '听到']
    if any(keyword in context[-50:] for keyword in action_keywords):
        return True

    # 3. 如果出现力量/技能相关词汇
    power_keywords = ['施展', '使用', '释放', '修炼', '境界']
    if any(keyword in context for keyword in power_keywords):
        return True

    return False
```

---

### 阶段三：缓存优化（优先级 ⭐）

**减少重复查询，提升性能**

#### 3.1 使用 Redis 缓存元数据

```python
from app.core.redis import get_redis
import json

async def get_cached_guidelines(work_id: str):
    """获取缓存的创作规范"""
    redis = await get_redis()
    cache_key = f"guidelines:{work_id}"

    # 1. 尝试从缓存获取
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # 2. 从数据库查询
    from app.services.ai_guidelines_service import AIGuidelinesService
    service = AIGuidelinesService(db)
    guidelines = await service.get_by_work_id(work_id)

    if guidelines:
        # 3. 序列化并缓存（1小时过期）
        cache_data = {
            "writing_style": guidelines.writing_style,
            "narrative_rhythm": guidelines.narrative_rhythm,
            "protagonist_name": guidelines.protagonist_name,
            # ... 其他字段
        }
        await redis.setex(cache_key, 3600, json.dumps(cache_data))
        return cache_data

    return None
```

---

## 📊 性能影响分析

### 延迟预估

| 操作 | 耗时 | 说明 |
|------|------|------|
| 基础补全（无元数据） | ~500ms | LLM推理时间 |
| + 加载 AI Guidelines | +10ms | 数据库单表查询 |
| + 加载章节概要 | +15ms | 2次数据库查询 |
| + RAG 检索（可选） | +200ms | 向量计算+检索 |
| **总计（不含RAG）** | **~525ms** | ✅ 可接受 |
| **总计（含RAG）** | **~725ms** | ⚠️ 偏慢，建议异步预加载 |

### 优化建议

1. **Guidelines 缓存**：使用 Redis 缓存，避免每次查询
2. **章节概要预加载**：编辑器打开时预加载
3. **RAG 默认关闭**：仅在必要时（对话/战斗场景）启用
4. **Token 限制**：元数据总长度不超过 800 字符

---

## 🎯 推荐实施顺序

### Week 1: 基础版本
✅ 实现阶段一（基础元数据注入）
- 加载 AI Guidelines
- 加载章节概要
- 修改 API 和前端调用
- **预期效果**：补全内容符合作品风格和人设

### Week 2: 性能优化
✅ 实现阶段三（缓存优化）
- Redis 缓存 Guidelines
- 前端预加载章节元数据
- **预期效果**：延迟降低到 ~300ms

### Week 3: 进阶功能（可选）
⭕ 实现阶段二（智能 RAG）
- 人物名智能提取
- 条件化 RAG 触发
- **预期效果**：特殊场景下更准确

---

## 📝 示例效果对比

### Before（无元数据）
```
用户输入：林凡走进拍卖行，看到
AI补全：一个身穿华服的老者站在台上。
```
❌ 问题：不知道林凡的身份、当前情节、拍卖行的世界观设定

### After（有元数据）
```
【作品设定】
文笔风格: 简洁明快，多用短句，节奏紧凑
主角: 林凡（修仙者，性格谨慎，擅长阵法）
力量体系: 修仙境界（炼气→筑基→金丹→元婴）
世界规则: 修仙界拍卖行禁止私斗，由元婴期修士坐镇

【本章剧情】
林凡来到天宝阁拍卖行，准备竞拍筑基丹突破境界

用户输入：林凡走进拍卖行，看到
AI补全：大厅内已经坐满了修士，空气中弥漫着灵气的波动。
```
✅ 改进：符合修仙背景、契合人物身份、延续剧情

---

## 🔧 技术细节

### 数据库查询优化

```python
# 使用 joinedload 预加载关联数据，避免 N+1 查询
from sqlalchemy.orm import joinedload

query = select(Work).options(
    joinedload(Work.ai_guidelines),
    joinedload(Work.chapters)
).where(Work.id == work_id)
```

### Token 预算管理

```python
MAX_METADATA_TOKENS = 200  # 元数据最多占用200 tokens
MAX_CONTEXT_TOKENS = 400   # 用户上下文最多400 tokens
MAX_COMPLETION_TOKENS = 100  # 补全内容100 tokens
# 总计：~700 tokens（安全边界）
```

---

## ✅ 验收标准

1. **功能性**
   - ✅ 补全内容符合作品的文笔风格
   - ✅ 不违反世界观规则（如力量体系）
   - ✅ 保持主角性格一致性

2. **性能**
   - ✅ 平均响应时间 < 600ms（不含RAG）
   - ✅ P95 响应时间 < 1000ms

3. **稳定性**
   - ✅ 元数据缺失时降级为基础补全
   - ✅ 数据库查询失败不影响核心功能

---

## 📚 参考资料

- [项目 AI Guidelines 模型](../../backend/app/models/ai_guidelines.py)
- [向量检索服务](../../backend/app/services/vector_store_service.py)
- [章节服务](../../backend/app/services/chapter_service.py)
