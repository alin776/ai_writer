/**
 * Novel 编辑器组件
 * 基于 Tiptap 的富文本编辑器
 */
import React, { useEffect, useState, useCallback, useRef, useMemo } from 'react';
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
import AIRevisionBar, { RevisionData } from './AIRevisionBar'; // 🆕 AI 修订操作栏
import { SlashCommand } from './SlashCommandExtension';
import { AIHighlight } from './AIHighlightExtension';
import { AIAutoCompleteExtension } from './AIAutoCompleteExtension';
import { AIDeleted, AIInserted } from './AIRevisionMark'; // 🆕 AI 修订标记扩展
import { ToastContainer } from '@/components/ui/Toast';
import { useToast } from '@/hooks/useToast';
import { useEditorStore } from '@/store/editorStore';
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
  // ===== InlineAI 回调 =====
  onInlineAISend?: (message: string, context: InlineAIContext) => void;
  isInlineAILoading?: boolean;
}

// Inline AI 上下文类型（原本由 InlineAIInput 提供）
export interface InlineAIContext {
  selected_text: string;
  selected_text_html: string;
  selection_position: { from: number; to: number };
  knowledge_doc_ids?: string[];
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
  onInlineAISend,
  isInlineAILoading = false,
}) => {
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'unsaved'>('saved');
  const [wordCount, setWordCount] = useState(0);
  const toast = useToast();
  const { setRightSidebarType } = useEditorStore();

  // 🆕 选区快照：在点击 Ask AI 按钮时立即保存，防止后续操作丢失
  const [inlineAISelectionSnapshot, setInlineAISelectionSnapshot] = useState<{
    text: string;
    html: string;
    from: number;
    to: number;
  } | null>(null);

  // 🆕 AI 修订状态管理
  const [activeRevision, setActiveRevision] = useState<RevisionData | null>(null);
  const [revisionBarPosition, setRevisionBarPosition] = useState<{ top: number; left: number } | null>(null);
  const [isRevisionLoading, setIsRevisionLoading] = useState(false);
  const lastRevisionContextRef = useRef<{ message: string; context: InlineAIContext } | null>(null);
  const handleInlineAISendRef = useRef<((message: string, context: InlineAIContext) => void) | null>(null);

  // 按作品/章节隔离本地缓存，避免不同作品间内容串联
  const contentStorageKey = useMemo(() => {
    if (workId && chapterId) return `novel-editor-content-${workId}-${chapterId}`;
    return null;
  }, [workId, chapterId]);
  const jsonStorageKey = useMemo(() => {
    if (workId && chapterId) return `novel-editor-json-${workId}-${chapterId}`;
    return null;
  }, [workId, chapterId]);

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
      // 🆕 AI 修订标记扩展（删除线+插入标记）
      AIDeleted,
      AIInserted,
      // AI 自动补全扩展（流式版本）
      AIAutoCompleteExtension.configure({
        delay: 1000, // 提前触发，提升响应速度
        minChars: 30, // 提前触发，减少等待
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
      if (contentStorageKey) {
        localStorage.setItem(contentStorageKey, html);
      }
      if (jsonStorageKey) {
        localStorage.setItem(jsonStorageKey, JSON.stringify(json));
      }

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
    if (!content && editor && contentStorageKey) {
      const savedContent = localStorage.getItem(contentStorageKey);
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
        if (contentStorageKey) {
          localStorage.setItem(contentStorageKey, html);
        }
        if (jsonStorageKey) {
          localStorage.setItem(jsonStorageKey, JSON.stringify(json));
        }
        if (onSave) {
          onSave(html, json);
        }
      }
    };
  }, [editor, autoSave, onSave, contentStorageKey, jsonStorageKey]);

  // ===== 预加载元数据（降低首次自动补全延迟） =====
  useEffect(() => {
    if (workId && chapterId) {
      console.log('[NovelEditor] 预加载章节元数据:', { workId, chapterId });
      AIService.preloadMetadata(workId, chapterId);
    }
  }, [workId, chapterId]);

  // ===== 动态更新 AI 自动补全开关状态 =====
  useEffect(() => {
    if (!editor) return;

    const storage: any = (editor as any).storage;

    console.log('[NovelEditor] 检查 AI 自动补全状态:', {
      hasEditor: !!editor,
      storage,
      aiAutoComplete: storage?.aiAutoComplete,
      enabled: aiAutoCompleteEnabled
    });

    if (storage?.aiAutoComplete) {
      storage.aiAutoComplete.enabled = aiAutoCompleteEnabled;
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
  // 现在改为显示修订标记，而不是直接替换
  useEffect(() => {
    if (!editor) return;

    // 🆕 显示修订标记（不直接替换，等待用户确认）
    const handleShowRevision = (event: Event) => {
      const customEvent = event as CustomEvent<{
        type: 'modify' | 'continue';
        original: string;
        replacement: string;
        position?: { from: number; to: number };
        revisionId?: string;
        originalMessage?: string;
        context?: any;
      }>;

      const { type, original, replacement, position, revisionId, originalMessage, context } = customEvent.detail;

      console.log('[NovelEditor] 收到显示修订请求:', {
        type,
        original: original?.substring(0, 50) + '...',
        replacement: replacement?.substring(0, 50) + '...',
        position
      });

      if (!replacement) {
        console.error('[NovelEditor] 修订请求缺少内容');
        return;
      }

      const rid = revisionId || `rev-${Date.now()}`;

      try {
        if (type === 'modify' && position && position.from !== undefined && position.to !== undefined) {
          // 修改模式：原文显示删除线 + 新内容显示绿色高亮
          console.log('[NovelEditor] 应用修改模式修订标记');

          // 1. 先在原文位置应用 AIDeleted 标记（删除线）
          editor.chain()
            .focus()
            .setTextSelection({ from: position.from, to: position.to })
            .setMark('aiDeleted')
            .run();

          // 2. 在原文后面插入新内容（使用纯文本方式，然后应用标记，避免 HTML 注入）
          const insertPos = position.to;
          editor.chain()
            .setTextSelection(insertPos)
            .insertContent(replacement || '')  // 插入纯文本
            .run();

          // 3. 对插入的内容应用 aiInserted 标记
          const endPos = insertPos + (replacement?.length || 0);
          editor.chain()
            .setTextSelection({ from: insertPos, to: endPos })
            .setMark('aiInserted')
            .run();

          // 4. 计算操作栏位置
          const { view } = editor;
          const coords = view.coordsAtPos(insertPos);
          setRevisionBarPosition({
            top: coords.bottom + 8,
            left: coords.left
          });

          // 5. 设置活跃修订
          setActiveRevision({
            id: rid,
            type: 'modify',
            position,
            original,
            replacement,
            originalMessage,
            context
          });

          // 保存原始上下文用于重新生成
          if (originalMessage && context) {
            lastRevisionContextRef.current = { message: originalMessage, context };
          }

        } else if (type === 'continue') {
          // 续写模式：新内容显示绿色高亮
          console.log('[NovelEditor] 应用续写模式修订标记');

          const insertPos = position?.to || editor.state.doc.content.size;

          // 插入新内容（使用纯文本方式，然后应用标记，避免 HTML 注入）
          editor.chain()
            .focus()
            .setTextSelection(insertPos)
            .insertContent(replacement || '')  // 插入纯文本
            .run();

          // 对插入的内容应用 aiInserted 标记
          const endPos = insertPos + (replacement?.length || 0);
          editor.chain()
            .setTextSelection({ from: insertPos, to: endPos })
            .setMark('aiInserted')
            .run();

          // 计算操作栏位置
          const { view } = editor;
          const coords = view.coordsAtPos(insertPos);
          setRevisionBarPosition({
            top: coords.bottom + 8,
            left: coords.left
          });

          // 设置活跃修订
          setActiveRevision({
            id: rid,
            type: 'continue',
            position: position || { from: insertPos, to: insertPos },
            replacement,
            originalMessage,
            context
          });

          if (originalMessage && context) {
            lastRevisionContextRef.current = { message: originalMessage, context };
          }
        }

        toast.info('请确认修订内容');
      } catch (error) {
        console.error('[NovelEditor] 应用修订标记失败:', error);
        toast.error('显示修订失败');
      }
    };

    // 直接替换事件（用于用户确认采纳后的最终应用）
    const handleAgentReplace = (event: Event) => {
      const customEvent = event as CustomEvent<{
        original: string;
        replacement: string;
        position?: { from: number; to: number };
        action_type?: string;
        skipRevision?: boolean;  // 跳过修订标记，直接替换
      }>;

      const { original, replacement, position, action_type, skipRevision } = customEvent.detail;

      // 如果不是跳过修订标记的请求，转发到显示修订
      if (!skipRevision) {
        console.log('[NovelEditor] 转发到修订显示流程');
        window.dispatchEvent(new CustomEvent('agent-show-revision', {
          detail: {
            type: 'modify',
            original,
            replacement,
            position
          }
        }));
        return;
      }

      console.log('[NovelEditor] 收到直接替换请求:', {
        original: original?.substring(0, 50) + '...',
        replacement: replacement?.substring(0, 50) + '...',
        position,
        action_type
      });

      if (!replacement) {
        console.error('[NovelEditor] 替换请求缺少必要参数');
        return;
      }

      try {
        if (position && position.from !== undefined && position.to !== undefined) {
          editor.chain()
            .focus()
            .setTextSelection({ from: position.from, to: position.to })
            .deleteSelection()
            .insertContent(replacement)
            .run();

          setSaveStatus('unsaved');
          if (autoSave) {
            debouncedSave(editor);
          }

          toast.success('已应用 AI 改写');
          return;
        }

        if (!original) {
          console.error('[NovelEditor] 缺少原文本且无位置信息');
          return;
        }

        const currentHtml = editor.getHTML();
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = currentHtml;
        const currentText = tempDiv.innerText || tempDiv.textContent || '';

        if (currentText.includes(original)) {
          const newHtml = currentHtml.replace(original, replacement);
          editor.commands.setContent(newHtml);

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

    // 🆕 InlineAI: 监听 Agent 续写事件
    const handleAgentAppend = (event: Event) => {
      const customEvent = event as CustomEvent<{
        content: string;
        position?: { from: number; to: number };
        action_type?: string;
        skipRevision?: boolean;
      }>;

      const { content, position, skipRevision } = customEvent.detail;

      // 如果不是跳过修订标记的请求，转发到显示修订
      if (!skipRevision) {
        console.log('[NovelEditor] 转发到修订显示流程');
        window.dispatchEvent(new CustomEvent('agent-show-revision', {
          detail: {
            type: 'continue',
            replacement: content,
            position
          }
        }));
        return;
      }

      console.log('[NovelEditor] 收到直接续写请求:', {
        content: content?.substring(0, 50) + '...',
        position
      });

      if (!content) {
        console.error('[NovelEditor] 续写请求缺少内容');
        return;
      }

      try {
        if (position && position.to !== undefined) {
          editor.chain()
            .focus()
            .setTextSelection(position.to)
            .insertContent(content)
            .run();
        } else {
          const currentHtml = editor.getHTML();
          editor.commands.setContent(currentHtml + content);
        }

        setSaveStatus('unsaved');
        if (autoSave) {
          debouncedSave(editor);
        }

        toast.success('已应用 AI 续写');
      } catch (error) {
        console.error('[NovelEditor] 应用续写失败:', error);
        toast.error('应用续写失败');
      }
    };

    window.addEventListener('agent-show-revision', handleShowRevision as EventListener);
    window.addEventListener('agent-replace-text', handleAgentReplace as EventListener);
    window.addEventListener('agent-append-text', handleAgentAppend as EventListener);

    return () => {
      window.removeEventListener('agent-show-revision', handleShowRevision as EventListener);
      window.removeEventListener('agent-replace-text', handleAgentReplace as EventListener);
      window.removeEventListener('agent-append-text', handleAgentAppend as EventListener);
    };
  }, [editor, autoSave, toast, debouncedSave]);

  // 🆕 打开 Ask AI：保存选区并通知右侧 Agent
  const handleOpenInlineAI = useCallback(() => {
    if (!editor) return;

    // 获取选中文字的位置，用于定位浮动输入框
    const { from, to } = editor.state.selection;

    // 如果没有选中文字，不打开
    if (from === to) {
      toast.warning('请先选中一些文字');
      return;
    }

    // 🔑 关键修复：在打开弹层之前立即保存选区快照（同步操作）
    // 这是防止选区丢失的核心：在任何异步操作或状态变化之前就保存好选区
    const selectedText = editor.state.doc.textBetween(from, to, ' ');
    const selectedHtml = selectedText; // 简化处理，后续可以用更复杂的序列化

    console.log('[NovelEditor] 🔒 保存选区快照:', { text: selectedText, from, to });

    setInlineAISelectionSnapshot({
      text: selectedText,
      html: selectedHtml,
      from,
      to,
    });

    // 通知右侧 Agent 面板，提供选区上下文
    const intentPayload = {
      selected_text: selectedText,
      selected_text_html: selectedHtml,
      selection_position: { from, to },
    };
    const intentEvent = new CustomEvent('inline-ai-intent', {
      detail: intentPayload,
    });
    window.dispatchEvent(intentEvent);

    // 确保右侧切到 AI 助手
    setRightSidebarType('agent');

    // 如已挂载全局回调，则直接调用以减少延迟
    const intentHandler = (window as any).__agentInlineIntent__;
    if (typeof intentHandler === 'function') {
      try {
        intentHandler(intentPayload);
      } catch (error) {
        console.warn('[NovelEditor] 调用 __agentInlineIntent__ 失败，改为事件派发', error);
      }
    }

    // 队列方式兜底，避免监听尚未挂载
    if (!(window as any).__inlineAIIntentQueue__) {
      (window as any).__inlineAIIntentQueue__ = [];
    }
    (window as any).__inlineAIIntentQueue__.push(intentPayload);
  }, [editor, toast, setRightSidebarType]);

  // 🆕 采纳修订 - 删除原文（删除线），保留新内容
  const handleAcceptRevision = useCallback(() => {
    if (!activeRevision || !editor) return;

    const { id, type, position, replacement } = activeRevision;

    console.log('[NovelEditor] 采纳修订:', { id, type, position });

    try {
      // 使用 DOM API 替代正则表达式（更安全、更可靠）
      const currentHtml = editor.getHTML();
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = currentHtml;

      if (type === 'modify' && position) {
        // 修改模式：删除带删除线的原文，移除新内容的插入标记

        // 1. 移除所有 aiDeleted 标记的元素（删除原文）
        const deletedElements = tempDiv.querySelectorAll('del[data-ai-deleted], del.ai-deleted');
        deletedElements.forEach(el => {
          el.remove();
        });

        // 2. 移除 aiInserted 标记，但保留其内容
        const insertedElements = tempDiv.querySelectorAll('ins[data-ai-inserted], ins.ai-inserted');
        insertedElements.forEach(el => {
          // 将 ins 标签替换为其内容
          const fragment = document.createDocumentFragment();
          while (el.firstChild) {
            fragment.appendChild(el.firstChild);
          }
          el.parentNode?.replaceChild(fragment, el);
        });
      } else if (type === 'continue') {
        // 续写模式：移除插入标记，保留内容
        const insertedElements = tempDiv.querySelectorAll('ins[data-ai-inserted], ins.ai-inserted');
        insertedElements.forEach(el => {
          const fragment = document.createDocumentFragment();
          while (el.firstChild) {
            fragment.appendChild(el.firstChild);
          }
          el.parentNode?.replaceChild(fragment, el);
        });
      }

      editor.commands.setContent(tempDiv.innerHTML);

      // 触发保存
      setSaveStatus('unsaved');
      if (autoSave) {
        debouncedSave(editor);
      }

      // 清理状态
      setActiveRevision(null);
      setRevisionBarPosition(null);
      lastRevisionContextRef.current = null;

      toast.success('已采纳修改');
    } catch (error) {
      console.error('[NovelEditor] 采纳修订失败:', error);
      toast.error('采纳修改失败');
    }
  }, [activeRevision, editor, autoSave, debouncedSave, toast]);

  // 🆕 弃用修订 - 移除新内容，恢复原文
  const handleDiscardRevision = useCallback(() => {
    if (!activeRevision || !editor) return;

    const { id, type, position, original } = activeRevision;

    console.log('[NovelEditor] 弃用修订:', { id, type, position });

    try {
      // 使用 DOM API 替代正则表达式（更安全、更可靠）
      const currentHtml = editor.getHTML();
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = currentHtml;

      if (type === 'modify') {
        // 修改模式：移除插入的新内容，恢复原文（移除删除线标记）

        // 1. 移除 aiInserted 标记及其内容（删除新内容）
        const insertedElements = tempDiv.querySelectorAll('ins[data-ai-inserted], ins.ai-inserted');
        insertedElements.forEach(el => {
          el.remove();
        });

        // 2. 移除 aiDeleted 标记，但保留其内容（恢复原文）
        const deletedElements = tempDiv.querySelectorAll('del[data-ai-deleted], del.ai-deleted');
        deletedElements.forEach(el => {
          const fragment = document.createDocumentFragment();
          while (el.firstChild) {
            fragment.appendChild(el.firstChild);
          }
          el.parentNode?.replaceChild(fragment, el);
        });
      } else if (type === 'continue') {
        // 续写模式：移除插入的新内容
        const insertedElements = tempDiv.querySelectorAll('ins[data-ai-inserted], ins.ai-inserted');
        insertedElements.forEach(el => {
          el.remove();
        });
      }

      editor.commands.setContent(tempDiv.innerHTML);

      // 清理状态
      setActiveRevision(null);
      setRevisionBarPosition(null);
      lastRevisionContextRef.current = null;

      toast.info('已弃用修改');
    } catch (error) {
      console.error('[NovelEditor] 弃用修订失败:', error);
      toast.error('弃用修改失败');
    }
  }, [activeRevision, editor, toast]);

  // 🆕 重新生成修订
  const handleRegenerateRevision = useCallback(() => {
    if (!activeRevision || !editor) return;

    console.log('[NovelEditor] 重新生成修订');

    // 先弃用当前修订
    handleDiscardRevision();

    // 获取原始上下文
    const savedContext = lastRevisionContextRef.current;

    if (savedContext && handleInlineAISendRef.current) {
      // 标记正在加载
      setIsRevisionLoading(true);

      // 重新发送请求
      setTimeout(() => {
        handleInlineAISendRef.current?.(savedContext.message, savedContext.context);
        setIsRevisionLoading(false);
      }, 100);
    } else {
      toast.warning('无法重新生成，请重新选择文字并发送指令');
    }
  }, [activeRevision, editor, handleDiscardRevision, toast]);

  // 🆕 InlineAI 发送消息
  const handleInlineAISend = useCallback((message: string, context: InlineAIContext) => {
    // 🔍 自测诊断日志 - 检查 NovelEditor 接收到的选区信息
    console.log('===== NovelEditor 接收 InlineAI =====');
    console.log('1. 传入的 context.selected_text:', context?.selected_text);
    console.log('2. 传入的 context.selection_position:', context?.selection_position);
    console.log('3. inlineAISelectionSnapshot (预先保存):', inlineAISelectionSnapshot);
    console.log('4. 当前 editor.state.selection:', editor ? { from: editor.state.selection.from, to: editor.state.selection.to } : 'editor 不存在');
    console.log('5. editor 实时读取文本:', editor ? editor.state.doc.textBetween(editor.state.selection.from, editor.state.selection.to, ' ') : 'N/A');
    console.log('6. editor focused?:', editor?.isFocused);
    console.log('========================================');

    // 🔑 冗余保护：多层来源保证选区不丢失
    // 优先级：传入的 context > 预先保存的快照 > editor 实时读取
    let finalContext = context;
    let selectionSource = 'none';

    // 检查传入的 context 是否有有效选区
    const contextHasSelection = context?.selected_text && context.selected_text.trim().length > 0;

    if (contextHasSelection) {
      // 来源 1：传入的 context 有选区，直接使用
      selectionSource = 'context';
      console.log('[NovelEditor] ✅ 使用来源 1: 传入的 context');
    } else if (inlineAISelectionSnapshot && inlineAISelectionSnapshot.text) {
      // 来源 2：使用预先保存的快照（在弹层打开前保存的）
      selectionSource = 'snapshot';
      console.log('[NovelEditor] ✅ 使用来源 2: inlineAISelectionSnapshot 快照');
      finalContext = {
        ...context,
        selected_text: inlineAISelectionSnapshot.text,
        selected_text_html: inlineAISelectionSnapshot.html,
        selection_position: { from: inlineAISelectionSnapshot.from, to: inlineAISelectionSnapshot.to },
      };
    } else if (editor) {
      // 来源 3：从 editor 实时读取（可能会失败）
      const { from, to } = editor.state.selection;
      const fallbackText = editor.state.doc.textBetween(from, to, ' ');
      const hasSelection = from !== to && fallbackText.trim().length > 0;

      if (hasSelection) {
        selectionSource = 'editor-realtime';
        console.log('[NovelEditor] ✅ 使用来源 3: editor 实时读取');
        finalContext = {
          ...context,
          selected_text: fallbackText,
          selected_text_html: fallbackText,
          selection_position: { from, to },
        };
      }
    }

    // 最终检查：如果所有来源都没有选区，发出警告
    if (selectionSource === 'none') {
      console.warn('[NovelEditor] ⚠️ 警告：所有选区来源都为空！用户选中的文本可能已丢失');
      console.warn('[NovelEditor] 可能原因：');
      console.warn('  - 弹层打开时选区已清空');
      console.warn('  - 点击输入框导致编辑器失焦');
      console.warn('  - initialSelection 未正确传递');
    } else {
      console.log(`[NovelEditor] 📍 选区来源: ${selectionSource}`);
      console.log('[NovelEditor] 📍 最终选中文本:', finalContext.selected_text?.substring(0, 50) + '...');
      console.log('[NovelEditor] 📍 最终选区位置:', finalContext.selection_position);
    }

    console.log('[NovelEditor] InlineAI 最终发送:', { message, context: finalContext });

    // 确保右侧切到 AI 助手面板，保证消息接收
    setRightSidebarType('agent');

    const requestId = `inline-${Date.now()}-${Math.random().toString(16).slice(2)}`;
    const payload = { message, context: finalContext, requestId };

    // 初始化队列，防止监听未挂载时丢失
    if (!(window as any).__inlineAIQueue__) {
      (window as any).__inlineAIQueue__ = [];
    }
    (window as any).__inlineAIQueue__.push(payload);
    console.log('[NovelEditor] inline-ai payload queued', payload, 'queue size', (window as any).__inlineAIQueue__?.length);

    // 尝试直接调用全局回调（由 AIPanel 挂载）
    const globalHandler = (window as any).__agentInlineSend__;
    const dispatchEventToAgent = () => {
      const event = new CustomEvent('inline-ai-send', { detail: payload });
      window.dispatchEvent(event);
      console.log('[NovelEditor] inline-ai-send dispatched', payload);
    };

    if (typeof globalHandler === 'function') {
      try {
        console.log('[NovelEditor] 调用全局 __agentInlineSend__', payload);
        globalHandler(message, finalContext, requestId);
      } catch (err) {
        console.warn('[NovelEditor] 调用全局 __agentInlineSend__ 失败，回退事件', err);
        dispatchEventToAgent();
      }
    } else {
      // 稍作延迟，确保右侧面板挂载完成再派发；并二次重发防丢失
      setTimeout(dispatchEventToAgent, 200);
      setTimeout(dispatchEventToAgent, 800);
    }

    if (onInlineAISend) {
      onInlineAISend(message, finalContext);
    }

    toast.info('已发送到 AI 助手');
  }, [editor, inlineAISelectionSnapshot, onInlineAISend, toast, setRightSidebarType]);

  // 🆕 更新 handleInlineAISend ref（用于 handleRegenerateRevision 调用）
  useEffect(() => {
    handleInlineAISendRef.current = handleInlineAISend;
  }, [handleInlineAISend]);

  if (!editor) {
    return (
      <div className="flex items-center justify-center min-h-[500px] dark:bg-slate-900">
        <div className="text-gray-500 dark:text-slate-400">加载编辑器...</div>
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

      <div className="novel-editor w-full h-full flex flex-col bg-white dark:bg-slate-900">
        {/* 顶部工具栏 */}
        <EditorToolbar
          editor={editor}
          aiAutoCompleteEnabled={aiAutoCompleteEnabled}
          onToggleAIAutoComplete={onToggleAIAutoComplete}
        />

        {/* 状态栏 - 极简设计 */}
        <div className="flex items-center justify-between px-5 py-1.5 bg-zinc-50/40 border-b border-zinc-100 dark:bg-slate-800/50 dark:border-slate-700">
          <div className="flex items-center gap-3 text-[11px] text-zinc-600 dark:text-slate-400">
            <div className="flex items-center gap-1.5">
              <span>字数:</span>
              <span className="text-zinc-900 dark:text-slate-200">{wordCount}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span>字符:</span>
              <span className="text-zinc-900 dark:text-slate-200">{countCharactersInHtml(editor.getHTML())}</span>
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
        <div className="flex-1 overflow-y-auto bg-white dark:bg-slate-900">
          <EditorContent editor={editor} className="editor-canvas" />
          {/* 气泡菜单 - 选中文本时显示 */}
          <BubbleMenu editor={editor} onOpenInlineAI={handleOpenInlineAI} />
          {/* AI 菜单 - 选中文本时显示 AI 操作 */}
          <AIMenu editor={editor} onOpenInlineAI={handleOpenInlineAI} />
        </div>
      </div>

      {/* 🆕 AI 修订操作栏 */}
      {activeRevision && (
        <AIRevisionBar
          revision={activeRevision}
          position={revisionBarPosition}
          onRegenerate={handleRegenerateRevision}
          onDiscard={handleDiscardRevision}
          onAccept={handleAcceptRevision}
          isLoading={isRevisionLoading}
        />
      )}
    </>
  );
};

export default NovelEditor;
