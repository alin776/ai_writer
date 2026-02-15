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
import { replaceAll } from '@milkdown/utils';
import '@milkdown/crepe/theme/common/style.css';
import '@milkdown/crepe/theme/frame.css';

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

  return (
    <div className="flex flex-col h-full">
      {/* 编辑器主体 */}
      <div
        ref={containerRef}
        className="flex-1 overflow-y-auto"
      />
      {/* 底部状态栏 */}
      <div className="flex items-center justify-between px-4 py-1.5 text-[11px] text-zinc-400 dark:text-slate-500 border-t border-zinc-100 dark:border-slate-700 flex-shrink-0">
        <span>{wordCount} 字</span>
        <span>Markdown</span>
      </div>
    </div>
  );
};

export default MilkdownEditor;
