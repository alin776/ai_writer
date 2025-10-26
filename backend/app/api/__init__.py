from fastapi import APIRouter
from app.api.v1 import auth, users, works, chapters, ai, worldview, novel_analysis, admin, search, relationships, timeline, groups, rewrite_history, humanize, review, ws
from app.api.v1 import export as export_routes
from app.api.v1 import import_routes
from app.api import ai_logs

api_router = APIRouter()

# 注册路由
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(works.router, prefix="/works", tags=["works"])
api_router.include_router(chapters.router, prefix="/chapters", tags=["chapters"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(worldview.router, prefix="/worldview", tags=["worldview"])
api_router.include_router(relationships.router, prefix="/relationships", tags=["relationships"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(novel_analysis.router, prefix="/analysis", tags=["novel-analysis"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(rewrite_history.router, prefix="/rewrite-history", tags=["rewrite-history"])  # AI改写历史
api_router.include_router(humanize.router, prefix="/humanize", tags=["humanize"])  # AI去痕迹功能
api_router.include_router(review.router, prefix="/review", tags=["review"])  # 小说评审功能
api_router.include_router(ws.router, tags=["websocket"])  # WebSocket实时推送
api_router.include_router(export_routes.router, tags=["export"])  # 导出功能（路由已包含/works前缀）
api_router.include_router(import_routes.router, tags=["import"])  # 导入功能（路由已包含/works前缀）
api_router.include_router(ai_logs.router)  # AI日志和成本统计
