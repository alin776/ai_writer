from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from app.core.config import settings

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    future=True,
    pool_pre_ping=True,      # 连接前ping测试，确保连接有效
    pool_size=10,             # 连接池大小
    max_overflow=20,          # 最大溢出连接数
    pool_recycle=3600,        # 1小时后回收连接，防止长时间连接失效
    connect_args={
        "server_settings": {
            "statement_timeout": "3600000",  # SQL语句超时：1小时（毫秒）
            "idle_in_transaction_session_timeout": "3600000"  # 事务空闲超时：1小时
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

# 创建基础模型类
Base = declarative_base()


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
            await session.close()


async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """关闭数据库连接"""
    await engine.dispose()
