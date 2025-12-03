# 配置项文档

> ⚠️ **文档状态**: 设计文档，功能尚未实现

## 1. 配置概览

积分系统所有可配置参数均通过环境变量设置，在 `config.py` 中读取。

### 1.1 核心配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| CREDITS_PER_DOLLAR | CREDITS_PER_DOLLAR | 12400 | 1美元兑换积分数（基于混合使用） |
| NEW_USER_GIFT_CREDITS | NEW_USER_GIFT_CREDITS | 5000.00 | 新用户赠送积分（混合写5万字） |
| CREDITS_EXPIRE_DAYS | CREDITS_EXPIRE_DAYS | 0 | 积分有效期（天），0=永久 |
| REDEEM_CODE_EXPIRE_DAYS | REDEEM_CODE_EXPIRE_DAYS | 90 | 兑换码默认有效期（天） |
| CREDITS_ENABLED | CREDITS_ENABLED | True | 是否启用积分系统 |
| ADMIN_CREDITS_EXEMPT | ADMIN_CREDITS_EXEMPT | True | 管理员是否豁免积分检查 |

### 1.2 邀请系统配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| INVITATION_REWARD_CREDITS | INVITATION_REWARD_CREDITS | 1000.00 | 邀请奖励积分（混合写1万字） |
| INVITATION_MAX_USES_PER_CODE | INVITATION_MAX_USES_PER_CODE | 10 | 每个邀请码最多使用次数 |
| USER_MAX_INVITATION_CODES | USER_MAX_INVITATION_CODES | 3 | 每个用户最多持有邀请码数 |
| INVITATION_CODE_EXPIRE_DAYS | INVITATION_CODE_EXPIRE_DAYS | 365 | 邀请码有效期（天） |
| NEW_USER_INVITE_COOLDOWN_HOURS | NEW_USER_INVITE_COOLDOWN_HOURS | 72 | 新用户邀请冷却时间（小时） |

### 1.3 邀请激活配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| INVITATION_ACTIVATION_MIN_CONSUME | INVITATION_ACTIVATION_MIN_CONSUME | 200.00 | 激活所需最小消费积分（混合2次） |
| INVITATION_ACTIVATION_MIN_RECHARGE | INVITATION_ACTIVATION_MIN_RECHARGE | 0.01 | 激活所需最小充值积分 |
| INVITATION_ACTIVATION_DEADLINE_DAYS | INVITATION_ACTIVATION_DEADLINE_DAYS | 7 | 激活期限（天） |

### 1.4 防刷机制配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| SAME_IP_REGISTER_LIMIT_24H | SAME_IP_REGISTER_LIMIT_24H | 3 | 同IP 24小时注册上限 |
| SAME_DEVICE_REGISTER_LIMIT_7D | SAME_DEVICE_REGISTER_LIMIT_7D | 5 | 同设备7天注册上限 |

---

## 2. 配置详情

### 2.1 CREDITS_PER_DOLLAR

**美元兑积分比例**

```
CREDITS_PER_DOLLAR=12400
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 12400 |
| 范围 | 1000 - 50000 |
| 说明 | 1 美元可兑换的积分数量（基于混合使用模型） |

**换算示例**（默认值 12400）：

| AI 调用成本 (USD) | 消耗积分 |
|-------------------|----------|
| $0.001 | 12.4 |
| $0.01 | 124 |
| $0.10 | 1,240 |
| $1.00 | 12,400 |

**定价参考**（续写1000字场景）：

| 模型 | 单次成本 | 对应积分 | 10000积分能续写次数 |
|------|---------|---------|-------------------|
| gemini-2.5-pro | $0.01775 | 220 | 约 45次 |
| gemini-2.5-flash | $0.00435 | 54 | 约 185次 |
| gemini-2.5-flash-lite | $0.00145 | 18 | 约 556次 |
| **混合使用(60%F+30%P+10%L)** | **$0.00808** | **100** | **100次** |

**写不同字数成本**：

| 字数 | Flash | 混合使用 | Pro | Lite |
|------|-------|---------|-----|------|
| 1千字 | 54积分 | **100积分** | 220积分 | 18积分 |
| 1万字 | 540积分 | **1,000积分** | 2,200积分 | 180积分 |
| 5万字 | 2,700积分 | **5,000积分** | 11,000积分 | 900积分 |
| 10万字 | 5,400积分 | **10,000积分** | 22,000积分 | 1,800积分 |

---

### 2.2 NEW_USER_GIFT_CREDITS

**新用户赠送积分**

```
NEW_USER_GIFT_CREDITS=5000.00
```

| 属性 | 值 |
|------|-----|
| 类型 | Decimal |
| 默认值 | 5000.00 |
| 范围 | 0.00 - 100000.00 |
| 说明 | 新用户注册时自动赠送的积分数量（通过邀请码注册） |

**5000积分能做什么**：
- **混合使用：50,000字**（设计基准）
- Flash续写：约92,600字
- Pro续写：约22,700字
- Lite续写：约277,800字

**设置为 0 则不赠送**。

> ⚠️ 注意：本系统采用**封闭注册**，所有用户必须通过邀请码注册

---

### 2.3 INVITATION_REWARD_CREDITS

**邀请奖励积分**

```
INVITATION_REWARD_CREDITS=1000.00
```

| 属性 | 值 |
|------|-----|
| 类型 | Decimal |
| 默认值 | 1000.00 |
| 范围 | 0.00 - 100000.00 |
| 说明 | 成功邀请新用户后的奖励积分（需激活） |

**1000积分能做什么**：
- **混合使用：10,000字**
- Flash续写：约18,500字
- Pro续写：约4,500字

**双向奖励**：
- 新用户B注册：立即获得 5000积分
- 邀请者A：获得 1000积分（需被邀请人激活）

**激活条件**（二选一）：
- 被邀请人消费 ≥ 200积分（约混合使用2次）
- 被邀请人充值 ≥ 1积分

---

### 2.4 CREDITS_EXPIRE_DAYS

**积分有效期**

```
CREDITS_EXPIRE_DAYS=0
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 0 |
| 范围 | 0 - 3650（10年） |
| 说明 | 积分从充值/赠送之日起的有效天数 |

**设置为 0 则永久有效**（推荐）。

**过期时间计算逻辑**（如果设置非0）：
- 新用户赠送：`注册时间 + CREDITS_EXPIRE_DAYS`
- 兑换码充值：`max(当前过期时间, 充值时间 + CREDITS_EXPIRE_DAYS)`
- 邀请奖励：`获得时间 + CREDITS_EXPIRE_DAYS`

---

### 2.5 REDEEM_CODE_EXPIRE_DAYS

**兑换码默认有效期**

```
REDEEM_CODE_EXPIRE_DAYS=90
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 90 |
| 范围 | 1 - 365 |
| 说明 | 管理员生成兑换码时的默认有效期（3个月） |

**管理员可在生成时指定其他有效期**。

---

### 2.6 CREDITS_ENABLED

**积分系统开关**

```
CREDITS_ENABLED=true
```

| 属性 | 值 |
|------|-----|
| 类型 | bool |
| 默认值 | True |
| 说明 | 是否启用积分系统 |

**设置为 false 时**：
- 跳过余额检查
- 跳过积分扣减
- AI 功能不受限制（所有用户免费使用）

**用途**：
- 开发/测试环境关闭积分
- 紧急情况下临时关闭

---

### 2.7 ADMIN_CREDITS_EXEMPT

**管理员积分豁免**

```
ADMIN_CREDITS_EXEMPT=true
```

| 属性 | 值 |
|------|-----|
| 类型 | bool |
| 默认值 | True |
| 说明 | 管理员是否豁免积分检查 |

**设置为 true 时**：
- 管理员使用AI功能不检查余额
- 管理员使用AI功能不扣减积分
- 成本记录到 ai_call_logs 但不影响积分

**判断逻辑**：
```python
if settings.ADMIN_CREDITS_EXEMPT and user.is_admin:
    # 跳过积分检查和扣减
    pass
```

---

### 2.8 邀请系统配置

#### 2.8.1 INVITATION_MAX_USES_PER_CODE

**每个邀请码最多使用次数**

```
INVITATION_MAX_USES_PER_CODE=10
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 10 |
| 说明 | 单个邀请码最多可被使用的次数 |

#### 2.8.2 USER_MAX_INVITATION_CODES

**每个用户最多持有邀请码数**

```
USER_MAX_INVITATION_CODES=3
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 3 |
| 说明 | 每个用户最多可同时持有的有效邀请码数量 |

#### 2.8.3 INVITATION_CODE_EXPIRE_DAYS

**邀请码有效期**

```
INVITATION_CODE_EXPIRE_DAYS=365
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 365 |
| 说明 | 邀请码的有效期（天） |

#### 2.8.4 NEW_USER_INVITE_COOLDOWN_HOURS

**新用户邀请冷却时间**

```
NEW_USER_INVITE_COOLDOWN_HOURS=72
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 72 |
| 说明 | 新用户注册后多久才能生成邀请码（防刷） |

---

### 2.9 邀请激活配置

#### 2.9.1 INVITATION_ACTIVATION_MIN_CONSUME

**激活所需最小消费**

```
INVITATION_ACTIVATION_MIN_CONSUME=200.00
```

| 属性 | 值 |
|------|-----|
| 类型 | Decimal |
| 默认值 | 200.00 |
| 说明 | 被邀请人至少消费多少积分才算激活（混合使用约2次） |

#### 2.9.2 INVITATION_ACTIVATION_MIN_RECHARGE

**激活所需最小充值**

```
INVITATION_ACTIVATION_MIN_RECHARGE=1.00
```

| 属性 | 值 |
|------|-----|
| 类型 | Decimal |
| 默认值 | 1.00 |
| 说明 | 被邀请人至少充值多少积分才算激活（二选一） |

#### 2.9.3 INVITATION_ACTIVATION_DEADLINE_DAYS

**激活期限**

```
INVITATION_ACTIVATION_DEADLINE_DAYS=7
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 7 |
| 说明 | 被邀请人必须在多少天内完成激活 |

**激活逻辑**：
```
被邀请人注册后7天内，满足以下任一条件：
1. 消费 ≥ 200积分（混合使用约2次）
2. 充值 ≥ 1积分

激活后，邀请者获得1000积分奖励（混合写1万字）
```

---

### 2.10 防刷机制配置

#### 2.10.1 SAME_IP_REGISTER_LIMIT_24H

**同IP 24小时注册上限**

```
SAME_IP_REGISTER_LIMIT_24H=3
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 3 |
| 说明 | 同一IP地址24小时内最多注册账号数 |

#### 2.10.2 SAME_DEVICE_REGISTER_LIMIT_7D

**同设备7天注册上限**

```
SAME_DEVICE_REGISTER_LIMIT_7D=5
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 5 |
| 说明 | 同一设备指纹7天内最多注册账号数 |

---

## 3. config.py 实现

```python
# backend/app/core/config.py

from pydantic_settings import BaseSettings
from decimal import Decimal

class Settings(BaseSettings):
    # ... 其他配置 ...

    # ========== 积分系统核心配置 ==========

    # 积分系统开关
    CREDITS_ENABLED: bool = True

    # 管理员积分豁免
    ADMIN_CREDITS_EXEMPT: bool = True

    # 美元兑积分比例（基于混合使用模型：1 USD = 12,400 积分）
    CREDITS_PER_DOLLAR: int = 12400

    # 新用户赠送积分（混合写50,000字）
    NEW_USER_GIFT_CREDITS: Decimal = Decimal("5000.00")

    # 积分有效期（天），0 表示永久
    CREDITS_EXPIRE_DAYS: int = 0

    # 兑换码默认有效期（天）
    REDEEM_CODE_EXPIRE_DAYS: int = 90

    # ========== 邀请系统配置 ==========

    # 邀请奖励积分（混合写10,000字）
    INVITATION_REWARD_CREDITS: Decimal = Decimal("1000.00")

    # 邀请码限制
    INVITATION_MAX_USES_PER_CODE: int = 10
    USER_MAX_INVITATION_CODES: int = 3
    INVITATION_CODE_EXPIRE_DAYS: int = 365
    NEW_USER_INVITE_COOLDOWN_HOURS: int = 72

    # 邀请激活条件
    INVITATION_ACTIVATION_MIN_CONSUME: Decimal = Decimal("200.00")
    INVITATION_ACTIVATION_MIN_RECHARGE: Decimal = Decimal("1.00")
    INVITATION_ACTIVATION_DEADLINE_DAYS: int = 7

    # ========== 防刷机制配置 ==========

    # IP和设备限制
    SAME_IP_REGISTER_LIMIT_24H: int = 3
    SAME_DEVICE_REGISTER_LIMIT_7D: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

---

## 4. .env 示例

```bash
# ========== 积分系统核心配置 ==========

# 是否启用积分系统 (true/false)
CREDITS_ENABLED=true

# 管理员是否豁免积分检查 (true/false)
ADMIN_CREDITS_EXEMPT=true

# 美元兑积分比例（基于混合使用模型：1 USD = 12,400 积分）
CREDITS_PER_DOLLAR=12400

# 新用户赠送积分（混合写50,000字）
NEW_USER_GIFT_CREDITS=5000.00

# 积分有效期（天），0 表示永久有效
CREDITS_EXPIRE_DAYS=0

# 兑换码默认有效期（天）
REDEEM_CODE_EXPIRE_DAYS=90

# ========== 邀请系统配置 ==========

# 邀请奖励积分（混合写10,000字）
INVITATION_REWARD_CREDITS=1000.00

# 邀请码限制
INVITATION_MAX_USES_PER_CODE=10
USER_MAX_INVITATION_CODES=3
INVITATION_CODE_EXPIRE_DAYS=365
NEW_USER_INVITE_COOLDOWN_HOURS=72

# 邀请激活条件（混合使用约2次）
INVITATION_ACTIVATION_MIN_CONSUME=200.00
INVITATION_ACTIVATION_MIN_RECHARGE=1.00
INVITATION_ACTIVATION_DEADLINE_DAYS=7

# ========== 防刷机制配置 ==========

# 同IP 24小时注册上限
SAME_IP_REGISTER_LIMIT_24H=3

# 同设备7天注册上限
SAME_DEVICE_REGISTER_LIMIT_7D=5
```

---

## 5. 环境配置建议

### 5.1 开发环境

```bash
CREDITS_ENABLED=false                # 关闭积分，方便开发调试
ADMIN_CREDITS_EXEMPT=true            # 管理员豁免
CREDITS_PER_DOLLAR=12400             # 保持生产配置
NEW_USER_GIFT_CREDITS=100000.00      # 赠送大量积分便于测试
SAME_IP_REGISTER_LIMIT_24H=100       # 放宽限制便于测试
```

### 5.2 测试环境

```bash
CREDITS_ENABLED=true
ADMIN_CREDITS_EXEMPT=true
CREDITS_PER_DOLLAR=12400
NEW_USER_GIFT_CREDITS=10000.00       # 适量赠送
CREDITS_EXPIRE_DAYS=30               # 短有效期便于测试过期逻辑
INVITATION_ACTIVATION_MIN_CONSUME=100.00  # 降低激活门槛便于测试
```

### 5.3 生产环境

```bash
CREDITS_ENABLED=true
ADMIN_CREDITS_EXEMPT=true
CREDITS_PER_DOLLAR=12400
NEW_USER_GIFT_CREDITS=5000.00
CREDITS_EXPIRE_DAYS=0                # 永久有效
REDEEM_CODE_EXPIRE_DAYS=90           # 兑换码3个月有效
INVITATION_REWARD_CREDITS=1000.00
INVITATION_ACTIVATION_MIN_CONSUME=200.00
SAME_IP_REGISTER_LIMIT_24H=3         # 严格防刷
SAME_DEVICE_REGISTER_LIMIT_7D=5
```

---

## 6. 充值档位建议

基于 `CREDITS_PER_DOLLAR=12400`，人民币汇率约7：

| 档位名称 | 价格（元） | 基础积分 | 赠送积分 | 总积分 | 优惠幅度 | 混合能写 | Flash能写 |
|---------|----------|---------|---------|--------|---------|---------|----------|
| 体验包 | 1 | 1,771 | 89 | **1,860** | +5% | 1.86万字 | 3.4万字 |
| 入门包 | 10 | 17,714 | 2,126 | **19,840** | +12% | 19.8万字 | 36.7万字 |
| 进阶包 | 30 | 53,143 | 8,857 | **62,000** | +17% | 62万字 | 114.8万字 |
| 专业包 | 100 | 177,143 | 39,857 | **217,000** | +22% | 217万字 | 401.8万字 |

**计算公式**：
```
1元人民币 ≈ 1/7 美金 ≈ 1,771积分（基础）
混合1000字 = 100积分
Flash1000字 = 54积分
充值越多，赠送比例越高
```

---

## 7. 配置验证

```python
# backend/app/core/config.py

from pydantic import field_validator

class Settings(BaseSettings):
    # ...

    @field_validator("CREDITS_PER_DOLLAR")
    @classmethod
    def validate_credits_per_dollar(cls, v):
        if v < 1000 or v > 50000:
            raise ValueError("CREDITS_PER_DOLLAR 必须在 1000-50000 之间")
        return v

    @field_validator("NEW_USER_GIFT_CREDITS")
    @classmethod
    def validate_new_user_gift(cls, v):
        if v < 0 or v > 100000:
            raise ValueError("NEW_USER_GIFT_CREDITS 必须在 0-100000 之间")
        return v

    @field_validator("INVITATION_REWARD_CREDITS")
    @classmethod
    def validate_invitation_reward(cls, v):
        if v < 0 or v > 100000:
            raise ValueError("INVITATION_REWARD_CREDITS 必须在 0-100000 之间")
        return v

    @field_validator("CREDITS_EXPIRE_DAYS")
    @classmethod
    def validate_expire_days(cls, v):
        if v < 0 or v > 3650:
            raise ValueError("CREDITS_EXPIRE_DAYS 必须在 0-3650 之间")
        return v

    @field_validator("SAME_IP_REGISTER_LIMIT_24H")
    @classmethod
    def validate_ip_limit(cls, v):
        if v < 1 or v > 100:
            raise ValueError("SAME_IP_REGISTER_LIMIT_24H 必须在 1-100 之间")
        return v
```

---

## 8. 配置热更新

当前设计配置在启动时加载，**不支持热更新**。

如需修改配置：
1. 修改 `.env` 文件
2. 重启服务

**后续可考虑**：
- 将部分配置存入数据库（如赠送金额、充值档位）
- 通过管理后台实时调整
- 支持 A/B 测试不同配置

---

**文档版本**: v3.0
**创建时间**: 2025-12-02
**最后更新**: 2025-12-03
**作者**: Claude Code
**主要变更**：
- 换算比例调整为 1美金=12,400积分（基于混合使用模型）
- 新用户赠送调整为 5000积分（混合写5万字）
- 邀请奖励调整为 1000积分（混合写1万字）
- 封闭注册系统，必须通过邀请码注册
