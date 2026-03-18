from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import sqlalchemy as sa
from typing import AsyncGenerator
import logging
from contextlib import asynccontextmanager

from app.core.config import settings

logger = logging.getLogger(__name__)

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    future=True,
    pool_pre_ping=True,      # 连接前ping测试，确保连接有效
    pool_size=5,              # 连接池大小（配合 PG max_connections=20）
    max_overflow=10,          # 最大溢出连接数（总计 15，留 5 余量给 psql/Alembic）
    pool_recycle=1800,        # 30分钟后回收连接，防止长时间连接失效
    pool_timeout=30,          # 连接池获取连接的超时时间（秒）
    connect_args={
        "timeout": 10,        # TCP连接超时：10秒
        "command_timeout": 60,  # 命令执行超时：60秒
        "server_settings": {
            "statement_timeout": "900000",  # SQL语句超时：15分钟（毫秒）
            "idle_in_transaction_session_timeout": "900000"  # 事务空闲超时：15分钟
        }
    }
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 导出别名，供测试使用
async_session_maker = AsyncSessionLocal

# 创建基础模型类
Base = declarative_base()

def _ensure_worldview_version_column(sync_conn) -> None:
    """Ensure works.worldview_version exists for legacy DBs."""
    try:
        inspector = sa.inspect(sync_conn)
        if "works" not in inspector.get_table_names():
            return
        columns = {col["name"] for col in inspector.get_columns("works")}
        if "worldview_version" in columns:
            return
        logger.warning("[DB] works.worldview_version missing; adding column")
        sync_conn.execute(sa.text("ALTER TABLE works ADD COLUMN worldview_version INTEGER NOT NULL DEFAULT 1"))
    except Exception as exc:
        logger.warning(f"[DB] Failed to ensure works.worldview_version: {exc}")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    数据库会话依赖

    使用方法:
    async def some_route(db: AsyncSession = Depends(get_db)):
        ...
    """
    async with AsyncSessionLocal() as session:
        try:
            # 将提交职责交给服务层，避免在路由完成后再次提交引发异常
            yield session
        except Exception:
            # 出现异常时回滚事务
            await session.rollback()
            raise
        finally:
            # 确保会话被正确关闭
            try:
                await session.close()
            except Exception as e:
                logger.warning(f"关闭数据库会话时出错: {e}")
                # 强制关闭连接
                await session.invalidate()


@asynccontextmanager
async def create_db_session():
    """
    创建独立的数据库会话(用于并发任务)

    使用方法:
    async with create_db_session() as session:
        # 使用session
        await session.commit()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            try:
                await session.close()
            except Exception as e:
                logger.warning(f"关闭数据库会话时出错: {e}")
                await session.invalidate()


async def init_db():
    """初始化数据库表，带重试机制"""
    import asyncio
    import logging

    logger = logging.getLogger(__name__)
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            logger.info(f"正在初始化数据库... (尝试 {attempt + 1}/{max_retries})")
            async with engine.begin() as conn:
                # 检测 pgvector 扩展是否可用（用 savepoint 隔离，防止失败污染事务）
                pgvector_available = False
                try:
                    await conn.execute(sa.text("SAVEPOINT pgvector_check"))
                    await conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS vector"))
                    await conn.execute(sa.text("RELEASE SAVEPOINT pgvector_check"))
                    pgvector_available = True
                except Exception:
                    await conn.execute(sa.text("ROLLBACK TO SAVEPOINT pgvector_check"))
                    logger.warning("⚠️ pgvector 扩展未安装，跳过向量表创建。向量相关功能将不可用。")

                # 根据 pgvector 可用性决定创建哪些表
                if pgvector_available:
                    await conn.run_sync(Base.metadata.create_all)
                else:
                    tables_to_create = [
                        t for t in Base.metadata.sorted_tables
                        if t.name != "novel_analysis_vectors"
                    ]
                    await conn.run_sync(Base.metadata.create_all, tables=tables_to_create)

                await conn.run_sync(_ensure_worldview_version_column)
            logger.info("✅ 数据库初始化成功")
            return
        except Exception as e:
            logger.warning(f"数据库初始化失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"等待 {retry_delay} 秒后重试...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # 指数退避
            else:
                logger.error("❌ 数据库初始化失败，已达到最大重试次数")
                raise


async def close_db():
    """关闭数据库连接"""
    await engine.dispose()
