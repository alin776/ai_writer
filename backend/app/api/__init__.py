from fastapi import APIRouter
from app.api.v1 import auth, users, works, chapters, ai, worldview, novel_analysis

api_router = APIRouter()

# 注册路由
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(works.router, prefix="/works", tags=["works"])
api_router.include_router(chapters.router, prefix="/chapters", tags=["chapters"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(worldview.router, prefix="/worldview", tags=["worldview"])
api_router.include_router(novel_analysis.router, prefix="/analysis", tags=["novel-analysis"])
