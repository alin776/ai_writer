# API 接口文档

> ⚠️ **文档状态**: 设计文档，功能尚未实现

## 1. 接口概览

### 1.1 用户端接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/credits/balance | 查询积分余额 |
| GET | /api/v1/credits/transactions | 查询交易记录 |
| POST | /api/v1/credits/redeem | 兑换码兑换 |
| POST | /api/v1/invitations/generate | 生成邀请码 |
| GET | /api/v1/invitations/my-codes | 查询我的邀请码 |
| GET | /api/v1/invitations/stats | 查询邀请统计 |

### 1.2 管理端接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/admin/credits/codes/generate | 生成兑换码 |
| GET | /api/v1/admin/credits/codes | 查询兑换码列表 |
| POST | /api/v1/admin/credits/gift | 手动赠送积分 |
| GET | /api/v1/admin/credits/stats | 积分统计 |
| POST | /api/v1/admin/invitations/batch-generate | 批量生成邀请码 |
| GET | /api/v1/admin/invitations/list | 查询所有邀请码 |

### 1.3 公开接口（无需认证）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/auth/register | 注册（需邀请码） |
| POST | /api/v1/invitations/validate | 验证邀请码 |

---

## 2. 用户端接口详情

### 2.1 查询积分余额

**GET** `/api/v1/credits/balance`

#### 请求头
```
Authorization: Bearer <access_token>
```

#### 响应

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "balance": 99.50,
        "total_recharged": 200.00,
        "total_consumed": 100.50,
        "total_gifted": 50.00,
        "expires_at": "2025-12-31T23:59:59Z",
        "is_expired": false
    }
}
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| balance | number | 当前可用余额 |
| total_recharged | number | 累计充值 |
| total_consumed | number | 累计消耗 |
| total_gifted | number | 累计赠送获得 |
| expires_at | string | 过期时间（ISO 8601） |
| is_expired | boolean | 是否已过期 |

---

### 2.2 查询交易记录

**GET** `/api/v1/credits/transactions`

#### 请求头
```
Authorization: Bearer <access_token>
```

#### 请求参数（Query）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| page_size | int | 否 | 20 | 每页数量（最大 100） |
| type | string | 否 | - | 筛选类型：recharge/consume/gift/expire/refund |
| start_date | string | 否 | - | 开始日期（YYYY-MM-DD） |
| end_date | string | 否 | - | 结束日期（YYYY-MM-DD） |

#### 响应

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "items": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "type": "consume",
                "amount": -2.50,
                "balance_before": 102.00,
                "balance_after": 99.50,
                "description": "AI 写作助手调用",
                "related_type": "ai_call",
                "related_id": "550e8400-e29b-41d4-a716-446655440002",
                "created_at": "2025-12-02T10:30:00Z"
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440003",
                "type": "recharge",
                "amount": 100.00,
                "balance_before": 2.00,
                "balance_after": 102.00,
                "description": "兑换码充值",
                "related_type": "redeem_code",
                "related_id": "550e8400-e29b-41d4-a716-446655440004",
                "created_at": "2025-12-02T09:00:00Z"
            }
        ],
        "total": 25,
        "page": 1,
        "page_size": 20,
        "total_pages": 2
    }
}
```

---

### 2.3 兑换码兑换

**POST** `/api/v1/credits/redeem`

#### 请求头
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### 请求体

```json
{
    "code": "AB3CDE5FGH7K"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 兑换码（12位） |

#### 响应 - 成功

```json
{
    "code": 200,
    "message": "兑换成功",
    "data": {
        "credits": 100.00,
        "balance_before": 99.50,
        "balance_after": 199.50
    }
}
```

#### 响应 - 失败

```json
{
    "code": 400,
    "message": "兑换码无效或已使用",
    "data": null
}
```

#### 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 兑换码格式错误 |
| 404 | 兑换码不存在 |
| 409 | 兑换码已被使用 |
| 410 | 兑换码已过期 |

---

### 2.4 生成邀请码

**POST** `/api/v1/invitations/generate`

#### 请求头
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### 请求体

```json
{
    "max_uses": 10,
    "expires_days": 365
}
```

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| max_uses | int | 否 | 10 | 最大使用次数 |
| expires_days | int | 否 | NULL | 有效期天数 |

#### 响应 - 成功

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "code": "AB3CDE5F",
    "max_uses": 10,
    "used_count": 0,
    "activated_count": 0,
    "total_rewards": 0.00,
    "expires_at": "2026-12-03T23:59:59Z",
    "created_at": "2025-12-03T10:00:00Z"
}
```

#### 响应 - 失败

```json
{
    "detail": "每位用户最多生成 3 个邀请码"
}
```

或

```json
{
    "detail": "新用户需等待 48 小时后才能生成邀请码"
}
```

---

### 2.5 查询我的邀请码

**GET** `/api/v1/invitations/my-codes`

#### 请求头
```
Authorization: Bearer <access_token>
```

#### 响应

> 注意: 直接返回数组，不是 `{ items: [], total: x }` 格式

```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "code": "AB3CDE5F",
        "max_uses": 10,
        "used_count": 3,
        "activated_count": 2,
        "total_rewards": 2000.00,
        "expires_at": "2026-12-03T23:59:59Z",
        "created_at": "2025-12-03T10:00:00Z",
        "invitees": [
            {
                "username": "user123",
                "status": "active",
                "registered_at": "2025-12-01T10:00:00Z",
                "activated_at": "2025-12-02T15:30:00Z"
            },
            {
                "username": "user456",
                "status": "pending",
                "registered_at": "2025-12-03T08:00:00Z",
                "activated_at": null
            }
        ]
    }
]
```

---

### 2.6 查询邀请统计

**GET** `/api/v1/invitations/stats`

#### 请求头
```
Authorization: Bearer <access_token>
```

#### 响应

```json
{
    "total_invitations": 2,
    "total_used": 5,
    "total_activated": 3,
    "total_rewards": 3000.00,
    "can_generate_more": true,
    "remaining_quota": 1
}
```

---

## 3. 公开接口详情

### 3.1 验证邀请码

**POST** `/api/v1/invitations/validate`

#### 请求头
```
Content-Type: application/json
```

#### 请求体

```json
{
    "code": "AB3CDE5F"
}
```

#### 响应 - 有效

```json
{
    "valid": true,
    "message": "邀请码有效"
}
```

#### 响应 - 无效

```json
{
    "valid": false,
    "message": "邀请码不存在"
}
```

或

```json
{
    "valid": false,
    "message": "邀请码已过期"
}
```

或

```json
{
    "valid": false,
    "message": "邀请码使用次数已满"
}
```

---

### 3.2 注册（需邀请码）

**POST** `/api/v1/auth/register`

#### 请求头
```
Content-Type: application/json
```

#### 请求体

```json
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword",
    "invitation_code": "AB3CDE5F"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| email | string | 是 | 邮箱 |
| password | string | 是 | 密码 |
| invitation_code | string | 是 | 邀请码（8位） |

#### 响应 - 成功

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440099",
    "username": "newuser",
    "email": "newuser@example.com",
    "credits": {
        "balance": 5000.00,
        "gift_from_registration": 5000.00
    },
    "access_token": "eyJhbGci...",
    "token_type": "bearer"
}
```

#### 响应 - 失败

```json
{
    "detail": "邀请码无效或已过期"
}
```

或

```json
{
    "detail": "该IP地址24小时内注册次数过多，请稍后再试"
}
```

---

## 4. 管理端接口详情

### 3.1 生成兑换码

**POST** `/api/v1/admin/credits/codes/generate`

#### 请求头
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

#### 请求体

```json
{
    "count": 10,
    "credits": 100.00,
    "expires_days": 30,
    "remark": "12月促销活动"
}
```

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| count | int | 是 | - | 生成数量（1-100） |
| credits | number | 是 | - | 每个兑换码的积分数量 |
| expires_days | int | 否 | 配置默认值 | 有效期天数 |
| remark | string | 否 | - | 备注 |

#### 响应

```json
{
    "code": 200,
    "message": "生成成功",
    "data": {
        "codes": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "code": "AB3CDE5FGH7K",
                "credits": 100.00,
                "expires_at": "2026-01-01T23:59:59Z"
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "code": "MN9PQR2STUV4",
                "credits": 100.00,
                "expires_at": "2026-01-01T23:59:59Z"
            }
        ],
        "total_generated": 10,
        "total_credits": 1000.00
    }
}
```

---

### 3.2 查询兑换码列表

**GET** `/api/v1/admin/credits/codes`

#### 请求头
```
Authorization: Bearer <admin_access_token>
```

#### 请求参数（Query）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| page_size | int | 否 | 20 | 每页数量 |
| is_used | boolean | 否 | - | 筛选：已使用/未使用 |
| is_expired | boolean | 否 | - | 筛选：已过期/未过期 |
| created_by | uuid | 否 | - | 筛选：创建者 |

#### 响应

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "items": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "code": "AB3CDE5FGH7K",
                "credits": 100.00,
                "is_used": true,
                "used_by": {
                    "id": "user-uuid",
                    "username": "testuser"
                },
                "used_at": "2025-12-02T10:00:00Z",
                "expires_at": "2026-01-01T23:59:59Z",
                "is_expired": false,
                "created_by": {
                    "id": "admin-uuid",
                    "username": "admin"
                },
                "remark": "12月促销活动",
                "created_at": "2025-12-01T12:00:00Z"
            }
        ],
        "total": 50,
        "page": 1,
        "page_size": 20,
        "total_pages": 3,
        "stats": {
            "total_codes": 50,
            "used_codes": 25,
            "unused_codes": 25,
            "expired_codes": 5
        }
    }
}
```

---

### 3.3 手动赠送积分

**POST** `/api/v1/admin/credits/gift`

#### 请求头
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

#### 请求体

```json
{
    "user_id": "550e8400-e29b-41d4-a716-446655440001",
    "credits": 50.00,
    "reason": "用户反馈奖励"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | uuid | 是 | 用户ID |
| credits | number | 是 | 赠送积分数量 |
| reason | string | 否 | 赠送原因 |

#### 响应

```json
{
    "code": 200,
    "message": "赠送成功",
    "data": {
        "user_id": "550e8400-e29b-41d4-a716-446655440001",
        "username": "testuser",
        "credits_gifted": 50.00,
        "balance_before": 99.50,
        "balance_after": 149.50
    }
}
```

---

### 3.4 积分统计

**GET** `/api/v1/admin/credits/stats`

#### 请求头
```
Authorization: Bearer <admin_access_token>
```

#### 请求参数（Query）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| start_date | string | 否 | 30天前 | 开始日期 |
| end_date | string | 否 | 今天 | 结束日期 |

#### 响应

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "overview": {
            "total_users_with_credits": 150,
            "total_balance": 15000.00,
            "total_recharged": 50000.00,
            "total_consumed": 35000.00,
            "total_gifted": 5000.00
        },
        "period": {
            "start_date": "2025-11-02",
            "end_date": "2025-12-02",
            "recharge_count": 200,
            "recharge_amount": 10000.00,
            "consume_count": 5000,
            "consume_amount": 8000.00,
            "gift_count": 50,
            "gift_amount": 500.00
        },
        "daily_trend": [
            {
                "date": "2025-12-01",
                "recharge": 500.00,
                "consume": 300.00
            },
            {
                "date": "2025-12-02",
                "recharge": 600.00,
                "consume": 350.00
            }
        ]
    }
}
```

---

### 4.5 批量生成邀请码（管理员）

**POST** `/api/v1/admin/invitations/batch-generate`

#### 请求头
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

#### 请求体

```json
{
    "count": 10,
    "max_uses": 10,
    "expires_days": 365,
    "remark": "市场推广活动"
}
```

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| count | int | 是 | - | 生成数量（1-100） |
| max_uses | int | 否 | 10 | 每个码最大使用次数 |
| expires_days | int | 否 | NULL | 有效期天数 |
| remark | string | 否 | - | 备注 |

#### 响应

```json
{
    "codes": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "code": "AB3CDE5F",
            "max_uses": 10,
            "expires_at": "2026-12-03T23:59:59Z"
        },
        {
            "id": "550e8400-e29b-41d4-a716-446655440002",
            "code": "MN9PQR2S",
            "max_uses": 10,
            "expires_at": "2026-12-03T23:59:59Z"
        }
    ],
    "total_generated": 10,
    "remark": "市场推广活动"
}
```

---

### 4.6 查询所有邀请码（管理员）

**GET** `/api/v1/admin/invitations/list`

#### 请求头
```
Authorization: Bearer <admin_access_token>
```

#### 请求参数（Query）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| page_size | int | 否 | 20 | 每页数量 |
| status | string | 否 | - | 筛选：active/expired/full |
| user_id | uuid | 否 | - | 筛选：创建者 |

#### 响应

```json
{
    "items": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "code": "AB3CDE5F",
            "user": {
                "id": "user-uuid",
                "username": "testuser"
            },
            "max_uses": 10,
            "used_count": 5,
            "activated_count": 3,
            "total_rewards": 3000.00,
            "expires_at": "2026-12-03T23:59:59Z",
            "created_at": "2025-12-03T10:00:00Z"
        }
    ],
    "total": 50,
    "page": 1,
    "page_size": 20,
    "total_pages": 3,
    "stats": {
        "total_codes": 50,
        "active_codes": 35,
        "expired_codes": 10,
        "full_codes": 5
    }
}
```

---

## 5. 通用响应格式

> ⚠️ **注意**: 本项目 API **直接返回数据**，不使用 `code/message/data` 包装。

### 5.1 成功响应

直接返回数据对象或列表：

```json
// 单个对象
{
    "balance": 99.50,
    "total_recharged": 200.00,
    ...
}

// 分页列表
{
    "total": 25,
    "items": [...]
}
```

### 5.2 错误响应

使用 FastAPI 的 HTTPException：

```json
{
    "detail": "错误描述"
}

// 或结构化错误
{
    "detail": {
        "code": "INSUFFICIENT_CREDITS",
        "message": "积分余额不足",
        "required": 10.0,
        "available": 5.0
    }
}
```

### 5.3 HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（Token 无效） |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 409 | 冲突（如兑换码已使用） |
| 410 | 资源已过期 |
| 500 | 服务器错误 |

---

## 6. Pydantic Schemas

### 6.1 请求 Schemas

```python
# 兑换请求
class RedeemRequest(BaseModel):
    code: str = Field(..., min_length=12, max_length=12, pattern="^[A-Z0-9]+$")

# 生成兑换码请求
class GenerateCodesRequest(BaseModel):
    count: int = Field(..., ge=1, le=100)
    credits: Decimal = Field(..., gt=0)
    expires_days: Optional[int] = Field(None, ge=1, le=365)
    remark: Optional[str] = Field(None, max_length=255)

# 赠送积分请求
class GiftCreditsRequest(BaseModel):
    user_id: UUID
    credits: Decimal = Field(..., gt=0)
    reason: Optional[str] = Field(None, max_length=255)
```

### 6.2 响应 Schemas

```python
# 余额响应
class BalanceResponse(BaseModel):
    balance: Decimal
    total_recharged: Decimal
    total_consumed: Decimal
    total_gifted: Decimal
    expires_at: Optional[datetime]
    is_expired: bool

# 交易记录响应
class TransactionResponse(BaseModel):
    id: UUID
    type: str
    amount: Decimal
    balance_before: Decimal
    balance_after: Decimal
    description: Optional[str]
    related_type: Optional[str]
    related_id: Optional[UUID]
    created_at: datetime

# 兑换码响应
class RedeemCodeResponse(BaseModel):
    id: UUID
    code: str
    credits: Decimal
    is_used: bool
    used_by: Optional[UserBrief]
    used_at: Optional[datetime]
    expires_at: Optional[datetime]
    is_expired: bool
    created_by: Optional[UserBrief]
    remark: Optional[str]
    created_at: datetime

# 邀请码响应
class InvitationCodeResponse(BaseModel):
    id: UUID
    code: str
    max_uses: int
    used_count: int
    activated_count: int
    total_rewards: Decimal
    expires_at: Optional[datetime]
    created_at: datetime

# 邀请统计响应
class InvitationStatsResponse(BaseModel):
    total_invitations: int
    total_used: int
    total_activated: int
    total_rewards: Decimal
    can_generate_more: bool
    remaining_quota: int

# 注册请求（含邀请码）
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    invitation_code: str = Field(..., min_length=8, max_length=8, pattern="^[A-Z0-9]+$")
```

---

**文档版本**: v2.0
**创建时间**: 2025-12-02
**最后更新**: 2025-12-03
**更新内容**:
- 添加邀请系统接口（生成、查询、验证）
- 添加管理员批量生成邀请码接口
- 更新注册接口要求邀请码
- 添加邀请相关 Schemas
**作者**: Claude Code
