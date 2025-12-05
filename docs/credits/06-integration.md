# 系统集成方案

> ⚠️ **文档状态**: 设计文档，功能尚未实现

## 1. 集成概览

积分系统需要与以下现有模块集成：

| 模块 | 集成点 | 说明 |
|------|--------|------|
| 用户服务 | 新用户注册 | 验证邀请码、赠送初始积分 |
| AI 服务 | AI 调用 | 管理员豁免、检查余额、扣减积分 |
| 认证系统 | API 路由 | 权限验证 |
| 邀请系统 | 激活检测 | 消费/充值后检查激活条件 |

---

## 2. 用户注册集成（含邀请码）

### 2.1 修改位置

**文件**: `backend/app/api/v1/auth.py`

**路由**: `POST /api/v1/auth/register`

### 2.2 集成代码

```python
# backend/app/api/v1/auth.py

from app.services.credit_service import CreditService
from app.services.invitation_service import InvitationService
from app.core.config import settings

@router.post("/register")
async def register(
    request: RegisterRequest,
    request_info: Request,
    db: AsyncSession = Depends(get_db)
):
    """注册（需邀请码）"""
    invitation_service = InvitationService(db)
    credit_service = CreditService(db)

    # 1. 验证邀请码
    ip_address = request_info.client.host
    device_fingerprint = request_info.headers.get("X-Device-Fingerprint")

    is_valid, error_msg, invitation = await invitation_service.validate_invitation_code(
        code=request.invitation_code,
        ip_address=ip_address,
        device_fingerprint=device_fingerprint
    )
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # 2. 创建用户
    user = User(
        username=request.username,
        email=request.email,
        hashed_password=hash_password(request.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # 3. 赠送新用户积分
    if settings.NEW_USER_GIFT_CREDITS > 0:
        await credit_service.gift(
            user_id=user.id,
            amount=settings.NEW_USER_GIFT_CREDITS,
            description="新用户注册赠送",
            related_type="new_user"
        )

    # 4. 记录邀请使用
    await invitation_service.use_invitation_code(
        code=request.invitation_code,
        invitee_id=user.id,
        ip_address=ip_address,
        device_fingerprint=device_fingerprint
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "credits": {
            "balance": settings.NEW_USER_GIFT_CREDITS,
            "gift_from_registration": settings.NEW_USER_GIFT_CREDITS
        }
    }
```

---

## 3. AI 调用集成

### 3.1 集成架构

```
┌─────────────────────────────────────────────────────────┐
│                     AI 调用流程                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  1. 检查积分系统开关   │
              │  settings.CREDITS_ENABLED
              └───────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            │ 关闭                       │ 开启
            ▼                           ▼
   ┌─────────────┐           ┌───────────────────────┐
   │ 直接调用 AI  │           │  2. 检查余额          │
   └─────────────┘           │  credit_service.      │
                             │    check_sufficient() │
                             └───────────────────────┘
                                        │
                          ┌─────────────┴─────────────┐
                          │ 不足                       │ 充足
                          ▼                           ▼
               ┌─────────────────┐         ┌───────────────────┐
               │ 返回余额不足错误 │         │  3. 调用 AI        │
               └─────────────────┘         └───────────────────┘
                                                      │
                                                      ▼
                                           ┌───────────────────┐
                                           │  4. 计算消耗积分   │
                                           │  calculate_credits │
                                           └───────────────────┘
                                                      │
                                           ┌──────────┴──────────┐
                                           │ 失败                 │ 成功
                                           ▼                     ▼
                                  ┌──────────────┐    ┌───────────────────┐
                                  │ 不扣积分     │    │  5. 扣减积分      │
                                  │ (或退还预扣) │    │  credit_service.  │
                                  └──────────────┘    │    consume()      │
                                                      └───────────────────┘
```

### 3.2 修改位置

**方案 A**: 在 Agent 层集成（推荐）

**文件**: `backend/app/services/agent/langgraph_agent.py`

**方案 B**: 在 AI Service 层集成

**文件**: `backend/app/services/ai/http_ai_service.py`

### 3.3 Agent 层集成代码（含管理员豁免）

```python
# backend/app/services/agent/langgraph_agent.py

from app.services.credit_service import CreditService
from app.services.invitation_service import InvitationService
from app.services.credit_exceptions import InsufficientCreditsError
from app.utils.credit_utils import calculate_credits_for_ai_call
from app.core.config import settings

class WritingAgentGraph:

    async def chat_stream(
        self,
        user: User,  # 传入完整 User 对象
        message: str,
        ...
    ):
        """流式对话"""

        # 1. 检查管理员豁免
        is_admin_exempt = user.is_admin and settings.ADMIN_CREDITS_EXEMPT

        # 2. 检查积分（非管理员）
        if settings.CREDITS_ENABLED and not is_admin_exempt:
            credit_service = CreditService(self.db)
            is_sufficient, balance = await credit_service.check_sufficient(
                user_id=user.id,
                required_credits=Decimal("0.01")  # 最小检查值
            )
            if not is_sufficient:
                raise InsufficientCreditsError(
                    required=Decimal("0.01"),
                    available=balance
                )

        # 3. 执行 AI 调用
        try:
            result = await self._execute_ai_call(...)

            # 4. 计算并扣减积分
            if settings.CREDITS_ENABLED:
                credits_consumed = calculate_credits_for_ai_call(
                    model_name=result.model_name,
                    prompt_tokens=result.prompt_tokens,
                    completion_tokens=result.completion_tokens
                )

                if is_admin_exempt:
                    # 管理员豁免：仅记录日志，不扣积分
                    logger.info(
                        f"Admin {user.username} used {credits_consumed} credits (exempt)"
                    )
                else:
                    # 普通用户：扣减积分
                    await credit_service.consume(
                        user_id=user.id,
                        amount=credits_consumed,
                        description=f"AI 调用: {result.model_name}",
                        related_id=result.log_id
                    )

                    # 5. 检查邀请激活（如果是被邀请人）
                    invitation_service = InvitationService(self.db)
                    await invitation_service.activate_invitation(user.id)

            return result

        except Exception as e:
            # AI 调用失败，不扣积分
            raise
```

### 3.4 异常处理

```python
# backend/app/api/v1/agent.py

from app.services.credit_exceptions import InsufficientCreditsError, CreditsExpiredError

@router.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        agent = WritingAgentGraph(db=db, ...)
        result = await agent.chat_stream(
            user_id=current_user.id,
            message=request.message
        )
        return result

    except InsufficientCreditsError as e:
        raise HTTPException(
            status_code=402,  # Payment Required
            detail={
                "code": "INSUFFICIENT_CREDITS",
                "message": "积分余额不足",
                "required": float(e.required),
                "available": float(e.available)
            }
        )

    except CreditsExpiredError as e:
        raise HTTPException(
            status_code=402,
            detail={
                "code": "CREDITS_EXPIRED",
                "message": "积分已过期",
                "expired_at": e.expired_at.isoformat()
            }
        )
```

---

## 4. 邀请激活集成

### 4.1 消费后激活检测

在 AI 调用扣费后自动检查激活（如上 3.3 所示）。

### 4.2 充值后激活检测

在兑换码兑换后检查激活：

```python
# backend/app/api/v1/credits.py

from app.services.invitation_service import InvitationService

@router.post("/redeem")
async def redeem_code(
    request: RedeemRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """兑换码兑换"""
    redeem_service = RedeemCodeService(db)
    invitation_service = InvitationService(db)

    # 1. 兑换
    result = await redeem_service.redeem(
        code=request.code,
        user_id=current_user.id
    )

    # 2. 检查邀请激活
    await invitation_service.activate_invitation(current_user.id)

    return {
        "credits": result.credits,
        "balance_before": result.balance_before,
        "balance_after": result.balance_after
    }
```

### 4.3 定时任务：过期邀请清理

```python
# backend/app/tasks/invitation_cleanup.py

from datetime import datetime, timedelta
from app.services.invitation_service import InvitationService

async def cleanup_expired_invitations(db: AsyncSession):
    """清理过期未激活的邀请"""
    invitation_service = InvitationService(db)

    # 查询 7 天前注册但未激活的邀请
    seven_days_ago = datetime.now() - timedelta(days=7)

    stmt = select(InvitationUsage).where(
        InvitationUsage.status == "pending",
        InvitationUsage.created_at < seven_days_ago
    )
    result = await db.execute(stmt)
    expired_usages = result.scalars().all()

    # 标记为已过期
    for usage in expired_usages:
        usage.status = "expired"

    await db.commit()

    logger.info(f"Marked {len(expired_usages)} invitations as expired")
```

---

## 5. API 路由注册

### 5.1 注册积分路由

**文件**: `backend/app/api/__init__.py`

```python
from app.api.v1 import credits, invitations

api_router = APIRouter()

# ... 其他路由 ...

# 积分系统路由
api_router.include_router(
    credits.router,
    prefix="/credits",
    tags=["credits"]
)

# 邀请系统路由
api_router.include_router(
    invitations.router,
    prefix="/invitations",
    tags=["invitations"]
)
```

### 5.2 注册管理端路由

```python
from app.api.v1 import admin_credits, admin_invitations

# 管理端积分路由
api_router.include_router(
    admin_credits.router,
    prefix="/admin/credits",
    tags=["admin-credits"]
)

# 管理端邀请路由
api_router.include_router(
    admin_invitations.router,
    prefix="/admin/invitations",
    tags=["admin-invitations"]
)
```

---

## 6. 模型注册

### 6.1 注册新模型

**文件**: `backend/app/models/__init__.py`

```python
from app.models.user_credits import UserCredits
from app.models.credit_transaction import CreditTransaction
from app.models.redeem_code import RedeemCode
from app.models.user_invitation import UserInvitation
from app.models.invitation_usage import InvitationUsage

__all__ = [
    # ... 其他模型 ...
    "UserCredits",
    "CreditTransaction",
    "RedeemCode",
    "UserInvitation",
    "InvitationUsage",
]
```

---

## 7. 数据库迁移

### 7.1 生成迁移

```bash
cd backend

# 积分系统迁移
./venv/Scripts/alembic.exe revision --autogenerate -m "add_credits_tables"

# 邀请系统迁移
./venv/Scripts/alembic.exe revision --autogenerate -m "add_invitation_tables"
```

### 7.2 执行迁移

```bash
./venv/Scripts/alembic.exe upgrade head
```

### 7.3 迁移文件示例

```python
# backend/alembic/versions/20251202_xxxx_add_credits_tables.py

"""add credits tables

Revision ID: xxxx
Revises: yyyy
Create Date: 2025-12-02 xx:xx:xx
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'xxxx'
down_revision = 'yyyy'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # user_credits 表
    op.create_table(
        'user_credits',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('balance', sa.DECIMAL(10, 2), nullable=False, server_default='0.00'),
        sa.Column('total_recharged', sa.DECIMAL(10, 2), nullable=False, server_default='0.00'),
        sa.Column('total_consumed', sa.DECIMAL(10, 2), nullable=False, server_default='0.00'),
        sa.Column('total_gifted', sa.DECIMAL(10, 2), nullable=False, server_default='0.00'),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_user_credits_user_id', 'user_credits', ['user_id'])
    op.create_index('ix_user_credits_expires_at', 'user_credits', ['expires_at'])

    # credit_transactions 表
    op.create_table(
        'credit_transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('amount', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('balance_before', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('balance_after', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('related_type', sa.String(50), nullable=True),
        sa.Column('related_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_credit_trans_user_id', 'credit_transactions', ['user_id'])
    op.create_index('ix_credit_trans_type', 'credit_transactions', ['type'])
    op.create_index('ix_credit_trans_created_at', 'credit_transactions', ['created_at'])
    op.create_index('ix_credit_trans_user_created', 'credit_transactions', ['user_id', 'created_at'])

    # redeem_codes 表
    op.create_table(
        'redeem_codes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('code', sa.String(12), nullable=False, unique=True),
        sa.Column('credits', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('is_used', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('used_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('remark', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_redeem_codes_code', 'redeem_codes', ['code'], unique=True)
    op.create_index('ix_redeem_codes_is_used', 'redeem_codes', ['is_used'])
    op.create_index('ix_redeem_codes_expires_at', 'redeem_codes', ['expires_at'])
    op.create_index('ix_redeem_codes_created_by', 'redeem_codes', ['created_by'])


def downgrade() -> None:
    op.drop_table('redeem_codes')
    op.drop_table('credit_transactions')
    op.drop_table('user_credits')
```

---

## 8. 前端集成

### 7.1 余额不足处理

在前端全局拦截 402 错误：

```typescript
// src/services/api.ts

import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 402) {
      const detail = error.response.data.detail;
      if (detail.code === 'INSUFFICIENT_CREDITS') {
        // 显示余额不足弹窗
        showInsufficientCreditsDialog({
          available: detail.available,
        });
      } else if (detail.code === 'CREDITS_EXPIRED') {
        // 显示积分过期提示
        showCreditsExpiredDialog({
          expiredAt: detail.expired_at,
        });
      }
    }
    return Promise.reject(error);
  }
);
```

### 7.2 Header 显示余额

在页面 Header 显示用户当前余额：

```typescript
// src/components/layout/Header.tsx

import { useBalance } from '@/hooks/queries/credits';

function Header() {
  const { data: balance } = useBalance();

  return (
    <header>
      {/* ... */}
      <div className="credits-display">
        💰 {balance?.balance.toFixed(2)} 积分
      </div>
      {/* ... */}
    </header>
  );
}
```

---

## 9. 测试要点

### 9.1 单元测试

**积分系统**:
- [ ] CreditService.consume() 正确扣减
- [ ] CreditService.check_sufficient() 正确检查
- [ ] RedeemCodeService.redeem() 正确兑换
- [ ] 并发扣减不会超扣
- [ ] 管理员豁免正确跳过扣费

**邀请系统**:
- [ ] InvitationService.generate_code() 生成唯一码
- [ ] InvitationService.validate_code() 正确验证
- [ ] InvitationService.activate_invitation() 正确激活
- [ ] 防刷机制正确限制

### 9.2 集成测试

**积分系统**:
- [ ] 新用户注册获得初始积分
- [ ] AI 调用正确扣减积分
- [ ] 管理员 AI 调用不扣积分
- [ ] 余额不足时拒绝 AI 调用
- [ ] 兑换码正确充值

**邀请系统**:
- [ ] 注册需要有效邀请码
- [ ] 被邀请人消费 200 积分后邀请人获得 1000 积分
- [ ] 被邀请人充值 1 积分后邀请人获得 1000 积分
- [ ] IP/设备限制正确阻止刷邀请
- [ ] 新用户冷却期正确限制生成

### 9.3 边界测试

**积分系统**:
- [ ] 余额刚好够用
- [ ] 余额恰好为 0
- [ ] 积分过期处理（配置为永不过期）
- [ ] 兑换码过期处理（90 天）
- [ ] 重复兑换同一码

**邀请系统**:
- [ ] 邀请码使用次数已满
- [ ] 邀请码已过期
- [ ] 7 天内未激活的邀请
- [ ] 同一 IP 24 小时内注册多次
- [ ] 同一设备 7 天内注册多次

---

## 10. 上线检查清单

### 10.1 后端检查

- [ ] 数据库迁移执行成功（积分表 + 邀请表）
- [ ] 配置项已添加到 .env（28 个配置项）
- [ ] API 路由已注册（积分 + 邀请）
- [ ] 模型已注册到 models/__init__.py
- [ ] 为现有用户初始化积分记录
- [ ] 管理员用户已标记 is_admin=True

### 10.2 前端检查

- [ ] 前端页面已部署（积分中心 + 邀请中心）
- [ ] 注册页面要求邀请码
- [ ] Header 显示积分余额
- [ ] 余额不足提示正常
- [ ] 路由配置正确

### 10.3 数据检查

- [ ] 为现有用户初始化积分（可选）
- [ ] 管理员批量生成邀请码用于推广
- [ ] 定时任务配置（过期邀请清理）

### 10.4 监控告警

- [ ] 积分消耗异常告警
- [ ] 邀请激活率监控
- [ ] IP/设备刷邀请检测告警
- [ ] 兑换码使用率监控

---

**文档版本**: v2.0
**创建时间**: 2025-12-02
**最后更新**: 2025-12-03
**更新内容**:
- 添加邀请系统集成方案
- 添加管理员豁免检查逻辑
- 添加邀请激活检测流程
- 更新注册流程（需邀请码）
- 添加邀请系统测试要点
- 更新上线检查清单
**作者**: Claude Code
