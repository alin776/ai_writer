"""
View analysis results - English version to avoid encoding issues
"""
import asyncio
from app.core.database import get_db
from app.models.novel_analysis import NovelAnalysis
from sqlalchemy import select


async def main():
    work_id = "fba38d52-78b1-4d9f-af74-958b70eb749d"
    
    async for db in get_db():
        result = await db.execute(
            select(NovelAnalysis).where(NovelAnalysis.work_id == work_id)
        )
        analysis = result.scalar_one_or_none()
        
        if analysis:
            print("=" * 60)
            print("ANALYSIS RESULTS")
            print("=" * 60)
            print(f"Status: {analysis.status}")
            print(f"Progress: {analysis.analyzed_chapters}/{analysis.total_chapters}")
            print(f"Stage: {analysis.current_stage}")
            print()
            
            if analysis.macro_results:
                print("Macro Analysis Report:")
                print("-" * 60)
                print(analysis.macro_results)
                print("-" * 60)
            else:
                print("No macro analysis results yet")
            
            print()
            print("View in browser:")
            print(f"http://localhost:5173/works/{work_id}")
            print("=" * 60)
        else:
            print("No analysis found for this work")
        
        break


if __name__ == "__main__":
    asyncio.run(main())
