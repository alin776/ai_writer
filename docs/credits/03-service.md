# 服务层设计

> ⚠️ **文档状态**: 设计文档，功能尚未实现

## 1. 服务概览

积分系统包含 3 个核心服务：

| 服务 | 文件 | 说明 |
|------|------|------|
| CreditService | credit_service.py | 积分管理核心服务 |
| RedeemCodeService | redeem_code_service.py | 兑换码服务 |
| InvitationService | invitation_service.py | 邀请系统服务 |

---

## 2. CreditService - 积分服务

### 2.1 类定义

```python
class CreditService:
    """积分服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
```

### 2.2 方法列表

| 方法 | 说明 |
|------|------|
| `get_or_create_credits()` | 获取或创建用户积分记录 |
| `get_balance()` | 查询用户余额 |
| `check_sufficient()` | 检查余额是否充足 |
| `consume()` | 消费积分 |
| `recharge()` | 充值积分 |
| `gift()` | 赠送积分 |
| `refund()` | 退还积分 |
| `get_transactions()` | 查询交易记录 |
| `get_stats()` | 获取统计数据（管理员） |

---

### 2.3 方法详情

#### 2.3.1 get_or_create_credits

获取用户积分记录，如果不存在则创建。

```python
async def get_or_create_credits(
    self,
    user_id: UUID,
    gift_credits: Optional[Decimal] = None
) -> UserCredits:
    """
    获取或创建用户积分记录

    Args:
        user_id: 用户ID
        gift_credits: 新用户赠送积分（可选，默认使用配置值）

    Returns:
        UserCredits: 用户积分记录
    """
```

**逻辑**:
1. 查询 user_credits 表
2. 如果存在，直接返回
3. 如果不存在：
   - 创建新记录
   - 设置初始余额为 `gift_credits` 或配置的 `NEW_USER_GIFT_CREDITS`
   - 创建 GIFT 类型的交易记录
   - 设置过期时间

---

#### 2.3.2 get_balance

查询用户当前余额。

```python
async def get_balance(self, user_id: UUID) -> BalanceInfo:
    """
    查询用户余额

    Args:
        user_id: 用户ID

    Returns:
        BalanceInfo: 余额信息
    """
```

**返回数据**:
```python
@dataclass
class BalanceInfo:
    balance: Decimal           # 当前余额
    total_recharged: Decimal   # 累计充值
    total_consumed: Decimal    # 累计消耗
    total_gifted: Decimal      # 累计赠送
    expires_at: Optional[datetime]  # 过期时间
    is_expired: bool           # 是否已过期
```

---

#### 2.3.3 check_sufficient

检查余额是否充足。

```python
async def check_sufficient(
    self,
    user_id: UUID,
    required_credits: Decimal
) -> Tuple[bool, Decimal]:
    """
    检查余额是否充足

    Args:
        user_id: 用户ID
        required_credits: 需要的积分数量

    Returns:
        Tuple[bool, Decimal]: (是否充足, 当前余额)
    """
```

**逻辑**:
1. 获取用户积分记录
2. 检查是否过期
3. 比较余额与所需积分
4. 返回 (is_sufficient, current_balance)

---

#### 2.3.4 consume

消费积分（AI 调用扣费）。

```python
async def consume(
    self,
    user_id: UUID,
    amount: Decimal,
    description: str,
    related_id: Optional[UUID] = None,
    skip_check: bool = False
) -> Optional[CreditTransaction]:
    """
    消费积分

    Args:
        user_id: 用户ID
        amount: 消费数量（正数）
        description: 描述（如 "AI 写作助手调用"）
        related_id: 关联的 ai_call_log ID
        skip_check: 跳过检查（管理员豁免）

    Returns:
        CreditTransaction: 交易记录（管理员豁免时返回 None）

    Raises:
        InsufficientCreditsError: 余额不足
        CreditsExpiredError: 积分已过期
    """
```

**逻辑**:
1. **检查管理员豁免** - 如果 `skip_check=True`，直接返回 None
2. 获取用户积分记录（加锁）
3. 检查是否过期
4. 检查余额是否充足
5. 扣减余额
6. 更新 total_consumed
7. 创建 CONSUME 类型交易记录
8. 提交事务

**管理员豁免**:
```python
# 调用层判断
from app.core.config import settings

if user.is_admin and settings.ADMIN_CREDITS_EXEMPT:
    # 跳过积分扣减，仅记录日志
    return await credit_service.consume(
        user_id=user.id,
        amount=credits,
        description=description,
        skip_check=True  # 管理员豁免
    )
```

**并发安全**:
```python
# 使用 SELECT FOR UPDATE 加行锁
stmt = select(UserCredits).where(
    UserCredits.user_id == user_id
).with_for_update()
```

---

#### 2.3.5 recharge

充值积分（兑换码兑换）。

```python
async def recharge(
    self,
    user_id: UUID,
    amount: Decimal,
    description: str,
    related_id: UUID
) -> CreditTransaction:
    """
    充值积分

    Args:
        user_id: 用户ID
        amount: 充值数量
        description: 描述
        related_id: 关联的 redeem_code ID

    Returns:
        CreditTransaction: 交易记录
    """
```

**逻辑**:
1. 获取或创建用户积分记录
2. 增加余额
3. 更新 total_recharged
4. 延长过期时间（如果配置了有效期）
5. 创建 RECHARGE 类型交易记录
6. 提交事务

---

#### 2.3.6 gift

赠送积分（管理员/新用户）。

```python
async def gift(
    self,
    user_id: UUID,
    amount: Decimal,
    description: str,
    related_type: str = "admin_gift"
) -> CreditTransaction:
    """
    赠送积分

    Args:
        user_id: 用户ID
        amount: 赠送数量
        description: 描述
        related_type: 关联类型 (admin_gift / new_user)

    Returns:
        CreditTransaction: 交易记录
    """
```

---

#### 2.3.7 refund

退还积分（AI 调用失败时）。

```python
async def refund(
    self,
    user_id: UUID,
    amount: Decimal,
    description: str,
    related_id: Optional[UUID] = None
) -> CreditTransaction:
    """
    退还积分

    Args:
        user_id: 用户ID
        amount: 退还数量
        description: 描述
        related_id: 关联的 ai_call_log ID

    Returns:
        CreditTransaction: 交易记录
    """
```

---

#### 2.3.8 get_transactions

查询交易记录。

```python
async def get_transactions(
    self,
    user_id: UUID,
    page: int = 1,
    page_size: int = 20,
    type: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> PaginatedResult[CreditTransaction]:
    """
    查询交易记录

    Args:
        user_id: 用户ID
        page: 页码
        page_size: 每页数量
        type: 筛选类型
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        PaginatedResult: 分页结果
    """
```

---

## 3. RedeemCodeService - 兑换码服务

### 3.1 类定义

```python
class RedeemCodeService:
    """兑换码服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.credit_service = CreditService(db)
```

### 3.2 方法列表

| 方法 | 说明 |
|------|------|
| `generate_codes()` | 批量生成兑换码 |
| `redeem()` | 兑换 |
| `get_code()` | 查询单个兑换码 |
| `list_codes()` | 查询兑换码列表 |
| `get_stats()` | 获取统计数据 |

---

### 3.3 方法详情

#### 3.3.1 generate_codes

批量生成兑换码。

```python
async def generate_codes(
    self,
    count: int,
    credits: Decimal,
    expires_days: Optional[int] = None,
    remark: Optional[str] = None,
    created_by: UUID = None
) -> List[RedeemCode]:
    """
    批量生成兑换码

    Args:
        count: 生成数量（1-100）
        credits: 每个兑换码的积分数量
        expires_days: 有效期天数（默认使用配置值）
        remark: 备注
        created_by: 创建者（管理员）ID

    Returns:
        List[RedeemCode]: 生成的兑换码列表
    """
```

**逻辑**:
1. 验证参数
2. 计算过期时间
3. 批量生成唯一兑换码
4. 批量插入数据库
5. 返回生成的兑换码

**兑换码生成**:
```python
VALID_CHARS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"

def generate_unique_code(existing_codes: Set[str]) -> str:
    """生成唯一兑换码"""
    while True:
        code = ''.join(secrets.choice(VALID_CHARS) for _ in range(12))
        if code not in existing_codes:
            return code
```

---

#### 3.3.2 redeem

兑换码兑换。

```python
async def redeem(
    self,
    code: str,
    user_id: UUID
) -> RedeemResult:
    """
    兑换码兑换

    Args:
        code: 兑换码
        user_id: 用户ID

    Returns:
        RedeemResult: 兑换结果

    Raises:
        RedeemCodeNotFoundError: 兑换码不存在
        RedeemCodeUsedError: 兑换码已使用
        RedeemCodeExpiredError: 兑换码已过期
    """
```

**逻辑**:
1. 查询兑换码（加锁）
2. 验证：
   - 是否存在
   - 是否已使用
   - 是否已过期
3. 调用 CreditService.recharge() 充值积分
4. 更新兑换码状态：
   - is_used = True
   - used_by = user_id
   - used_at = now()
5. 提交事务
6. 返回兑换结果

**返回数据**:
```python
@dataclass
class RedeemResult:
    credits: Decimal           # 充值积分
    balance_before: Decimal    # 充值前余额
    balance_after: Decimal     # 充值后余额
```

**并发安全**:
```python
# 使用 SELECT FOR UPDATE 防止重复兑换
stmt = select(RedeemCode).where(
    RedeemCode.code == code
).with_for_update()
```

---

#### 3.3.3 list_codes

查询兑换码列表（管理员）。

```python
async def list_codes(
    self,
    page: int = 1,
    page_size: int = 20,
    is_used: Optional[bool] = None,
    is_expired: Optional[bool] = None,
    created_by: Optional[UUID] = None
) -> PaginatedResult[RedeemCode]:
    """
    查询兑换码列表

    Args:
        page: 页码
        page_size: 每页数量
        is_used: 筛选已使用/未使用
        is_expired: 筛选已过期/未过期
        created_by: 筛选创建者

    Returns:
        PaginatedResult: 分页结果
    """
```

---

## 4. InvitationService - 邀请服务

### 4.1 类定义

```python
class InvitationService:
    """邀请服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.credit_service = CreditService(db)
```

### 4.2 方法列表

| 方法 | 说明 |
|------|------|
| `generate_invitation_code()` | 生成邀请码 |
| `validate_invitation_code()` | 验证邀请码 |
| `use_invitation_code()` | 使用邀请码（注册时） |
| `check_activation()` | 检查激活条件 |
| `activate_invitation()` | 激活邀请（奖励邀请人） |
| `get_my_invitations()` | 查询我的邀请码 |
| `get_invitation_stats()` | 查询邀请统计 |

---

### 4.3 方法详情

#### 4.3.1 generate_invitation_code

生成邀请码。

```python
async def generate_invitation_code(
    self,
    user_id: UUID,
    max_uses: int = 10,
    expires_days: Optional[int] = None
) -> UserInvitation:
    """
    生成邀请码

    Args:
        user_id: 用户ID
        max_uses: 最大使用次数（默认 10）
        expires_days: 有效期天数（可选）

    Returns:
        UserInvitation: 邀请码记录

    Raises:
        InvitationQuotaExceededError: 超过生成数量限制
        NewUserCooldownError: 新用户冷却期未过
    """
```

**逻辑**:
1. 查询用户已有邀请码数量
2. 验证：
   - 是否超过 3 个码限制
   - 是否在新用户冷却期（72 小时）
3. 生成唯一邀请码（8 位）
4. 计算过期时间
5. 创建 UserInvitation 记录
6. 返回邀请码

**示例**:
```python
invitation = await invitation_service.generate_invitation_code(
    user_id=user.id,
    max_uses=10,
    expires_days=365
)
# invitation.code = "AB3CDE5F"
```

---

#### 4.3.2 validate_invitation_code

验证邀请码是否有效。

```python
async def validate_invitation_code(
    self,
    code: str,
    ip_address: Optional[str] = None,
    device_fingerprint: Optional[str] = None
) -> Tuple[bool, str, Optional[UserInvitation]]:
    """
    验证邀请码

    Args:
        code: 邀请码
        ip_address: IP 地址
        device_fingerprint: 设备指纹

    Returns:
        Tuple[bool, str, Optional[UserInvitation]]:
            (是否有效, 错误信息, 邀请码记录)
    """
```

**验证逻辑**:
1. 查询邀请码是否存在
2. 检查是否过期
3. 检查使用次数是否已满
4. **防刷检查**：
   - IP 限制：同一 IP 24 小时内最多注册 3 次
   - 设备指纹限制：同一设备 7 天内最多注册 5 次
5. 返回验证结果

---

#### 4.3.3 use_invitation_code

使用邀请码（注册时调用）。

```python
async def use_invitation_code(
    self,
    code: str,
    invitee_id: UUID,
    ip_address: Optional[str] = None,
    device_fingerprint: Optional[str] = None
) -> InvitationUsage:
    """
    使用邀请码

    Args:
        code: 邀请码
        invitee_id: 被邀请人 ID
        ip_address: IP 地址
        device_fingerprint: 设备指纹

    Returns:
        InvitationUsage: 使用记录

    Raises:
        InvitationCodeInvalidError: 邀请码无效
        InvitationCodeExpiredError: 邀请码过期
        InvitationCodeFullError: 邀请码已满
        AntiAbuseLimitError: 触发防刷限制
    """
```

**逻辑**:
1. 验证邀请码（调用 validate_invitation_code）
2. 使用事务：
   - 增加 used_count
   - 创建 InvitationUsage 记录（status=pending）
3. 提交事务
4. 返回使用记录

---

#### 4.3.4 check_activation

检查激活条件是否满足。

```python
async def check_activation(
    self,
    invitee_id: UUID
) -> Tuple[bool, Decimal, Decimal]:
    """
    检查激活条件

    Args:
        invitee_id: 被邀请人 ID

    Returns:
        Tuple[bool, Decimal, Decimal]:
            (是否满足, 已消费积分, 已充值积分)
    """
```

**激活条件**:
- 消费 ≥ 200 积分 **或**
- 充值 ≥ 1 积分
- 必须在注册后 7 天内完成

**逻辑**:
1. 查询被邀请人的 InvitationUsage 记录
2. 检查是否超过 7 天
3. 查询累计消费积分（从 credit_transactions）
4. 查询累计充值积分（从 credit_transactions）
5. 判断是否满足激活条件
6. 返回结果

---

#### 4.3.5 activate_invitation

激活邀请（奖励邀请人）。

```python
async def activate_invitation(
    self,
    invitee_id: UUID
) -> Optional[CreditTransaction]:
    """
    激活邀请

    Args:
        invitee_id: 被邀请人 ID

    Returns:
        Optional[CreditTransaction]: 奖励交易记录（如果激活成功）
    """
```

**逻辑**:
1. 检查激活条件（调用 check_activation）
2. 如果不满足，返回 None
3. 查询 InvitationUsage 记录
4. 检查是否已激活（status=active）
5. 使用事务：
   - 更新 InvitationUsage.status = "active"
   - 更新 InvitationUsage.activated_at = now()
   - 增加 UserInvitation.activated_count
   - 增加 UserInvitation.total_rewards
   - 调用 CreditService.gift() 给邀请人 1000 积分
6. 提交事务
7. 返回奖励交易记录

**自动激活**:
```python
# 在 AI 调用扣费后自动检查
await invitation_service.activate_invitation(user.id)

# 在兑换充值后自动检查
await invitation_service.activate_invitation(user.id)
```

---

#### 4.3.6 get_my_invitations

查询我的邀请码列表。

```python
async def get_my_invitations(
    self,
    user_id: UUID
) -> List[UserInvitation]:
    """
    查询我的邀请码

    Args:
        user_id: 用户ID

    Returns:
        List[UserInvitation]: 邀请码列表（包含使用统计）
    """
```

---

## 5. 异常类

```python
# credit_exceptions.py

class CreditError(Exception):
    """积分异常基类"""
    pass

class InsufficientCreditsError(CreditError):
    """余额不足"""
    def __init__(self, required: Decimal, available: Decimal):
        self.required = required
        self.available = available
        super().__init__(f"余额不足：需要 {required}，当前 {available}")

class CreditsExpiredError(CreditError):
    """积分已过期"""
    def __init__(self, expired_at: datetime):
        self.expired_at = expired_at
        super().__init__(f"积分已于 {expired_at} 过期")

class RedeemCodeNotFoundError(CreditError):
    """兑换码不存在"""
    pass

class RedeemCodeUsedError(CreditError):
    """兑换码已使用"""
    def __init__(self, used_at: datetime, used_by: str):
        self.used_at = used_at
        self.used_by = used_by
        super().__init__(f"兑换码已于 {used_at} 被 {used_by} 使用")

class RedeemCodeExpiredError(CreditError):
    """兑换码已过期"""
    def __init__(self, expired_at: datetime):
        self.expired_at = expired_at
        super().__init__(f"兑换码已于 {expired_at} 过期")

# ============ 邀请系统异常 ============

class InvitationError(Exception):
    """邀请系统异常基类"""
    pass

class InvitationQuotaExceededError(InvitationError):
    """超过邀请码生成数量限制"""
    def __init__(self, max_count: int = 3):
        self.max_count = max_count
        super().__init__(f"每位用户最多生成 {max_count} 个邀请码")

class NewUserCooldownError(InvitationError):
    """新用户冷却期未过"""
    def __init__(self, remaining_hours: int):
        self.remaining_hours = remaining_hours
        super().__init__(f"新用户需等待 {remaining_hours} 小时后才能生成邀请码")

class InvitationCodeInvalidError(InvitationError):
    """邀请码无效"""
    pass

class InvitationCodeExpiredError(InvitationError):
    """邀请码已过期"""
    def __init__(self, expired_at: datetime):
        self.expired_at = expired_at
        super().__init__(f"邀请码已于 {expired_at} 过期")

class InvitationCodeFullError(InvitationError):
    """邀请码使用次数已满"""
    def __init__(self, max_uses: int):
        self.max_uses = max_uses
        super().__init__(f"邀请码已达到最大使用次数 {max_uses}")

class AntiAbuseLimitError(InvitationError):
    """触发防刷限制"""
    def __init__(self, limit_type: str, message: str):
        self.limit_type = limit_type  # "ip" or "device"
        super().__init__(message)
```

---

## 5. 辅助函数

### 5.1 积分计算

```python
# credit_utils.py

from app.utils.cost_calculator import CostCalculator
from app.core.config import settings

def calculate_credits_from_cost(cost_usd: float) -> Decimal:
    """
    将美元成本转换为积分

    Args:
        cost_usd: 美元成本

    Returns:
        Decimal: 积分数量（两位小数）
    """
    credits = Decimal(str(cost_usd)) * Decimal(str(settings.CREDITS_PER_DOLLAR))
    return credits.quantize(Decimal("0.01"))


def calculate_credits_for_ai_call(
    model_name: str,
    prompt_tokens: int,
    completion_tokens: int
) -> Decimal:
    """
    计算 AI 调用消耗的积分

    Args:
        model_name: 模型名称
        prompt_tokens: 输入 token 数
        completion_tokens: 输出 token 数

    Returns:
        Decimal: 消耗积分
    """
    cost_data = CostCalculator.calculate_cost(
        model_name=model_name,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens
    )
    return calculate_credits_from_cost(cost_data["total_cost"])
```

---

## 6. 服务调用示例

### 6.1 AI 调用扣费流程

```python
async def ai_call_with_credits(
    user_id: UUID,
    db: AsyncSession,
    ai_service: HTTPAIService
):
    credit_service = CreditService(db)

    # 1. 检查余额（预估消耗）
    estimated_credits = Decimal("1.00")  # 预估值
    is_sufficient, balance = await credit_service.check_sufficient(
        user_id, estimated_credits
    )
    if not is_sufficient:
        raise InsufficientCreditsError(estimated_credits, balance)

    # 2. 执行 AI 调用
    result = await ai_service.call(...)

    # 3. 计算实际消耗
    actual_credits = calculate_credits_for_ai_call(
        model_name=result.model,
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens
    )

    # 4. 扣减积分
    await credit_service.consume(
        user_id=user_id,
        amount=actual_credits,
        description=f"AI 调用: {result.model}",
        related_id=result.log_id
    )

    return result
```

### 6.2 兑换码兑换流程

```python
async def redeem_code(
    code: str,
    user_id: UUID,
    db: AsyncSession
):
    redeem_service = RedeemCodeService(db)

    result = await redeem_service.redeem(code, user_id)

    return {
        "credits": result.credits,
        "balance_before": result.balance_before,
        "balance_after": result.balance_after
    }
```

### 6.3 邀请激活流程

```python
async def register_with_invitation(
    invitation_code: str,
    user_data: dict,
    ip_address: str,
    device_fingerprint: str,
    db: AsyncSession
):
    """注册并使用邀请码"""
    invitation_service = InvitationService(db)
    credit_service = CreditService(db)

    # 1. 验证邀请码
    is_valid, error_msg, invitation = await invitation_service.validate_invitation_code(
        code=invitation_code,
        ip_address=ip_address,
        device_fingerprint=device_fingerprint
    )
    if not is_valid:
        raise InvitationCodeInvalidError(error_msg)

    # 2. 创建用户
    user = await user_service.create_user(**user_data)

    # 3. 赠送新用户积分
    await credit_service.get_or_create_credits(
        user_id=user.id,
        gift_credits=Decimal("5000.00")
    )

    # 4. 记录邀请使用
    await invitation_service.use_invitation_code(
        code=invitation_code,
        invitee_id=user.id,
        ip_address=ip_address,
        device_fingerprint=device_fingerprint
    )

    return user

async def on_ai_call_complete(user_id: UUID, db: AsyncSession):
    """AI 调用完成后检查激活"""
    invitation_service = InvitationService(db)

    # 自动检查并激活邀请
    await invitation_service.activate_invitation(user_id)
```

---

**文档版本**: v2.0
**创建时间**: 2025-12-02
**最后更新**: 2025-12-03
**更新内容**:
- 添加 InvitationService 设计
- 添加管理员豁免逻辑（skip_check 参数）
- 添加邀请系统异常类
- 添加邀请激活流程示例
**作者**: Claude Code
