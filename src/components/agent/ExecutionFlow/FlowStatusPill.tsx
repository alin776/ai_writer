/**
 * FlowStatusPill - 轻量胶囊状态展示
 */

import type { ReactNode } from 'react';

type Tone = 'info' | 'warn' | 'success' | 'error';

interface FlowStatusPillProps {
  label: string;
  badge?: string;
  details?: string[];
  tone?: Tone;
  icon?: ReactNode;
}

const toneStyles: Record<Tone, { text: string; badge: string; dot: string }> = {
  info: {
    text: 'text-gray-600 dark:text-slate-400',
    badge: 'bg-gray-100 text-gray-600 dark:bg-slate-700 dark:text-slate-300',
    dot: 'bg-blue-500'
  },
  warn: {
    text: 'text-gray-600 dark:text-slate-400',
    badge: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-200',
    dot: 'bg-amber-500'
  },
  success: {
    text: 'text-gray-600 dark:text-slate-400',
    badge: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-200',
    dot: 'bg-emerald-500'
  },
  error: {
    text: 'text-gray-600 dark:text-slate-400',
    badge: 'bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-200',
    dot: 'bg-rose-500'
  }
};

export function FlowStatusPill({
  label,
  badge,
  details = [],
  tone = 'info',
  icon
}: FlowStatusPillProps) {
  const styles = toneStyles[tone];
  const compactDetails = details.filter((item) => item && item.trim());

  return (
    <div className="mb-2">
      <div
        className="inline-flex items-center gap-2 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] px-[10px] py-1 text-[12px]"
      >
        {icon && (
          <span className={styles.text}>{icon}</span>
        )}
        <span className={`text-[12px] font-medium ${styles.text}`}>{label}</span>
        {badge && (
          <span className={`ml-1 text-[10px] px-1.5 py-0.5 rounded-full ${styles.badge}`}>
            {badge}
          </span>
        )}
      </div>
      {compactDetails.length > 0 && (
        <div className="mt-1 ml-1 text-[12px] text-gray-500 dark:text-slate-400 leading-[1.6] space-y-1">
          {compactDetails.map((line, index) => (
            <div key={`${label}-${index}`}>{line}</div>
          ))}
        </div>
      )}
    </div>
  );
}
