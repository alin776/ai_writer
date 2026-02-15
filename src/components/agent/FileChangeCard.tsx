/**
 * FileChangeCard — 单个文件变更卡片
 *
 * 显示：文件图标 + 路径 + 操作类型 + ✓/× 按钮
 */
import React from 'react';
import { Check, X, FilePlus, FileEdit, FileX } from 'lucide-react';

interface FileChangeCardProps {
  path: string;
  op: string;
  index: number;
  onAccept: (index: number) => void;
  onReject: (index: number) => void;
  onClick?: (index: number) => void;
}

const opConfig: Record<string, { icon: React.ElementType; label: string; color: string }> = {
  create: { icon: FilePlus, label: '新建', color: 'text-green-600' },
  modify: { icon: FileEdit, label: '修改', color: 'text-amber-600' },
  delete: { icon: FileX, label: '删除', color: 'text-red-600' },
};

const FileChangeCard: React.FC<FileChangeCardProps> = ({
  path,
  op,
  index,
  onAccept,
  onReject,
  onClick,
}) => {
  const config = opConfig[op] || opConfig.modify;
  const Icon = config.icon;

  return (
    <div
      className="group flex items-center gap-2 px-3 py-2 rounded-lg border border-zinc-100 dark:border-slate-700 hover:bg-zinc-50 dark:hover:bg-slate-800 transition-colors cursor-pointer"
      onClick={() => onClick?.(index)}
    >
      <Icon className={`h-4 w-4 flex-shrink-0 ${config.color}`} />
      <span className="text-sm text-zinc-700 dark:text-slate-300 flex-1 truncate" title={path}>
        {path}
      </span>
      <span className={`text-xs px-1.5 py-0.5 rounded ${config.color} bg-opacity-10`}>
        {config.label}
      </span>
      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
        <button
          type="button"
          onClick={(e) => { e.stopPropagation(); onAccept(index); }}
          className="h-6 w-6 flex items-center justify-center rounded hover:bg-green-100 text-green-600 dark:hover:bg-green-900/30"
          title="接受"
        >
          <Check className="h-3.5 w-3.5" />
        </button>
        <button
          type="button"
          onClick={(e) => { e.stopPropagation(); onReject(index); }}
          className="h-6 w-6 flex items-center justify-center rounded hover:bg-red-100 text-red-600 dark:hover:bg-red-900/30"
          title="拒绝"
        >
          <X className="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
  );
};

export default FileChangeCard;
