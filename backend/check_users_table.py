import asyncio
import asyncpg

async def check_users_table():
    """Check users table structure"""
    try:
        conn = await asyncpg.connect(
            host='localhost',
            port=5433,
            user='novelaide',
            password='novelaide_password',
            database='novelaide'
        )

        print("[OK] Connected to database")

        # Get table columns
        columns = await conn.fetch(
            """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position
            """
        )

        if columns:
            print("\n[INFO] Users table structure:")
            print("-" * 80)
            for col in columns:
                print(f"  - {col['column_name']:20} | {col['data_type']:15} | Nullable: {col['is_nullable']}")
            print("-" * 80)
        else:
            print("[WARN] No columns found for users table")

        await conn.close()

    except Exception as e:
        print(f"[ERROR] Failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_users_table())
