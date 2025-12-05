from pathlib import Path
from uuid import UUID
import re

path = Path('backend/app/services/import_service.py')
text = path.read_text(encoding='utf-8', errors='ignore')
start = text.find('async def _import_text')
end = text.find('\n    def _extract_title', start)
if start == -1 or end == -1:
    raise SystemExit('markers not found')
new_block = """async def _import_text(
        self,
        content: bytes,
        user_id: UUID,
        options: ImportOptions,
        append_to: Optional[str] = None
    ) -> ImportResponse:
        \"\"\"导入文本/Markdown格式\"\"\"
        logger.info(f\"用户 {user_id} 开始导入文本数据\")
        
        text = content.decode('utf-8')
        
        # 提取标题
        title = self._extract_title(text)
        
        # 分割章节
        chapters = self._split_chapters(text)
        if not chapters:
            chapters = [{'title': title, 'content': text.strip()}]
        
        work: Work
        starting_order = 0
        total_words = 0

        if append_to:
            work_id = UUID(str(append_to)) if not isinstance(append_to, UUID) else append_to
            work = await self.db.get(Work, work_id)
            if not work:
                raise ValueError(\"目标作品不存在，无法导入\")
            if str(work.author_id) != str(user_id):
                raise ValueError(\"无权导入到该作品\")
            starting_order = work.total_chapters or 0
            total_words = work.total_words or 0
        else:
            work = Work(
                author_id=user_id,
                title=title,
                description=None,
                genre=WorkGenre.OTHER,
                status=WorkStatus.DRAFT,
                total_words=0,
                total_chapters=0
            )
            self.db.add(work)
            await self.db.flush()
        
        # 导入章节
        chapters_created = 0
        for idx, chapter_data in enumerate(chapters):
            content_text = chapter_data['content']
            word_count = len(content_text.replace('\\n', '').replace(' ', ''))
            total_words += word_count

            chapter = Chapter(
                work_id=work.id,
                title=chapter_data['title'],
                content=f\"<p>{content_text.replace(chr(10), '</p><p>')}</p>\",  # 简单HTML转换
                order=starting_order + idx + 1,
                word_count=word_count,
                status=ChapterStatus.DRAFT,
                is_published=False
            )
            self.db.add(chapter)
            chapters_created += 1

        # 更新作品统计
        work.total_chapters = (work.total_chapters or 0) + chapters_created
        work.total_words = total_words
        
        await self.db.commit()
        
        logger.info(f\"文本导入完成: 作品ID={work.id}, 章节={chapters_created}\")
        
        return ImportResponse(
            work_id=work.id,
            chapters_created=chapters_created,
            message=\"导入成功\"
        )

"""

new_text = text[:start] + new_block + text[end+1:]
path.write_text(new_text, encoding='utf-8')
