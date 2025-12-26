import React, { useState, useRef, useEffect, useLayoutEffect, useCallback, useMemo, KeyboardEvent } from 'react';
import { createPortal } from 'react-dom';
import { Button } from '../ui/button';
import { Bot, Send, Loader2, Square, BookOpen, Sparkles, ChevronRight, ChevronLeft, Tag, X, Copy } from 'lucide-react';
import { useAgentChat } from '../../hooks/useAgentChat';
import { useEditorStore } from '../../store/editorStore';
import { useChatDraftStore } from '../../store/chatDraftStore';
import type { AgentChatRequest } from '../../types/agent';
import type { AgentMode } from '../agent/ModeSelector';
import ModeSelector from '../agent/ModeSelector';
import ActivityStream from '../agent/ActivityStream';  // ✅ 导入ActivityStream
import { ExecutionFlow } from '../agent/ExecutionFlow';  // ✅ v5.0: 执行轨迹可视化
import AgentEditConfirmDialog from '../agent/AgentEditConfirmDialog';  // ✅ 导入确认对话框
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';  // ✅ 支持 GFM 表格
import { knowledgeApi } from '@/services/knowledgeApi';

interface AIPanelProps {
  workId: string;
  chapterId?: string;
  sessionId?: string;
  onTitleChange?: (title: string) => void;
  /** 是否为当前活动面板（只有活动面板才处理 InlineAI 事件） */
  isActive?: boolean;
}

// Markdown渲染组件
const MarkdownContent: React.FC<{ content: string }> = ({ content }) => {
  return (
    <div className="text-[14px] leading-relaxed markdown-content">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={{
          // 代码块
          code({ node, inline, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
              <SyntaxHighlighter
                style={vscDarkPlus}
                language={match[1]}
                PreTag="div"
                className="rounded-md text-[12px] my-1.5"
                {...props}
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            ) : (
              <code className="bg-zinc-100 text-zinc-800 px-1 py-0.5 rounded text-[12px] font-mono" {...props}>
                {children}
              </code>
            );
          },
          // 段落
          p({ children }) {
            return <p className="mb-1.5 last:mb-0 text-[14px]">{children}</p>;
          },
          // 标题
          h1({ children }) {
            return <h1 className="text-[15px] font-semibold mb-1.5 mt-2 first:mt-0">{children}</h1>;
          },
          h2({ children }) {
            return <h2 className="text-[14px] font-semibold mb-1.5 mt-2 first:mt-0">{children}</h2>;
          },
          h3({ children }) {
            return <h3 className="text-[14px] font-medium mb-1 mt-1.5 first:mt-0">{children}</h3>;
          },
          // 列表
          ul({ children }) {
            return <ul className="list-disc list-inside mb-1.5 space-y-0.5 text-[14px]">{children}</ul>;
          },
          ol({ children }) {
            return <ol className="list-decimal list-inside mb-1.5 space-y-0.5 text-[14px]">{children}</ol>;
          },
          li({ children }) {
            return <li className="text-[14px]">{children}</li>;
          },
          // 链接
          a({ href, children }) {
            return (
              <a href={href} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline text-[14px]">
                {children}
              </a>
            );
          },
          // 引用
          blockquote({ children }) {
            return <blockquote className="border-l-2 border-zinc-300 pl-2 my-1.5 text-zinc-600 text-[14px]">{children}</blockquote>;
          },
          // 分割线
          hr() {
            return <hr className="my-2 border-zinc-200" />;
          },
          // 表格
          table({ children }) {
            return <table className="border-collapse border border-zinc-200 my-1.5 text-[12px]">{children}</table>;
          },
          thead({ children }) {
            return <thead className="bg-zinc-50">{children}</thead>;
          },
          th({ children }) {
            return <th className="border border-zinc-200 px-1.5 py-0.5 font-semibold text-[12px]">{children}</th>;
          },
          td({ children }) {
            return <td className="border border-zinc-200 px-1.5 py-0.5 text-[12px]">{children}</td>;
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

type AtCommandStage = 'root' | 'knowledge';

type RootCommandOption = {
  key: 'knowledge' | 'optimization';
  label: string;
  description: string;
  icon: React.ReactNode;
  hasChildren?: boolean;
};

const ROOT_OPTIONS: RootCommandOption[] = [
  {
    key: 'knowledge',
    label: '@Knowledge',
    description: '引用知识库里的文档',
    icon: <BookOpen className="w-4 h-4" />,
    hasChildren: true,
  },
  {
    key: 'optimization',
    label: '@optimization',
    description: '开启 AI 去痕迹优化',
    icon: <Sparkles className="w-4 h-4" />,
  },
];

const AT_CHARS = ['@', '＠'];

const extractKnowledgeTags = (value: string): string[] => {
  const regex = /@'([^']+)'/g;
  const tags = new Set<string>();
  let match: RegExpExecArray | null;
  while ((match = regex.exec(value))) {
    if (match[1]) tags.add(match[1]);
  }
  return Array.from(tags);
};

const escapeRegExp = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// 全局去重集合，确保跨组件只处理一次 inline-ai 消息
const getInlineAIProcessedSet = (): Set<string> => {
  if (typeof window === 'undefined') return new Set<string>();
  if (!(window as any).__inlineAIProcessed__) {
    (window as any).__inlineAIProcessed__ = new Set<string>();
  }
  return (window as any).__inlineAIProcessed__ as Set<string>;
};

export function AIPanel({ workId, chapterId, sessionId, onTitleChange, isActive = true }: AIPanelProps) {
  const {
    messages,
    isLoading,
    error,
    suggestedActions,
    tasks,
    currentTaskId,
    activities,
    flowItems,  // v5.0: 执行轨迹项
    sendMessageStream,
    stopStreaming,
    pendingApproval,
    submitApproval,
  } = useAgentChat({ workId, chapterId, sessionId });  // 🆕 传递workId和chapterId进行会话隔离

  // 获取当前章节内容，便于 @optimization 直接调用去痕迹接口
  const { currentChapter } = useEditorStore();

  // 获取草稿 store 方法，用于会话切换时保存/恢复输入状态
  const { saveDraft, getDraft, clearDraft } = useChatDraftStore();

  const [inputValue, setInputValue] = useState('');
  const [mode, setMode] = useState<AgentMode>('plan'); // ✅ Agent执行模式：plan(固定规划) | agent(DeepAgent反思)
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const shouldAutoScrollRef = useRef(true); // 用于追踪是否应该自动滚动
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const [atMenuOpen, setAtMenuOpen] = useState(false);
  const [atStage, setAtStage] = useState<AtCommandStage>('root');
  const [atQuery, setAtQuery] = useState('');
  const [highlightIndex, setHighlightIndex] = useState(0);
  const [knowledgeDocs, setKnowledgeDocs] = useState<Array<{ id: string; title: string; tags?: string[] }>>([]);
  const [knowledgeLoading, setKnowledgeLoading] = useState(false);
  const [knowledgeError, setKnowledgeError] = useState<string | null>(null);
  const [knowledgeLoadedOnce, setKnowledgeLoadedOnce] = useState(false);
  const [knowledgePage, setKnowledgePage] = useState(1);
  const [knowledgeHasMore, setKnowledgeHasMore] = useState(false);
  const [atTriggerIndex, setAtTriggerIndex] = useState<number | null>(null);
  const [menuPosition, setMenuPosition] = useState<{ left: number; top: number; width: number } | null>(null);
  const [menuHeight, setMenuHeight] = useState<number>(220);
  const menuRef = useRef<HTMLDivElement>(null);
  const knowledgeListRef = useRef<HTMLDivElement>(null);

  const [selectedDocs, setSelectedDocs] = useState<Array<{ id: string; title: string }>>([]);
  const [optimizationSelected, setOptimizationSelected] = useState(false);
  const [selectionContext, setSelectionContext] = useState<{
    selected_text?: string;
    selected_text_html?: string;
    selection_position?: { from: number; to: number };
  } | null>(null);

  // 组件挂载时恢复草稿
  useEffect(() => {
    if (sessionId) {
      const draft = getDraft(sessionId);
      if (draft) {
        setInputValue(draft.inputValue);
        setSelectedDocs(draft.selectedDocs);
        setOptimizationSelected(draft.optimizationSelected);
        setSelectionContext(draft.selectionContext);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // 只在挂载时执行一次

  // 实时保存草稿：每次输入变化时自动保存
  useEffect(() => {
    if (!sessionId) return;

    const hasContent = inputValue.trim() || selectedDocs.length > 0 || optimizationSelected || selectionContext;

    if (hasContent) {
      saveDraft(sessionId, {
        inputValue,
        selectedDocs,
        optimizationSelected,
        selectionContext,
      });
    } else {
      // 如果没有内容，清除草稿
      clearDraft(sessionId);
    }
  }, [sessionId, inputValue, selectedDocs, optimizationSelected, selectionContext, saveDraft, clearDraft]);

  // ✅ 流式输出：后端逐字发送，前端直接显示（无需前端打字机效果）

  const copyMessage = useCallback(async (content: string) => {
    try {
      await navigator.clipboard.writeText(content || '');
    } catch (err) {
      console.error('Copy failed:', err);
    }
  }, []);

  const containsAt = useMemo(() => AT_CHARS.some((c) => inputValue.includes(c)), [inputValue]);
  // 去痕长度保护与提示
  const MAX_HUMANIZE_CHARS = 5000;
  const rawChapterContent = currentChapter?.content?.trim() || '';
  const truncatedCount =
    optimizationSelected && rawChapterContent.length > MAX_HUMANIZE_CHARS
      ? rawChapterContent.length - MAX_HUMANIZE_CHARS
      : 0;
  const safeChapterContent =
    optimizationSelected && rawChapterContent
      ? rawChapterContent.slice(0, MAX_HUMANIZE_CHARS)
      : undefined;

  const filteredRootOptions = useMemo(() => {
    const query = atQuery.trim().toLowerCase();
    if (!query) return ROOT_OPTIONS;
    return ROOT_OPTIONS.filter(
      (opt) => opt.label.toLowerCase().includes(query) || opt.description.toLowerCase().includes(query)
    );
  }, [atQuery]);

  const filteredKnowledgeDocs = useMemo(() => {
    const query = atQuery.trim().toLowerCase();
    if (!query) return knowledgeDocs;
    return knowledgeDocs.filter((doc) => doc.title.toLowerCase().includes(query));
  }, [atQuery, knowledgeDocs]);

  // 监控：activities状态变化（仅在有数据时记录）
  useEffect(() => {
    if (activities.length > 0) {
      console.log('[AIPanel] 活动流更新:', activities.length, '个活动');
    }
  }, [activities]);

  // ??????????????
  const lastSentTitleRef = useRef<string | null>(null);
  useEffect(() => {
    if (!onTitleChange || messages.length === 0) return;
    if (typeof window !== 'undefined') {
      try {
        if (localStorage.getItem(`agent_session_title_locked_${sessionId}`) === '1') {
          return;
        }
      } catch {
        /* ignore */
      }
    }

    const firstUserMessage = messages.find((m) => m.role === 'user');
    if (!firstUserMessage) return;

    const content = firstUserMessage.content.trim();
    const title = content.length <= 30 ? content : `${content.substring(0, 30)}...`;

    if (lastSentTitleRef.current === title) return;
    lastSentTitleRef.current = title;
    onTitleChange(title);
  }, [messages, onTitleChange, sessionId]);

  // 监控：mode切换
  useEffect(() => {
    console.log('[AIPanel] 模式:', mode);
  }, [mode]);

  // 🆕 定义 handleSendWithContext 用于处理带上下文的消息（InlineAI）
  const handleSendWithContext = useCallback(async (message: string, context?: any) => {
    if (!message.trim()) return;

    console.log('[AIPanel] handleSendWithContext 调用:', { message, context });
    const backendMode: AgentChatRequest['mode'] = mode === 'agent' ? 'react' : 'planning';

    // 🔑 固定 payload 结构：将选区信息放入独立的 selection 字段
    // 避免将选中文本混入 prompt/chapter_context 导致被覆盖或结构混乱
    const selectionData = context?.selected_text ? {
      text: context.selected_text,
      html: context.selected_text_html || context.selected_text,
      from: context.selection_position?.from,
      to: context.selection_position?.to,
    } : null;

    const request: AgentChatRequest = {
      message,
      mode: backendMode,
      work_id: workId,
      chapter_id: chapterId,
      enable_reflection: mode === 'agent',
      context: {
        ...context,
        // 🔑 独立的 selection 字段（推荐结构）
        selection: selectionData,
        // 保留 selected_text 字段以兼容旧逻辑
        selected_text: context?.selected_text,
        selection_position: context?.selection_position,
        // chapter_context 只放章节标识，不混入选中文本
        chapter_context: chapterId ? `当前章节ID: ${chapterId}` : undefined,
        // 🔑 如果有选中文本，添加结构化的指令上下文
        instruction_context: context?.selected_text
          ? `用户选中了以下文本进行操作:\n---\n${context.selected_text}\n---\n用户指令: ${message}`
          : undefined,
      },
    };

    console.log('[AIPanel] 🔑 固定结构 payload:', {
      message,
      selection: selectionData,
      hasSelectedText: !!context?.selected_text,
    });

    // 用户发送消息时，标记应该自动滚动
    shouldAutoScrollRef.current = true;

    try {
      await sendMessageStream(request);
    } catch (err) {
      console.error('[AIPanel] Failed to send message:', err);
    }
  }, [mode, workId, chapterId, sendMessageStream]);

  // 🆕 监听来自编辑器 InlineAI 的消息（只有活动面板才处理）
  useEffect(() => {
    // 非活动面板不设置监听器
    if (!isActive) {
      console.log('[AIPanel] 非活动面板，跳过 InlineAI 监听设置');
      return;
    }

    console.log('[AIPanel] 挂载 InlineAI 事件监听（活动面板）');

    // 消费队列中的遗留消息
    const queue: any[] = (window as any).__inlineAIQueue__ || [];
    const consumed = getInlineAIProcessedSet();

    queue.forEach((item) => {
      const rid = item?.requestId || JSON.stringify(item);
      if (!consumed.has(rid)) {
        consumed.add(rid);
        console.log('[AIPanel] consuming queued inline-ai payload', item);

        // 🔑 直接传入原始 context，handleSendWithContext 会正确处理 selection 字段
        handleSendWithContext(item.message || '', item.context || {});
      }
    });
    (window as any).__inlineAIQueue__ = [];

    // 暴露全局回调
    (window as any).__agentInlineSend__ = (msg: string, ctx?: any, requestId?: string) => {
      const rid = requestId || `inline-${Date.now()}-${Math.random().toString(16).slice(2)}`;
      if (consumed.has(rid)) return;
      consumed.add(rid);
      console.log('[AIPanel] __agentInlineSend__ invoked', { msg, ctx, rid });

      // 🔑 直接传入原始 context，handleSendWithContext 会正确处理 selection 字段
      handleSendWithContext(msg, ctx);
    };

    // 监听 inline-ai-send 事件
    const handleInlineAIMessage = (event: CustomEvent<{
      message: string;
      context: {
        selected_text?: string;
        selected_text_html?: string;
        selection_position?: { from: number; to: number };
        knowledge_doc_ids?: string[];
      };
      requestId?: string;
    }>) => {
      const { message, context, requestId } = event.detail;
      console.log('[AIPanel] 收到 InlineAI 消息:', { message, context, requestId });

      // 去重检查
      const rid = requestId || `inline-${Date.now()}`;
      if (consumed.has(rid)) {
        console.log('[AIPanel] 消息已处理，跳过:', rid);
        return;
      }
      consumed.add(rid);

      // 🔑 直接传入原始 context，handleSendWithContext 会正确处理 selection 字段
      handleSendWithContext(message, context);
    };

    window.addEventListener('inline-ai-send', handleInlineAIMessage as EventListener);

    return () => {
      window.removeEventListener('inline-ai-send', handleInlineAIMessage as EventListener);
      delete (window as any).__agentInlineSend__;
      console.log('[AIPanel] 卸载 InlineAI 事件监听');
    };
  }, [handleSendWithContext, isActive]);

  // 🆕 监听 InlineAI intent（仅填充引用，不立即发送），全局 + 队列兜底
  useEffect(() => {
    if (!isActive) return;
    const intentQueue: any[] = (window as any).__inlineAIIntentQueue__ || [];
    if (intentQueue.length > 0) {
      const last = intentQueue[intentQueue.length - 1];
      console.log('[AIPanel] intentQueue consumed (AIPanel):', last);
      setSelectionContext(last || null);
      (window as any).__inlineAIIntentQueue__ = [];
    }

    (window as any).__agentInlineIntent__ = (ctx?: {
      selected_text?: string;
      selected_text_html?: string;
      selection_position?: { from: number; to: number };
    }) => {
      setSelectionContext(ctx || null);
    };

    const handleInlineAIIntent = (event: CustomEvent<{
      selected_text?: string;
      selected_text_html?: string;
      selection_position?: { from: number; to: number };
    }>) => {
      console.log('[AIPanel] 收到 InlineAI intent:', event.detail);
      setSelectionContext(event.detail || null);
    };

    window.addEventListener('inline-ai-intent', handleInlineAIIntent as EventListener);
    return () => {
      window.removeEventListener('inline-ai-intent', handleInlineAIIntent as EventListener);
      delete (window as any).__agentInlineIntent__;
    };
  }, [isActive]);

  // 检测用户是否在底部
  const checkIfAtBottom = useCallback(() => {
    const container = messagesContainerRef.current;
    if (!container) return false;

    // 检测滚动位置是否接近底部（允许50px的误差）
    const threshold = 50;
    const isAtBottom = container.scrollHeight - container.scrollTop - container.clientHeight < threshold;
    return isAtBottom;
  }, []);

  // 滚动到底部
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  // 监听滚动事件，更新是否应该自动滚动的标志
  useEffect(() => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      shouldAutoScrollRef.current = checkIfAtBottom();
    };

    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, [checkIfAtBottom]);

  // 当消息或任务更新时，如果用户在底部就自动滚动
  useEffect(() => {
    if (shouldAutoScrollRef.current) {
      scrollToBottom();
    }
  }, [messages, tasks, scrollToBottom]);

  // ✅ 流式输出：后端已实现逐字发送，前端直接使用 message.content

  const repositionMenu = useCallback(() => {
    const inputEl = inputRef.current;
    if (!inputEl) return;
    const rect = inputEl.getBoundingClientRect();
    const estimatedHeight = menuHeight || 220;
    const margin = 6;
    const belowSpace = window.innerHeight - rect.bottom;
    let top: number;
    if (belowSpace >= estimatedHeight + margin) {
      top = rect.bottom + margin;
    } else {
      top = Math.max(rect.top - estimatedHeight - margin, margin);
    }
    setMenuPosition({
      left: rect.left,
      top,
      width: rect.width,
    });
  }, [menuHeight]);

  const updateAtState = useCallback(
    (value: string, caret: number | null) => {
      if (caret === null) return;

      const lastIndex = Math.max(...AT_CHARS.map((c) => value.lastIndexOf(c, caret - 1)));
      if (lastIndex === -1) {
        setAtMenuOpen(false);
        return;
      }

      const tokenText = value.slice(lastIndex + 1, caret);
      if (tokenText.includes(' ') || tokenText.includes('\n')) {
        setAtMenuOpen(false);
        return;
      }

      setAtMenuOpen(true);
      setAtTriggerIndex(lastIndex);
      setAtQuery(tokenText);
      setHighlightIndex(0);
      repositionMenu();
    },
    [repositionMenu]
  );

  const syncAtStateFromRef = useCallback(() => {
    const el = inputRef.current;
    const caret = el?.selectionStart ?? null;
    const value = el?.value ?? inputValue;
    updateAtState(value, caret);
  }, [inputValue, updateAtState]);

  useEffect(() => {
    if (!containsAt) {
      setAtMenuOpen(false);
      setAtStage('root');
      return;
    }
    syncAtStateFromRef();
  }, [containsAt, inputValue, syncAtStateFromRef]);

  useEffect(() => {
    if (!atMenuOpen) return;
    repositionMenu();
    if (menuRef.current) {
      const h = menuRef.current.getBoundingClientRect().height;
      if (h && Math.abs(h - menuHeight) > 2) {
        setMenuHeight(h);
      }
    }
    const handleWindow = () => repositionMenu();
    window.addEventListener('resize', handleWindow);
    window.addEventListener('scroll', handleWindow, true);
    return () => {
      window.removeEventListener('resize', handleWindow);
      window.removeEventListener('scroll', handleWindow, true);
    };
  }, [atMenuOpen, repositionMenu]);

  useEffect(() => {
    const loadDocs = async () => {
      if (knowledgeLoading) return;
      try {
        setKnowledgeLoading(true);
        setKnowledgeError(null);
        // 使用新的 getDocTitles API，返回 {id, title}[]
        const docs = await knowledgeApi.getDocTitles();
        console.log('[AIPanel] 获取知识库文档列表:', docs);
        setKnowledgeDocs(docs.map((d) => ({ id: d.id, title: d.title || '未命名文档' })));
        setKnowledgeHasMore(false);
      } catch (err: any) {
        const status = err?.response?.status;
        if (status === 404) {
          setKnowledgeDocs([]);
          setKnowledgeError(null);
        } else {
          setKnowledgeError(err?.message || '知识库文档获取失败');
        }
        setKnowledgeHasMore(false);
      } finally {
        setKnowledgeLoading(false);
        setKnowledgeLoadedOnce(true);
      }
    };

    if (atMenuOpen && atStage === 'knowledge' && !knowledgeLoading && !knowledgeLoadedOnce) {
      loadDocs();
    }
  }, [atMenuOpen, atStage, knowledgeLoading, knowledgeLoadedOnce]);

  const closeAtMenu = useCallback(() => {
    setAtMenuOpen(false);
    setAtStage('root');
    setAtQuery('');
    setHighlightIndex(0);
    setAtTriggerIndex(null);
    setKnowledgeLoadedOnce(false);
    setKnowledgePage(1);
    setKnowledgeHasMore(false);
  }, []);

  const stripCurrentToken = useCallback(() => {
    const el = inputRef.current;
    const caret = el?.selectionStart ?? inputValue.length;
    const trigger = atTriggerIndex ?? Math.max(...AT_CHARS.map((c) => inputValue.lastIndexOf(c, caret - 1)));
    if (trigger < 0) return inputValue;
    const rest = inputValue.slice(trigger);
    const nextSpaceIndex = rest.search(/[\s]/);
    const end = nextSpaceIndex === -1 ? inputValue.length : trigger + nextSpaceIndex;
    const before = inputValue.slice(0, trigger).trimEnd();
    const after = inputValue.slice(end).trimStart();
    const combined = before && after ? `${before} ${after}` : before || after;
    return combined;
  }, [atTriggerIndex, inputValue]);

  const handleRootOption = useCallback(
    (option: RootCommandOption) => {
      if (option.key === 'optimization') {
        setOptimizationSelected(true);
        setInputValue(stripCurrentToken());
        closeAtMenu();
        requestAnimationFrame(() => inputRef.current?.focus());
        return;
      }
      setAtStage('knowledge');
      setAtQuery('');
      setHighlightIndex(0);
      setAtMenuOpen(true);
      repositionMenu();
    },
    [closeAtMenu, repositionMenu, stripCurrentToken]
  );

  const handleKnowledgeSelect = useCallback(
    (doc: { id: string; title: string }) => {
      setSelectedDocs((prev) => (prev.find((d) => d.id === doc.id) ? prev : [...prev, doc]));
      setInputValue(stripCurrentToken());
      closeAtMenu();
      requestAnimationFrame(() => inputRef.current?.focus());
    },
    [closeAtMenu, stripCurrentToken]
  );

  const adjustInputHeight = useCallback(() => {
    const el = inputRef.current;
    if (!el) return;

    // 如果没有内容，直接设置为最小高度
    if (!el.value || el.value.trim() === '') {
      el.style.height = '32px';
      el.style.overflowY = 'hidden';
      return;
    }

    // 先重置高度，让 scrollHeight 能正确计算实际内容高度
    el.style.height = '32px';
    const maxH = 200;
    // 根据实际内容计算高度
    const contentHeight = el.scrollHeight;
    const nextHeight = Math.min(contentHeight, maxH);
    el.style.height = `${Math.max(nextHeight, 32)}px`;
    el.style.overflowY = contentHeight > maxH ? 'auto' : 'hidden';
  }, []);

  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      const value = e.target.value;
      setInputValue(value);
      updateAtState(value, e.target.selectionStart ?? value.length);
      adjustInputHeight();
    },
    [adjustInputHeight, updateAtState]
  );

  const removeKnowledgeTag = useCallback((tag: string) => {
    setSelectedDocs((prev) => prev.filter((t) => t.id !== tag));
  }, []);

  const removeOptimization = useCallback(() => {
    setOptimizationSelected(false);
  }, []);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const message = inputValue.trim();
    const knowledgeDocIds = selectedDocs.map((d) => d.id);
    const useOptimization = optimizationSelected;
    const chapterContent = currentChapter?.content?.trim();
    const MAX_HUMANIZE_CHARS = 5000;
    const safeChapterContent =
      chapterContent && chapterContent.length > MAX_HUMANIZE_CHARS
        ? chapterContent.slice(0, MAX_HUMANIZE_CHARS)
        : chapterContent;

    const selectionPayload = selectionContext?.selected_text
      ? {
          selected_text: selectionContext.selected_text,
          selected_text_html: selectionContext.selected_text_html || selectionContext.selected_text,
          selection_position: selectionContext.selection_position,
          selection: {
            text: selectionContext.selected_text,
            html: selectionContext.selected_text_html || selectionContext.selected_text,
            from: selectionContext.selection_position?.from,
            to: selectionContext.selection_position?.to,
          },
        }
      : {};

    // 调试日志：查看发送的知识库文档ID
    console.log('[AIPanel] 发送消息，knowledge_doc_ids:', knowledgeDocIds, 'selectedDocs:', selectedDocs, 'selection:', selectionPayload);

    // Agent 模式 = Planning + DeepAgent 反思（可动态调整任务）
    // Plan 模式 = 纯 Planning，无反思（任务列表固定）
    const enableDeepAgent = mode === 'agent';

    const request: AgentChatRequest = {
      message,
      mode: 'planning',  // 后端始终使用 planning 模式
      enable_reflection: enableDeepAgent,  // Agent 模式启用 DeepAgent 反思
      work_id: workId,
      chapter_id: chapterId,
      context: {
        chapter_context: chapterId ? `当前章节ID: ${chapterId}` : undefined,
        knowledge_doc_ids: knowledgeDocIds,
        use_optimization: useOptimization,
        ...selectionPayload,
        ...(useOptimization && safeChapterContent
          ? {
              current_content: safeChapterContent,
              text: safeChapterContent, // 兼容后端可能读取 text 字段
            }
          : {}),
        instruction_context: selectionContext?.selected_text
          ? `用户选中了以下文本进行操作:\n---\n${selectionContext.selected_text}\n---\n用户指令: ${message}`
          : undefined,
      },
    };

    setInputValue('');
    closeAtMenu();
    adjustInputHeight();
    setSelectedDocs([]);
    setOptimizationSelected(false);
    setSelectionContext(null);

    // 发送成功后清除该会话的草稿
    if (sessionId) {
      clearDraft(sessionId);
    }

    // 用户发送消息时，标记应该自动滚动
    shouldAutoScrollRef.current = true;

    try {
      await sendMessageStream(request);
    } catch (err) {
      console.error('Failed to send message:', err);
    }
  };

  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLTextAreaElement>) => {
      const options = atStage === 'root' ? filteredRootOptions : filteredKnowledgeDocs;
      const hasOptions = options.length > 0;

      if (atMenuOpen && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
        e.preventDefault();
        if (!hasOptions) return;
        setHighlightIndex((prev) => {
          if (e.key === 'ArrowDown') {
            return (prev + 1) % options.length;
          }
          return (prev - 1 + options.length) % options.length;
        });
        return;
      }

      if (e.key === 'Enter' && !e.shiftKey) {
        if (atMenuOpen && hasOptions) {
          e.preventDefault();
          const option = options[Math.min(highlightIndex, options.length - 1)];
          if (atStage === 'root') {
            handleRootOption(option as RootCommandOption);
          } else {
            handleKnowledgeSelect(option as { id: string; title: string });
          }
          return;
        }
        e.preventDefault();
        handleSend();
        return;
      }

      if (e.key === 'Escape') {
        closeAtMenu();
      }

      // 回退删除：当输入为空时，Backspace 删除最后一个胶囊（优先知识文档，其次 optimization）
      if (e.key === 'Backspace' && !inputValue.trim()) {
        if (selectedDocs.length > 0) {
          e.preventDefault();
          const last = selectedDocs[selectedDocs.length - 1];
          removeKnowledgeTag(last.id);
          return;
        }
        if (optimizationSelected) {
          e.preventDefault();
          removeOptimization();
        }
      }
    },
    [
      atMenuOpen,
      atStage,
      closeAtMenu,
      filteredKnowledgeDocs,
      filteredRootOptions,
      handleKnowledgeSelect,
      handleRootOption,
      handleSend,
      highlightIndex,
      inputValue,
      optimizationSelected,
      removeKnowledgeTag,
      removeOptimization,
      selectedDocs,
    ]
  );
  const handleStop = useCallback(() => {
    stopStreaming();
  }, [stopStreaming]);

  useLayoutEffect(() => {
    adjustInputHeight();
  }, [inputValue, selectedDocs.length, optimizationSelected, adjustInputHeight]);

  const lastMessageIsAgent = messages.length > 0 && messages[messages.length - 1]?.role === 'agent';
  // ✅ 流式输出：后端逐字发送，前端直接显示 message.content
  const hasStreamingAgentMessage = isLoading && lastMessageIsAgent;
  // ✅ 获取最后一条 agent 消息的内容（用于 Agent 响应块）
  // 条件：正在 streaming 或 有执行轨迹时，都需要显示最后一条消息内容
  const lastAgentContent = lastMessageIsAgent ? (messages[messages.length - 1]?.content || '') : '';
  // v5.1: 从当前消息获取 flowItems
  const lastAgentFlowItems = lastMessageIsAgent ? ((messages[messages.length - 1] as any)?.flowItems || []) : [];
  const shouldShowAgentContent = (hasStreamingAgentMessage || lastAgentFlowItems.length > 0) && lastAgentContent;

  return (
    <div className="p-3 h-full flex flex-col overflow-hidden dark:bg-slate-900">
      <div
        ref={messagesContainerRef}
        className="flex-1 min-h-0 mb-3 space-y-2.5 overflow-y-auto overflow-x-hidden custom-scrollbar bg-white dark:bg-slate-900"
      >
        {/* 欢迎消息 */}
        {messages.length === 0 && (
          <div className="flex items-start gap-2">
            <div className="h-6 w-6 rounded-full bg-zinc-900 dark:bg-slate-700 flex items-center justify-center flex-shrink-0">
              <Bot className="h-3.5 w-3.5 text-white" />
            </div>
            <div className="flex-1 p-2.5 rounded-lg bg-zinc-50/70 border border-zinc-100 dark:bg-slate-800 dark:border-slate-700">
              <p className="text-[11px] leading-relaxed text-zinc-500 dark:text-slate-400">
                你好！我是你的写作助手。我可以帮你续写故事情节、优化文字表达、分析人物关系，以及提供创作建议。
              </p>
            </div>
          </div>
        )}

        {/* 消息列表 */}
        {messages.map((message, index) => {
          // 过滤掉null或undefined的消息
          if (!message) {
            return null;
          }

          // 判断是否是最后一条消息
          const isLastMessage = index === messages.length - 1;
          // v5.1: 获取当前消息的 flowItems
          const messageFlowItems = (message as any).flowItems || [];
          // v5.1 修复: 最后一条 agent 消息如果正在流式传输或有执行轨迹，在 Agent 响应块中渲染
          // 这样可以避免同一消息在两处重复渲染
          const shouldRenderInAgentBlock = isLastMessage && message.role === 'agent' &&
            (hasStreamingAgentMessage || messageFlowItems.length > 0);

          // 如果应该在 Agent 响应块中渲染，先不在这里渲染
          if (shouldRenderInAgentBlock) {
            return null;
          }

          const isUser = message.role === 'user';
          // messageFlowItems 已在上面定义

          return (
            <div key={index} className={`flex items-start gap-2 ${isUser ? 'justify-end' : ''}`}>
              {!isUser && (
                <div className="h-6 w-6 rounded-full bg-zinc-900 dark:bg-slate-700 flex items-center justify-center flex-shrink-0 mt-4">
                  <Bot className="h-3.5 w-3.5 text-white" />
                </div>
              )}

              <div className={`flex flex-col gap-1 w-full ${isUser ? 'items-end' : 'items-start'} group`}>
                <div
                  className={`relative ${
                    isUser
                      ? 'p-2.5 rounded-lg flex-initial w-fit max-w-[85%] md:max-w-[75ch] bg-zinc-800 dark:bg-blue-600 text-zinc-50 shadow-sm ml-auto break-words'
                      : 'flex-1 max-w-[95%] mt-8'
                  }`}
                >
                  {isUser ? (
                    <p className="text-[14px] leading-relaxed whitespace-pre-wrap break-words">
                      {message.content}
                    </p>
                  ) : (
                    <div className="text-zinc-500 dark:text-slate-300">
                      {/* v5.1: 显示该消息的执行轨迹 */}
                      {messageFlowItems.length > 0 && (
                        <ExecutionFlow items={messageFlowItems} />
                      )}
                      <MarkdownContent content={message.content} />
                    </div>
                  )}

                  {/* Agent步骤展示（可选） */}
                  {message.role === 'agent' && message.agentSteps && message.agentSteps.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-zinc-200/50 dark:border-slate-600">
                      <details className="text-[10px] text-zinc-400 dark:text-slate-500">
                        <summary className="cursor-pointer hover:text-zinc-600 dark:hover:text-slate-300">查看执行步骤</summary>
                        <div className="mt-1 space-y-1">
                          {message.agentSteps.map((step, idx) => (
                            <div key={idx} className="pl-2 border-l-2 border-zinc-200 dark:border-slate-600">
                              <div className="font-medium dark:text-slate-300">{step.step}</div>
                              <div className="text-zinc-500 dark:text-slate-400">{step.result}</div>
                            </div>
                          ))}
                        </div>
                      </details>
                    </div>
                  )}

                  {/* 用户消息复制按钮 - 悬停显示 */}
                  {isUser && (
                    <button
                      onClick={() => copyMessage(message.content)}
                      className="absolute -bottom-1 -right-1 translate-y-full opacity-0 group-hover:opacity-100 inline-flex items-center justify-center w-6 h-6 text-zinc-400 hover:text-zinc-600 dark:hover:text-slate-300 transition-all"
                      aria-label="复制消息"
                    >
                      <Copy className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>

                {isUser ? null : (
                  <button
                    onClick={() => copyMessage(message.content)}
                    className="inline-flex self-start items-center justify-center w-8 h-8 text-zinc-500 hover:text-zinc-700 dark:text-slate-400 dark:hover:text-slate-200 transition-colors"
                    aria-label="复制AI内容"
                  >
                    <Copy className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          );
        })}

        {/* Agent 响应块 - 单一头像，包含执行轨迹、任务进度、流式内容 */}
        {(() => {
          // v5.1: 从当前流式消息中获取 flowItems
          const lastMessage = messages[messages.length - 1];
          const currentFlowItems = (lastMessage?.role === 'agent' ? (lastMessage as any).flowItems : []) || [];

          // 判断是否有 Agent 响应内容需要显示
          const hasActivityStream = mode === 'agent' && activities.length > 0;
          const hasExecutionFlow = currentFlowItems.length > 0;
          const hasTaskProgress = isLoading && tasks.length > 0 && !lastAgentContent;
          const hasThinking = isLoading && tasks.length === 0 && !lastAgentContent && currentFlowItems.length === 0;

          const hasAgentResponse = hasActivityStream || hasExecutionFlow || hasTaskProgress || hasThinking || shouldShowAgentContent;

          if (!hasAgentResponse) return null;

          return (
            <div className="flex items-start gap-2 mt-4">
              {/* 单一 Bot 头像 */}
              <div className="h-6 w-6 rounded-full bg-zinc-900 dark:bg-slate-700 flex items-center justify-center flex-shrink-0">
                <Bot className="h-3.5 w-3.5 text-white" />
              </div>

              <div className="flex-1 space-y-4">
                {/* 1. ActivityStream（Agent模式活动流） */}
                {hasActivityStream && (
                  <div className="min-w-0">
                    <ActivityStream
                      key={`activities-${activities.length}`}
                      activities={activities}
                    />
                  </div>
                )}

                {/* 2. ExecutionFlow（执行轨迹可视化）- v5.1: 使用当前消息的 flowItems */}
                {hasExecutionFlow && (
                  <ExecutionFlow items={currentFlowItems} />
                )}

                {/* 3. 任务执行进度（todolist） */}
                {hasTaskProgress && (
                  <div className="space-y-3 will-change-contents">
                    {/* 标题与进度 */}
                    <div className="flex items-center gap-2">
                      <span className="text-[11px] text-zinc-400 dark:text-slate-500">执行中</span>
                      <div className="flex-1 h-px bg-zinc-200 dark:bg-slate-700"></div>
                      <span className="text-[10px] text-zinc-300 dark:text-slate-500 font-mono">
                        {tasks.filter(t => t.status === 'completed').length}/{tasks.length}
                      </span>
                    </div>

                    {/* 步骤列表 */}
                    <div className="space-y-2">
                      {tasks.map((task) => (
                        <div
                          key={task.task_id}
                          className="flex items-start gap-2.5 transition-opacity duration-200 ease-in-out"
                          style={{ opacity: 1 }}
                        >
                          {/* 状态指示器 */}
                          {task.status === 'completed' ? (
                            <div className="h-1 w-1 rounded-full bg-zinc-300 dark:bg-slate-500 flex-shrink-0 mt-1.5 transition-all duration-300"></div>
                          ) : task.status === 'running' ? (
                            <div className="relative flex-shrink-0 mt-1.5 w-3 h-3 flex items-center justify-center outline-none">
                              <div className="h-1 w-1 rounded-full bg-zinc-900 dark:bg-blue-400 relative z-10 animate-pulse outline-none"></div>
                            </div>
                          ) : (
                            <div className="h-1 w-1 rounded-full bg-zinc-200 dark:bg-slate-600 flex-shrink-0 mt-1.5 transition-all duration-300"></div>
                          )}

                          <div className="flex-1 min-w-0 flex items-baseline justify-between gap-2">
                            <p className={`text-[11px] leading-relaxed transition-colors duration-200 outline-none ${
                              task.status === 'running' ? 'text-zinc-700 dark:text-slate-200 animate-pulse' : 'text-zinc-400 dark:text-slate-500'
                            }`}>
                              {task.description}
                            </p>
                            {task.status === 'completed' && task.elapsed_time !== undefined && (
                              <span className="text-[10px] text-zinc-300 dark:text-slate-500 font-mono flex-shrink-0 animate-[fadeIn_0.3s_ease-in]">
                                {task.elapsed_time.toFixed(1)}s
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* 进度条 */}
                    <div className="relative h-px bg-zinc-100 dark:bg-slate-700 overflow-hidden">
                      <div
                        className="absolute left-0 top-0 h-full bg-zinc-400 dark:bg-blue-500 transition-all duration-500 ease-out"
                        style={{ width: `${(tasks.filter(t => t.status === 'completed').length / tasks.length) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                )}

                {/* 4. Thinking 状态 */}
                {hasThinking && (
                  <span className="text-[12px] text-zinc-400 dark:text-slate-400 animate-[pulse_2s_ease-in-out_infinite] outline-none">
                    Thinking...
                  </span>
                )}

                {/* 5. Agent 输出内容（流式或已完成） */}
                {shouldShowAgentContent && (
                  <div className="max-w-[95%]">
                    <div className="text-zinc-500 dark:text-slate-300">
                      <MarkdownContent content={lastAgentContent} />
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })()}

        {/* 错误提示 */}
        {error && (
          <div className="flex items-start gap-2">
            <div className="h-6 w-6 rounded-full bg-red-500 flex items-center justify-center flex-shrink-0">
              <Bot className="h-3.5 w-3.5 text-white" />
            </div>
            <div className="flex-1 p-2.5 rounded-lg bg-red-50 border border-red-200 dark:bg-red-900/20 dark:border-red-800">
              <p className="text-[11px] leading-relaxed text-red-600 dark:text-red-400">
                {error}
              </p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* 建议操作 */}
      {suggestedActions.length > 0 && !isLoading && (
        <div className="mb-2 flex flex-wrap gap-1.5">
          {suggestedActions.map((action, idx) => (
            <button
              key={idx}
              onClick={() => {
                setInputValue(action);
              }}
              className="px-2 py-1 text-[10px] bg-zinc-100 hover:bg-zinc-200 text-zinc-600 rounded transition-colors dark:bg-slate-700 dark:hover:bg-slate-600 dark:text-slate-300"
            >
              {action}
            </button>
          ))}
        </div>
      )}

      {/* 模式选择 + 输入区（上下分区） */}
      <div className="rounded-2xl border border-gray-200 bg-white shadow-sm px-4 py-3 space-y-3 flex-shrink-0 dark:border-slate-700 dark:bg-slate-800">
        <div className="relative">
          <div className="flex flex-wrap items-start gap-2 w-full min-h-12 px-1 py-2 rounded-xl bg-transparent text-gray-800 dark:text-slate-200">
            {/* 胶囊在前，输入在后，保持同一行逻辑 */}
            {selectionContext?.selected_text && (
              <span
                className="inline-flex items-center gap-2 rounded-xl bg-zinc-50 text-zinc-800 px-3 py-2 text-[11px] border border-zinc-200 shadow-sm dark:bg-slate-700 dark:text-slate-200 dark:border-slate-600"
                style={{ maxWidth: '100%' }}
                title={selectionContext.selected_text}
              >
                <Sparkles className="w-3.5 h-3.5 text-zinc-600 dark:text-slate-400" />
                <span className="truncate max-w-[240px]">{selectionContext.selected_text}</span>
                <button
                  type="button"
                  className="hover:text-zinc-900 transition-colors dark:hover:text-slate-100"
                  onMouseDown={(e) => e.preventDefault()}
                  onClick={(e) => {
                    e.preventDefault();
                    setSelectionContext(null);
                  }}
                  aria-label="移除引用"
                >
                  <X className="w-3 h-3" />
                </button>
              </span>
            )}
            {optimizationSelected && (
              <span className="inline-flex items-center gap-1 rounded-full bg-zinc-100 text-zinc-700 px-3 py-1 text-[11px] border border-zinc-200 shadow-sm dark:bg-slate-700 dark:text-slate-200 dark:border-slate-600">
                <Sparkles className="w-3.5 h-3.5 text-zinc-600 dark:text-slate-400" />
                optimization
                <button
                  type="button"
                  className="hover:text-zinc-900 transition-colors"
                  onMouseDown={(e) => e.preventDefault()}
                  onClick={(e) => {
                    e.preventDefault();
                    removeOptimization();
                  }}
                  aria-label="移除 AI 去痕迹"
                >
                  <X className="w-3 h-3" />
                </button>
              </span>
            )}
            {selectedDocs.map((doc) => (
              <span
                key={doc.id}
                className="inline-flex items-center gap-1 rounded-full bg-zinc-100 text-zinc-700 px-3 py-1 text-[11px] border border-zinc-200 shadow-sm dark:bg-slate-700 dark:text-slate-200 dark:border-slate-600"
              >
                <Tag className="w-3.5 h-3.5 text-zinc-600 dark:text-slate-400" />
                {doc.title}
                <button
                  type="button"
                  className="hover:text-zinc-900 transition-colors dark:hover:text-slate-100"
                  onMouseDown={(e) => e.preventDefault()}
                  onClick={(e) => {
                    e.preventDefault();
                    removeKnowledgeTag(doc.id);
                  }}
                  aria-label={`移除 ${doc.title}`}
                >
                  <X className="w-3 h-3" />
                </button>
              </span>
            ))}

            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              onClick={syncAtStateFromRef}
              onFocus={syncAtStateFromRef}
              placeholder="发消息或输入@选择指令..."
              className="flex-1 min-w-[200px] bg-transparent outline-none border-none text-[12px] placeholder:text-gray-400 resize-none leading-relaxed dark:text-slate-200 dark:placeholder:text-slate-500"
              disabled={isLoading}
              rows={1}
              wrap="soft"
              style={{
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
                overflowWrap: 'break-word',
                overflowY: 'hidden',
                overflowX: 'hidden',
                padding: '6px 0',
                flexBasis: '100%',
                minWidth: '100%',
                minHeight: '32px',
                maxHeight: '200px',
              }}
            />
          </div>
        </div>

        {truncatedCount > 0 && (
          <div className="text-[11px] text-amber-600 px-1 dark:text-amber-400">
            章节内容超过 5000 字，已截断超出的 {truncatedCount} 字发送去痕迹。
          </div>
        )}

        <div className="flex items-center justify-between gap-2">
          <ModeSelector
            mode={mode}
            onModeChange={setMode}
            disabled={isLoading}
            compact
            className="bg-white dark:bg-slate-800"
          />

          <div className="flex items-center gap-1.5">
            {isLoading ? (
              <button
                onClick={handleStop}
                className="w-10 h-10 rounded-full bg-gray-200 hover:bg-gray-300 text-gray-800 flex items-center justify-center shadow-sm border border-gray-200 transition-colors dark:bg-slate-600 dark:hover:bg-slate-500 dark:text-slate-200 dark:border-slate-500"
                aria-label="停止生成"
              >
                <Square className="w-4 h-4" strokeWidth={2.5} />
              </button>
            ) : inputValue.trim() ? (
              <button
                onClick={handleSend}
                disabled={!inputValue.trim()}
                className="w-10 h-10 rounded-full transition-all flex items-center justify-center bg-gray-900 text-white hover:bg-gray-800 active:scale-95 shadow-sm dark:bg-blue-600 dark:hover:bg-blue-500"
                aria-label="发送"
              >
                <Send className="h-4 w-4" strokeWidth={2.4} />
              </button>
            ) : null}
          </div>
        </div>
      </div>

      {atMenuOpen && menuPosition &&
        createPortal(
          <div
            className="fixed z-[1200]"
            style={{ left: menuPosition.left, top: menuPosition.top, width: menuPosition.width }}
          >
            <div
              ref={menuRef}
              className="rounded-2xl border border-slate-800/70 bg-slate-900 text-slate-50 shadow-2xl overflow-hidden max-w-[360px] w-full"
            >
              <div className="flex items-center justify-between px-3 py-2 border-b border-slate-800/70 text-[12px]">
                <div className="flex items-center gap-2">
                  {atStage === 'knowledge' ? (
                    <button
                      type="button"
                      onMouseDown={(e) => e.preventDefault()}
                      onClick={() => {
                        setAtStage('root');
                        setHighlightIndex(0);
                        setAtQuery('');
                      }}
                      className="inline-flex items-center gap-1 text-slate-300 hover:text-white transition-colors"
                    >
                      <ChevronLeft className="w-4 h-4" />
                      返回
                    </button>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-slate-300">
                      <Sparkles className="w-4 h-4" />
                      @ 指令
                    </span>
                  )}
                  <span className="text-slate-400 text-[11px]">
                    {atStage === 'knowledge' ? '选择要引用的知识库文档' : '选择指令或继续输入'}
                  </span>
                </div>
                <span className="text-[10px] text-slate-500">Enter 选中 · ↑↓ 移动</span>
              </div>

              <div ref={knowledgeListRef} className="max-h-72 overflow-y-auto custom-scrollbar py-2">
                {atStage === 'root' ? (
                  filteredRootOptions.length > 0 ? (
                    filteredRootOptions.map((option, idx) => (
                      <button
                        key={option.key}
                        type="button"
                        onMouseDown={(e) => e.preventDefault()}
                        onClick={() => handleRootOption(option)}
                        onMouseEnter={() => setHighlightIndex(idx)}
                        className={`w-full px-3 py-2.5 flex items-center justify-between text-left transition-colors ${
                          idx === highlightIndex ? 'bg-slate-800/80 border-l-2 border-slate-500' : 'hover:bg-slate-800/60'
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          <span className="text-slate-200">{option.icon}</span>
                          <div className="flex flex-col">
                            <span className="text-[12px] text-white">{option.label}</span>
                            <span className="text-[11px] text-slate-400">{option.description}</span>
                          </div>
                        </div>
                        {option.hasChildren && <ChevronRight className="w-4 h-4 text-slate-400" />}
                      </button>
                    ))
                  ) : (
                    <div className="px-3 py-2 text-[12px] text-slate-400">没有匹配的指令</div>
                  )
                ) : (
                  <div className="space-y-1">
                    {knowledgeLoading && (
                      <div className="px-3 py-2 text-[12px] text-slate-400 flex items-center gap-2">
                        <Loader2 className="w-4 h-4 animate-spin" />
                        正在加载知识库文档...
                      </div>
                    )}
                    {knowledgeError && !knowledgeLoading && (
                      <div className="px-3 py-2 text-[12px] text-amber-200">
                        {knowledgeError}
                      </div>
                    )}
                    {!knowledgeLoading && !knowledgeError && filteredKnowledgeDocs.length === 0 && (
                      <div className="px-3 py-2 text-[12px] text-slate-400">暂无可用文档</div>
                    )}
                    {!knowledgeLoading &&
                      !knowledgeError &&
                      filteredKnowledgeDocs.map((doc, idx) => (
                        <button
                          key={doc.id}
                          type="button"
                          onMouseDown={(e) => e.preventDefault()}
                          onClick={() => handleKnowledgeSelect(doc)}
                          onMouseEnter={() => setHighlightIndex(idx)}
                          className={`w-full px-3 py-2.5 flex items-center justify-between text-left transition-colors ${
                            idx === highlightIndex ? 'bg-slate-800/80 border-l-2 border-slate-500' : 'hover:bg-slate-800/60'
                          }`}
                        >
                          <div className="flex items-center gap-2">
                            <Tag className="w-4 h-4 text-slate-200" />
                            <span className="text-[12px] text-white">{doc.title}</span>
                          </div>
                          <ChevronRight className="w-4 h-4 text-slate-400 opacity-60" />
                        </button>
                      ))}
                  </div>
                )}
              </div>
            </div>
          </div>,
          document.body
        )}

      {/* ✅ 编辑器确认对话框 */}
      {pendingApproval && (
        <AgentEditConfirmDialog
          isOpen={true}
          approvalRequest={pendingApproval}
          onApprove={(selectedVersion) => submitApproval(true, selectedVersion)}
          onReject={() => submitApproval(false)}
          onClose={() => submitApproval(false)}
        />
      )}
    </div>
  );
}



