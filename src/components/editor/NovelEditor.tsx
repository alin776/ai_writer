/**
 * Novel 编辑器组件
 * 基于 Tiptap 的富文本编辑器
 */
import React, { useEffect, useState } from 'react';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Placeholder from '@tiptap/extension-placeholder';
import CharacterCount from '@tiptap/extension-character-count';
// 注意：StarterKit 3.7.0+ 已包含 Link 和 Underline，不要重复导入
import Image from '@tiptap/extension-image';
import HorizontalRule from '@tiptap/extension-horizontal-rule';
import { TextStyle } from '@tiptap/extension-text-style';
import { Color } from '@tiptap/extension-color';
import Highlight from '@tiptap/extension-highlight';
import TaskList from '@tiptap/extension-task-list';
import TaskItem from '@tiptap/extension-task-item';
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight';
import { Markdown } from 'tiptap-markdown';
import { common, createLowlight } from 'lowlight';
import { useDebouncedCallback } from 'use-debounce';
import GlobalDragHandle from 'tiptap-extension-global-drag-handle';
import BubbleMenuExtension from '@tiptap/extension-bubble-menu';
import EditorToolbar from './EditorToolbar';
import BubbleMenu from './BubbleMenu';
import AIMenu from './AIMenu';
import { SlashCommand } from './SlashCommandExtension';
import { AIHighlight } from './AIHighlightExtension';
import { AIAutoCompleteExtension } from './AIAutoCompleteExtension';
import { ToastContainer } from '@/components/ui/Toast';
import { useToast } from '@/hooks/useToast';
import AIService from '@/services/AIService';
import { getEditorWordCount, countCharactersInHtml } from '@/utils/wordCount';
import './editor-styles.css';
import './interactive-styles.css';
import './sidebar-styles.css';

interface NovelEditorProps {
  content?: string;
  onSave?: (content: string, json: any) => void;
  placeholder?: string;
  autoSave?: boolean;
  autoSaveInterval?: number;
}

/**
 * Novel 编辑器组件
 */
const NovelEditor: React.FC<NovelEditorProps> = ({
  content = '',
  onSave,
  placeholder = '开始写作...',
  autoSave = true,
  autoSaveInterval = 3000,
}) => {
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'unsaved'>('saved');
  const [wordCount, setWordCount] = useState(0);
  const toast = useToast();

  // 初始化编辑器
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        heading: {
          levels: [1, 2, 3, 4, 5, 6],
        },
        codeBlock: false, // 禁用默认代码块，使用 CodeBlockLowlight
        horizontalRule: false, // 禁用默认水平线，稍后单独引入
        // Link 和 Underline 在 StarterKit 3.7.0+ 中已包含，无需单独引入
        link: {
          openOnClick: false,
          HTMLAttributes: {
            class: 'text-blue-600 hover:text-blue-800 underline cursor-pointer',
          },
        },
        // underline: true, // 启用下划线（StarterKit 3.7.0+ 已包含）
      }),
      // 水平分割线（单独引入以便自定义）
      HorizontalRule,
      // 代码块语法高亮
      CodeBlockLowlight.configure({
        lowlight: createLowlight(common),
        HTMLAttributes: {
          class: 'code-block-wrapper',
        },
      }),
      // Markdown 支持
      Markdown.configure({
        html: true,
        transformPastedText: true,
        transformCopiedText: false,
      }),
      Placeholder.configure({
        placeholder,
        emptyEditorClass: 'is-editor-empty',
      }),
      CharacterCount,
      // Link 和 Underline 已在 StarterKit 中配置，无需重复
      Image.configure({
        HTMLAttributes: {
          class: 'rounded-lg max-w-full h-auto',
        },
      }),
      TextStyle,
      Color,
      Highlight.configure({
        multicolor: true,
      }),
      TaskList.configure({
        HTMLAttributes: {
          class: 'task-list',
        },
      }),
      TaskItem.configure({
        nested: true,
        HTMLAttributes: {
          class: 'task-item',
        },
      }),
      // Slash 命令
      SlashCommand,
      // 拖拽手柄
      GlobalDragHandle.configure({
        dragHandleWidth: 24,
      }),
      // 气泡菜单扩展
      BubbleMenuExtension,
      // AI 高亮扩展
      AIHighlight,
      // AI 自动补全扩展
      AIAutoCompleteExtension.configure({
        delay: 3000, // 3秒延迟
        enabled: true,
        onTrigger: async (text: string) => {
          try {
            // 调用快速补全 API
            const suggestion = await AIService.quickComplete(text);
            return suggestion;
          } catch (error) {
            console.error('自动补全失败:', error);
            return '';
          }
        },
      }),
    ],
    content: content || '<p></p>',
    editorProps: {
      attributes: {
        class:
          'prose prose-lg dark:prose-invert max-w-[900px] mx-auto focus:outline-none min-h-screen px-16 py-12',
      },
    },
    onUpdate: ({ editor }) => {
      setSaveStatus('unsaved');
      // 使用自定义字数统计（与后端一致）
      setWordCount(getEditorWordCount(editor));

      if (autoSave) {
        debouncedSave(editor);
      }
    },
  });

  // 防抖保存函数
  const debouncedSave = useDebouncedCallback(
    (editor) => {
      setSaveStatus('saving');
      const html = editor.getHTML();
      const json = editor.getJSON();

      // 保存到 localStorage（作为备份）
      localStorage.setItem('novel-editor-content', html);
      localStorage.setItem('novel-editor-json', JSON.stringify(json));

      // 调用外部保存回调
      if (onSave) {
        onSave(html, json);
      }

      // 延迟显示已保存状态
      setTimeout(() => {
        setSaveStatus('saved');
      }, 500);
    },
    autoSaveInterval
  );

  // 当 content prop 变化时更新编辑器内容
  useEffect(() => {
    if (editor && content !== undefined) {
      const currentContent = editor.getHTML();
      // 只有当内容真的不同时才更新，避免不必要的重新渲染
      if (currentContent !== content) {
        console.log('[NovelEditor] 更新编辑器内容:', {
          contentLength: content?.length || 0,
          contentPreview: content?.substring(0, 50) + '...',
        });
        editor.commands.setContent(content || '<p></p>');
      }
    }
  }, [editor, content]);

  // 从 localStorage 恢复内容（仅在初始化且没有传入 content 时）
  useEffect(() => {
    if (!content && editor) {
      const savedContent = localStorage.getItem('novel-editor-content');
      if (savedContent && savedContent !== '<p></p>') {
        editor.commands.setContent(savedContent);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 组件卸载时保存
  useEffect(() => {
    return () => {
      if (editor && autoSave) {
        const html = editor.getHTML();
        const json = editor.getJSON();
        localStorage.setItem('novel-editor-content', html);
        localStorage.setItem('novel-editor-json', JSON.stringify(json));
        if (onSave) {
          onSave(html, json);
        }
      }
    };
  }, [editor, autoSave, onSave]);

  if (!editor) {
    return (
      <div className="flex items-center justify-center min-h-[500px]">
        <div className="text-gray-500">加载编辑器...</div>
      </div>
    );
  }

  return (
    <>
      {/* Toast 通知容器 */}
      <ToastContainer messages={toast.messages} onClose={toast.close} />

      <div className="novel-editor w-full h-full flex flex-col bg-white">
        {/* 顶部工具栏 */}
        <EditorToolbar editor={editor} />

        {/* 状态栏 - 极简设计 */}
        <div className="flex items-center justify-between px-6 py-3 bg-white border-b border-gray-100">
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <span className="font-medium">字数:</span>
              <span>{wordCount}</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="font-medium">字符:</span>
              <span>{countCharactersInHtml(editor.getHTML())}</span>
            </div>
          </div>

          {/* 保存状态 */}
          <div className="flex items-center space-x-2">
            {saveStatus === 'saved' && (
              <div className="flex items-center space-x-1 text-green-600">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm">已保存</span>
              </div>
            )}
            {saveStatus === 'saving' && (
              <div className="flex items-center space-x-1 text-blue-600">
                <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                <span className="text-sm">保存中...</span>
              </div>
            )}
            {saveStatus === 'unsaved' && (
              <div className="flex items-center space-x-1 text-orange-600">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span className="text-sm">未保存</span>
              </div>
            )}
          </div>
        </div>

        {/* 编辑器内容区域 - 沉浸式画布 */}
        <div className="flex-1 overflow-y-auto bg-white">
          <EditorContent editor={editor} className="editor-canvas" />
          {/* 气泡菜单 - 选中文本时显示 */}
          <BubbleMenu editor={editor} />
          {/* AI 菜单 - 选中文本时显示 AI 操作 */}
          <AIMenu editor={editor} />
        </div>
      </div>
    </>
  );
};

export default NovelEditor;
