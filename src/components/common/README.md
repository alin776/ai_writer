# 通用组件库

本目录包含所有可复用的通用 UI 组件，使用 TypeScript 和 Tailwind CSS 构建。

## 组件列表

### 1. Button（按钮组件）

**文件路径：** `C:\Users\Administrator\Desktop\ai-writer\src\components\common\Button.tsx`

**功能特性：**
- 支持多种变体样式：`primary`, `secondary`, `danger`, `outline`, `ghost`
- 支持多种尺寸：`sm`, `md`, `lg`
- 支持 `loading` 状态（带旋转动画）
- 支持 `disabled` 状态
- 支持 `fullWidth` 完整宽度
- 完全支持原生 button 属性

**使用示例：**
```tsx
import { Button } from '@/components/common';

<Button variant="primary" size="md" onClick={handleClick}>
  点击我
</Button>

<Button variant="danger" loading disabled>
  加载中...
</Button>

<Button variant="outline" size="lg" fullWidth>
  完整宽度按钮
</Button>
```

---

### 2. Input（输入框组件）

**文件路径：** `C:\Users\Administrator\Desktop\ai-writer\src\components\common\Input.tsx`

**功能特性：**
- 支持多种输入类型：`text`, `email`, `password`, `number`, `tel`, `url`
- 支持错误提示和帮助文本
- 支持 `label` 和 `placeholder`
- 完整的受控组件实现
- 支持必填标识（红色星号）
- 使用 `forwardRef` 支持 ref 转发
- 自动生成唯一 ID 用于 label 关联
- 支持无障碍访问（ARIA 属性）

**使用示例：**
```tsx
import { Input } from '@/components/common';

<Input
  label="邮箱"
  type="email"
  placeholder="请输入邮箱"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={emailError}
  required
/>

<Input
  label="密码"
  type="password"
  helperText="密码至少 8 位字符"
  value={password}
  onChange={(e) => setPassword(e.target.value)}
/>
```

---

### 3. Modal（模态框组件）

**文件路径：** `C:\Users\Administrator\Desktop\ai-writer\src\components\common\Modal.tsx`

**功能特性：**
- 支持标题、内容、底部按钮区域
- 支持点击遮罩层关闭（可配置）
- 支持按 ESC 键关闭（可配置）
- 带淡入淡出和缩放动画效果
- 使用 React Portal 渲染到 body
- 支持多种尺寸：`sm`, `md`, `lg`, `xl`, `full`
- 自动管理 body 滚动锁定
- 支持关闭按钮显示/隐藏
- 自动聚焦管理

**使用示例：**
```tsx
import { Modal, Button } from '@/components/common';

<Modal
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  title="确认删除"
  size="md"
  footer={
    <>
      <Button variant="secondary" onClick={() => setIsOpen(false)}>
        取消
      </Button>
      <Button variant="danger" onClick={handleDelete}>
        删除
      </Button>
    </>
  }
>
  <p>确定要删除这个项目吗？此操作不可撤销。</p>
</Modal>
```

---

### 4. Loading（加载指示器）

**文件路径：** `C:\Users\Administrator\Desktop\ai-writer\src\components\common\Loading.tsx`

**功能特性：**
- 支持多种尺寸：`sm`, `md`, `lg`, `xl`
- 旋转动画效果
- 支持全屏遮罩模式
- 支持加载提示文本
- 支持多种颜色：`blue`, `white`, `gray`, `red`, `green`
- 内联和全屏两种显示模式

**使用示例：**
```tsx
import { Loading } from '@/components/common';

// 基础用法
<Loading size="md" />

// 全屏遮罩模式
<Loading fullscreen text="加载中，请稍候..." />

// 自定义颜色
<Loading color="white" size="lg" />

// 内联显示带文本
<Loading size="sm" text="处理中..." />
```

---

### 5. Toast（消息提示组件）

**文件路径：** `C:\Users\Administrator\Desktop\ai-writer\src\components\common\Toast.tsx`

**功能特性：**
- 支持四种类型：`success`, `error`, `warning`, `info`
- 自动消失（可配置时长，默认 3000ms）
- 使用 lucide-react 图标
- 与 globalStore 集成
- 支持多个 Toast 同时显示
- 使用 React Portal 渲染到 body
- 带滑入动画效果
- 支持手动关闭

**使用示例：**
```tsx
import { Toast } from '@/components/common';
import { useGlobalStore } from '@/store/globalStore';

// 在 App 组件中添加 Toast 容器
function App() {
  return (
    <>
      <Toast />
      <YourAppContent />
    </>
  );
}

// 在其他组件中调用
function YourComponent() {
  const { showToast } = useGlobalStore();

  const handleSuccess = () => {
    showToast('success', '操作成功！', 3000);
  };

  const handleError = () => {
    showToast('error', '操作失败，请重试', 5000);
  };

  // 或使用快捷方法
  const { success, error, warning, info } = useGlobalStore();
  success('保存成功！');
  error('网络错误');
  warning('注意：数据即将过期');
  info('系统将在 5 分钟后维护');
}
```

---

### 6. Card（卡片组件）

**文件路径：** `C:\Users\Administrator\Desktop\ai-writer\src\components\common\Card.tsx`

**功能特性：**
- 基础卡片容器
- 支持 hover 效果（悬停时阴影加深、上移）
- 支持多种阴影大小：`sm`, `md`, `lg`, `xl`, `none`
- 支持多种内边距：`none`, `sm`, `md`, `lg`, `xl`
- 支持多种圆角：`none`, `sm`, `md`, `lg`, `xl`, `full`
- 支持边框显示/隐藏
- 支持多种背景颜色：`white`, `gray`, `transparent`
- 支持点击事件
- 提供 `CardHeader`, `CardContent`, `CardFooter` 子组件

**使用示例：**
```tsx
import { Card, CardHeader, CardContent, CardFooter, Button } from '@/components/common';

// 基础用法
<Card hoverable shadow padding="lg">
  <h3>卡片标题</h3>
  <p>卡片内容...</p>
</Card>

// 使用子组件
<Card hoverable shadowSize="md" padding="none">
  <CardHeader className="p-4">
    <h3 className="text-lg font-semibold">用户信息</h3>
  </CardHeader>
  <CardContent className="p-4">
    <p>这里是卡片的主要内容区域</p>
  </CardContent>
  <CardFooter className="p-4">
    <Button variant="primary">保存</Button>
    <Button variant="secondary">取消</Button>
  </CardFooter>
</Card>

// 可点击卡片
<Card onClick={handleCardClick} hoverable>
  点击我
</Card>
```

---

## 导入方式

所有组件都可以通过统一的导出文件导入：

```tsx
import {
  Button,
  Input,
  Modal,
  Loading,
  Toast,
  Card,
  CardHeader,
  CardContent,
  CardFooter
} from '@/components/common';
```

或者单独导入：

```tsx
import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
```

---

## 类型定义

所有组件都提供了完整的 TypeScript 类型定义，可以导入使用：

```tsx
import type {
  ButtonProps,
  ButtonVariant,
  ButtonSize,
  InputProps,
  InputType,
  ModalProps,
  LoadingProps,
  LoadingSize,
  CardProps
} from '@/components/common';
```

---

## 样式说明

所有组件使用 Tailwind CSS 进行样式设计，并在 `C:\Users\Administrator\Desktop\ai-writer\src\styles\globals.css` 中定义了自定义动画：

- `animate-fadeIn` - 淡入动画（用于 Modal 遮罩）
- `animate-scaleIn` - 缩放动画（用于 Modal 内容）
- `animate-slideInRight` - 右侧滑入动画（用于 Toast）
- `animate-spin` - 旋转动画（用于 Loading 和 Button loading 状态）

---

## 设计原则

1. **类型安全**：所有组件使用 TypeScript 编写，提供完整的类型定义
2. **可访问性**：遵循 ARIA 规范，支持键盘导航和屏幕阅读器
3. **响应式**：适配各种屏幕尺寸
4. **可定制**：支持通过 props 和 className 自定义样式
5. **性能优化**：使用 React.memo、forwardRef 等优化技术
6. **用户体验**：流畅的动画效果和交互反馈

---

## 与项目集成

### Toast 集成

Toast 组件已与 `globalStore` 集成，需要在 App 根组件中添加 Toast 容器：

```tsx
import { Toast } from '@/components/common';

function App() {
  return (
    <>
      <Toast />
      {/* 其他应用内容 */}
    </>
  );
}
```

### Loading 集成

Loading 组件可以与 `globalStore` 的 `isLoading` 状态集成：

```tsx
import { Loading } from '@/components/common';
import { useGlobalStore } from '@/store/globalStore';

function App() {
  const { isLoading, loadingMessage } = useGlobalStore();

  return (
    <>
      {isLoading && <Loading fullscreen text={loadingMessage} />}
      {/* 其他应用内容 */}
    </>
  );
}
```

---

## 注意事项

1. **Modal 和 Toast** 使用了 React Portal，确保应用中有 `document.body` 可用
2. **Input** 组件使用 `forwardRef`，可以获取 input 元素的 ref
3. **Card** 组件的 `onClick` 会自动设置 `role="button"` 和 `tabIndex={0}`
4. 所有组件都支持通过 `className` 属性添加自定义样式

---

## 浏览器兼容性

- 现代浏览器（Chrome, Firefox, Safari, Edge）
- 需要支持 ES6+ 特性
- 需要支持 CSS3 动画和过渡效果

---

## 更新日志

### v1.0.0 (2025-10-15)
- 初始版本
- 创建 6 个基础通用组件
- 完整的 TypeScript 类型定义
- 与 globalStore 集成
- 完善的文档和示例
