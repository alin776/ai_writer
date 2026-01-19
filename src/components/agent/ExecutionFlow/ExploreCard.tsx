/**
 * ExploreCard - Explore 轨迹聚合展示
 * 按轮次聚合 search/locate/read 结果
 * v10.2: 优化深色模式为深蓝色调（slate 系列）
 *
 * 设计规范：
 * - 响应式主题：使用 Tailwind dark: 前缀
 * - 浅色模式：白色背景，灰色边框和文本
 * - 深色模式：深蓝灰色背景（slate-800/900），深蓝色边框（slate-700）
 * - 高亮色：蓝色 (#5c9eff)，成功色：绿色 (#10b981)，警告色：橙色 (#f59e0b)
 */

import { useState } from 'react';
import type { ComponentType } from 'react';
import { Check, Scan, Search, Crosshair, FileText, CheckCircle, AlertTriangle, Clock, Brain, ArrowRightCircle, FileSearch, BookOpen, Layers, ChevronUp, ChevronDown } from 'lucide-react';
import type { ExploreFlowData, ExploreRound, ExploreEvidenceItem, ExploreRoundFlowData, ExploreSummaryFlowData, ExploreToolCall } from '@/types/agent';

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
    return { label: '通过', icon: CheckCircle, tone: 'text-[#10b981]' };
  }
  if (status === 'insufficient') {
    return { label: '覆盖不足', icon: AlertTriangle, tone: 'text-[#f59e0b]' };
  }
  return { label: '待评', icon: Clock, tone: 'text-[#888]' };
};

const renderEvidenceMeta = (item: ExploreEvidenceItem) => {
  const chapter = item.chapterOrder !== undefined && item.chapterOrder !== null
    ? `第${item.chapterOrder}章`
    : item.chapterTitle || (item.chapter ? `第${item.chapter}章` : '');
  const paragraph = renderParagraphLabel(item.paragraphIndex ?? item.paragraph);
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
          <Check size={12} className="text-gray-500 dark:text-slate-400" />
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-[14px] font-medium text-gray-900 dark:text-white">
            Explore 轨迹（{safeRounds.length}轮）
          </span>
          <span className="text-gray-400 dark:text-slate-600 flex items-center">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>
        <div className="flex-1" />
      </div>

      {expanded && (
        <div className="ml-[26px] pt-1">
          {/* explore-panel 容器 */}
          <div className="my-2">
            {safeRounds.map((round, index) => (
              <LegacyRoundCard key={round.id} round={round} index={index} />
            ))}
          </div>
          <div className="text-[13px] text-gray-500 dark:text-slate-300 leading-[1.6] my-2">
            多轮检索-定位-原文读取，逐轮 review 覆盖度，补漏后输出完整证据链。
          </div>
        </div>
      )}
    </div>
  );
}

// 旧版 ExploreRound 组件（聚合数据）- 适配浅色/深色主题
function LegacyRoundCard({ round, index }: { round: ExploreRound; index: number }) {
  const [expanded, setExpanded] = useState(false);
  const [evidenceExpanded, setEvidenceExpanded] = useState(false);
  const review = renderReview(round);
  const hitCount = round.evidence?.length || round.search?.results?.length || 0;
  const chapterLabel = renderChapterLabel(round);
  const paragraphLabel = renderParagraphLabel(round.locate?.paragraphIndex ?? round.readSegment?.paragraphIndex);

  return (
    <div className="flex gap-[10px] py-2 items-start">
      {/* 胶囊容器 - 适配浅色/深色主题 */}
      <div
        className={`
          bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] self-start max-w-full
          ${expanded
            ? 'inline-flex flex-col px-[10px] py-[6px]'
            : 'inline-flex flex-row items-center gap-2 px-[10px] py-1'
          }
        `}
      >
        {/* Header */}
        <div
          className="flex items-center gap-2 cursor-pointer select-none"
          onClick={() => setExpanded(!expanded)}
        >
          <div className="text-gray-500 dark:text-slate-400 flex items-center justify-center text-[12px] font-medium">
            <Scan size={12} />
          </div>
          <div className={`flex items-center gap-2 text-[13px] text-gray-600 dark:text-slate-400 ${expanded ? 'mb-0' : 'text-[12px]'}`}>
            {buildRoundTitle(round, index)}
          </div>
          <span className="text-gray-400 dark:text-slate-600 ml-auto flex items-center">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>

          {/* Body - 展开时显示 */}
          {expanded && (
            <div className="flex-1 w-fit max-w-full mt-2">
              {/* 工具标签 */}
              <div className="flex flex-wrap gap-[6px] w-fit max-w-full">
                {round.search?.query && (
                  <span className="inline-flex items-center gap-1 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] px-[10px] py-1 text-[12px] text-gray-600 dark:text-slate-400">
                    <Search size={12} className="text-gray-500 dark:text-slate-400" />
                    Search: <span className="text-gray-700 dark:text-slate-400 font-medium truncate max-w-[220px] inline-block">{round.search.query}</span>
                  </span>
                )}
                {chapterLabel && (
                  <span className="inline-flex items-center gap-1 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] px-[10px] py-1 text-[12px] text-gray-600 dark:text-slate-400">
                    <Crosshair size={12} className="text-gray-500 dark:text-slate-400" />
                    Locate: <span className="text-gray-700 dark:text-slate-400">{chapterLabel}{paragraphLabel ? ` · ${paragraphLabel}` : ''}</span>
                  </span>
                )}
                {(round.readRaw?.chapterOrder !== undefined || round.readRaw?.chapterTitle) && (
                  <span className="inline-flex items-center gap-1 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] px-[10px] py-1 text-[12px] text-gray-600 dark:text-slate-400">
                    <FileText size={12} className="text-gray-500 dark:text-slate-400" />
                    ReadRaw: <span className="text-gray-700 dark:text-slate-400">
                      {round.readRaw?.chapterOrder !== undefined
                        ? `第${round.readRaw.chapterOrder}章`
                        : round.readRaw?.chapterTitle}
                    </span>
                  </span>
                )}
                <span className="inline-flex items-center gap-1 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] px-[10px] py-1 text-[12px] text-gray-600 dark:text-slate-400">
                  <review.icon size={12} className={review.tone} />
                  Review: <span className="text-gray-700 dark:text-slate-400">{review.label}</span>
                </span>
              </div>

              {/* 状态信息 */}
              {hitCount > 0 && (
                <div className="flex flex-wrap gap-[10px] mt-[6px] text-[11px] text-gray-500 dark:text-slate-500 w-fit max-w-full">
                  <span className="text-[#10b981]">命中 {hitCount} 条</span>
                </div>
              )}

              {/* 证据片段 */}
              {round.evidence && round.evidence.length > 0 && (
                <div className="bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] px-[10px] py-1 mt-[6px] text-[12px] text-gray-600 dark:text-slate-400 w-fit max-w-full">
                  <div
                    className="flex items-center gap-[6px] cursor-pointer select-none"
                    onClick={(e) => {
                      e.stopPropagation();
                      setEvidenceExpanded(!evidenceExpanded);
                    }}
                  >
                    <span className="text-[11px] text-gray-600 dark:text-slate-400">证据片段（{round.evidence.length}）</span>
                    <span className="text-gray-400 dark:text-slate-600 flex items-center">
                      {evidenceExpanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
                    </span>
                  </div>
                  {evidenceExpanded && (
                    <div className="pt-1">
                      {round.evidence.map((item, idx) => (
                        <div
                          key={`${round.id}-evidence-${idx}`}
                          className={`py-[2px] ${idx > 0 ? 'border-t border-dashed border-gray-200 dark:border-slate-700' : ''}`}
                        >
                          <div className="text-[10px] text-gray-500 dark:text-slate-500">
                            {renderEvidenceMeta(item)}
                          </div>
                          <div className="text-[12px] text-gray-700 dark:text-slate-400">{item.text}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
      </div>
    </div>
  );
}

// ==================== 流事件组件 (v9.0) ====================

// 工具类型图标映射
const TOOL_ICONS: Record<string, ComponentType<any>> = {
  Search: Search,
  Locate: Crosshair,
  ReadRaw: FileText,
  Review: CheckCircle,
};

// 解析 review 状态
const parseReviewStatus = (status: string) => {
  if (status === '通过' || status === 'pass') {
    return { label: '通过', icon: CheckCircle, tone: 'text-[#10b981]' };
  }
  if (status === '覆盖不足' || status === 'insufficient') {
    return { label: '覆盖不足', icon: AlertTriangle, tone: 'text-[#f59e0b]' };
  }
  if (status === '补齐要点') {
    return { label: '补齐要点', icon: CheckCircle, tone: 'text-[#5c9eff]' };
  }
  return { label: status || '待评', icon: Clock, tone: 'text-[#888]' };
};

// 工具标签组件 - 适配浅色/深色主题
function ExploreTag({ toolCall }: { toolCall: ExploreToolCall }) {
  const IconComponent = TOOL_ICONS[toolCall.type] || Search;
  const isSearchType = toolCall.type === 'Search';

  return (
    <span className="inline-flex items-center gap-1 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] px-[10px] py-1 text-[12px] text-gray-600 dark:text-slate-400">
      <IconComponent size={12} className="text-gray-500 dark:text-slate-400" />
      {toolCall.type}:{' '}
      <span className={isSearchType ? 'text-gray-700 dark:text-slate-400 font-medium' : 'text-gray-700 dark:text-slate-400'}>
        {toolCall.highlight || toolCall.value}
      </span>
    </span>
  );
}

/**
 * ExploreRoundCard - 流事件轮次组件
 * 适配浅色/深色主题
 */
export function ExploreRoundCard({
  roundIdx,
  title,
  reason,  // AI 生成的决策理由（完整）
  toolCalls,
  hitCount,
  missingItems,
  statusText,
  evidences,
  reviewStatus,
  status,
}: ExploreRoundFlowData) {
  const [expanded, setExpanded] = useState(false);
  const [evidenceExpanded, setEvidenceExpanded] = useState(false);
  const review = parseReviewStatus(reviewStatus);
  const isRunning = status === 'running';
  const hasReviewTag = (toolCalls || []).some((tc) => tc.type === 'Review');

  return (
    <div className="flex flex-col gap-2 py-2">
      {/* AI 决策理由（独立显示，在胶囊框上方） */}
      {reason && (
        <div className="text-[13px] text-gray-600 dark:text-slate-400 leading-relaxed">
          {reason}
        </div>
      )}

      {/* 胶囊容器 - 适配浅色/深色主题 */}
      <div
        className={`
          bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] self-start max-w-full
          ${expanded
            ? 'inline-flex flex-col px-[10px] py-[6px]'
            : 'inline-flex flex-row items-center gap-2 px-[10px] py-1'
          }
          ${isRunning ? 'animate-pulse' : ''}
        `}
      >
        {/* Header */}
        <div
          className={`flex items-center gap-2 cursor-pointer select-none ${expanded ? '' : ''}`}
          onClick={() => setExpanded(!expanded)}
        >
          {/* 轮次图标 */}
          <div className="text-gray-500 dark:text-slate-400 flex items-center justify-center text-[12px] font-medium">
            <Scan size={12} />
          </div>
          {/* 轮次标题 */}
          <div className={`flex items-center gap-2 text-[13px] text-gray-600 dark:text-slate-400 ${expanded ? 'mb-0' : 'text-[12px]'}`}>
            {title || `深度探索（第${roundIdx}轮）`}
          </div>
          {/* 展开/折叠按钮 */}
          <span className="text-gray-400 dark:text-slate-600 ml-auto flex items-center">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>

          {/* Body - 展开时显示 */}
          {expanded && (
            <div className="flex-1 w-fit max-w-full mt-2">
              {/* 工具标签 - 适配浅色/深色主题 */}
              <div className="flex flex-wrap gap-[6px] w-fit max-w-full">
                {toolCalls?.map((tc, idx) => (
                  <ExploreTag key={idx} toolCall={tc} />
                ))}
                {reviewStatus && !hasReviewTag && (
                  <span className="inline-flex items-center gap-1 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] px-[10px] py-1 text-[12px] text-gray-600 dark:text-slate-400">
                    <review.icon size={12} className={review.tone} />
                    Review: <span className="text-gray-700 dark:text-slate-400">{review.label}</span>
                  </span>
                )}
              </div>

              {/* 状态信息 - 适配浅色/深色主题 */}
              <div className="flex flex-wrap gap-[10px] mt-[6px] text-[11px] text-gray-500 dark:text-slate-500 w-fit max-w-full">
                {hitCount > 0 && (
                  <span className="text-[#10b981]">命中 {hitCount} 条</span>
                )}
                {missingItems && missingItems.length > 0 ? (
                  <span className="text-[#f59e0b]">缺少：{missingItems.join('、')}</span>
                ) : statusText ? (
                  <span>{statusText}</span>
                ) : null}
              </div>

              {/* 证据片段 - 适配浅色/深色主题 */}
              {evidences && evidences.length > 0 && (
                <div className="bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] px-[10px] py-1 mt-[6px] text-[12px] text-gray-600 dark:text-slate-400 w-fit max-w-full">
                  <div
                    className="flex items-center gap-[6px] cursor-pointer select-none"
                    onClick={(e) => {
                      e.stopPropagation();
                      setEvidenceExpanded(!evidenceExpanded);
                    }}
                  >
                    <span className="text-[11px] text-gray-600 dark:text-slate-400">证据片段（{evidences.length}）</span>
                    <span className="text-gray-400 dark:text-slate-600 flex items-center">
                      {evidenceExpanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
                    </span>
                  </div>
                  {evidenceExpanded && (
                    <div className="pt-1">
                      {evidences.map((item, idx) => (
                        <div
                          key={`evidence-${idx}`}
                          className={`py-[2px] ${idx > 0 ? 'border-t border-dashed border-gray-200 dark:border-slate-700' : ''}`}
                        >
                          <div className="text-[10px] text-gray-500 dark:text-slate-500">
                            {renderEvidenceMeta(item)}
                          </div>
                          <div className="text-[12px] text-gray-700 dark:text-slate-400">{item.text}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
      </div>
    </div>
  );
}

/**
 * ExploreSummaryCard - 流事件总结组件
 * 适配浅色/深色主题
 */
export function ExploreSummaryCard({
  totalRounds,
  summary,
  nextAction,
  nextTool,
  sufficient,
  coverage,
  stats,
}: ExploreSummaryFlowData) {
  const [expanded, setExpanded] = useState(true);
  const isSufficient = sufficient === true;
  const isInsufficient = sufficient === false;
  const CoverageIcon = isInsufficient ? AlertTriangle : isSufficient ? CheckCircle : Clock;
  const coverageTone = isInsufficient
    ? 'text-[#f59e0b]'
    : isSufficient
      ? 'text-[#10b981]'
      : 'text-gray-500 dark:text-slate-400';

  return (
    <div className="mt-3 mb-3">
      {/* 卡片容器 - 适配浅色/深色主题 */}
      <div className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] px-[10px] py-1 inline-block max-w-full">
        {/* Header */}
        <div
          className="flex items-center gap-2 cursor-pointer select-none"
          onClick={() => setExpanded(!expanded)}
          style={{ marginBottom: expanded ? '10px' : '0' }}
        >
          <span className="text-gray-500 dark:text-slate-400 flex items-center">
            <Brain size={12} />
          </span>
          <span
            className="text-[13px] font-medium text-gray-900 dark:text-white"
            style={{ fontWeight: expanded ? 500 : 'normal' }}
          >
            AI 分析与规划
          </span>
          <span className="text-gray-400 dark:text-slate-600 ml-auto flex items-center">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>

        {/* Content */}
        {expanded && (
          <div>
            {/* 探索总结 */}
            {summary && (
              <div className="mb-[10px]">
                <div className="flex items-center gap-[6px] mb-1">
                  <span className="text-gray-500 dark:text-slate-400 flex items-center">
                    <FileSearch size={12} />
                  </span>
                  <span className="text-[12px] text-gray-600 dark:text-slate-400 font-medium">探索总结</span>
                </div>
                <div className="text-[12px] text-gray-600 dark:text-slate-300 leading-[1.7] pl-[18px]">
                  {summary}
                </div>
              </div>
            )}

            {/* 覆盖度说明 */}
            {coverage && (
              <div className="mb-[10px]">
                <div className="flex items-center gap-[6px] mb-1">
                  <span className="text-gray-500 dark:text-slate-400 flex items-center">
                    <Brain size={12} />
                  </span>
                  <span className="text-[12px] text-gray-600 dark:text-slate-400 font-medium">覆盖度说明</span>
                </div>
                <div className="text-[12px] text-gray-600 dark:text-slate-300 leading-[1.7] pl-[18px]">
                  {coverage}
                </div>
              </div>
            )}

            {/* 下一步行动 */}
            {nextAction && (
              <div className="mb-[10px]">
                <div className="flex items-center gap-[6px] mb-1">
                  <span className="text-gray-500 dark:text-slate-400 flex items-center">
                    <ArrowRightCircle size={12} />
                  </span>
                  <span className="text-[12px] text-gray-600 dark:text-slate-400 font-medium">下一步行动</span>
                </div>
                <div className="text-[12px] text-gray-600 dark:text-slate-300 leading-[1.7] pl-[18px]">
                  {nextAction}
                  {nextTool && (
                    <span className="ml-1 text-[#5c9eff] dark:text-[#7db3ff] font-mono text-[11px]">{nextTool}</span>
                  )}
                </div>
              </div>
            )}

          </div>
        )}
      </div>
    </div>
  );
}
