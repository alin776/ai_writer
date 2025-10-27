# AI拆书功能格式扩展方案 (EPUB & PDF)

> **任务优先级**: P1
> **预计时间**: 7小时
> **创建日期**: 2025-10-27
> **状态**: 待开始

---

## 📋 目录

1. [任务概述](#任务概述)
2. [EPUB格式支持](#epub格式支持)
3. [PDF格式支持](#pdf格式支持)
4. [统一解析器接口](#统一解析器接口)
5. [实施计划](#实施计划)

---

## 任务概述

### 当前状态

- ✅ **TXT格式**: 100%支持,正则匹配章节标题
- ❌ **EPUB格式**: 未实现
- ❌ **PDF格式**: 未实现

### 目标

1. **EPUB支持**: 解析HTML结构,提取章节内容
2. **PDF支持**: 提取文字内容,识别章节标题
3. **统一接口**: 抽象解析器基类,工厂模式管理

### 技术难点

| 格式 | 难点 | 解决方案 |
|------|------|---------|
| EPUB | HTML标签清理 | BeautifulSoup |
| EPUB | 章节顺序混乱 | 使用spine顺序 |
| PDF | 扫描版无法识别 | 提示用户使用OCR |
| PDF | 双栏排版 | 使用pdfplumber布局检测 |
| PDF | 性能问题 | 添加超时保护 |

---

## EPUB格式支持

### EPUB文件结构

EPUB是一种基于HTML的电子书格式:
```
book.epub (ZIP压缩包)
├── META-INF/
│   └── container.xml      # 指向内容文档
├── OEBPS/
│   ├── content.opf        # 元数据和目录
│   ├── toc.ncx            # 目录导航
│   ├── chapter1.xhtml     # 章节内容
│   ├── chapter2.xhtml
│   └── ...
└── mimetype
```

### 技术方案

#### 依赖安装

```bash
cd backend
pip install ebooklib beautifulsoup4 lxml
```

**requirements.txt**:
```txt
ebooklib>=0.18
beautifulsoup4>=4.12.0
lxml>=5.0.0  # 更快的HTML解析器
```

---

### 实现代码

#### 步骤1: 创建解析器基类

**文件**: `backend/app/services/book_analysis/parsers/base_parser.py`

```python
"""
解析器基类

所有格式解析器的抽象基类
"""

from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass


@dataclass
class ChapterData:
    """章节数据结构"""
    index: int           # 章节序号 (从1开始)
    title: str           # 章节标题
    content: str         # 章节内容
    word_count: int      # 字数

    @classmethod
    def from_text(cls, index: int, title: str, content: str):
        """从文本创建章节数据"""
        return cls(
            index=index,
            title=title,
            content=content,
            word_count=len(content)
        )


class BaseParser(ABC):
    """解析器基类"""

    def __init__(self, min_chapter_length: int = 100):
        """
        Args:
            min_chapter_length: 最小章节长度 (字符数)
        """
        self.min_chapter_length = min_chapter_length

    @abstractmethod
    def parse(self, file_path: str) -> List[ChapterData]:
        """
        解析文件为章节列表

        Args:
            file_path: 文件路径

        Returns:
            章节数据列表
        """
        pass

    def validate_chapters(self, chapters: List[ChapterData]) -> List[ChapterData]:
        """
        验证章节列表

        过滤掉过短的章节
        """
        return [
            ch for ch in chapters
            if ch.word_count >= self.min_chapter_length
        ]
```

---

#### 步骤2: 实现EPUB解析器

**文件**: `backend/app/services/book_analysis/parsers/epub_parser.py`

```python
"""
EPUB格式解析器

功能:
- 解析EPUB文件结构
- 提取HTML章节内容
- 清理HTML标签
- 识别章节标题
"""

import logging
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from typing import List, Optional

from .base_parser import BaseParser, ChapterData

logger = logging.getLogger(__name__)


class EPUBParser(BaseParser):
    """EPUB格式解析器"""

    def parse(self, file_path: str) -> List[ChapterData]:
        """
        解析EPUB文件

        Args:
            file_path: EPUB文件路径

        Returns:
            章节数据列表
        """
        logger.info(f"📚 开始解析EPUB文件: {file_path}")

        try:
            # 1. 读取EPUB文件
            book = epub.read_epub(file_path)
            logger.info(f"✅ EPUB文件读取成功")

            # 2. 提取章节
            chapters = self._extract_chapters(book)

            # 3. 验证章节
            valid_chapters = self.validate_chapters(chapters)

            logger.info(f"✅ EPUB解析完成: {len(valid_chapters)} 个有效章节")
            return valid_chapters

        except Exception as e:
            logger.error(f"❌ EPUB解析失败: {e}")
            raise

    def _extract_chapters(self, book: epub.EpubBook) -> List[ChapterData]:
        """
        从EPUB提取章节

        按照spine顺序提取 (spine定义了章节阅读顺序)
        """
        chapters = []

        # 获取spine (章节阅读顺序)
        spine = book.spine
        logger.info(f"📖 EPUB spine包含 {len(spine)} 个条目")

        for i, (item_id, linear) in enumerate(spine):
            # 获取章节内容
            item = book.get_item_with_id(item_id)

            if item is None:
                logger.warning(f"⚠️  找不到章节: {item_id}")
                continue

            # 只处理文档类型 (XHTML/HTML)
            if item.get_type() != ebooklib.ITEM_DOCUMENT:
                logger.debug(f"⏭️  跳过非文档类型: {item.get_name()}")
                continue

            # 解析HTML内容
            chapter_data = self._parse_html_item(item, i + 1)

            if chapter_data:
                chapters.append(chapter_data)

        return chapters

    def _parse_html_item(
        self,
        item: epub.EpubItem,
        index: int
    ) -> Optional[ChapterData]:
        """
        解析HTML章节

        Args:
            item: EPUB章节项
            index: 章节序号

        Returns:
            章节数据,如果内容过短则返回None
        """
        try:
            # 1. 获取HTML内容
            html_content = item.get_content().decode('utf-8', errors='ignore')

            # 2. 使用BeautifulSoup解析
            soup = BeautifulSoup(html_content, 'lxml')

            # 3. 提取标题
            title = self._extract_title(soup, item.get_name())

            # 4. 清理HTML标签,提取纯文本
            text_content = self._clean_html(soup)

            # 5. 检查内容长度
            if len(text_content) < self.min_chapter_length:
                logger.debug(f"⏭️  章节过短,跳过: {title} ({len(text_content)}字符)")
                return None

            logger.info(f"✅ 提取章节: {title} ({len(text_content)}字符)")

            return ChapterData(
                index=index,
                title=title,
                content=text_content,
                word_count=len(text_content)
            )

        except Exception as e:
            logger.error(f"❌ 解析HTML章节失败: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup, default: str) -> str:
        """
        从HTML提取标题

        优先级:
        1. <h1> 标签
        2. <h2> 标签
        3. <h3> 标签
        4. <title> 标签
        5. 文件名
        """
        # 尝试标题标签
        for tag in ['h1', 'h2', 'h3']:
            title_tag = soup.find(tag)
            if title_tag:
                title = title_tag.get_text(strip=True)
                if title:
                    return title

        # 尝试<title>标签
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            if title:
                return title

        # 使用文件名
        return default

    def _clean_html(self, soup: BeautifulSoup) -> str:
        """
        清理HTML标签,提取纯文本

        处理:
        - 移除<script>和<style>标签
        - 保留换行结构
        - 清理多余空白
        """
        # 移除script和style标签
        for tag in soup(['script', 'style', 'meta', 'link']):
            tag.decompose()

        # 提取纯文本
        text = soup.get_text(separator='\n', strip=True)

        # 清理多余空行 (连续空行合并为一个)
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]  # 移除空行

        return '\n\n'.join(lines)


# 测试代码
if __name__ == "__main__":
    parser = EPUBParser()
    chapters = parser.parse("test.epub")
    print(f"提取章节数: {len(chapters)}")
    for ch in chapters[:3]:
        print(f"- {ch.title}: {ch.word_count}字")
```

---

### EPUB解析的特殊处理

#### 处理1: 章节顺序问题

有些EPUB文件的`spine`顺序不正确,需要备用方案:

```python
def _extract_chapters_fallback(self, book: epub.EpubBook) -> List[ChapterData]:
    """
    备用方案: 使用TOC (目录) 提取章节

    适用于spine顺序混乱的情况
    """
    chapters = []

    # 获取TOC (Table of Contents)
    toc = book.toc

    for i, toc_item in enumerate(toc):
        # TOC可能是嵌套结构,递归处理
        if isinstance(toc_item, tuple):
            # 处理章节组
            self._process_toc_section(toc_item, chapters, i)
        else:
            # 处理单个章节
            chapter_data = self._process_toc_item(toc_item, i + 1)
            if chapter_data:
                chapters.append(chapter_data)

    return chapters
```

#### 处理2: 图片和多媒体

EPUB可能包含图片,当前版本忽略:

```python
# 在_clean_html中添加
for tag in soup(['img', 'svg', 'video', 'audio']):
    # 可以选择保留图片链接或完全移除
    tag.decompose()
```

---

### 单元测试

**文件**: `backend/tests/test_epub_parser.py`

```python
"""
EPUB解析器单元测试
"""

import pytest
from pathlib import Path
from app.services.book_analysis.parsers.epub_parser import EPUBParser


@pytest.fixture
def epub_parser():
    """创建EPUB解析器"""
    return EPUBParser(min_chapter_length=100)


def test_parse_valid_epub(epub_parser):
    """测试解析有效的EPUB文件"""
    test_file = "tests/fixtures/test_book.epub"

    if not Path(test_file).exists():
        pytest.skip("测试文件不存在")

    chapters = epub_parser.parse(test_file)

    assert len(chapters) > 0
    assert all(ch.word_count > 0 for ch in chapters)
    assert all(ch.title for ch in chapters)


def test_invalid_epub(epub_parser):
    """测试解析无效的EPUB文件"""
    with pytest.raises(Exception):
        epub_parser.parse("invalid.epub")


def test_chapter_filtering(epub_parser):
    """测试章节过滤 (过短的章节应被移除)"""
    # 这个测试需要构造特殊的EPUB文件
    pass
```

---

## PDF格式支持

### PDF解析的挑战

PDF格式比EPUB复杂得多:

| 挑战 | 说明 | 解决方案 |
|------|------|---------|
| **扫描版PDF** | 图片无法识别文字 | 提示用户使用OCR工具 |
| **双栏排版** | 文字顺序混乱 | 使用pdfplumber布局检测 |
| **表格和图片** | 干扰文字提取 | 过滤非文本区域 |
| **性能问题** | 大文件解析慢 | 添加超时保护,分页处理 |
| **格式多样** | 无统一标准 | 尽力而为,提供手动调整选项 |

---

### 技术方案

#### 依赖安装

```bash
cd backend
pip install pdfplumber
```

**requirements.txt**:
```txt
pdfplumber>=0.10.0
```

**说明**: 为什么选择`pdfplumber`而不是`PyPDF2`?
- ✅ pdfplumber: 更好的布局检测,支持表格提取
- ❌ PyPDF2: 简单文字提取,布局混乱

---

### 实现代码

#### 步骤1: 实现PDF解析器

**文件**: `backend/app/services/book_analysis/parsers/pdf_parser.py`

```python
"""
PDF格式解析器

功能:
- 提取PDF文字内容
- 识别章节标题
- 处理双栏排版
- 超时保护

限制:
- 仅支持文字版PDF (扫描版需OCR预处理)
- 复杂排版可能识别不准确
"""

import re
import logging
import pdfplumber
from typing import List, Optional
from pathlib import Path

from .base_parser import BaseParser, ChapterData
from ..smart_sampling import SmartSamplingAnalyzer

logger = logging.getLogger(__name__)


class PDFParser(BaseParser):
    """PDF格式解析器"""

    # 章节标题正则 (复用TXT解析器的正则)
    CHAPTER_PATTERN = SmartSamplingAnalyzer.CHAPTER_TITLE_PATTERN

    def __init__(
        self,
        min_chapter_length: int = 100,
        page_timeout: int = 5  # 单页提取超时(秒)
    ):
        super().__init__(min_chapter_length)
        self.page_timeout = page_timeout

    def parse(self, file_path: str) -> List[ChapterData]:
        """
        解析PDF文件

        Args:
            file_path: PDF文件路径

        Returns:
            章节数据列表
        """
        logger.info(f"📄 开始解析PDF文件: {file_path}")

        # 检查文件大小
        file_size = Path(file_path).stat().st_size / 1024 / 1024  # MB
        logger.info(f"📏 文件大小: {file_size:.2f} MB")

        if file_size > 50:
            logger.warning(f"⚠️  文件较大,解析可能较慢")

        try:
            # 1. 打开PDF文件
            with pdfplumber.open(file_path) as pdf:
                logger.info(f"📖 PDF总页数: {len(pdf.pages)}")

                # 2. 逐页提取文字
                full_text = self._extract_text_from_pdf(pdf)

                # 3. 识别章节
                chapters = self._split_into_chapters(full_text)

                # 4. 验证章节
                valid_chapters = self.validate_chapters(chapters)

                logger.info(f"✅ PDF解析完成: {len(valid_chapters)} 个有效章节")
                return valid_chapters

        except Exception as e:
            logger.error(f"❌ PDF解析失败: {e}")
            raise

    def _extract_text_from_pdf(self, pdf: pdfplumber.PDF) -> str:
        """
        从PDF提取全文

        逐页提取,添加超时保护
        """
        text_parts = []

        for i, page in enumerate(pdf.pages):
            try:
                logger.debug(f"📄 提取第 {i+1}/{len(pdf.pages)} 页")

                # 提取页面文字 (TODO: 添加超时保护)
                text = page.extract_text()

                if text:
                    text_parts.append(text)
                else:
                    logger.warning(f"⚠️  第{i+1}页无文字内容 (可能是扫描版)")

            except Exception as e:
                logger.error(f"❌ 第{i+1}页提取失败: {e}")
                continue

        full_text = '\n\n'.join(text_parts)
        logger.info(f"✅ 提取完成: {len(full_text)} 字符")

        return full_text

    def _split_into_chapters(self, full_text: str) -> List[ChapterData]:
        """
        将全文分割为章节

        策略:
        1. 使用正则匹配章节标题
        2. 如果找不到章节,使用备用策略
        """
        chapters = []

        # 1. 尝试正则匹配
        matches = list(self.CHAPTER_PATTERN.finditer(full_text))

        if matches:
            logger.info(f"✅ 正则匹配到 {len(matches)} 个章节标题")
            chapters = self._extract_chapters_by_regex(full_text, matches)
        else:
            logger.warning(f"⚠️  正则未匹配到章节,使用备用策略")
            chapters = self._extract_chapters_fallback(full_text)

        return chapters

    def _extract_chapters_by_regex(
        self,
        full_text: str,
        matches: List[re.Match]
    ) -> List[ChapterData]:
        """
        使用正则匹配结果提取章节
        """
        chapters = []

        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)

            # 提取章节标题和内容
            title = match.group(0).strip()
            content = full_text[start:end].strip()

            # 移除标题行
            content = content[len(title):].strip()

            if len(content) < self.min_chapter_length:
                logger.debug(f"⏭️  章节过短,跳过: {title}")
                continue

            chapters.append(ChapterData(
                index=len(chapters) + 1,
                title=title,
                content=content,
                word_count=len(content)
            ))

        return chapters

    def _extract_chapters_fallback(self, full_text: str) -> List[ChapterData]:
        """
        备用策略: 按固定长度分割

        适用于无法识别章节标题的情况
        """
        logger.info("📝 使用备用策略: 按固定长度分割")

        # 每10000字符一个章节
        chunk_size = 10000
        chunks = [
            full_text[i:i+chunk_size]
            for i in range(0, len(full_text), chunk_size)
        ]

        chapters = []
        for i, chunk in enumerate(chunks):
            if len(chunk) < self.min_chapter_length:
                continue

            chapters.append(ChapterData(
                index=i + 1,
                title=f"第{i+1}部分",
                content=chunk,
                word_count=len(chunk)
            ))

        return chapters


# 测试代码
if __name__ == "__main__":
    parser = PDFParser()
    chapters = parser.parse("test.pdf")
    print(f"提取章节数: {len(chapters)}")
    for ch in chapters[:3]:
        print(f"- {ch.title}: {ch.word_count}字")
```

---

### PDF解析的特殊处理

#### 处理1: 检测扫描版PDF

```python
def is_scanned_pdf(self, pdf: pdfplumber.PDF) -> bool:
    """
    检测是否为扫描版PDF

    策略: 检查前3页是否包含文字
    """
    text_count = 0

    for page in pdf.pages[:3]:
        text = page.extract_text()
        if text and len(text.strip()) > 100:
            text_count += 1

    # 如果3页都没有文字,判定为扫描版
    if text_count == 0:
        return True

    return False


# 在parse()方法开头添加检测
if self.is_scanned_pdf(pdf):
    raise ValueError(
        "检测到扫描版PDF,无法直接提取文字。\n"
        "请使用OCR工具 (如Adobe Acrobat/ABBYY) 转换为文字版后重试。"
    )
```

#### 处理2: 双栏排版处理

```python
def _extract_text_with_layout(self, page) -> str:
    """
    考虑布局的文字提取

    使用pdfplumber的layout参数
    """
    # 提取带布局信息的文字
    words = page.extract_words(
        x_tolerance=3,
        y_tolerance=3,
        keep_blank_chars=False
    )

    # 按Y坐标 (top) 分组,再按X坐标 (x0) 排序
    # 这样可以处理双栏排版
    lines = {}
    for word in words:
        y = round(word['top'])
        if y not in lines:
            lines[y] = []
        lines[y].append(word)

    # 按Y坐标排序 (从上到下)
    sorted_lines = sorted(lines.items())

    # 每行按X坐标排序 (从左到右)
    text_lines = []
    for y, words in sorted_lines:
        sorted_words = sorted(words, key=lambda w: w['x0'])
        line_text = ' '.join(w['text'] for w in sorted_words)
        text_lines.append(line_text)

    return '\n'.join(text_lines)
```

---

### 单元测试

**文件**: `backend/tests/test_pdf_parser.py`

```python
"""
PDF解析器单元测试
"""

import pytest
from pathlib import Path
from app.services.book_analysis.parsers.pdf_parser import PDFParser


@pytest.fixture
def pdf_parser():
    """创建PDF解析器"""
    return PDFParser(min_chapter_length=100)


def test_parse_valid_pdf(pdf_parser):
    """测试解析有效的PDF文件"""
    test_file = "tests/fixtures/test_book.pdf"

    if not Path(test_file).exists():
        pytest.skip("测试文件不存在")

    chapters = pdf_parser.parse(test_file)

    assert len(chapters) > 0
    assert all(ch.word_count > 0 for ch in chapters)


def test_scanned_pdf_detection(pdf_parser):
    """测试扫描版PDF检测"""
    # 需要准备扫描版PDF测试文件
    pass


def test_invalid_pdf(pdf_parser):
    """测试解析无效的PDF文件"""
    with pytest.raises(Exception):
        pdf_parser.parse("invalid.pdf")
```

---

## 统一解析器接口

### 解析器工厂模式

**文件**: `backend/app/services/book_analysis/parsers/__init__.py`

```python
"""
解析器工厂

根据文件扩展名自动选择解析器
"""

from typing import Dict, Type
from .base_parser import BaseParser
from .txt_parser import TXTParser
from .epub_parser import EPUBParser
from .pdf_parser import PDFParser


class ParserFactory:
    """解析器工厂"""

    # 解析器注册表
    _PARSERS: Dict[str, Type[BaseParser]] = {
        '.txt': TXTParser,
        '.epub': EPUBParser,
        '.pdf': PDFParser,
    }

    @classmethod
    def get_parser(cls, file_extension: str) -> BaseParser:
        """
        根据文件扩展名获取解析器

        Args:
            file_extension: 文件扩展名 (如 '.txt', '.epub', '.pdf')

        Returns:
            解析器实例

        Raises:
            ValueError: 不支持的文件格式
        """
        file_extension = file_extension.lower()

        parser_class = cls._PARSERS.get(file_extension)
        if not parser_class:
            supported = ', '.join(cls._PARSERS.keys())
            raise ValueError(
                f"不支持的文件格式: {file_extension}\n"
                f"支持的格式: {supported}"
            )

        return parser_class()

    @classmethod
    def register_parser(cls, extension: str, parser_class: Type[BaseParser]):
        """
        注册自定义解析器

        Args:
            extension: 文件扩展名
            parser_class: 解析器类
        """
        cls._PARSERS[extension.lower()] = parser_class

    @classmethod
    def supported_formats(cls) -> list:
        """获取支持的格式列表"""
        return list(cls._PARSERS.keys())


# 使用示例
if __name__ == "__main__":
    # 自动选择解析器
    parser = ParserFactory.get_parser('.epub')
    chapters = parser.parse('book.epub')

    # 注册自定义解析器
    # ParserFactory.register_parser('.docx', DOCXParser)
```

---

### TXT解析器重构

将现有的TXT解析逻辑迁移到新的解析器架构:

**文件**: `backend/app/services/book_analysis/parsers/txt_parser.py`

```python
"""
TXT格式解析器

复用SmartSamplingAnalyzer的解析逻辑
"""

import logging
from typing import List

from .base_parser import BaseParser, ChapterData
from ..smart_sampling import SmartSamplingAnalyzer

logger = logging.getLogger(__name__)


class TXTParser(BaseParser):
    """TXT格式解析器"""

    def parse(self, file_path: str) -> List[ChapterData]:
        """
        解析TXT文件

        复用SmartSamplingAnalyzer的逻辑
        """
        logger.info(f"📝 开始解析TXT文件: {file_path}")

        # 使用SmartSamplingAnalyzer解析
        analyzer = SmartSamplingAnalyzer(
            min_chapter_length=self.min_chapter_length
        )

        chapters = analyzer.parse_txt_file(file_path)

        logger.info(f"✅ TXT解析完成: {len(chapters)} 个章节")
        return chapters
```

---

### API接口适配

**文件**: `backend/app/api/v1/book_breakdown.py`

```python
from app.services.book_analysis.parsers import ParserFactory


@router.post("/upload")
async def upload_book(
    file: UploadFile = File(...),
    book_title: Optional[str] = None,
    strategy_id: str = "web_novel_11d",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    上传图书并启动分析

    支持格式: .txt, .epub, .pdf
    """

    # 1. 验证文件格式
    file_ext = os.path.splitext(file.filename)[1].lower()

    try:
        # 检查格式是否支持
        ParserFactory.get_parser(file_ext)
    except ValueError as e:
        raise HTTPException(400, str(e))

    # 2. 保存文件
    upload_dir = Path("uploads/books")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / f"{uuid4()}{file_ext}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 3. 创建分析任务
    job = BookAnalysisJob(
        user_id=current_user.id,
        book_title=book_title or file.filename,
        original_filename=file.filename,
        file_format=file_ext[1:],  # 去掉点号
        file_path=str(file_path),
        strategy_id=strategy_id,
        status="pending"
    )

    db.add(job)
    await db.commit()
    await db.refresh(job)

    # 4. 启动后台分析任务
    # ... (保持原有逻辑)

    return {
        "id": str(job.id),
        "message": f"上传成功,开始分析 ({file_ext} 格式)"
    }
```

---

## 实施计划

### Phase 1: EPUB解析器实现 (2小时)

**任务清单**:
- [ ] 创建解析器基类 `base_parser.py`
- [ ] 实现EPUB解析器 `epub_parser.py`
- [ ] 编写单元测试 `test_epub_parser.py`
- [ ] 测试真实EPUB文件

**验收标准**:
- ✅ 能正确提取章节标题
- ✅ 能清理HTML标签
- ✅ 章节顺序正确
- ✅ 单元测试通过

---

### Phase 2: PDF解析器实现 (3小时)

**任务清单**:
- [ ] 实现PDF解析器 `pdf_parser.py`
- [ ] 实现扫描版检测
- [ ] 实现双栏排版处理 (可选)
- [ ] 编写单元测试 `test_pdf_parser.py`
- [ ] 测试真实PDF文件

**验收标准**:
- ✅ 能提取PDF文字内容
- ✅ 能识别章节标题
- ✅ 能检测扫描版PDF
- ✅ 单元测试通过

---

### Phase 3: 统一接口重构 (1小时)

**任务清单**:
- [ ] 实现解析器工厂 `ParserFactory`
- [ ] 重构TXT解析器 `txt_parser.py`
- [ ] 更新API接口 `book_breakdown.py`
- [ ] 编写集成测试

**验收标准**:
- ✅ 三种格式都能正确解析
- ✅ 解析器自动选择正确
- ✅ API接口支持新格式

---

### Phase 4: 集成测试与文档 (1小时)

**任务清单**:
- [ ] 端到端测试 (上传EPUB/PDF → 分析)
- [ ] 更新API文档
- [ ] 更新用户指南
- [ ] 添加格式说明

**验收标准**:
- ✅ 所有格式测试通过
- ✅ 文档完整更新
- ✅ 用户指南清晰

---

## 验收标准总结

### 功能完整性
- ✅ EPUB格式支持
- ✅ PDF格式支持
- ✅ 统一解析器接口
- ✅ 格式自动检测

### 质量标准
- ✅ 章节识别准确率 ≥ 90%
- ✅ HTML标签清理完整
- ✅ 扫描版PDF能正确提示
- ✅ 单元测试覆盖率 ≥ 80%

### 性能标准
- ✅ EPUB解析: < 10秒 (100页)
- ✅ PDF解析: < 30秒 (100页)
- ✅ 内存使用: < 500MB

---

**创建时间**: 2025-10-27
**最后更新**: 2025-10-27
**维护者**: NovelAIde 开发团队
