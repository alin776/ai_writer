from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import traceback

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.redis import redis_client
from app.api import api_router
from app.tasks import start_scheduler, stop_scheduler

# 配置日志
import os
from logging.handlers import RotatingFileHandler

# 确保logs目录存在
os.makedirs("./logs", exist_ok=True)

# 配置根日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # 控制台输出
        logging.StreamHandler(),
        # 文件输出
        RotatingFileHandler(
            './logs/app.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("[STARTUP] 应用启动中...")

    await init_db()
    # await redis_client.init()  # TODO: Redis 暂时禁用
    await start_scheduler()  # 启动定时任务

    # 预初始化AsyncRedisSaver索引（性能优化）
    try:
        from app.services.agent.langgraph_agent import WritingAgentGraph
        logger.info("[STARTUP] 开始初始化AsyncRedisSaver索引...")
        await WritingAgentGraph.setup_checkpointer()
        logger.info("[STARTUP] AsyncRedisSaver索引初始化完成")
    except Exception as e:
        logger.warning(f"[STARTUP] AsyncRedisSaver索引初始化失败: {e}")

    # 预加载Embedding模型（性能优化）
    try:
        from app.services.vector_store_service import VectorStoreService
        logger.info("[STARTUP] 开始预加载Embedding模型...")
        VectorStoreService.preload_model()
        logger.info("[STARTUP] Embedding模型预加载完成")
    except Exception as e:
        logger.warning(f"[STARTUP] Embedding模型预加载失败: {e}")
        logger.warning("[STARTUP] 首次向量化时将自动加载模型")

    logger.info("[STARTUP] 应用启动完成")

    yield

    # 关闭时执行
    logger.info("[SHUTDOWN] 应用关闭中...")
    await stop_scheduler()  # 停止定时任务
    await close_db()
    # await redis_client.close()  # TODO: Redis 暂时禁用
    logger.info("[SHUTDOWN] 应用已关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI辅助写小说工具 - 后端API",
    lifespan=lifespan,
)

# 全局异常处理
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """捕获422参数验证错误，详细记录"""
    logger.error("="*60)
    logger.error(f"422 参数验证错误 - URL: {request.url.path}")
    logger.error(f"请求方法: {request.method}")
    
    # 记录请求体
    try:
        body = await request.body()
        logger.error(f"请求体: {body.decode('utf-8')}")
    except:
        logger.error("无法读取请求体")
    
    # 记录验证错误详情
    logger.error(f"验证错误详情: {exc.errors()}")
    logger.error("="*60)
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """捕获所有未处理的异常"""
    logger.error(f"Global exception handler caught: {type(exc).__name__}")
    logger.error(f"Exception: {exc}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": f"Internal server error: {type(exc).__name__}: {str(exc)}"
        }
    )

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    # 配置 uvicorn 日志
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_config["formatters"]["access"]["fmt"] = '%(asctime)s - %(levelname)s - %(client_addr)s - "%(request_line)s" %(status_code)s'

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=log_config,
        log_level="info"
    )
