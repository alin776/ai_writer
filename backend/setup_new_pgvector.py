import asyncio
import asyncpg

async def setup_pgvector():
    """在新的 Docker PostgreSQL 中创建 pgvector 扩展"""
    try:
        # 连接到新的数据库（端口 5433）
        conn = await asyncpg.connect(
            host='localhost',
            port=5433,
            user='novelaide',
            password='novelaide_password',
            database='novelaide'
        )

        print("[OK] Successfully connected to new PostgreSQL database (port 5433)")

        # 创建 vector 扩展
        await conn.execute('CREATE EXTENSION IF NOT EXISTS vector;')
        print("[OK] pgvector extension created successfully!")

        # 验证扩展
        result = await conn.fetch("SELECT * FROM pg_extension WHERE extname = 'vector';")
        if result:
            print("[OK] pgvector extension verified")
            print(f"     Version: {result[0]['extversion']}")
        else:
            print("[WARN] Extension created but verification failed")

        await conn.close()
        print("\n[OK] Database connection closed")
        print("\n[INFO] Next steps:")
        print("       1. Update DATABASE_URL in .env to use port 5433")
        print("       2. Restart the backend server")

    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        print(f"        Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(setup_pgvector())
