/**
 * ReflectCard for agent reflection output.
 */

import type { ReflectFlowData } from '@/types/agent';

interface ReflectCardProps extends ReflectFlowData {}

export function ReflectCard({ summary, nextAction, stopReason }: ReflectCardProps) {
  return (
    <div className="mb-3 ml-[26px] text-[13px] text-gray-600 dark:text-slate-300 leading-[1.6]">
      <div className="font-medium text-gray-700 dark:text-slate-200 mb-1">Reflect</div>
      <div>{summary}</div>
      {nextAction && <div className="mt-1">Next: {nextAction}</div>}
      {stopReason && <div className="mt-1 text-gray-500">Stop reason: {stopReason}</div>}
    </div>
  );
}


