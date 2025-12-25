/**
 * ToolCard - 工具卡片组件
 * 样式复用 ActivityStream.module.css 风格
 */

import {
  FileText,
  Search,
  PenTool,
  Edit3,
  Plus,
  Check,
  BarChart2,
  BookOpen,
  RefreshCw,
  Wrench,
  Loader2,
  CheckCircle,
  MessageSquare,
  Sparkles,
  Star,
  ListTodo,
  Save,
  FileSearch
} from 'lucide-react';

// Lucide 图标映射
const ICON_MAP: Record<string, React.ComponentType<any>> = {
  FileText,
  Search,
  PenTool,
  Edit3,
  Plus,
  Check,
  BarChart2,
  BookOpen,
  RefreshCw,
  Wrench,
  MessageSquare,
  Sparkles,
  Star,
  ListTodo,
  Save,
  FileSearch
};

interface ToolCardProps {
  taskId: number;
  icon: string;
  title: string;
  description: string;
  status: 'running' | 'done' | 'error';
}

export function ToolCard({ icon, title, description, status }: ToolCardProps) {
  const IconComponent = ICON_MAP[icon] || Wrench;

  // 卡片容器样式 - 复用 ActivityStream 风格
  const cardStyles = {
    running: 'border-blue-200 bg-blue-50 dark:border-blue-500/30 dark:bg-blue-500/10',
    done: 'border-emerald-100 bg-emerald-50 dark:border-emerald-500/30 dark:bg-emerald-500/10',
    error: 'border-red-200 bg-red-50 dark:border-red-500/30 dark:bg-red-500/10'
  };

  // 图标颜色样式
  const iconColorStyles = {
    running: 'text-blue-600 dark:text-blue-400',
    done: 'text-emerald-500 dark:text-emerald-400',
    error: 'text-red-500 dark:text-red-400'
  };

  return (
    <div className={`flex gap-2.5 p-2.5 rounded-[10px] border my-2.5 transition-all duration-300 ease-out ${cardStyles[status]}`}>
      {/* 工具图标 - 28px 圆形，固定背景色 */}
      <div className="w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 bg-indigo-50 dark:bg-slate-700">
        <IconComponent size={14} className={`transition-colors duration-300 ${iconColorStyles[status]}`} />
      </div>

      {/* 内容区域 */}
      <div className="flex-1 min-w-0">
        <div className="text-[13px] font-medium text-slate-800 dark:text-slate-200">
          {title}
        </div>
        <div className="flex gap-1.5 mt-1">
          {/* 工具调用标签 */}
          <span className="text-[11px] px-1.5 py-0.5 rounded-full font-medium bg-sky-100 text-sky-700 dark:bg-sky-900/50 dark:text-sky-300">
            工具调用
          </span>
          {/* 参数描述标签 */}
          {description && (
            <span className="text-[11px] px-1.5 py-0.5 rounded-full font-medium bg-violet-100 text-violet-800 dark:bg-violet-900/50 dark:text-violet-300">
              {description}
            </span>
          )}
        </div>
      </div>

      {/* 状态指示器 - 带过渡动画 */}
      <div className="flex items-center justify-center w-5 flex-shrink-0 transition-opacity duration-300">
        {status === 'running' && (
          <Loader2 size={14} className="text-blue-500 animate-spin" />
        )}
        {status === 'done' && (
          <CheckCircle size={14} className="text-emerald-500" />
        )}
      </div>
    </div>
  );
}
