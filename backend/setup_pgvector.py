import asyncio
import asyncpg

async def setup_pgvector():
    """尝试在数据库中创建 pgvector 扩展"""
    try:
        # 连接到数据库
        conn = await asyncpg.connect(
            host='localhost',
            port=5432,
            user='novelaide',
            password='novelaide_password',
            database='novelaide'
        )

        print("[OK] Successfully connected to database")

        # 尝试创建 vector 扩展
        try:
            await conn.execute('CREATE EXTENSION IF NOT EXISTS vector;')
            print("[OK] pgvector extension created successfully!")

            # 验证扩展
            result = await conn.fetch("SELECT * FROM pg_extension WHERE extname = 'vector';")
            if result:
                print("[OK] pgvector extension verified")
                print(f"     Version: {result[0]['extversion']}")
            else:
                print("[WARN] Extension created but verification failed")

        except asyncpg.exceptions.UndefinedFileError as e:
            print("[ERROR] pgvector extension files not found")
            print("        This means pgvector is not installed in PostgreSQL")
            print("\n        Solutions:")
            print("        1. Use Docker with pgvector-enabled PostgreSQL (recommended)")
            print("        2. Manually compile and install pgvector (requires build tools)")
            print(f"\n        Error details: {e}")

        except Exception as e:
            print(f"[ERROR] Error creating extension: {e}")
            print(f"        Error type: {type(e).__name__}")

        await conn.close()
        print("\n[OK] Database connection closed")

    except asyncpg.exceptions.InvalidPasswordError:
        print("[ERROR] Invalid database password")
        print("        Please check DATABASE_URL in .env file")
    except asyncpg.exceptions.InvalidCatalogNameError:
        print("[ERROR] Database does not exist")
        print("        Please create 'novelaide' database first")
    except Exception as e:
        print(f"[ERROR] Failed to connect to database: {e}")
        print(f"        Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(setup_pgvector())
