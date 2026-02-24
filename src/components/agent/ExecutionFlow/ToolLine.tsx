/**
 * ToolLine - 单行工具调用组件（Claude Code 风格）
 *
 * 替代 StepCard，将工具调用压缩为一行显示：
 * 🟢 Read(chapter_1.md)  — running（绿色闪烁圆点）
 * ⚫ Read(chapter_1.md)  — done（灰色圆点）
 * 🔴 Read(chapter_1.md)  — error（红色圆点）
 */

import type { StepFlowData } from '@/types/agent';

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
      const prompt = String(toolInput.prompt || '').slice(0, 40);
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
    default:
      return verb;
  }
}

interface ToolLineProps extends StepFlowData {
  children?: React.ReactNode;
}

export function ToolLine({ status, toolName, toolInput, title, children }: ToolLineProps) {
  const displayText = formatToolLine(toolName, toolInput, title);

  // write_todos 不单独渲染为 ToolLine（由 TodoBlock 接管）
  if (toolName === 'write_todos') {
    return children ? <>{children}</> : null;
  }

  return (
    <div className="flex flex-col">
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
      {/* 内嵌的 RevisionCard 等子元素 */}
      {children && <div className="ml-4">{children}</div>}
    </div>
  );
}
