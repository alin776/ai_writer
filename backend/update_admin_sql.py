import asyncio
import asyncpg
from app.core.security import get_password_hash

async def update_admin():
    """直接用SQL更新管理员权限"""
    conn = await asyncpg.connect(
        host='localhost',
        port=5432,
        user='novelaide',
        password='131457',
        database='novelaide'
    )
    
    # 检查用户是否存在
    user = await conn.fetchrow(
        "SELECT * FROM users WHERE username = $1",
        "alin"
    )
    
    if user:
        print("用户 'alin' 已存在，正在更新为管理员权限...")
        await conn.execute(
            """UPDATE users 
               SET is_admin = true, is_active = true, is_verified = true
               WHERE username = $1""",
            "alin"
        )
        print("✅ 用户 'alin' 已更新为管理员！")
    else:
        print("创建新的管理员账号...")
        hashed_password = get_password_hash("131457")
        await conn.execute(
            """INSERT INTO users (username, email, hashed_password, is_active, is_admin, is_verified)
               VALUES ($1, $2, $3, $4, $5, $6)""",
            "alin", "alin@example.com", hashed_password, True, True, True
        )
        print("✅ 管理员账号创建成功！")
    
    print("\n管理员信息:")
    print(f"  用户名: alin")
    print(f"  密码: 131457")
    print(f"  管理员权限: 是")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(update_admin())
