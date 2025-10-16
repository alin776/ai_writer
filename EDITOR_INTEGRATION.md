# Novel 编辑器集成文档

## 集成完成时间
2025-10-15

## 集成方案

由于 novel-main 项目是基于 Next.js 的 monorepo，而我们的项目使用 React + Vite，直接使用 novel 包会有兼容性问题。因此采用了**基于 Tiptap 的自定义编辑器方案**。

## 已安装的依赖

### Tiptap 核心依赖
```json
{
  "@tiptap/react": "^2.11.2",
  "@tiptap/core": "^2.11.2",
  "@tiptap/starter-kit": "^2.11.2",
  "@tiptap/pm": "^2.11.2"
}
```

### Tiptap 扩展
```json
{
  "@tiptap/extension-placeholder": "^2.11.2",
  "@tiptap/extension-character-count": "^2.11.2",
  "@tiptap/extension-underline": "^2.11.2",
  "@tiptap/extension-code-block-lowlight": "^2.11.2",
  "@tiptap/extension-color": "^2.11.2",
  "@tiptap/extension-highlight": "^2.11.2",
  "@tiptap/extension-horizontal-rule": "^2.11.2",
  "@tiptap/extension-image": "^2.11.2",
  "@tiptap/extension-link": "^2.11.2",
  "@tiptap/extension-task-item": "^2.11.2",
  "@tiptap/extension-task-list": "^2.11.2",
  "@tiptap/extension-text-style": "^2.11.2",
  "@tiptap/suggestion": "^2.11.2"
}
```

### 辅助工具
```json
{
  "tippy.js": "^6.3.7",
  "lowlight": "^3.1.0",
  "highlight.js": "^11.9.0",
  "tiptap-markdown": "^0.8.10",
  "use-debounce": "^10.0.0",
  "@radix-ui/react-popover": "^1.0.7",
  "@radix-ui/react-separator": "^1.0.3",
  "cmdk": "^1.0.4"
}
```

## 创建的文件

### 1. NovelEditor.tsx
**路径**: `src/components/editor/NovelEditor.tsx`

**功能**:
- 基于 Tiptap 的富文本编辑器
- 支持多种文本格式（粗体、斜体、下划线、删除线、高亮等）
- 支持标题（H1-H6）
- 支持列表（有序、无序、任务列表）
- 支持链接和图片
- 字数和字符统计
- 自动保存功能（防抖 3 秒）
- LocalStorage 备份

**Props**:
```typescript
interface NovelEditorProps {
  content?: string;           // 初始内容
  onSave?: (content: string, json: any) => void; // 保存回调
  placeholder?: string;        // 占位符文本
  autoSave?: boolean;          // 是否自动保存
  autoSaveInterval?: number;   // 自动保存间隔（毫秒）
}
```

### 2. EditorToolbar.tsx
**路径**: `src/components/editor/EditorToolbar.tsx`

**功能**:
- 完整的编辑器工具栏
- 撤销/重做
- 文本格式化按钮
- 标题、列表、引用等
- 链接和图片插入
- 按钮激活状态高亮

### 3. editor-styles.css
**路径**: `src/components/editor/editor-styles.css`

**功能**:
- ProseMirror 编辑器样式
- 响应式设计
- 打印样式优化
- 任务列表样式
- 代码块语法高亮
- 图片、表格、链接等元素样式

## 集成到 EditorView

在 `src/views/EditorView/index.tsx` 中：

```tsx
import NovelEditor from '../../components/editor/NovelEditor';

// 使用编辑器
<NovelEditor
  content={content}
  onSave={(html, json) => {
    setContent(html);
    console.log('Editor JSON:', json);
  }}
  placeholder="开始写作..."
  autoSave={true}
  autoSaveInterval={3000}
/>
```

## 编辑器特性

### ✅ 已实现功能

1. **富文本编辑**
   - 粗体 (Ctrl+B)
   - 斜体 (Ctrl+I)
   - 下划线 (Ctrl+U)
   - 删除线
   - 高亮
   - 行内代码

2. **结构化内容**
   - 标题 (H1-H6)
   - 段落
   - 引用
   - 代码块
   - 水平分割线

3. **列表**
   - 无序列表
   - 有序列表
   - 任务列表（待办事项）

4. **媒体**
   - 链接插入
   - 图片插入
   - 图片显示优化

5. **编辑功能**
   - 撤销/重做
   - 字数统计
   - 字符统计
   - 自动保存
   - LocalStorage 备份

6. **用户体验**
   - 工具栏激活状态
   - 保存状态提示
   - 占位符提示
   - 快捷键支持

### ⏳ 待实现功能

1. **AI 集成**
   - AI 续写
   - AI 润色
   - AI 扩写
   - AI 缩写

2. **高级格式**
   - 表格
   - 数学公式 (KaTeX)
   - Mermaid 图表
   - 代码语法高亮（多语言）

3. **协作功能**
   - 实时协作编辑
   - 评论系统
   - 修改历史

4. **导入导出**
   - Markdown 导出
   - Word (DOCX) 导出
   - PDF 导出
   - 从其他格式导入

5. **图片上传**
   - 拖拽上传
   - 粘贴上传
   - 图片压缩
   - 云存储集成

## 使用说明

### 启动项目

```bash
cd C:\Users\Administrator\Desktop\ai-writer
npm run dev
```

项目将在 http://localhost:3000 启动

### 访问编辑器

1. 登录系统
2. 进入"我的作品"
3. 选择一个作品
4. 点击章节进入编辑器

### 工具栏快捷键

- `Ctrl+B` - 粗体
- `Ctrl+I` - 斜体
- `Ctrl+U` - 下划线
- `Ctrl+Z` - 撤销
- `Ctrl+Y` - 重做
- `Ctrl+Shift+X` - 删除线

## 自定义编辑器

### 添加新的扩展

在 `NovelEditor.tsx` 中的 `extensions` 数组添加：

```typescript
import { YourExtension } from '@tiptap/extension-your-extension';

const editor = useEditor({
  extensions: [
    // ... 现有扩展
    YourExtension.configure({
      // 配置选项
    }),
  ],
});
```

### 修改工具栏

编辑 `EditorToolbar.tsx`，添加新的按钮：

```tsx
<ToolbarButton
  onClick={() => editor.chain().focus().yourCommand().run()}
  isActive={editor.isActive('yourMark')}
  title="你的功能"
>
  <YourIcon className="w-4 h-4" />
</ToolbarButton>
```

### 调整样式

编辑 `editor-styles.css` 来自定义编辑器外观。

## 故障排查

### 问题1: 编辑器不显示

**解决方案**:
- 检查 Console 是否有错误
- 确认所有依赖已安装
- 清除浏览器缓存和 LocalStorage

### 问题2: 工具栏按钮无响应

**解决方案**:
- 确认 editor 实例已正确创建
- 检查 `editor.can()` 方法返回值
- 查看是否有权限限制

### 问题3: 自动保存不工作

**解决方案**:
- 确认 `autoSave={true}` 已设置
- 检查 `onSave` 回调是否正确
- 查看 Console 是否有保存错误

## 性能优化建议

1. **大文档处理**
   - 对于超过 100,000 字的文档，考虑分章节加载
   - 使用虚拟滚动

2. **自动保存优化**
   - 调整防抖间隔（默认 3000ms）
   - 只在内容真正改变时保存

3. **图片优化**
   - 实现图片懒加载
   - 压缩图片尺寸
   - 使用 CDN 加速

## 下一步计划

1. **AI 功能集成** (优先级: 高)
   - 集成 OpenAI API
   - 实现 AI 续写功能
   - 添加 AI 提示词管理

2. **高级编辑功能** (优先级: 中)
   - 表格编辑
   - 数学公式
   - 代码语法高亮

3. **协作功能** (优先级: 低)
   - WebSocket 实时同步
   - 评论和批注
   - 修改历史追踪

## 参考资源

- [Tiptap 官方文档](https://tiptap.dev/)
- [Novel 项目](https://github.com/steven-tey/novel)
- [ProseMirror 文档](https://prosemirror.net/)

## 技术支持

如有问题，请查看:
1. 项目 `todo2.md` - 完整的开发任务清单
2. Tiptap 官方文档
3. GitHub Issues

---

**最后更新**: 2025-10-15
**版本**: 1.0.0
**状态**: ✅ 可用
