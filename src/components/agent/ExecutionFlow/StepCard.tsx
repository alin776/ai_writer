/**
 * StepCard - 鎵ц姝ラ鍗＄墖缁勪欢
 * 鍙姌鍙狅紝鏄剧ず鐘舵€佸浘鏍囥€佺煡璇嗚皟鍙栥€佸伐鍏疯皟鐢ㄣ€佸唴宓屼慨璁㈣兌鍥?
 */

import { useState, type ReactNode } from 'react';
import { Check, Loader2, ChevronUp, ChevronDown, Wrench } from 'lucide-react';
import type { StepFlowData } from '@/types/agent';
import { KnowledgeContainer } from './KnowledgeContainer';
import { RevisionCard } from './RevisionCard';

interface StepCardProps extends StepFlowData {
  defaultExpanded?: boolean;
  children?: ReactNode;
  revisionEventTimestamp?: string;
  onAcceptRevision?: (selectedVersion?: number) => void;
  onDiscardRevision?: () => void;
  onUndoRevision?: () => void;
  onRedoRevision?: () => void;
  onJumpRevision?: () => void;
}

export function StepCard({
  title,
  status,
  description,
  knowledge,
  toolCall,
  children,
  revision,
  revisionEventTimestamp,
  defaultExpanded = true,
  onAcceptRevision,
  onDiscardRevision,
  onUndoRevision,
  onRedoRevision,
  onJumpRevision
}: StepCardProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const showToolCall = toolCall && toolCall.name !== 'explore_content';

  return (
    <div className="mb-3">
      {/* 姝ラ澶撮儴 */}
      <div
        className="flex items-center gap-2 py-1.5 cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        {/* 鐘舵€佸浘鏍?*/}
        <div className="w-[18px] h-[18px] flex items-center justify-center">
          {status === 'running' ? (
            <Loader2 size={12} className="text-blue-500 animate-spin" />
          ) : status === 'done' ? (
            <Check size={12} className="text-gray-500" />
          ) : (
            <span className="w-2 h-2 rounded-full bg-red-500" />
          )}
        </div>

        {/* 鏍囬鍖哄煙 */}
        <div className="flex items-center gap-1.5">
          <span className="text-[14px] font-medium text-gray-900 dark:text-white">{title}</span>
          <span className="text-gray-400 dark:text-slate-600 text-[10px]">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>

        <div className="flex-1" />
      </div>

      {/* 姝ラ鍐呭 */}
      {expanded && (
        <div className="ml-[26px] pt-1">
          {/* 鐭ヨ瘑璋冨彇 */}
          {knowledge && knowledge.length > 0 && (
            <div className="mb-2">
              {knowledge.map((k, index) => (
                <KnowledgeContainer key={index} {...k} />
              ))}
            </div>
          )}

          {/* 姝ラ鎻忚堪 */}
          {description && (
            <div className="text-[13px] text-gray-500 dark:text-slate-300 my-2 leading-[1.6]">
              {description}
            </div>
          )}

          {/* 宸ュ叿璋冪敤鏍囩 */}
          {showToolCall && (
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-full my-2">
              <span className="text-gray-400 dark:text-slate-500">
                <Wrench size={12} />
              </span>
              <span className="text-[13px] text-gray-500 dark:text-slate-400">璋冪敤宸ュ叿</span>
              <span className="font-mono text-[12px] text-gray-600 dark:text-slate-300">
                {toolCall.name}
              </span>
            </div>
          )}

          {children && (
            <div className="mt-2">
              {children}
            </div>
          )}

          {/* v7.3: 鍐呭祵淇鑳跺泭 */}
          {revision && (
            <div className="mt-2">
              <RevisionCard
                {...revision}
                eventTimestamp={revisionEventTimestamp}
                onAccept={onAcceptRevision}
                onDiscard={onDiscardRevision}
                onUndo={onUndoRevision}
                onRedo={onRedoRevision}
                onJump={onJumpRevision}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

