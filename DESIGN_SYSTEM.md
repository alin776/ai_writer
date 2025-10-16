# AI Writer 设计系统

## 设计理念

**Less is More, Clarity is Key** - 极简主义与功能性美学的完美结合

### 核心原则

1. **极简主义** - 去除多余装饰，专注核心内容
2. **专注性** - 清晰的视觉重心，引导用户专注任务
3. **呼吸感** - 充分的留白空间，提升可读性
4. **统一性** - 全局设计元素保持一致
5. **功能美学** - 设计服务于功能

---

## 色彩系统

### 主色调
- **黑色**: `#111827` (gray-900) - 主要文本、按钮、重要元素
- **白色**: `#FFFFFF` - 背景、卡片

### 灰度系统
```
gray-50:  #F9FAFB  - 浅背景
gray-100: #F3F4F6  - 边框、分隔线
gray-200: #E5E7EB  - 次要边框
gray-400: #9CA3AF  - 辅助文字
gray-500: #6B7280  - 二级文字
gray-600: #4B5563  - 导航链接
gray-700: #374151  - 主要文字
gray-800: #1F2937  - Hover 状态
gray-900: #111827  - 强调元素
```

### 使用原则
- 背景：纯白 (#FFFFFF) 或极浅灰 (gray-50)
- 边框：gray-100 / gray-200 极细线条
- 文字：gray-900 (主) / gray-600 (次) / gray-500 (辅)
- 强调：gray-900 黑色按钮/元素

---

## 字体系统

### 字体家族
```css
font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
```

### 字体层级

#### 标题
- **Hero**: 60-72px / font-light / line-height: 1.1
- **H1**: 48-60px / font-light / line-height: 1.1
- **H2**: 30-36px / font-light / line-height: 1.2
- **H3**: 14px / font-medium / line-height: 1.4

#### 正文
- **Body Large**: 18px / font-normal / line-height: 1.6
- **Body**: 16px / font-normal / line-height: 1.6
- **Body Small**: 14px / font-normal / line-height: 1.5
- **Caption**: 12px / font-normal / line-height: 1.5

#### 字重
- Light (300): 大标题
- Normal (400): 正文
- Medium (500): 小标题
- Semibold (600): 强调

---

## 间距系统

### 标准间距（基于 4px）
```
xs:  4px   - 紧密元素间距
sm:  8px   - 小间距
md:  16px  - 标准间距
lg:  24px  - 大间距
xl:  32px  - 区块间距
2xl: 48px  - 大区块间距
3xl: 64px  - Section 间距
```

### 页面边距
- Container max-width: 1200px (max-w-6xl)
- Hero max-width: 896px (max-w-4xl)
- Content max-width: 800px (max-w-3xl)
- 水平 padding: 24px (px-6)

### 垂直间距
- Section: py-20 (80px)
- Hero: py-24 md:py-32 (96-128px)
- Card内部: p-6 (24px)

---

## 组件样式

### 按钮

#### Primary Button
```tsx
className="px-6 py-2.5 bg-gray-900 text-white text-sm rounded
           hover:bg-gray-800 transition-colors duration-200"
```

#### Secondary Button
```tsx
className="px-6 py-2.5 text-sm text-gray-700 border border-gray-200 rounded
           hover:border-gray-300 hover:bg-gray-50 transition-all duration-200"
```

#### Ghost Button
```tsx
className="px-4 py-1.5 text-sm text-gray-700
           hover:text-gray-900 transition-colors duration-200"
```

### 卡片
```tsx
className="p-6 bg-white border border-gray-100 rounded-lg
           hover:border-gray-200 hover:shadow-sm
           transition-all duration-200"
```

### 输入框
```tsx
className="px-4 py-2.5 text-sm border border-gray-200 rounded
           focus:border-gray-400 focus:outline-none
           transition-colors duration-200"
```

---

## 圆角系统

```
none:   0px
sm:     2px    - 小元素
default: 4px   - 按钮、输入框
md:     6px    - 卡片
lg:     8px    - 大卡片
xl:     12px   - Modal
```

**使用原则**: 统一使用 4px (rounded) 或 8px (rounded-lg)

---

## 阴影系统

```css
/* 极轻微阴影 - 卡片 hover */
shadow-sm: 0 1px 2px rgba(0,0,0,0.05)

/* 轻阴影 - Modal */
shadow: 0 1px 3px rgba(0,0,0,0.1)

/* 中等阴影 - Dropdown */
shadow-md: 0 4px 6px rgba(0,0,0,0.1)
```

**使用原则**: 默认无阴影，hover 时添加 shadow-sm

---

## 动画与过渡

### 标准过渡
```css
transition-colors duration-200  /* 颜色变化 */
transition-all duration-200     /* 综合变化 */
```

### Hover 效果

#### 按钮
- 颜色加深: `hover:bg-gray-800`
- 边框加深: `hover:border-gray-300`

#### 卡片
- 边框变化: `hover:border-gray-200`
- 添加阴影: `hover:shadow-sm`

#### 图标
- 位移: `group-hover:translate-x-0.5`
- 颜色: `group-hover:text-white`

**使用原则**: 平滑、微弱、不过度

---

## 页面布局规范

### 首页 (HomeView)

#### Header
- 高度: h-14 (56px)
- 背景: bg-white/80 backdrop-blur-sm
- 边框: border-b border-gray-100
- Logo: 6x6 黑色方块 + 文字
- 导航: 极简文字链接
- CTA: 黑色主按钮

#### Hero Section
- 垂直间距: py-24 md:py-32
- 水平宽度: max-w-4xl
- Badge: 12px 灰色文字 + 图标
- 标题: 60-72px font-light 黑色
- 副标题: 16-18px gray-500 双行
- 按钮: 间距 gap-3

#### Features Section
- 背景: bg-gray-50/50 (微妙灰)
- 网格: 3列 gap-6
- 卡片: p-6 白色背景 轻边框
- 图标: 10x10 gray-50 背景
- 标题: 14px font-medium
- 描述: 12px gray-500

#### CTA Section
- 背景: bg-gray-900 黑色
- 文字: 白色/gray-400
- 按钮: 白底黑字 + 边框

#### Footer
- 高度: py-8
- 边框: border-t border-gray-100
- 文字: text-xs gray-400

---

## 登录/注册页面

### 布局
- 全屏居中
- 表单容器: max-w-md (448px)
- 圆角: rounded-lg
- 内边距: p-8

### 表单元素
- 标签: text-sm font-medium gray-700
- 输入框: py-2.5 border-gray-200
- 按钮: w-full py-2.5 黑色
- 链接: text-sm gray-600

---

## 编辑器页面

### 核心原则
- **绝对专注**: 编辑区域无边框干扰
- **纯净背景**: 白色或极浅灰
- **高对比度**: 确保可读性

### 布局
- 编辑区: 宽敞、居中、max-w-4xl
- 工具栏: 扁平化、图标为主
- 侧边栏: 可收起、轻边框

---

## 后台管理页面

### 表格
- 行高: h-12
- 边框: border-gray-100
- Hover: bg-gray-50
- 表头: font-medium gray-700

### 操作按钮
- 尺寸: text-sm px-3 py-1.5
- 间距: gap-2
- 颜色: gray-700

---

## 图标使用

### 来源
Lucide React - 统一的线性图标库

### 尺寸规范
- 大图标: h-6 w-6 (24px)
- 标准: h-5 w-5 (20px)
- 小图标: h-4 w-4 (16px)
- 极小: h-3 w-3 (12px)

### 颜色
- 默认: text-gray-600
- Hover: text-gray-900
- 强调: text-white (黑色背景)

---

## 响应式设计

### 断点
```
sm:  640px
md:  768px
lg:  1024px
xl:  1280px
2xl: 1536px
```

### 适配规则
- 移动端: 单列布局
- 平板: 2列网格
- 桌面: 3列网格
- 字号: 移动端适当缩小

---

## 可访问性

### 对比度
- 主文字: 至少 7:1
- 次要文字: 至少 4.5:1

### Focus 状态
```css
focus:outline-none focus:ring-2 focus:ring-gray-400
```

### 语义化
- 使用正确的 HTML 标签
- 添加 aria-label
- 键盘导航支持

---

## 实施检查清单

### 每个新页面
- [ ] 使用统一的色彩系统
- [ ] 遵循字体层级规范
- [ ] 保持充足的留白空间
- [ ] 统一圆角和阴影
- [ ] 添加平滑过渡动画
- [ ] 确保响应式适配
- [ ] 测试可访问性

### 每个新组件
- [ ] 提取可复用样式
- [ ] 使用 TypeScript 类型
- [ ] 添加 Hover 状态
- [ ] 考虑 Loading 状态
- [ ] 考虑 Error 状态
- [ ] 添加适当注释

---

## 设计原则总结

1. **少即是多** - 删除不必要的元素
2. **留白为王** - 给内容呼吸空间
3. **层级清晰** - 用大小、颜色区分
4. **统一一致** - 保持全局一致性
5. **功能优先** - 美感服务于功能
6. **细节完美** - 关注微交互
7. **性能重要** - 优化加载体验

---

**最后更新**: 2025-10-15
**版本**: v1.0.0
