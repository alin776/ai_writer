/**
 * AgentHeader - Agent头部组件
 * 显示Logo、名称、标签
 */

interface AgentHeaderProps {
  name?: string;
  badge?: string;
}

export function AgentHeader({
  name = '文枢AI',
  badge
}: AgentHeaderProps) {
  return (
    <div className="flex items-center gap-2 mb-3">
      {/* Logo */}
      <img
        src="/logo-icon.svg"
        alt="文枢AI"
        className="w-[22px] h-[22px] dark:invert"
      />
      {/* 名称 */}
      <span className="text-[15px] font-semibold text-gray-900 dark:text-white">{name}</span>
      {/* 标签 */}
      {badge && (
        <span className="text-[10px] px-[5px] py-[1px] bg-white dark:bg-slate-800 text-gray-500 dark:text-slate-400 rounded-[3px] border border-gray-200 dark:border-slate-700">
          {badge}
        </span>
      )}
    </div>
  );
}
