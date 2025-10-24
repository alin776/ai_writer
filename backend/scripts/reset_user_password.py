"""
Reset user password
"""
import asyncio
from app.core.database import get_db
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import select


async def main():
    username = "test_ai_user_3115"
    new_password = "test123456"
    
    print("=" * 60)
    print("Reset User Password")
    print("=" * 60)
    
    async for db in get_db():
        # Find user
        result = await db.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"User '{username}' not found")
            return
        
        print(f"Found user: {user.username}")
        print(f"User ID: {user.id}")
        print()
        
        # Update password
        user.hashed_password = get_password_hash(new_password)
        await db.commit()
        
        print(f"Password reset successfully!")
        print(f"Username: {username}")
        print(f"New password: {new_password}")
        print()
        print("You can now login with:")
        print(f"  Username: {username}")
        print(f"  Password: {new_password}")
        print()
        print("Frontend login: http://localhost:5173/login")
        
        break
    
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
