/**
 * AIRevisionBar - AI修订操作栏组件
 * 显示在修订内容旁边，提供三个操作：重新生成、弃用、采纳
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
  onRegenerate: () => void;
  onDiscard: () => void;
  onAccept: () => void;
  isLoading?: boolean;
}

const AIRevisionBar: React.FC<AIRevisionBarProps> = ({
  revision,
  position,
  onRegenerate,
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
      className="ai-revision-bar"
      style={{
        position: 'fixed',
        top: position.top,
        left: position.left,
        zIndex: 1000
      }}
    >
      {/* 重新生成按钮 */}
      <button
        onClick={onRegenerate}
        disabled={isLoading}
        className="ai-revision-btn ai-revision-btn-refresh"
        title={t('editor.aiRevision.regenerate')}
      >
        {isLoading ? (
          <svg className="animate-spin w-3.5 h-3.5" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        ) : (
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        )}
        <span>{t('editor.aiRevision.refresh')}</span>
      </button>

      {/* 弃用按钮 */}
      <button
        onClick={onDiscard}
        disabled={isLoading}
        className="ai-revision-btn ai-revision-btn-discard"
        title={t('editor.aiRevision.discardChange')}
      >
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
        <span>{t('editor.aiRevision.discard')}</span>
      </button>

      {/* 采纳按钮 */}
      <button
        onClick={onAccept}
        disabled={isLoading}
        className="ai-revision-btn ai-revision-btn-accept"
        title={t('editor.aiRevision.acceptChange')}
      >
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        </svg>
        <span>{t('editor.aiRevision.accept')}</span>
      </button>
    </div>
  );
};

export default AIRevisionBar;
