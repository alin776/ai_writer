/**
 * MilkdownEditor — 基于 Milkdown 的 Markdown 编辑器
 *
 * 数据流：md string in → Milkdown 渲染 → md string out（零转换）
 *
 * 核心 props：
 *   content     - Markdown 字符串
 *   onSave      - 保存回调 (md: string) => void
 *   autoSaveInterval - 自动保存间隔 ms（默认 3000）
 *   readOnly    - 是否只读
 *   placeholder - 占位文本
 */
import React, { useEffect, useRef, useCallback, useState } from 'react';
import { Crepe } from '@milkdown/crepe';
import { editorViewCtx } from '@milkdown/core';
import { replaceAll } from '@milkdown/utils';
import { EditorState } from '@milkdown/prose/state';
import '@milkdown/crepe/theme/common/style.css';
import '@milkdown/crepe/theme/frame.css';
import { diffPluginKey, createDiffDecorationPlugin } from './diffDecorationPlugin';

interface MilkdownEditorProps {
  content: string;
  onSave?: (md: string) => void;
  autoSaveInterval?: number;
  readOnly?: boolean;
  placeholder?: string;
  storageKey?: string;
}

const MilkdownEditor: React.FC<MilkdownEditorProps> = ({
  content,
  onSave,
  autoSaveInterval = 3000,
  readOnly = false,
  placeholder = '开始写作...',
  storageKey = 'default',
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const crepeRef = useRef<Crepe | null>(null);
  const lastSavedRef = useRef<string>(content);
  const syncedContentRef = useRef<string>(content);
  const pendingContentRef = useRef<string | null>(null);
  const autoSaveTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const destroyedRef = useRef(false);
  const [wordCount, setWordCount] = useState(0);

  // 获取编辑器当前内容
  const getMarkdown = useCallback((): string => {
    if (!crepeRef.current) return '';
    try {
      return crepeRef.current.getMarkdown();
    } catch {
      return '';
    }
  }, []);

  // 自动保存逻辑
  const scheduleSave = useCallback(() => {
    if (!onSave) return;
    if (autoSaveTimerRef.current) {
      clearTimeout(autoSaveTimerRef.current);
    }
    autoSaveTimerRef.current = setTimeout(() => {
      const md = getMarkdown();
      if (md !== lastSavedRef.current) {
        lastSavedRef.current = md;
        onSave(md);
      }
    }, autoSaveInterval);
  }, [onSave, autoSaveInterval, getMarkdown]);

  // 计算字数
  const updateWordCount = useCallback((md: string) => {
    const text = md.replace(/[#*`>\-\[\]()!|_~]/g, '').trim();
    setWordCount(text.length);
  }, []);

  // localStorage 备份（按 storageKey 隔离，避免跨章节覆盖）
  const backupToStorage = useCallback((md: string) => {
    try {
      localStorage.setItem(`milkdown-backup-${storageKey}`, md);
    } catch {
      // ignore
    }
  }, [storageKey]);

  // 初始化 Milkdown
  useEffect(() => {
    if (!containerRef.current) return;
    destroyedRef.current = false;

    const crepe = new Crepe({
      root: containerRef.current,
      defaultValue: content,
      features: {
        [Crepe.Feature.LinkTooltip]: true,
        [Crepe.Feature.ImageBlock]: true,
        [Crepe.Feature.BlockEdit]: false,
        [Crepe.Feature.Placeholder]: true,
        [Crepe.Feature.CodeMirror]: true,
        [Crepe.Feature.ListItem]: true,
        [Crepe.Feature.Table]: true,
        [Crepe.Feature.Toolbar]: !readOnly,
      },
      featureConfigs: {
        [Crepe.Feature.Placeholder]: {
          text: placeholder,
        },
        [Crepe.Feature.Toolbar]: {
          buildToolbar: (builder: any) => {
            builder.addGroup('ai-quote', '引用到AI').addItem('quote-to-ai', {
              icon: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 10h.01"/><path d="M12 10h.01"/><path d="M16 10h.01"/></svg>',
              active: () => false,
              onRun: (ctx: any) => {
                try {
                  const view = ctx.get(editorViewCtx);
                  const { state } = view;
                  const { from, to } = state.selection;
                  if (from === to) return; // 没有选中文本则不操作
                  const selectedText = state.doc.textBetween(from, to, '\n');
                  if (!selectedText.trim()) return;

                  // 派发 inline-ai-intent 事件（AIPanel 已有监听）
                  window.dispatchEvent(new CustomEvent('inline-ai-intent', {
                    detail: {
                      selected_text: selectedText,
                      selected_text_html: selectedText,
                      selection_position: { from, to },
                    },
                  }));
                  // 派发 focus-ai-input 事件，让 AIPanel 输入框聚焦
                  window.dispatchEvent(new CustomEvent('focus-ai-input'));
                } catch {
                  // ignore
                }
              },
            });
          },
        },
      },
    });

    crepe.setReadonly(readOnly);

    // 监听编辑器变化
    crepe.on((listener: any) => {
      listener.markdownUpdated((_ctx: any, md: string) => {
        updateWordCount(md);
        backupToStorage(md);
        scheduleSave();
      });
    });

    crepe.create().then(() => {
      if (destroyedRef.current) return; // 组件已卸载，不再操作
      crepeRef.current = crepe;

      // 注册内联 Diff 装饰插件
      try {
        crepe.editor.action((ctx) => {
          const view = ctx.get(editorViewCtx);
          const state = view.state;
          const newState = EditorState.create({
            schema: state.schema,
            doc: state.doc,
            selection: state.selection,
            plugins: [...state.plugins, createDiffDecorationPlugin()],
          });
          view.updateState(newState);
        });
      } catch {
        // ignore — 插件注册失败不影响编辑器正常使用
      }
      // 如果在 Crepe 初始化期间有新的 content 到达，立即应用
      if (pendingContentRef.current !== null) {
        const pending = pendingContentRef.current;
        pendingContentRef.current = null;
        try {
          crepe.editor.action(replaceAll(pending));
          syncedContentRef.current = pending;
          lastSavedRef.current = pending;
          updateWordCount(pending);
        } catch {
          // ignore
        }
      } else {
        updateWordCount(content);
      }
    });

    return () => {
      destroyedRef.current = true;
      if (autoSaveTimerRef.current) {
        clearTimeout(autoSaveTimerRef.current);
      }
      // 卸载前保存
      if (crepeRef.current && onSave) {
        const md = getMarkdown();
        if (md && md !== lastSavedRef.current) {
          onSave(md);
        }
      }
      crepe.destroy();
      crepeRef.current = null;
    };
  }, []); // 只在挂载时执行一次

  // 当外部 content prop 变化时（如异步加载完成），同步到编辑器
  useEffect(() => {
    if (content === syncedContentRef.current) return;
    // Crepe 尚未初始化完成，暂存内容，等 create() 完成后再应用
    if (!crepeRef.current) {
      pendingContentRef.current = content;
      return;
    }
    syncedContentRef.current = content;
    lastSavedRef.current = content;
    try {
      crepeRef.current.editor.action(replaceAll(content));
      updateWordCount(content);
    } catch {
      // editor not ready
      pendingContentRef.current = content;
    }
  }, [content, updateWordCount]);

  // 监听内联 Diff 事件
  useEffect(() => {
    const handleInlineDiff = (e: Event) => {
      const { oldString, newString, append } = (e as CustomEvent).detail || {};
      // oldString 可以为空字符串（create 操作），只检查 newString 和编辑器实例
      if (newString == null || !crepeRef.current) return;
      try {
        crepeRef.current.editor.action((ctx) => {
          const view = ctx.get(editorViewCtx);
          const tr = view.state.tr.setMeta(diffPluginKey, { oldString: oldString ?? '', newString, append });
          view.dispatch(tr);
        });
      } catch {
        // ignore
      }
    };

    const handleClearDiff = () => {
      if (!crepeRef.current) return;
      try {
        crepeRef.current.editor.action((ctx) => {
          const view = ctx.get(editorViewCtx);
          const tr = view.state.tr.setMeta(diffPluginKey, { clear: true });
          view.dispatch(tr);
        });
      } catch {
        // ignore
      }
    };

    window.addEventListener('editor-inline-diff', handleInlineDiff);
    window.addEventListener('editor-hide-diff', handleClearDiff);
    return () => {
      window.removeEventListener('editor-inline-diff', handleInlineDiff);
      window.removeEventListener('editor-hide-diff', handleClearDiff);
    };
  }, []);

  return (
    <div className="flex flex-col h-full">
      {/* 编辑器主体 */}
      <div
        ref={containerRef}
        className="flex-1 overflow-y-auto overflow-x-hidden scrollbar-visible"
      />
    </div>
  );
};

export default MilkdownEditor;
