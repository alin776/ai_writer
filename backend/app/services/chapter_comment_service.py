"""
章节评论服务
处理评论相关的业务逻辑，包括级联删除
"""
import logging
import re
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_

from app.models.chapter_comment import ChapterComment

logger = logging.getLogger(__name__)


# 中文句子分割正则（与前端保持一致）
SENTENCE_END_REGEX = re.compile(r'([。！？.!?]+)')


def parse_paragraphs_from_html(html_content: str) -> List[str]:
    """
    从 HTML 内容中解析段落
    与前端 useContentParser 保持一致的逻辑
    """
    if not html_content:
        return []

    # 简单移除 HTML 标签
    import re
    # 移除 style 和 script 标签及其内容
    html_content = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # 尝试按 <p> 或 <div> 标签分割
    paragraphs = []

    # 查找所有 <p>...</p> 或 <div>...</div> 内容
    p_pattern = re.compile(r'<(?:p|div)[^>]*>(.*?)</(?:p|div)>', re.DOTALL | re.IGNORECASE)
    matches = p_pattern.findall(html_content)

    if matches:
        for match in matches:
            # 移除内部标签，只保留文本
            text = re.sub(r'<[^>]+>', '', match).strip()
            if text:
                paragraphs.append(text)
    else:
        # 如果没有 p/div 标签，移除所有标签后按换行符分割
        text = re.sub(r'<[^>]+>', '', html_content)
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                paragraphs.append(line)

    return paragraphs


def parse_sentences_from_paragraph(paragraph_text: str) -> List[str]:
    """
    从段落文本中解析句子
    与前端 useContentParser 保持一致的逻辑
    """
    if not paragraph_text:
        return []

    text = paragraph_text.strip()
    if not text:
        return []

    # 使用正则分割句子
    parts = SENTENCE_END_REGEX.split(text)
    sentences = []
    current_sentence = ''

    for part in parts:
        if not part:
            continue

        # 检查是否是句子结束标点
        if SENTENCE_END_REGEX.match(part):
            # 将标点加到当前句子
            current_sentence += part
            # 保存句子
            if current_sentence.strip():
                sentences.append(current_sentence.strip())
            current_sentence = ''
        else:
            current_sentence += part

    # 处理最后一个没有标点的句子
    if current_sentence.strip():
        sentences.append(current_sentence.strip())

    # 如果没有分割出句子，整个段落作为一个句子
    if not sentences and text:
        sentences.append(text)

    return sentences


async def cleanup_invalid_comments(
    db: AsyncSession,
    chapter_id: UUID,
    new_content: str,
    old_content: Optional[str] = None
) -> int:
    """
    清理因章节内容编辑而失效的评论

    策略：
    1. 章节级评论保留
    2. 段落级评论：如果段落索引超出新内容的段落数量，删除
    3. 句子级评论：如果段落或句子索引超出范围，或引用文本不再存在，删除

    返回：删除的评论数量
    """
    # 解析新内容的段落和句子结构
    new_paragraphs = parse_paragraphs_from_html(new_content)
    new_sentences_by_paragraph = {}

    for i, para in enumerate(new_paragraphs):
        new_sentences_by_paragraph[i] = parse_sentences_from_paragraph(para)

    logger.info(f"[ChapterCommentService] 章节 {chapter_id} 内容更新，新段落数: {len(new_paragraphs)}")

    # 获取该章节的所有非章节级评论
    query = select(ChapterComment).where(
        and_(
            ChapterComment.chapter_id == chapter_id,
            ChapterComment.is_deleted == False,
            ChapterComment.location_type != 'chapter'
        )
    )
    result = await db.execute(query)
    comments = result.scalars().all()

    deleted_count = 0
    comments_to_delete = []

    for comment in comments:
        should_delete = False
        reason = ""

        if comment.location_type == 'paragraph':
            # 检查段落索引是否有效
            if comment.paragraph_index is None or comment.paragraph_index >= len(new_paragraphs):
                should_delete = True
                reason = f"段落索引 {comment.paragraph_index} 超出范围 (共 {len(new_paragraphs)} 段)"

        elif comment.location_type == 'sentence':
            # 检查段落索引
            if comment.paragraph_index is None or comment.paragraph_index >= len(new_paragraphs):
                should_delete = True
                reason = f"段落索引 {comment.paragraph_index} 超出范围"
            else:
                # 检查句子索引
                sentences = new_sentences_by_paragraph.get(comment.paragraph_index, [])
                if comment.sentence_index is None or comment.sentence_index >= len(sentences):
                    should_delete = True
                    reason = f"句子索引 {comment.sentence_index} 超出范围 (该段共 {len(sentences)} 句)"
                elif comment.quoted_text:
                    # 可选：检查引用文本是否还存在于对应句子中
                    sentence_text = sentences[comment.sentence_index] if comment.sentence_index < len(sentences) else ""
                    if comment.quoted_text not in sentence_text:
                        # 也检查整个段落
                        paragraph_text = new_paragraphs[comment.paragraph_index]
                        if comment.quoted_text not in paragraph_text:
                            should_delete = True
                            reason = f"引用文本不再存在"

        if should_delete:
            comments_to_delete.append(comment)
            logger.info(f"[ChapterCommentService] 标记删除评论 {comment.id}: {reason}")

    # 软删除这些评论
    for comment in comments_to_delete:
        comment.is_deleted = True
        deleted_count += 1

    if deleted_count > 0:
        await db.commit()
        logger.info(f"[ChapterCommentService] 章节 {chapter_id} 清理了 {deleted_count} 条失效评论")

    return deleted_count


async def delete_all_chapter_comments(db: AsyncSession, chapter_id: UUID) -> int:
    """
    删除章节的所有评论（当章节被删除时调用）
    使用软删除
    """
    # 软删除所有评论
    query = select(ChapterComment).where(
        and_(
            ChapterComment.chapter_id == chapter_id,
            ChapterComment.is_deleted == False
        )
    )
    result = await db.execute(query)
    comments = result.scalars().all()

    deleted_count = 0
    for comment in comments:
        comment.is_deleted = True
        deleted_count += 1

    if deleted_count > 0:
        await db.commit()
        logger.info(f"[ChapterCommentService] 章节 {chapter_id} 删除，清理了 {deleted_count} 条评论")

    return deleted_count
