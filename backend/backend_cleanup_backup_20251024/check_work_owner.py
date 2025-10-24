"""
Check work owner
"""
import asyncio
from app.core.database import get_db
from app.models.work import Work
from app.models.user import User
from sqlalchemy import select


async def main():
    work_id = "fba38d52-78b1-4d9f-af74-958b70eb749d"
    username = "test_ai_user_3115"
    
    print("=" * 60)
    print("Check Work Owner")
    print("=" * 60)
    
    async for db in get_db():
        # Get work
        result = await db.execute(select(Work).where(Work.id == work_id))
        work = result.scalar_one_or_none()
        
        if not work:
            print(f"Work {work_id} not found!")
            return
        
        print(f"Work found: {work.title}")
        print(f"Work ID: {work.id}")
        print(f"Author ID: {work.author_id}")
        print()
        
        # Get user
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"User {username} not found!")
            return
        
        print(f"User: {user.username}")
        print(f"User ID: {user.id}")
        print()
        
        # Check ownership
        if str(work.author_id) == str(user.id):
            print("STATUS: User owns this work!")
            print()
            print("You should be able to access:")
            print(f"http://localhost:5173/works/{work_id}")
        else:
            print("STATUS: User does NOT own this work!")
            print()
            print("SOLUTION: The work belongs to a different user.")
            print("Options:")
            print("1. Re-run the performance test after logging in with current user")
            print("2. Or change work ownership (see below)")
            print()
            print("To change ownership:")
            print(f"UPDATE works SET author_id = '{user.id}' WHERE id = '{work_id}';")
        
        break
    
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
