/**
 * TodoBlock - TodoList 组件（Claude Code 风格）
 *
 * 处理 write_todos 工具的输出，显示任务清单：
 * Planned(当前任务) 或 Planned(2/5 completed)
 *   ☐ 任务 A
 *   ✅ 任务 B（已完成）
 */

import type { TodoFlowData, TodoItem } from '@/types/agent';

interface TodoBlockProps extends TodoFlowData {}

export function TodoBlock({ todos, currentTask }: TodoBlockProps) {
  if (!todos || todos.length === 0) return null;

  const completedCount = todos.filter(t => t.status === 'completed').length;
  const total = todos.length;
  const allDone = completedCount === total;

  // 标题行：全部完成 Planned，否则 Planning
  const headerText = allDone
    ? `Planned(${total}/${total} completed)`
    : currentTask
      ? `Planning(${currentTask})`
      : completedCount > 0
        ? `Planning(${completedCount}/${total} completed)`
        : `Planning(${total} tasks)`;

  return (
    <div className="py-1">
      {/* 标题行 */}
      <div className="flex items-center gap-2 text-base font-mono">
        <span
          className={`inline-block w-2 h-2 rounded-full flex-shrink-0 ${
            allDone
              ? 'bg-gray-400 dark:bg-gray-500'
              : 'bg-emerald-500 animate-pulse'
          }`}
        />
        <span className="text-gray-500 dark:text-gray-400">
          {headerText}
        </span>
      </div>

      {/* 子项清单 */}
      <div className="ml-4 mt-1 space-y-0.5">
        {todos.map((todo: TodoItem, idx: number) => (
          <div
            key={idx}
            className="flex items-start gap-2 text-base font-mono"
          >
            <span className="flex-shrink-0 w-4 text-center">
              {todo.status === 'completed' ? '✅' : '☐'}
            </span>
            <span className={`${
              todo.status === 'completed'
                ? 'text-gray-400 dark:text-gray-500 line-through'
                : todo.status === 'in_progress'
                  ? 'text-emerald-700 dark:text-emerald-400'
                  : 'text-gray-600 dark:text-gray-300'
            }`}>
              {typeof todo.description === 'string' ? todo.description : String(todo.description ?? '')}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
