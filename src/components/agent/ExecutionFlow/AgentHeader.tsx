/**
 * AgentHeader - Agent头部组件
 * 显示Logo、名称
 */

interface AgentHeaderProps {
  name?: string;
}

export function AgentHeader({
  name = '文枢AI',
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
    </div>
  );
}
