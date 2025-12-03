# 系统集成方案

> ⚠️ **文档状态**: 设计文档，功能尚未实现

## 1. 集成概览

积分系统需要与以下现有模块集成：

| 模块 | 集成点 | 说明 |
|------|--------|------|
| 用户服务 | 新用户注册 | 赠送初始积分 |
| AI 服务 | AI 调用 | 检查余额、扣减积分 |
| 认证系统 | API 路由 | 权限验证 |

---

## 2. 用户注册集成

### 2.1 修改位置

**文件**: `backend/app/services/user_service.py`

**方法**: `create_user()` 或 `register()`

### 2.2 集成代码

```python
# backend/app/services/user_service.py

from app.services.credit_service import CreditService
from app.core.config import settings

class UserService:

    async def create_user(self, user_data: UserCreate) -> User:
        """创建新用户"""
        # 1. 原有逻辑：创建用户
        user = User(**user_data.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        # 2. 新增：赠送初始积分
        if settings.CREDITS_ENABLED and settings.NEW_USER_GIFT_CREDITS > 0:
            credit_service = CreditService(self.db)
            await credit_service.gift(
                user_id=user.id,
                amount=settings.NEW_USER_GIFT_CREDITS,
                description="新用户注册赠送",
                related_type="new_user"
            )

        return user
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

### 3.3 Agent 层集成代码

```python
# backend/app/services/agent/langgraph_agent.py

from app.services.credit_service import CreditService
from app.services.credit_exceptions import InsufficientCreditsError, CreditsExpiredError
from app.utils.credit_utils import calculate_credits_for_ai_call
from app.core.config import settings

class WritingAgentGraph:

    async def chat_stream(
        self,
        user_id: UUID,
        message: str,
        ...
    ):
        """流式对话"""

        # 1. 检查积分（如果启用）
        if settings.CREDITS_ENABLED:
            credit_service = CreditService(self.db)
            is_sufficient, balance = await credit_service.check_sufficient(
                user_id=user_id,
                required_credits=Decimal("0.01")  # 最小检查值
            )
            if not is_sufficient:
                raise InsufficientCreditsError(
                    required=Decimal("0.01"),
                    available=balance
                )

        # 2. 执行 AI 调用
        try:
            result = await self._execute_ai_call(...)

            # 3. 计算并扣减积分
            if settings.CREDITS_ENABLED:
                credits_consumed = calculate_credits_for_ai_call(
                    model_name=result.model_name,
                    prompt_tokens=result.prompt_tokens,
                    completion_tokens=result.completion_tokens
                )
                await credit_service.consume(
                    user_id=user_id,
                    amount=credits_consumed,
                    description=f"AI 调用: {result.model_name}",
                    related_id=result.log_id
                )

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

## 4. API 路由注册

### 4.1 注册积分路由

**文件**: `backend/app/api/__init__.py`

```python
from app.api.v1 import credits

api_router = APIRouter()

# ... 其他路由 ...

# 积分系统路由
api_router.include_router(
    credits.router,
    prefix="/credits",
    tags=["credits"]
)
```

### 4.2 注册管理端路由

```python
from app.api.v1 import admin_credits

# 管理端积分路由
api_router.include_router(
    admin_credits.router,
    prefix="/admin/credits",
    tags=["admin-credits"]
)
```

---

## 5. 模型注册

### 5.1 注册新模型

**文件**: `backend/app/models/__init__.py`

```python
from app.models.user_credits import UserCredits
from app.models.credit_transaction import CreditTransaction
from app.models.redeem_code import RedeemCode

__all__ = [
    # ... 其他模型 ...
    "UserCredits",
    "CreditTransaction",
    "RedeemCode",
]
```

---

## 6. 数据库迁移

### 6.1 生成迁移

```bash
cd backend
./venv/Scripts/alembic.exe revision --autogenerate -m "add_credits_tables"
```

### 6.2 执行迁移

```bash
./venv/Scripts/alembic.exe upgrade head
```

### 6.3 迁移文件示例

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

## 7. 前端集成

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

## 8. 测试要点

### 8.1 单元测试

- [ ] CreditService.consume() 正确扣减
- [ ] CreditService.check_sufficient() 正确检查
- [ ] RedeemCodeService.redeem() 正确兑换
- [ ] 并发扣减不会超扣

### 8.2 集成测试

- [ ] 新用户注册获得初始积分
- [ ] AI 调用正确扣减积分
- [ ] 余额不足时拒绝 AI 调用
- [ ] 兑换码正确充值

### 8.3 边界测试

- [ ] 余额刚好够用
- [ ] 余额恰好为 0
- [ ] 积分过期处理
- [ ] 兑换码过期处理
- [ ] 重复兑换同一码

---

## 9. 上线检查清单

- [ ] 数据库迁移执行成功
- [ ] 配置项已添加到 .env
- [ ] API 路由已注册
- [ ] 前端页面已部署
- [ ] 为现有用户初始化积分记录
- [ ] 监控告警配置

---

**文档版本**: v1.0
**创建时间**: 2025-12-02
**作者**: Claude Code
