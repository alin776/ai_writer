from fastapi import APIRouter
from app.api.v1 import (
    auth,
    users,
    works,
    ai,
    worldview,
    novel_analysis,
    admin,
    search,
    relationships,
    timeline,
    groups,
    rewrite_history,

    ws,
    agent,
    monitoring,
    credits,
    invitations,
    admin_credits,
    admin_invitations,
    admin_works,
    admin_reports,
    notifications,
    user_tasks,
    library,
    comments,
    ratings,
    contact,
    channels,
    chapter_comments,
    stickers,
    friends,
    chapters_fs,
)
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
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(worldview.router, prefix="/worldview", tags=["worldview"])
api_router.include_router(relationships.router, prefix="/relationships", tags=["relationships"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(novel_analysis.router, prefix="/analysis", tags=["novel-analysis"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(rewrite_history.router, prefix="/rewrite-history", tags=["rewrite-history"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(ws.router, tags=["websocket"])
api_router.include_router(export_routes.router, prefix="/export", tags=["export"])
api_router.include_router(import_routes.router, tags=["import"])
api_router.include_router(ai_logs.router)

# 积分 / 邀请 / 通知 / 任务系统路由
api_router.include_router(credits.router, prefix="/credits", tags=["credits"])
api_router.include_router(invitations.router, prefix="/invitations", tags=["invitations"])
api_router.include_router(admin_credits.router, prefix="/admin/credits", tags=["admin-credits"])
api_router.include_router(admin_invitations.router, prefix="/admin/invitations", tags=["admin-invitations"])
api_router.include_router(admin_works.router, prefix="/admin/works", tags=["admin-works"])
api_router.include_router(admin_reports.router, prefix="/admin/reports", tags=["admin-reports"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(user_tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(library.router, prefix="/library", tags=["library"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(channels.router, prefix="/channels", tags=["channels"])
api_router.include_router(chapter_comments.router, tags=["chapter-comments"])
api_router.include_router(stickers.router, tags=["stickers"])
api_router.include_router(friends.router, prefix="/friends", tags=["friends"])
api_router.include_router(chapters_fs.router, prefix="/v2", tags=["chapters-fs"])
