/**
 * OperateCard - ContentOperator 执行轨迹展示
 * v2.0: 匹配 HTML 预览设计，三阶段默认展开
 *
 * 设计规范：
 * - 响应式主题：使用 Tailwind dark: 前缀
 * - 浅色模式：白色背景，灰色边框和文本
 * - 深色模式：深蓝灰色背景（slate-800/900），深蓝色边框（slate-700）
 * - 与 ExploreCard 保持一致的胶囊/标签样式
 */

import { useState } from 'react';
import {
  Check,
  ChevronUp,
  ChevronDown,
  GitBranch,
  Crosshair,
  Play,
  ArrowRight,
  Wrench,
  Cog,
  Search,
  MapPin,
  CheckCircle,
  Edit3,
  FileText,
  Clock,
  Brain,
} from 'lucide-react';
import type {
  OperateFlowData,
  OperatePhaseData,
  OperateTag,
  OperateOperationType,
} from '@/types/agent';

// ==================== 映射常量 ====================

/** 操作类型映射（技术值 → 用户显示） */
const OPERATION_LABELS: Record<string, string> = {
  append: '追加内容',
  replace: '替换段落',
  insert: '插入内容',
  content: '整章替换',
  replace_all: '整章替换',
  create: '创建章节',
  title: '修改标题',
};

/** 工具名称映射 - 保持代码格式 */
const TOOL_LABELS: Record<string, string> = {
  apply_chapter_edit: 'apply_chapter_edit',
  create_chapter: 'create_chapter',
  update_chapter_title: 'update_chapter_title',
};

/** 定位方式映射 */
const LOCATE_METHOD_LABELS: Record<string, string> = {
  direct: '直接定位',
  text_match: '文本匹配',
  semantic: '语义定位',
  none: '无需定位',
  fallback: '降级处理',
  failed: '定位失败',
};

/** 阶段标题 */
const PHASE_TITLES: Record<number, string> = {
  1: '意图路由',
  2: '智能定位',
  3: '执行操作',
};

/** 阶段图标 */
const PHASE_ICONS = {
  1: GitBranch,
  2: Crosshair,
  3: Play,
};

// ==================== 工具函数 ====================

/** 判断操作是否需要定位 */
function needsLocate(operation: OperateOperationType): boolean {
  return ['replace', 'insert'].includes(operation);
}

/** 从后端数据构建三阶段数据 */
export function buildOperatePhases(data: Partial<OperateFlowData>): OperatePhaseData[] {
  const operation = data.operation || 'append';
  const locateMethod = data.locateMethod || 'none';
  const targetOperation = data.targetOperation || operation;
  const toolUsed = data.toolUsed || 'apply_chapter_edit';
  const status = data.status || 'running';
  const requiresConfirmation = data.requiresConfirmation ?? false;
  const locateTarget = data.locateTarget || data.chapterTitle || '';

  // 阶段1：意图路由
  const phase1: OperatePhaseData = {
    phase: 1,
    title: PHASE_TITLES[1],
    status: 'done',
    tags: [
      { label: '输入', value: operation, icon: 'arrow-right' },
      { label: '工具', value: TOOL_LABELS[toolUsed] || toolUsed, icon: 'wrench' },
      { label: '底层', value: targetOperation, icon: 'cog' },
      { label: '需定位', value: needsLocate(operation) ? '是' : '否', icon: 'crosshair', variant: needsLocate(operation) ? 'success' : 'default' },
    ],
  };

  // 阶段2：智能定位
  const needsLocatePhase = needsLocate(operation);
  const phase2: OperatePhaseData = {
    phase: 2,
    title: PHASE_TITLES[2],
    status: needsLocatePhase
      ? (locateMethod === 'failed' ? 'done' : status === 'done' ? 'done' : 'running')
      : 'skipped',
    tags: needsLocatePhase
      ? [
          { label: '方式', value: LOCATE_METHOD_LABELS[locateMethod] || locateMethod, icon: 'search' },
          { label: '位置', value: locateTarget || '定位中...', icon: 'map-pin' },
          {
            label: '状态',
            value: locateMethod === 'failed' ? '定位失败' : locateTarget ? '已定位' : '定位中...',
            icon: 'check-circle',
            variant: locateMethod === 'failed' ? 'warning' : locateTarget ? 'success' : 'default',
          },
        ]
      : [{ label: '状态', value: '跳过（无需定位）', icon: 'check-circle' }],
  };

  // 阶段3：执行操作
  const statusValue = requiresConfirmation
    ? '等待确认'
    : status === 'done'
      ? '已完成'
      : status === 'error'
        ? '执行失败'
        : '执行中...';
  const statusVariant = status === 'done' && !requiresConfirmation
    ? 'success'
    : status === 'error'
      ? 'warning'
      : 'success';  // 等待确认也用 success 色

  const phase3: OperatePhaseData = {
    phase: 3,
    title: PHASE_TITLES[3],
    status: status === 'done' || status === 'error' ? 'done' : 'running',
    tags: [
      { label: '操作', value: OPERATION_LABELS[targetOperation] || targetOperation, icon: 'edit-3' },
      { label: '目标', value: locateTarget || '整章', icon: 'file-text' },
      { label: '状态', value: statusValue, icon: 'clock', variant: statusVariant },
    ],
  };

  return [phase1, phase2, phase3];
}

// ==================== 图标映射 ====================

const IconMap: Record<string, React.ComponentType<{ size: number; className?: string }>> = {
  'arrow-right': ArrowRight,
  'wrench': Wrench,
  'cog': Cog,
  'crosshair': Crosshair,
  'search': Search,
  'map-pin': MapPin,
  'check-circle': CheckCircle,
  'edit-3': Edit3,
  'file-text': FileText,
  'clock': Clock,
};

// ==================== 组件 ====================

interface OperateCardProps {
  data: OperateFlowData;
  defaultExpanded?: boolean;
}

export function OperateCard({ data, defaultExpanded = true }: OperateCardProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);

  // 如果没有 phases，从原始数据构建
  const phases = data.phases?.length ? data.phases : buildOperatePhases(data);
  const isRunning = data.status === 'running';

  return (
    <div className="mb-3">
      {/* Header */}
      <div
        className="flex items-center gap-2 py-1.5 cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="w-[18px] h-[18px] flex items-center justify-center">
          {isRunning ? (
            <Clock size={12} className="text-gray-500 dark:text-slate-400 animate-pulse" />
          ) : (
            <Check size={12} className="text-gray-500 dark:text-slate-400" />
          )}
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-[14px] font-medium text-gray-900 dark:text-white">
            Operate 轨迹（3 阶段）
          </span>
          <span className="text-gray-400 dark:text-slate-600 flex items-center">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>
        <div className="flex-1" />
      </div>

      {/* Body */}
      {expanded && (
        <div className="ml-[26px] pt-1">
          {/* 三阶段面板 */}
          <div className="my-2">
            {phases.map((phase) => (
              <OperatePhaseCard key={phase.phase} phase={phase} />
            ))}
          </div>

          {/* Operate 执行总结 */}
          <OperateSummaryCard data={data} />

          {/* 步骤描述 */}
          <div className="text-[13px] text-gray-500 dark:text-slate-300 leading-[1.6] my-2">
            三阶段流程：意图路由 → 智能定位 → 执行操作，自动完成参数映射和定位。
          </div>

          {/* 工具调用标签 */}
          <div className="inline-flex items-center gap-1.5 px-[10px] py-1 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-[16px] my-2">
            <Wrench size={12} className="text-gray-500 dark:text-slate-400" />
            <span className="text-[13px] text-gray-500 dark:text-slate-400">调用工具</span>
            <span className="text-[12px] font-mono text-gray-600 dark:text-slate-300">
              operate_apply (operation: {data.operation})
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

/** 阶段卡片 - 默认展开 */
function OperatePhaseCard({ phase }: { phase: OperatePhaseData }) {
  const [expanded, setExpanded] = useState(true);  // 默认展开
  const PhaseIcon = PHASE_ICONS[phase.phase] || GitBranch;
  const isSkipped = phase.status === 'skipped';
  const isRunning = phase.status === 'running';

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
          ${isSkipped ? 'opacity-50' : ''}
          ${isRunning ? 'animate-pulse' : ''}
        `}
      >
        {/* Header */}
        <div
          className="flex items-center gap-2 cursor-pointer select-none"
          onClick={() => setExpanded(!expanded)}
        >
          <div className="text-gray-500 dark:text-slate-400 flex items-center justify-center text-[12px] font-medium">
            <PhaseIcon size={12} />
          </div>
          <div className={`flex items-center gap-2 text-[13px] text-gray-600 dark:text-slate-400 ${expanded ? 'mb-0' : 'text-[12px]'}`}>
            阶段{phase.phase}：{phase.title}
          </div>
          <span className="text-gray-400 dark:text-slate-600 ml-auto flex items-center">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>

        {/* Body - 展开时显示标签组 */}
        {expanded && (
          <div className="flex-1 w-fit max-w-full mt-2">
            <div className="flex flex-wrap gap-[6px] w-fit max-w-full">
              {phase.tags.map((tag, idx) => (
                <OperateTagComponent key={idx} tag={tag} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/** 标签组件 - 匹配 HTML 设计 */
function OperateTagComponent({ tag }: { tag: OperateTag }) {
  const IconComponent = tag.icon ? IconMap[tag.icon] : null;

  // 根据 variant 确定样式
  const isSuccess = tag.variant === 'success';
  const isWarning = tag.variant === 'warning';

  // 工具和底层字段使用 code 样式
  const isCodeField = tag.icon === 'wrench' || tag.icon === 'cog';

  const baseClass = 'inline-flex items-center gap-1 rounded-[16px] px-[10px] py-1 text-[12px]';
  const variantClass = isSuccess
    ? 'bg-[rgba(16,185,129,0.1)] border border-[rgba(16,185,129,0.3)] text-gray-600 dark:text-slate-400'
    : isWarning
      ? 'bg-[rgba(245,158,11,0.1)] border border-[rgba(245,158,11,0.3)] text-gray-600 dark:text-slate-400'
      : 'bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-600 dark:text-slate-400';

  const valueClass = isSuccess
    ? 'text-[#10b981] font-medium'
    : isWarning
      ? 'text-[#f59e0b] font-medium'
      : isCodeField
        ? 'font-mono text-gray-500 dark:text-slate-400'
        : 'text-gray-700 dark:text-slate-300 font-medium';

  return (
    <span className={`${baseClass} ${variantClass}`}>
      {IconComponent && <IconComponent size={11} className="text-gray-500 dark:text-slate-400" />}
      {tag.label}: <span className={valueClass}>{tag.value}</span>
    </span>
  );
}

/** Operate 执行总结卡片 - 默认折叠 */
function OperateSummaryCard({ data }: { data: OperateFlowData }) {
  const [expanded, setExpanded] = useState(false);  // 默认折叠
  const operation = data.operation || 'append';
  const locateMethod = data.locateMethod || 'none';
  const toolUsed = data.toolUsed || 'apply_chapter_edit';

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
            Operate 执行总结
          </span>
          <span className="text-gray-400 dark:text-slate-600 ml-auto flex items-center">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>

        {/* Body */}
        {expanded && (
          <div>
            {/* 路由决策 */}
            <div className="mb-[10px]">
              <div className="flex items-center gap-[6px] mb-1">
                <span className="text-gray-500 dark:text-slate-400 flex items-center">
                  <GitBranch size={12} />
                </span>
                <span className="text-[12px] text-gray-600 dark:text-slate-400 font-medium">路由决策</span>
              </div>
              <div className="text-[12px] text-gray-600 dark:text-slate-300 leading-[1.7] pl-[18px]">
                输入操作 <span className="text-[#5c9eff] font-medium">{operation}</span>
                {needsLocate(operation as OperateOperationType) ? ' 需要定位到具体段落，' : ' 无需定位，'}
                自动选择 <span className="font-mono text-[11px] text-[#10b981]">{toolUsed}</span> 工具执行。
              </div>
            </div>

            {/* 定位过程（如果需要） */}
            {needsLocate(operation as OperateOperationType) && (
              <div className="mb-[10px]">
                <div className="flex items-center gap-[6px] mb-1">
                  <span className="text-gray-500 dark:text-slate-400 flex items-center">
                    <Crosshair size={12} />
                  </span>
                  <span className="text-[12px] text-gray-600 dark:text-slate-400 font-medium">定位过程</span>
                </div>
                <div className="text-[12px] text-gray-600 dark:text-slate-300 leading-[1.7] pl-[18px]">
                  使用 <span className="text-[#10b981]">{LOCATE_METHOD_LABELS[locateMethod] || locateMethod}</span> 策略
                  定位到 {data.locateTarget || data.chapterTitle || '目标位置'}。
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ==================== 导出 ====================

export default OperateCard;
