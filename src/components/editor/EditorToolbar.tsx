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
}

const EditorToolbar: React.FC<EditorToolbarProps> = ({ editor }) => {
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
      onClick={onClick}
      disabled={disabled}
      title={title}
      className={`p-2 rounded-md hover:bg-gray-50 transition-all duration-150 ${
        isActive ? 'bg-gray-100 text-gray-900' : 'text-gray-600'
      } ${disabled ? 'opacity-30 cursor-not-allowed' : 'cursor-pointer hover:text-gray-900'}`}
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
    <div className="editor-toolbar border-b border-gray-100 bg-white sticky top-0 z-10 shadow-sm">
      <div className="flex flex-wrap items-center gap-2 px-6 py-3">
        {/* 撤销/重做 */}
        <div className="flex items-center gap-1 pr-3 mr-1 border-r border-gray-200">
          <ToolbarButton
            onClick={() => editor.chain().focus().undo().run()}
            disabled={!editor.can().undo()}
            title="撤销 (Ctrl+Z)"
          >
            <Undo className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().redo().run()}
            disabled={!editor.can().redo()}
            title="重做 (Ctrl+Y)"
          >
            <Redo className="w-4 h-4" />
          </ToolbarButton>
        </div>

        {/* 标题 */}
        <div className="flex items-center gap-1 pr-3 mr-1 border-r border-gray-200">
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}
            isActive={editor.isActive('heading', { level: 1 })}
            title="一级标题"
          >
            <Heading1 className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
            isActive={editor.isActive('heading', { level: 2 })}
            title="二级标题"
          >
            <Heading2 className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleHeading({ level: 3 }).run()}
            isActive={editor.isActive('heading', { level: 3 })}
            title="三级标题"
          >
            <Heading3 className="w-4 h-4" />
          </ToolbarButton>
        </div>

        {/* 文本样式 */}
        <div className="flex items-center gap-1 pr-3 mr-1 border-r border-gray-200">
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleBold().run()}
            isActive={editor.isActive('bold')}
            title="粗体 (Ctrl+B)"
          >
            <Bold className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleItalic().run()}
            isActive={editor.isActive('italic')}
            title="斜体 (Ctrl+I)"
          >
            <Italic className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleUnderline().run()}
            isActive={editor.isActive('underline')}
            title="下划线 (Ctrl+U)"
          >
            <UnderlineIcon className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleStrike().run()}
            isActive={editor.isActive('strike')}
            title="删除线"
          >
            <Strikethrough className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleHighlight().run()}
            isActive={editor.isActive('highlight')}
            title="高亮"
          >
            <Highlighter className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleCode().run()}
            isActive={editor.isActive('code')}
            title="行内代码"
          >
            <Code className="w-4 h-4" />
          </ToolbarButton>
        </div>

        {/* 列表 */}
        <div className="flex items-center gap-1 pr-3 mr-1 border-r border-gray-200">
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleBulletList().run()}
            isActive={editor.isActive('bulletList')}
            title="无序列表"
          >
            <List className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleOrderedList().run()}
            isActive={editor.isActive('orderedList')}
            title="有序列表"
          >
            <ListOrdered className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleTaskList().run()}
            isActive={editor.isActive('taskList')}
            title="任务列表"
          >
            <CheckSquare className="w-4 h-4" />
          </ToolbarButton>
        </div>

        {/* 引用和代码块 */}
        <div className="flex items-center gap-1 pr-3 mr-1 border-r border-gray-200">
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleBlockquote().run()}
            isActive={editor.isActive('blockquote')}
            title="引用"
          >
            <Quote className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleCodeBlock().run()}
            isActive={editor.isActive('codeBlock')}
            title="代码块"
          >
            <FileCode className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton
            onClick={() => editor.chain().focus().setHorizontalRule().run()}
            title="水平分割线"
          >
            <Minus className="w-4 h-4" />
          </ToolbarButton>
        </div>

        {/* 链接和图片 */}
        <div className="flex items-center gap-1 pr-3 mr-1 border-r border-gray-200">
          <ToolbarButton
            onClick={setLink}
            isActive={editor.isActive('link')}
            title="插入链接"
          >
            <LinkIcon className="w-4 h-4" />
          </ToolbarButton>
          <ToolbarButton onClick={addImage} title="插入图片">
            <ImageIcon className="w-4 h-4" />
          </ToolbarButton>
        </div>

        {/* AI 功能 */}
        <div className="flex items-center gap-1 ml-auto">
          <button
            onClick={() => {
              const event = new CustomEvent('ai-continue', {
                detail: { editor },
              });
              window.dispatchEvent(event);
            }}
            className="px-4 py-2 rounded-md bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white text-sm font-medium transition-all flex items-center gap-2 shadow-sm"
            title="AI 续写"
          >
            <Wand2 className="w-4 h-4" />
            <span>AI 续写</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default EditorToolbar;
