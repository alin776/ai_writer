# 前端页面设计

> ⚠️ **文档状态**: 设计文档，功能尚未实现

## 1. 技术栈

项目前端使用：
- **React 19** + **TypeScript**
- **Zustand** - 状态管理（直接管理，无 React Query）
- **Axios** - HTTP 请求
- **Tailwind CSS** - 原子化样式（非 CSS Modules）
- **Radix UI** - 无头组件库
- **React Router v7** - 路由

---

## 2. 页面规划

### 2.1 用户端页面

| 页面 | 路由 | 说明 |
|------|------|------|
| 积分中心 | /credits | 余额、交易记录、兑换 |
| 邀请中心 | /invitations | 邀请码管理、邀请统计 |

### 2.2 管理端页面

| 页面 | 路由 | 说明 |
|------|------|------|
| 兑换码管理 | /admin/credits/codes | 生成、查看兑换码 |
| 积分统计 | /admin/credits/stats | 统计数据 |
| 邀请码管理 | /admin/invitations | 查看所有邀请码、批量生成 |

### 2.3 公开页面

| 页面 | 路由 | 说明 |
|------|------|------|
| 注册页面 | /register | 需要邀请码才能注册 |

---

## 3. 用户端 - 积分中心页面

### 3.1 页面结构

```
┌──────────────────────────────────────────────────────────┐
│  积分中心                                                 │
├──────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────┐  │
│  │  💰 当前余额                                        │  │
│  │                                                    │  │
│  │     99.50 积分                                     │  │
│  │                                                    │  │
│  │  有效期至：2025-12-31                              │  │
│  │                                                    │  │
│  │  [兑换积分]                                        │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  📊 积分统计                                        │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │  │
│  │  │累计充值   │  │累计消耗   │  │累计赠送   │         │  │
│  │  │ 200.00   │  │ 100.50   │  │  50.00   │         │  │
│  │  └──────────┘  └──────────┘  └──────────┘         │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  📜 交易记录                                        │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │ 类型筛选: [全部 ▼]    日期: [____] - [____]  │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │                                                    │  │
│  │  ┌──────┬────────┬──────────┬────────┬─────────┐  │  │
│  │  │ 类型 │  金额   │   描述    │  余额  │  时间   │  │  │
│  │  ├──────┼────────┼──────────┼────────┼─────────┤  │  │
│  │  │ 消费 │ -2.50  │ AI调用   │ 99.50  │ 12-02   │  │  │
│  │  │ 充值 │+100.00 │ 兑换码   │102.00  │ 12-02   │  │  │
│  │  │ 赠送 │ +50.00 │ 新用户   │  2.00  │ 12-01   │  │  │
│  │  └──────┴────────┴──────────┴────────┴─────────┘  │  │
│  │                                                    │  │
│  │  [上一页]  1 / 3  [下一页]                         │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 3.2 兑换弹窗

```
┌──────────────────────────────────────┐
│  🎁 兑换积分                    [×]  │
├──────────────────────────────────────┤
│                                      │
│  请输入兑换码：                       │
│  ┌────────────────────────────────┐  │
│  │  AB3CDE5FGH7K                  │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────┐  ┌────────────┐     │
│  │   取消     │  │   确认兑换  │     │
│  └────────────┘  └────────────┘     │
│                                      │
└──────────────────────────────────────┘
```

### 3.3 兑换成功提示

```
┌──────────────────────────────────────┐
│  ✅ 兑换成功                    [×]  │
├──────────────────────────────────────┤
│                                      │
│  恭喜！成功兑换 100.00 积分          │
│                                      │
│  当前余额：199.50 积分               │
│                                      │
│           ┌────────────┐            │
│           │    确定    │            │
│           └────────────┘            │
│                                      │
└──────────────────────────────────────┘
```

---

## 4. 用户端 - 邀请中心页面

### 4.1 页面结构

```
┌──────────────────────────────────────────────────────────┐
│  邀请中心                                                 │
├──────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────┐  │
│  │  🎁 邀请统计                                        │  │
│  │  ┌─────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │总邀请数  │  │激活人数   │  │获得奖励   │          │  │
│  │  │   3     │  │    2     │  │ 2000积分  │          │  │
│  │  └─────────┘  └──────────┘  └──────────┘          │  │
│  │                                                    │  │
│  │  剩余生成次数：0 / 3     [+ 生成新邀请码]           │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  📋 我的邀请码                                      │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │ 邀请码: AB3CDE5F    [复制]                    │  │  │
│  │  │ 使用次数: 3/10                                │  │  │
│  │  │ 激活人数: 2                                   │  │  │
│  │  │ 获得奖励: 2000积分                            │  │  │
│  │  │ 有效期至: 2026-12-03                          │  │  │
│  │  │                                              │  │  │
│  │  │ 已邀请用户：                                  │  │  │
│  │  │ ✅ user123 (已激活) - 2025-12-01            │  │  │
│  │  │ ⏳ user456 (待激活) - 2025-12-03            │  │  │
│  │  │ ✅ user789 (已激活) - 2025-11-30            │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 4.2 生成邀请码弹窗

```
┌──────────────────────────────────────┐
│  🎫 生成邀请码                  [×]  │
├──────────────────────────────────────┤
│                                      │
│  最大使用次数：                       │
│  ┌──────────────────────┐           │
│  │  10                  │           │
│  └──────────────────────┘           │
│                                      │
│  有效期（天）：                       │
│  ┌──────────────────────┐           │
│  │  365  (留空永不过期)  │           │
│  └──────────────────────┘           │
│                                      │
│  说明：                              │
│  • 每位用户最多生成 3 个邀请码         │
│  • 被邀请人消费 200 积分或充值 1 积分  │
│    后激活，你将获得 1000 积分奖励      │
│                                      │
│  ┌────────────┐  ┌────────────┐     │
│  │   取消     │  │   生成     │     │
│  └────────────┘  └────────────┘     │
│                                      │
└──────────────────────────────────────┘
```

### 4.3 注册页面（含邀请码验证）

```
┌──────────────────────────────────────┐
│  注册账号                            │
├──────────────────────────────────────┤
│                                      │
│  邀请码：                            │
│  ┌──────────────────────┐           │
│  │  AB3CDE5F            │  [验证]   │
│  └──────────────────────┘           │
│  ✅ 邀请码有效                        │
│                                      │
│  用户名：                            │
│  ┌──────────────────────┐           │
│  │  newuser             │           │
│  └──────────────────────┘           │
│                                      │
│  邮箱：                              │
│  ┌──────────────────────┐           │
│  │  user@example.com    │           │
│  └──────────────────────┘           │
│                                      │
│  密码：                              │
│  ┌──────────────────────┐           │
│  │  ••••••••            │           │
│  └──────────────────────┘           │
│                                      │
│  ┌────────────────────┐             │
│  │      注册          │             │
│  └────────────────────┘             │
│                                      │
│  注册成功即可获得 5000 积分！         │
│                                      │
└──────────────────────────────────────┘
```

---

## 5. 管理端 - 兑换码管理页面

### 4.1 页面结构

```
┌──────────────────────────────────────────────────────────┐
│  兑换码管理                              [+ 生成兑换码]   │
├──────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────┐  │
│  │ 筛选: 状态 [全部 ▼]  创建者 [全部 ▼]              │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 统计: 总数 50 | 已用 25 | 未用 20 | 过期 5         │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 兑换码        │ 积分  │ 状态   │ 使用者  │ 创建时间 │  │
│  ├───────────────┼───────┼────────┼─────────┼──────────┤  │
│  │ AB3CDE5FGH7K │ 100   │ ✅已用  │ user1  │ 12-01    │  │
│  │ MN9PQR2STUV4 │ 100   │ ⏳未用  │  -     │ 12-01    │  │
│  │ WX4YZ6ABCD8E │ 50    │ ❌过期  │  -     │ 11-01    │  │
│  └───────────────┴───────┴────────┴─────────┴──────────┘  │
│                                                          │
│  [上一页]  1 / 3  [下一页]                               │
└──────────────────────────────────────────────────────────┘
```

### 4.2 生成兑换码弹窗

```
┌──────────────────────────────────────┐
│  🎫 生成兑换码                  [×]  │
├──────────────────────────────────────┤
│                                      │
│  生成数量：                          │
│  ┌──────────────────────┐           │
│  │  10                  │           │
│  └──────────────────────┘           │
│                                      │
│  每张积分：                          │
│  ┌──────────────────────┐           │
│  │  100.00              │           │
│  └──────────────────────┘           │
│                                      │
│  有效期（天）：                       │
│  ┌──────────────────────┐           │
│  │  30                  │           │
│  └──────────────────────┘           │
│                                      │
│  备注：                              │
│  ┌──────────────────────┐           │
│  │  12月促销活动         │           │
│  └──────────────────────┘           │
│                                      │
│  ┌────────────┐  ┌────────────┐     │
│  │   取消     │  │   生成     │     │
│  └────────────┘  └────────────┘     │
│                                      │
└──────────────────────────────────────┘
```

### 4.3 生成成功 - 展示兑换码

```
┌──────────────────────────────────────┐
│  ✅ 生成成功                    [×]  │
├──────────────────────────────────────┤
│                                      │
│  成功生成 10 张兑换码，共 1000 积分   │
│                                      │
│  ┌────────────────────────────────┐  │
│  │ AB3CDE5FGH7K                   │  │
│  │ MN9PQR2STUV4                   │  │
│  │ WX4YZ6ABCD8E                   │  │
│  │ ...                            │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────┐  ┌────────────┐     │
│  │  复制全部   │  │   关闭     │     │
│  └────────────┘  └────────────┘     │
│                                      │
└──────────────────────────────────────┘
```

---

## 6. 文件结构

> 📁 项目前端代码在根目录 `src/` 下，不是 `frontend/src/`

```
src/
├── views/                          # 页面视图（扁平结构）
│   ├── CreditsView.tsx             # 用户积分中心页面
│   ├── InvitationsView.tsx         # 用户邀请中心页面
│   ├── RegisterView.tsx            # 注册页面（含邀请码验证）
│   ├── AdminCreditsView.tsx        # 管理端兑换码管理页面
│   └── AdminInvitationsView.tsx    # 管理端邀请码管理页面
│
├── components/
│   ├── credits/                    # 积分相关组件
│   │   ├── BalanceCard.tsx         # 余额卡片
│   │   ├── StatsCard.tsx           # 统计卡片
│   │   ├── TransactionList.tsx     # 交易记录列表
│   │   ├── RedeemDialog.tsx        # 兑换弹窗
│   │   ├── CodeList.tsx            # 兑换码列表（管理端）
│   │   └── GenerateDialog.tsx      # 生成兑换码弹窗
│   │
│   ├── invitations/                # 邀请相关组件
│   │   ├── InvitationStatsCard.tsx # 邀请统计卡片
│   │   ├── InvitationCodeCard.tsx  # 邀请码卡片
│   │   ├── GenerateInvitationDialog.tsx  # 生成邀请码弹窗
│   │   └── InviteeList.tsx         # 被邀请人列表
│   │
│   └── common/                     # 通用组件（已有）
│       ├── Button.tsx
│       ├── Modal.tsx
│       └── ...
│
├── services/
│   ├── ApiAdapter.ts               # API 适配器（已有，新增方法）
│   └── DataService.ts              # 数据服务（已有，新增方法）
│
├── store/
│   ├── creditsStore.ts             # 积分状态管理（Zustand）
│   └── invitationsStore.ts         # 邀请状态管理（Zustand）
│
└── types/
    ├── credits.ts                  # 积分相关类型定义
    └── invitations.ts              # 邀请相关类型定义
```

> ⚠️ **注意**: 本项目**不使用 React Query**，使用 Zustand + Axios 直接管理状态和请求。

---

## 7. 类型定义

### 7.1 积分类型（credits.ts）

```typescript
// src/types/credits.ts

// 余额信息
export interface BalanceInfo {
  balance: number;
  total_recharged: number;
  total_consumed: number;
  total_gifted: number;
  expires_at: string | null;
  is_expired: boolean;
}

// 交易记录
export interface CreditTransaction {
  id: string;
  type: 'recharge' | 'consume' | 'gift' | 'expire' | 'refund';
  amount: number;
  balance_before: number;
  balance_after: number;
  description: string | null;
  related_type: string | null;
  related_id: string | null;
  created_at: string;
}

// 兑换码
export interface RedeemCode {
  id: string;
  code: string;
  credits: number;
  is_used: boolean;
  used_by: UserBrief | null;
  used_at: string | null;
  expires_at: string | null;
  is_expired: boolean;
  created_by: UserBrief | null;
  remark: string | null;
  created_at: string;
}

// 用户简要信息
export interface UserBrief {
  id: string;
  username: string;
}

// 兑换请求
export interface RedeemRequest {
  code: string;
}

// 兑换响应
export interface RedeemResponse {
  credits: number;
  balance_before: number;
  balance_after: number;
}

// 生成兑换码请求
export interface GenerateCodesRequest {
  count: number;
  credits: number;
  expires_days?: number;
  remark?: string;
}

// 分页响应
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
```

### 7.2 邀请类型（invitations.ts）

```typescript
// src/types/invitations.ts

// 邀请码
export interface InvitationCode {
  id: string;
  code: string;
  max_uses: number;
  used_count: number;
  activated_count: number;
  total_rewards: number;
  expires_at: string | null;
  created_at: string;
}

// 邀请统计
export interface InvitationStats {
  total_invitations: number;
  total_used: number;
  total_activated: number;
  total_rewards: number;
  can_generate_more: boolean;
  remaining_quota: number;
}

// 被邀请人
export interface Invitee {
  username: string;
  status: 'pending' | 'active' | 'expired';
  registered_at: string;
  activated_at: string | null;
}

// 邀请码详情（含被邀请人列表）
export interface InvitationCodeDetail extends InvitationCode {
  invitees: Invitee[];
}

// 生成邀请码请求
export interface GenerateInvitationRequest {
  max_uses?: number;
  expires_days?: number;
}

// 验证邀请码响应
export interface ValidateInvitationResponse {
  valid: boolean;
  message: string;
}

// 注册请求
export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  invitation_code: string;
}
```

---

## 8. Zustand Store

> ⚠️ 本项目使用 Zustand 管理状态，不使用 React Query

### 7.1 creditsStore.ts

```typescript
// src/store/creditsStore.ts

import { create } from 'zustand';
import { ApiAdapter } from '../services/ApiAdapter';
import type { BalanceInfo, CreditTransaction, PaginatedResponse } from '../types/credits';

interface CreditsState {
  // 状态
  balance: BalanceInfo | null;
  transactions: CreditTransaction[];
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchBalance: () => Promise<void>;
  fetchTransactions: (params?: TransactionParams) => Promise<void>;
  redeem: (code: string) => Promise<RedeemResponse>;
  clearError: () => void;
}

interface TransactionParams {
  page?: number;
  pageSize?: number;
  type?: string;
}

const api = new ApiAdapter();

export const useCreditsStore = create<CreditsState>((set, get) => ({
  balance: null,
  transactions: [],
  isLoading: false,
  error: null,

  fetchBalance: async () => {
    set({ isLoading: true, error: null });
    try {
      const data = await api.get('/credits/balance');
      set({ balance: data, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchTransactions: async (params = {}) => {
    set({ isLoading: true, error: null });
    try {
      const data = await api.get('/credits/transactions', { params });
      set({ transactions: data.items, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  redeem: async (code: string) => {
    set({ isLoading: true, error: null });
    try {
      const result = await api.post('/credits/redeem', { code });
      // 刷新余额
      await get().fetchBalance();
      set({ isLoading: false });
      return result;
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));
```

### 8.2 invitationsStore.ts

```typescript
// src/store/invitationsStore.ts

import { create } from 'zustand';
import { ApiAdapter } from '../services/ApiAdapter';
import type {
  InvitationCode,
  InvitationCodeDetail,
  InvitationStats,
  GenerateInvitationRequest,
  ValidateInvitationResponse
} from '../types/invitations';

interface InvitationsState {
  // 状态
  stats: InvitationStats | null;
  myCodes: InvitationCodeDetail[];
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchStats: () => Promise<void>;
  fetchMyCodes: () => Promise<void>;
  generateCode: (params: GenerateInvitationRequest) => Promise<InvitationCode>;
  validateCode: (code: string) => Promise<ValidateInvitationResponse>;
  clearError: () => void;
}

const api = new ApiAdapter();

export const useInvitationsStore = create<InvitationsState>((set) => ({
  stats: null,
  myCodes: [],
  isLoading: false,
  error: null,

  fetchStats: async () => {
    set({ isLoading: true, error: null });
    try {
      const data = await api.get('/invitations/stats');
      set({ stats: data, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchMyCodes: async () => {
    set({ isLoading: true, error: null });
    try {
      const data = await api.get('/invitations/my-codes');
      set({ myCodes: data.items, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  generateCode: async (params: GenerateInvitationRequest) => {
    set({ isLoading: true, error: null });
    try {
      const result = await api.post('/invitations/generate', params);
      // 刷新列表和统计
      await get().fetchMyCodes();
      await get().fetchStats();
      set({ isLoading: false });
      return result;
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  validateCode: async (code: string) => {
    try {
      return await api.post('/invitations/validate', { code });
    } catch (error: any) {
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));
```

### 8.3 使用示例

```typescript
// 在积分组件中使用
import { useCreditsStore } from '../store/creditsStore';

function CreditsView() {
  const { balance, transactions, isLoading, fetchBalance, fetchTransactions } = useCreditsStore();

  useEffect(() => {
    fetchBalance();
    fetchTransactions();
  }, []);

  if (isLoading) return <Loading />;

  return (
    <div>
      <BalanceCard balance={balance} />
      <TransactionList transactions={transactions} />
    </div>
  );
}

// 在邀请组件中使用
import { useInvitationsStore } from '../store/invitationsStore';

function InvitationsView() {
  const { stats, myCodes, isLoading, fetchStats, fetchMyCodes } = useInvitationsStore();

  useEffect(() => {
    fetchStats();
    fetchMyCodes();
  }, []);

  if (isLoading) return <Loading />;

  return (
    <div>
      <InvitationStatsCard stats={stats} />
      {myCodes.map(code => (
        <InvitationCodeCard key={code.id} code={code} />
      ))}
    </div>
  );
}
```

---

## 9. API 服务封装

在现有 `ApiAdapter.ts` 中扩展积分相关方法：

```typescript
// src/services/ApiAdapter.ts (扩展部分)

export class ApiAdapter implements IDataAdapter {
  // ... 现有代码 ...

  // === 积分相关 API ===

  // 查询余额
  async getCreditsBalance(): Promise<BalanceInfo> {
    return this.axiosInstance.get('/credits/balance');
  }

  // 查询交易记录
  async getCreditsTransactions(params: {
    page?: number;
    pageSize?: number;
    type?: string;
    startDate?: string;
    endDate?: string;
  }): Promise<PaginatedResponse<CreditTransaction>> {
    return this.axiosInstance.get('/credits/transactions', { params });
  }

  // 兑换码兑换
  async redeemCredits(code: string): Promise<RedeemResponse> {
    return this.axiosInstance.post('/credits/redeem', { code });
  }

  // === 管理端 API ===

  // 生成兑换码
  async generateRedeemCodes(data: GenerateCodesRequest): Promise<{ codes: RedeemCode[] }> {
    return this.axiosInstance.post('/admin/credits/codes/generate', data);
  }

  // 查询兑换码列表
  async getRedeemCodes(params: {
    page?: number;
    pageSize?: number;
    isUsed?: boolean;
    isExpired?: boolean;
  }): Promise<PaginatedResponse<RedeemCode>> {
    return this.axiosInstance.get('/admin/credits/codes', { params });
  }

  // === 邀请相关 API ===

  // 查询邀请统计
  async getInvitationStats(): Promise<InvitationStats> {
    return this.axiosInstance.get('/invitations/stats');
  }

  // 查询我的邀请码
  async getMyInvitations(): Promise<{ items: InvitationCodeDetail[] }> {
    return this.axiosInstance.get('/invitations/my-codes');
  }

  // 生成邀请码
  async generateInvitation(params: GenerateInvitationRequest): Promise<InvitationCode> {
    return this.axiosInstance.post('/invitations/generate', params);
  }

  // 验证邀请码
  async validateInvitation(code: string): Promise<ValidateInvitationResponse> {
    return this.axiosInstance.post('/invitations/validate', { code });
  }

  // 注册（含邀请码）
  async registerWithInvitation(data: RegisterRequest): Promise<any> {
    return this.axiosInstance.post('/auth/register', data);
  }

  // === 管理端邀请 API ===

  // 批量生成邀请码
  async batchGenerateInvitations(data: {
    count: number;
    max_uses?: number;
    expires_days?: number;
    remark?: string;
  }): Promise<{ codes: InvitationCode[] }> {
    return this.axiosInstance.post('/admin/invitations/batch-generate', data);
  }

  // 查询所有邀请码
  async getAllInvitations(params: {
    page?: number;
    pageSize?: number;
    status?: string;
    userId?: string;
  }): Promise<PaginatedResponse<InvitationCode>> {
    return this.axiosInstance.get('/admin/invitations/list', { params });
  }
}
```

> 💡 **注意**: 本项目使用 `ApiAdapter` 类封装 Axios，响应数据会自动从 snake_case 转换为 camelCase。

---

## 10. 路由配置

在 `src/router/index.ts` 中添加路由：

```typescript
// src/router/index.ts (React Router v7)

import { createBrowserRouter } from 'react-router-dom';
import CreditsView from '../views/CreditsView';
import InvitationsView from '../views/InvitationsView';
import RegisterView from '../views/RegisterView';
import AdminCreditsView from '../views/AdminCreditsView';
import AdminInvitationsView from '../views/AdminInvitationsView';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      // ... 现有路由 ...

      // 公开路由
      {
        path: 'register',
        element: <RegisterView />,  // 需要邀请码才能注册
      },

      // 用户端路由
      {
        path: 'credits',
        element: <CreditsView />,
      },
      {
        path: 'invitations',
        element: <InvitationsView />,
      },

      // 管理端路由
      {
        path: 'admin',
        element: <AdminLayout />,
        children: [
          // ... 现有管理路由 ...
          {
            path: 'credits/codes',
            element: <AdminCreditsView />,
          },
          {
            path: 'invitations',
            element: <AdminInvitationsView />,
          },
        ],
      },
    ],
  },
]);
```

---

## 11. 余额不足提示

当 AI 调用因余额不足被拒绝时，显示提示：

```
┌──────────────────────────────────────┐
│  ⚠️ 余额不足                    [×]  │
├──────────────────────────────────────┤
│                                      │
│  当前积分余额不足，无法使用 AI 功能    │
│                                      │
│  当前余额：0.50 积分                  │
│                                      │
│  ┌────────────┐  ┌────────────┐     │
│  │   关闭     │  │  去充值    │     │
│  └────────────┘  └────────────┘     │
│                                      │
└──────────────────────────────────────┘
```

---

## 12. 新用户冷却期提示

当新用户尝试生成邀请码但在冷却期内时，显示提示：

```
┌──────────────────────────────────────┐
│  ⚠️ 暂时无法生成                [×]  │
├──────────────────────────────────────┤
│                                      │
│  新用户需等待 48 小时后才能生成邀请码 │
│                                      │
│  您的账号创建于：2025-12-03 10:00    │
│  可生成时间：2025-12-05 10:00        │
│                                      │
│  ┌────────────────────┐             │
│  │      知道了         │             │
│  └────────────────────┘             │
│                                      │
└──────────────────────────────────────┘
```

---

**文档版本**: v2.0
**创建时间**: 2025-12-02
**最后更新**: 2025-12-03
**更新内容**:
- 添加邀请中心页面设计
- 添加注册页面（需邀请码）
- 添加管理员邀请码管理页面
- 添加邀请相关类型定义
- 添加 invitationsStore
- 添加邀请相关 API 封装
- 更新路由配置
**作者**: Claude Code
