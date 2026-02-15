import React, { useState, useRef, useEffect, useLayoutEffect, useCallback, useMemo, KeyboardEvent } from 'react';
import { createPortal } from 'react-dom';
import { Button } from '../ui/button';
import { Send, Loader2, Square, BookOpen, Sparkles, ChevronRight, ChevronUp, ChevronDown, Tag, X, Copy, Check, Plus } from 'lucide-react';
import { useAgentChat } from '../../hooks/useAgentChat';
import { useEditorStore } from '../../store/editorStore';
import { useChatDraftStore } from '../../store/chatDraftStore';
import { agentApi } from '../../services/agentApi';  // v7.5: 非阻塞式修订
import type { AgentChatRequest, TaskSnapshot, RevisionFlowData, FlowItem, StepFlowData } from '../../types/agent';
import type { AgentMode } from '../agent/ModeSelector';
import ActivityStream from '../agent/ActivityStream';  // 导入 ActivityStream
import { ExecutionFlow } from '../agent/ExecutionFlow';  // v5.0: 执行轨迹可视化
import AgentEditConfirmDialog from '../agent/AgentEditConfirmDialog';  // 编辑确认对话框
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { ToastContainer } from '@/components/ui/Toast';
import { useToast } from '@/hooks/useToast';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';  // 支持 GFM 语法
import { knowledgeApi } from '@/services/knowledgeApi';

interface AIPanelProps {
  workId: string;
  chapterId?: string;
  sessionId?: string;
  onTitleChange?: (title: string) => void;
  /** 是否为当前活跃（只有活跃窗口才监听 InlineAI 事件）*/
  isActive?: boolean;
  /** 展开模式：编辑器收起时为 true，滚动由外层容器处理 */
  expandedMode?: boolean;
}

const getNodesInfoPayload = () => {
  if (typeof window === 'undefined') return undefined;
  const api = (window as any).__editorNodeAPI;
  const nodes = api?.getAllNodes?.();
  if (!Array.isArray(nodes) || nodes.length === 0) return undefined;
  return JSON.stringify(nodes.map((node: any) => ({ id: node.id })));
};

const parseChineseNumber = (input: string): number | null => {
  const value = input.trim();
  if (!value) return null;
  if (/^\d+$/.test(value)) return parseInt(value, 10);
  const map: Record<string, number> = {
    '\u96f6': 0,
    '\u4e00': 1,
    '\u4e8c': 2,
    '\u4e24': 2,
    '\u4e09': 3,
    '\u56db': 4,
    '\u4e94': 5,
    '\u516d': 6,
    '\u4e03': 7,
    '\u516b': 8,
    '\u4e5d': 9,
    '\u5341': 10,
  };
  if (value === '\u5341') return 10;
  if (value.includes('\u5341')) {
    const parts = value.split('\u5341');
    const tens = parts[0] ? (map[parts[0]] ?? 0) : 1;
    const ones = parts[1] ? (map[parts[1]] ?? 0) : 0;
    return tens * 10 + ones;
  }
  if (value.length === 1 && map[value] !== undefined) return map[value];
  return map[value] !== undefined ? map[value] : null;
};

const getStructuralLocateHint = (message: string) => {
  if (typeof window === 'undefined') return {};
  const api = (window as any).__editorNodeAPI;
  const nodes = api?.getAllNodes?.();
  if (!Array.isArray(nodes) || nodes.length === 0) return {};
  const compact = message.replace(/\s+/g, '');
  let index: number | null = null;
  if (/(\u5f00\u5934|\u5f00\u7bc7|\u9996\u6bb5|\u7b2c\u4e00\u6bb5|\u5f00\u573a)/.test(compact)) {
    index = 0;
  }
  if (/(\u7ed3\u5c3e|\u672b\u5c3e|\u6700\u540e\u4e00\u6bb5|\u6536\u5c3e|\u7ed3\u5c40)/.test(compact)) {
    index = nodes.length - 1;
  }
  const match = compact.match(/\u7b2c([0-9]+|[\u4e00\u4e8c\u4e24\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]+)\u6bb5/);
  if (match) {
    const parsed = parseChineseNumber(match[1]);
    if (parsed !== null) index = parsed - 1;
  }
  if (index === null || index < 0 || index >= nodes.length) return {};
  const nodeId = nodes[index]?.id;
  if (!nodeId) return {};
  return {
    locate_node_id: nodeId,
    locate_paragraph_index: index,
    locate_method: 'structural'
  };
};

const QUOTED_PATTERNS: RegExp[] = [
  /\u201C([^\u201D]+)\u201D/,
  /"([^"]+)"/,
  /'([^']+)'/,
  /\u300C([^\u300D]+)\u300D/,
  /\u300E([^\u300F]+)\u300F/,
  /\u3008([^\u3009]+)\u3009/,
  /\u2018([^\u2019]+)\u2019/,
  /`([^`]+)`/,
];
const getQuotedRangeLocateHint = (message: string) => {
  const value = message || '';
  if (!value.trim()) return {};
  for (const pattern of QUOTED_PATTERNS) {
    const match = value.match(pattern);
    const quoted = match?.[1]?.trim();
    if (quoted) {
      return {
        locate_original_text: quoted,
        locate_method: 'quoted',
      };
    }
  }
  return {};
};


// ✅ 优化：缓存 remarkPlugins 和 rehypePlugins，避免每次渲染都创建新数组
const remarkPluginsCache = [remarkGfm];
const rehypePluginsCache = [rehypeRaw];

// ✅ 优化：使用 React.memo 包裹 Markdown 渲染组件
const MarkdownContent: React.FC<{ content: string }> = React.memo(({ content }) => {
  return (
    <div className="text-[14px] leading-relaxed markdown-content">
      <ReactMarkdown
        remarkPlugins={remarkPluginsCache}
        rehypePlugins={rehypePluginsCache}
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
            return <h1 className="text-[18px] font-bold mb-2 mt-3 first:mt-0 text-zinc-900 dark:text-zinc-100 border-b border-zinc-200 dark:border-zinc-700 pb-1">{children}</h1>;
          },
          h2({ children }) {
            return <h2 className="text-[16px] font-semibold mb-2 mt-3 first:mt-0 text-zinc-800 dark:text-zinc-200">{children}</h2>;
          },
          h3({ children }) {
            return <h3 className="text-[15px] font-medium mb-1.5 mt-2 first:mt-0 text-zinc-700 dark:text-zinc-300">{children}</h3>;
          },
          // 列表 - 使用 list-outside 让嵌套列表有更好的缩进
          ul({ children, className }) {
            // 检查是否是任务列表（contains-task-list）
            const isTaskList = className?.includes('contains-task-list');
            return (
              <ul className={`mb-1.5 space-y-1 text-[14px] ${isTaskList ? 'list-none pl-0' : 'list-disc list-outside pl-5'}`}>
                {children}
              </ul>
            );
          },
          ol({ children }) {
            return <ol className="list-decimal list-outside mb-1.5 space-y-1 text-[14px] pl-5">{children}</ol>;
          },
          li({ children, className }) {
            const isTaskItem = className?.includes('task-list-item');
            return (
              <li className={`text-[14px] ${isTaskItem ? 'flex items-start gap-2 list-none' : ''}`}>
                {children}
              </li>
            );
          },
          // 任务列表 checkbox
          input({ type, checked, disabled }) {
            if (type === 'checkbox') {
              return (
                <span className={`inline-flex items-center justify-center w-4 h-4 rounded border flex-shrink-0 mt-0.5 ${
                  checked
                    ? 'bg-blue-500 border-blue-500 text-white'
                    : 'border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800'
                }`}>
                  {checked && (
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  )}
                </span>
              );
            }
            return null;
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
}, (prevProps, nextProps) => {
  // 自定义比较：只有内容变化时才重新渲染
  return prevProps.content === nextProps.content;
});

MarkdownContent.displayName = 'MarkdownContent';


const TaskList = ({ tasks }: { tasks: TaskSnapshot[] }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!tasks || tasks.length === 0) return null;

  // 计算已完成任务数
  const completedCount = tasks.filter(t => t.status === 'completed').length;
  const totalCount = tasks.length;

  // 获取当前执行的任务（running 状态），如果没有则取最后一个任务
  const currentTask = tasks.find(t => t.status === 'running') || tasks[tasks.length - 1];

  return (
    <div className="relative">
      {/* 展开状态：绝对定位往上展开 */}
      {isExpanded && (
        <div className="absolute bottom-full left-0 right-0 mb-1 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 overflow-hidden shadow-lg z-10">
          {/* 头部：任务进度 + 收缩按钮 */}
          <button
            onClick={() => setIsExpanded(false)}
            className="w-full flex items-center justify-between px-3 py-2 hover:bg-gray-50 dark:hover:bg-slate-700/50 transition-colors"
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
          <div className="px-2 pb-2 space-y-1 max-h-64 overflow-y-auto">
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
                <span className="flex-1 min-w-0 whitespace-normal break-words">{task.description}</span>
                {task.elapsed_time !== undefined && task.status === 'completed' && (
                  <span className="text-[10px] opacity-60 flex-shrink-0">{task.elapsed_time.toFixed(1)}s</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 收缩状态：只显示当前任务行 */}
      {currentTask && (
        <div className="rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 overflow-hidden">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className={`w-full flex items-center gap-2 px-3 py-2 text-[11px] hover:bg-gray-50 dark:hover:bg-slate-700/50 transition-colors ${
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
            <ChevronUp className={`w-3.5 h-3.5 text-zinc-400 dark:text-slate-500 flex-shrink-0 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
          </button>
        </div>
      )}
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
    label: '从知识库中添加',
    description: '从知识库中添加',
    icon: <BookOpen className="w-4 h-4" />,
    hasChildren: true,
  },
  {
    key: 'optimization',
    label: '文本自然化',
    description: '文本自然化',
    icon: <Sparkles className="w-4 h-4" />,
  },
];

const AT_CHARS = ['@', '\uFF20'];

const MENU_COLUMN_WIDTH = 240;
const MENU_GAP = 8;


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

export function AIPanel({ workId, chapterId, sessionId, onTitleChange, isActive = true, expandedMode = false }: AIPanelProps) {
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
    updateRevisionStatus,
    undoRevision,      // v7.2
    redoRevision,      // v7.2
    acceptAllRevisions,   // v7.3: 批量采纳
    discardAllRevisions,  // v7.3: 批量弃用
    // v8.0: 批量操作管理
    hasOperations,
    acceptAllOperations,
    rollbackAllOperations,
  } = useAgentChat({ workId, chapterId, sessionId });  // 传入 workId 和 chapterId 进行会话隔离

  // 获取当前章节内容，用 @optimization 直接调用去痕迹接口
  const { currentChapter } = useEditorStore();

  // 获取草稿 store 的方法，用于会话切换时保存/恢复输入状态
  const { saveDraft, getDraft, clearDraft } = useChatDraftStore();

  const [inputValue, setInputValue] = useState('');
  const [mode] = useState<AgentMode>('plan'); // Agent 执行模式：plan(固定规划) | agent(DeepAgent 反思)
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const messagesContentRef = useRef<HTMLDivElement>(null);
  const lastUserMessageRef = useRef<HTMLDivElement>(null);
  const shouldAutoScrollRef = useRef(true); // 跟踪是否应该自动滚动
  const anchorLatestUserRef = useRef(false);
  const skipAutoScrollRef = useRef(false);
  const freezeAutoScrollRef = useRef(false);
  const ignoreScrollEventRef = useRef(false);
  const userScrollIntentRef = useRef(false);
  const anchoredOnceRef = useRef(false);
  const isInputFocusedRef = useRef(false);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const hasOperationsRef = useRef(false);
  const scrollPositionRef = useRef<number>(0); // 保存滚动位置比例
  const prevExpandedModeRef = useRef(expandedMode); // 追踪上一次的 expandedMode
  const [scrollBufferHeight, setScrollBufferHeight] = useState(0);
  const [isAtBottom, setIsAtBottom] = useState(true);
  const atBottomStateRef = useRef(true);
  const syncAtBottomState = useCallback((next: boolean) => {
    if (atBottomStateRef.current === next) return;
    atBottomStateRef.current = next;
    setIsAtBottom(next);
  }, []);

  const [atMenuOpen, setAtMenuOpen] = useState(false);
  const [manualMenuOpen, setManualMenuOpen] = useState(false);
  const [knowledgePanelOpen, setKnowledgePanelOpen] = useState(false);
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
  const resolveRevisionRequestId = useCallback((revision?: RevisionFlowData | null) => {
    if (!revision) return undefined;
    return (revision.requestId || (revision as any).request_id) as string | undefined;
  }, []);
  const resolveRevisionChapterId = useCallback((revision?: RevisionFlowData | null) => {
    if (!revision) return undefined;
    const anyRevision = revision as any;
    const editorAction = anyRevision.editorAction || anyRevision.editor_action || {};
    return (
      revision.chapterId ||
      anyRevision.chapter_id ||
      anyRevision.targetChapterId ||
      anyRevision.target_chapter_id ||
      editorAction.chapterId ||
      editorAction.chapter_id
    ) as string | undefined;
  }, []);
  const resolveRevisionChapterTitle = useCallback((revision?: RevisionFlowData | null) => {
    if (!revision) return undefined;
    const anyRevision = revision as any;
    return (
      revision.chapterTitle ||
      anyRevision.chapter_title ||
      anyRevision.targetChapterTitle ||
      anyRevision.target_chapter_title
    ) as string | undefined;
  }, []);
  const resolveRevisionChapterOrder = useCallback((revision?: RevisionFlowData | null) => {
    if (!revision) return undefined;
    const anyRevision = revision as any;
    const editorAction = anyRevision.editorAction || anyRevision.editor_action || {};
    const rawOrder =
      anyRevision.chapterOrder ??
      anyRevision.chapter_order ??
      anyRevision.targetChapterOrder ??
      anyRevision.target_chapter_order ??
      editorAction.chapterOrder ??
      editorAction.chapter_order;
    if (rawOrder === undefined || rawOrder === null) return undefined;
    if (typeof rawOrder === 'number') {
      return Number.isFinite(rawOrder) ? rawOrder : undefined;
    }
    if (typeof rawOrder === 'string') {
      const trimmed = rawOrder.trim();
      if (!trimmed) return undefined;
      const numeric = Number(trimmed);
      return Number.isNaN(numeric) ? trimmed : numeric;
    }
    return undefined;
  }, []);
  const resolveRevisionPosition = useCallback((revision?: RevisionFlowData | null) => {
    if (!revision) return undefined;
    const editorAction = (revision as any).editorAction || (revision as any).editor_action;
    return (revision as any).editorPosition || editorAction?.position;
  }, []);
  const crossChapterPendingCount = useMemo(() => {
    if (!chapterId) return 0;
    const pendingIds = new Set<string>();

    const collectRevision = (revision: RevisionFlowData | undefined | null, fallbackId?: string) => {
      if (!revision) return;
      if (revision.status !== 'pending') return;
      const revisionChapterId = resolveRevisionChapterId(revision);
      if (!revisionChapterId || revisionChapterId === chapterId) return;
      const id = (revision.requestId || (revision as any).request_id || fallbackId) as string | undefined;
      if (id) pendingIds.add(id);
    };

    messages.forEach((message) => {
      const messageFlowItems = (message as any).flowItems || [];
      messageFlowItems.forEach((item: FlowItem) => {
        if (item.type === 'step') {
          const stepData = item.data as StepFlowData;
          collectRevision(stepData.revision as RevisionFlowData | undefined, stepData.revisionItemId || item.id);
          return;
        }
        if (item.type === 'revision') {
          collectRevision(item.data as RevisionFlowData, item.id);
        }
      });
    });

    return pendingIds.size;
  }, [chapterId, messages, resolveRevisionChapterId]);
  const disableBatchOperationControls = crossChapterPendingCount > 0;

  // 🔧 expandedMode 切换时保存/恢复滚动位置，避免跳动
  useLayoutEffect(() => {
    // 模式没变化，不处理
    if (prevExpandedModeRef.current === expandedMode) return;

    const getScrollContainer = () => messagesContainerRef.current;

    // 保存旧容器的滚动位置比例
    const oldContainer = getScrollContainer();
    if (oldContainer) {
      const { scrollTop, scrollHeight, clientHeight } = oldContainer;
      const maxScroll = scrollHeight - clientHeight;
      scrollPositionRef.current = maxScroll > 0 ? scrollTop / maxScroll : 0;
    }

    // 更新 ref
    prevExpandedModeRef.current = expandedMode;

    // 延迟恢复滚动位置（等待 DOM 更新）
    requestAnimationFrame(() => {
      const newContainer = getScrollContainer();
      if (newContainer) {
        const { scrollHeight, clientHeight } = newContainer;
        const maxScroll = scrollHeight - clientHeight;
        newContainer.scrollTop = maxScroll * scrollPositionRef.current;
      }
    });
  }, [expandedMode]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (hasOperations && !isLoading && !hasOperationsRef.current) {
      window.dispatchEvent(new CustomEvent('agent-operations-applied', {
        detail: { workId, chapterId }
      }));
    }
    hasOperationsRef.current = hasOperations;
  }, [hasOperations, isLoading, workId, chapterId]);
  const menuRef = useRef<HTMLDivElement>(null);
  const knowledgeListRef = useRef<HTMLDivElement>(null);

  const [selectedDocs, setSelectedDocs] = useState<Array<{ id: string; title: string }>>([]);
  const [optimizationSelected, setOptimizationSelected] = useState(false);
  const [selectionContext, setSelectionContext] = useState<{
    selected_text?: string;
    selected_text_html?: string;
    selection_position?: { from: number; to: number };
  } | null>(null);

  // 复制成功状态，显示提示
  const [copiedMessageId, setCopiedMessageId] = useState<string | null>(null);

  // 添加到知识库对话框状态
  const [showAddKnowledgeDialog, setShowAddKnowledgeDialog] = useState(false);
  const [knowledgeFormTitle, setKnowledgeFormTitle] = useState('');
  const [knowledgeFormContent, setKnowledgeFormContent] = useState('');
  const [knowledgeFormCategory, setKnowledgeFormCategory] = useState<'technique' | 'character' | 'worldview' | 'plot' | 'dialogue' | 'description' | 'reference' | 'other'>('reference');
  const [knowledgeFormTags, setKnowledgeFormTags] = useState('');
  const [knowledgeSubmitting, setKnowledgeSubmitting] = useState(false);

  // Toast 提示
  const { messages: toastMessages, success: showSuccess, error: showError, close: closeToast } = useToast();

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

  // 流式输出：真正的字符流，前端直接显示，不在前端处理换行效果

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

  // 打开添加知识对话框
  const handleOpenAddKnowledge = useCallback((title: string, content: string) => {
    setKnowledgeFormTitle(title);
    setKnowledgeFormContent(content);
    setKnowledgeFormCategory('reference');
    setKnowledgeFormTags('');
    setShowAddKnowledgeDialog(true);
  }, []);

  // 提交添加知识
  const handleSubmitKnowledge = useCallback(async () => {
    if (!knowledgeFormTitle.trim() || !knowledgeFormContent.trim()) return;

    try {
      setKnowledgeSubmitting(true);
      await knowledgeApi.create({
        title: knowledgeFormTitle.trim(),
        content: knowledgeFormContent.trim(),
        category: knowledgeFormCategory,
        tags: knowledgeFormTags.split(',').map((t) => t.trim()).filter(Boolean),
      });
      setShowAddKnowledgeDialog(false);
      // 重置表单
      setKnowledgeFormTitle('');
      setKnowledgeFormContent('');
      setKnowledgeFormCategory('reference');
      setKnowledgeFormTags('');
      showSuccess('添加成功', '内容已保存到知识库');
    } catch (error: any) {
      console.error('Failed to add knowledge:', error);
      const errorMessage = error?.response?.data?.detail || error?.message || '添加失败，请稍后重试';
      showError('添加失败', errorMessage);
    } finally {
      setKnowledgeSubmitting(false);
    }
  }, [knowledgeFormTitle, knowledgeFormContent, knowledgeFormCategory, knowledgeFormTags, showSuccess, showError]);

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

  // 定义 handleSendWithContext 用于处理带上下文的消息（InlineAI 消息）
  // 使用 useRef 存储回调函数，让 useEffect 不因回调变化而重新渲染
  const handleSendWithContextRef = useRef<(message: string, context?: any) => Promise<void>>(undefined);

  handleSendWithContextRef.current = async (message: string, context?: any) => {
    if (!message.trim() || isLoading) return;

    const backendMode: AgentChatRequest['mode'] = mode === 'agent' ? 'react' : 'planning';

    // 固定 payload 结构，将选中信息放入独立 selection 字段
    // 避免将选中文本放入 prompt/chapter_context 导致被覆盖或结构混乱
    const selectionData = context?.selected_text ? {
      text: context.selected_text,
      html: context.selected_text_html || context.selected_text,
      from: context.selection_position?.from,
      to: context.selection_position?.to,
    } : null;

    const locateHint = (() => {
      const quoted = getQuotedRangeLocateHint(message);
      if (Object.keys(quoted).length > 0) return quoted;
      return getStructuralLocateHint(message);
    })();

    const request: AgentChatRequest = {
      message,
      mode: backendMode,
      work_id: workId,
      chapter_id: chapterId,
      enable_reflection: mode === 'agent',
      context: {
        ...context,
        // 新增独立 selection 字段，推荐结构化
        selection: selectionData,
        // 保留 selected_text 字段以兼容旧逻辑
        selected_text: context?.selected_text,
        selection_position: context?.selection_position,
        nodes_info: getNodesInfoPayload(),
        ...locateHint,
        // chapter_context 只放章节标识，不放选中文本
        chapter_context: chapterId ? `当前章节ID: ${chapterId}` : undefined,
        // 如果有选中文本，添加结构化的指令上下文
        instruction_context: context?.selected_text
          ? `用户选中了以下文本进行操作:
---
${context.selected_text}
---
用户指令: ${message}`
          : undefined,
      },
    };

    // 用户发送消息时，将最新用户消息顶格，并停止自动跟随
    shouldAutoScrollRef.current = false;
    freezeAutoScrollRef.current = true;
    userScrollIntentRef.current = false;
    anchoredOnceRef.current = false;
    anchorLatestUserRef.current = true;
    skipAutoScrollRef.current = true;
    ignoreScrollEventRef.current = false; // 重置滚动事件忽略标志

    try {
      await sendMessageStream(request);
    } catch (err) {
      console.error('[AIPanel] Failed to send message:', err);
    }
  };

  // 稳定的回调封装，避免因依赖变化而重新创建
  const handleSendWithContext = useCallback((message: string, context?: any) => {
    return handleSendWithContextRef.current?.(message, context);
  }, []);

  // 监听来自编辑器 InlineAI 的消息，只有活跃窗口才监听
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
        // 直接传递原始 context，handleSendWithContext 会正确构建 selection 字段
        handleSendWithContext(item.message || '', item.context || {});
      }
    });
    (window as any).__inlineAIQueue__ = [];

    // 暴露全局回调
    (window as any).__agentInlineSend__ = (msg: string, ctx?: any, requestId?: string) => {
      const rid = requestId || `inline-${Date.now()}-${Math.random().toString(16).slice(2)}`;
      if (consumed.has(rid)) return;
      consumed.add(rid);
      // 直接传递原始 context，handleSendWithContext 会正确构建 selection 字段
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

      // 直接传递原始 context，handleSendWithContext 会正确构建 selection 字段
      handleSendWithContext(message, context);
    };

    window.addEventListener('inline-ai-send', handleInlineAIMessage as EventListener);

    return () => {
      window.removeEventListener('inline-ai-send', handleInlineAIMessage as EventListener);
      delete (window as any).__agentInlineSend__;
    };
  }, [handleSendWithContext, isActive]);

  // 监听 InlineAI intent（用于设置上下文，不发送消息）：全局 + 事件队列
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

  // 计算最后一条 agent 消息与索引，用于锚定与自动滚动逻辑
  const lastAgentMessage = useMemo(() => [...messages].reverse().find(m => m.role === 'agent'), [messages]);
  const flowItemsCount = (lastAgentMessage as any)?.flowItems?.length || 0;
  const lastUserMessageIndex = useMemo(() => {
    for (let i = messages.length - 1; i >= 0; i -= 1) {
      if (messages[i]?.role === 'user') return i;
    }
    return -1;
  }, [messages]);

  // 检查用户是否在底部
  const checkIfAtBottom = useCallback(() => {
    const container = messagesContainerRef.current;
    if (!container) return false;

    // 检查滚动位置是否接近底部（允许50px误差）
    const threshold = 50;
    const isAtBottom = container.scrollHeight - container.scrollTop - container.clientHeight < threshold;
    return isAtBottom;
  }, []);

  // 滚动到底部
  const scrollToBottom = useCallback((behavior: ScrollBehavior = 'smooth') => {
    const end = messagesEndRef.current;
    if (!end) return;
    end.scrollIntoView({ behavior, block: 'end' });
  }, []);

  // 滚动到最新用户消息位置（靠近顶部）
  const scrollUserMessageToTop = useCallback((offset: number = 0) => {
    const container = messagesContainerRef.current;
    const target = lastUserMessageRef.current;
    if (!container || !target) return;
    target.scrollIntoView({ block: 'start', behavior: 'auto' });
    if (offset) {
      container.scrollTop -= offset;
    }
  }, []);

  const markUserScrollIntent = useCallback(() => {
    userScrollIntentRef.current = true;
  }, []);

  const handleJumpToBottom = useCallback(() => {
    const container = messagesContainerRef.current;
    anchorLatestUserRef.current = false;
    skipAutoScrollRef.current = false;
    shouldAutoScrollRef.current = true;
    freezeAutoScrollRef.current = false;
    if (container) {
      container.scrollTop = container.scrollHeight;
    } else {
      scrollToBottom();
    }
    requestAnimationFrame(() => {
      syncAtBottomState(true);
    });
  }, [scrollToBottom, syncAtBottomState]);

  // 监听滚动事件，更新是否应该自动滚动的标志
  useEffect(() => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      if (ignoreScrollEventRef.current) return;
      const hasUserIntent = userScrollIntentRef.current;
      if (anchorLatestUserRef.current && hasUserIntent) {
        anchorLatestUserRef.current = false;
        skipAutoScrollRef.current = false;
      }
      userScrollIntentRef.current = false;
      const atBottom = checkIfAtBottom();
      syncAtBottomState(atBottom);
      if (freezeAutoScrollRef.current) {
        shouldAutoScrollRef.current = false;
        return;
      }
      shouldAutoScrollRef.current = atBottom;
    };

    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, [checkIfAtBottom, messages.length, syncAtBottomState]);

  // 当消息列表或执行轨迹更新时，如果用户在底部则自动滚动
  useEffect(() => {
    if (skipAutoScrollRef.current) {
      skipAutoScrollRef.current = false;
      return;
    }
    if (anchorLatestUserRef.current) {
      return;
    }
    if (freezeAutoScrollRef.current) {
      return;
    }
    if (shouldAutoScrollRef.current) {
      scrollToBottom();
    }
  }, [messages.length, tasks.length, flowItemsCount, scrollToBottom]);

  // 发送后仅做一次顶格，不持续跟随
  useLayoutEffect(() => {
    if (!anchorLatestUserRef.current) return;
    if (anchoredOnceRef.current) return;
    ignoreScrollEventRef.current = true;
    shouldAutoScrollRef.current = false;
    syncAtBottomState(checkIfAtBottom());
    // 标记已经开始处理顶格，防止重复触发
    anchoredOnceRef.current = true;
    requestAnimationFrame(() => {
      scrollUserMessageToTop();
      // 顶格完成后才重置 anchorLatestUserRef，确保 ResizeObserver 在此期间能保持顶格
      anchorLatestUserRef.current = false;
      ignoreScrollEventRef.current = false;
    });
  }, [checkIfAtBottom, messages.length, scrollBufferHeight, scrollUserMessageToTop, syncAtBottomState]);

  // 流式输出时内容高度变化，保持自动滚动/顶格
  useLayoutEffect(() => {
    const container = messagesContainerRef.current;
    const content = messagesContentRef.current;
    if (!container || !content || typeof ResizeObserver === 'undefined') return;

    let rafId: number | null = null;
    const observer = new ResizeObserver(() => {
      if (anchorLatestUserRef.current) {
        const target = lastUserMessageRef.current;
        if (!target) return;
        if (rafId !== null) cancelAnimationFrame(rafId);
        rafId = requestAnimationFrame(() => {
          const containerRect = container.getBoundingClientRect();
          const targetRect = target.getBoundingClientRect();
          const delta = targetRect.top - containerRect.top;
          if (Math.abs(delta) < 0.5) return;
          ignoreScrollEventRef.current = true;
          container.scrollTop += delta;
          ignoreScrollEventRef.current = false;
        });
        return;
      }
      if (!shouldAutoScrollRef.current || skipAutoScrollRef.current) {
        if (rafId !== null) cancelAnimationFrame(rafId);
        rafId = requestAnimationFrame(() => {
          syncAtBottomState(checkIfAtBottom());
        });
        return;
      }
      if (rafId !== null) cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(() => {
        scrollToBottom('auto');
      });
    });

    observer.observe(content);
    return () => {
      if (rafId !== null) cancelAnimationFrame(rafId);
      observer.disconnect();
    };
  }, [checkIfAtBottom, messages.length, scrollToBottom, syncAtBottomState]);

  // 流式输出：真正的字符流，前端直接使用 message.content

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
        if (manualMenuOpen) return;
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
      setManualMenuOpen(false);
      repositionMenu();
    },
    [manualMenuOpen, repositionMenu]
  );

  const syncAtStateFromRef = useCallback(() => {
    const el = inputRef.current;
    const caret = el?.selectionStart ?? null;
    const value = el?.value ?? inputValue;
    updateAtState(value, caret);
  }, [inputValue, updateAtState]);

  const handleInputFocus = useCallback(() => {
    isInputFocusedRef.current = true;
    syncAtStateFromRef();
  }, [syncAtStateFromRef]);

  const handleInputBlur = useCallback(() => {
    isInputFocusedRef.current = false;
    const container = messagesContainerRef.current;
    if (!container) return;
    const base = Math.max(container.clientHeight - 24, 0);
    const next = Math.min(Math.round(container.clientHeight * 0.6), base);
    setScrollBufferHeight(next);
  }, []);

  useEffect(() => {
    if (!containsAt && !manualMenuOpen) {
      setAtMenuOpen(false);
      setAtStage('root');
      setKnowledgePanelOpen(false);
      return;
    }
    if (containsAt) {
      syncAtStateFromRef();
    }
  }, [containsAt, inputValue, manualMenuOpen, syncAtStateFromRef]);

  useEffect(() => {
    if (!atMenuOpen || atStage === 'knowledge') return;
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
  }, [atMenuOpen, atStage, repositionMenu]);

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
    setManualMenuOpen(false);
    setKnowledgePanelOpen(false);
    setAtStage('root');
    setAtQuery('');
    setHighlightIndex(0);
    setAtTriggerIndex(null);
  }, []);

  useEffect(() => {
    if (!atMenuOpen) return;
    const handlePointerDown = (event: PointerEvent) => {
      const target = event.target as HTMLElement | null;
      if (!target) return;
      if (menuRef.current?.contains(target)) return;
      if (inputRef.current?.contains(target)) return;
      if (target.closest('[data-command-trigger="true"]')) return;
      closeAtMenu();
    };
    document.addEventListener('pointerdown', handlePointerDown);
    return () => {
      document.removeEventListener('pointerdown', handlePointerDown);
    };
  }, [atMenuOpen, closeAtMenu]);

  const openCommandMenu = useCallback(() => {
    setManualMenuOpen(true);
    setAtMenuOpen(true);
    setKnowledgePanelOpen(false);
    setAtStage('root');
    setAtQuery('');
    setHighlightIndex(0);
    setAtTriggerIndex(null);
    repositionMenu();
    requestAnimationFrame(() => inputRef.current?.focus());
  }, [repositionMenu]);

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
      setKnowledgePanelOpen(true);
      setAtStage('knowledge');
      setAtQuery('');
      setHighlightIndex(0);
      setAtMenuOpen(true);
    },
    [closeAtMenu, stripCurrentToken]
  );

  const handleRootHover = useCallback(
    (option: RootCommandOption, index: number) => {
      setHighlightIndex(index);
      if (option.key === 'knowledge') {
        if (!knowledgePanelOpen || atStage !== 'knowledge') {
          setKnowledgePanelOpen(true);
          setAtStage('knowledge');
        }
        return;
      }
      if (knowledgePanelOpen || atStage === 'knowledge') {
        setKnowledgePanelOpen(false);
        setAtStage('root');
      }
    },
    [knowledgePanelOpen, atStage]
  );

  const stopMenuScrollChain = useCallback((event: React.WheelEvent<HTMLDivElement>) => {
    const el = event.currentTarget;
    const { scrollTop, scrollHeight, clientHeight } = el;
    const delta = event.deltaY;
    const atTop = scrollTop <= 0;
    const atBottom = scrollTop + clientHeight >= scrollHeight - 1;
    if ((delta < 0 && atTop) || (delta > 0 && atBottom)) {
      event.preventDefault();
    }
    event.stopPropagation();
  }, []);

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

    // 先重置高度，确保 scrollHeight 能正确反映实际内容高度
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
    // Plan 模式 = 仅 Planning，无反思，任务列表固定
    const enableDeepAgent = mode === 'agent';

    const locateHint = (() => {
      const quoted = getQuotedRangeLocateHint(message);
      if (Object.keys(quoted).length > 0) return quoted;
      return getStructuralLocateHint(message);
    })();

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
        nodes_info: getNodesInfoPayload(),
        ...locateHint,
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

    // 用户发送消息时，将最新用户消息顶格，并停止自动跟随
    shouldAutoScrollRef.current = false;
    freezeAutoScrollRef.current = true;
    userScrollIntentRef.current = false;
    anchoredOnceRef.current = false;
    anchorLatestUserRef.current = true;
    skipAutoScrollRef.current = true;
    ignoreScrollEventRef.current = false; // 重置滚动事件忽略标志

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

  // 预留底部滚动缓冲，让最新消息可被顶到顶部
  useLayoutEffect(() => {
    const container = messagesContainerRef.current;
    if (!container || typeof ResizeObserver === 'undefined') return;

    const updateBuffer = () => {
      if (isInputFocusedRef.current) return;
      // Reduce the spacer so new messages don't leave an oversized blank area.
      const base = Math.max(container.clientHeight - 24, 0);
      const next = Math.min(Math.round(container.clientHeight * 0.6), base);
      setScrollBufferHeight(next);
    };

    updateBuffer();
    const observer = new ResizeObserver(() => {
      updateBuffer();
    });
    observer.observe(container);
    return () => observer.disconnect();
  }, [expandedMode, messages.length]);

  return (
    <div className="p-3 flex flex-col h-full min-h-0 dark:bg-slate-900 overflow-hidden">
      <ToastContainer messages={toastMessages} onClose={closeToast} />

      {/* 新会话欢迎界面 - 输入框居中偏上 */}
      {messages.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center min-h-0 pb-24">
          <h1 className="text-4xl font-medium text-zinc-700 dark:text-slate-200 mb-8">
            我能为你做什么？
          </h1>

          {/* 居中的输入框区域 */}
          <div className="w-full max-w-2xl rounded-3xl bg-white border border-gray-200 px-4 py-3 space-y-3 dark:bg-slate-800 dark:border-slate-700">
            <div className="relative">
              <div className="flex flex-wrap items-start gap-2 w-full min-h-12 px-1 py-2 rounded-xl bg-transparent text-gray-800 dark:text-slate-200">
                {/* 选中文本前置 */}
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
                    文本自然化
                    <button
                      type="button"
                      className="hover:text-zinc-900 transition-colors"
                      onMouseDown={(e) => e.preventDefault()}
                      onClick={(e) => {
                        e.preventDefault();
                        removeOptimization();
                      }}
                      aria-label="移除文本自然化"
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
                  onFocus={handleInputFocus}
                  onBlur={handleInputBlur}
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

            <div className="flex items-center justify-between gap-2">
              <button
                type="button"
                onClick={openCommandMenu}
                disabled={isLoading}
                data-command-trigger="true"
                className={`w-10 h-10 rounded-full bg-white text-gray-700 shadow-sm transition-colors flex items-center justify-center ring-1 ring-gray-200/60 dark:bg-slate-800 dark:text-slate-200 dark:ring-slate-700/60 ${
                  isLoading ? 'opacity-60 cursor-not-allowed' : 'hover:bg-gray-50 dark:hover:bg-slate-700'
                }`}
                aria-label="打开指令列表"
                title="指令"
              >
                <Plus className="w-4 h-4" strokeWidth={2.5} />
              </button>

              <div className="flex items-center gap-1.5">
                {isLoading ? (
                  <button
                    onClick={handleStop}
                    className="w-10 h-10 rounded-full bg-gray-200 hover:bg-gray-300 text-gray-800 flex items-center justify-center shadow-sm border border-gray-200 transition-colors dark:bg-slate-600 dark:hover:bg-slate-500 dark:text-slate-200 dark:border-slate-500"
                    aria-label="停止发送"
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
        </div>
      ) : (
        <>
        {/* 有消息时：消息列表 + 底部固定输入框 */}
        <div className="relative flex-1 min-h-0 mb-3">
          <div
            ref={messagesContainerRef}
            data-ai-scroll-container={isActive ? 'active' : undefined}
            className="h-full overflow-x-hidden overflow-y-auto scrollbar-auto-hide bg-white dark:bg-slate-900"
            onWheel={markUserScrollIntent}
            onPointerDown={markUserScrollIntent}
            onTouchStart={markUserScrollIntent}
          >
            <div className={`flex w-full ${expandedMode ? 'justify-center' : ''}`}>
            <div className={`${expandedMode ? 'w-full max-w-3xl' : 'w-full'}`}>
              <div ref={messagesContentRef} className="flex flex-col gap-2.5">
          {messages.map((message, index) => {
            // Skip null/undefined messages
            if (!message) {
              return null;
            }

            const isUser = message.role === 'user';
            const isLastMessage = index === messages.length - 1;


          if (isUser) {
            return (
              <div
                key={index}
                ref={index === lastUserMessageIndex ? lastUserMessageRef : null}
                className="flex items-start gap-2 justify-end"
              >
                <div className="flex flex-col gap-1 w-full items-end group">
                  <div className="relative p-2.5 rounded-2xl flex-initial w-fit max-w-[80%] md:max-w-[60ch] bg-gray-100 text-gray-800 dark:bg-slate-700 dark:text-slate-200 shadow-sm ml-auto break-words">
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
          // DEBUG: 检查 flowItems 是否正确加载
          if (process.env.NODE_ENV === 'development' && !isUser) {
            console.log(`[AIPanel] Message ${index} flowItems:`, messageFlowItems.length, messageFlowItems.map((i: any) => i?.type));
          }
          // v6.2: completion 应该和 output 一起显示在内容区域，而不是在执行轨迹区域
          // v6.6: 保留 agent_header 在执行轨迹区域，确保流式输出过程中也能显示 logo 和名称
          const flowItemsWithoutOutput = messageFlowItems.filter((item: any) =>
            item?.type !== 'output' && item?.type !== 'completion'
          );
          // 仅在“有实质执行信息”时才关闭 Thinking（忽略装饰性事件）
          const meaningfulFlowItems = flowItemsWithoutOutput.filter((item: any) =>
            item?.type !== 'agent_header' && item?.type !== 'text'
          );
          const outputItems = messageFlowItems.filter((item: any) => item?.type === 'output');
          const completionItem = messageFlowItems.find((item: any) => item?.type === 'completion');
          const lastOutputItem = outputItems.length > 0 ? outputItems[outputItems.length - 1] : null;
          const isStreamingMessage = isLastMessage && isLoading;
          const showActivityStream = isStreamingMessage && mode === 'agent' && activities.length > 0;
          const showThinking = isStreamingMessage && !showActivityStream && meaningfulFlowItems.length === 0;
          const showFlowBlock = flowItemsWithoutOutput.length > 0 || showActivityStream || showThinking;
          const findRevisionByItemId = (targetId: string): RevisionFlowData | null => {
            if (!targetId) return null;
            for (const item of messageFlowItems as FlowItem[]) {
              if (!item) continue;
              if (item.type === 'step') {
                const stepData = item.data as StepFlowData;
                if ((stepData.revisionItemId === targetId || item.id === targetId) && stepData.revision) {
                  return stepData.revision as RevisionFlowData;
                }
              }
              if (item.type === 'revision' && item.id === targetId) {
                return item.data as RevisionFlowData;
              }
            }
            return null;
          };

          return (
            <div key={index} className="space-y-2">
              {showFlowBlock && (
                <div className="flex items-start">
                  <div className="flex-1 !border-none !bg-transparent">
                    {flowItemsWithoutOutput.length > 0 && (
                      <ExecutionFlow
                        items={flowItemsWithoutOutput}
                        onAcceptRevision={(itemId, requestId, selectedVersion) => {
                          console.log('[AIPanel] RevisionCard accepted:', { itemId, requestId, selectedVersion });
                          const revisionData = findRevisionByItemId(itemId);
                          const resolvedRequestId = requestId || resolveRevisionRequestId(revisionData);
                          const targetChapterId = resolveRevisionChapterId(revisionData);
                          const isPendingApprovalMatch = Boolean(
                            pendingApproval &&
                            resolvedRequestId &&
                            pendingApproval.request_id === resolvedRequestId
                          );
                          const matchedPendingApproval = isPendingApprovalMatch ? pendingApproval : null;

                          // v7.2: 从 pendingApproval 中提取快照数据用于撤销/重做
                          let snapshot: {
                            originalContent?: string;
                            newContent?: string;
                            editorPosition?: { from: number; to: number };
                            selectedVersion?: number;
                          } | undefined;

                          if (matchedPendingApproval) {
                            // 根据不同类型提取快照数据
                            const originalContent = matchedPendingApproval.original_content;
                            let newContent = matchedPendingApproval.new_content;
                            const editorPosition = matchedPendingApproval.editor_action?.position;

                            // 如果是 rewrite 类型，使用选择的版本内容
                            if (matchedPendingApproval.action_type === 'rewrite' &&
                                selectedVersion !== undefined &&
                                matchedPendingApproval.versions?.[selectedVersion]?.content) {
                              newContent = matchedPendingApproval.versions[selectedVersion].content;
                            }

                            snapshot = {
                              originalContent,
                              newContent,
                              editorPosition,
                              selectedVersion
                            };

                            console.log('[AIPanel] 保存快照数据:', {
                              hasOriginal: !!originalContent,
                              hasNew: !!newContent,
                              hasPosition: !!editorPosition,
                              selectedVersion
                            });
                          }

                          // 如果是 pendingApproval，且 requestId 匹配，则走统一审批链路（成功后再落状态）
                          if (matchedPendingApproval) {
                            submitApproval(true, selectedVersion).then((success) => {
                              updateRevisionStatus(itemId, success ? 'accepted' : 'pending', snapshot);
                            });
                          } else if (resolvedRequestId) {
                            const targetChapterTitle = resolveRevisionChapterTitle(revisionData);
                            const targetChapterOrder = resolveRevisionChapterOrder(revisionData);
                            const hasOrderHint =
                              targetChapterOrder !== undefined && targetChapterOrder !== null;
                            const shouldJumpById = Boolean(
                              targetChapterId &&
                              (!chapterId || chapterId !== targetChapterId)
                            );
                            const shouldJumpByHint = Boolean(
                              !targetChapterId &&
                              (targetChapterTitle || hasOrderHint)
                            );
                            const shouldJumpAfterAccept = shouldJumpById || shouldJumpByHint;
                            const shouldDispatchLocalAcceptEvent = Boolean(targetChapterId || !shouldJumpByHint);
                            const effectiveChapterId = targetChapterId;
                            if (shouldJumpAfterAccept) {
                              console.info('[AIPanel] 采纳后尝试定位目标章节', {
                                requestId: resolvedRequestId,
                                currentChapterId: chapterId,
                                targetChapterId,
                                targetChapterTitle,
                                targetChapterOrder
                              });
                            }
                            // v7.5: 非阻塞式修订 - 直接调用后端 API 写入数据
                            console.log('[AIPanel] 非阻塞式修订，直接调用后端 API');
                            agentApi.submitApprovalResponse({
                              request_id: resolvedRequestId,
                              approved: true,
                              selected_version: selectedVersion,
                              chapter_id: effectiveChapterId,
                              work_id: workId
                            }).then(() => {
                              console.log('[AIPanel] ✅ 修订已写入数据库');
                              if (workId) {
                                window.dispatchEvent(new CustomEvent('agent-chapter-confirm', {
                                  detail: { work_id: workId }
                                }));
                                console.log('[AIPanel] ✅ 派发章节确认事件，刷新列表');
                              }
                              if (shouldDispatchLocalAcceptEvent) {
                                window.dispatchEvent(
                                  new CustomEvent('agent-accept-revision', {
                                    detail: {
                                      request_id: resolvedRequestId,
                                      revision_id: itemId,
                                      chapter_id: targetChapterId
                                    }
                                  })
                                );
                              } else {
                                console.info('[AIPanel] 跳过本地采纳事件，等待章节定位后刷新内容', {
                                  requestId: resolvedRequestId
                                });
                              }
                              if (shouldJumpAfterAccept) {
                                window.dispatchEvent(
                                  new CustomEvent('agent-jump-revision', {
                                    detail: {
                                      workId,
                                      chapterId: targetChapterId,
                                      chapterTitle: targetChapterTitle,
                                      chapterOrder: targetChapterOrder,
                                      requestId: resolvedRequestId,
                                      revisionId: resolvedRequestId,
                                      position: resolveRevisionPosition(revisionData)
                                    }
                                  })
                                );
                              }
                              updateRevisionStatus(itemId, 'accepted', snapshot);
                            }).catch((err) => {
                              console.error('[AIPanel] 写入数据库失败:', err);
                              updateRevisionStatus(itemId, 'pending');
                            });
                          } else {
                            console.error('[AIPanel] 缺少 request_id，无法提交采纳:', { itemId, revisionData });
                            showError('修订缺少 request_id，无法采纳，请重试或重新生成');
                            updateRevisionStatus(itemId, 'pending', snapshot);
                          }
                        }}
                        onDiscardRevision={(itemId, requestId) => {
                          console.log('[AIPanel] RevisionCard discarded:', { itemId, requestId });
                          const revisionData = findRevisionByItemId(itemId);
                          const resolvedRequestId = requestId || resolveRevisionRequestId(revisionData);
                          const targetChapterId = resolveRevisionChapterId(revisionData);
                          const isPendingApprovalMatch = Boolean(
                            pendingApproval &&
                            resolvedRequestId &&
                            pendingApproval.request_id === resolvedRequestId
                          );
                          const matchedPendingApproval = isPendingApprovalMatch ? pendingApproval : null;

                          // v7.2: 从 pendingApproval 中提取快照数据用于重做
                          let snapshot: {
                            originalContent?: string;
                            newContent?: string;
                            editorPosition?: { from: number; to: number };
                            selectedVersion?: number;
                          } | undefined;

                          if (matchedPendingApproval) {
                            const originalContent = matchedPendingApproval.original_content;
                            const newContent = matchedPendingApproval.new_content;
                            const editorPosition = matchedPendingApproval.editor_action?.position;

                            snapshot = {
                              originalContent,
                              newContent,
                              editorPosition
                            };
                          }

                          if (matchedPendingApproval) {
                            submitApproval(false).then((success) => {
                              updateRevisionStatus(itemId, success ? 'discarded' : 'pending', snapshot);
                            });
                          } else if (resolvedRequestId) {
                            const targetChapterTitle = resolveRevisionChapterTitle(revisionData);
                            const targetChapterOrder = resolveRevisionChapterOrder(revisionData);
                            const hasOrderHint =
                              targetChapterOrder !== undefined && targetChapterOrder !== null;
                            const shouldDeferLocalDiscard = Boolean(
                              !targetChapterId && (targetChapterTitle || hasOrderHint)
                            );
                            const effectiveChapterId = targetChapterId;
                            const chapterMismatch = Boolean(
                              chapterId &&
                              targetChapterId &&
                              chapterId !== targetChapterId
                            );
                            if (chapterMismatch && targetChapterId) {
                              console.info('[AIPanel] 跨章节弃用，按目标章节提交', {
                                requestId: resolvedRequestId,
                                currentChapterId: chapterId,
                                targetChapterId
                              });
                            }
                            // v7.5: 非阻塞式修订 - 直接调用后端 API
                            console.log('[AIPanel] 非阻塞式修订，直接调用后端 API (弃用)');
                            agentApi.submitApprovalResponse({
                              request_id: resolvedRequestId,
                              approved: false,
                              chapter_id: effectiveChapterId,
                              work_id: workId
                            }).then(() => {
                              if (!shouldDeferLocalDiscard) {
                                window.dispatchEvent(
                                  new CustomEvent('agent-discard-revision', {
                                    detail: {
                                      request_id: resolvedRequestId,
                                      revision_id: itemId,
                                      chapter_id: effectiveChapterId
                                    }
                                  })
                                );
                              } else {
                                console.info('[AIPanel] 跳过本地弃用事件，等待章节定位/刷新后同步状态', {
                                  requestId: resolvedRequestId
                                });
                              }
                              updateRevisionStatus(itemId, 'discarded', snapshot);
                            }).catch((err) => {
                              console.error('[AIPanel] 弃用请求失败:', err);
                              updateRevisionStatus(itemId, 'pending');
                            });
                          } else {
                            console.error('[AIPanel] 缺少 request_id，无法提交弃用:', { itemId, revisionData });
                            showError('修订缺少 request_id，无法弃用，请重试或重新生成');
                            updateRevisionStatus(itemId, 'pending', snapshot);
                          }
                        }}
                        onJumpRevision={(itemId, requestId) => {
                          console.log('[AIPanel] RevisionCard jump:', { itemId, requestId });
                          const revisionData = findRevisionByItemId(itemId);
                          const resolvedRequestId = requestId || resolveRevisionRequestId(revisionData);
                          const targetChapterId = resolveRevisionChapterId(revisionData);
                          const targetChapterTitle = resolveRevisionChapterTitle(revisionData);
                          const targetChapterOrder = resolveRevisionChapterOrder(revisionData);
                          const targetRevisionId = resolvedRequestId || itemId;
                          window.dispatchEvent(
                            new CustomEvent('agent-jump-revision', {
                              detail: {
                                workId,
                                chapterId: targetChapterId,
                                chapterTitle: targetChapterTitle,
                                chapterOrder: targetChapterOrder,
                                revisionId: targetRevisionId,
                                requestId: resolvedRequestId,
                                position: resolveRevisionPosition(revisionData)
                              }
                            })
                          );
                        }}
                        onUndoRevision={(itemId) => {
                          console.log('[AIPanel] RevisionCard undo:', { itemId });
                          undoRevision(itemId);
                        }}
                        onRedoRevision={(itemId) => {
                          console.log('[AIPanel] RevisionCard redo:', { itemId });
                          redoRevision(itemId);
                        }}
                        // v7.3: 批量操作回调
                        onAcceptAllRevisions={(itemIds) => {
                          console.log('[AIPanel] Accept all revisions:', itemIds);
                          acceptAllRevisions(itemIds);
                        }}
                        onDiscardAllRevisions={(itemIds) => {
                          console.log('[AIPanel] Discard all revisions:', itemIds);
                          discardAllRevisions(itemIds);
                        }}
                      />
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
                      <span className="text-[12px] text-zinc-400 dark:text-slate-400 thinking-blink">
                        Thinking...
                      </span>
                    )}
                  </div>
                </div>
              )}

              {/* v6.6: 只有当有实际内容时才显示内容区域（AgentHeader 已在执行轨迹区域显示）*/}
              {(message.content || lastOutputItem) && (
                <div className="flex items-start">
                  <div className="flex flex-col gap-1 w-full group">
                    <div className="text-zinc-500 dark:text-slate-300">
                      {/* v6.5: 统一使用 ExecutionFlow 样式，删除纯文本降级逻辑 */}
                      <ExecutionFlow
                        items={[{
                          id: lastOutputItem?.id || `output-fallback-${index}`,
                          type: 'output' as const,
                          data: {
                            title: (lastOutputItem?.data as any)?.title || '回复',
                            content: message.content || (lastOutputItem?.data as any)?.content || '',
                            intro: (lastOutputItem?.data as any)?.intro,
                            introHighlight: (lastOutputItem?.data as any)?.introHighlight,
                            isApplicable: (lastOutputItem?.data as any)?.isApplicable,
                          },
                          timestamp: lastOutputItem?.timestamp || message.timestamp,
                        }]}
                        onAddToKnowledge={handleOpenAddKnowledge}
                        onApplyContent={(content) => {
                          // 派发 agent-show-revision 事件到编辑器
                          window.dispatchEvent(new CustomEvent('agent-show-revision', {
                            detail: {
                              type: 'continue',
                              replacement: content,
                              revisionId: `output-${Date.now()}`
                            }
                          }));
                        }}
                      />
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
          <div aria-hidden="true" style={{ height: scrollBufferHeight }} />
                </div>
              </div>
            </div>
          </div>

          {!isAtBottom && (
            <button
              type="button"
              onClick={handleJumpToBottom}
              className="absolute bottom-3 left-1/2 -translate-x-1/2 inline-flex items-center justify-center w-9 h-9 rounded-full border border-zinc-200 bg-white/90 text-zinc-600 shadow-lg backdrop-blur transition hover:text-zinc-900 hover:border-zinc-300 dark:border-slate-600 dark:bg-slate-800/90 dark:text-slate-200 dark:hover:text-white"
              aria-label="滚动到最新消息"
            >
              <ChevronDown className="w-4 h-4" />
            </button>
          )}
        </div>

      <div className={`flex w-full ${expandedMode ? 'justify-center' : ''}`}>
        <div className={`${expandedMode ? 'w-full max-w-3xl' : 'w-full'}`}>
          {/* v8.0: 批量操作确认（采纳/弃用）- 放在任务列表上方 */}
          {hasOperations && !isLoading && (
            <div className="mb-2 p-3 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800">
              <p className="text-[12px] text-zinc-600 dark:text-slate-300 mb-2">
                Agent 已执行章节操作，请确认是否保留这些修改：
              </p>
              {disableBatchOperationControls && (
                <p className="text-[11px] text-amber-600 dark:text-amber-400 mb-2">
                  检测到跨章节修订，需逐条采纳或撤销后才能进行批量操作。
                </p>
              )}
              <div className="flex gap-2">
                <button
                  onClick={rollbackAllOperations}
                  disabled={disableBatchOperationControls}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 text-[11px] bg-zinc-100 hover:bg-zinc-200 text-zinc-700 dark:bg-slate-700 dark:hover:bg-slate-600 dark:text-slate-200 rounded-full border border-zinc-200 dark:border-slate-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <X className="w-3.5 h-3.5" />
                  撤销
                </button>
                <button
                  onClick={acceptAllOperations}
                  disabled={disableBatchOperationControls}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 text-[11px] bg-green-50 hover:bg-green-100 text-green-700 dark:bg-green-900/30 dark:hover:bg-green-900/50 dark:text-green-400 rounded-full border border-green-200 dark:border-green-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Check className="w-3.5 h-3.5" />
                  采纳
                </button>
              </div>
            </div>
          )}

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

          {/* 模式选择 + 输入框（放在下方区域）*/}
          <div className="rounded-3xl bg-white border border-gray-200 px-4 py-3 space-y-3 flex-shrink-0 dark:bg-slate-800 dark:border-slate-700">
            <div className="relative">
              <div className="flex flex-wrap items-start gap-2 w-full min-h-12 px-1 py-2 rounded-xl bg-transparent text-gray-800 dark:text-slate-200">
                {/* 选中文本前置（放在后，保持同一行逻辑）*/}
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
                    文本自然化
                    <button
                      type="button"
                      className="hover:text-zinc-900 transition-colors"
                      onMouseDown={(e) => e.preventDefault()}
                      onClick={(e) => {
                        e.preventDefault();
                        removeOptimization();
                      }}
                      aria-label="移除文本自然化"
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
                  onFocus={handleInputFocus}
                  onBlur={handleInputBlur}
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
                章节内容超过 5000 字，已截断超过的 {truncatedCount} 字符进行去痕迹处理
              </div>
            )}

            <div className="flex items-center justify-between gap-2">
              <button
                type="button"
                onClick={openCommandMenu}
                disabled={isLoading}
                data-command-trigger="true"
                className={`w-10 h-10 rounded-full bg-white text-gray-700 shadow-sm transition-colors flex items-center justify-center ring-1 ring-gray-200/60 dark:bg-slate-800 dark:text-slate-200 dark:ring-slate-700/60 ${
                  isLoading ? 'opacity-60 cursor-not-allowed' : 'hover:bg-gray-50 dark:hover:bg-slate-700'
                }`}
                aria-label="打开指令列表"
                title="指令"
              >
                <Plus className="w-4 h-4" strokeWidth={2.5} />
              </button>

              <div className="flex items-center gap-1.5">
                {isLoading ? (
                  <button
                    onClick={handleStop}
                    className="w-10 h-10 rounded-full bg-gray-200 hover:bg-gray-300 text-gray-800 flex items-center justify-center shadow-sm border border-gray-200 transition-colors dark:bg-slate-600 dark:hover:bg-slate-500 dark:text-slate-200 dark:border-slate-500"
                    aria-label="\u505c\u6b62\u53d1\u9001"
                  >
                    <Square className="w-4 h-4" strokeWidth={2.5} />
                  </button>
                ) : inputValue.trim() ? (
                  <button
                    onClick={handleSend}
                    disabled={!inputValue.trim()}
                    className="w-10 h-10 rounded-full transition-all flex items-center justify-center bg-gray-900 text-white hover:bg-gray-800 active:scale-95 shadow-sm dark:bg-blue-600 dark:hover:bg-blue-500"
                    aria-label="\u53d1\u9001"
                  >
                    <Send className="h-4 w-4" strokeWidth={2.4} />
                  </button>
                ) : null}
              </div>
            </div>
          </div>
        </div>
      </div>
      </>
      )}

      {atMenuOpen && menuPosition &&
        createPortal(
          <div
            className="fixed z-[1200]"
            data-scroll-scope="command-menu"
            style={{
              left: menuPosition.left,
              top: menuPosition.top,
              width: knowledgePanelOpen && atStage === 'knowledge'
                ? MENU_COLUMN_WIDTH * 2 + MENU_GAP
                : MENU_COLUMN_WIDTH
            }}
          >
            {atStage === 'knowledge' && knowledgePanelOpen ? (
              <div ref={menuRef} className="grid grid-cols-2 gap-2 items-start">
                <div className="rounded-2xl border border-slate-200 bg-white text-slate-900 shadow-2xl overflow-hidden w-full self-start dark:border-slate-800/70 dark:bg-slate-900 dark:text-slate-50">
                  <div className="max-h-72 overflow-y-auto custom-scrollbar px-2 py-2" onWheel={stopMenuScrollChain}>
                    {filteredRootOptions.length > 0 ? (
                      filteredRootOptions.map((option, idx) => {
                        const isHighlighted = knowledgePanelOpen && atStage === 'knowledge'
                          ? option.key === 'knowledge'
                          : idx === highlightIndex;
                        return (
                          <button
                            key={option.key}
                            type="button"
                            onMouseDown={(e) => e.preventDefault()}
                            onClick={() => handleRootOption(option)}
                            onMouseEnter={() => handleRootHover(option, idx)}
                            className={`w-full px-3 py-2.5 rounded-xl flex items-center justify-between text-left transition-colors ${
                              isHighlighted
                                ? 'bg-slate-100 ring-1 ring-slate-200 dark:bg-slate-800/80 dark:ring-slate-600/60'
                                : 'hover:bg-slate-50 dark:hover:bg-slate-800/60'
                            }`}
                          >
                            <div className="flex items-center gap-2">
                              <span className="text-slate-700 dark:text-slate-200">{option.icon}</span>
                              <div className="flex flex-col">
                                <span className="text-[12px] text-slate-900 dark:text-white">{option.label}</span>
                              </div>
                            </div>
                            {option.hasChildren && <ChevronRight className="w-4 h-4 text-slate-400" />}
                          </button>
                        );
                      })
                    ) : (
                      <div className="px-3 py-2 text-[12px] text-slate-400">{'\u6ca1\u6709\u5339\u914d\u7684\u6307\u4ee4'}</div>
                    )}
                  </div>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-white text-slate-900 shadow-2xl overflow-hidden w-full -mt-4 dark:border-slate-800/70 dark:bg-slate-900 dark:text-slate-50">
                  <div
                    ref={knowledgeListRef}
                    className="max-h-[220px] overflow-y-auto overscroll-contain custom-scrollbar px-2 py-2"
                    onWheel={stopMenuScrollChain}
                  >
                    <div className="space-y-1">
                      {knowledgeLoading && (
                        <div className="px-3 py-2 text-[12px] text-slate-500 dark:text-slate-400 flex items-center gap-2">
                          <Loader2 className="w-4 h-4 animate-spin" />
                          {'\u6b63\u5728\u52a0\u8f7d\u77e5\u8bc6\u5e93\u6587\u6863...'}
                        </div>
                      )}
                      {knowledgeError && !knowledgeLoading && (
                        <div className="px-3 py-2 text-[12px] text-amber-600 dark:text-amber-200">
                          {knowledgeError}
                        </div>
                      )}
                      {!knowledgeLoading && !knowledgeError && filteredKnowledgeDocs.length === 0 && (
                        <div className="px-3 py-2 text-[12px] text-slate-500 dark:text-slate-400">暂无可用文档</div>
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
                                ? 'bg-slate-100 ring-1 ring-slate-200 dark:bg-slate-800/80 dark:ring-slate-600/60'
                                : 'hover:bg-slate-50 dark:hover:bg-slate-800/60'
                            }`}
                          >
                            <div className="flex items-center gap-2 min-w-0">
                              <Tag className="w-4 h-4 text-slate-600 dark:text-slate-200" />
                              <span className="text-[12px] text-slate-900 dark:text-white truncate max-w-[150px]">{doc.title}</span>
                            </div>
                          </button>
                        ))}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div
                ref={menuRef}
                className="rounded-2xl border border-slate-200 bg-white text-slate-900 shadow-2xl overflow-hidden w-full dark:border-slate-800/70 dark:bg-slate-900 dark:text-slate-50"
              >
                <div className="max-h-72 overflow-y-auto custom-scrollbar px-2 py-2" onWheel={stopMenuScrollChain}>
                  {filteredRootOptions.length > 0 ? (
                    filteredRootOptions.map((option, idx) => (
                      <button
                        key={option.key}
                        type="button"
                        onMouseDown={(e) => e.preventDefault()}
                        onClick={() => handleRootOption(option)}
                        onMouseEnter={() => handleRootHover(option, idx)}
                        className={`w-full px-3 py-2.5 rounded-xl flex items-center justify-between text-left transition-colors ${
                          idx === highlightIndex
                            ? 'bg-slate-100 ring-1 ring-slate-200 dark:bg-slate-800/80 dark:ring-slate-600/60'
                            : 'hover:bg-slate-50 dark:hover:bg-slate-800/60'
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          <span className="text-slate-700 dark:text-slate-200">{option.icon}</span>
                          <div className="flex flex-col">
                            <span className="text-[12px] text-slate-900 dark:text-white">{option.label}</span>
                          </div>
                        </div>
                        {option.hasChildren && <ChevronRight className="w-4 h-4 text-slate-400" />}
                      </button>
                    ))
                  ) : (
                    <div className="px-3 py-2 text-[12px] text-slate-400">{'\u6ca1\u6709\u5339\u914d\u7684\u6307\u4ee4'}</div>
                  )}
                </div>
              </div>
            )}
          </div>,
          document.body
        )}

      {/* 添加到知识库对话框*/}
      <Dialog open={showAddKnowledgeDialog} onOpenChange={setShowAddKnowledgeDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>添加到知识库</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">标题</label>
              <Input
                value={knowledgeFormTitle}
                onChange={(e) => setKnowledgeFormTitle(e.target.value)}
                placeholder="输入标题..."
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">分类</label>
              <Select value={knowledgeFormCategory} onValueChange={(value: any) => setKnowledgeFormCategory(value)}>
                <SelectTrigger className="mt-1 w-full">
                  <SelectValue placeholder="选择分类" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="technique">{'\u5199\u4f5c\u6280\u5de7'}</SelectItem>
                  <SelectItem value="character">特色设定</SelectItem>
                  <SelectItem value="worldview">{'\u4e16\u754c\u89c2'}</SelectItem>
                  <SelectItem value="plot">支线剧情</SelectItem>
                  <SelectItem value="dialogue">对话台词</SelectItem>
                  <SelectItem value="description">场景描写</SelectItem>
                  <SelectItem value="reference">{'\u53c2\u8003\u8d44\u6599'}</SelectItem>
                  <SelectItem value="other">其他</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">内容</label>
              <textarea
                value={knowledgeFormContent}
                onChange={(e) => setKnowledgeFormContent(e.target.value)}
                placeholder="输入知识内容..."
                className="mt-1 w-full h-40 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm resize-none bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">标签</label>
              <Input
                value={knowledgeFormTags}
                onChange={(e) => setKnowledgeFormTags(e.target.value)}
                placeholder="\u7528\u9017\u53f7\u5206\u9694\uff0c\u4f8b\u5982\uff1a\u5199\u4f5c\u6280\u5de7, \u7279\u8272\u8bbe\u5b9a"
                className="mt-1"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAddKnowledgeDialog(false)}>
              取消
            </Button>
            <Button onClick={handleSubmitKnowledge} disabled={knowledgeSubmitting || !knowledgeFormTitle.trim() || !knowledgeFormContent.trim()}>
              {knowledgeSubmitting ? '\u6dfb\u52a0\u4e2d...' : '\u6dfb\u52a0'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}












