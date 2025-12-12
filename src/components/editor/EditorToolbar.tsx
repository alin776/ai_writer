/**
 * 编辑器工具栏组件
 */
import React from 'react';
import { Editor } from '@tiptap/react';
import {
  Bold,
  Italic,
  Strikethrough,
  Code,
  Heading1,
  Heading2,
  Heading3,
  List,
  ListOrdered,
  Quote,
  Undo,
  Redo,
  Link as LinkIcon,
  Image as ImageIcon,
  Highlighter,
  Underline as UnderlineIcon,
  CheckSquare,
  FileCode,
  Minus,
  Wand2,
} from 'lucide-react';

interface EditorToolbarProps {
  editor: Editor;
  aiAutoCompleteEnabled?: boolean;
  onToggleAIAutoComplete?: () => void;
}

const EditorToolbar: React.FC<EditorToolbarProps> = ({
  editor,
  aiAutoCompleteEnabled = false,
  onToggleAIAutoComplete,
}) => {
  if (!editor) {
    return null;
  }

  /**
   * 工具栏按钮组件
   */
  const ToolbarButton: React.FC<{
    onClick: () => void;
    isActive?: boolean;
    disabled?: boolean;
    children: React.ReactNode;
    title: string;
  }> = ({ onClick, isActive, disabled, children, title }) => (
    <button
      type="button"
      onMouseDown={(e) => {
        e.preventDefault(); // 阻止按钮获取焦点，保持编辑器选区
      }}
      onClick={onClick}
      disabled={disabled}
      title={title}
      className={`h-7 w-7 p-0 flex items-center justify-center rounded transition-all ${
        isActive
          ? 'bg-zinc-100 text-zinc-900 dark:bg-slate-700 dark:text-slate-100'
          : 'text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-700'
      } ${disabled ? 'opacity-30 cursor-not-allowed' : 'cursor-pointer'}`}
    >
      {children}
    </button>
  );

  /**
   * 添加链接
   */
  const setLink = () => {
    const previousUrl = editor.getAttributes('link').href;
    const url = window.prompt('请输入链接地址:', previousUrl);

    // 取消
    if (url === null) {
      return;
    }

    // 清空
    if (url === '') {
      editor.chain().focus().extendMarkRange('link').unsetLink().run();
      return;
    }

    // 设置链接
    editor.chain().focus().extendMarkRange('link').setLink({ href: url }).run();
  };

  /**
   * 添加图片
   */
  const addImage = () => {
    const url = window.prompt('请输入图片地址:');

    if (url) {
      editor.chain().focus().setImage({ src: url }).run();
    }
  };

  return (
    <div className="px-3 py-1.5 flex items-center gap-1.5 border-b border-zinc-100 bg-white shadow-sm shadow-zinc-100/50 dark:bg-slate-900 dark:border-slate-700 dark:shadow-none">
      {/* AI 自动补全 + 撤销/重做 */}
      <div className="flex items-center gap-0.5">
        <ToolbarButton
          onClick={() => onToggleAIAutoComplete?.()}
          isActive={aiAutoCompleteEnabled}
          title={aiAutoCompleteEnabled ? 'AI 自动补全已开启（点击关闭）' : 'AI 自动补全已关闭（点击开启）'}
        >
          <Wand2 className="h-3.5 w-3.5" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().undo().run()}
          disabled={!editor.can().undo()}
          title="撤销 (Ctrl+Z)"
        >
          <Undo className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().redo().run()}
          disabled={!editor.can().redo()}
          title="重做 (Ctrl+Y)"
        >
          <Redo className="h-3 w-3" />
        </ToolbarButton>
      </div>

      <div className="w-px h-4 bg-zinc-200 dark:bg-slate-600" />

      {/* 标题 */}
      <div className="flex items-center">
        <button
          type="button"
          onMouseDown={(e) => e.preventDefault()}
          onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}
          className={`h-7 px-2 text-[11px] rounded transition-all ${
            editor.isActive('heading', { level: 1 })
              ? 'bg-zinc-100 text-zinc-900 dark:bg-slate-700 dark:text-slate-100'
              : 'text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-700'
          }`}
          title="一级标题"
        >
          H1
        </button>
        <button
          type="button"
          onMouseDown={(e) => e.preventDefault()}
          onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
          className={`h-7 px-2 text-[11px] rounded transition-all ${
            editor.isActive('heading', { level: 2 })
              ? 'bg-zinc-100 text-zinc-900 dark:bg-slate-700 dark:text-slate-100'
              : 'text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-700'
          }`}
          title="二级标题"
        >
          H2
        </button>
        <button
          type="button"
          onMouseDown={(e) => e.preventDefault()}
          onClick={() => editor.chain().focus().toggleHeading({ level: 3 }).run()}
          className={`h-7 px-2 text-[11px] rounded transition-all ${
            editor.isActive('heading', { level: 3 })
              ? 'bg-zinc-100 text-zinc-900 dark:bg-slate-700 dark:text-slate-100'
              : 'text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-700'
          }`}
          title="三级标题"
        >
          H3
        </button>
      </div>

      <div className="w-px h-4 bg-zinc-200 dark:bg-slate-600" />

      {/* 文本样式 */}
      <div className="flex items-center">
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleBold().run()}
          isActive={editor.isActive('bold')}
          title="粗体 (Ctrl+B)"
        >
          <Bold className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleItalic().run()}
          isActive={editor.isActive('italic')}
          title="斜体 (Ctrl+I)"
        >
          <Italic className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleUnderline().run()}
          isActive={editor.isActive('underline')}
          title="下划线 (Ctrl+U)"
        >
          <UnderlineIcon className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleStrike().run()}
          isActive={editor.isActive('strike')}
          title="删除线"
        >
          <Strikethrough className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleHighlight().run()}
          isActive={editor.isActive('highlight')}
          title="高亮"
        >
          <Highlighter className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleCode().run()}
          isActive={editor.isActive('code')}
          title="行内代码"
        >
          <Code className="h-3 w-3" />
        </ToolbarButton>
      </div>

      <div className="w-px h-4 bg-zinc-200 dark:bg-slate-600" />

      {/* 列表 */}
      <div className="flex items-center">
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleBulletList().run()}
          isActive={editor.isActive('bulletList')}
          title="无序列表"
        >
          <List className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleOrderedList().run()}
          isActive={editor.isActive('orderedList')}
          title="有序列表"
        >
          <ListOrdered className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleTaskList().run()}
          isActive={editor.isActive('taskList')}
          title="任务列表"
        >
          <CheckSquare className="h-3 w-3" />
        </ToolbarButton>
      </div>

      <div className="w-px h-4 bg-zinc-200 dark:bg-slate-600" />

      {/* 引用和代码块 */}
      <div className="flex items-center">
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleBlockquote().run()}
          isActive={editor.isActive('blockquote')}
          title="引用"
        >
          <Quote className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().toggleCodeBlock().run()}
          isActive={editor.isActive('codeBlock')}
          title="代码块"
        >
          <FileCode className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().setHorizontalRule().run()}
          title="水平分割线"
        >
          <Minus className="h-3 w-3" />
        </ToolbarButton>
      </div>

      <div className="w-px h-4 bg-zinc-200 dark:bg-slate-600" />

      {/* 链接和图片 */}
      <div className="flex items-center">
        <ToolbarButton
          onClick={setLink}
          isActive={editor.isActive('link')}
          title="插入链接"
        >
          <LinkIcon className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton onClick={addImage} title="插入图片">
          <ImageIcon className="h-3 w-3" />
        </ToolbarButton>
      </div>
    </div>
  );
};

export default EditorToolbar;
