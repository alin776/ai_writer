from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import traceback
import os
import sys

# ⚡ 最早设置 HuggingFace 镜像，必须在任何 huggingface_hub / sentence_transformers 导入之前
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

# 修复 Windows 控制台 UTF-8 编码问题（解决 emoji 输出导致的 UnicodeEncodeError）
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# 确保启动时加载全部模型，init_db(create_all) 才能感知新增表结构。
import app.models  # noqa: F401

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.redis import redis_client
from app.api import api_router
from app.api.middleware import TraceMiddleware, MonitoringMiddleware
from app.tasks import start_scheduler, stop_scheduler

# 配置日志
from logging.handlers import RotatingFileHandler


class AccessLogFilter(logging.Filter):
    """过滤高频轮询接口的访问日志"""
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        return "/api/v1/channels/unread-summary" not in msg


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
# 调度开关（用于避免多实例重复跑任务）
ENABLE_SCHEDULER = os.getenv("ENABLE_SCHEDULER", "true").lower() == "true"

# 🔧 2025-12-02: Phase 1 日志优化 - 配置第三方库日志级别
# 防止第三方库的DEBUG日志污染系统日志
logging.getLogger('jieba').setLevel(logging.WARNING)
logging.getLogger('chromadb').setLevel(logging.WARNING)
logging.getLogger('chromadb.telemetry').setLevel(logging.ERROR)  # 关闭telemetry提示
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('apscheduler').setLevel(logging.WARNING)
logging.getLogger('redisvl').setLevel(logging.WARNING)
logging.getLogger('langgraph').setLevel(logging.WARNING)

# 降低monitoring_middleware的日志级别，减少日志冗余
logging.getLogger('app.api.middleware.monitoring_middleware').setLevel(logging.DEBUG)

# 过滤 uvicorn access log 中的高频轮询接口
logging.getLogger('uvicorn.access').addFilter(AccessLogFilter())

# 抑制jieba的pkg_resources警告
import warnings
warnings.filterwarnings('ignore', module='jieba._compat')
warnings.filterwarnings('ignore', message='pkg_resources is deprecated')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("[STARTUP] 应用启动中...")

    await init_db()

    # 预加载 Embedding 模型，避免首次 Agent 调用时 ~7 秒延迟
    try:
        from app.services.embedding import preload_model
        preload_model()
    except Exception as e:
        logger.warning(f"[STARTUP] ⚠️ Embedding 模型预加载失败（不影响启动）: {e}")

    # 初始化官方频道
    try:
        from init_official_channels_sql import init_channels
        logger.info("[STARTUP] 开始检查并初始化官方频道...")
        await init_channels()
        logger.info("[STARTUP] ✅ 官方频道检查完成")
    except Exception as e:
        logger.warning(f"[STARTUP] ⚠️ 官方频道初始化失败: {e}")

    # await redis_client.init()  # TODO: Redis 暂时禁用
    scheduler_started = False
    if ENABLE_SCHEDULER:
        start_scheduler()  # 启动定时任务（同步函数）
        scheduler_started = True
    else:
        logger.info("[STARTUP] 跳过启动定时任务调度器（ENABLE_SCHEDULER=false）")

    logger.info("[STARTUP] 应用启动完成")

    # 清理上次崩溃/重启可能遗留的 Docker sandbox 容器
    try:
        from app.services.agent.deep_agent.docker_sandbox import DockerSandbox
        cleaned = DockerSandbox.cleanup_stale_containers()
        if cleaned:
            logger.info("[STARTUP] 已清理 %d 个残留 sandbox 容器", cleaned)
    except Exception as e:
        logger.debug("[STARTUP] Docker sandbox 清理跳过: %s", e)

    yield

    # 关闭时执行
    logger.info("[SHUTDOWN] 应用关闭中...")
    if scheduler_started:
        stop_scheduler()  # 停止定时任务（同步函数）
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

# 🔧 添加监控中间件
# 注意：中间件执行顺序是反向的，先添加的后执行
# 执行顺序：MonitoringMiddleware -> TraceMiddleware -> 业务逻辑
app.add_middleware(MonitoringMiddleware)  # 监控（使用trace_id）
app.add_middleware(TraceMiddleware)       # 生成trace_id（最先执行）

logger.info("[STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware")

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
        reload_dirs=["app"] if settings.DEBUG else None,
        log_config=log_config,
        log_level="info"
    )
