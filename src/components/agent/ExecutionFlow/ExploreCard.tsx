/**
 * ExploreCard - Explore 轨迹聚合展示
 * 按轮次聚合 search/locate/read 结果
 */

import { useState } from 'react';
import type { ComponentType } from 'react';
import { Check, ChevronUp, ChevronDown, Scan, Search, Crosshair, FileText, CheckCircle, AlertTriangle, Clock } from 'lucide-react';
import type { ExploreFlowData, ExploreRound, ExploreEvidenceItem } from '@/types/agent';

interface ExploreCardProps extends ExploreFlowData {
  defaultExpanded?: boolean;
}

const renderChapterLabel = (round: ExploreRound) => {
  const order = round.locate?.chapterOrder ?? round.readRaw?.chapterOrder ?? round.readSegment?.chapterOrder;
  const title = round.locate?.chapterTitle ?? round.readRaw?.chapterTitle ?? round.readSegment?.chapterTitle;
  if (order !== undefined && order !== null) {
    return `第${order}章`;
  }
  return title || '';
};

const renderParagraphLabel = (paragraphIndex?: number) => {
  if (paragraphIndex === undefined || paragraphIndex === null) {
    return '';
  }
  return `第${paragraphIndex + 1}段`;
};

const renderReview = (round: ExploreRound) => {
  const status = round.review?.status || 'pending';
  if (status === 'pass') {
    return { label: '通过', icon: CheckCircle, tone: 'text-emerald-500 dark:text-emerald-400' };
  }
  if (status === 'insufficient') {
    return { label: '覆盖不足', icon: AlertTriangle, tone: 'text-amber-500 dark:text-amber-400' };
  }
  return { label: '待评', icon: Clock, tone: 'text-gray-400 dark:text-slate-500' };
};

const renderEvidenceMeta = (item: ExploreEvidenceItem) => {
  const chapter = item.chapterOrder !== undefined && item.chapterOrder !== null
    ? `第${item.chapterOrder}章`
    : item.chapterTitle || '';
  const paragraph = renderParagraphLabel(item.paragraphIndex);
  if (chapter && paragraph) {
    return `${chapter} · ${paragraph}`;
  }
  return chapter || paragraph || '';
};

const buildRoundTitle = (round: ExploreRound, index: number) => {
  if (round.title) {
    return round.title;
  }
  if (round.query) {
    return `探索：${round.query}`;
  }
  return `探索轮次 ${index + 1}`;
};

export function ExploreCard({ rounds, defaultExpanded = true }: ExploreCardProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const safeRounds = rounds || [];

  if (safeRounds.length === 0) {
    return null;
  }

  return (
    <div className="mb-3">
      <div
        className="flex items-center gap-2 py-1.5 cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="w-[18px] h-[18px] flex items-center justify-center">
          <Check size={12} className="text-gray-500" />
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-[14px] font-medium text-gray-900 dark:text-white">
            Explore 轨迹（{safeRounds.length}轮）
          </span>
          <span className="text-gray-400 dark:text-gray-600 text-[10px]">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>
        <div className="flex-1" />
      </div>

      {expanded && (
        <div className="ml-[26px] pt-1 space-y-2">
          <div className="text-[13px] text-gray-500 dark:text-[#999] leading-[1.6]">
            多轮检索-定位-原文读取，逐轮 review 覆盖度，补漏后输出完整证据链。
          </div>
          {safeRounds.map((round, index) => (
            <ExploreRoundCard key={round.id} round={round} index={index} />
          ))}
        </div>
      )}
    </div>
  );
}

function ExploreRoundCard({ round, index }: { round: ExploreRound; index: number }) {
  const [expanded, setExpanded] = useState(false);
  const [evidenceExpanded, setEvidenceExpanded] = useState(false);
  const review = renderReview(round);
  const hitCount = round.evidence?.length || round.search?.results?.length || 0;
  const chapterLabel = renderChapterLabel(round);
  const paragraphLabel = renderParagraphLabel(round.locate?.paragraphIndex ?? round.readSegment?.paragraphIndex);

  return (
    <div>
      <div
        className="inline-flex items-center gap-2 px-3 py-1.5 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-full cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        <span className="text-gray-500">
          <Scan size={12} />
        </span>
        <span className="text-[13px] text-gray-700 dark:text-slate-300">
          {buildRoundTitle(round, index)}
        </span>
        <span className="text-gray-400 dark:text-gray-600 text-[9px]">
          {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
        </span>
      </div>

      {expanded && (
        <div className="mt-2 ml-6 space-y-2">
          <div className="flex flex-wrap gap-2">
            {round.search?.query && (
              <Tag icon={Search} label="Search" tone="text-blue-500 dark:text-blue-400">
                <span className="font-medium text-gray-600 dark:text-slate-300 truncate max-w-[220px] inline-block">
                  {round.search.query}
                </span>
              </Tag>
            )}
            {chapterLabel && (
              <Tag icon={Crosshair} label="Locate" tone="text-gray-500">
                <span className="text-gray-600 dark:text-slate-300">
                  {chapterLabel}{paragraphLabel ? ` · ${paragraphLabel}` : ''}
                </span>
              </Tag>
            )}
            {(round.readRaw?.chapterOrder || round.readRaw?.chapterTitle) && (
              <Tag icon={FileText} label="ReadRaw" tone="text-gray-500">
                <span className="text-gray-600 dark:text-slate-300">
                  {round.readRaw?.chapterOrder !== undefined && round.readRaw?.chapterOrder !== null
                    ? `第${round.readRaw.chapterOrder}章`
                    : round.readRaw?.chapterTitle}
                </span>
              </Tag>
            )}
            <Tag icon={review.icon} label="Review" tone={review.tone}>
              <span className="text-gray-600 dark:text-slate-300">{review.label}</span>
            </Tag>
          </div>

          {hitCount > 0 && (
            <div className="text-[12px] text-gray-500 dark:text-slate-400">
              命中 {hitCount} 条
            </div>
          )}

          {round.evidence && round.evidence.length > 0 && (
            <div>
              <div
                className={`inline-flex items-center gap-1.5 px-2.5 py-1 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 cursor-pointer select-none ${
                  evidenceExpanded ? 'rounded-xl' : 'rounded-full'
                }`}
                onClick={() => setEvidenceExpanded(!evidenceExpanded)}
              >
                <span className="text-[12px] text-gray-500">证据片段（{round.evidence.length}）</span>
                <span className="text-gray-400 dark:text-gray-600 text-[9px]">
                  {evidenceExpanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
                </span>
              </div>
              {evidenceExpanded && (
                <div className="mt-2 space-y-2">
                  {round.evidence.map((item, idx) => (
                    <div
                      key={`${round.id}-evidence-${idx}`}
                      className="rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-[13px] text-gray-600 dark:text-slate-300"
                    >
                      <div className="text-[11px] text-gray-400 dark:text-slate-500 mb-1">
                        {renderEvidenceMeta(item)}
                      </div>
                      {item.text}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function Tag({
  icon: Icon,
  label,
  tone,
  children,
}: {
  icon: ComponentType<any>;
  label: string;
  tone?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-full">
      <span className={tone || 'text-gray-500'}>
        <Icon size={12} />
      </span>
      <span className="text-[12px] text-gray-500">{label}:</span>
      {children}
    </div>
  );
}
