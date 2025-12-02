# 数据模型设计

## 1. 模型概览

积分系统包含 3 个核心数据模型：

| 模型 | 表名 | 说明 |
|------|------|------|
| UserCredits | user_credits | 用户积分主表 |
| CreditTransaction | credit_transactions | 积分变动记录 |
| RedeemCode | redeem_codes | 兑换码 |

## 2. UserCredits - 用户积分表

### 2.1 表结构

```sql
CREATE TABLE user_credits (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,

    -- 积分信息
    balance         DECIMAL(10,2) NOT NULL DEFAULT 0.00,      -- 当前余额
    total_recharged DECIMAL(10,2) NOT NULL DEFAULT 0.00,      -- 累计充值
    total_consumed  DECIMAL(10,2) NOT NULL DEFAULT 0.00,      -- 累计消耗
    total_gifted    DECIMAL(10,2) NOT NULL DEFAULT 0.00,      -- 累计赠送获得

    -- 有效期
    expires_at      TIMESTAMP WITH TIME ZONE,                  -- 积分过期时间

    -- 时间戳
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE UNIQUE INDEX ix_user_credits_user_id ON user_credits(user_id);
CREATE INDEX ix_user_credits_expires_at ON user_credits(expires_at);
```

### 2.2 字段说明

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | UUID | 是 | 自动生成 | 主键 |
| user_id | UUID | 是 | - | 关联用户，唯一 |
| balance | DECIMAL(10,2) | 是 | 0.00 | 当前可用余额 |
| total_recharged | DECIMAL(10,2) | 是 | 0.00 | 累计充值积分 |
| total_consumed | DECIMAL(10,2) | 是 | 0.00 | 累计消耗积分 |
| total_gifted | DECIMAL(10,2) | 是 | 0.00 | 累计赠送获得 |
| expires_at | TIMESTAMP | 否 | NULL | 积分过期时间 |
| created_at | TIMESTAMP | 是 | NOW() | 创建时间 |
| updated_at | TIMESTAMP | 是 | NOW() | 更新时间 |

### 2.3 SQLAlchemy 模型

```python
class UserCredits(Base):
    """用户积分"""

    __tablename__ = "user_credits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    # 积分信息
    balance = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))
    total_recharged = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))
    total_consumed = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))
    total_gifted = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))

    # 有效期
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联
    user = relationship("User", backref="credits")
    transactions = relationship("CreditTransaction", back_populates="user_credits")
```

---

## 3. CreditTransaction - 积分变动记录

### 3.1 表结构

```sql
CREATE TABLE credit_transactions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- 交易信息
    type            VARCHAR(20) NOT NULL,                      -- 类型: recharge/consume/gift/expire/refund
    amount          DECIMAL(10,2) NOT NULL,                    -- 变动数量 (正数增加，负数减少)
    balance_before  DECIMAL(10,2) NOT NULL,                    -- 变动前余额
    balance_after   DECIMAL(10,2) NOT NULL,                    -- 变动后余额

    -- 描述信息
    description     VARCHAR(255),                              -- 描述

    -- 关联信息
    related_type    VARCHAR(50),                               -- 关联类型: ai_call/redeem_code/admin_gift
    related_id      UUID,                                      -- 关联ID

    -- 时间戳
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX ix_credit_trans_user_id ON credit_transactions(user_id);
CREATE INDEX ix_credit_trans_type ON credit_transactions(type);
CREATE INDEX ix_credit_trans_created_at ON credit_transactions(created_at);
CREATE INDEX ix_credit_trans_user_created ON credit_transactions(user_id, created_at);
```

### 3.2 字段说明

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | UUID | 是 | 自动生成 | 主键 |
| user_id | UUID | 是 | - | 关联用户 |
| type | VARCHAR(20) | 是 | - | 交易类型 |
| amount | DECIMAL(10,2) | 是 | - | 变动数量（正/负） |
| balance_before | DECIMAL(10,2) | 是 | - | 变动前余额 |
| balance_after | DECIMAL(10,2) | 是 | - | 变动后余额 |
| description | VARCHAR(255) | 否 | NULL | 描述 |
| related_type | VARCHAR(50) | 否 | NULL | 关联类型 |
| related_id | UUID | 否 | NULL | 关联ID |
| created_at | TIMESTAMP | 是 | NOW() | 创建时间 |

### 3.3 交易类型枚举

```python
class TransactionType(str, Enum):
    """交易类型"""
    RECHARGE = "recharge"   # 充值（兑换码兑换）
    CONSUME = "consume"     # 消费（AI调用）
    GIFT = "gift"           # 赠送（新用户/管理员赠送）
    EXPIRE = "expire"       # 过期扣除
    REFUND = "refund"       # 退还（调用失败退还）
```

### 3.4 关联类型枚举

```python
class RelatedType(str, Enum):
    """关联类型"""
    AI_CALL = "ai_call"           # 关联 ai_call_logs.id
    REDEEM_CODE = "redeem_code"   # 关联 redeem_codes.id
    ADMIN_GIFT = "admin_gift"     # 管理员赠送（无关联ID）
    NEW_USER = "new_user"         # 新用户赠送（无关联ID）
```

### 3.5 SQLAlchemy 模型

```python
class CreditTransaction(Base):
    """积分变动记录"""

    __tablename__ = "credit_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 交易信息
    type = Column(String(20), nullable=False, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    balance_before = Column(DECIMAL(10, 2), nullable=False)
    balance_after = Column(DECIMAL(10, 2), nullable=False)

    # 描述
    description = Column(String(255), nullable=True)

    # 关联
    related_type = Column(String(50), nullable=True)
    related_id = Column(UUID(as_uuid=True), nullable=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # 关联关系
    user = relationship("User", backref="credit_transactions")

    __table_args__ = (
        Index('ix_credit_trans_user_created', 'user_id', 'created_at'),
    )
```

---

## 4. RedeemCode - 兑换码

### 4.1 表结构

```sql
CREATE TABLE redeem_codes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 兑换码信息
    code            VARCHAR(12) NOT NULL UNIQUE,               -- 兑换码（12位）
    credits         DECIMAL(10,2) NOT NULL,                    -- 积分数量

    -- 状态
    is_used         BOOLEAN NOT NULL DEFAULT FALSE,            -- 是否已使用
    used_by         UUID REFERENCES users(id) ON DELETE SET NULL,  -- 使用者
    used_at         TIMESTAMP WITH TIME ZONE,                  -- 使用时间

    -- 有效期
    expires_at      TIMESTAMP WITH TIME ZONE,                  -- 过期时间

    -- 创建信息
    created_by      UUID REFERENCES users(id) ON DELETE SET NULL,  -- 创建者（管理员）
    remark          VARCHAR(255),                              -- 备注

    -- 时间戳
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE UNIQUE INDEX ix_redeem_codes_code ON redeem_codes(code);
CREATE INDEX ix_redeem_codes_is_used ON redeem_codes(is_used);
CREATE INDEX ix_redeem_codes_expires_at ON redeem_codes(expires_at);
CREATE INDEX ix_redeem_codes_created_by ON redeem_codes(created_by);
```

### 4.2 字段说明

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | UUID | 是 | 自动生成 | 主键 |
| code | VARCHAR(12) | 是 | - | 兑换码，唯一 |
| credits | DECIMAL(10,2) | 是 | - | 积分数量 |
| is_used | BOOLEAN | 是 | FALSE | 是否已使用 |
| used_by | UUID | 否 | NULL | 使用者ID |
| used_at | TIMESTAMP | 否 | NULL | 使用时间 |
| expires_at | TIMESTAMP | 否 | NULL | 过期时间 |
| created_by | UUID | 否 | NULL | 创建者（管理员） |
| remark | VARCHAR(255) | 否 | NULL | 备注 |
| created_at | TIMESTAMP | 是 | NOW() | 创建时间 |

### 4.3 SQLAlchemy 模型

```python
class RedeemCode(Base):
    """兑换码"""

    __tablename__ = "redeem_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 兑换码信息
    code = Column(String(12), nullable=False, unique=True, index=True)
    credits = Column(DECIMAL(10, 2), nullable=False)

    # 状态
    is_used = Column(Boolean, nullable=False, default=False, index=True)
    used_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    used_at = Column(DateTime(timezone=True), nullable=True)

    # 有效期
    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # 创建信息
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    remark = Column(String(255), nullable=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联关系
    user = relationship("User", foreign_keys=[used_by], backref="used_redeem_codes")
    creator = relationship("User", foreign_keys=[created_by], backref="created_redeem_codes")
```

---

## 5. 兑换码生成规则

### 5.1 格式规范
- 长度：12 位
- 字符集：大写字母 A-Z + 数字 0-9（排除易混淆字符 O, 0, I, 1, L）
- 有效字符：`ABCDEFGHJKMNPQRSTUVWXYZ23456789`（共 32 个字符）

### 5.2 生成算法

```python
import secrets
import string

VALID_CHARS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"  # 排除 O,0,I,1,L

def generate_redeem_code(length: int = 12) -> str:
    """生成兑换码"""
    return ''.join(secrets.choice(VALID_CHARS) for _ in range(length))
```

### 5.3 示例兑换码
```
AB3CDE5FGH7K
MN9PQR2STUV
WX4YZ6ABCD8E
```

---

## 6. ER 图

```
┌─────────────────┐       ┌──────────────────────┐
│      users      │       │     user_credits     │
├─────────────────┤       ├──────────────────────┤
│ id (PK)         │──1:1──│ user_id (FK, UNIQUE) │
│ username        │       │ balance              │
│ ...             │       │ total_recharged      │
└─────────────────┘       │ total_consumed       │
        │                 │ expires_at           │
        │                 └──────────────────────┘
        │
        │ 1:N
        ▼
┌──────────────────────┐
│  credit_transactions │
├──────────────────────┤
│ id (PK)              │
│ user_id (FK)         │
│ type                 │
│ amount               │
│ balance_before       │
│ balance_after        │
│ related_type         │
│ related_id           │──────▶ ai_call_logs.id / redeem_codes.id
└──────────────────────┘

┌─────────────────┐       ┌──────────────────────┐
│      users      │       │     redeem_codes     │
├─────────────────┤       ├──────────────────────┤
│ id (PK)         │──1:N──│ created_by (FK)      │
│ (admin)         │       │ code (UNIQUE)        │
└─────────────────┘       │ credits              │
        │                 │ is_used              │
        │ 1:N             │ used_by (FK)         │
        └─────────────────│ expires_at           │
                          └──────────────────────┘
```

---

## 7. 迁移文件

文件名：`backend/alembic/versions/20251202_xxxx_add_credits_tables.py`

详见开发实现阶段。

---

**文档版本**: v1.0
**创建时间**: 2025-12-02
**作者**: Claude Code
