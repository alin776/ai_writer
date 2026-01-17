/**
 * ExploreCard - Explore 轨迹聚合展示
 * 按轮次聚合 search/locate/read 结果
 * v10.0: 完全匹配 HTML 设计稿 (agent-writing-preview - 副本 (2).html)
 *
 * 设计规范参考：docs/explore/09-frontend-ui.md
 * - 胶囊背景：#2a2a2a，边框：#3a3a3a
 * - 圆角：16px
 * - 高亮色：#5c9eff，命中色：#10b981，警告色：#f59e0b
 */

import { useState } from 'react';
import type { ComponentType } from 'react';
import { Check, Scan, Search, Crosshair, FileText, CheckCircle, AlertTriangle, Clock, Brain, ArrowRightCircle, FileSearch, BookOpen, Layers } from 'lucide-react';
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
          <Check size={12} className="text-[#888]" />
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-[14px] font-medium text-white">
            Explore 轨迹（{safeRounds.length}轮）
          </span>
          <span className="text-[#666] text-[10px]">
            {expanded ? '∧' : '∨'}
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
          <div className="text-[13px] text-[#999] leading-[1.6] my-2">
            多轮检索-定位-原文读取，逐轮 review 覆盖度，补漏后输出完整证据链。
          </div>
        </div>
      )}
    </div>
  );
}

// 旧版 ExploreRound 组件（聚合数据）- 更新为匹配设计稿样式
function LegacyRoundCard({ round, index }: { round: ExploreRound; index: number }) {
  const [expanded, setExpanded] = useState(false);
  const [evidenceExpanded, setEvidenceExpanded] = useState(false);
  const review = renderReview(round);
  const hitCount = round.evidence?.length || round.search?.results?.length || 0;
  const chapterLabel = renderChapterLabel(round);
  const paragraphLabel = renderParagraphLabel(round.locate?.paragraphIndex ?? round.readSegment?.paragraphIndex);

  return (
    <div className="flex gap-[10px] py-2 items-start">
      {/* 胶囊容器 - 匹配设计稿的 .explore-round-capsule */}
      <div
        className={`
          bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] self-start max-w-full
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
          <div className="text-[#888] flex items-center justify-center text-[12px] font-medium">
            <Scan size={12} />
          </div>
          <div className={`flex items-center gap-2 text-[13px] text-[#888] ${expanded ? 'mb-0' : 'text-[12px]'}`}>
            {buildRoundTitle(round, index)}
          </div>
          {expanded && (
            <span className="text-[10px] text-[#666] ml-auto">∧</span>
          )}
        </div>

        {/* Body - 展开时显示 */}
        {expanded && (
          <div className="flex-1 w-fit max-w-full mt-2">
            {/* 工具标签 */}
            <div className="flex flex-wrap gap-[6px] w-fit max-w-full">
              {round.search?.query && (
                <span className="inline-flex items-center gap-1 bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] px-[10px] py-1 text-[12px] text-[#888]">
                  <Search size={12} className="text-[#888]" />
                  Search: <span className="text-[#5c9eff] font-medium truncate max-w-[220px] inline-block">{round.search.query}</span>
                </span>
              )}
              {chapterLabel && (
                <span className="inline-flex items-center gap-1 bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] px-[10px] py-1 text-[12px] text-[#888]">
                  <Crosshair size={12} className="text-[#888]" />
                  Locate: <span className="text-[#888]">{chapterLabel}{paragraphLabel ? ` · ${paragraphLabel}` : ''}</span>
                </span>
              )}
              {(round.readRaw?.chapterOrder !== undefined || round.readRaw?.chapterTitle) && (
                <span className="inline-flex items-center gap-1 bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] px-[10px] py-1 text-[12px] text-[#888]">
                  <FileText size={12} className="text-[#888]" />
                  ReadRaw: <span className="text-[#888]">
                    {round.readRaw?.chapterOrder !== undefined
                      ? `第${round.readRaw.chapterOrder}章`
                      : round.readRaw?.chapterTitle}
                  </span>
                </span>
              )}
              <span className="inline-flex items-center gap-1 bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] px-[10px] py-1 text-[12px] text-[#888]">
                <review.icon size={12} className={review.tone} />
                Review: <span className="text-[#888]">{review.label}</span>
              </span>
            </div>

            {/* 状态信息 */}
            {hitCount > 0 && (
              <div className="flex flex-wrap gap-[10px] mt-[6px] text-[11px] text-[#777] w-fit max-w-full">
                <span className="text-[#10b981]">命中 {hitCount} 条</span>
              </div>
            )}

            {/* 证据片段 */}
            {round.evidence && round.evidence.length > 0 && (
              <div className="bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] px-[10px] py-1 mt-[6px] text-[12px] text-[#888] w-fit max-w-full">
                <div
                  className="flex items-center gap-[6px] cursor-pointer select-none"
                  onClick={(e) => {
                    e.stopPropagation();
                    setEvidenceExpanded(!evidenceExpanded);
                  }}
                >
                  <span className="text-[11px] text-[#888]">证据片段（{round.evidence.length}）</span>
                  <span className="text-[9px] text-[#666]">{evidenceExpanded ? '∧' : '∨'}</span>
                </div>
                {evidenceExpanded && (
                  <div className="pt-1">
                    {round.evidence.map((item, idx) => (
                      <div
                        key={`${round.id}-evidence-${idx}`}
                        className={`py-[2px] ${idx > 0 ? 'border-t border-dashed border-[#3a3a3a]' : ''}`}
                      >
                        <div className="text-[10px] text-[#6f6f6f]">
                          {renderEvidenceMeta(item)}
                        </div>
                        <div className="text-[12px] text-[#888]">{item.text}</div>
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

// 工具标签组件 - 匹配设计稿的 .explore-tag
function ExploreTag({ toolCall }: { toolCall: ExploreToolCall }) {
  const IconComponent = TOOL_ICONS[toolCall.type] || Search;
  const isSearchType = toolCall.type === 'Search';

  return (
    <span className="inline-flex items-center gap-1 bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] px-[10px] py-1 text-[12px] text-[#888]">
      <IconComponent size={12} className="text-[#888]" />
      {toolCall.type}:{' '}
      <span className={isSearchType ? 'text-[#5c9eff] font-medium' : 'text-[#888]'}>
        {toolCall.highlight || toolCall.value}
      </span>
    </span>
  );
}

/**
 * ExploreRoundCard - 流事件轮次组件
 * 完全匹配 HTML 设计稿样式
 */
export function ExploreRoundCard({
  roundIdx,
  title,
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

  return (
    <div className="flex gap-[10px] py-2 items-start">
      {/* 胶囊容器 - 匹配设计稿的 .explore-round-capsule */}
      <div
        className={`
          bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] self-start max-w-full
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
          <div className="text-[#888] flex items-center justify-center text-[12px] font-medium">
            <Scan size={12} />
          </div>
          {/* 轮次标题 */}
          <div className={`flex items-center gap-2 text-[13px] text-[#888] ${expanded ? 'mb-0' : 'text-[12px]'}`}>
            {title || `深度探索（第${roundIdx}轮）`}
          </div>
          {/* 展开/折叠按钮 - 折叠时隐藏 */}
          {expanded && (
            <span className="text-[10px] text-[#666] ml-auto">∧</span>
          )}
        </div>

        {/* Body - 展开时显示 */}
        {expanded && (
          <div className="flex-1 w-fit max-w-full mt-2">
            {/* 工具标签 - 匹配设计稿的 .explore-tags */}
            <div className="flex flex-wrap gap-[6px] w-fit max-w-full">
              {toolCalls?.map((tc, idx) => (
                <ExploreTag key={idx} toolCall={tc} />
              ))}
              {reviewStatus && (
                <span className="inline-flex items-center gap-1 bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] px-[10px] py-1 text-[12px] text-[#888]">
                  <review.icon size={12} className={review.tone} />
                  Review: <span className="text-[#888]">{review.label}</span>
                </span>
              )}
            </div>

            {/* 状态信息 - 匹配设计稿的 .explore-status */}
            <div className="flex flex-wrap gap-[10px] mt-[6px] text-[11px] text-[#777] w-fit max-w-full">
              {hitCount > 0 && (
                <span className="text-[#10b981]">命中 {hitCount} 条</span>
              )}
              {missingItems && missingItems.length > 0 ? (
                <span className="text-[#f59e0b]">缺少：{missingItems.join('、')}</span>
              ) : statusText ? (
                <span>{statusText}</span>
              ) : null}
            </div>

            {/* 证据片段 - 匹配设计稿的 .explore-evidence */}
            {evidences && evidences.length > 0 && (
              <div className="bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] px-[10px] py-1 mt-[6px] text-[12px] text-[#888] w-fit max-w-full">
                <div
                  className="flex items-center gap-[6px] cursor-pointer select-none"
                  onClick={(e) => {
                    e.stopPropagation();
                    setEvidenceExpanded(!evidenceExpanded);
                  }}
                >
                  <span className="text-[11px] text-[#888]">证据片段（{evidences.length}）</span>
                  <span className="text-[9px] text-[#666]">{evidenceExpanded ? '∧' : '∨'}</span>
                </div>
                {evidenceExpanded && (
                  <div className="pt-1">
                    {evidences.map((item, idx) => (
                      <div
                        key={`evidence-${idx}`}
                        className={`py-[2px] ${idx > 0 ? 'border-t border-dashed border-[#3a3a3a]' : ''}`}
                      >
                        <div className="text-[10px] text-[#6f6f6f]">
                          {renderEvidenceMeta(item)}
                        </div>
                        <div className="text-[12px] text-[#888]">{item.text}</div>
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
 * 完全匹配 HTML 设计稿的 "AI 分析与规划" 卡片样式
 */
export function ExploreSummaryCard({
  totalRounds,
  summary,
  nextAction,
  nextTool,
  stats,
}: ExploreSummaryFlowData) {
  const [expanded, setExpanded] = useState(true);

  return (
    <div className="mt-3 mb-3">
      {/* 卡片容器 - 匹配设计稿内联样式 */}
      <div className="bg-[#2a2a2a] border border-[#3a3a3a] rounded-[16px] px-[10px] py-1 inline-block max-w-full">
        {/* Header */}
        <div
          className="flex items-center gap-2 cursor-pointer select-none"
          onClick={() => setExpanded(!expanded)}
          style={{ marginBottom: expanded ? '10px' : '0' }}
        >
          <span className="text-[#888] flex items-center">
            <Brain size={12} />
          </span>
          <span
            className="text-[13px] font-medium"
            style={{ color: expanded ? '#fff' : '#888', fontWeight: expanded ? 500 : 'normal' }}
          >
            AI 分析与规划
          </span>
          <span className="text-[9px] text-[#666] ml-auto">{expanded ? '∧' : '∨'}</span>
        </div>

        {/* Content */}
        {expanded && (
          <div>
            {/* 探索总结 */}
            {summary && (
              <div className="mb-[10px]">
                <div className="flex items-center gap-[6px] mb-1">
                  <span className="text-[#888] flex items-center">
                    <FileSearch size={12} />
                  </span>
                  <span className="text-[12px] text-[#888] font-medium">探索总结</span>
                </div>
                <div className="text-[12px] text-[#999] leading-[1.7] pl-[18px]">
                  {summary}
                </div>
              </div>
            )}

            {/* 下一步行动 */}
            {nextAction && (
              <div className="mb-[10px]">
                <div className="flex items-center gap-[6px] mb-1">
                  <span className="text-[#888] flex items-center">
                    <ArrowRightCircle size={12} />
                  </span>
                  <span className="text-[12px] text-[#888] font-medium">下一步行动</span>
                </div>
                <div className="text-[12px] text-[#999] leading-[1.7] pl-[18px]">
                  {nextAction}
                  {nextTool && (
                    <span className="ml-1 text-[#5c9eff] font-mono text-[11px]">{nextTool}</span>
                  )}
                </div>
              </div>
            )}

            {/* 统计标签 - 匹配设计稿样式 */}
            {stats && (
              <div className="flex flex-wrap gap-2 pl-[18px]">
                {stats.worldview !== undefined && (
                  <div className="flex items-center gap-1 px-[6px] py-[2px] bg-[#222] rounded text-[11px]">
                    <BookOpen size={11} className="text-[#666]" />
                    <span className="text-[#666]">世界观</span>
                    <span className="text-[#5c9eff] font-medium">{stats.worldview}</span>
                  </div>
                )}
                {stats.chapters && (
                  <div className="flex items-center gap-1 px-[6px] py-[2px] bg-[#222] rounded text-[11px]">
                    <FileText size={11} className="text-[#666]" />
                    <span className="text-[#666]">章节</span>
                    <span className="text-[#5c9eff] font-medium">{stats.chapters}</span>
                  </div>
                )}
                {stats.evidences !== undefined && (
                  <div className="flex items-center gap-1 px-[6px] py-[2px] bg-[#222] rounded text-[11px]">
                    <Layers size={11} className="text-[#666]" />
                    <span className="text-[#666]">证据</span>
                    <span className="text-[#5c9eff] font-medium">{stats.evidences}</span>
                  </div>
                )}
                {stats.coverage && (
                  <div className="flex items-center gap-1 px-[6px] py-[2px] bg-[#222] rounded text-[11px]">
                    <CheckCircle size={11} className="text-[#10b981]" />
                    <span className="text-[#666]">覆盖度</span>
                    <span className="text-[#10b981] font-medium">{stats.coverage}</span>
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
