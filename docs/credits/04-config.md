# 配置项文档

> ⚠️ **文档状态**: 设计文档，功能尚未实现

## 1. 配置概览

积分系统所有可配置参数均通过环境变量设置，在 `config.py` 中读取。

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| CREDITS_PER_DOLLAR | CREDITS_PER_DOLLAR | 100 | 1美元兑换积分数 |
| NEW_USER_GIFT_CREDITS | NEW_USER_GIFT_CREDITS | 10.00 | 新用户赠送积分 |
| CREDITS_EXPIRE_DAYS | CREDITS_EXPIRE_DAYS | 365 | 积分有效期（天） |
| REDEEM_CODE_EXPIRE_DAYS | REDEEM_CODE_EXPIRE_DAYS | 30 | 兑换码默认有效期（天） |
| CREDITS_ENABLED | CREDITS_ENABLED | True | 是否启用积分系统 |

---

## 2. 配置详情

### 2.1 CREDITS_PER_DOLLAR

**美元兑积分比例**

```
CREDITS_PER_DOLLAR=100
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 100 |
| 范围 | 1 - 10000 |
| 说明 | 1 美元可兑换的积分数量 |

**换算示例**（以默认值 100 为例）：

| AI 调用成本 (USD) | 消耗积分 |
|-------------------|----------|
| $0.01 | 1.00 |
| $0.10 | 10.00 |
| $1.00 | 100.00 |

**定价参考**：

| 模型 | 1000 tokens 成本 | 对应积分 |
|------|------------------|----------|
| gemini-2.5-flash-lite | ~$0.0001 | ~0.01 |
| gemini-2.5-flash | ~$0.0003 | ~0.03 |
| gemini-2.5-pro | ~$0.00125 | ~0.125 |

---

### 2.2 NEW_USER_GIFT_CREDITS

**新用户赠送积分**

```
NEW_USER_GIFT_CREDITS=10.00
```

| 属性 | 值 |
|------|-----|
| 类型 | Decimal |
| 默认值 | 10.00 |
| 范围 | 0.00 - 1000.00 |
| 说明 | 新用户注册时自动赠送的积分数量 |

**设置为 0 则不赠送**。

---

### 2.3 CREDITS_EXPIRE_DAYS

**积分有效期**

```
CREDITS_EXPIRE_DAYS=365
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 365 |
| 范围 | 0 - 3650（10年） |
| 说明 | 积分从充值/赠送之日起的有效天数 |

**设置为 0 则永久有效**。

**过期时间计算逻辑**：
- 新用户赠送：`注册时间 + CREDITS_EXPIRE_DAYS`
- 兑换码充值：`max(当前过期时间, 充值时间 + CREDITS_EXPIRE_DAYS)`

---

### 2.4 REDEEM_CODE_EXPIRE_DAYS

**兑换码默认有效期**

```
REDEEM_CODE_EXPIRE_DAYS=30
```

| 属性 | 值 |
|------|-----|
| 类型 | int |
| 默认值 | 30 |
| 范围 | 1 - 365 |
| 说明 | 管理员生成兑换码时的默认有效期 |

**管理员可在生成时指定其他有效期**。

---

### 2.5 CREDITS_ENABLED

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
- AI 功能不受限制

**用途**：
- 开发/测试环境关闭积分
- 紧急情况下临时关闭

---

## 3. config.py 实现

```python
# backend/app/core/config.py

from pydantic_settings import BaseSettings
from decimal import Decimal

class Settings(BaseSettings):
    # ... 其他配置 ...

    # ========== 积分系统配置 ==========

    # 积分系统开关
    CREDITS_ENABLED: bool = True

    # 美元兑积分比例 (1 USD = ? 积分)
    CREDITS_PER_DOLLAR: int = 100

    # 新用户赠送积分
    NEW_USER_GIFT_CREDITS: Decimal = Decimal("10.00")

    # 积分有效期（天），0 表示永久
    CREDITS_EXPIRE_DAYS: int = 365

    # 兑换码默认有效期（天）
    REDEEM_CODE_EXPIRE_DAYS: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

---

## 4. .env 示例

```bash
# ========== 积分系统配置 ==========

# 是否启用积分系统 (true/false)
CREDITS_ENABLED=true

# 美元兑积分比例 (1 USD = 100 积分)
CREDITS_PER_DOLLAR=100

# 新用户赠送积分
NEW_USER_GIFT_CREDITS=10.00

# 积分有效期（天），0 表示永久有效
CREDITS_EXPIRE_DAYS=365

# 兑换码默认有效期（天）
REDEEM_CODE_EXPIRE_DAYS=30
```

---

## 5. 环境配置建议

### 5.1 开发环境

```bash
CREDITS_ENABLED=false          # 关闭积分，方便开发调试
NEW_USER_GIFT_CREDITS=1000.00  # 赠送大量积分便于测试
```

### 5.2 测试环境

```bash
CREDITS_ENABLED=true
CREDITS_PER_DOLLAR=100
NEW_USER_GIFT_CREDITS=100.00   # 适量赠送
CREDITS_EXPIRE_DAYS=30         # 短有效期便于测试过期逻辑
```

### 5.3 生产环境

```bash
CREDITS_ENABLED=true
CREDITS_PER_DOLLAR=100         # 根据定价策略调整
NEW_USER_GIFT_CREDITS=10.00    # 根据运营策略调整
CREDITS_EXPIRE_DAYS=365        # 一年有效期
REDEEM_CODE_EXPIRE_DAYS=30     # 兑换码一个月有效
```

---

## 6. 配置热更新

当前设计配置在启动时加载，**不支持热更新**。

如需修改配置：
1. 修改 `.env` 文件
2. 重启服务

**后续可考虑**：
- 将部分配置存入数据库
- 通过管理后台实时调整
- 支持 A/B 测试不同配置

---

## 7. 配置验证

```python
# backend/app/core/config.py

from pydantic import validator

class Settings(BaseSettings):
    # ...

    @validator("CREDITS_PER_DOLLAR")
    def validate_credits_per_dollar(cls, v):
        if v < 1 or v > 10000:
            raise ValueError("CREDITS_PER_DOLLAR 必须在 1-10000 之间")
        return v

    @validator("NEW_USER_GIFT_CREDITS")
    def validate_new_user_gift(cls, v):
        if v < 0 or v > 1000:
            raise ValueError("NEW_USER_GIFT_CREDITS 必须在 0-1000 之间")
        return v

    @validator("CREDITS_EXPIRE_DAYS")
    def validate_expire_days(cls, v):
        if v < 0 or v > 3650:
            raise ValueError("CREDITS_EXPIRE_DAYS 必须在 0-3650 之间")
        return v
```

---

**文档版本**: v1.0
**创建时间**: 2025-12-02
**作者**: Claude Code
