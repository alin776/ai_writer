/**
 * CompletionStatus - 完成状态组件
 * 显示绿色勾选图标 + "任务已完成"
 */

import { CheckCircle } from 'lucide-react';

interface CompletionStatusProps {
  text?: string;
}

export function CompletionStatus({
  text = '任务已完成'
}: CompletionStatusProps) {
  return (
    <div className="flex items-center gap-1.5 mt-4 first:mt-0 text-emerald-600 dark:text-[#10b981] text-[13px]">
      <CheckCircle size={14} />
      <span>{text}</span>
    </div>
  );
}
