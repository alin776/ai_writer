# 积分系统UI设计决策记录

**确认时间**: 2025-12-03
**状态**: ✅ 已确认，可以开始开发

---

## ✅ 设计决策总结

| 决策项 | 最终选择 | 说明 |
|--------|---------|------|
| 余额展示位置 | **仅页面显示** | 余额只在积分中心页面显示，后续可扩展到Header |
| 余额不足提示 | **被动提示** | 用户点击AI功能后，如果余额不足则弹窗提示（后端返回402） |
| 邀请码展示 | **完整码 + 复制按钮** | 直接显示完整邀请码 `AB3CDE5FGH7K`，方便复制分享 |
| 交易记录筛选 | **进阶版** | 支持类型筛选 + 日期范围筛选 |
| 移动端优先级 | **PC为主** | 优先考虑PC端体验，使用表格等复杂组件 |

---

## 📋 实现要点

### 1. 余额展示
```
仅在 /credits 页面显示
- BalanceCard 组件显示余额
- 不在 Header 显示
```

### 2. 余额不足处理
```
后端：
- AI调用时检查余额
- 余额不足返回 402 Payment Required

前端：
- 全局拦截 402 状态码
- 弹窗提示"余额不足"
- 提供[去充值]按钮跳转 /credits
```

### 3. 邀请码展示
```jsx
<code className="text-lg font-mono">AB3CDE5FGH7K</code>
<Button onClick={handleCopy}>复制</Button>
```

### 4. 交易记录筛选器
```jsx
<Select>  {/* 类型筛选 */}
  <option value="">全部类型</option>
  <option value="recharge">充值</option>
  <option value="consume">消费</option>
  <option value="gift">赠送</option>
</Select>

<DateRangePicker />  {/* 日期范围 */}
```

### 5. 移动端处理
```
PC端：
- 使用表格（多列）
- 鼠标悬浮提示
- 横向筛选器

移动端：
- 表格可左右滑动
- 小屏幕隐藏部分列（可选）
- 不需要专门优化
```

---

## 🎨 UI规范快速参考

### 色彩
- 积分/余额: `text-amber-600 bg-amber-50`
- 充值/赠送: `text-green-600 bg-green-50`
- 消费/扣减: `text-red-600 bg-red-50`
- 已激活: `text-green-500`
- 待激活: `text-orange-500`
- 过期: `text-gray-400 bg-gray-50`

### 布局
- 卡片: `rounded-lg shadow-sm border border-gray-200 bg-white p-6`
- 响应式网格: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4`
- 页面边距: `px-4 py-6`

---

## 📚 相关文档

- [10-ui-design-summary.md](./10-ui-design-summary.md) - 完整设计总结
- [09-ui-design-reference.md](./09-ui-design-reference.md) - UI设计参考文档

---

**文档版本**: v1.0
**最后更新**: 2025-12-03
