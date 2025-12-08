from fastapi import APIRouter
from app.api.v1 import auth, users, works, chapters, ai, worldview, novel_analysis, admin, search, relationships, timeline, groups, rewrite_history, humanize, review, ws, knowledge, agent, monitoring, credits, invitations, admin_credits, admin_invitations
from app.api.v1.endpoints import books
from app.api.v1 import export as export_routes
from app.api.v1 import import_routes
from app.api import ai_logs

api_router = APIRouter()

# 注册路由
# 监控和健康检查（基础设施）
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])

# 业务路由
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
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])  # 知识库功能
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])  # Agent智能助手
api_router.include_router(books.router, prefix="/books", tags=["books"])  # AI拆书功能
api_router.include_router(ws.router, tags=["websocket"])  # WebSocket实时推送
api_router.include_router(export_routes.router, tags=["export"])  # 导出功能（路由已包含/works前缀）
api_router.include_router(import_routes.router, tags=["import"])  # 导入功能（路由已包含/works前缀）
api_router.include_router(ai_logs.router)  # AI日志和成本统计

# 积分系统路由
api_router.include_router(credits.router, prefix="/credits", tags=["credits"])  # 积分管理
api_router.include_router(invitations.router, prefix="/invitations", tags=["invitations"])  # 邀请系统
api_router.include_router(admin_credits.router, prefix="/admin/credits", tags=["admin-credits"])  # 管理端积分
api_router.include_router(admin_invitations.router, prefix="/admin/invitations", tags=["admin-invitations"])  # 管理端邀请码
