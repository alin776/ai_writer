/**
 * ChatInput - Agent chat input with @ directive menu.
 * - Multiline input, Enter send / Shift+Enter newline
 * - Optional context textarea
 * - Mode selector
 * - @ menu (root: @Knowledge -> tags, @optimization)
 */

import React, { useEffect, useLayoutEffect, useMemo, useRef, useState, KeyboardEvent } from 'react';
import { createPortal } from 'react-dom';
import {
  Square,
  Send,
  BookOpen,
  Sparkles,
  ChevronRight,
  ChevronLeft,
  Loader2,
  X,
} from 'lucide-react';
import ModeSelector, { type AgentMode } from './ModeSelector';
import { knowledgeApi } from '@/services/knowledgeApi';

interface ChatInputProps {
  onSend: (message: string, context?: any) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
  mode: AgentMode;
  onModeChange: (mode: AgentMode) => void;
  isLoading?: boolean;
  onStop?: () => void;
  selectionContext?: {
    selected_text?: string;
    selected_text_html?: string;
    selection_position?: { from: number; to: number };
  };
  onClearSelection?: () => void;
}

type AtCommandStage = 'root' | 'knowledge' | 'optimization';

// 去痕迹强度选项
type OptimizationIntensity = 'light' | 'medium' | 'strong';

interface IntensityOption {
  key: OptimizationIntensity;
  label: string;
  description: string;
  changePercent: string;
}

const INTENSITY_OPTIONS: IntensityOption[] = [
  {
    key: 'light',
    label: '轻度',
    description: '仅去除明显AI套话，保持原文风格',
    changePercent: '~5%',
  },
  {
    key: 'medium',
    label: '中度',
    description: '平衡自然度与内容保留，推荐使用',
    changePercent: '~20%',
  },
  {
    key: 'strong',
    label: '强度',
    description: '深度重构句式，最大化自然度',
    changePercent: '~40%',
  },
];

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
    description: '引用知识库文档',
    icon: <BookOpen className="w-4 h-4" />,
    hasChildren: true,
  },
  {
    key: 'optimization',
    label: '@optimization',
    description: '开启 AI 去痕迹',
    icon: <Sparkles className="w-4 h-4" />,
    hasChildren: true,
  },
];

// 知识库文档类型
interface KnowledgeDoc {
  id: string;
  title: string;
}

const escapeRegExp = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

export default function ChatInput({
  onSend,
  disabled = false,
  placeholder = '输入消息...',
  maxLength = 2000,
  mode,
  onModeChange,
  isLoading = false,
  onStop,
  selectionContext,
  onClearSelection,
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [showContext, setShowContext] = useState(false);
  const [contextText, setContextText] = useState('');

  const [atMenuOpen, setAtMenuOpen] = useState(false);
  const [atStage, setAtStage] = useState<AtCommandStage>('root');
  const [atQuery, setAtQuery] = useState('');
  const [highlightIndex, setHighlightIndex] = useState(0);
  const [knowledgeDocs, setKnowledgeDocs] = useState<KnowledgeDoc[]>([]);
  const [knowledgeLoading, setKnowledgeLoading] = useState(false);
  const [knowledgeError, setKnowledgeError] = useState<string | null>(null);
  const [atTriggerIndex, setAtTriggerIndex] = useState<number | null>(null);
  const [menuPosition, setMenuPosition] = useState<{ left: number; top: number; width: number } | null>(null);
  // 已选择的文档（用于胶囊显示和发送）
  const [selectedDocs, setSelectedDocs] = useState<KnowledgeDoc[]>([]);
  // 已选择的去痕迹强度
  const [selectedIntensity, setSelectedIntensity] = useState<OptimizationIntensity | null>(null);

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // 检测是否启用了优化（通过@optimization或选择了强度）
  const optimizationEnabled = useMemo(
    () => message.toLowerCase().includes('@optimization') || selectedIntensity !== null,
    [message, selectedIntensity]
  );
  const containsAt = useMemo(() => message.includes('@') || message.includes('＠'), [message]);

  const MAX_HUMANIZE_CHARS = 5000;
  const truncatedChapterContent =
    contextText && optimizationEnabled && contextText.length > MAX_HUMANIZE_CHARS
      ? contextText.slice(0, MAX_HUMANIZE_CHARS)
      : contextText;
  const truncatedCount =
    contextText && optimizationEnabled && contextText.length > MAX_HUMANIZE_CHARS
      ? contextText.length - MAX_HUMANIZE_CHARS
      : 0;

  const filteredRootOptions = useMemo(() => {
    const query = atQuery.trim().toLowerCase();
    if (!query) return ROOT_OPTIONS;
    return ROOT_OPTIONS.filter(
      (opt) =>
        opt.label.toLowerCase().includes(query) || opt.description.toLowerCase().includes(query)
    );
  }, [atQuery]);

  const filteredKnowledgeDocs = useMemo(() => {
    const query = atQuery.trim().toLowerCase();
    if (!query) return knowledgeDocs;
    return knowledgeDocs.filter((doc) => doc.title.toLowerCase().includes(query));
  }, [atQuery, knowledgeDocs]);

  // Debug: component mount
  useEffect(() => {
    console.log('[ChatInput] mounted');
  }, []);

  // 选区引用到达时自动聚焦输入框
  useEffect(() => {
    if (selectionContext?.selected_text && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [selectionContext]);

  const adjustHeight = () => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = 'auto';
    const nextHeight = Math.min(textarea.scrollHeight, 240);
    textarea.style.height = `${nextHeight}px`;
    textarea.style.overflowY = textarea.scrollHeight > 240 ? 'auto' : 'hidden';
    textarea.style.overflowX = 'hidden';
    textarea.style.whiteSpace = 'pre-wrap';
    textarea.style.wordBreak = 'break-word';
    textarea.style.overflowWrap = 'break-word';
  };

  const repositionMenu = () => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    const rect = textarea.getBoundingClientRect();
    const estimatedHeight = 280;
    const belowSpace = window.innerHeight - rect.bottom;
    let top = rect.bottom + 8; // fixed 相对视口，无需加 scroll
    if (belowSpace < estimatedHeight && rect.top > estimatedHeight) {
      top = rect.top - estimatedHeight - 8;
    }
    setMenuPosition({
      left: rect.left,
      top,
      width: rect.width,
    });
  };

  const updateAtState = (value: string, caret: number | null) => {
    if (caret === null) return;

    const lastAscii = value.lastIndexOf('@', caret - 1);
    const lastFull = value.lastIndexOf('＠', caret - 1);
    const triggerIndex = Math.max(lastAscii, lastFull);
    if (triggerIndex === -1) {
      return;
    }

    const tokenText = value.slice(triggerIndex + 1, caret);
    if (tokenText.includes(' ') || tokenText.includes('\n')) {
      return;
    }

    setAtMenuOpen(true);
    setAtTriggerIndex(triggerIndex);
    setAtQuery(tokenText.toLowerCase());
    setHighlightIndex(0);
    repositionMenu();
  };

  const syncAtStateFromRef = () => {
    const textarea = textareaRef.current;
    const caret = textarea?.selectionStart ?? null;
    const value = textarea?.value ?? message;
    updateAtState(value, caret);
    repositionMenu();
  };

  useLayoutEffect(() => {
    adjustHeight();
  }, [message]);

  // Always open menu when 存在 @，确保不被事件时机影响
  useEffect(() => {
    syncAtStateFromRef();
    if (containsAt) {
      setAtMenuOpen(true);
      setAtStage('root');
      setAtQuery('');
      setHighlightIndex(0);
      repositionMenu();
    } else {
      setAtMenuOpen(false);
    }
    console.log('[ChatInput] message change', { message, containsAt, atMenuOpen: true });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [message, containsAt]);

  useEffect(() => {
    if (!atMenuOpen) return;
    repositionMenu();
    const handleWindowChange = () => repositionMenu();
    window.addEventListener('resize', handleWindowChange);
    window.addEventListener('scroll', handleWindowChange, true);
    return () => {
      window.removeEventListener('resize', handleWindowChange);
      window.removeEventListener('scroll', handleWindowChange, true);
    };
  }, [atMenuOpen]);

  useEffect(() => {
    const loadDocs = async () => {
      try {
        setKnowledgeLoading(true);
        setKnowledgeError(null);
        const docs = await knowledgeApi.getDocTitles();
        setKnowledgeDocs(docs || []);
      } catch (error: any) {
        setKnowledgeError(error?.message || '知识库文档获取失败');
      } finally {
        setKnowledgeLoading(false);
      }
    };

    if (atMenuOpen && atStage === 'knowledge' && knowledgeDocs.length === 0 && !knowledgeLoading) {
      loadDocs();
    }
  }, [atMenuOpen, atStage, knowledgeDocs.length, knowledgeLoading]);

  const closeAtMenu = () => {
    setAtMenuOpen(false);
    setAtStage('root');
    setAtQuery('');
    setHighlightIndex(0);
    setAtTriggerIndex(null);
  };

  const insertDirectiveText = (text: string) => {
    const textarea = textareaRef.current;
    const caret = textarea?.selectionStart ?? message.length;
    const start = atTriggerIndex ?? Math.max(caret - (atQuery.length + 1), 0);
    const rest = message.slice(start + 1);
    const nextSpaceIndex = rest.search(/[\s]/);
    const end = nextSpaceIndex === -1 ? message.length : start + 1 + nextSpaceIndex;

    let prefix = message.slice(0, start);
    let suffix = message.slice(end);

    if (prefix && !/\s$/.test(prefix)) prefix += ' ';
    if (suffix && !suffix.startsWith(' ')) suffix = ' ' + suffix;
    else if (!suffix) suffix = ' ';

    const newValue = `${prefix}${text}${suffix}`;
    setMessage(newValue);
    closeAtMenu();

    requestAnimationFrame(() => {
      if (textarea) {
        const pos = Math.min(prefix.length + text.length + 1, newValue.length);
        textarea.setSelectionRange(pos, pos);
      }
    });
  };

  const handleRootOption = (option: RootCommandOption) => {
    if (option.key === 'knowledge') {
      setAtStage('knowledge');
      setAtQuery('');
      setHighlightIndex(0);
      return;
    }
    if (option.key === 'optimization') {
      setAtStage('optimization');
      setAtQuery('');
      setHighlightIndex(0);
      return;
    }
  };

  const handleKnowledgeOption = (doc: KnowledgeDoc) => {
    // 添加到已选文档列表（避免重复）
    setSelectedDocs((prev) => {
      if (prev.some((d) => d.id === doc.id)) return prev;
      return [...prev, doc];
    });
    // 关闭菜单，清除 @ 触发文本
    const textarea = textareaRef.current;
    const caret = textarea?.selectionStart ?? message.length;
    const start = atTriggerIndex ?? Math.max(caret - (atQuery.length + 1), 0);
    const rest = message.slice(start + 1);
    const nextSpaceIndex = rest.search(/[\s]/);
    const end = nextSpaceIndex === -1 ? message.length : start + 1 + nextSpaceIndex;
    const newValue = message.slice(0, start) + message.slice(end);
    setMessage(newValue.trim());
    closeAtMenu();
  };

  const handleOptimizationOption = (intensity: IntensityOption) => {
    // 设置选择的强度
    setSelectedIntensity(intensity.key);
    // 关闭菜单，清除 @ 触发文本
    const textarea = textareaRef.current;
    const caret = textarea?.selectionStart ?? message.length;
    const start = atTriggerIndex ?? Math.max(caret - (atQuery.length + 1), 0);
    const rest = message.slice(start + 1);
    const nextSpaceIndex = rest.search(/[\s]/);
    const end = nextSpaceIndex === -1 ? message.length : start + 1 + nextSpaceIndex;
    const newValue = message.slice(0, start) + message.slice(end);
    setMessage(newValue.trim());
    closeAtMenu();
  };

  const handleMenuSelect = (index: number) => {
    if (!atMenuOpen) return;
    if (atStage === 'knowledge') {
      const doc = filteredKnowledgeDocs[index];
      if (doc) handleKnowledgeOption(doc);
    } else if (atStage === 'optimization') {
      const intensity = INTENSITY_OPTIONS[index];
      if (intensity) handleOptimizationOption(intensity);
    } else {
      const option = filteredRootOptions[index];
      if (option) handleRootOption(option);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setMessage(value);
    adjustHeight();
    updateAtState(value, e.target.selectionStart);
  };

  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (!trimmedMessage || disabled) return;

    const contextPayload = contextText.trim()
      ? {
          text: optimizationEnabled ? truncatedChapterContent?.trim() || contextText.trim() : contextText.trim(),
          chapter_context: contextText.trim(),
          current_content: optimizationEnabled ? truncatedChapterContent?.trim() || contextText.trim() : contextText.trim(),
        }
      : {};

    const directiveContext =
      selectedDocs.length || optimizationEnabled
        ? {
            ...(selectedDocs.length ? { knowledge_doc_ids: selectedDocs.map((d) => d.id) } : {}),
            ...(optimizationEnabled
              ? {
                  use_optimization: true,
                  intensity: selectedIntensity || 'medium',
                  ...(truncatedChapterContent
                    ? {
                        current_content: truncatedChapterContent,
                        text: truncatedChapterContent,
                      }
                    : {}),
                }
              : {}),
          }
        : {};

    const selectionPayload = selectionContext?.selected_text
      ? {
          selected_text: selectionContext.selected_text,
          selected_text_html: selectionContext.selected_text_html || selectionContext.selected_text,
          selection_position: selectionContext.selection_position,
          chapter_context: selectionContext.selected_text
            ? `Selected text:\n${selectionContext.selected_text}\n\nUser instruction:\n${trimmedMessage}`
            : undefined,
        }
      : {};

    const mergedContext = { ...selectionPayload, ...contextPayload, ...directiveContext };
    const hasContext = Object.keys(mergedContext).length > 0;

    onSend(trimmedMessage, hasContext ? mergedContext : undefined);

    setMessage('');
    setContextText('');
    setShowContext(false);
    setSelectedDocs([]);
    setSelectedIntensity(null);
    closeAtMenu();
    if (onClearSelection) onClearSelection();
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    const activeLength =
      atStage === 'knowledge'
        ? filteredKnowledgeDocs.length
        : atStage === 'optimization'
        ? INTENSITY_OPTIONS.length
        : filteredRootOptions.length;

    if (atMenuOpen && activeLength > 0) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setHighlightIndex((prev) => (prev + 1) % activeLength);
        return;
      }
      if (e.key === 'ArrowUp') {
        e.preventDefault();
        setHighlightIndex((prev) => (prev - 1 + activeLength) % activeLength);
        return;
      }
      if (e.key === 'Enter') {
        e.preventDefault();
        handleMenuSelect(highlightIndex);
        return;
      }
      if (e.key === 'Escape') {
        e.preventDefault();
        closeAtMenu();
        return;
      }
    }

    if (e.key === '@' || e.key === '＠') {
      setAtMenuOpen(true);
      setAtStage('root');
      setAtQuery('');
      setHighlightIndex(0);
      repositionMenu();
      return;
    }

    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const removeKnowledgeDoc = (docId: string) => {
    setSelectedDocs((prev) => prev.filter((d) => d.id !== docId));
  };

  const removeOptimization = () => {
    setMessage((prev) => prev.replace(/\s*@optimization\s*/gi, ' ').replace(/\s+/g, ' ').trimStart());
    setSelectedIntensity(null);
  };

  const charCount = message.length;
  const isNearLimit = charCount > maxLength * 0.8;
  const isOverLimit = charCount > maxLength;
  const hasMessage = !!message.trim() || selectedDocs.length > 0;
  const isSendDisabled = disabled || (!message.trim() && selectedDocs.length === 0) || isOverLimit;
  const showStop = isLoading && !!onStop;
  const showSend = (!!message.trim() || selectedDocs.length > 0) && !showStop;

  const menuContent = (
    <div
      style={{
        position: 'fixed',
        left: menuPosition ? menuPosition.left : 12,
        top: menuPosition ? menuPosition.top : 12,
        width: menuPosition ? Math.min(380, menuPosition.width || 360) : 320,
        background: '#fff',
        border: '1px solid #e5e7eb',
        borderRadius: 12,
        boxShadow: '0 12px 30px rgba(0,0,0,0.14)',
        zIndex: 99999,
        pointerEvents: 'auto',
      }}
    >
      <div className="p-2">
        {atStage === 'knowledge' ? (
          <div className="flex items-center gap-2 px-1 pb-1 text-xs text-gray-600">
            <button
              type="button"
              onClick={() => {
                setAtStage('root');
                setAtQuery('');
                setHighlightIndex(0);
              }}
              className="p-1 rounded-md hover:bg-gray-100 text-gray-500"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="font-medium text-gray-800">@Knowledge</span>
            <span className="text-gray-400">·</span>
            <span className="text-gray-500">选择知识库文档</span>
          </div>
        ) : atStage === 'optimization' ? (
          <div className="flex items-center gap-2 px-1 pb-1 text-xs text-gray-600">
            <button
              type="button"
              onClick={() => {
                setAtStage('root');
                setAtQuery('');
                setHighlightIndex(0);
              }}
              className="p-1 rounded-md hover:bg-gray-100 text-gray-500"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="font-medium text-gray-800">@optimization</span>
            <span className="text-gray-400">·</span>
            <span className="text-gray-500">选择去痕强度</span>
          </div>
        ) : (
          <div className="px-1 pb-1 text-xs text-gray-500">选择要插入的 @ 指令</div>
        )}

        <div className="max-h-64 overflow-y-auto space-y-1">
          {atStage === 'knowledge' ? (
            <>
              {knowledgeLoading && (
                <div className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  加载知识库文档...
                </div>
              )}
              {knowledgeError && !knowledgeLoading && (
                <div className="px-3 py-2 text-xs text-red-500">{knowledgeError}</div>
              )}
              {!knowledgeLoading && !knowledgeError && filteredKnowledgeDocs.length === 0 && (
                <div className="px-3 py-2 text-xs text-gray-500">暂无可用文档</div>
              )}
              {!knowledgeLoading &&
                !knowledgeError &&
                filteredKnowledgeDocs.map((doc, index) => {
                  const selected = index === highlightIndex;
                  const isAlreadySelected = selectedDocs.some((d) => d.id === doc.id);
                  return (
                    <button
                      key={doc.id}
                      onClick={() => handleKnowledgeOption(doc)}
                      onMouseEnter={() => setHighlightIndex(index)}
                      disabled={isAlreadySelected}
                      className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-left transition-colors ${
                        isAlreadySelected
                          ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                          : selected
                          ? 'bg-blue-50 border border-blue-100 text-blue-800'
                          : 'hover:bg-gray-50'
                      }`}
                    >
                      <span className="inline-flex items-center justify-center w-7 h-7 rounded-md bg-gray-100 text-gray-700">
                        <BookOpen className="w-4 h-4" />
                      </span>
                      <span className="text-sm font-medium truncate">{doc.title}</span>
                      {isAlreadySelected && (
                        <span className="ml-auto text-xs text-gray-400">已选择</span>
                      )}
                    </button>
                  );
                })}
            </>
          ) : atStage === 'optimization' ? (
            <>
              {INTENSITY_OPTIONS.map((intensity, index) => {
                const selected = index === highlightIndex;
                const isCurrentSelection = selectedIntensity === intensity.key;
                return (
                  <button
                    key={intensity.key}
                    onClick={() => handleOptimizationOption(intensity)}
                    onMouseEnter={() => setHighlightIndex(index)}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-left transition-colors ${
                      isCurrentSelection
                        ? 'bg-purple-50 border border-purple-200 text-purple-800'
                        : selected
                        ? 'bg-blue-50 border border-blue-100 text-blue-800'
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className={`inline-flex items-center justify-center w-8 h-8 rounded-md ${
                        isCurrentSelection ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-700'
                      }`}>
                        <Sparkles className="w-4 h-4" />
                      </span>
                      <div className="text-left">
                        <div className="text-sm font-medium flex items-center gap-2">
                          {intensity.label}
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-gray-100 text-gray-500">
                            {intensity.changePercent}
                          </span>
                        </div>
                        <div className="text-xs text-gray-500">{intensity.description}</div>
                      </div>
                    </div>
                    {isCurrentSelection && (
                      <span className="text-xs text-purple-600 font-medium">当前</span>
                    )}
                  </button>
                );
              })}
            </>
          ) : (
            <>
              {filteredRootOptions.map((option, index) => {
                const selected = index === highlightIndex;
                return (
                  <button
                    key={option.key}
                    onClick={() => handleRootOption(option)}
                    onMouseEnter={() => setHighlightIndex(index)}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-left transition-colors ${
                      selected ? 'bg-blue-50 border border-blue-100 text-blue-800' : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="inline-flex items-center justify-center w-8 h-8 rounded-md bg-gray-100 text-gray-700">
                        {option.icon}
                      </span>
                      <div className="text-left">
                        <div className="text-sm font-medium">{option.label}</div>
                        <div className="text-xs text-gray-500">{option.description}</div>
                      </div>
                    </div>
                    {option.hasChildren && <ChevronRight className="w-4 h-4 text-gray-400" />}
                  </button>
                );
              })}
            </>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="chat-input-wrapper space-y-2">
      {createPortal(
        <div
          style={{
            position: 'fixed',
            bottom: 8,
            right: 8,
            padding: '6px 10px',
            background: 'rgba(34,197,94,0.18)',
            color: '#166534',
            fontSize: 11,
            borderRadius: 8,
            zIndex: 100000,
            pointerEvents: 'none',
          }}
        >
          ChatInput active
        </div>,
        document.body
      )}
      {/* Context input */}
      {selectionContext?.selected_text && (
        <div className="flex items-start gap-3 rounded-xl border border-gray-200 bg-gray-50 px-3 py-2">
          <span className="inline-flex items-center justify-center w-9 h-9 rounded-full bg-gray-900 text-white text-xs font-semibold shadow-sm">
            <Sparkles className="w-4 h-4" />
          </span>
          <div className="flex-1 min-w-0">
            <div className="text-[11px] text-gray-500 mb-1 leading-tight">引用选中文本</div>
            <div
              className="text-sm text-gray-800 leading-snug break-words"
              style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}
              title={selectionContext.selected_text}
            >
              {selectionContext.selected_text}
            </div>
          </div>
          <button
            type="button"
            onClick={onClearSelection}
            className="mt-1 p-1 rounded-full hover:bg-gray-200 text-gray-500"
            aria-label="移除引用"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}
      {showContext && (
        <div className="context-input p-3 bg-gray-50 border border-gray-200 rounded-xl">
          <div className="flex items-center justify-between mb-1.5">
            <label className="text-xs font-medium text-gray-700">附加上下文（可选）</label>
            <button
              onClick={() => setShowContext(false)}
              className="text-gray-400 hover:text-gray-600 text-xs"
            >
              关闭
            </button>
          </div>
          <textarea
            value={contextText}
            onChange={(e) => setContextText(e.target.value)}
            placeholder="输入章节内容、待分析文本等..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none text-xs bg-white"
            rows={3}
          />
          <div className="text-[10px] text-gray-500 mt-1">提示: 这些内容会作为额外上下文发送给AI</div>
        </div>
      )}

      <div className="rounded-2xl border border-gray-200 bg-white shadow-sm px-4 py-3 space-y-3 relative">
        {/* Input */}
        <div className="relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            onKeyUp={syncAtStateFromRef}
            onClick={syncAtStateFromRef}
            onFocus={syncAtStateFromRef}
            disabled={disabled}
            placeholder={placeholder}
            className={`w-full px-1 py-1 pr-16 text-sm min-h-[72px] resize-none bg-transparent border-none focus:outline-none focus-visible:outline-none focus:ring-0 whitespace-pre-wrap break-words leading-relaxed ${
              disabled ? 'text-gray-400 cursor-not-allowed' : 'text-gray-800'
            } ${isOverLimit ? 'focus:ring-red-400' : ''}`}
            rows={3}
            maxLength={maxLength}
            wrap="soft"
            style={{
              wordBreak: 'break-word',
              overflowWrap: 'break-word',
              whiteSpace: 'pre-wrap',
              overflowY: 'hidden',
              overflowX: 'hidden',
            }}
          />

          {/* Char counter */}
          <div
            className={`absolute right-1 bottom-1 text-[11px] ${
              isOverLimit
                ? 'text-red-500 font-semibold'
                : isNearLimit
                ? 'text-orange-500'
                : 'text-gray-400'
            }`}
          >
            {charCount}/{maxLength}
          </div>
        </div>

        {/* @ menu portal */}
        {atMenuOpen && createPortal(
          <>
            {/* Debug overlay to 确认渲染 */}
            <div style={{
              position: 'fixed',
              left: 8,
              top: 8,
              padding: '4px 8px',
              background: 'rgba(99,102,241,0.12)',
              color: '#312e81',
              fontSize: 10,
              borderRadius: 6,
              zIndex: 99998,
              pointerEvents: 'none'
            }}>
              @menu
            </div>
            {menuContent}
          </>,
          document.body
        )}

        {/* Selected chips */}
        {(optimizationEnabled || selectedDocs.length > 0) && (
          <div className="flex flex-wrap gap-2 border border-dashed border-gray-200 rounded-lg px-3 py-2 bg-gray-50">
            {optimizationEnabled && (
              <span className="inline-flex items-center gap-1.5 px-2 py-1 rounded-full bg-purple-50 text-purple-700 text-xs font-medium border border-purple-100">
                <Sparkles className="w-3.5 h-3.5" />
                <span>AI去痕迹</span>
                {selectedIntensity && (
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-purple-100 text-purple-600 font-medium">
                    {INTENSITY_OPTIONS.find(i => i.key === selectedIntensity)?.label || '中度'}
                  </span>
                )}
                {truncatedCount > 0 && (
                  <span className="text-[10px] text-amber-600 ml-1">
                    已截断 {truncatedCount} 字
                  </span>
                )}
                <button
                  type="button"
                  onClick={removeOptimization}
                  className="p-0.5 rounded-full hover:bg-purple-100 text-purple-600"
                  aria-label="移除 AI 去痕迹"
                >
                  <X className="w-3 h-3" />
                </button>
              </span>
            )}
            {selectedDocs.map((doc) => (
              <span
                key={doc.id}
                className="inline-flex items-center gap-1.5 px-2 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-medium border border-blue-100"
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>{doc.title}</span>
                <button
                  type="button"
                  onClick={() => removeKnowledgeDoc(doc.id)}
                  className="p-0.5 rounded-full hover:bg-blue-100 text-blue-600"
                  aria-label={`移除文档 ${doc.title}`}
                >
                  <X className="w-3 h-3" />
                </button>
              </span>
            ))}
          </div>
        )}

        {/* Toolbar */}
        <div className="flex items-center justify-between gap-3">
          <ModeSelector
            mode={mode}
            onModeChange={onModeChange}
            disabled={disabled}
            compact
            className="shrink-0"
          />

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowContext(!showContext)}
              disabled={disabled}
              className={`px-3 py-2 rounded-full border border-transparent text-sm transition-colors ${
                showContext ? 'bg-primary-50 text-primary-700' : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
              } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
              title="添加上下文"
            >
              上下文
            </button>

            {showStop ? (
              <button
                onClick={onStop}
                className="w-10 h-10 rounded-full bg-gray-200 hover:bg-gray-300 text-gray-800 flex items-center justify-center shadow-sm border border-gray-200 transition-colors"
                aria-label="停止对话"
              >
                <Square className="w-4 h-4" strokeWidth={2.5} />
              </button>
            ) : showSend ? (
              <button
                onClick={handleSend}
                disabled={isSendDisabled}
                className="w-10 h-10 rounded-full transition-all flex items-center justify-center bg-gray-900 text-white hover:bg-gray-800 active:scale-95 shadow-sm"
                aria-label="发送"
              >
                <Send className="w-4 h-4" strokeWidth={2.4} />
              </button>
            ) : null}
          </div>
        </div>

        <div className="text-[11px] text-gray-500 flex items-center gap-2 pt-1">
          <span>按 Enter 发送</span>
          <span className="text-gray-300">·</span>
          <span>Shift + Enter 换行</span>
        </div>
      </div>
    </div>
  );
}
