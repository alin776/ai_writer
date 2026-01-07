/**
 * KnowledgeContainer - 知识调取容器组件
 * 圆角胶囊样式，可展开/收起
 */

import { useState } from 'react';
import { BookOpen, FileText, Search, ChevronUp, ChevronDown } from 'lucide-react';
import type { KnowledgeFlowData } from '@/types/agent';

const ICON_MAP: Record<string, React.ComponentType<any>> = {
  BookOpen,
  FileText,
  Search,
};

interface KnowledgeContainerProps extends KnowledgeFlowData {
  defaultExpanded?: boolean;
}

export function KnowledgeContainer({
  title,
  icon,
  items,
  defaultExpanded = true
}: KnowledgeContainerProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const IconComponent = ICON_MAP[icon] || BookOpen;

  return (
    <div className="inline-block bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl px-3 py-2 mb-2">
      {/* 头部 */}
      <div
        className="flex items-center gap-1.5 cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        <span className="text-gray-500">
          <IconComponent size={12} />
        </span>
        <span className="text-[13px] text-gray-500">{title}</span>
        <span className="text-gray-400 dark:text-gray-600 text-[9px] ml-0.5">
          {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
        </span>
      </div>

      {/* 知识项列表 */}
      {expanded && items.length > 0 && (
        <div className="pt-1.5">
          {items.map((item, index) => (
            <a
              key={index}
              className="block py-[3px] text-[13px] text-blue-500 dark:text-[#5c9eff] cursor-pointer underline underline-offset-2 hover:text-blue-600 dark:hover:text-[#7cb3ff]"
            >
              {item.name}
              {item.similarity !== undefined && (
                <span className="text-gray-500 text-[11px] ml-1 no-underline">
                  (相似度: {item.similarity.toFixed(2)})
                </span>
              )}
              {item.tag && (
                <span className="inline-block text-[10px] px-1 py-0.5 bg-gray-100 dark:bg-slate-700 text-gray-500 dark:text-slate-400 rounded ml-1.5 no-underline">
                  {item.tag}
                </span>
              )}
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
