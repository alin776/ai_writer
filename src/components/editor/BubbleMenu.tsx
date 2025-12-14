/**
 * 气泡菜单 - 选中文本时显示的浮动工具栏
 */
import React, { useState, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { BubbleMenu as TiptapBubbleMenu } from '@tiptap/react/menus';
import { Editor } from '@tiptap/core';
import {
  Bold,
  Italic,
  Underline as UnderlineIcon,
  Strikethrough,
  Code,
  Highlighter,
  Link as LinkIcon,
  Unlink,
  Sparkles,
} from 'lucide-react';

interface BubbleMenuProps {
  editor: Editor;
  onOpenInlineAI?: () => void;
}

/**
 * 气泡菜单组件
 */
const BubbleMenu: React.FC<BubbleMenuProps> = ({ editor, onOpenInlineAI }) => {
  const { t } = useTranslation();

  if (!editor) {
    return null;
  }

  /**
   * 打开浮动 AI 输入框
   */
  const handleAskAI = useCallback(() => {
    if (onOpenInlineAI) {
      onOpenInlineAI();
    }
  }, [onOpenInlineAI]);

  /**
   * 设置链接
   */
  const setLink = () => {
    const previousUrl = editor.getAttributes('link').href;
    const url = window.prompt(t('editor.toolbar.enterLinkUrl'), previousUrl);

    if (url === null) {
      return;
    }

    if (url === '') {
      editor.chain().focus().extendMarkRange('link').unsetLink().run();
      return;
    }

    editor.chain().focus().extendMarkRange('link').setLink({ href: url }).run();
  };

  /**
   * 移除链接
   */
  const unsetLink = () => {
    editor.chain().focus().unsetLink().run();
  };

  const BubbleButton: React.FC<{
    onClick: () => void;
    isActive?: boolean;
    children: React.ReactNode;
    title: string;
  }> = ({ onClick, isActive, children, title }) => (
    <button
      onClick={onClick}
      className={`bubble-menu-button ${isActive ? 'active' : ''}`}
      title={title}
      type="button"
    >
      {children}
    </button>
  );

  return (
    <TiptapBubbleMenu
      editor={editor}
      className="bubble-menu-container"
    >
      {/* Ask AI 按钮 */}
      <button
        onClick={handleAskAI}
        className="bubble-menu-button ai-button"
        title="Ask AI"
        type="button"
      >
        <Sparkles className="w-4 h-4 text-purple-500" />
        <span className="ml-1 text-sm text-purple-500 font-medium">Ask AI</span>
      </button>

      {/* 分隔符 */}
      <div className="bubble-menu-separator" />

      {/* 文本样式 */}
      <div className="bubble-menu-group">
        <BubbleButton
          onClick={() => editor.chain().focus().toggleBold().run()}
          isActive={editor.isActive('bold')}
          title={`${t('editor.toolbar.bold')} (Ctrl+B)`}
        >
          <Bold className="w-4 h-4" />
        </BubbleButton>

        <BubbleButton
          onClick={() => editor.chain().focus().toggleItalic().run()}
          isActive={editor.isActive('italic')}
          title={`${t('editor.toolbar.italic')} (Ctrl+I)`}
        >
          <Italic className="w-4 h-4" />
        </BubbleButton>

        <BubbleButton
          onClick={() => editor.chain().focus().toggleUnderline().run()}
          isActive={editor.isActive('underline')}
          title={`${t('editor.toolbar.underline')} (Ctrl+U)`}
        >
          <UnderlineIcon className="w-4 h-4" />
        </BubbleButton>

        <BubbleButton
          onClick={() => editor.chain().focus().toggleStrike().run()}
          isActive={editor.isActive('strike')}
          title={t('editor.toolbar.strikethrough')}
        >
          <Strikethrough className="w-4 h-4" />
        </BubbleButton>
      </div>

      {/* 分隔符 */}
      <div className="bubble-menu-separator" />

      {/* 高亮和代码 */}
      <div className="bubble-menu-group">
        <BubbleButton
          onClick={() => editor.chain().focus().toggleHighlight().run()}
          isActive={editor.isActive('highlight')}
          title={t('editor.toolbar.highlight')}
        >
          <Highlighter className="w-4 h-4" />
        </BubbleButton>

        <BubbleButton
          onClick={() => editor.chain().focus().toggleCode().run()}
          isActive={editor.isActive('code')}
          title={t('editor.toolbar.inlineCode')}
        >
          <Code className="w-4 h-4" />
        </BubbleButton>
      </div>

      {/* 分隔符 */}
      <div className="bubble-menu-separator" />

      {/* 链接 */}
      <div className="bubble-menu-group">
        {editor.isActive('link') ? (
          <BubbleButton onClick={unsetLink} title={t('editor.toolbar.removeLink')}>
            <Unlink className="w-4 h-4" />
          </BubbleButton>
        ) : (
          <BubbleButton onClick={setLink} title={t('editor.toolbar.insertLink')}>
            <LinkIcon className="w-4 h-4" />
          </BubbleButton>
        )}
      </div>
    </TiptapBubbleMenu>
  );
};

export default BubbleMenu;
