/**
 * SummarizationCard - AI整合分析卡片组件
 * 显示任务分类和上下文处理信息
 */

import { useState } from 'react';
import { Check, Loader2, ChevronUp, ChevronDown, FileText, Wrench } from 'lucide-react';
import type { SummarizationFlowData } from '@/types/agent';
import { KnowledgeContainer } from './KnowledgeContainer';

interface SummarizationCardProps extends SummarizationFlowData {
  defaultExpanded?: boolean;
}

export function SummarizationCard({
  status,
  taskClassification,
  contextStats,
  defaultExpanded = true
}: SummarizationCardProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const [contextExpanded, setContextExpanded] = useState(false);  // 二级卡片默认收缩

  // 防御性处理：确保数据存在
  const safeTaskClassification = taskClassification || {
    inputTasks: [],
    outputTasks: [],
    displayTasks: []
  };
  const safeContextStats = contextStats || {
    originalLength: 0,
    compressedLength: 0,
    mode: '流式生成'
  };

  // 计算任务总数
  const totalTasks =
    safeTaskClassification.inputTasks.length +
    safeTaskClassification.outputTasks.length +
    safeTaskClassification.displayTasks.length;

  // 构建任务分类的知识项
  const taskItems = [
    ...safeTaskClassification.inputTasks.map(t => ({ name: t.tool, tag: '输入型' })),
    ...safeTaskClassification.outputTasks.map(t => ({ name: t.tool, tag: '输出型' })),
    ...safeTaskClassification.displayTasks.map(t => ({ name: t.tool, tag: '展示型' }))
  ];

  return (
    <div className="mb-3">
      {/* 步骤头部 */}
      <div
        className="flex items-center gap-2 py-1.5 cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        {/* 状态图标 */}
        <div className="w-[18px] h-[18px] flex items-center justify-center">
          {status === 'running' ? (
            <Loader2 size={12} className="text-blue-500 animate-spin" />
          ) : (
            <Check size={12} className="text-gray-500" />
          )}
        </div>

        {/* 标题区域 */}
        <div className="flex items-center gap-1.5">
          <span className="text-[14px] font-medium text-gray-900 dark:text-white">AI整合分析</span>
          <span className="text-gray-400 dark:text-gray-600 text-[10px]">
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
          </span>
        </div>

        <div className="flex-1" />
      </div>

      {/* 步骤内容 */}
      {expanded && (
        <div className="ml-[26px] pt-1">
          {/* 任务分类 */}
          {totalTasks > 0 && (
            <div className="mb-2">
              <KnowledgeContainer
                title={`任务分类(${totalTasks})`}
                icon="Layers"
                items={taskItems}
              />
            </div>
          )}

          {/* 上下文处理 */}
          <div className="mb-2">
            <div className={`inline-block bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 ${
              contextExpanded ? 'rounded-xl px-3 py-2' : 'rounded-full px-2.5 py-1'
            }`}>
              <div
                className="flex items-center gap-1.5 cursor-pointer select-none"
                onClick={() => setContextExpanded(!contextExpanded)}
              >
                <span className="text-gray-500">
                  <FileText size={12} />
                </span>
                <span className="text-[13px] text-gray-500">上下文处理</span>
                <span className="text-gray-400 dark:text-gray-600 text-[9px] ml-0.5">
                  {contextExpanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
                </span>
              </div>
              {contextExpanded && (
                <div className="pt-1.5 space-y-1">
                  <div className="flex items-center gap-2 text-[13px]">
                    <span className="text-gray-500 min-w-[60px]">原始大小</span>
                    <span className="font-mono text-[12px] text-gray-600 dark:text-gray-400">
                      {safeContextStats.originalLength} 字符
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-[13px]">
                    <span className="text-gray-500 min-w-[60px]">处理后</span>
                    <span className="font-mono text-[12px] text-gray-600 dark:text-gray-400">
                      {safeContextStats.compressedLength} 字符
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-[13px]">
                    <span className="text-gray-500 min-w-[60px]">整合模式</span>
                    <span className="font-mono text-[12px] text-gray-600 dark:text-gray-400">
                      {safeContextStats.mode}
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* 步骤描述 */}
          <div className="text-[13px] text-gray-500 dark:text-[#999] my-2 leading-[1.6]">
            将{safeTaskClassification.inputTasks.length}个输入型任务和{safeTaskClassification.outputTasks.length}个输出型任务的结果进行AI整合，生成连贯的最终响应。
          </div>

          {/* 工具调用标签 */}
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-full my-2">
            <span className="text-gray-400 dark:text-slate-500">
              <Wrench size={12} />
            </span>
            <span className="text-[13px] text-gray-500 dark:text-slate-400">调用工具</span>
            <span className="font-mono text-[12px] text-gray-600 dark:text-slate-300">
              response_builder.summarize
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
