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

### 2.2 管理端页面

| 页面 | 路由 | 说明 |
|------|------|------|
| 兑换码管理 | /admin/credits/codes | 生成、查看兑换码 |
| 积分统计 | /admin/credits/stats | 统计数据 |

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

## 4. 管理端 - 兑换码管理页面

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

## 5. 文件结构

> 📁 项目前端代码在根目录 `src/` 下，不是 `frontend/src/`

```
src/
├── views/                          # 页面视图（扁平结构）
│   ├── CreditsView.tsx             # 用户积分中心页面
│   └── AdminCreditsView.tsx        # 管理端兑换码管理页面
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
│   └── common/                     # 通用组件（已有）
│       ├── Button.tsx
│       ├── Modal.tsx
│       └── ...
│
├── services/
│   ├── ApiAdapter.ts               # API 适配器（已有，新增积分方法）
│   └── DataService.ts              # 数据服务（已有，新增积分方法）
│
├── store/
│   └── creditsStore.ts             # 积分状态管理（Zustand）
│
└── types/
    └── credits.ts                  # 积分相关类型定义
```

> ⚠️ **注意**: 本项目**不使用 React Query**，使用 Zustand + Axios 直接管理状态和请求。

---

## 6. 类型定义

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

---

## 7. Zustand Store

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

### 7.2 使用示例

```typescript
// 在组件中使用
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
```

---

## 8. API 服务封装

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
}
```

> 💡 **注意**: 本项目使用 `ApiAdapter` 类封装 Axios，响应数据会自动从 snake_case 转换为 camelCase。

---

## 9. 路由配置

在 `src/router/index.ts` 中添加路由：

```typescript
// src/router/index.ts (React Router v7)

import { createBrowserRouter } from 'react-router-dom';
import CreditsView from '../views/CreditsView';
import AdminCreditsView from '../views/AdminCreditsView';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      // ... 现有路由 ...

      // 用户积分中心
      {
        path: 'credits',
        element: <CreditsView />,
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
        ],
      },
    ],
  },
]);
```

---

## 10. 余额不足提示

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

**文档版本**: v1.0
**创建时间**: 2025-12-02
**作者**: Claude Code
