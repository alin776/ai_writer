/**
 * ToolLine - 单行工具调用组件（Claude Code 风格）
 *
 * 替代 StepCard，将工具调用压缩为一行显示：
 * 🟢 Read(chapter_1.md)  — running（绿色闪烁圆点）
 * ⚫ Read(chapter_1.md)  — done（灰色圆点）
 * 🔴 Read(chapter_1.md)  — error（红色圆点）
 *
 * Task 嵌套展示（Claude Code 风格）：
 * ● Task("阅读第1-5章，分析每章的爽点分布")
 *   └ ● Read(chapters/03-蕴养筋脉.md)      ← 实时最新子步骤
 *       +4 more                              ← 折叠已完成数
 *
 * 完成后：
 * ● Task("阅读第1-5章，分析每章的爽点分布")
 *   └ Done (7 tool uses)                     ← 完成摘要
 */

import type { StepFlowData, ChildStepData } from '@/types/agent';

// 工具名 → 显示动词映射
const TOOL_VERB_MAP: Record<string, string> = {
  read_file: 'Read',
  write_file: 'Write',
  edit_file: 'Edit',
  ls: 'List',
  glob: 'Search',
  grep: 'Grep',
  semantic_search: 'Search',
  write_todos: 'Planned',
  read_todos: 'ReadTodos',
  task: 'Task',
  skill: 'Skill',
  skill_switch: 'Switch',
  execute: 'Run',
  web_search: 'Web Search',
  fetch_url: 'Fetch',
};

/**
 * 从 toolName + toolInput 生成 ToolLine 显示文字
 * 格式：动词(参数)
 */
function formatToolLine(toolName?: string, toolInput?: any, fallbackTitle?: string): string {
  if (!toolName) return fallbackTitle || 'Working…';

  const verb = TOOL_VERB_MAP[toolName] || toolName;

  if (!toolInput || typeof toolInput !== 'object') return verb;

  // 根据工具类型提取关键参数
  switch (toolName) {
    case 'read_file':
    case 'write_file':
    case 'edit_file': {
      const filePath = toolInput.file_path || '';
      return `${verb}(${filePath})`;
    }
    case 'ls': {
      const dir = toolInput.path || '/';
      return `${verb}(${dir})`;
    }
    case 'glob':
    case 'grep': {
      const pattern = toolInput.pattern || '';
      return `${verb}(${pattern})`;
    }
    case 'semantic_search': {
      const query = String(toolInput.query || '').slice(0, 30);
      return `${verb}("${query}")`;
    }
    case 'task': {
      const prompt = String(toolInput.description || '').slice(0, 40);
      return `${verb}("${prompt}")`;
    }
    case 'skill':
    case 'skill_switch': {
      const skillName = toolInput?.skill_name || '';
      return `${verb}(${skillName})`;
    }
    case 'write_todos':
      return 'Planned';
    case 'execute': {
      const cmd = String(toolInput.command || '').slice(0, 60);
      return `${verb}(${cmd})`;
    }
    case 'web_search': {
      const query = String(toolInput.query || '').slice(0, 50);
      return `${verb}("${query}")`;
    }
    case 'fetch_url': {
      const url = String(toolInput.url || '').slice(0, 60);
      return `${verb}(${url})`;
    }
    default:
      return verb;
  }
}

/**
 * 渲染 Task 子步骤嵌套内容
 */
function TaskChildContent({
  status,
  childSteps,
  childToolCount,
}: {
  status: StepFlowData['status'];
  childSteps?: ChildStepData[];
  childToolCount?: number;
}) {
  // 完成态：摘要
  if (status === 'done') {
    const count = childToolCount ?? childSteps?.length ?? 0;
    if (count > 0) {
      return (
        <div className="flex items-center gap-2 py-0.5 text-base font-mono text-gray-400 dark:text-gray-500">
          <span>└</span>
          <span>Done ({count} tool uses)</span>
        </div>
      );
    }
    return null;
  }

  // 运行态：最新子步骤 + 折叠计数
  if (childSteps && childSteps.length > 0) {
    const latest = childSteps[childSteps.length - 1];
    const doneCount = childSteps.filter(c => c.status === 'done').length;
    const collapsed = latest.status === 'done' ? doneCount - 1 : doneCount;

    return (
      <div className="flex flex-col">
        <div className="flex items-center gap-2 py-0.5 text-base font-mono text-gray-400 dark:text-gray-500">
          <span>└</span>
          <span className="truncate">
            {formatToolLine(latest.toolName, latest.toolInput, latest.title)}
          </span>
        </div>
        {collapsed > 0 && (
          <div className="ml-6 text-base font-mono text-gray-400 dark:text-gray-500">
            +{collapsed} more tool uses
          </div>
        )}
      </div>
    );
  }

  return null;
}

interface ToolLineProps extends StepFlowData {
  children?: React.ReactNode;
}

export function ToolLine({
  status,
  toolName,
  toolInput,
  title,
  description,
  isTask,
  isMemory,
  childSteps,
  childToolCount,
  children,
}: ToolLineProps) {
  // Memory 步骤：running → "Add a memory"，done → "Memory updated"
  const displayText = isMemory
    ? (status === 'done' ? (description || 'Memory updated') : (title || 'Add a memory'))
    : formatToolLine(toolName, toolInput, title);

  // write_todos 不单独渲染为 ToolLine（由 TodoBlock 接管）
  if (toolName === 'write_todos') {
    return children ? <>{children}</> : null;
  }

  const isTaskStep = isTask || toolName === 'task';

  return (
    <div className="flex flex-col">
      {/* 主行 */}
      <div className="flex items-center gap-2 py-0.5 text-base font-mono">
        {/* 状态圆点 */}
        <span
          className={`inline-block w-2 h-2 rounded-full flex-shrink-0 ${
            status === 'running'
              ? 'bg-emerald-500 animate-pulse'
              : status === 'error'
                ? 'bg-red-500'
                : 'bg-gray-400 dark:bg-gray-500'
          }`}
        />
        {/* 工具调用文字 */}
        <span className="text-gray-500 dark:text-gray-400 truncate">
          {displayText}
        </span>
      </div>
      {/* 完成/错误描述（memory done 已显示在主行，不重复；error 始终显示） */}
      {description && (status === 'error' || (!isMemory && status === 'done' && (toolName === 'web_search' || toolName === 'fetch_url'))) && (
        <div className={`ml-4 text-base font-mono ${
          status === 'error'
            ? 'text-red-500 dark:text-red-400'
            : 'text-gray-400 dark:text-gray-500'
        }`}>
          └ {description}
        </div>
      )}
      {/* 子步骤嵌套区（仅 task 步骤） */}
      {isTaskStep && (
        <div className="ml-4">
          <TaskChildContent
            status={status}
            childSteps={childSteps}
            childToolCount={childToolCount}
          />
        </div>
      )}
      {/* 内嵌的 RevisionCard 等子元素 */}
      {children && <div className="ml-4">{children}</div>}
    </div>
  );
}
