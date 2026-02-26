import { FileText, Check, X } from 'lucide-react';

interface DemoRevisionCardProps {
  filename: string;
  additions: number;
  accepted?: boolean;
}

export default function DemoRevisionCard({ filename, additions, accepted = false }: DemoRevisionCardProps) {
  return (
    <div className="flex items-center gap-2 px-2.5 py-1.5 backdrop-blur-md border border-white/[0.08] rounded-lg text-[13px]"
      style={{ background: 'linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%)' }}
    >
      {/* 文件图标 */}
      <FileText className="h-3.5 w-3.5 text-slate-500 flex-shrink-0" />

      {/* 文件名 */}
      <span className="text-slate-300 truncate">{filename}</span>

      {/* 添加行数 */}
      <span className="text-green-400 text-xs flex-shrink-0">+{additions}</span>

      {/* 操作按钮 */}
      <div className="ml-auto flex items-center gap-1">
        {accepted ? (
          <span className="flex items-center justify-center w-[22px] h-[22px] rounded bg-emerald-500/20 text-emerald-400">
            <Check className="h-3 w-3" />
          </span>
        ) : (
          <>
            <button className="flex items-center justify-center w-[22px] h-[22px] rounded hover:bg-slate-700 text-slate-400">
              <Check className="h-3 w-3" />
            </button>
            <button className="flex items-center justify-center w-[22px] h-[22px] rounded hover:bg-slate-700 text-slate-400">
              <X className="h-3 w-3" />
            </button>
          </>
        )}
      </div>
    </div>
  );
}
