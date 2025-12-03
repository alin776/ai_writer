# 积分系统前端实现方案

**创建时间**: 2025-12-03
**状态**: 待开发
**最后更新**: 2025-12-03

---

## 1. 最终设计方案

### 1.1 侧边栏结构

```
AI Writer (Logo)
|-- 创作
|   |-- 作品管理        /works
|   |-- 知识库          /knowledge
|-- 我的服务 (可折叠)
|   |-- 我的积分        /service/credits
|   |-- 使用记录        /service/usage
|   |-- 获取积分        /service/obtain
|-- 系统设置            /settings
|-- 用户信息
```

### 1.2 页面规划

| 页面 | 路由 | 说明 |
|------|------|------|
| 我的积分 | `/service/credits` | 余额卡片 + 统计概览 |
| 使用记录 | `/service/usage` | Token统计图表 + 积分交易流水 (合并页面) |
| 获取积分 | `/service/obtain` | [兑换码] [邀请好友] Tabs |

---

## 2. 技术栈 (与现有项目一致)

| 类型 | 技术 |
|------|------|
| 框架 | React 18 + TypeScript |
| 路由 | react-router-dom |
| 状态管理 | Zustand |
| 样式 | Tailwind CSS |
| 组件库 | Radix UI + 自定义组件 |
| 图标 | lucide-react |
| HTTP | 现有 DataService/ApiAdapter |
| 工具 | clsx, cn() |

---

## 3. 目录结构

```
src/
|-- components/
|   |-- service/                    # 我的服务相关组件
|   |   |-- BalanceCard.tsx         # 余额卡片
|   |   |-- StatsCard.tsx           # 统计卡片
|   |   |-- UsageChart.tsx          # Token使用饼图
|   |   |-- ModelStatsTable.tsx     # 模型统计表格
|   |   |-- TransactionList.tsx     # 交易记录列表
|   |   |-- RedeemForm.tsx          # 兑换码表单
|   |   |-- InvitationStats.tsx     # 邀请统计
|   |   |-- InvitationCodeList.tsx  # 邀请码列表
|   |   |-- GenerateInvitationDialog.tsx  # 生成邀请码弹窗
|   |-- layout/
|   |   |-- Sidebar.tsx             # 侧边栏 (需修改,添加我的服务)
|-- views/
|   |-- ServiceCreditsView/         # 我的积分页面
|   |   |-- index.tsx
|   |-- ServiceUsageView/           # 使用记录页面
|   |   |-- index.tsx
|   |-- ServiceObtainView/          # 获取积分页面
|   |   |-- index.tsx
|-- store/
|   |-- creditsStore.ts             # 积分状态管理
|   |-- invitationsStore.ts         # 邀请状态管理
|-- services/
|   |-- CreditsService.ts           # 积分API封装
|   |-- InvitationsService.ts       # 邀请API封装
|-- types/
|   |-- credits.ts                  # 积分类型定义 (已存在)
|   |-- invitations.ts              # 邀请类型定义 (已存在)
```

---

## 4. 页面详细设计

### 4.1 我的积分页面 (`/service/credits`)

```
+---------------------------------------------+
|  我的积分                                    |
+---------------------------------------------+
|  +---------------------------------------+  |
|  |  当前余额                              |  |
|  |                                       |  |
|  |     5,000.00 积分                      |  |
|  |     永不过期                           |  |
|  |                                       |  |
|  |     [兑换积分]                         |  |
|  +---------------------------------------+  |
|                                             |
|  +---------------------------------------+  |
|  |  积分统计                              |  |
|  |  +----------+ +----------+ +--------+ |  |
|  |  |累计充值   | |累计消耗   | |累计赠送 | |  |
|  |  |  0.00    | |  0.00    | |5000.00 | |  |
|  |  +----------+ +----------+ +--------+ |  |
|  +---------------------------------------+  |
|                                             |
|  最近交易 (5条)              [查看全部 ->]  |
|  +---------------------------------------+  |
|  | 赠送 | +5000.00 | 新用户赠送 | 12-03   |  |
|  +---------------------------------------+  |
+---------------------------------------------+
```

**API调用:**
- `GET /credits/balance` - 获取余额和统计
- `GET /credits/transactions?page_size=5` - 最近5条交易

### 4.2 使用记录页面 (`/service/usage`)

```
+---------------------------------------------+
|  使用记录                   [日期: 最近30天] |
+---------------------------------------------+
|  +------------------+  +------------------+  |
|  |  Token使用分布    |  |  详细统计数据     |  |
|  |                  |  |                  |  |
|  |   [饼图]         |  |  模型  请求 Token |  |
|  |                  |  |  gemini 386 35M  |  |
|  |                  |  |  claude 156 11M  |  |
|  +------------------+  +------------------+  |
|                                             |
+---------------------------------------------+
|  积分交易流水                                |
|  +---------------------------------------+  |
|  | 类型 | 金额    | 描述      | 时间      |  |
|  |------|---------|-----------|----------|  |
|  | 消费 | -2.50   | AI调用    | 2小时前   |  |
|  | 充值 | +100.00 | 兑换码    | 1天前     |  |
|  | 赠送 | +5000   | 新用户    | 2天前     |  |
|  +---------------------------------------+  |
|  [< 1 2 3 ... >]                            |
+---------------------------------------------+
```

**API调用:**
- `GET /ai-logs/me/stats?days=30` - Token统计
- `GET /credits/transactions` - 积分交易流水

### 4.3 获取积分页面 (`/service/obtain`)

```
+---------------------------------------------+
|  获取积分                                    |
+---------------------------------------------+
|  [兑换码]  [邀请好友]   <- Tabs              |
+---------------------------------------------+
|  (Tab1: 兑换码)                             |
|  +---------------------------------------+  |
|  |  输入兑换码                            |  |
|  |  +---------------------------+        |  |
|  |  | 请输入12位兑换码          |        |  |
|  |  +---------------------------+        |  |
|  |               [立即兑换]               |  |
|  |                                       |  |
|  |  说明:                                |  |
|  |  - 兑换码为12位字母数字组合            |  |
|  |  - 每个兑换码仅可使用一次              |  |
|  |  - 兑换成功后积分立即到账              |  |
|  +---------------------------------------+  |
+---------------------------------------------+
|  (Tab2: 邀请好友)                           |
|  +---------------------------------------+  |
|  |  邀请统计                [+ 生成邀请码] |  |
|  |  +------+ +------+ +------+ +------+  |  |
|  |  |总数 3| |激活 2| |奖励  | |配额  |  |  |
|  |  |     | |     | |2000 | |0/3  |  |  |
|  |  +------+ +------+ +------+ +------+  |  |
|  +---------------------------------------+  |
|                                             |
|  +---------------------------------------+  |
|  |  我的邀请码                            |  |
|  |  +-----------------------------------+|  |
|  |  | AB3CDE5F        [复制]    [展开]  ||  |
|  |  | ||||||||-- 3/10                   ||  |
|  |  | 激活: 2人  奖励: 2000积分          ||  |
|  |  |                                   ||  |
|  |  | 已邀请:                           ||  |
|  |  | [v] user123 已激活 2025-12-01     ||  |
|  |  | [o] user456 待激活 2025-12-03     ||  |
|  |  +-----------------------------------+|  |
|  +---------------------------------------+  |
+---------------------------------------------+
```

**API调用:**
- `POST /credits/redeem` - 兑换积分
- `GET /invitations/stats` - 邀请统计
- `GET /invitations/my-codes` - 我的邀请码
- `POST /invitations/generate` - 生成邀请码

---

## 5. 侧边栏修改方案

### 5.1 新增导航配置

```typescript
// Sidebar.tsx 新增配置

import {
  Wallet,           // 我的积分
  BarChart3,        // 使用记录
  Gift,             // 获取积分
  ChevronDown,      // 折叠箭头
} from 'lucide-react';

/**
 * 我的服务导航菜单配置
 */
const serviceNavItems: NavItem[] = [
  {
    id: 'credits',
    label: '我的积分',
    icon: Wallet,
    path: '/service/credits',
  },
  {
    id: 'usage',
    label: '使用记录',
    icon: BarChart3,
    path: '/service/usage',
  },
  {
    id: 'obtain',
    label: '获取积分',
    icon: Gift,
    path: '/service/obtain',
  },
];
```

### 5.2 可折叠菜单组实现

```typescript
// 新增状态
const [isServiceExpanded, setIsServiceExpanded] = useState(true);

// 渲染可折叠菜单组
<div className="mt-6 space-y-0.5">
  {/* 菜单组标题 - 可点击折叠 */}
  <button
    onClick={() => setIsServiceExpanded(!isServiceExpanded)}
    className={clsx(
      'w-full flex items-center justify-between px-3 py-2 text-xs font-medium text-gray-400 uppercase tracking-wider hover:text-gray-600 transition-colors',
      isCollapsed && 'justify-center'
    )}
  >
    {!isCollapsed && <span>我的服务</span>}
    <ChevronDown
      className={clsx(
        'w-4 h-4 transition-transform',
        !isServiceExpanded && '-rotate-90'
      )}
    />
  </button>

  {/* 子菜单项 */}
  {isServiceExpanded && serviceNavItems.map(renderNavItem)}
</div>
```

---

## 6. Store 设计

### 6.1 creditsStore.ts

```typescript
import { create } from 'zustand';
import { CreditsService } from '../services/CreditsService';

interface CreditsState {
  // 数据
  balance: BalanceInfo | null;
  transactions: CreditTransaction[];
  transactionTotal: number;

  // 状态
  isLoading: boolean;
  error: string | null;

  // 方法
  fetchBalance: () => Promise<void>;
  fetchTransactions: (page?: number, pageSize?: number, type?: string) => Promise<void>;
  redeem: (code: string) => Promise<RedeemResponse>;
  clearError: () => void;
}

export const useCreditsStore = create<CreditsState>((set, get) => ({
  balance: null,
  transactions: [],
  transactionTotal: 0,
  isLoading: false,
  error: null,

  fetchBalance: async () => {
    set({ isLoading: true, error: null });
    try {
      const balance = await CreditsService.getBalance();
      set({ balance, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchTransactions: async (page = 1, pageSize = 20, type) => {
    set({ isLoading: true, error: null });
    try {
      const result = await CreditsService.getTransactions({ page, page_size: pageSize, type });
      set({
        transactions: result.transactions,
        transactionTotal: result.total,
        isLoading: false
      });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  redeem: async (code: string) => {
    set({ isLoading: true, error: null });
    try {
      const result = await CreditsService.redeem(code);
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

### 6.2 invitationsStore.ts

```typescript
import { create } from 'zustand';
import { InvitationsService } from '../services/InvitationsService';

interface InvitationsState {
  // 数据
  stats: InvitationStats | null;
  myCodes: InvitationCodeDetail[];

  // 状态
  isLoading: boolean;
  error: string | null;

  // 方法
  fetchStats: () => Promise<void>;
  fetchMyCodes: () => Promise<void>;
  generateCode: (maxUses?: number, expiresDays?: number) => Promise<InvitationCodeDetail>;
  clearError: () => void;
}

export const useInvitationsStore = create<InvitationsState>((set, get) => ({
  stats: null,
  myCodes: [],
  isLoading: false,
  error: null,

  fetchStats: async () => {
    set({ isLoading: true, error: null });
    try {
      const stats = await InvitationsService.getStats();
      set({ stats, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchMyCodes: async () => {
    set({ isLoading: true, error: null });
    try {
      const myCodes = await InvitationsService.getMyCodes();
      set({ myCodes, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  generateCode: async (maxUses = 10, expiresDays) => {
    set({ isLoading: true, error: null });
    try {
      const code = await InvitationsService.generate({ max_uses: maxUses, expires_days: expiresDays });
      // 刷新列表和统计
      await Promise.all([get().fetchMyCodes(), get().fetchStats()]);
      set({ isLoading: false });
      return code;  // 返回 InvitationCodeDetail
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));
```

---

## 7. API Service 封装

### 7.1 CreditsService.ts

```typescript
import { ApiAdapter } from './ApiAdapter';

export class CreditsService {
  /**
   * 获取积分余额
   */
  static async getBalance(): Promise<BalanceInfo> {
    return ApiAdapter.get('/credits/balance');
  }

  /**
   * 获取交易记录
   */
  static async getTransactions(params: {
    page?: number;
    page_size?: number;
    type?: string;
  }): Promise<TransactionListResponse> {
    return ApiAdapter.get('/credits/transactions', { params });
  }

  /**
   * 兑换积分
   */
  static async redeem(code: string): Promise<RedeemResponse> {
    return ApiAdapter.post('/credits/redeem', { code });
  }
}
```

### 7.2 InvitationsService.ts

```typescript
import { ApiAdapter } from './ApiAdapter';

export class InvitationsService {
  /**
   * 获取邀请统计
   */
  static async getStats(): Promise<InvitationStats> {
    return ApiAdapter.get('/invitations/stats');
  }

  /**
   * 获取我的邀请码（含被邀请人列表）
   */
  static async getMyCodes(): Promise<InvitationCodeDetail[]> {
    return ApiAdapter.get('/invitations/my-codes');
  }

  /**
   * 生成邀请码
   * 注意：后端直接返回 InvitationCodeDetail，不是 { code: ... } 格式
   */
  static async generate(params: {
    max_uses?: number;
    expires_days?: number;
  }): Promise<InvitationCodeDetail> {
    return ApiAdapter.post('/invitations/generate', params);
  }

  /**
   * 验证邀请码 (公开接口)
   */
  static async validate(code: string): Promise<ValidateResponse> {
    return ApiAdapter.post('/invitations/validate', { code });
  }
}
```

---

## 8. 组件代码风格规范

### 8.1 组件模板

```typescript
import React, { useState, useEffect } from 'react';
import { IconName } from 'lucide-react';
import { Card, Button } from '../../components/common';
import { useCreditsStore } from '../../store/creditsStore';
import { useToast } from '../../hooks/useToast';
import clsx from 'clsx';

interface ComponentNameProps {
  prop1?: string;
  prop2?: number;
}

/**
 * ComponentName 组件 - 组件描述
 *
 * 功能:
 * - 功能点1
 * - 功能点2
 */
const ComponentName: React.FC<ComponentNameProps> = ({
  prop1 = 'default',
  prop2,
}) => {
  const { data, isLoading, fetchData } = useCreditsStore();
  const { success, error } = useToast();

  useEffect(() => {
    fetchData();
  }, []);

  if (isLoading) {
    return <div className="text-center py-8 text-gray-500">加载中...</div>;
  }

  return (
    <Card padding="lg">
      {/* 组件内容 */}
    </Card>
  );
};

export default ComponentName;
```

### 8.2 样式规范

```typescript
// 颜色规范
const colors = {
  // 积分相关
  balance: 'text-amber-600',      // 余额数字
  recharge: 'text-green-600',     // 充值/收入
  consume: 'text-red-600',        // 消费/支出
  gift: 'text-blue-600',          // 赠送

  // 状态相关
  active: 'text-green-500',       // 已激活
  pending: 'text-orange-500',     // 待激活
  expired: 'text-gray-400',       // 已过期
};

// 间距规范
const spacing = {
  page: 'p-6',                    // 页面内边距
  section: 'space-y-6',           // 区块间距
  card: 'p-4',                    // 卡片内边距
  grid: 'gap-4',                  // 网格间距
};

// 响应式布局
const responsive = {
  statsGrid: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4',
  twoColumn: 'grid grid-cols-1 lg:grid-cols-2 gap-6',
};
```

---

## 9. 开发顺序

### Phase 1: 基础设施
1. [ ] 创建 `src/types/credits.ts` 类型定义 (已存在,检查完整性)
2. [ ] 创建 `src/types/invitations.ts` 类型定义 (已存在,检查完整性)
3. [ ] 创建 `src/services/CreditsService.ts`
4. [ ] 创建 `src/services/InvitationsService.ts`
5. [ ] 创建 `src/store/creditsStore.ts`
6. [ ] 创建 `src/store/invitationsStore.ts`

### Phase 2: 侧边栏修改
7. [ ] 修改 `src/components/layout/Sidebar.tsx` 添加"我的服务"菜单组
8. [ ] 添加路由配置

### Phase 3: 页面开发
9. [ ] 创建 `src/views/ServiceCreditsView/index.tsx` - 我的积分
10. [ ] 创建 `src/views/ServiceUsageView/index.tsx` - 使用记录
11. [ ] 创建 `src/views/ServiceObtainView/index.tsx` - 获取积分

### Phase 4: 组件开发
12. [ ] BalanceCard.tsx - 余额卡片
13. [ ] StatsCard.tsx - 统计卡片
14. [ ] UsageChart.tsx - Token使用饼图
15. [ ] TransactionList.tsx - 交易记录列表
16. [ ] RedeemForm.tsx - 兑换码表单
17. [ ] InvitationCodeList.tsx - 邀请码列表

### Phase 5: 集成测试
18. [ ] 页面联调测试
19. [ ] 样式调整
20. [ ] 响应式适配

---

## 10. 注意事项

1. **保持代码风格一致**: 参考现有 SettingsView, Sidebar 的写法
2. **使用现有组件**: Card, Button, Input, Tabs 等
3. **使用现有hooks**: useToast, useAuthStore
4. **TypeScript严格模式**: 所有接口和类型都要定义
5. **错误处理**: 统一使用 useToast 显示错误
6. **加载状态**: 所有异步操作显示加载状态

---

**文档版本**: v1.0
**创建时间**: 2025-12-03
**作者**: Claude Code
