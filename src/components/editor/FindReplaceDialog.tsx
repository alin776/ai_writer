/**
 * 全文查找替换悬浮窗组件
 */
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Editor } from '@tiptap/react';
import { Plugin, PluginKey, Transaction, EditorState } from 'prosemirror-state';
import { Decoration, DecorationSet } from 'prosemirror-view';
import {
  X,
  Search,
  Replace,
  ChevronUp,
  ChevronDown,
  CaseSensitive,
  WholeWord,
  GripHorizontal,
} from 'lucide-react';

interface FindReplaceDialogProps {
  editor: Editor;
  isOpen: boolean;
  onClose: () => void;
}

interface MatchResult {
  from: number;
  to: number;
  text: string;
}

// 创建高亮插件的 PluginKey
const findReplacePluginKey = new PluginKey('findReplace');
const FIND_REPLACE_PLUGIN_NAME = '__findReplacePlugin__';

const FindReplaceDialog: React.FC<FindReplaceDialogProps> = ({
  editor,
  isOpen,
  onClose,
}) => {
  const [findText, setFindText] = useState('');
  const [replaceText, setReplaceText] = useState('');
  const [caseSensitive, setCaseSensitive] = useState(false);
  const [wholeWord, setWholeWord] = useState(false);
  const [matches, setMatches] = useState<MatchResult[]>([]);
  const [currentMatchIndex, setCurrentMatchIndex] = useState(-1);
  const [replaceCount, setReplaceCount] = useState(0);
  const [showReplaceSuccess, setShowReplaceSuccess] = useState(false);

  // 拖动相关状态
  const [position, setPosition] = useState({ x: window.innerWidth - 420, y: 80 });
  const [isDragging, setIsDragging] = useState(false);
  const dragOffset = useRef({ x: 0, y: 0 });
  const dialogRef = useRef<HTMLDivElement>(null);

  const findInputRef = useRef<HTMLInputElement>(null);

  // 打开时聚焦到查找输入框
  useEffect(() => {
    if (isOpen && findInputRef.current) {
      findInputRef.current.focus();
      // 如果有选中文本，自动填入查找框
      const { from, to } = editor.state.selection;
      if (from !== to) {
        const selectedText = editor.state.doc.textBetween(from, to, ' ');
        if (selectedText && selectedText.length < 100) {
          setFindText(selectedText);
        }
      }
    }
  }, [isOpen, editor]);

  // 搜索并返回匹配结果
  const findAllMatches = useCallback((searchText: string): MatchResult[] => {
    if (!searchText.trim()) {
      return [];
    }

    const doc = editor.state.doc;
    const results: MatchResult[] = [];

    doc.descendants((node, pos) => {
      if (node.isText && node.text) {
        const text = node.text;
        let search = searchText;
        let nodeText = text;

        if (!caseSensitive) {
          search = search.toLowerCase();
          nodeText = text.toLowerCase();
        }

        let index = 0;
        while (index < nodeText.length) {
          const foundIndex = nodeText.indexOf(search, index);
          if (foundIndex === -1) break;

          // 检查整词匹配
          if (wholeWord) {
            const before = foundIndex > 0 ? nodeText[foundIndex - 1] : ' ';
            const after = foundIndex + search.length < nodeText.length
              ? nodeText[foundIndex + search.length]
              : ' ';
            const isWordBoundaryBefore = /\s|[，。！？、；：""''【】《》（）\[\]{}.,!?;:'"()\-]/.test(before);
            const isWordBoundaryAfter = /\s|[，。！？、；：""''【】《》（）\[\]{}.,!?;:'"()\-]/.test(after);

            if (!isWordBoundaryBefore || !isWordBoundaryAfter) {
              index = foundIndex + 1;
              continue;
            }
          }

          results.push({
            from: pos + foundIndex,
            to: pos + foundIndex + searchText.length,
            text: text.slice(foundIndex, foundIndex + searchText.length),
          });

          index = foundIndex + 1;
        }
      }
    });

    return results;
  }, [editor, caseSensitive, wholeWord]);

  // 更新高亮装饰
  const updateHighlights = useCallback((matchResults: MatchResult[], currentIndex: number) => {
    // 移除旧插件
    const existingPlugins = editor.state.plugins.filter(
      (p: any) => p.__findReplacePlugin !== true
    );

    if (matchResults.length === 0) {
      // 如果没有匹配，只移除旧插件
      if (existingPlugins.length !== editor.state.plugins.length) {
        const newState = editor.state.reconfigure({ plugins: existingPlugins });
        editor.view.updateState(newState);
      }
      return;
    }

    // 创建装饰
    const decorations = matchResults.map((match, index) => {
      const isCurrent = index === currentIndex;
      return Decoration.inline(match.from, match.to, {
        class: isCurrent ? 'find-replace-current' : 'find-replace-highlight',
        style: isCurrent
          ? 'background-color: #f97316; color: white; border-radius: 2px; padding: 1px 0;'
          : 'background-color: #fef08a; border-radius: 2px; padding: 1px 0;',
      });
    });

    // 创建新插件
    const decorationSet = DecorationSet.create(editor.state.doc, decorations);
    const plugin = new Plugin({
      key: findReplacePluginKey,
      state: {
        init(): DecorationSet {
          return decorationSet;
        },
        apply(tr: Transaction, oldState: DecorationSet): DecorationSet {
          return oldState.map(tr.mapping, tr.doc);
        },
      },
      props: {
        decorations(state: EditorState): DecorationSet | undefined {
          return findReplacePluginKey.getState(state);
        },
      },
    });

    // 标记这是查找替换插件
    (plugin as any).__findReplacePlugin = true;

    // 添加新插件
    const newPlugins = [...existingPlugins, plugin];
    const newState = editor.state.reconfigure({ plugins: newPlugins });
    editor.view.updateState(newState);
  }, [editor]);

  // 清除高亮
  const clearHighlights = useCallback(() => {
    try {
      const filteredPlugins = editor.state.plugins.filter(
        (p: any) => p.__findReplacePlugin !== true
      );

      if (filteredPlugins.length !== editor.state.plugins.length) {
        const newState = editor.state.reconfigure({ plugins: filteredPlugins });
        editor.view.updateState(newState);
      }
    } catch (e) {
      console.error('清除高亮失败:', e);
    }
  }, [editor]);

  // 搜索文本
  const findMatches = useCallback(() => {
    const results = findAllMatches(findText);
    setMatches(results);

    if (results.length > 0) {
      const newIndex = 0;
      setCurrentMatchIndex(newIndex);
      updateHighlights(results, newIndex);
      // 跳转到第一个匹配
      editor.chain().focus().setTextSelection(results[0].from).run();
      scrollToMatch(results[0]);
    } else {
      setCurrentMatchIndex(-1);
      clearHighlights();
    }
  }, [findText, findAllMatches, updateHighlights, clearHighlights, editor]);

  // 滚动到匹配位置
  const scrollToMatch = (match: MatchResult) => {
    const { from } = match;
    const coords = editor.view.coordsAtPos(from);
    const editorElement = document.querySelector('.novel-editor .ProseMirror');
    if (editorElement && coords) {
      const editorRect = editorElement.getBoundingClientRect();
      const scrollTop = coords.top - editorRect.top - editorRect.height / 3;
      editorElement.scrollBy({ top: scrollTop, behavior: 'smooth' });
    }
  };

  // 上一个匹配
  const goToPrevMatch = () => {
    if (matches.length === 0) return;
    const newIndex = currentMatchIndex <= 0 ? matches.length - 1 : currentMatchIndex - 1;
    setCurrentMatchIndex(newIndex);
    updateHighlights(matches, newIndex);
    editor.chain().focus().setTextSelection(matches[newIndex].from).run();
    scrollToMatch(matches[newIndex]);
  };

  // 下一个匹配
  const goToNextMatch = () => {
    if (matches.length === 0) return;
    const newIndex = currentMatchIndex >= matches.length - 1 ? 0 : currentMatchIndex + 1;
    setCurrentMatchIndex(newIndex);
    updateHighlights(matches, newIndex);
    editor.chain().focus().setTextSelection(matches[newIndex].from).run();
    scrollToMatch(matches[newIndex]);
  };

  // 替换当前匹配
  const replaceCurrent = () => {
    if (matches.length === 0 || currentMatchIndex < 0) return;

    const match = matches[currentMatchIndex];
    editor
      .chain()
      .focus()
      .setTextSelection({ from: match.from, to: match.to })
      .deleteSelection()
      .insertContent(replaceText)
      .run();

    setReplaceCount(1);
    setShowReplaceSuccess(true);
    setTimeout(() => setShowReplaceSuccess(false), 2000);

    // 重新搜索
    setTimeout(() => findMatches(), 50);
  };

  // 全部替换
  const replaceAll = () => {
    if (matches.length === 0) return;

    // 从后往前替换，避免位置偏移问题
    const sortedMatches = [...matches].sort((a, b) => b.from - a.from);

    let chain = editor.chain();
    sortedMatches.forEach((match) => {
      chain = chain
        .setTextSelection({ from: match.from, to: match.to })
        .deleteSelection()
        .insertContent(replaceText);
    });
    chain.run();

    const count = matches.length;
    setReplaceCount(count);
    setShowReplaceSuccess(true);
    setTimeout(() => setShowReplaceSuccess(false), 3000);

    // 清空匹配
    setMatches([]);
    setCurrentMatchIndex(-1);
    clearHighlights();
  };

  // 监听查找文本变化
  useEffect(() => {
    const timer = setTimeout(() => {
      findMatches();
    }, 200);
    return () => clearTimeout(timer);
  }, [findText, caseSensitive, wholeWord]);

  // 关闭时清理
  useEffect(() => {
    if (!isOpen) {
      clearHighlights();
      setFindText('');
      setReplaceText('');
      setMatches([]);
      setCurrentMatchIndex(-1);
      setReplaceCount(0);
      setShowReplaceSuccess(false);
    }
  }, [isOpen, clearHighlights]);

  // 拖动处理
  const handleMouseDown = (e: React.MouseEvent) => {
    if (dialogRef.current) {
      setIsDragging(true);
      const rect = dialogRef.current.getBoundingClientRect();
      dragOffset.current = {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      };
    }
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDragging) {
        const newX = Math.max(0, Math.min(window.innerWidth - 400, e.clientX - dragOffset.current.x));
        const newY = Math.max(0, Math.min(window.innerHeight - 100, e.clientY - dragOffset.current.y));
        setPosition({ x: newX, y: newY });
      }
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging]);

  // 键盘快捷键
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      if (e.shiftKey) {
        goToPrevMatch();
      } else {
        goToNextMatch();
      }
      e.preventDefault();
    } else if (e.key === 'Escape') {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div
      ref={dialogRef}
      className="fixed z-50 bg-white dark:bg-slate-800 rounded-xl shadow-2xl w-[380px] overflow-hidden border border-zinc-200 dark:border-slate-600"
      style={{
        left: position.x,
        top: position.y,
        cursor: isDragging ? 'grabbing' : 'default',
      }}
      onKeyDown={handleKeyDown}
    >
      {/* 标题栏 - 可拖动 */}
      <div
        className="flex items-center justify-between px-3 py-2 border-b border-zinc-100 dark:border-slate-700 bg-zinc-50 dark:bg-slate-800/80 cursor-grab active:cursor-grabbing select-none"
        onMouseDown={handleMouseDown}
      >
        <div className="flex items-center gap-2">
          <GripHorizontal className="w-4 h-4 text-zinc-400 dark:text-slate-500" />
          <h3 className="text-xs font-medium text-zinc-700 dark:text-slate-300 flex items-center gap-1.5">
            <Replace className="w-3.5 h-3.5" />
            查找替换
          </h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded hover:bg-zinc-200 dark:hover:bg-slate-600 transition-colors"
        >
          <X className="w-3.5 h-3.5 text-zinc-500 dark:text-slate-400" />
        </button>
      </div>

      {/* 内容区域 */}
      <div className="p-3 space-y-3">
        {/* 查找输入框 */}
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zinc-400 dark:text-slate-500" />
          <input
            ref={findInputRef}
            type="text"
            value={findText}
            onChange={(e) => setFindText(e.target.value)}
            placeholder="查找..."
            className="w-full pl-8 pr-20 py-2 text-sm border border-zinc-200 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-zinc-800 dark:text-slate-200 placeholder-zinc-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500"
          />
          {/* 匹配计数和导航 */}
          <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-0.5">
            {findText && (
              <span className="text-[10px] text-zinc-500 dark:text-slate-400 mr-1">
                {matches.length > 0 ? `${currentMatchIndex + 1}/${matches.length}` : '0'}
              </span>
            )}
            <button
              onClick={goToPrevMatch}
              disabled={matches.length === 0}
              className="p-0.5 rounded hover:bg-zinc-100 dark:hover:bg-slate-600 disabled:opacity-30"
              title="上一个 (Shift+Enter)"
            >
              <ChevronUp className="w-3.5 h-3.5 text-zinc-500 dark:text-slate-400" />
            </button>
            <button
              onClick={goToNextMatch}
              disabled={matches.length === 0}
              className="p-0.5 rounded hover:bg-zinc-100 dark:hover:bg-slate-600 disabled:opacity-30"
              title="下一个 (Enter)"
            >
              <ChevronDown className="w-3.5 h-3.5 text-zinc-500 dark:text-slate-400" />
            </button>
          </div>
        </div>

        {/* 替换输入框 */}
        <div className="relative">
          <Replace className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zinc-400 dark:text-slate-500" />
          <input
            type="text"
            value={replaceText}
            onChange={(e) => setReplaceText(e.target.value)}
            placeholder="替换为..."
            className="w-full pl-8 pr-3 py-2 text-sm border border-zinc-200 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-zinc-800 dark:text-slate-200 placeholder-zinc-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500"
          />
        </div>

        {/* 搜索选项 */}
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-1.5 cursor-pointer">
            <input
              type="checkbox"
              checked={caseSensitive}
              onChange={(e) => setCaseSensitive(e.target.checked)}
              className="w-3.5 h-3.5 rounded border-zinc-300 dark:border-slate-600 text-blue-500 focus:ring-blue-500/50"
            />
            <span className="text-[11px] text-zinc-600 dark:text-slate-400 flex items-center gap-0.5">
              <CaseSensitive className="w-3 h-3" />
              大小写
            </span>
          </label>
          <label className="flex items-center gap-1.5 cursor-pointer">
            <input
              type="checkbox"
              checked={wholeWord}
              onChange={(e) => setWholeWord(e.target.checked)}
              className="w-3.5 h-3.5 rounded border-zinc-300 dark:border-slate-600 text-blue-500 focus:ring-blue-500/50"
            />
            <span className="text-[11px] text-zinc-600 dark:text-slate-400 flex items-center gap-0.5">
              <WholeWord className="w-3 h-3" />
              全词
            </span>
          </label>
        </div>

        {/* 替换成功提示 */}
        {showReplaceSuccess && (
          <div className="flex items-center gap-1.5 px-2.5 py-1.5 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
            <svg className="w-3.5 h-3.5 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="text-[11px] text-green-700 dark:text-green-400">
              已替换 {replaceCount} 处
            </span>
          </div>
        )}

        {/* 操作按钮 */}
        <div className="flex items-center gap-2">
          <button
            onClick={replaceCurrent}
            disabled={matches.length === 0 || currentMatchIndex < 0}
            className="flex-1 px-3 py-1.5 text-xs bg-zinc-100 dark:bg-slate-700 text-zinc-700 dark:text-slate-300 rounded-lg hover:bg-zinc-200 dark:hover:bg-slate-600 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            替换
          </button>
          <button
            onClick={replaceAll}
            disabled={matches.length === 0}
            className="flex-1 px-3 py-1.5 text-xs bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            全部替换 {matches.length > 0 && `(${matches.length})`}
          </button>
        </div>
      </div>
    </div>
  );
};

export default FindReplaceDialog;
