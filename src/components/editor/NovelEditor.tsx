/**
 * Novel 编辑器组件
 * 基于 Tiptap 的富文本编辑器
 */
import React, { useEffect, useState } from 'react';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Placeholder from '@tiptap/extension-placeholder';
import CharacterCount from '@tiptap/extension-character-count';
import Underline from '@tiptap/extension-underline';
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
import editorSyncService, { EditorUpdateEvent } from '@/services/EditorSyncService';
import { AgentEditConfirmDialog } from '@/components/agent';
import './editor-styles.css';
import './interactive-styles.css';
import './sidebar-styles.css';

interface NovelEditorProps {
  content?: string;
  onSave?: (content: string, json: any) => void;
  placeholder?: string;
  autoSave?: boolean;
  autoSaveInterval?: number;
  // ===== Context-Aware 元数据 =====
  workId?: string;
  chapterId?: string;
  // ===== AI 自动补全开关 =====
  aiAutoCompleteEnabled?: boolean;
  onToggleAIAutoComplete?: () => void;
}

type AgentActionType = 'edit' | 'rewrite' | 'insert';

type AgentApprovalRequest = {
  request_id: string;
  action_type: AgentActionType;
  operation?: string;
  original_content?: string;
  new_content?: string;
  description?: string;
  versions?: Array<{
    version_id: string;
    style?: string;
    style_name: string;
    content?: string;
  }>;
};

/**
 * Novel 编辑器组件
 */
const NovelEditor: React.FC<NovelEditorProps> = ({
  content = '',
  onSave,
  placeholder = '开始写作...',
  autoSave = true,
  autoSaveInterval = 3000,
  workId,      // Context-Aware 参数
  chapterId,   // Context-Aware 参数
  aiAutoCompleteEnabled = false, // 默认关闭，避免意外消耗积分
  onToggleAIAutoComplete,
}) => {
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'unsaved'>('saved');
  const [wordCount, setWordCount] = useState(0);
  const toast = useToast();

  // 🆕 Agent 编辑确认对话框状态
  const [confirmDialog, setConfirmDialog] = useState<{
    isOpen: boolean;
    approvalRequest: AgentApprovalRequest;
    onApprove: (selectedVersion?: number) => void;
    onReject: () => void;
  }>({
    isOpen: false,
    approvalRequest: {
      request_id: 'agent-edit-request',
      action_type: 'edit',
      new_content: '',
    },
    onApprove: () => {},
    onReject: () => {}
  });

  // 初始化编辑器
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        heading: {
          levels: [1, 2, 3, 4, 5, 6],
        },
        codeBlock: false, // 禁用默认代码块，使用 CodeBlockLowlight
        horizontalRule: false, // 禁用默认水平线，稍后单独引入
      }),
      // 水平分割线（单独引入以便自定义）
      HorizontalRule,
      // 下划线（显式添加） - 暂时注释测试
      // Underline,
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
      // AI 自动补全扩展（流式版本）
      AIAutoCompleteExtension.configure({
        delay: 2000, // 2秒延迟，快速响应
        minChars: 50, // 至少50个字符才触发
        enabled: aiAutoCompleteEnabled, // 由用户偏好控制
        onTrigger: async (text: string, onChunk: (chunk: string, fullText: string) => void) => {
          try {
            // 使用流式补全，边生成边显示
            const suggestion = await AIService.quickCompleteStream(
              text,
              onChunk,
              workId,      // 作品ID
              chapterId    // 章节ID
            );
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
          'novel-editor-content w-full focus:outline-none min-h-screen px-8 py-8',
        style: 'font-kerning: none !important; font-feature-settings: "kern" 0, "liga" 0, "calt" 0, "palt" 0, "halt" 0 !important; letter-spacing: 0 !important;',
      },
      // 处理粘贴的HTML，去除所有样式，只保留基本结构
      transformPastedHTML(html) {
        // 创建一个临时div来解析HTML
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;

        // 递归清理所有节点的样式属性
        const cleanNode = (node: Node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            const element = node as HTMLElement;
            // 移除所有样式属性
            element.removeAttribute('style');
            element.removeAttribute('class');
            element.removeAttribute('color');
            element.removeAttribute('face');
            element.removeAttribute('size');

            // 递归处理子节点
            Array.from(element.childNodes).forEach(cleanNode);
          }
        };

        cleanNode(tempDiv);
        return tempDiv.innerHTML;
      },
      // 处理粘贴的纯文本
      transformPastedText(text) {
        // 保持换行，将纯文本转换为段落
        return text;
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

  // ===== 预加载元数据（降低首次自动补全延迟） =====
  useEffect(() => {
    if (workId && chapterId) {
      console.log('[NovelEditor] 预加载章节元数据:', { workId, chapterId });
      AIService.preloadMetadata(workId, chapterId);
    }
  }, [workId, chapterId]);

  // ===== 动态更新 AI 自动补全开关状态 =====
  useEffect(() => {
    if (editor && editor.storage.aiAutoComplete) {
      editor.storage.aiAutoComplete.enabled = aiAutoCompleteEnabled;
      console.log('[NovelEditor] AI 自动补全状态更新:', aiAutoCompleteEnabled);
    }
  }, [editor, aiAutoCompleteEnabled]);

  // 🆕 订阅 EditorSyncService 的章节更新事件
  useEffect(() => {
    if (!editor || !chapterId) return;

    console.log('[NovelEditor] 订阅 EditorSyncService 事件:', chapterId);

    // 订阅章节更新事件
    const unsubscribe = editorSyncService.onUpdate((event: EditorUpdateEvent) => {
      // 只处理当前章节的更新
      if (event.chapterId !== chapterId) return;

      // 忽略来自用户的更新（避免循环）
      if (event.source === 'user') return;

      console.log('[NovelEditor] 收到 Agent 更新事件:', event);

      // 如果需要用户确认，显示确认对话框
      if (event.source === 'agent') {
        const currentContent = editor.getHTML();
        const actionType: AgentActionType = event.operation === 'append' ? 'edit' :
          event.operation === 'replace' ? 'rewrite' : 'insert';

        setConfirmDialog({
          isOpen: true,
          approvalRequest: {
            request_id: `agent-${chapterId || 'chapter'}-${Date.now()}`,
            action_type: actionType,
            operation: event.operation,
            original_content: currentContent,
            new_content: event.content,
            description: `Agent 建议${
              event.operation === 'append' ? '续写' :
              event.operation === 'replace' ? '改写' : '插入'
            }内容`,
          },
          onApprove: (selectedVersion?: number) => {
            // 用户确认，应用更新
            console.log('[NovelEditor] 用户确认 Agent 编辑');

            // 应用内容更新
            if (event.operation === 'append') {
              // 续写：追加到末尾
              const currentHtml = editor.getHTML();
              editor.commands.setContent(currentHtml + event.content);
            } else if (event.operation === 'replace') {
              // 改写：替换全部内容
              editor.commands.setContent(event.content);
            } else if (event.operation === 'insert' && event.position) {
              // 插入：在指定位置插入
              editor.commands.insertContentAt(event.position.start, event.content);
            }

            // 触发保存
            setSaveStatus('unsaved');
            if (autoSave) {
              debouncedSave(editor);
            }

            // 关闭对话框
            setConfirmDialog(prev => ({ ...prev, isOpen: false }));

            // 显示成功提示
            toast.success('已应用 AI 编辑');
          },
          onReject: () => {
            // 用户取消，不做任何操作
            console.log('[NovelEditor] 用户取消 Agent 编辑');
            setConfirmDialog(prev => ({ ...prev, isOpen: false }));
            toast.info('已取消 AI 编辑');
          }
        });
      }
    });

    // 订阅同步错误事件
    const unsubscribeError = editorSyncService.onSyncError((data) => {
      if (data.chapterId === chapterId) {
        console.error('[NovelEditor] 同步失败:', data.error);
        toast.error('内容同步失败，请稍后重试');
      }
    });

    // 订阅同步成功事件
    const unsubscribeSuccess = editorSyncService.onSyncSuccess((data) => {
      if (data.chapterId === chapterId) {
        console.log('[NovelEditor] 同步成功');
      }
    });

    return () => {
      unsubscribe();
      unsubscribeError();
      unsubscribeSuccess();
    };
  }, [editor, chapterId, autoSave, toast, debouncedSave]);

  // 🆕 监听 Agent 改写确认事件（从 useAgentChat 触发）
  useEffect(() => {
    if (!editor) return;

    const handleAgentReplace = (event: Event) => {
      const customEvent = event as CustomEvent<{
        original: string;
        replacement: string;
      }>;

      const { original, replacement } = customEvent.detail;

      console.log('[NovelEditor] 收到 Agent 改写确认事件:', {
        original: original?.substring(0, 50) + '...',
        replacement: replacement?.substring(0, 50) + '...'
      });

      if (!original || !replacement) {
        console.error('[NovelEditor] 改写事件缺少必要参数');
        return;
      }

      try {
        // 获取编辑器当前内容
        const currentHtml = editor.getHTML();

        // 在HTML中查找原文本（需要处理HTML标签）
        // 提取纯文本内容用于查找
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = currentHtml;
        const currentText = tempDiv.innerText || tempDiv.textContent || '';

        // 检查原文本是否存在
        if (currentText.includes(original)) {
          console.log('[NovelEditor] 找到原文本，执行替换');

          // 简单替换：直接在HTML中查找并替换文本
          // 注意：这种方法适用于简单的文本替换，如果原文本包含HTML标签需要更复杂的处理
          const newHtml = currentHtml.replace(original, replacement);

          // 更新编辑器内容
          editor.commands.setContent(newHtml);

          // 触发保存
          setSaveStatus('unsaved');
          if (autoSave) {
            debouncedSave(editor);
          }

          toast.success('已应用 AI 改写');
        } else {
          console.warn('[NovelEditor] 未找到原文本，可能已被修改');
          toast.warning('原文本已变更，无法自动替换');
        }
      } catch (error) {
        console.error('[NovelEditor] 应用改写失败:', error);
        toast.error('应用改写失败');
      }
    };

    window.addEventListener('agent-replace-text', handleAgentReplace as EventListener);

    return () => {
      window.removeEventListener('agent-replace-text', handleAgentReplace as EventListener);
    };
  }, [editor, autoSave, toast, debouncedSave]);

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

      {/* 🆕 Agent 编辑确认对话框 */}
      <AgentEditConfirmDialog
        isOpen={confirmDialog.isOpen}
        approvalRequest={confirmDialog.approvalRequest}
        onApprove={confirmDialog.onApprove}
        onReject={confirmDialog.onReject}
        onClose={confirmDialog.onReject}
      />

      <div className="novel-editor w-full h-full flex flex-col bg-white">
        {/* 顶部工具栏 */}
        <EditorToolbar
          editor={editor}
          aiAutoCompleteEnabled={aiAutoCompleteEnabled}
          onToggleAIAutoComplete={onToggleAIAutoComplete}
        />

        {/* 状态栏 - 极简设计 */}
        <div className="flex items-center justify-between px-5 py-1.5 bg-zinc-50/40 border-b border-zinc-100">
          <div className="flex items-center gap-3 text-[11px] text-zinc-600">
            <div className="flex items-center gap-1.5">
              <span>字数:</span>
              <span className="text-zinc-900">{wordCount}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span>字符:</span>
              <span className="text-zinc-900">{countCharactersInHtml(editor.getHTML())}</span>
            </div>
          </div>

          {/* 保存状态 */}
          <div className="flex items-center">
            {saveStatus === 'saved' && (
              <div className="flex items-center gap-1 text-green-600">
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-[11px]">已保存</span>
              </div>
            )}
            {saveStatus === 'saving' && (
              <div className="flex items-center gap-1 text-blue-600">
                <svg className="animate-spin w-3 h-3" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                <span className="text-[11px]">保存中...</span>
              </div>
            )}
            {saveStatus === 'unsaved' && (
              <div className="flex items-center gap-1 text-orange-600">
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span className="text-[11px]">未保存</span>
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
