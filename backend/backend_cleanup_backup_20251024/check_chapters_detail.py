"""
Check chapters detail
"""
import asyncio
from app.core.database import get_db
from app.models.chapter import Chapter
from sqlalchemy import select, func


async def main():
    work_id = "fba38d52-78b1-4d9f-af74-958b70eb749d"
    
    print("=" * 60)
    print("Check Chapters Detail")
    print("=" * 60)
    
    async for db in get_db():
        # Count chapters
        result = await db.execute(
            select(func.count(Chapter.id)).where(Chapter.work_id == work_id)
        )
        count = result.scalar()
        
        print(f"Total chapters: {count}")
        print()
        
        if count > 0:
            # Get all chapters
            result = await db.execute(
                select(Chapter)
                .where(Chapter.work_id == work_id)
                .order_by(Chapter.order)
            )
            chapters = result.scalars().all()
            
            print(f"Chapter list:")
            for ch in chapters:
                print(f"  [{ch.order}] {ch.title} - {ch.word_count} words (ID: {ch.id})")
        else:
            print("No chapters found!")
            print()
            print("This means the performance test did not create chapters successfully.")
            print("Possible reasons:")
            print("1. Test script was interrupted")
            print("2. Database transaction rollback")
            print("3. Permission issues")
        
        break
    
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
