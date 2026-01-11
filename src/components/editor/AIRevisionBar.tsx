/**
 * AIRevisionBar - AI修订操作栏组件
 * 显示在修订内容旁边，提供两个操作：弃用、采纳
 */

import React, { useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';

export interface RevisionData {
  id: string;
  type: 'modify' | 'continue' | 'insert';
  position: { from: number; to: number };
  original?: string;
  replacement: string;
  originalMessage?: string;  // 原始用户指令，用于重新生成
  context?: any;             // 原始上下文
}

interface AIRevisionBarProps {
  revision: RevisionData;
  position: { top: number; left: number } | null;
  onRegenerate?: () => void;  // 保留接口但设为可选
  onDiscard: () => void;
  onAccept: () => void;
  isLoading?: boolean;
}

const AIRevisionBar: React.FC<AIRevisionBarProps> = ({
  revision,
  position,
  onDiscard,
  onAccept,
  isLoading = false
}) => {
  const { t } = useTranslation();
  const barRef = useRef<HTMLDivElement>(null);

  // 确保操作栏不超出视口
  useEffect(() => {
    if (!barRef.current || !position) return;

    const bar = barRef.current;
    const rect = bar.getBoundingClientRect();
    const maxRight = window.innerWidth - 20;
    const maxBottom = window.innerHeight - 20;

    if (rect.right > maxRight) {
      bar.style.left = `${position.left - (rect.right - maxRight)}px`;
    }
    if (rect.bottom > maxBottom) {
      bar.style.top = `${position.top - rect.height - 10}px`;
    }
  }, [position]);

  if (!position) return null;

  return (
    <div
      ref={barRef}
      className="flex items-center gap-1.5 px-2 py-1.5 bg-white dark:bg-slate-800 border border-zinc-200 dark:border-slate-600 rounded-lg shadow-lg animate-in fade-in slide-in-from-top-1 duration-200"
      style={{
        position: 'fixed',
        top: position.top,
        left: position.left,
        zIndex: 1000
      }}
    >
      {/* 弃用按钮 */}
      <button
        onClick={onDiscard}
        disabled={isLoading}
        className="flex items-center gap-1 px-2.5 py-1 text-[11px] font-medium bg-zinc-100 hover:bg-zinc-200 text-zinc-600 dark:bg-slate-700 dark:hover:bg-slate-600 dark:text-slate-300 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        title={t('editor.aiRevision.discardChange')}
      >
        <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
        <span>{t('editor.aiRevision.discard')}</span>
      </button>

      {/* 采纳按钮 */}
      <button
        onClick={onAccept}
        disabled={isLoading}
        className="flex items-center gap-1 px-2.5 py-1 text-[11px] font-medium bg-green-600 hover:bg-green-700 text-white rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        title={t('editor.aiRevision.acceptChange')}
      >
        <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        </svg>
        <span>{t('editor.aiRevision.accept')}</span>
      </button>
    </div>
  );
};

export default AIRevisionBar;
