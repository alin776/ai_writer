import React, { useState, useRef, useEffect, useLayoutEffect, useCallback, useMemo, KeyboardEvent } from 'react';
import { createPortal } from 'react-dom';
import { Button } from '../ui/button';
import { Send, Loader2, Square, BookOpen, Sparkles, ChevronRight, ChevronLeft, ChevronUp, ChevronDown, Tag, X, Copy, Check } from 'lucide-react';
import { useAgentChat } from '../../hooks/useAgentChat';
import { useEditorStore } from '../../store/editorStore';
import { useChatDraftStore } from '../../store/chatDraftStore';
import type { AgentChatRequest, TaskSnapshot } from '../../types/agent';
import type { AgentMode } from '../agent/ModeSelector';
import ModeSelector from '../agent/ModeSelector';
import ActivityStream from '../agent/ActivityStream';  // ✅ 导入ActivityStream
import { ExecutionFlow } from '../agent/ExecutionFlow';  // ✅ v5.0: 执行轨迹可视化
import { AgentHeader } from '../agent/ExecutionFlow/AgentHeader';
import AgentEditConfirmDialog from '../agent/AgentEditConfirmDialog';  // ✅ 编辑确认对话框
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';  // ✅ 支持 GFM 语法
import { knowledgeApi } from '@/services/knowledgeApi';

interface AIPanelProps {
  workId: string;
  chapterId?: string;
  sessionId?: string;
  onTitleChange?: (title: string) => void;
  /** 是否为当前活体（只有活跃窗口才监听 InlineAI 事件） */
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
          // 分隔线
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


const TaskList = ({ tasks }: { tasks: TaskSnapshot[] }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!tasks || tasks.length === 0) return null;

  // 计算已完成任务数
  const completedCount = tasks.filter(t => t.status === 'completed').length;
  const totalCount = tasks.length;

  // 获取当前执行的任务（running状态），如果没有则取最后一个任务
  const currentTask = tasks.find(t => t.status === 'running') || tasks[tasks.length - 1];

  // 收缩状态：只显示当前任务行（带计数和展开按钮）
  if (!isExpanded && currentTask) {
    return (
      <div className="rounded-xl border border-zinc-200 dark:border-slate-700 bg-zinc-50/50 dark:bg-slate-800/50 overflow-hidden">
        <button
          onClick={() => setIsExpanded(true)}
          className={`w-full flex items-center gap-2 px-3 py-2 text-[11px] hover:bg-zinc-100/50 dark:hover:bg-slate-700/50 transition-colors ${
            currentTask.status === 'completed'
              ? 'text-green-700 dark:text-green-400'
              : currentTask.status === 'running'
                ? 'text-blue-700 dark:text-blue-400'
                : 'text-zinc-600 dark:text-slate-400'
          }`}
        >
          {currentTask.status === 'completed' ? (
            <Check className="w-3.5 h-3.5 flex-shrink-0" />
          ) : currentTask.status === 'running' ? (
            <Loader2 className="w-3.5 h-3.5 animate-spin flex-shrink-0" />
          ) : (
            <div className="w-3.5 h-3.5 rounded-full border border-current flex-shrink-0" />
          )}
          <span className="flex-1 truncate text-left">{currentTask.description}</span>
          <span className="text-[11px] text-zinc-500 dark:text-slate-400 flex-shrink-0">
            {completedCount} / {totalCount}
          </span>
          <ChevronUp className="w-3.5 h-3.5 text-zinc-400 dark:text-slate-500 flex-shrink-0" />
        </button>
      </div>
    );
  }

  // 展开状态：显示完整列表
  return (
    <div className="rounded-xl border border-zinc-200 dark:border-slate-700 bg-zinc-50/50 dark:bg-slate-800/50 overflow-hidden">
      {/* 头部：任务进度 + 收缩按钮 */}
      <button
        onClick={() => setIsExpanded(false)}
        className="w-full flex items-center justify-between px-3 py-2 hover:bg-zinc-100/50 dark:hover:bg-slate-700/50 transition-colors"
      >
        <span className="text-[11px] font-medium text-zinc-600 dark:text-slate-300">
          任务进度
        </span>
        <div className="flex items-center gap-2">
          <span className="text-[11px] text-zinc-500 dark:text-slate-400">
            {completedCount} / {totalCount}
          </span>
          <ChevronDown className="w-3.5 h-3.5 text-zinc-400 dark:text-slate-500" />
        </div>
      </button>

      {/* 任务列表 */}
      <div className="px-2 pb-2 space-y-1">
        {tasks.map((task) => (
          <div
            key={task.task_id}
            className={`flex items-center gap-2 px-2.5 py-1.5 rounded-lg text-[11px] ${
              task.status === 'completed'
                ? 'bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-400'
                : task.status === 'running'
                  ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400'
                  : 'bg-zinc-100 text-zinc-600 dark:bg-slate-700 dark:text-slate-400'
            }`}
          >
            {task.status === 'completed' ? (
              <Check className="w-3.5 h-3.5 flex-shrink-0" />
            ) : task.status === 'running' ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin flex-shrink-0" />
            ) : (
              <div className="w-3.5 h-3.5 rounded-full border border-current flex-shrink-0" />
            )}
            <span className="flex-1 truncate">{task.description}</span>
            {task.elapsed_time !== undefined && task.status === 'completed' && (
              <span className="text-[10px] opacity-60 flex-shrink-0">{task.elapsed_time.toFixed(1)}s</span>
            )}
          </div>
        ))}
      </div>
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
    description: '引用知识库中的文档',
    icon: <BookOpen className="w-4 h-4" />,
    hasChildren: true,
  },
  {
    key: 'optimization',
    label: '@optimization',
    description: '调用 AI 去痕迹优化',
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

// 全局去重集合，确保消息只处理一次 inline-ai 消息
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
    activities,
    sendMessageStream,
    stopStreaming,
    pendingApproval,
    submitApproval,
  } = useAgentChat({ workId, chapterId, sessionId });  // ✅ 传入workId和chapterId进行会话隔离

  // 获取当前章节内容，用于 @optimization 直接调用去痕迹接口
  const { currentChapter } = useEditorStore();

  // 获取草稿 store 的方法，用于会话切换时保存/恢复输入状态
  const { saveDraft, getDraft, clearDraft } = useChatDraftStore();

  const [inputValue, setInputValue] = useState('');
  const [mode, setMode] = useState<AgentMode>('plan'); // ✅ Agent执行模式：plan(固定规划) | agent(DeepAgent反思)
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const shouldAutoScrollRef = useRef(true); // 跟踪是否应该自动滚动
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

  // 复制成功状态，显示 ✓
  const [copiedMessageId, setCopiedMessageId] = useState<string | null>(null);

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

  // 实时保存草稿：每当内容变化时自动保存
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

  // ✅ 流式输出：真正的字符流，前端直接显示，不在前端处理换行效果

  const copyMessage = useCallback(async (content: string, messageId: string) => {
    try {
      await navigator.clipboard.writeText(content || '');
      setCopiedMessageId(messageId);
      // 2秒后恢复
      setTimeout(() => setCopiedMessageId(null), 2000);
    } catch (err) {
      console.error('Copy failed:', err);
    }
  }, []);

  const containsAt = useMemo(() => AT_CHARS.some((c) => inputValue.includes(c)), [inputValue]);
  // 去痕长度变量，用于显示
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


  // 标题自动生成
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

  // ✅ 定义 handleSendWithContext 用于处理带上下文的消息（InlineAI）
  // ✅ 使用 useRef 存储回调函数，让 useEffect 不因回调变化而重新渲染
  const handleSendWithContextRef = useRef<(message: string, context?: any) => Promise<void>>();

  handleSendWithContextRef.current = async (message: string, context?: any) => {
    if (!message.trim()) return;

    const backendMode: AgentChatRequest['mode'] = mode === 'agent' ? 'react' : 'planning';

    // ✅ 固定 payload 结构，将选中信息放入独立的 selection 字段
    // 避免将选中文本放入 prompt/chapter_context 导致被覆盖或结构混乱
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
        // ✅ 新增独立 selection 字段，推荐结构化
        selection: selectionData,
        // 保留 selected_text 字段以兼容旧逻辑
        selected_text: context?.selected_text,
        selection_position: context?.selection_position,
        // chapter_context 只放章节标识，不放选中文本
        chapter_context: chapterId ? `当前章节ID: ${chapterId}` : undefined,
        // ✅ 如果有选中文本，添加结构化的指令上下文
        instruction_context: context?.selected_text
          ? `用户选中了以下文本进行操作:
---
${context.selected_text}
---
用户指令: ${message}`
          : undefined,
      },
    };

    // 用户发送消息时，重新应该自动滚动
    shouldAutoScrollRef.current = true;

    try {
      await sendMessageStream(request);
    } catch (err) {
      console.error('[AIPanel] Failed to send message:', err);
    }
  };

  // ✅ 稳定的回调封装，避免因依赖变化而重新创建
  const handleSendWithContext = useCallback((message: string, context?: any) => {
    return handleSendWithContextRef.current?.(message, context);
  }, []);

  // ✅ 监听来自编辑器 InlineAI 的消息，只有活跃窗口才监听
  useEffect(() => {
    // 非活跃不设置监听
    if (!isActive) {
      return;
    }

    // 处理已队列中的待处理消息
    const queue: any[] = (window as any).__inlineAIQueue__ || [];
    const consumed = getInlineAIProcessedSet();

    queue.forEach((item) => {
      const rid = item?.requestId || JSON.stringify(item);
      if (!consumed.has(rid)) {
        consumed.add(rid);
        // ✅ 直接传递原始 context，handleSendWithContext 会正确构建 selection 字段
        handleSendWithContext(item.message || '', item.context || {});
      }
    });
    (window as any).__inlineAIQueue__ = [];

    // 暴露全局回调
    (window as any).__agentInlineSend__ = (msg: string, ctx?: any, requestId?: string) => {
      const rid = requestId || `inline-${Date.now()}-${Math.random().toString(16).slice(2)}`;
      if (consumed.has(rid)) return;
      consumed.add(rid);
      // ✅ 直接传递原始 context，handleSendWithContext 会正确构建 selection 字段
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

      // 去重检查
      const rid = requestId || `inline-${Date.now()}`;
      if (consumed.has(rid)) {
        return;
      }
      consumed.add(rid);

      // ✅ 直接传递原始 context，handleSendWithContext 会正确构建 selection 字段
      handleSendWithContext(message, context);
    };

    window.addEventListener('inline-ai-send', handleInlineAIMessage as EventListener);

    return () => {
      window.removeEventListener('inline-ai-send', handleInlineAIMessage as EventListener);
      delete (window as any).__agentInlineSend__;
    };
  }, [handleSendWithContext, isActive]);

  // ✅ 监听 InlineAI intent（用于设置上下文，不发送消息）：全局 + 事件队列
  useEffect(() => {
    if (!isActive) return;
    const intentQueue: any[] = (window as any).__inlineAIIntentQueue__ || [];
    if (intentQueue.length > 0) {
      const last = intentQueue[intentQueue.length - 1];
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
      setSelectionContext(event.detail || null);
    };

    window.addEventListener('inline-ai-intent', handleInlineAIIntent as EventListener);
    return () => {
      window.removeEventListener('inline-ai-intent', handleInlineAIIntent as EventListener);
      delete (window as any).__agentInlineIntent__;
    };
  }, [isActive]);

  // 检查用户是否在底部
  const checkIfAtBottom = useCallback(() => {
    const container = messagesContainerRef.current;
    if (!container) return false;

    // 检查滚动位置是否接近底部（允许50px误差）
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

  // 当消息列表更新时，如果用户在底部则自动滚动
  // 只在消息数量变化时滚动，避免流式内容更新时频繁滚动外层
  useEffect(() => {
    if (shouldAutoScrollRef.current) {
      scrollToBottom();
    }
  }, [messages.length, tasks.length, scrollToBottom]);

  // ✅ 流式输出：真正的字符流，前端直接使用 message.content

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

    // 先重置高度，让 scrollHeight 能正确反映实际内容高度
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

    // Agent 模式 = Planning + DeepAgent 反思，可动态调整计划
    // Plan 模式 = 纯 Planning，无反思，任务列表固定
    const enableDeepAgent = mode === 'agent';

    const request: AgentChatRequest = {
      message,
      mode: 'planning',  // 始终使用 planning 模式
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
          ? `用户选中了以下文本进行操作:
---
${selectionContext.selected_text}
---
用户指令: ${message}`
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

    // 用户发送消息时，重新应该自动滚动
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

      // 当输入框内容为空时，Backspace 删除最后一个标签（先知识文档，再 optimization）
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

  return (
    <div className="p-3 h-full flex flex-col overflow-hidden dark:bg-slate-900">
      <div
        ref={messagesContainerRef}
        className="flex-1 min-h-0 mb-3 space-y-2.5 overflow-y-auto overflow-x-hidden scrollbar-auto-hide bg-white dark:bg-slate-900"
      >
        {/* 欢迎消息 */}
        {messages.length === 0 && (
          <div className="flex items-start">
            <div className="flex-1 p-2.5 rounded-lg bg-zinc-50/70 border border-zinc-100 dark:bg-slate-800 dark:border-slate-700">
              <p className="text-[11px] leading-relaxed text-zinc-500 dark:text-slate-400">
                你好，我是你的写作助手。我可以帮你续写、润色、优化文字表达、梳理情节脉络，以及提供创作建议。
              </p>
            </div>
          </div>
        )}

        {/* 消息列表 */}
        {messages.map((message, index) => {
          // 过滤掉null和undefined消息
          if (!message) {
            return null;
          }

          const isUser = message.role === 'user';
          const isLastMessage = index === messages.length - 1;

          if (isUser) {
            return (
              <div key={index} className="flex items-start gap-2 justify-end">
                <div className="flex flex-col gap-1 w-full items-end group">
                  <div className="relative p-2.5 rounded-lg flex-initial w-fit max-w-[80%] md:max-w-[60ch] bg-zinc-800 dark:bg-blue-600 text-zinc-50 shadow-sm ml-auto break-words">
                    <p className="text-[14px] leading-relaxed whitespace-pre-wrap break-words">
                      {message.content}
                    </p>

                    {/* 用户消息复制按钮 - 悬停显示 */}
                    <button
                      onClick={() => copyMessage(message.content, `msg-${index}`)}
                      className="absolute -bottom-1 -right-1 translate-y-full opacity-0 group-hover:opacity-100 inline-flex items-center justify-center w-6 h-6 text-zinc-400 hover:text-zinc-600 dark:hover:text-slate-300 transition-all"
                      aria-label="复制消息"
                    >
                      {copiedMessageId === `msg-${index}` ? (
                        <Check className="w-3.5 h-3.5 text-green-500" />
                      ) : (
                        <Copy className="w-3.5 h-3.5" />
                      )}
                    </button>
                  </div>
                </div>
              </div>
            );
          }

          const messageFlowItems = (message as any).flowItems || [];
          // v6.2: completion 应该和 output 一起显示在内容区域，而不是在执行轨迹区域
          // v6.4: agent_header 也排除，因为内容区域已经有 AgentHeader 组件
          const flowItemsWithoutOutput = messageFlowItems.filter((item: any) =>
            item?.type !== 'output' && item?.type !== 'completion' && item?.type !== 'agent_header'
          );
          const outputItems = messageFlowItems.filter((item: any) => item?.type === 'output');
          const completionItem = messageFlowItems.find((item: any) => item?.type === 'completion');
          const lastOutputItem = outputItems.length > 0 ? outputItems[outputItems.length - 1] : null;
          const isStreamingMessage = isLastMessage && isLoading;
          const showActivityStream = isStreamingMessage && mode === 'agent' && activities.length > 0;
          const showThinking = isStreamingMessage && !showActivityStream && flowItemsWithoutOutput.length === 0;
          const showFlowBlock = flowItemsWithoutOutput.length > 0 || showActivityStream || showThinking;

          return (
            <div key={index} className="space-y-2">
              {showFlowBlock && (
                <div className="flex items-start">
                  <div className="flex-1">
                    {flowItemsWithoutOutput.length > 0 && (
                      <ExecutionFlow items={flowItemsWithoutOutput} />
                    )}
                    {showActivityStream && (
                      <div className="min-w-0">
                        <ActivityStream
                          key={`activities-${activities.length}`}
                          activities={activities}
                        />
                      </div>
                    )}
                    {showThinking && (
                      <span className="text-[12px] text-zinc-400 dark:text-slate-400 animate-[pulse_2s_ease-in-out_infinite] outline-none">
                        Thinking...
                      </span>
                    )}
                  </div>
                </div>
              )}

              {/* v6.2: 只有当有实际内容时才显示AgentHeader和内容区域 */}
              {(message.content || lastOutputItem) && (
                <div className="flex items-start">
                  <div className="flex flex-col gap-1 w-full group">
                    <AgentHeader />
                    <div className="text-zinc-500 dark:text-slate-300">
                      {lastOutputItem ? (
                        // v6.3: 当 output flowItem 存在时，优先使用 message.content（流式内容）
                        // 如果 message.content 为空，则使用 flowItem 中的 content
                        <ExecutionFlow
                          items={[{
                            ...lastOutputItem,
                            data: {
                              ...(lastOutputItem.data as any),
                              content: message.content || (lastOutputItem.data as any).content
                            }
                          }]}
                        />
                      ) : (
                        <MarkdownContent content={message.content} />
                      )}
                    </div>

                    {/* v6.2: 在内容下方显示completion状态，只有当消息不在流式输出中时才显示 */}
                    {completionItem && !isStreamingMessage && (
                      <ExecutionFlow items={[completionItem]} />
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}

        {/* 错误提示 */}
        {error && (
          <div className="flex items-start">
            <div className="flex-1 p-2.5 rounded-lg bg-red-50 border border-red-200 dark:bg-red-900/20 dark:border-red-800">
              <p className="text-[11px] leading-relaxed text-red-600 dark:text-red-400">
                {error}
              </p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* 任务列表（固定在底部，不随消息滚动） */}
      {tasks.length > 0 && (
        <div className="mb-2">
          <TaskList tasks={tasks as TaskSnapshot[]} />
        </div>
      )}

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

      {/* 模式选择 + 输入框（放在下方区域） */}
      <div className="rounded-2xl border border-gray-200 bg-white shadow-sm px-4 py-3 space-y-3 flex-shrink-0 dark:border-slate-700 dark:bg-slate-800">
        <div className="relative">
          <div className="flex flex-wrap items-start gap-2 w-full min-h-12 px-1 py-2 rounded-xl bg-transparent text-gray-800 dark:text-slate-200">
            {/* 选中文本前置（放在后，保持同一行逻辑） */}
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
                  aria-label="移除选中"
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
              placeholder="输入消息，输入@选择指令..."
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
            章节内容超过 5000 字，已截断超过的 {truncatedCount} 字符进行去痕迹。
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
                aria-label="ֹͣ发送"
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
                      发送
                    </button>
                  ) : (
                    <span className="inline-flex items-center text-slate-300">
                      @ 指令
                    </span>
                  )}
                </div>
              </div>

              <div ref={knowledgeListRef} className="max-h-72 overflow-y-auto custom-scrollbar px-2 py-2">
                {atStage === 'root' ? (
                  filteredRootOptions.length > 0 ? (
                    filteredRootOptions.map((option, idx) => (
                      <button
                        key={option.key}
                        type="button"
                        onMouseDown={(e) => e.preventDefault()}
                        onClick={() => handleRootOption(option)}
                        onMouseEnter={() => setHighlightIndex(idx)}
                        className={`w-full px-3 py-2.5 rounded-xl flex items-center justify-between text-left transition-colors ${
                          idx === highlightIndex
                            ? 'bg-slate-800/80 ring-1 ring-slate-600/60'
                            : 'hover:bg-slate-800/60'
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
                          className={`w-full px-3 py-2.5 rounded-xl flex items-center justify-between text-left transition-colors ${
                            idx === highlightIndex
                              ? 'bg-slate-800/80 ring-1 ring-slate-600/60'
                              : 'hover:bg-slate-800/60'
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

      {/* ✅ 编辑确认对话框 */}
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



