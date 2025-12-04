import asyncio
import asyncpg
import bcrypt
from uuid import uuid4

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

async def create_admin_user():
    """Create admin user in database"""
    try:
        # Connect to database
        conn = await asyncpg.connect(
            host='localhost',
            port=5433,
            user='novelaide',
            password='novelaide_password',
            database='novelaide'
        )

        print("[OK] Connected to database")

        # Check if users table exists
        table_exists = await conn.fetchval(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')"
        )

        if not table_exists:
            print("[ERROR] Users table does not exist. Please run database migrations first.")
            await conn.close()
            return

        print("[OK] Users table exists")

        # Check if admin user already exists
        admin_email = "admin@example.com"
        existing_user = await conn.fetchrow(
            "SELECT * FROM users WHERE email = $1",
            admin_email
        )

        if existing_user:
            print(f"[INFO] Admin user already exists: {admin_email}")
            print(f"      User ID: {existing_user['id']}")
            print(f"      Username: {existing_user['username']}")
            print("\n[INFO] You can login with:")
            print(f"      Email: {admin_email}")
            print(f"      Password: change-this-password")
            await conn.close()
            return

        # Create admin user
        hashed_password = hash_password("change-this-password")
        user_id = uuid4()

        await conn.execute(
            """
            INSERT INTO users (id, username, email, hashed_password, is_active, is_admin, is_verified)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            user_id,
            "admin",
            admin_email,
            hashed_password,
            True,
            True,
            True
        )

        print(f"[OK] Admin user created successfully!")
        print(f"     User ID: {user_id}")
        print(f"     Username: admin")
        print(f"     Email: {admin_email}")
        print("\n[INFO] You can now login with:")
        print(f"      Email: {admin_email}")
        print(f"      Password: change-this-password")

        await conn.close()
        print("\n[OK] Database connection closed")

    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        print(f"        Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(create_admin_user())
