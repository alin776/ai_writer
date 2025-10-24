"""
Check work statistics
"""
import asyncio
from app.core.database import get_db
from app.models.work import Work
from sqlalchemy import select


async def main():
    work_id = "fba38d52-78b1-4d9f-af74-958b70eb749d"
    
    print("=" * 60)
    print("Check Work Statistics")
    print("=" * 60)
    
    async for db in get_db():
        result = await db.execute(select(Work).where(Work.id == work_id))
        work = result.scalar_one_or_none()
        
        if work:
            print(f"Title: {work.title}")
            print(f"Total chapters: {work.total_chapters}")
            print(f"Total words: {work.total_words}")
            print(f"Status: {work.status}")
            print(f"Genre: {work.genre}")
            print()
            
            if work.total_chapters is None or work.total_chapters == 0:
                print("PROBLEM: total_chapters is not set!")
                print()
                print("Need to update work statistics.")
                print("Run this SQL in pgAdmin:")
                print()
                print(f"UPDATE works SET ")
                print(f"  total_chapters = (SELECT COUNT(*) FROM chapters WHERE work_id = '{work_id}'),")
                print(f"  total_words = (SELECT SUM(word_count) FROM chapters WHERE work_id = '{work_id}')")
                print(f"WHERE id = '{work_id}';")
        else:
            print("Work not found!")
        
        break
    
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
