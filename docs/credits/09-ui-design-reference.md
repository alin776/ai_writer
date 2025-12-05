# 积分系统UI设计参考文档

**创建时间**: 2025-12-03
**参考项目**: [QuantumNous/new-api](https://github.com/QuantumNous/new-api)
**状态**: 设计阶段

---

## 📚 参考项目分析

### 项目背景
**new-api** 是一个AI模型聚合管理中转分发系统，包含完整的用户管理、钱包管理、兑换码系统。

- **GitHub**: https://github.com/QuantumNous/new-api
- **Stars**: 13.1k
- **技术栈**:
  - 前端: React + Vite + Tailwind CSS + Semi UI
  - 后端: Go
- **许可**: GNU AGPL v3.0

### 核心页面
- **TopUp** - 充值/余额管理页面
- **Redemption** - 兑换码管理页面
- **Token** - 令牌管理
- **Pricing** - 价格展示

---

## 🎨 设计要点总结

### 1. 架构设计
```
页面组件 (简洁)
   ↓
业务组件 (复杂逻辑)
   ↓
子组件 (可复用)
```

#### 示例：Redemption 页面
```jsx
// pages/Redemption/index.jsx (简洁的页面组件)
const Redemption = () => {
  return (
    <div className='mt-[60px] px-2'>
      <RedemptionsTable />
    </div>
  );
};

// components/table/redemptions/RedemptionsTable.jsx (复杂的业务组件)
const RedemptionsTable = (props) => {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const columns = useMemo(() => getRedemptionsColumns(...), [deps]);

  return (
    <>
      <CardTable
        columns={columns}
        dataSource={redemptions}
        pagination={{ ... }}
        empty={<Empty illustration={...} />}
      />
      <DeleteRedemptionModal ... />
    </>
  );
};
```

**优点**:
- 页面组件职责单一，易于维护
- 业务逻辑集中在业务组件
- 子组件高度复用

---

### 2. 表格设计

#### 核心组件：CardTable
- 使用 Semi UI 的 CardTable 组件
- 支持分页：10 / 20 / 50 / 100 条/页
- 支持排序、筛选
- 空状态展示：Empty 组件 + 插图

#### 列配置 (useMemo优化)
```jsx
const columns = useMemo(() => getRedemptionsColumns({
  handleEdit,
  handleDelete,
  isCompactMode,
  t
}), [handleEdit, handleDelete, isCompactMode, t]);
```

#### 响应式设计
```jsx
// compact mode 适配移动端
if (isCompactMode) {
  // 移除固定宽度的操作列
  columnsConfig = columnsConfig.filter(col => col.key !== 'actions');
}
```

---

### 3. 模态框设计

#### 确认模态框
- 危险操作（删除）使用 Modal 确认
- 统一的样式和交互
- 明确的操作提示

```jsx
<DeleteRedemptionModal
  visible={showDeleteModal}
  onCancel={() => setShowDeleteModal(false)}
  onConfirm={() => manageRedemption(deletingRecord.id)}
  record={deletingRecord}
/>
```

#### 表单模态框
- 输入框验证
- 提交状态管理
- 错误提示

---

### 4. 状态管理模式

```jsx
// 列表数据
const [redemptions, setRedemptions] = useState([]);
const [loading, setLoading] = useState(false);

// 分页
const [pagination, setPagination] = useState({
  currentPage: 1,
  pageSize: 10,
  total: 0
});

// UI状态
const [showDeleteModal, setShowDeleteModal] = useState(false);
const [deletingRecord, setDeletingRecord] = useState(null);
```

---

### 5. 空状态设计

```jsx
<Empty
  illustration={<IllustrationNoResult style={{ width: 150, height: 150 }} />}
  darkModeIllustration={<IllustrationNoResultDark style={{ width: 150, height: 150 }} />}
  title={t('No search results')}
  description={t('Try adjusting your search terms')}
/>
```

---

## 🎯 应用到积分系统的设计方案

### 页面结构设计

#### 1. 用户端 - 积分中心 (`/credits`)
```
CreditsView (页面)
  ├── BalanceCard (余额卡片)
  ├── StatsCard (统计卡片)
  └── TransactionsTable (交易记录表格)
       ├── TransactionFilters (筛选器)
       ├── CardTable (数据表格)
       └── TransactionDetailsModal (详情弹窗)
```

#### 2. 用户端 - 兑换功能
```
RedeemDialog (兑换弹窗)
  ├── Input (兑换码输入)
  ├── Button (验证/兑换按钮)
  └── Result (成功/失败提示)
```

#### 3. 用户端 - 邀请中心 (`/invitations`)
```
InvitationsView (页面)
  ├── InvitationStatsCard (统计卡片)
  ├── MyInvitationsList (我的邀请码列表)
  │    └── InvitationCodeCard (邀请码卡片 - 可展开)
  │         └── InviteesList (被邀请人列表)
  └── GenerateInvitationDialog (生成弹窗)
```

#### 4. 管理端 - 兑换码管理 (`/admin/credits/codes`)
```
AdminCreditsView (页面)
  ├── PageHeader (页头 + 生成按钮)
  ├── CodesFilters (筛选器)
  ├── CodesStats (统计数据)
  └── RedeemCodesTable (兑换码表格)
       ├── CardTable
       └── GenerateCodesDialog (生成弹窗)
            └── GeneratedCodesResult (生成结果展示)
```

#### 5. 管理端 - 邀请码管理 (`/admin/invitations`)
```
AdminInvitationsView (页面)
  ├── PageHeader (页头 + 批量生成按钮)
  ├── InvitationsFilters (筛选器)
  └── InvitationsTable (邀请码表格)
       ├── CardTable
       └── BatchGenerateDialog (批量生成弹窗)
```

---

## 🎨 UI设计细节

### 色彩方案

#### 积分相关
- **余额/积分**: `text-amber-600` `bg-amber-50` 金色系
- **充值/赠送**: `text-green-600` `bg-green-50` 绿色系
- **消费/扣减**: `text-red-600` `bg-red-50` 红色系
- **过期**: `text-gray-400` `bg-gray-50` 灰色系

#### 邀请相关
- **已激活**: `text-green-500` 绿色
- **待激活**: `text-orange-500` 橙色
- **已过期**: `text-gray-400` 灰色

#### 状态标识
```jsx
// 交易类型徽章
<Badge className={TRANSACTION_TYPE_CONFIG[type].color}>
  {TRANSACTION_TYPE_CONFIG[type].icon} {TRANSACTION_TYPE_CONFIG[type].label}
</Badge>

// 邀请状态徽章
<Badge className={INVITATION_STATUS_CONFIG[status].color}>
  {INVITATION_STATUS_CONFIG[status].icon} {INVITATION_STATUS_CONFIG[status].label}
</Badge>
```

---

### 布局设计

#### 卡片统一样式
```jsx
<div className="rounded-lg shadow-sm border border-gray-200 bg-white p-6">
  {/* 卡片内容 */}
</div>
```

#### 响应式网格
```jsx
// 统计卡片 - 3列布局
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <StatsItem label="累计充值" value={totalRecharged} />
  <StatsItem label="累计消耗" value={totalConsumed} />
  <StatsItem label="累计赠送" value={totalGifted} />
</div>
```

#### 间距规范
- 页面边距: `px-4 py-6` 或 `p-6`
- 卡片间距: `gap-4` 或 `gap-6`
- 组件内间距: `space-y-4`

---

### 交互设计

#### 1. 一键复制
```jsx
const handleCopy = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text);
    toast.success('复制成功');
  } catch (error) {
    toast.error('复制失败');
  }
};

// UI
<Button
  onClick={() => handleCopy(code)}
  icon={<CopyIcon />}
  size="small"
>
  复制
</Button>
```

#### 2. 加载状态
```jsx
{isLoading ? (
  <Loading />
) : (
  <CardTable dataSource={data} />
)}
```

#### 3. 错误处理
```jsx
try {
  await api.redeemCredits(code);
  toast.success('兑换成功');
  await fetchBalance(); // 刷新余额
} catch (error) {
  toast.error(error.message || '兑换失败');
}
```

#### 4. 表单验证
```jsx
const validateCode = (code: string) => {
  if (!code) return '请输入兑换码';
  if (code.length !== 12) return '兑换码格式不正确';
  return null;
};
```

---

## 📦 组件设计清单

### 用户端组件

#### 积分组件 (`src/components/credits/`)
1. **BalanceCard.tsx** - 余额卡片
   - 大号余额数字 (text-4xl font-bold text-amber-600)
   - 有效期显示
   - 兑换按钮

2. **StatsCard.tsx** - 统计卡片
   - 3个统计项网格布局
   - 图标 + 数值展示

3. **TransactionList.tsx** - 交易记录列表
   - CardTable 表格
   - 类型筛选器
   - 日期范围选择器
   - 分页器

4. **RedeemDialog.tsx** - 兑换弹窗
   - Modal 组件
   - 输入框 + 验证
   - 成功/失败反馈

#### 邀请组件 (`src/components/invitations/`)
1. **InvitationStatsCard.tsx** - 邀请统计卡片
   - 4个统计项
   - 生成按钮

2. **InvitationCodeCard.tsx** - 邀请码卡片
   - 可展开/折叠
   - 复制按钮
   - 进度条 (已用/总数)
   - 被邀请人列表

3. **GenerateInvitationDialog.tsx** - 生成邀请码弹窗
   - 表单 (最大次数、有效期)
   - 限制检查提示
   - 冷却期提示

4. **InviteeList.tsx** - 被邀请人列表
   - 用户名
   - 状态徽章
   - 时间显示

---

### 管理端组件

#### 管理组件 (`src/components/admin/`)
1. **CodeList.tsx** - 兑换码列表
   - 筛选器组
   - 统计栏
   - CardTable 表格
   - 操作列 (复制/删除)

2. **GenerateCodesDialog.tsx** - 生成兑换码弹窗
   - 多步骤表单
   - 生成结果展示
   - 批量复制功能

3. **InvitationsList.tsx** - 邀请码管理列表
   - 筛选器
   - CardTable 表格
   - 详情查看

---

## 🔧 技术实现要点

### 1. 状态管理 (Zustand)

#### creditsStore.ts
```typescript
interface CreditsState {
  // 数据状态
  balance: BalanceInfo | null;
  transactions: CreditTransaction[];

  // UI状态
  isLoading: boolean;
  error: string | null;

  // 操作方法
  fetchBalance: () => Promise<void>;
  fetchTransactions: (params?: TransactionQueryParams) => Promise<void>;
  redeem: (code: string) => Promise<RedeemResponse>;
  clearError: () => void;
}
```

#### invitationsStore.ts
```typescript
interface InvitationsState {
  stats: InvitationStats | null;
  myCodes: InvitationCodeDetail[];
  isLoading: boolean;
  error: string | null;

  fetchStats: () => Promise<void>;
  fetchMyCodes: () => Promise<void>;
  generateCode: (params: GenerateInvitationRequest) => Promise<InvitationCode>;
  validateCode: (code: string) => Promise<ValidateInvitationResponse>;
}
```

---

### 2. API 封装

#### ApiAdapter 扩展
```typescript
// 积分相关
async getCreditsBalance(): Promise<BalanceInfo>
async getCreditsTransactions(params): Promise<PaginatedResponse<CreditTransaction>>
async redeemCredits(code: string): Promise<RedeemResponse>

// 管理端
async generateRedeemCodes(data): Promise<GenerateCodesResponse>
async getRedeemCodes(params): Promise<PaginatedResponse<RedeemCode>>

// 邀请相关
async getInvitationStats(): Promise<InvitationStats>
async getMyInvitations(): Promise<InvitationCodeDetail[]>
async generateInvitation(params): Promise<GenerateInvitationResponse>
async validateInvitation(code: string): Promise<ValidateInvitationResponse>

// 管理端
async batchGenerateInvitations(data): Promise<BatchGenerateInvitationsResponse>
async getAllInvitations(params): Promise<PaginatedResponse<InvitationCode>>
```

---

### 3. 数据格式化工具

#### 积分格式化
```typescript
export const formatCredits = (amount: number): string => {
  return amount.toFixed(2);
};

export const formatCreditsWithSign = (amount: number): string => {
  const sign = amount >= 0 ? '+' : '';
  return `${sign}${formatCredits(amount)}`;
};
```

#### 日期格式化
```typescript
export const formatDate = (dateStr: string): string => {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const formatRelativeTime = (dateStr: string): string => {
  const date = new Date(dateStr);
  const now = new Date();
  const diff = now.getTime() - date.getTime();

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  if (days > 0) return `${days}天前`;

  const hours = Math.floor(diff / (1000 * 60 * 60));
  if (hours > 0) return `${hours}小时前`;

  return '刚刚';
};
```

---

### 4. 复用现有组件

#### 基础组件 (src/components/common/)
- **Button.tsx** - 按钮组件
- **Modal.tsx** - 模态框组件
- **Input.tsx** - 输入框组件
- **Loading.tsx** - 加载组件
- **Toast.tsx** - 提示组件
- **Card.tsx** - 卡片组件

#### UI组件 (src/components/ui/)
- **badge.tsx** - 徽章组件
- **dialog.tsx** - 对话框组件
- **select.tsx** - 选择器组件
- **tabs.tsx** - 标签页组件

---

## 📊 页面布局示例

### 用户端 - 积分中心
```
┌─────────────────────────────────────────────────┐
│  积分中心                                        │
├─────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────┐    │
│  │  💰 当前余额                             │    │
│  │                                         │    │
│  │     5,280.50 积分                        │    │
│  │     永不过期                             │    │
│  │                                         │    │
│  │     [兑换积分]                           │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  📊 积分统计                             │    │
│  │  ┌───────┐  ┌───────┐  ┌───────┐        │    │
│  │  │累计充值│  │累计消耗│  │累计赠送│        │    │
│  │  │200.00 │  │100.50 │  │ 50.00 │        │    │
│  │  └───────┘  └───────┘  └───────┘        │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  📜 交易记录                             │    │
│  │  [类型▼] [日期范围]                     │    │
│  │  ┌───────────────────────────────────┐  │    │
│  │  │ 类型  │ 金额   │ 描述  │ 余额  │时间│  │    │
│  │  ├───────┼────────┼───────┼───────┼───┤  │    │
│  │  │💸消费 │ -2.50  │AI调用│99.50 │2h │  │    │
│  │  │💰充值 │+100.00 │兑换码│102.00│1d │  │    │
│  │  │🎁赠送 │ +50.00 │新用户│ 2.00 │2d │  │    │
│  │  └───────┴────────┴───────┴───────┴───┘  │    │
│  │  [< 1/5 >]                              │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### 用户端 - 邀请中心
```
┌─────────────────────────────────────────────────┐
│  邀请中心                                        │
├─────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────┐    │
│  │  🎁 邀请统计                [+ 生成新码]  │    │
│  │  ┌────┐  ┌────┐  ┌────┐  ┌────┐        │    │
│  │  │总数 │  │激活 │  │奖励 │  │配额 │        │    │
│  │  │ 3  │  │ 2  │  │2000│  │0/3 │        │    │
│  │  └────┘  └────┘  └────┘  └────┘        │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  📋 我的邀请码                           │    │
│  │  ┌─────────────────────────────────┐    │    │
│  │  │ 邀请码: AB3CDE5F    [复制] [▼] │    │    │
│  │  │ ▓▓▓▓▓▓░░░░ 3/10                 │    │    │
│  │  │ 激活: 2人  奖励: 2000积分        │    │    │
│  │  │                                 │    │    │
│  │  │ 已邀请用户:                      │    │    │
│  │  │ ✅ user123 (已激活) 2025-12-01  │    │    │
│  │  │ ⏳ user456 (待激活) 2025-12-03  │    │    │
│  │  │ ✅ user789 (已激活) 2025-11-30  │    │    │
│  │  └─────────────────────────────────┘    │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## 🚀 实施建议

### 开发顺序
1. **第一阶段**: 类型定义 + Store + API封装
2. **第二阶段**: 用户端积分中心 (核心功能)
3. **第三阶段**: 用户端邀请中心
4. **第四阶段**: 管理端功能
5. **第五阶段**: 注册页面改造
6. **第六阶段**: 路由和导航集成
7. **第七阶段**: 细节优化和测试

### 优先级
- **P0**: 积分余额展示、交易记录、兑换功能
- **P1**: 邀请码生成、我的邀请码
- **P2**: 管理端兑换码管理
- **P3**: 管理端邀请码管理、批量功能

### 技术风险
1. **Semi UI 替换** - new-api使用Semi UI，我们使用Radix UI
   - 解决方案: 参考设计思路，使用Radix UI实现

2. **CardTable组件** - 我们可能没有现成的CardTable
   - 解决方案: 使用HTML table + Tailwind CSS自定义

3. **响应式适配** - 确保移动端体验
   - 解决方案: 使用Tailwind响应式类，测试不同屏幕尺寸

---

## 📝 待讨论问题

1. **余额展示位置**: Header全局显示 vs 仅积分页面显示?
2. **余额不足提示**: 主动检查 vs 被动提示 vs 两者结合?
3. **邀请码展示**: 完整码 vs 短码 vs 二维码?
4. **交易记录筛选**: 基础版 vs 进阶版 vs 完整版?
5. **管理端优先级**: 哪些功能必须有，哪些可以后续迭代?
6. **移动端优先级**: PC为主 vs 移动为主 vs 两者兼顾?

---

## 📚 参考资源

### 项目链接
- **GitHub**: https://github.com/QuantumNous/new-api
- **文档**: https://docs.newapi.pro/

### 关键文件路径
- 兑换页面: `web/src/pages/Redemption/index.jsx`
- 兑换表格: `web/src/components/table/redemptions/RedemptionsTable.jsx`
- 充值页面: `web/src/pages/TopUp/index.js`

### 技术文档
- React 19: https://react.dev/
- Tailwind CSS: https://tailwindcss.com/
- Radix UI: https://www.radix-ui.com/
- Zustand: https://zustand-demo.pmnd.rs/

---

**文档版本**: v1.0
**最后更新**: 2025-12-03
**作者**: Claude Code
