# 服务层设计

## 1. 服务概览

积分系统包含 2 个核心服务：

| 服务 | 文件 | 说明 |
|------|------|------|
| CreditService | credit_service.py | 积分管理核心服务 |
| RedeemCodeService | redeem_code_service.py | 兑换码服务 |

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
    related_id: Optional[UUID] = None
) -> CreditTransaction:
    """
    消费积分

    Args:
        user_id: 用户ID
        amount: 消费数量（正数）
        description: 描述（如 "AI 写作助手调用"）
        related_id: 关联的 ai_call_log ID

    Returns:
        CreditTransaction: 交易记录

    Raises:
        InsufficientCreditsError: 余额不足
        CreditsExpiredError: 积分已过期
    """
```

**逻辑**:
1. 获取用户积分记录（加锁）
2. 检查是否过期
3. 检查余额是否充足
4. 扣减余额
5. 更新 total_consumed
6. 创建 CONSUME 类型交易记录
7. 提交事务

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

## 4. 异常类

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

---

**文档版本**: v1.0
**创建时间**: 2025-12-02
**作者**: Claude Code
