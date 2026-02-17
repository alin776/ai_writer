/**
 * FileChangeCard — RevisionCard 风格紧凑文件卡片
 *
 * 单行显示：[图标] 路径  [✓] [×]
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

const opIcon: Record<string, React.ElementType> = {
  create: FilePlus,
  modify: FileEdit,
  delete: FileX,
};

const FileChangeCard: React.FC<FileChangeCardProps> = ({
  path,
  op,
  index,
  onAccept,
  onReject,
  onClick,
}) => {
  const Icon = opIcon[op] || FileEdit;

  return (
    <div
      className="flex items-center gap-2 px-2.5 py-1.5 bg-[#192438] rounded-lg cursor-pointer hover:bg-slate-800 transition-colors text-[13px]"
      onClick={() => onClick?.(index)}
    >
      <Icon className="h-3.5 w-3.5 flex-shrink-0 text-slate-500" />
      <span className="text-slate-200 truncate flex-1" title={path}>{path}</span>
      <div className="flex gap-1 ml-auto flex-shrink-0">
        <button
          type="button"
          title="采纳"
          className="w-[22px] h-[22px] flex items-center justify-center rounded text-green-400 hover:bg-green-500/10 transition-colors"
          onClick={(e) => { e.stopPropagation(); onAccept(index); }}
        >
          <Check size={13} />
        </button>
        <button
          type="button"
          title="弃用"
          className="w-[22px] h-[22px] flex items-center justify-center rounded text-red-400 hover:bg-red-500/10 transition-colors"
          onClick={(e) => { e.stopPropagation(); onReject(index); }}
        >
          <X size={13} />
        </button>
      </div>
    </div>
  );
};

export default FileChangeCard;
