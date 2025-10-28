# AI拆书功能 Day 6 测试与优化方案

> **任务优先级**: P0
> **预计时间**: 6小时
> **创建日期**: 2025-10-27
> **状态**: 待开始

---

## 📋 目录

1. [任务概述](#任务概述)
2. [性能压测方案](#性能压测方案)
3. [错误处理增强方案](#错误处理增强方案)
4. [文档完善方案](#文档完善方案)
5. [实施计划](#实施计划)

---

## 任务概述

### 当前状态

根据测试脚本和实施总结:
- ✅ **基础功能**: 100%完成 (7/7测试通过)
- ✅ **测试覆盖**: 5章测试小说,~2分钟完成
- ⚠️ **性能未知**: 100章长篇网文性能未验证
- ⚠️ **错误处理**: 缺少断点续传、网络恢复机制

### 目标

1. **性能验证**: 确保100章长篇网文能在20分钟内完成分析
2. **稳定性提升**: 添加断点续传、重试机制、超时控制
3. **文档完善**: 提供完整的API文档、用户指南、开发者文档

---

## 性能压测方案

### 测试场景设计

#### 场景1: 中篇小说 (20章, 10万字)
```yaml
测试目标:
  - 章节数: 20章
  - 总字数: 10万字
  - 平均章节长度: 5000字

预期指标:
  - 分析时间: 8-10分钟
  - API调用次数: ~25次 (20章 + 5次增量分析)
  - 预期成本: $0.10-0.15
  - 内存使用: < 500MB
  - 数据库连接: < 10个

验收标准:
  - ✅ 分析成功完成
  - ✅ 提取知识点 ≥ 20个
  - ✅ 生成智能建议 ≥ 5个
  - ✅ 无内存泄漏
  - ✅ 无数据库连接泄漏
```

#### 场景2: 长篇小说 (100章, 50万字)
```yaml
测试目标:
  - 章节数: 100章
  - 总字数: 50万字
  - 平均章节长度: 5000字

预期指标:
  - 分析时间: 15-20分钟
  - API调用次数: ~35次 (智能采样)
  - 预期成本: $0.30-0.50
  - 内存使用: < 1GB
  - 峰值并发: 1个分析任务

验收标准:
  - ✅ 分析成功完成
  - ✅ 提取知识点 ≥ 100个
  - ✅ 生成智能建议 ≥ 15个
  - ✅ 智能采样策略生效 (不是全部章节分析)
  - ✅ 成本控制在预算内
```

#### 场景3: 超长篇小说 (500章, 200万字)
```yaml
测试目标:
  - 章节数: 500章
  - 总字数: 200万字
  - 平均章节长度: 4000字

预期指标:
  - 分析时间: < 30分钟
  - API调用次数: ~50次 (智能采样最大限制)
  - 预期成本: $0.50-0.80
  - 内存使用: < 1.5GB

验收标准:
  - ✅ 分析成功完成
  - ✅ 提取知识点 ≥ 150个
  - ✅ 生成智能建议 ≥ 20个
  - ✅ 智能采样策略生效 (分析章节数 ≤ 150章)
  - ✅ 时间控制在30分钟内
```

#### 场景4: 并发分析测试 (3用户同时上传)
```yaml
测试目标:
  - 并发用户: 3个
  - 每个用户上传: 20章小说
  - 总分析任务: 3个

预期指标:
  - 完成时间: < 15分钟 (而非3×10分钟)
  - 数据库连接池: 不超过20个连接
  - 内存使用: < 2GB

验收标准:
  - ✅ 3个任务全部成功
  - ✅ 无任务互相干扰
  - ✅ 无数据库死锁
  - ✅ 无内存溢出
```

---

### 测试脚本实现

#### 文件结构
```
backend/tests/
├── test_book_analysis_performance.py  # 性能测试主脚本
├── fixtures/
│   ├── generate_medium_novel.py      # 生成20章测试小说
│   ├── generate_long_novel.py        # 生成100章测试小说
│   └── generate_ultra_long_novel.py  # 生成500章测试小说
└── reports/
    └── performance_report_YYYYMMDD.md # 测试报告
```

#### 实现代码框架

**文件**: `backend/tests/test_book_analysis_performance.py`
```python
"""
AI拆书功能性能测试脚本

测试场景:
1. 中篇小说 (20章)
2. 长篇小说 (100章)
3. 超长篇小说 (500章)
4. 并发分析 (3用户)
"""

import asyncio
import time
import psutil
import requests
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class PerformanceTestRunner:
    """性能测试运行器"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1"
        self.token = None
        self.test_results = []

    # TODO: 实现各测试方法

    async def test_medium_novel(self):
        """测试1: 中篇小说 (20章)"""
        pass

    async def test_long_novel(self):
        """测试2: 长篇小说 (100章)"""
        pass

    async def test_ultra_long_novel(self):
        """测试3: 超长篇小说 (500章)"""
        pass

    async def test_concurrent_analysis(self):
        """测试4: 并发分析 (3用户)"""
        pass

    def generate_performance_report(self):
        """生成性能测试报告"""
        pass
```

---

### 监控指标

需要收集的性能指标:

```python
class PerformanceMetrics:
    """性能指标"""

    # 时间指标
    total_time: float           # 总耗时 (秒)
    parsing_time: float         # 解析时间
    analysis_time: float        # 分析时间
    avg_chapter_time: float     # 平均章节分析时间

    # 资源指标
    peak_memory_mb: float       # 峰值内存使用 (MB)
    peak_cpu_percent: float     # 峰值CPU使用率 (%)
    db_connections: int         # 数据库连接数

    # 成本指标
    total_api_calls: int        # 总API调用次数
    total_tokens: int           # 总Token消耗
    total_cost_usd: float       # 总成本 (USD)

    # 质量指标
    extracted_items: int        # 提取知识点数量
    suggestions_count: int      # 智能建议数量
    success_rate: float         # 成功率 (%)
```

---

## 错误处理增强方案

### 问题清单

1. ❌ 网络中断后无法恢复
2. ❌ AI API限流后直接失败
3. ❌ 分析中断后无法断点续传
4. ❌ 超时后无重试机制

---

### 解决方案A: 断点续传机制

#### 问题分析

**现有代码** (`backend/app/services/book_analysis_service.py`):
```python
async def analyze_book(job_id, file_path):
    # 分析所有章节
    for chapter in chapters:
        result = await analyze_chapter(chapter)  # ❌ 失败后重头开始
```

**问题**:
- 分析到第50章时网络中断,重新开始会从第1章再来一次
- 浪费时间和API成本

---

#### 实现方案

##### 步骤1: 数据库表字段扩展

**迁移文件**: `backend/alembic/versions/xxx_add_checkpoint_fields.py`

```python
"""添加断点续传字段

Revision ID: xxx
Revises: yyy
Create Date: 2025-10-27
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    # 添加检查点字段
    op.add_column('book_analysis_jobs',
        sa.Column('last_analyzed_chapter_index', sa.Integer(), default=0)
    )
    op.add_column('book_analysis_jobs',
        sa.Column('failed_chapters', postgresql.JSON(), default=[])
    )
    op.add_column('book_analysis_jobs',
        sa.Column('retry_count', sa.Integer(), default=0)
    )
    op.add_column('book_analysis_jobs',
        sa.Column('max_retries', sa.Integer(), default=3)
    )


def downgrade():
    op.drop_column('book_analysis_jobs', 'last_analyzed_chapter_index')
    op.drop_column('book_analysis_jobs', 'failed_chapters')
    op.drop_column('book_analysis_jobs', 'retry_count')
    op.drop_column('book_analysis_jobs', 'max_retries')
```

**执行迁移**:
```bash
cd backend
alembic upgrade head
```

---

##### 步骤2: 模型类更新

**文件**: `backend/app/models/book_analysis_job.py`

```python
from sqlalchemy import Column, Integer, JSON

class BookAnalysisJob(Base):
    __tablename__ = "book_analysis_jobs"

    # 现有字段...

    # 新增: 断点续传字段
    last_analyzed_chapter_index = Column(Integer, default=0, comment="上次分析到的章节索引")
    failed_chapters = Column(JSON, default=list, comment="失败章节列表 [{index, title, error}]")
    retry_count = Column(Integer, default=0, comment="重试次数")
    max_retries = Column(Integer, default=3, comment="最大重试次数")
```

---

##### 步骤3: Service层实现断点续传

**文件**: `backend/app/services/book_analysis_service.py`

```python
import logging
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class BookAnalysisService:
    """图书分析服务"""

    async def analyze_book_with_checkpoint(
        self,
        job_id: str,
        chapters: List[ChapterData],
        db: AsyncSession
    ):
        """
        带断点续传的图书分析

        功能:
        1. 读取上次分析进度
        2. 从断点位置继续分析
        3. 失败章节记录但不中断
        4. 支持手动重试失败章节
        """

        # 1. 获取任务对象
        job = await db.get(BookAnalysisJob, job_id)
        if not job:
            raise ValueError(f"任务不存在: {job_id}")

        # 2. 读取断点位置
        start_index = job.last_analyzed_chapter_index or 0
        logger.info(f"📍 从断点位置继续: 第{start_index}章")

        # 3. 遍历章节,从断点位置开始
        for i, chapter in enumerate(chapters):
            # 跳过已分析章节
            if i < start_index:
                logger.info(f"⏭️  跳过已分析章节: {chapter.title}")
                continue

            try:
                logger.info(f"📖 正在分析: {chapter.title} ({i+1}/{len(chapters)})")

                # 分析章节
                result = await self.analyze_chapter(chapter, job)

                # 更新进度
                job.last_analyzed_chapter_index = i + 1
                job.progress = int((i + 1) / len(chapters) * 100)
                job.current_step = f"已完成 {i+1}/{len(chapters)} 章"

                await db.commit()

                logger.info(f"✅ 章节分析完成: {chapter.title}")

            except Exception as e:
                # 记录失败但不中断
                logger.error(f"❌ 章节分析失败: {chapter.title}, 错误: {e}")

                # 添加到失败列表
                failed_chapters = job.failed_chapters or []
                failed_chapters.append({
                    "index": i,
                    "title": chapter.title,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })
                job.failed_chapters = failed_chapters

                # 更新检查点 (跳过失败章节)
                job.last_analyzed_chapter_index = i + 1

                await db.commit()

                # 继续下一章节
                continue

        # 4. 检查是否有失败章节需要重试
        if job.failed_chapters and job.retry_count < job.max_retries:
            logger.warning(f"⚠️  有 {len(job.failed_chapters)} 个章节失败,准备重试")
            await self.retry_failed_chapters(job_id, db)

        # 5. 标记任务完成
        job.status = "completed"
        job.completed_at = datetime.utcnow()
        await db.commit()

        logger.info(f"🎉 图书分析完成!")
        logger.info(f"   - 成功: {len(chapters) - len(job.failed_chapters or [])} 章")
        logger.info(f"   - 失败: {len(job.failed_chapters or [])} 章")


    async def retry_failed_chapters(
        self,
        job_id: str,
        db: AsyncSession
    ):
        """重试失败的章节"""

        job = await db.get(BookAnalysisJob, job_id)
        if not job or not job.failed_chapters:
            return

        logger.info(f"🔄 开始重试失败章节: {len(job.failed_chapters)} 个")

        # 增加重试计数
        job.retry_count += 1
        await db.commit()

        # 重新分析失败章节
        retry_success = []
        retry_failed = []

        for failed_info in job.failed_chapters:
            chapter_index = failed_info["index"]
            chapter_title = failed_info["title"]

            try:
                # TODO: 重新读取章节内容并分析
                logger.info(f"🔄 重试: {chapter_title}")

                # 成功后从失败列表移除
                retry_success.append(chapter_index)

            except Exception as e:
                logger.error(f"❌ 重试仍然失败: {chapter_title}, 错误: {e}")
                retry_failed.append(failed_info)

        # 更新失败列表
        job.failed_chapters = retry_failed
        await db.commit()

        logger.info(f"✅ 重试完成: 成功{len(retry_success)}个, 失败{len(retry_failed)}个")
```

---

#### API接口扩展

**新增接口**: `POST /api/v1/books/jobs/{job_id}/retry`

```python
# backend/app/api/v1/book_breakdown.py

@router.post("/jobs/{job_id}/retry")
async def retry_failed_chapters(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    重试失败的章节

    功能:
    - 只重新分析失败的章节
    - 不影响已成功的章节
    - 最多重试3次
    """

    service = BookAnalysisService(db)
    await service.retry_failed_chapters(job_id, db)

    return {"message": "重试任务已启动"}
```

---

### 解决方案B: AI API重试机制

#### 问题分析

**现有代码** (`backend/app/services/ai/http_ai_service.py`):
```python
async def call_ai(self, system_prompt, user_prompt):
    response = await openai_client.chat.completions.create(...)  # ❌ 失败直接抛异常
    return response
```

**问题**:
- AI API偶尔会超时或限流
- 一次失败就导致整个章节分析失败
- 没有重试机制

---

#### 实现方案

##### 步骤1: 安装依赖

```bash
cd backend
pip install tenacity
```

**requirements.txt**:
```txt
tenacity>=8.2.0  # 重试库
```

---

##### 步骤2: Service层添加重试装饰器

**文件**: `backend/app/services/ai/http_ai_service.py`

```python
import asyncio
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
from openai import RateLimitError, APIConnectionError, APITimeoutError

logger = logging.getLogger(__name__)


class HTTPAIService:
    """HTTP AI服务"""

    @retry(
        # 重试条件: 只重试特定异常
        retry=retry_if_exception_type((
            RateLimitError,       # API限流
            APIConnectionError,   # 网络连接失败
            APITimeoutError,      # 超时
        )),
        # 最多重试3次
        stop=stop_after_attempt(3),
        # 指数退避: 2秒 -> 4秒 -> 8秒
        wait=wait_exponential(multiplier=1, min=2, max=10),
        # 重试前记录日志
        before_sleep=before_sleep_log(logger, logging.WARNING),
        # 最终还是失败则抛出异常
        reraise=True
    )
    async def call_ai_with_retry(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3
    ) -> str:
        """
        AI调用(带重试)

        重试策略:
        - RateLimitError: 等待 retry_after 秒后重试
        - APIConnectionError: 指数退避重试
        - APITimeoutError: 指数退避重试
        - 其他异常: 不重试,直接抛出
        """

        try:
            return await self.call_ai(system_prompt, user_prompt, temperature)

        except RateLimitError as e:
            # 特殊处理: API限流
            retry_after = getattr(e, 'retry_after', 5)
            logger.warning(f"⚠️  API限流,将在 {retry_after}秒 后重试")
            await asyncio.sleep(retry_after)
            raise  # 继续抛出,触发retry装饰器

        except APIConnectionError as e:
            logger.warning(f"⚠️  网络连接失败,将重试: {e}")
            raise

        except APITimeoutError as e:
            logger.warning(f"⚠️  API超时,将重试: {e}")
            raise
```

---

##### 步骤3: 使用重试版本的AI调用

**文件**: `backend/app/services/book_analysis/web_novel_strategy.py`

```python
class WebNovelStrategy:
    """网文11维度分析策略"""

    async def analyze(self, chapter: ChapterData, context: Dict) -> Dict:
        """分析章节"""

        # 使用带重试的AI调用
        response = await self.ai_service.call_ai_with_retry(  # ✅ 改用重试版本
            system_prompt=self.build_system_prompt(),
            user_prompt=self.build_user_prompt(chapter),
            temperature=0.3
        )

        return self.parse_response(response)
```

---

### 解决方案C: 超时控制

#### 问题分析

**现有代码**:
```python
result = await analyze_chapter(chapter)  # ❌ 可能无限等待
```

**问题**:
- 某些章节可能因为内容特殊导致AI响应很慢
- 没有超时机制,可能无限等待

---

#### 实现方案

**文件**: `backend/app/services/book_analysis_service.py`

```python
import asyncio

async def analyze_chapter_with_timeout(
    self,
    chapter: ChapterData,
    timeout: int = 120  # 默认120秒超时
) -> Optional[Dict]:
    """
    分析章节(带超时控制)

    Args:
        chapter: 章节数据
        timeout: 超时时间(秒)

    Returns:
        分析结果,超时则返回None
    """

    try:
        # 使用asyncio.wait_for添加超时
        result = await asyncio.wait_for(
            self.analyze_chapter(chapter),
            timeout=timeout
        )
        return result

    except asyncio.TimeoutError:
        logger.error(
            f"❌ 章节分析超时({timeout}秒): {chapter.title}\n"
            f"   建议: 检查章节内容是否过长或格式异常"
        )
        # 返回None,但不中断整体流程
        return None
```

---

### 配置管理

将超时、重试等配置项集中管理:

**文件**: `backend/app/core/config.py`

```python
class Settings(BaseSettings):
    """应用配置"""

    # AI拆书功能配置
    BOOK_ANALYSIS_TIMEOUT: int = 120  # 单章超时时间(秒)
    BOOK_ANALYSIS_MAX_RETRIES: int = 3  # 最大重试次数
    BOOK_ANALYSIS_RETRY_DELAY: int = 2  # 重试延迟(秒)

    # AI API配置
    AI_REQUEST_TIMEOUT: int = 60  # AI请求超时(秒)
    AI_MAX_RETRIES: int = 3  # AI请求最大重试次数

    class Config:
        env_file = ".env"


settings = Settings()
```

---

## 文档完善方案

### 文档清单

#### 1. API接口文档

**文件**: `backend/docs/BOOK_ANALYSIS_API.md`

**内容大纲**:
```markdown
# AI拆书功能 API文档

## 接口列表

### 1. 上传图书
POST /api/v1/books/upload

### 2. 查询任务状态
GET /api/v1/books/jobs/{job_id}/status

### 3. 获取任务详情
GET /api/v1/books/jobs/{job_id}

### 4. 获取分析结果
GET /api/v1/books/jobs/{job_id}/result

### 5. 获取智能建议
GET /api/v1/books/jobs/{job_id}/suggestions

### 6. 采纳单个建议
POST /api/v1/books/suggestions/accept

### 7. 批量采纳建议
POST /api/v1/books/suggestions/batch-accept

### 8. 重试失败章节 (新增)
POST /api/v1/books/jobs/{job_id}/retry

### 9. 删除任务
DELETE /api/v1/books/jobs/{job_id}

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 400 | 文件格式不支持 | 请上传.txt/.epub/.pdf格式文件 |
| 413 | 文件过大 | 文件大小不能超过50MB |
| 429 | 请求过于频繁 | 请稍后重试 |
| 500 | 分析失败 | 请联系技术支持 |

## 重试机制说明

- 自动重试: 网络错误、API限流自动重试3次
- 手动重试: 调用 /retry 接口重新分析失败章节
- 断点续传: 中断后重新启动会从上次位置继续

## 性能指标参考

| 场景 | 章节数 | 预期时间 | 预期成本 |
|------|--------|---------|---------|
| 短篇 | 5-10章 | 2-3分钟 | $0.05 |
| 中篇 | 20-50章 | 8-15分钟 | $0.15 |
| 长篇 | 100-200章 | 15-25分钟 | $0.40 |
| 超长篇 | 500章+ | < 30分钟 | $0.60 |
```

---

#### 2. 用户使用指南

**文件**: `docs/AI拆书功能用户指南.md`

**内容大纲**:
```markdown
# AI拆书功能用户指南

## 快速开始

### 1. 准备图书文件

支持格式:
- .txt (纯文本)
- .epub (电子书)
- .pdf (仅支持文字版)

文件要求:
- 大小: ≤ 50MB
- 章节: 建议有明确的章节标题
- 编码: UTF-8

### 2. 上传与分析

步骤:
1. 点击"AI拆书分析"按钮
2. 选择图书文件
3. 填写图书信息
4. 选择分析策略 (网文11维度 / 通用分析)
5. 点击"开始分析"

### 3. 查看分析结果

分析完成后,可以:
- 查看提取的知识点
- 浏览智能建议
- 批量采纳建议到世界观

## 常见问题FAQ

### Q1: 分析需要多长时间?
- 短篇 (5-10章): 2-3分钟
- 中篇 (20-50章): 8-15分钟
- 长篇 (100+章): 15-30分钟

### Q2: 分析中断了怎么办?
系统支持断点续传,重新开始会从上次位置继续。

### Q3: 为什么有些章节分析失败?
可能原因:
- 章节内容过长
- 网络不稳定
- AI API限流

解决方案:
- 点击"重试失败章节"按钮
- 检查网络连接
- 联系技术支持

### Q4: 支持哪些图书类型?
- ✅ 网络小说 (玄幻/都市/科幻)
- ✅ 非虚构图书 (工具书/教程)
- ❌ 诗歌、散文 (格式不适合)

### Q5: 智能建议的置信度是什么意思?
置信度表示AI对该建议的把握程度:
- 0.8-1.0: 非常推荐
- 0.6-0.8: 推荐
- 0.4-0.6: 可选
- < 0.4: 不推荐

## 最佳实践

1. **章节标题规范**: 使用"第X章"格式
2. **内容长度**: 单章建议500-8000字
3. **文件编码**: 使用UTF-8编码
4. **格式选择**: 优先使用.txt格式 (解析最快)
```

---

#### 3. 开发者文档

**文件**: `backend/docs/BOOK_ANALYSIS_DEV_GUIDE.md`

**内容大纲**:
```markdown
# AI拆书功能开发者文档

## 架构设计

### 核心模块

1. **解析器 (Parsers)**
   - TXTParser: TXT文件解析
   - EPUBParser: EPUB文件解析
   - PDFParser: PDF文件解析

2. **分析策略 (Strategies)**
   - WebNovelStrategy: 网文11维度分析
   - GeneralBookStrategy: 通用图书分析

3. **智能采样 (SmartSampling)**
   - 前30章深度分析
   - 关键章节识别
   - 成本控制

4. **建议生成器 (SuggestionGenerator)**
   - 维度映射
   - 置信度评估
   - 智能建议生成

## 扩展指南

### 如何添加新的分析策略?

步骤:
1. 创建策略类继承 `BookAnalysisStrategy`
2. 实现 `analyze()` 方法
3. 注册到 `StrategyRegistry`

示例:
```python
class CustomStrategy(BookAnalysisStrategy):
    """自定义分析策略"""

    @property
    def strategy_id(self) -> str:
        return "custom_strategy"

    @property
    def dimensions(self) -> List[AnalysisDimension]:
        return [
            # 定义维度...
        ]

    async def analyze(self, chapter: ChapterData) -> Dict:
        # 实现分析逻辑...
        pass

# 注册策略
StrategyRegistry.register(CustomStrategy())
```

### 如何添加新的文件格式?

步骤:
1. 创建解析器类继承 `BaseParser`
2. 实现 `parse()` 方法
3. 注册到 `ParserFactory`

示例:
```python
class CustomParser(BaseParser):
    """自定义格式解析器"""

    def parse(self, file_path: str) -> List[ChapterData]:
        # 实现解析逻辑...
        pass

# 注册解析器
ParserFactory.register('.custom', CustomParser)
```

## 调试技巧

### 1. 查看AI原始响应

AI响应会保存到 `backend/debug_ai_responses/` 目录:
```
ch1_第一章标题.txt
ch2_第二章标题.txt
...
```

### 2. 开启详细日志

```python
# backend/app/main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,  # 改为DEBUG级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 3. 使用断点调试

```python
# 在代码中添加断点
import pdb; pdb.set_trace()

# 或使用ipdb (更友好)
import ipdb; ipdb.set_trace()
```

## 性能优化建议

1. **并行分析**: 使用 `asyncio.gather()` 并行分析多个章节
2. **缓存机制**: 使用Redis缓存分析结果
3. **批量写入**: 使用批量插入减少数据库IO
4. **连接池**: 配置合理的数据库连接池大小

## 测试指南

### 单元测试

```bash
cd backend
pytest tests/test_book_analysis.py -v
```

### 集成测试

```bash
python tests/test_book_analysis_auto.py
```

### 性能测试

```bash
python tests/test_book_analysis_performance.py
```
```

---

## 实施计划

### Day 6.1: 性能压测 (2小时)

**任务清单**:
- [ ] 创建测试脚本 `test_book_analysis_performance.py`
- [ ] 生成测试数据 (20章/100章/500章)
- [ ] 执行场景1: 中篇小说测试
- [ ] 执行场景2: 长篇小说测试
- [ ] 执行场景3: 超长篇小说测试
- [ ] 执行场景4: 并发分析测试
- [ ] 生成性能测试报告

**验收标准**:
- ✅ 所有测试场景通过
- ✅ 性能指标在预期范围内
- ✅ 发现并记录性能瓶颈

---

### Day 6.2: 错误处理增强 (3小时)

**任务清单**:
- [ ] 数据库迁移: 添加断点续传字段
- [ ] 实现断点续传逻辑
- [ ] 实现AI API重试机制
- [ ] 实现超时控制
- [ ] 实现重试失败章节接口
- [ ] 单元测试: 测试错误处理
- [ ] 集成测试: 模拟网络中断场景

**验收标准**:
- ✅ 断点续传功能正常
- ✅ 网络中断后能自动恢复
- ✅ API限流后能自动重试
- ✅ 超时后不阻塞其他章节

---

### Day 6.3: 文档完善 (1小时)

**任务清单**:
- [ ] 编写API接口文档 `BOOK_ANALYSIS_API.md`
- [ ] 编写用户使用指南 `AI拆书功能用户指南.md`
- [ ] 编写开发者文档 `BOOK_ANALYSIS_DEV_GUIDE.md`
- [ ] 更新主文档索引 `DOCS_INDEX.md`

**验收标准**:
- ✅ 3份文档完整编写
- ✅ 代码示例可运行
- ✅ FAQ覆盖常见问题

---

## 验收标准总结

### 性能指标
- ✅ 20章: 8-10分钟
- ✅ 100章: 15-20分钟
- ✅ 500章: < 30分钟
- ✅ 并发3用户: 无冲突

### 稳定性指标
- ✅ 断点续传功能正常
- ✅ 网络中断后能恢复
- ✅ API限流后能重试
- ✅ 超时后不阻塞

### 文档完整性
- ✅ API文档完整
- ✅ 用户指南清晰
- ✅ 开发者文档详细

---

**创建时间**: 2025-10-27
**最后更新**: 2025-10-27
**维护者**: NovelAIde 开发团队
