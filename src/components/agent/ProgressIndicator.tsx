/**
 * ProgressIndicator - Agent进度显示组件
 *
 * 实时显示Agent执行进度、工具调用等信息
 */

import React from 'react';
import type { ProgressEvent, ToolCallEvent } from '@/hooks/useAgentChatStream';

interface ProgressIndicatorProps {
  currentProgress: ProgressEvent | null;
  toolCalls?: ToolCallEvent[];
  className?: string;
}

// 步骤图标映射
const STEP_ICONS = {
  intent_analysis: '🔍',
  thinking: '💭',
  tool_execution: '🛠️',
};

// 步骤颜色映射
const STEP_COLORS = {
  intent_analysis: 'from-blue-500 to-indigo-600',
  thinking: 'from-purple-500 to-pink-600',
  tool_execution: 'from-green-500 to-teal-600',
};

/**
 * 格式化时间戳
 */
function formatTimestamp(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

/**
 * 工具名称友好化
 */
function getFriendlyToolName(toolName: string): string {
  const toolNames: Record<string, string> = {
    get_chapter_by_order_tool: '读取章节',
    continue_writing_tool: '继续创作',
    search_analysis_fragments_tool: '检索设定',
    search_memory_tool: '搜索记忆',
    add_todo_tool: '添加待办',
    get_work_details_tool: '获取作品信息',
    update_work_metadata_tool: '更新元数据',
  };

  return toolNames[toolName] || toolName;
}

export default function ProgressIndicator({
  currentProgress,
  toolCalls = [],
  className = '',
}: ProgressIndicatorProps) {
  if (!currentProgress) {
    return null;
  }

  const stepIcon = STEP_ICONS[currentProgress.step] || '⚙️';
  const stepColor = STEP_COLORS[currentProgress.step] || 'from-gray-500 to-gray-600';

  return (
    <div className={`progress-indicator ${className}`}>
      {/* 当前进度 */}
      <div className="flex items-start gap-2 mb-2">
        {/* Agent头像 */}
        <div
          className={`flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br ${stepColor} flex items-center justify-center text-white text-xs shadow-sm`}
        >
          {stepIcon}
        </div>

        {/* 进度信息 */}
        <div className="flex-1">
          <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-2xl rounded-tl-sm px-3 py-2 border border-gray-200 shadow-sm">
            <div className="flex items-center gap-2">
              {/* 动画点 */}
              <div className="flex gap-0.5">
                <span
                  className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce"
                  style={{ animationDelay: '0ms' }}
                ></span>
                <span
                  className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce"
                  style={{ animationDelay: '150ms' }}
                ></span>
                <span
                  className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce"
                  style={{ animationDelay: '300ms' }}
                ></span>
              </div>

              {/* 进度描述 */}
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-700">
                  {currentProgress.description}
                </p>

                {/* 详细信息 */}
                {currentProgress.details && (
                  <div className="mt-1 text-xs text-gray-500">
                    {currentProgress.details.intent && (
                      <span className="inline-block bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full mr-1">
                        意图: {currentProgress.details.intent}
                      </span>
                    )}
                    {currentProgress.node && (
                      <span className="inline-block bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                        节点: {currentProgress.node}
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* 时间戳 */}
              <span className="text-xs text-gray-400 ml-auto">
                {formatTimestamp(currentProgress.timestamp)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 工具调用历史 */}
      {toolCalls.length > 0 && (
        <div className="mt-2 ml-8 space-y-1">
          {toolCalls.map((toolCall, index) => (
            <div
              key={`${toolCall.tool}-${index}`}
              className="flex items-center gap-2 text-xs text-gray-600 bg-green-50 border border-green-200 rounded-lg px-3 py-1.5"
            >
              <span className="text-green-600">✓</span>
              <span className="font-medium text-green-700">
                {getFriendlyToolName(toolCall.tool)}
              </span>
              {toolCall.args && Object.keys(toolCall.args).length > 0 && (
                <span className="text-gray-500 truncate flex-1">
                  ({Object.entries(toolCall.args)
                    .slice(0, 2)
                    .map(([key, value]) => `${key}: ${value}`)
                    .join(', ')})
                </span>
              )}
              <span className="text-gray-400 ml-auto">
                {formatTimestamp(toolCall.timestamp)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
