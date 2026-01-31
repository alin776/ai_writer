/**
 * Novel 编辑器组件
 * 基于 Tiptap 的富文本编辑器
 */
import React, { useEffect, useState, useCallback, useRef, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import { useEditor, EditorContent } from '@tiptap/react';
import { TextSelection } from 'prosemirror-state';
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
import { AIDeleted, AIInserted, AIRevisionId } from './AIRevisionMark'; // 🆕 AI 修订标记扩展
import { UniqueID } from './UniqueIDExtension'; // 🆕 节点唯一ID扩展，用于精确定位
import { ToastContainer } from '@/components/ui/Toast';
import { useToast } from '@/hooks/useToast';
import { locateRevisionPosition, locateInsertPosition } from '@/utils/revisionLocator'; // 🆕 锚点定位工具
import { useEditorStore } from '@/store/editorStore';
import AIService from '@/services/AIService';
import { DataService } from '@/services/DataService';
import { agentApi } from '@/services/agentApi';
import type { ChapterRevision } from '@/types/revision';
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
  chapterTitle?: string;
  chapterOrder?: number;
  // ===== Context-Aware 元数据 =====
  workId?: string;
  chapterId?: string;
  // ===== AI 自动补全开关 =====
  aiAutoCompleteEnabled?: boolean;
  onToggleAIAutoComplete?: () => void;
  // ===== 左侧面板折叠状态 =====
  isLeftPanelCollapsed?: boolean;
  onExpandLeftPanel?: () => void;
  onCollapseLeftPanel?: () => void;
  // ===== 右侧面板折叠状态 =====
  isRightPanelCollapsed?: boolean;
  onExpandRightPanel?: () => void;
  onCollapseRightPanel?: () => void;
  // ===== AI 面板折叠状态 =====
  isAIPanelCollapsed?: boolean;
  onToggleAIPanel?: () => void;
  onCollapseAIPanel?: () => void;
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

type AgentActionType = 'edit' | 'rewrite' | 'insert' | 'create' | 'rename';

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

type RevisionJumpRequest = {
  chapterId?: string;
  revisionId?: string;
  requestId?: string;
  position?: { from: number; to: number };
  attempts?: number;
};

const CROSS_CHAPTER_REVISION_TTL_MS = 30 * 60 * 1000;

/**
 * Novel 编辑器组件
 */
const NovelEditor: React.FC<NovelEditorProps> = ({
  content = '',
  onSave,
  placeholder,
  autoSave = true,
  autoSaveInterval = 3000,
  chapterTitle,
  chapterOrder,
  workId,      // Context-Aware 参数
  chapterId,   // Context-Aware 参数
  aiAutoCompleteEnabled = false, // 默认关闭，避免意外消耗积分
  onToggleAIAutoComplete,
  isLeftPanelCollapsed = false,
  onExpandLeftPanel,
  onCollapseLeftPanel,
  isRightPanelCollapsed = false,
  onExpandRightPanel,
  onCollapseRightPanel,
  isAIPanelCollapsed = false,
  onToggleAIPanel,
  onCollapseAIPanel,
  onInlineAISend,
  isInlineAILoading = false,
}) => {
  const { t } = useTranslation();
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'unsaved'>('saved');
  const [wordCount, setWordCount] = useState(0);
  const toast = useToast();
  const {
    setRightSidebarType,
    pendingCrossChapterRevisions,
    enqueuePendingCrossChapterRevision,
    removePendingCrossChapterRevisions
  } = useEditorStore();

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
  const appliedRevisionIdsRef = useRef<Set<string>>(new Set());
  const suppressAutoSaveRef = useRef(false);
  const revisionSaveBlockedRef = useRef(false);
  const pendingRevisionJumpRef = useRef<RevisionJumpRequest | null>(null);
  const pendingJumpTimerRef = useRef<number | null>(null);

  useEffect(() => {
    appliedRevisionIdsRef.current.clear();
  }, [chapterId]);

  const clearPendingRevisions = useCallback((revisionIds: string[]) => {
    if (revisionIds.length === 0) return;
    revisionIds.forEach((revisionId) => appliedRevisionIdsRef.current.delete(revisionId));
    removePendingCrossChapterRevisions(revisionIds);
  }, [removePendingCrossChapterRevisions]);

  const getPendingRevisionIdsForChapter = useCallback((targetChapterId?: string) => {
    if (!targetChapterId) return [];
    return pendingCrossChapterRevisions
      .filter((revision) => revision.targetChapterId === targetChapterId)
      .map((revision) => revision.revisionId);
  }, [pendingCrossChapterRevisions]);
  const applyRevisionDecisionToHtml = (
    html: string,
    decision: 'accept' | 'discard',
    revisionIds?: string[]
  ) => {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    const ids = (revisionIds || []).filter(Boolean);
    const unwrap = (element: Element) => {
      const fragment = document.createDocumentFragment();
      while (element.firstChild) {
        fragment.appendChild(element.firstChild);
      }
      element.parentNode?.replaceChild(fragment, element);
    };
    const normalizeTargets = (revisionId: string) => {
      const revisionElements = Array.from(
        tempDiv.querySelectorAll(`[data-revision-id="${revisionId}"]`)
      );
      const deletedTargets = new Set<HTMLElement>();
      const insertedTargets = new Set<HTMLElement>();

      revisionElements.forEach((element) => {
        const deletedAncestor = element.closest('del[data-ai-deleted], del.ai-deleted');
        if (deletedAncestor) deletedTargets.add(deletedAncestor as HTMLElement);
        const insertedAncestor = element.closest('ins[data-ai-inserted], ins.ai-inserted');
        if (insertedAncestor) insertedTargets.add(insertedAncestor as HTMLElement);

        element.querySelectorAll('del[data-ai-deleted], del.ai-deleted').forEach((node) => {
          deletedTargets.add(node as HTMLElement);
        });
        element.querySelectorAll('ins[data-ai-inserted], ins.ai-inserted').forEach((node) => {
          insertedTargets.add(node as HTMLElement);
        });
      });

      return { deletedTargets, insertedTargets };
    };

    if (ids.length === 0) {
      const deletedElements = tempDiv.querySelectorAll('del[data-ai-deleted], del.ai-deleted');
      const insertedElements = tempDiv.querySelectorAll('ins[data-ai-inserted], ins.ai-inserted');
      const revisionIdElements = tempDiv.querySelectorAll('span[data-revision-id]');

      if (decision === 'accept') {
        deletedElements.forEach(el => el.remove());
        insertedElements.forEach(el => unwrap(el));
      } else {
        insertedElements.forEach(el => el.remove());
        deletedElements.forEach(el => unwrap(el));
      }
      revisionIdElements.forEach(el => unwrap(el));
      return tempDiv.innerHTML;
    }

    ids.forEach((revisionId) => {
      const { deletedTargets, insertedTargets } = normalizeTargets(revisionId);
      if (decision === 'accept') {
        deletedTargets.forEach(el => el.remove());
        insertedTargets.forEach(el => unwrap(el));
      } else {
        insertedTargets.forEach(el => el.remove());
        deletedTargets.forEach(el => unwrap(el));
      }
      const revisionIdElements = tempDiv.querySelectorAll(`[data-revision-id="${revisionId}"]`);
      revisionIdElements.forEach(el => unwrap(el));
    });

    return tempDiv.innerHTML;
  };

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
        placeholder: placeholder || t('editor.startWriting'),
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
      AIRevisionId,
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
      // 🆕 节点唯一ID扩展（用于 Agent 精确定位）
      UniqueID.configure({
        types: ['paragraph', 'heading', 'blockquote', 'codeBlock'],
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
      // 使用自定义字数统计（与后端一致）
      setWordCount(getEditorWordCount(editor));

      if (suppressAutoSaveRef.current || revisionSaveBlockedRef.current) {
        return;
      }

      setSaveStatus('unsaved');
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
      try {
        if (contentStorageKey) {
          localStorage.setItem(contentStorageKey, html);
        }
        if (jsonStorageKey) {
          localStorage.setItem(jsonStorageKey, JSON.stringify(json));
        }
      } catch (e) {
        console.warn('localStorage 存储失败，可能配额已满:', e);
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

  const findRevisionIdPosition = useCallback((revisionId: string) => {
    if (!editor || !revisionId) return null;
    let foundPos: number | null = null;
    editor.state.doc.descendants((node, pos) => {
      if (!node.isText) {
        return true;
      }
      if (node.marks.some(
        (mark) => mark.type.name === 'aiRevisionId' && mark.attrs?.revisionId === revisionId
      )) {
        foundPos = pos;
        return false;
      }
      return true;
    });
    return foundPos;
  }, [editor]);

  const jumpToRevision = useCallback((request: RevisionJumpRequest) => {
    if (!editor) return false;
    const { position, revisionId, requestId } = request;
    const { state, view } = editor;
    const maxPos = state.doc.content.size;
    const clamp = (value: number) => Math.max(0, Math.min(value, maxPos));
    const applySelection = (from: number, to: number) => {
      const safeFrom = clamp(Math.min(from, to));
      const safeTo = clamp(Math.max(from, to));
      const tr = state.tr.setSelection(TextSelection.create(state.doc, safeFrom, safeTo));
      tr.scrollIntoView();
      view.dispatch(tr);
      view.focus();
    };

    if (position) {
      applySelection(position.from, position.to);
      return true;
    }

    const targetId = revisionId || requestId;
    if (!targetId) return false;
    const pos = findRevisionIdPosition(targetId);
    if (pos === null) return false;
    applySelection(pos, pos);
    return true;
  }, [editor, findRevisionIdPosition]);

  const attemptPendingRevisionJump = useCallback(() => {
    const pending = pendingRevisionJumpRef.current;
    if (!pending) return;
    if (pending.chapterId && chapterId && pending.chapterId !== chapterId) return;
    if (jumpToRevision(pending)) {
      pendingRevisionJumpRef.current = null;
      return;
    }
    const attempts = pending.attempts ?? 0;
    if (attempts >= 3) return;
    pendingRevisionJumpRef.current = { ...pending, attempts: attempts + 1 };
    if (pendingJumpTimerRef.current !== null) return;
    pendingJumpTimerRef.current = window.setTimeout(() => {
      pendingJumpTimerRef.current = null;
      attemptPendingRevisionJump();
    }, 150);
  }, [chapterId, jumpToRevision]);

  useEffect(() => {
    attemptPendingRevisionJump();
  }, [attemptPendingRevisionJump, pendingCrossChapterRevisions]);

  useEffect(() => {
    return () => {
      if (pendingJumpTimerRef.current !== null) {
        window.clearTimeout(pendingJumpTimerRef.current);
        pendingJumpTimerRef.current = null;
      }
    };
  }, []);

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

  // 加载章节待处理修订（持久化）
  useEffect(() => {
    if (!editor || !chapterId) return;

    let cancelled = false;

    const loadRevisions = async () => {
      try {
        const revisions = await DataService.getChapterRevisions(chapterId);
        if (cancelled || !revisions || revisions.length === 0) return;

        revisions.forEach((revision: ChapterRevision) => {
          const editorType: 'modify' | 'continue' | 'insert' =
            revision.operation === 'append'
              ? 'continue'
              : revision.operation === 'insert'
                ? 'insert'
                : 'modify';

          window.dispatchEvent(new CustomEvent('agent-show-revision', {
            detail: {
              revisionId: revision.requestId,
              requestId: revision.requestId,
              chapterId: revision.chapterId,
              type: editorType,
              replacement: revision.newText,
              original: revision.originalText,
              position: revision.position,
              beforeAnchor: revision.beforeAnchor,
              afterAnchor: revision.afterAnchor,
              nodeId: revision.nodeId,
              paragraphIndex: revision.paragraphIndex,
              skipQueue: true,
              isPersistent: true,
            }
          }));
        });
      } catch (error) {
        console.error('[NovelEditor] 加载修订失败:', error);
      }
    };

    loadRevisions();
    return () => {
      cancelled = true;
    };
  }, [editor, chapterId]);

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
        const hasRevisionMarkers = html.includes('data-ai-deleted')
          || html.includes('data-ai-inserted')
          || html.includes('data-revision-id');
        if (revisionSaveBlockedRef.current || hasRevisionMarkers) {
          return;
        }
        const json = editor.getJSON();
        try {
          if (contentStorageKey) {
            localStorage.setItem(contentStorageKey, html);
          }
          if (jsonStorageKey) {
            localStorage.setItem(jsonStorageKey, JSON.stringify(json));
          }
        } catch (e) {
          console.warn('localStorage 存储失败，可能配额已满:', e);
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

  // ===== 暴露 UniqueID API 给外部调用（如 Agent） =====
  useEffect(() => {
    if (!editor) return;

    // 挂载到 window，供 Agent 或其他模块调用
    (window as any).__editorNodeAPI = {
      /**
       * 通过 ID 查找节点
       * @param id 节点 ID
       * @returns { success, position, text } 或 { success: false }
       */
      findByNodeID: (id: string) => {
        const result = (editor.storage as any).uniqueID?.findNodeByID(id);
        if (result) {
          return {
            success: true,
            position: { from: result.pos, to: result.pos + result.node.nodeSize },
            text: result.text,
          };
        }
        return { success: false };
      },

      /**
       * 获取所有节点列表（带 ID 和预览）
       * @returns 节点信息列表
       */
      getAllNodes: () => {
        return (editor.storage as any).uniqueID?.getAllNodes() || [];
      },

      /**
       * 通过 ID 选中节点
       * @param id 节点 ID
       * @returns 是否成功
       */
      selectNodeByID: (id: string) => {
        return (editor.storage as any).uniqueID?.selectNodeByID(id) || false;
      },

      /**
       * 通过 ID 替换节点内容
       * @param id 节点 ID
       * @param content 新内容（HTML 或纯文本）
       * @returns 是否成功
       */
      replaceNodeByID: (id: string, content: string) => {
        return (editor.storage as any).uniqueID?.replaceNodeByID(id, content) || false;
      },

      /**
       * 获取当前文档的 JSON 结构（带 ID）
       * @returns Tiptap JSON
       */
      getDocumentJSON: () => {
        return editor.getJSON();
      },
    };

    return () => {
      delete (window as any).__editorNodeAPI;
    };
  }, [editor]);

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
            toast.success(t('editor.aiMenu.appliedEdit'));
          },
          onReject: () => {
            // 用户取消，不做任何操作
            console.log('[NovelEditor] 用户取消 Agent 编辑');
            setConfirmDialog(prev => ({ ...prev, isOpen: false }));
            toast.info(t('editor.aiMenu.cancelledEdit'));
          }
        });
      }
    });

    // 订阅同步错误事件
    const unsubscribeError = editorSyncService.onSyncError((data) => {
      if (data.chapterId === chapterId) {
        console.error('[NovelEditor] 同步失败:', data.error);
        toast.error(t('editor.aiMenu.syncFailed'));
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

  // 🆕 章节切换时检查并显示待处理的跨章节修订
  useEffect(() => {
    if (!editor || !chapterId || pendingCrossChapterRevisions.length === 0) return;

    const now = Date.now();
    const chapterRevisions = pendingCrossChapterRevisions
      .filter((revision) => revision.targetChapterId === chapterId)
      .sort((a, b) => a.timestamp - b.timestamp);

    if (chapterRevisions.length === 0) return;

    const expiredRevisions = chapterRevisions.filter(
      (revision) => !revision.isPersistent && now - revision.timestamp > CROSS_CHAPTER_REVISION_TTL_MS
    );
    if (expiredRevisions.length > 0) {
      console.log('[NovelEditor] 跨章节修订已过期，清除:', expiredRevisions.map((r) => r.revisionId));
      clearPendingRevisions(expiredRevisions.map((r) => r.revisionId));
    }

    const activeRevisions = chapterRevisions.filter(
      (revision) => revision.isPersistent || now - revision.timestamp <= CROSS_CHAPTER_REVISION_TTL_MS
    );
    if (activeRevisions.length === 0) return;

    const unappliedRevisions = activeRevisions.filter(
      (revision) => !appliedRevisionIdsRef.current.has(revision.revisionId)
    );
    if (unappliedRevisions.length === 0) return;

    for (const revisionSnapshot of unappliedRevisions) {
      if (!revisionSnapshot.replacement) {
        console.warn('[NovelEditor] 跨章节修订：缺少新内容', revisionSnapshot);
        clearPendingRevisions([revisionSnapshot.revisionId]);
        continue;
      }

      window.dispatchEvent(new CustomEvent('agent-show-revision', {
        detail: {
          type: revisionSnapshot.type,
          original: revisionSnapshot.original,
          replacement: revisionSnapshot.replacement,
          position: revisionSnapshot.position,
          revisionId: revisionSnapshot.revisionId,
          requestId: revisionSnapshot.revisionId,
          beforeAnchor: revisionSnapshot.beforeAnchor,
          afterAnchor: revisionSnapshot.afterAnchor,
          nodeId: revisionSnapshot.nodeId,
          paragraphIndex: revisionSnapshot.paragraphIndex,
          chapterId: revisionSnapshot.targetChapterId,
          skipQueue: true,
          isPersistent: revisionSnapshot.isPersistent,
        }
      }));
    }
  }, [editor, chapterId, pendingCrossChapterRevisions, clearPendingRevisions]);

  // 🆕 监听 Agent 改写确认事件（从 useAgentChat 触发）
  // 现在改为显示修订标记，而不是直接替换
  useEffect(() => {
    if (!editor) return;

    // 🆕 显示修订标记（不直接替换，等待用户确认）
    const handleShowRevision = (event: Event) => {
      const customEvent = event as CustomEvent<{
        type: 'modify' | 'continue' | 'insert';
        original: string;
        replacement: string;
        position?: { from: number; to: number };
        revisionId?: string;
        requestId?: string;
        originalMessage?: string;
        context?: any;
        beforeAnchor?: string;  // 锚点定位
        afterAnchor?: string;   // 锚点定位
        nodeId?: string;        // 🆕 节点 ID（最高优先级）
        paragraphIndex?: number; // 🆕 段落索引
        chapterId?: string;     // 🆕 目标章节ID（跨章节检查）
        skipQueue?: boolean;
        isPersistent?: boolean;
      }>;

      const { type, original, replacement, position, revisionId, requestId, originalMessage, context, beforeAnchor, afterAnchor, nodeId, paragraphIndex, chapterId: targetChapterId, skipQueue, isPersistent } = customEvent.detail;

      if (!replacement) {
        console.error('[NovelEditor] 修订请求缺少内容');
        return;
      }

      const rid = requestId || revisionId || `rev-${Date.now()}`;
      const requestIdValue = requestId;
      const resolvedChapterId = targetChapterId || chapterId;
      const withAutoSaveSuppressed = (action: () => void) => {
        suppressAutoSaveRef.current = true;
        try {
          action();
        } finally {
          suppressAutoSaveRef.current = false;
        }
      };
      const blockRevisionSave = () => {
        revisionSaveBlockedRef.current = true;
        debouncedSave.cancel();
      };

      if (resolvedChapterId && !skipQueue) {
        enqueuePendingCrossChapterRevision({
          targetChapterId: resolvedChapterId,
          revisionId: rid,
          type,
          original,
          replacement,
          position,
          beforeAnchor,
          afterAnchor,
          nodeId,
          paragraphIndex,
          timestamp: Date.now(),
          isPersistent
        });
      }

      // 🆕 跨章节检查：如果目标章节不是当前章节，保存修订信息并提示用户
      // 后端已经在目标章节完成了修改，这里保存信息供切换章节时使用
      if (targetChapterId && chapterId && targetChapterId !== chapterId) {
        console.log('[NovelEditor] 跨章节修改，保存修订信息:', { targetChapterId, currentChapterId: chapterId });
        toast.info(t('editor.aiMenu.crossChapterModified') || '内容已在其他章节修改，请切换查看');
        return;  // 当前编辑器不显示修订标记，用户需要切换到目标章节查看
      }

      console.log('[NovelEditor] 收到显示修订请求:', {
        type,
        original: original?.substring(0, 50) + '...',
        replacement: replacement?.substring(0, 50) + '...',
        position,
        nodeId,
        paragraphIndex,
        beforeAnchor: beforeAnchor?.substring(0, 30),
        afterAnchor: afterAnchor?.substring(0, 30)
      });

      try {
        // 🆕 v8.3: 定位优先级：nodeId > paragraphIndex > position > 锚点 > 默认
        let resolvedPosition = position;

        // 1. 尝试通过 nodeId 定位（最高优先级）
        if (!resolvedPosition && nodeId) {
          const nodeResult = (window as any).__editorNodeAPI?.findByNodeID(nodeId);
          if (nodeResult?.success) {
            resolvedPosition = nodeResult.position;
            console.log('[NovelEditor] nodeId 定位成功:', nodeId, resolvedPosition);
          }
        }

        // 2. 尝试通过 paragraphIndex 定位（从 getAllNodes 获取 nodeId）
        if (!resolvedPosition && paragraphIndex !== undefined) {
          const nodes = (window as any).__editorNodeAPI?.getAllNodes();
          if (nodes && nodes[paragraphIndex]) {
            const targetNodeId = nodes[paragraphIndex].id;
            const nodeResult = (window as any).__editorNodeAPI?.findByNodeID(targetNodeId);
            if (nodeResult?.success) {
              resolvedPosition = nodeResult.position;
              console.log('[NovelEditor] paragraphIndex 定位成功:', paragraphIndex, '→', targetNodeId, resolvedPosition);
            }
          }
        }

        // 3. 如果没有 position 但有锚点，使用锚点定位
        if (!resolvedPosition && (beforeAnchor || afterAnchor)) {
          const docText = editor.state.doc.textContent;

          if (type === 'modify' && original) {
            // 修改模式：定位原文位置
            const result = locateRevisionPosition(docText, {
              originalText: original,
              beforeAnchor,
              afterAnchor
            });
            if (result.success && result.position) {
              resolvedPosition = result.position;
              console.log('[NovelEditor] 锚点定位成功 (modify):', result.method, resolvedPosition);
            }
          } else if (type === 'continue' || type === 'insert') {
            // 续写/插入模式：定位插入点
            const result = locateInsertPosition(docText, { beforeAnchor, afterAnchor });
            if (result.success && result.position) {
              const isAnchorFallback = (beforeAnchor || afterAnchor) && result.method === 'exact';
              if (!isAnchorFallback || type === 'continue') {
                resolvedPosition = result.position;
                console.log('[NovelEditor] 锚点定位成功 (insert):', result.method, resolvedPosition);
              } else {
                console.warn('[NovelEditor] 锚点定位失败，插入已取消');
              }
            }
          }
        }

        // 如果仍然没有位置，使用默认值
        if (!resolvedPosition) {
          if (type === 'continue') {
            // 续写默认追加到末尾
            const endPos = editor.state.doc.content.size;
            resolvedPosition = { from: endPos, to: endPos };
          } else if (type === 'modify') {
            const docText = editor.state.doc.textContent;
            const normalizeText = (text: string) => text.replace(/\s+/g, '');
            const normalizedOriginal = normalizeText(original || '');
            const normalizedDoc = normalizeText(docText);
            if (normalizedOriginal && normalizedOriginal === normalizedDoc) {
              resolvedPosition = { from: 0, to: editor.state.doc.content.size };
            } else {
              console.warn('[NovelEditor] 修订定位失败，已取消应用');
              toast.error(t('editor.aiMenu.revisionFailed'));
              return;
            }
          } else {
            console.warn('[NovelEditor] 插入定位失败，已取消应用');
            toast.error(t('editor.aiMenu.revisionFailed'));
            return;
          }
          console.log('[NovelEditor] 使用默认位置:', resolvedPosition);
        }

        blockRevisionSave();

        const insertPosForCheck =
          type === 'modify'
            ? resolvedPosition.to
            : type === 'insert'
              ? resolvedPosition.from
              : resolvedPosition.to;

        const { doc } = editor.state;
        const aiInsertedMark = editor.state.schema.marks.aiInserted;
        const aiRevisionIdMark = editor.state.schema.marks.aiRevisionId;
        const normalizeText = (value: string) => value.replace(/\s+/g, '');

        const revisionIdPos = findRevisionIdPosition(rid);
        if (revisionIdPos !== null) {
          console.log('[NovelEditor] 修订已存在，跳过重复应用:', rid);
          appliedRevisionIdsRef.current.add(rid);

          requestAnimationFrame(() => {
            try {
              const coords = editor.view.coordsAtPos(revisionIdPos);
              setRevisionBarPosition({
                top: coords.top - 40,
                left: coords.left
              });
            } catch (e) {
              console.warn('[NovelEditor] 无法计算修订栏位置:', e);
            }
          });

          setActiveRevision({
            id: rid,
            requestId: requestIdValue,
            type,
            position: resolvedPosition,
            original,
            replacement,
            originalMessage,
            context
          });
          return;
        }

        if (replacement) {
          const resolvedFrom = insertPosForCheck >= doc.content.size
            ? Math.max(0, doc.content.size - replacement.length)
            : insertPosForCheck;
          const resolvedTo = insertPosForCheck >= doc.content.size
            ? doc.content.size
            : Math.min(insertPosForCheck + replacement.length, doc.content.size);
          if (resolvedFrom < resolvedTo) {
            const existingText = doc.textBetween(resolvedFrom, resolvedTo, '\n', '\n');
            const hasInsertedMark = aiInsertedMark ? doc.rangeHasMark(resolvedFrom, resolvedTo, aiInsertedMark) : false;

            if (normalizeText(existingText) === normalizeText(replacement) && hasInsertedMark) {
              console.log('[NovelEditor] 修订已写入，跳过重复应用:', rid);
              appliedRevisionIdsRef.current.add(rid);

              requestAnimationFrame(() => {
                try {
                  const coords = editor.view.coordsAtPos(insertPosForCheck);
                  setRevisionBarPosition({
                    top: coords.top - 40,
                    left: coords.left
                  });
                } catch (e) {
                  console.warn('[NovelEditor] 无法计算修订栏位置:', e);
                }
              });

              setActiveRevision({
                id: rid,
                requestId: requestIdValue,
                type,
                position: resolvedPosition,
                original,
                replacement,
                originalMessage,
                context
              });
              return;
            }
          }
        }

        if (type === 'modify') {
          // 修改模式：原文显示删除线 + 新内容显示绿色高亮
          console.log('[NovelEditor] 应用修改模式修订标记, position:', resolvedPosition);

          // 🔧 修复：使用 ProseMirror Transaction API 确保原子性操作
          const { state, view } = editor;
          const { tr } = state;
          const aiDeletedMark = state.schema.marks.aiDeleted;
          const aiInsertedMark = state.schema.marks.aiInserted;
          const aiRevisionIdMark = state.schema.marks.aiRevisionId;

          if (!aiDeletedMark || !aiInsertedMark) {
            console.error('[NovelEditor] 修订标记扩展未正确注册');
            return;
          }

          withAutoSaveSuppressed(() => {
            // 1. 在原文位置添加删除标记
            tr.addMark(resolvedPosition.from, resolvedPosition.to, aiDeletedMark.create());
            if (aiRevisionIdMark) {
              tr.addMark(
                resolvedPosition.from,
                resolvedPosition.to,
                aiRevisionIdMark.create({ revisionId: rid })
              );
            }

            // 2. 在原文后面插入新内容（带有插入标记）
            const insertPos = resolvedPosition.to;
            const textContent = replacement || '';

            // 🔧 修复：处理包含换行符的文本
            if (textContent.includes('\n')) {
              // 包含换行符时，先提交删除标记，再用 insertContent 处理多段落
              view.dispatch(tr);

              // 使用 chain 插入内容并应用标记
              const endPos = insertPos + textContent.length;
              editor.chain()
                .focus()
                .setTextSelection(insertPos)
                .insertContent(textContent)
                .setTextSelection({ from: insertPos, to: endPos })
                .setMark('aiInserted')
                .setMark('aiRevisionId', { revisionId: rid })
                .run();
            } else {
              // 无换行符时，使用原子事务
              const marks = [aiInsertedMark.create()];
              if (aiRevisionIdMark) {
                marks.push(aiRevisionIdMark.create({ revisionId: rid }));
              }
              const insertedText = state.schema.text(textContent, marks);
              tr.insert(insertPos, insertedText);
              view.dispatch(tr);
            }
          });

          // 3. 计算操作栏位置（使用 requestAnimationFrame 确保 DOM 已重排）
          requestAnimationFrame(() => {
            try {
              const coords = view.coordsAtPos(resolvedPosition.to);
              setRevisionBarPosition({
                top: coords.top - 40,  // 显示在内容上方，避免遮挡高亮内容
                left: coords.left
              });
            } catch (e) {
              console.warn('[NovelEditor] 无法计算修订栏位置:', e);
            }
          });

          // 4. 设置活跃修订
          setActiveRevision({
            id: rid,
            requestId: requestIdValue,
            type: 'modify',
            position: resolvedPosition,
            original,
            replacement,
            originalMessage,
            context
          });
          appliedRevisionIdsRef.current.add(rid);

          // 保存原始上下文用于重新生成
          if (originalMessage && context) {
            lastRevisionContextRef.current = { message: originalMessage, context };
          }

          // 修订标记展示阶段不触发自动保存，避免版本变化导致审批冲突
          setSaveStatus('saved');

        } else if (type === 'continue') {
          // 续写模式：新内容显示绿色高亮
          console.log('[NovelEditor] 应用续写模式修订标记');

          // 🔧 修复：使用 ProseMirror Transaction API 确保原子性操作
          const { state, view } = editor;
          const { tr } = state;
          const aiInsertedMark = state.schema.marks.aiInserted;
          const aiRevisionIdMark = state.schema.marks.aiRevisionId;

          if (!aiInsertedMark) {
            console.error('[NovelEditor] aiInserted 标记扩展未正确注册');
            return;
          }

          const insertPos = resolvedPosition?.to ?? state.doc.content.size;
          const textContent = replacement || '';

          withAutoSaveSuppressed(() => {
            // 🔧 修复：处理包含换行符的文本
            if (textContent.includes('\n')) {
              // 包含换行符时，用 insertContent 处理多段落
              const endPos = insertPos + textContent.length;
              editor.chain()
                .focus()
                .setTextSelection(insertPos)
                .insertContent(textContent)
                .setTextSelection({ from: insertPos, to: endPos })
                .setMark('aiInserted')
                .setMark('aiRevisionId', { revisionId: rid })
                .run();
            } else {
              // 无换行符时，使用原子事务
              const marks = [aiInsertedMark.create()];
              if (aiRevisionIdMark) {
                marks.push(aiRevisionIdMark.create({ revisionId: rid }));
              }
              const insertedText = state.schema.text(textContent, marks);
              tr.insert(insertPos, insertedText);
              view.dispatch(tr);
            }
          });

          // 计算操作栏位置（使用 requestAnimationFrame 确保 DOM 已重排）
          requestAnimationFrame(() => {
            try {
              const coords = view.coordsAtPos(insertPos);
              setRevisionBarPosition({
                top: coords.top - 40,  // 显示在内容上方，避免遮挡高亮内容
                left: coords.left
              });
            } catch (e) {
              console.warn('[NovelEditor] 无法计算修订栏位置:', e);
            }
          });

          // 设置活跃修订
          setActiveRevision({
            id: rid,
            requestId: requestIdValue,
            type: 'continue',
            position: resolvedPosition || { from: insertPos, to: insertPos },
            replacement,
            originalMessage,
            context
          });
          appliedRevisionIdsRef.current.add(rid);

          if (originalMessage && context) {
            lastRevisionContextRef.current = { message: originalMessage, context };
          }

          // 修订标记展示阶段不触发自动保存，避免版本变化导致审批冲突
          setSaveStatus('saved');
        } else if (type === 'insert') {
          // 插入模式：在指定位置插入内容，显示绿色高亮
          console.log('[NovelEditor] 应用插入模式修订标记');

          // 🔧 修复：使用 ProseMirror Transaction API 确保原子性操作
          const { state, view } = editor;
          const { tr } = state;
          const aiInsertedMark = state.schema.marks.aiInserted;
          const aiRevisionIdMark = state.schema.marks.aiRevisionId;

          if (!aiInsertedMark) {
            console.error('[NovelEditor] aiInserted 标记扩展未正确注册');
            return;
          }

          const insertPos = resolvedPosition?.from ?? state.doc.content.size;
          const insertPosition = resolvedPosition ?? { from: insertPos, to: insertPos };
          const textContent = replacement || '';

          withAutoSaveSuppressed(() => {
            // 🔧 修复：处理包含换行符的文本
            if (textContent.includes('\n')) {
              // 包含换行符时，用 insertContent 处理多段落
              const endPos = insertPos + textContent.length;
              editor.chain()
                .focus()
                .setTextSelection(insertPos)
                .insertContent(textContent)
                .setTextSelection({ from: insertPos, to: endPos })
                .setMark('aiInserted')
                .setMark('aiRevisionId', { revisionId: rid })
                .run();
            } else {
              // 无换行符时，使用原子事务
              const marks = [aiInsertedMark.create()];
              if (aiRevisionIdMark) {
                marks.push(aiRevisionIdMark.create({ revisionId: rid }));
              }
              const insertedText = state.schema.text(textContent, marks);
              tr.insert(insertPos, insertedText);
              view.dispatch(tr);
            }
          });

          // 计算操作栏位置（使用 requestAnimationFrame 确保 DOM 已重排）
          requestAnimationFrame(() => {
            try {
              const coords = view.coordsAtPos(insertPos);
              setRevisionBarPosition({
                top: coords.top - 40,  // 显示在内容上方，避免遮挡高亮内容
                left: coords.left
              });
            } catch (e) {
              console.warn('[NovelEditor] 无法计算修订栏位置:', e);
            }
          });

          // 设置活跃修订
          setActiveRevision({
            id: rid,
            requestId: requestIdValue,
            type: 'insert',
            position: insertPosition,
            replacement,
            originalMessage,
            context
          });
          appliedRevisionIdsRef.current.add(rid);

          if (originalMessage && context) {
            lastRevisionContextRef.current = { message: originalMessage, context };
          }

          // 修订标记展示阶段不触发自动保存，避免版本变化导致审批冲突
          setSaveStatus('saved');
        }

        toast.info(t('editor.aiPanel.confirmRevision'));
      } catch (error) {
        console.error('[NovelEditor] 应用修订标记失败:', error);
        toast.error(t('editor.aiMenu.revisionFailed'));
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

          toast.success(t('editor.aiMenu.appliedRewrite'));
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

          toast.success(t('editor.aiMenu.appliedRewrite'));
        } else {
          console.warn('[NovelEditor] 未找到原文本，可能已被修改');
          toast.warning(t('editor.aiMenu.originalChanged'));
        }
      } catch (error) {
        console.error('[NovelEditor] 应用改写失败:', error);
        toast.error(t('editor.aiMenu.applyFailed'));
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

        toast.success(t('editor.aiMenu.appliedContinue'));
      } catch (error) {
        console.error('[NovelEditor] 应用续写失败:', error);
        toast.error(t('editor.aiMenu.continueFailed2'));
      }
    };

    // v7.6: 采纳修订事件处理 - 直接操作编辑器中的修订标记
    const handleAcceptRevisionEvent = (event: Event) => {
      console.log('[NovelEditor] 收到采纳修订请求');
      const isBatch = event.type === 'agent-accept-all-revisions';
      const customEvent = event as CustomEvent<{
        request_id?: string;
        revision_id?: string;
        chapter_id?: string;
        requestId?: string;
        revisionId?: string;
        chapterId?: string;
      }>;
      const detail = customEvent.detail || {};
      const targetChapterId = detail.chapter_id || detail.chapterId;
      const revisionIds = [
        detail.request_id,
        detail.revision_id,
        detail.requestId,
        detail.revisionId
      ].filter(Boolean) as string[];

      if (!isBatch && targetChapterId && chapterId && targetChapterId !== chapterId) {
        if (revisionIds.length > 0) {
          clearPendingRevisions(revisionIds);
        }
        return;
      }

      try {
        const currentHtml = editor.getHTML();
        const nextHtml = applyRevisionDecisionToHtml(
          currentHtml,
          'accept',
          isBatch ? undefined : (revisionIds.length > 0 ? revisionIds : undefined)
        );

        editor.commands.setContent(nextHtml);
        revisionSaveBlockedRef.current = false;

        const pendingIds = isBatch
          ? pendingCrossChapterRevisions.map((revision) => revision.revisionId)
          : revisionIds.length > 0 ? revisionIds : getPendingRevisionIdsForChapter(chapterId);
        clearPendingRevisions(pendingIds);

        // 触发保存
        setSaveStatus('unsaved');
        if (autoSave) {
          debouncedSave(editor);
        }

        // 清理状态
        setActiveRevision(null);
        setRevisionBarPosition(null);

        toast.success(t('editor.aiPanel.revisionAccepted'));
      } catch (error) {
        console.error('[NovelEditor] 采纳修订失败:', error);
        toast.error(t('editor.aiMenu.applyFailed'));
      }
    };

    // v7.6: 弃用修订事件处理 - 直接操作编辑器中的修订标记
    const handleDiscardRevisionEvent = (event: Event) => {
      console.log('[NovelEditor] 收到弃用修订请求');
      const isBatch = event.type === 'agent-discard-all-revisions';
      const customEvent = event as CustomEvent<{
        request_id?: string;
        revision_id?: string;
        chapter_id?: string;
        requestId?: string;
        revisionId?: string;
        chapterId?: string;
      }>;
      const detail = customEvent.detail || {};
      const targetChapterId = detail.chapter_id || detail.chapterId;
      const revisionIds = [
        detail.request_id,
        detail.revision_id,
        detail.requestId,
        detail.revisionId
      ].filter(Boolean) as string[];

      if (!isBatch && targetChapterId && chapterId && targetChapterId !== chapterId) {
        if (revisionIds.length > 0) {
          clearPendingRevisions(revisionIds);
        }
        return;
      }

      try {
        const currentHtml = editor.getHTML();
        const nextHtml = applyRevisionDecisionToHtml(
          currentHtml,
          'discard',
          isBatch ? undefined : (revisionIds.length > 0 ? revisionIds : undefined)
        );

        editor.commands.setContent(nextHtml);
        revisionSaveBlockedRef.current = false;

        const pendingIds = isBatch
          ? pendingCrossChapterRevisions.map((revision) => revision.revisionId)
          : revisionIds.length > 0 ? revisionIds : getPendingRevisionIdsForChapter(chapterId);
        clearPendingRevisions(pendingIds);

        // 清理状态
        setActiveRevision(null);
        setRevisionBarPosition(null);

        toast.info(t('editor.aiPanel.revisionDiscarded'));
      } catch (error) {
        console.error('[NovelEditor] 弃用修订失败:', error);
        toast.error(t('editor.aiMenu.applyFailed'));
      }
    };

    // v7.2: 撤销修订事件处理（用于已采纳后的撤销）
    const handleUndoRevision = (event: Event) => {
      const customEvent = event as CustomEvent<{
        itemId?: string;
        request_id?: string;
        revisionType?: string;
        originalContent?: string;
        newContent?: string;
        position?: { from: number; to: number };
      }>;

      const { revisionType, originalContent, newContent, position } = customEvent.detail;

      console.log('[NovelEditor] 收到撤销修订请求:', {
        revisionType,
        hasOriginal: originalContent !== undefined,
        hasNew: newContent !== undefined,
        position
      });

      // v7.6: 如果没有详细数据，尝试直接操作编辑器中的修订标记
      if (!position && !revisionType) {
        console.log('[NovelEditor] 无详细数据，尝试直接操作修订标记');
        handleDiscardRevisionEvent(event);
        return;
      }

      // v7.2: 空快照保护 - 如果没有足够的快照数据，无法撤销
      if (!position) {
        console.warn('[NovelEditor] 撤销失败：缺少位置信息');
        toast.warning('无法撤销：缺少位置信息');
        return;
      }

      try {
        if (revisionType === 'append' || revisionType === 'insert') {
          // 续写/插入类型：删除新增的内容
          if (newContent) {
            const deleteFrom = position.from;
            const deleteTo = position.from + newContent.length;

            // 边界检查
            const docSize = editor.state.doc.content.size;
            if (deleteFrom < 0 || deleteTo > docSize) {
              console.warn('[NovelEditor] 撤销失败：位置超出文档范围', { deleteFrom, deleteTo, docSize });
              toast.warning('无法撤销：内容已被修改');
              return;
            }

            editor.chain()
              .focus()
              .setTextSelection({ from: deleteFrom, to: deleteTo })
              .deleteSelection()
              .run();
            toast.info('已撤销修订');
          } else {
            console.warn('[NovelEditor] 撤销失败：缺少新内容快照');
            toast.warning('无法撤销：缺少内容快照');
            return;
          }
        } else if (revisionType === 'replace') {
          // 替换类型：恢复原始内容
          if (originalContent === undefined && !newContent) {
            console.warn('[NovelEditor] 撤销失败：缺少快照数据');
            toast.warning('无法撤销：缺少内容快照');
            return;
          }

          // 先删除新内容（如果有）
          if (newContent) {
            const deleteFrom = position.from;
            const deleteTo = position.from + newContent.length;

            // 边界检查
            const docSize = editor.state.doc.content.size;
            if (deleteFrom >= 0 && deleteTo <= docSize) {
              editor.chain()
                .focus()
                .setTextSelection({ from: deleteFrom, to: deleteTo })
                .deleteSelection()
                .run();
            }
          }

          // 插入原始内容（如果有）
          if (originalContent) {
            editor.chain()
              .setTextSelection(position.from)
              .insertContent(originalContent)
              .run();
          }
          toast.info('已撤销修订');
        } else {
          // 不支持的修订类型（create/rename）
          console.warn('[NovelEditor] 不支持的修订类型撤销:', revisionType);
          toast.warning(`暂不支持撤销"${revisionType}"类型的修订`);
          return;
        }

        setSaveStatus('unsaved');
        if (autoSave) {
          debouncedSave(editor);
        }
      } catch (error) {
        console.error('[NovelEditor] 撤销修订失败:', error);
        toast.error('撤销修订失败');
      }
    };

    const handleJumpRevision = (event: Event) => {
      const customEvent = event as CustomEvent<RevisionJumpRequest & { workId?: string }>;
      const { workId: targetWorkId, chapterId: targetChapterId, revisionId, requestId, position } = customEvent.detail || {};
      if (targetWorkId && workId && targetWorkId !== workId) return;
      pendingRevisionJumpRef.current = {
        chapterId: targetChapterId,
        revisionId,
        requestId,
        position
      };
      attemptPendingRevisionJump();
    };

    window.addEventListener('agent-show-revision', handleShowRevision as EventListener);
    window.addEventListener('agent-replace-text', handleAgentReplace as EventListener);
    window.addEventListener('agent-append-text', handleAgentAppend as EventListener);
    window.addEventListener('agent-undo-revision', handleUndoRevision as EventListener);
    window.addEventListener('agent-jump-revision', handleJumpRevision as EventListener);
    window.addEventListener('agent-accept-revision', handleAcceptRevisionEvent as EventListener);
    window.addEventListener('agent-accept-all-revisions', handleAcceptRevisionEvent as EventListener);  // v8.1: 批量采纳
    window.addEventListener('agent-discard-revision', handleDiscardRevisionEvent as EventListener);
    window.addEventListener('agent-discard-all-revisions', handleDiscardRevisionEvent as EventListener);  // v8.1: 批量撤销

    return () => {
      window.removeEventListener('agent-show-revision', handleShowRevision as EventListener);
      window.removeEventListener('agent-replace-text', handleAgentReplace as EventListener);
      window.removeEventListener('agent-append-text', handleAgentAppend as EventListener);
      window.removeEventListener('agent-undo-revision', handleUndoRevision as EventListener);
      window.removeEventListener('agent-jump-revision', handleJumpRevision as EventListener);
      window.removeEventListener('agent-accept-revision', handleAcceptRevisionEvent as EventListener);
      window.removeEventListener('agent-accept-all-revisions', handleAcceptRevisionEvent as EventListener);  // v8.1: 批量采纳
      window.removeEventListener('agent-discard-revision', handleDiscardRevisionEvent as EventListener);
      window.removeEventListener('agent-discard-all-revisions', handleDiscardRevisionEvent as EventListener);  // v8.1: 批量撤销
    };
  }, [
    editor,
    autoSave,
    toast,
    debouncedSave,
    chapterId,
    enqueuePendingCrossChapterRevision,
    pendingCrossChapterRevisions,
    clearPendingRevisions,
    getPendingRevisionIdsForChapter,
    applyRevisionDecisionToHtml,
    attemptPendingRevisionJump,
    workId,
    t
  ]);

  // 🆕 打开 Ask AI：保存选区并通知右侧 Agent
  const handleOpenInlineAI = useCallback(() => {
    if (!editor) return;

    // 获取选中文字的位置，用于定位浮动输入框
    const { from, to } = editor.state.selection;

    // 如果没有选中文字，不打开
    if (from === to) {
      toast.warning(t('editor.aiPanel.selectTextFirst'));
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
  const handleAcceptRevision = useCallback(async () => {
    if (!activeRevision || !editor) return;

    const { id, requestId, type, position } = activeRevision;

    if (requestId) {
      try {
        await agentApi.submitApprovalResponse({
          request_id: requestId,
          approved: true,
        });
      } catch (error) {
        console.error('[NovelEditor] 采纳修订写入失败:', error);
        toast.error(t('editor.aiMenu.applyFailed'));
        return;
      }
    }

    console.log('[NovelEditor] 采纳修订:', { id, type, position });

    try {
      const currentHtml = editor.getHTML();
      const revisionIds = [requestId, id].filter(Boolean) as string[];
      const nextHtml = applyRevisionDecisionToHtml(
        currentHtml,
        'accept',
        revisionIds.length > 0 ? revisionIds : undefined
      );

      editor.commands.setContent(nextHtml);
      revisionSaveBlockedRef.current = false;

      const pendingIds = revisionIds.length > 0 ? revisionIds : getPendingRevisionIdsForChapter(chapterId);
      clearPendingRevisions(pendingIds);

      // 触发保存
      setSaveStatus('unsaved');
      if (autoSave) {
        debouncedSave(editor);
      }

      // 清理状态
      setActiveRevision(null);
      setRevisionBarPosition(null);
      lastRevisionContextRef.current = null;

      toast.success(t('editor.aiPanel.revisionAccepted'));
    } catch (error) {
      console.error('[NovelEditor] 采纳修订失败:', error);
      toast.error(t('editor.aiMenu.applyFailed'));
    }
  }, [activeRevision, editor, autoSave, debouncedSave, toast, chapterId, getPendingRevisionIdsForChapter, clearPendingRevisions, t]);

  // 🆕 弃用修订 - 移除新内容，恢复原文
  const handleDiscardRevision = useCallback(async () => {
    if (!activeRevision || !editor) return;

    const { id, requestId, type, position } = activeRevision;

    if (requestId) {
      try {
        await agentApi.submitApprovalResponse({
          request_id: requestId,
          approved: false,
        });
      } catch (error) {
        console.error('[NovelEditor] 弃用修订写入失败:', error);
        toast.error(t('editor.aiMenu.applyFailed'));
        return;
      }
    }

    console.log('[NovelEditor] 弃用修订:', { id, type, position });

    try {
      const currentHtml = editor.getHTML();
      const revisionIds = [requestId, id].filter(Boolean) as string[];
      const nextHtml = applyRevisionDecisionToHtml(
        currentHtml,
        'discard',
        revisionIds.length > 0 ? revisionIds : undefined
      );

      editor.commands.setContent(nextHtml);
      revisionSaveBlockedRef.current = false;

      const pendingIds = revisionIds.length > 0 ? revisionIds : getPendingRevisionIdsForChapter(chapterId);
      clearPendingRevisions(pendingIds);

      // 清理状态
      setActiveRevision(null);
      setRevisionBarPosition(null);
      lastRevisionContextRef.current = null;

      toast.info(t('editor.aiPanel.revisionDiscarded'));
    } catch (error) {
      console.error('[NovelEditor] 弃用修订失败:', error);
      toast.error(t('editor.aiMenu.applyFailed'));
    }
  }, [activeRevision, editor, toast, chapterId, getPendingRevisionIdsForChapter, clearPendingRevisions, t]);

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
      toast.warning(t('editor.aiPanel.cannotRegenerate'));
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

    toast.info(t('editor.aiPanel.sentToAI'));
  }, [editor, inlineAISelectionSnapshot, onInlineAISend, toast, setRightSidebarType]);

  // 🆕 更新 handleInlineAISend ref（用于 handleRegenerateRevision 调用）
  useEffect(() => {
    handleInlineAISendRef.current = handleInlineAISend;
  }, [handleInlineAISend]);

  if (!editor) {
    return (
      <div className="flex items-center justify-center min-h-[500px] dark:bg-slate-900">
        <div className="text-gray-500 dark:text-slate-400">{t('editor.loadingEditor')}</div>
      </div>
    );
  }

  const displayChapterTitle = chapterTitle
    ? chapterTitle.replace(/^第\s*[\d一二三四五六七八九十百千零〇两]+\s*章[\s:：\-—·.]*?/, '')
    : '';
  const showChapterHeader = typeof chapterOrder === 'number' && displayChapterTitle;

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
          saveStatus={saveStatus}
          isEditorFullscreen={isAIPanelCollapsed}
          onToggleFullscreen={isAIPanelCollapsed ? onToggleAIPanel : onCollapseAIPanel}
        />

        {/* 编辑器内容区域 - 沉浸式画布 */}
        <div className="flex-1 overflow-y-auto bg-white dark:bg-slate-900">
          <div className="editor-canvas">
            {showChapterHeader && (
              <div className="chapter-header" aria-label="Chapter header">
                <div className="chapter-header__order">第{chapterOrder}章</div>
                <div className="chapter-header__rule">
                  <svg className="chapter-header__rule-svg" viewBox="0 0 240 14" aria-hidden="true">
                    <path d="M24 7 H216" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    <path d="M2 7 C6 3 12 3 20 7 C12 11 6 11 2 7 Z" fill="currentColor" />
                    <path d="M238 7 C234 3 228 3 220 7 C228 11 234 11 238 7 Z" fill="currentColor" />
                    <path d="M120 2 L126 7 L120 12 L114 7 Z" fill="currentColor" />
                  </svg>
                </div>
                <div className="chapter-header__title">{displayChapterTitle}</div>
              </div>
            )}
            <EditorContent editor={editor} className="editor-content-root" />
          </div>
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
