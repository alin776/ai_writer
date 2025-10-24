"""
Check analysis data in database
"""
import asyncio
from app.core.database import get_db
from app.models.novel_analysis import NovelAnalysis
from sqlalchemy import select


async def main():
    print("=" * 60)
    print("Checking Analysis Data")
    print("=" * 60)
    
    async for db in get_db():
        # Get all analyses
        result = await db.execute(select(NovelAnalysis))
        analyses = result.scalars().all()
        
        print(f"Total analyses in database: {len(analyses)}\n")
        
        for analysis in analyses:
            print(f"Analysis ID: {analysis.id}")
            print(f"Work ID: {analysis.work_id}")
            print(f"Status: {analysis.status}")
            print(f"Progress: {analysis.analyzed_chapters}/{analysis.total_chapters}")
            print(f"Has macro_results: {analysis.macro_results is not None}")
            if analysis.macro_results:
                print(f"Macro results length: {len(analysis.macro_results)} chars")
            print(f"Has micro_results: {analysis.micro_results is not None}")
            if analysis.micro_results:
                print(f"Micro results keys: {len(analysis.micro_results)} chapters")
            print("-" * 60)
        
        break


if __name__ == "__main__":
    asyncio.run(main())
