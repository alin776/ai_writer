import { useMemo, useState } from 'react';
import { Search } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import type { ChannelMember } from '@/services/channelApi';

interface MemberListPanelProps {
  members: ChannelMember[];
  onMemberClick?: (member: ChannelMember, event: React.MouseEvent) => void;
}

export function MemberListPanel({ members, onMemberClick }: MemberListPanelProps) {
  const [searchQuery, setSearchQuery] = useState('');

  // 过滤成员
  const filteredMembers = useMemo(() => {
    if (!searchQuery.trim()) return members;
    const query = searchQuery.toLowerCase();
    return members.filter(member =>
      member.username.toLowerCase().includes(query) ||
      member.fullName?.toLowerCase().includes(query)
    );
  }, [members, searchQuery]);

  // 按角色分组成员
  const groupedMembers = useMemo(() => {
    const owners: ChannelMember[] = [];
    const admins: ChannelMember[] = [];
    const onlineMembers: ChannelMember[] = [];
    const offlineMembers: ChannelMember[] = [];

    filteredMembers.forEach(member => {
      if (member.role === 'owner') {
        owners.push(member);
      } else if (member.role === 'admin') {
        admins.push(member);
      } else {
        // 暂时将所有普通成员放入在线分组
        // 后续可根据 onlineStatus 字段分离
        onlineMembers.push(member);
      }
    });

    return { owners, admins, onlineMembers, offlineMembers };
  }, [filteredMembers]);

  const renderMember = (member: ChannelMember, isSpecialRole: boolean = false) => (
    <div
      key={member.id}
      onClick={(e) => onMemberClick?.(member, e)}
      className="flex items-center gap-3 px-2 py-1.5 rounded-md cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors"
    >
      {/* 头像容器 - 包含状态指示器 */}
      <div className="relative flex-shrink-0">
        <Avatar className="w-8 h-8">
          <AvatarImage src={member.avatar} alt={member.username} />
          <AvatarFallback className="bg-gradient-to-br from-blue-400 to-purple-500 text-white text-xs">
            {member.username?.[0]?.toUpperCase() || 'U'}
          </AvatarFallback>
        </Avatar>
        {/* 在线状态指示器 */}
        <div
          className={cn(
            "absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full border-2 border-gray-50 dark:border-gray-800",
            member.onlineStatus === 'online' && "bg-green-500",
            member.onlineStatus === 'idle' && "bg-yellow-500",
            member.onlineStatus === 'dnd' && "bg-red-500",
            (!member.onlineStatus || member.onlineStatus === 'offline') && "bg-gray-400"
          )}
        />
      </div>
      <div className="flex-1 min-w-0 overflow-hidden">
        <div className="flex items-center gap-1.5 flex-wrap">
          <span
            className={cn(
              "text-sm font-medium truncate",
              isSpecialRole ? "text-green-600 dark:text-green-400" : "text-gray-800 dark:text-gray-200"
            )}
          >
            {member.fullName || member.username}
          </span>
          {/* 称号徽章 */}
          {member.title && (
            <span
              className="text-[10px] font-semibold px-1.5 py-0.5 rounded"
              style={{
                backgroundColor: member.titleColor || '#5865f2',
                color: '#fff'
              }}
            >
              {member.title}
            </span>
          )}
        </div>
        {/* 用户简介/状态 */}
        {member.bio && (
          <p className="text-xs text-gray-500 dark:text-gray-400 truncate mt-0.5">
            {member.bio}
          </p>
        )}
      </div>
    </div>
  );

  const renderGroup = (title: string, count: number, memberList: ChannelMember[], isSpecialRole: boolean = false) => {
    if (memberList.length === 0) return null;

    return (
      <div className="mb-2">
        <div className="px-2 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
          {title} — {count}
        </div>
        <div className="space-y-0.5">
          {memberList.map(member => renderMember(member, isSpecialRole))}
        </div>
      </div>
    );
  };

  return (
    <div className="w-60 bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-700 flex flex-col h-full">
      {/* 搜索框 */}
      <div className="p-2 flex-shrink-0">
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="搜索成员"
            className="w-full pl-3 pr-8 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 border-0 rounded-md outline-none focus:ring-1 focus:ring-blue-400 dark:focus:ring-blue-500 text-gray-800 dark:text-gray-200 placeholder-gray-400 dark:placeholder-gray-500"
          />
          <Search className="absolute right-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        </div>
      </div>

      {/* 成员列表 */}
      <div className="flex-1 overflow-y-auto p-2 pt-0">
        {/* 群主分组 */}
        {renderGroup('群主', groupedMembers.owners.length, groupedMembers.owners, true)}

        {/* 管理员分组 */}
        {renderGroup('管理员', groupedMembers.admins.length, groupedMembers.admins, true)}

        {/* 在线成员分组 */}
        {renderGroup('在线', groupedMembers.onlineMembers.length, groupedMembers.onlineMembers, false)}

        {/* 离线成员分组 */}
        {groupedMembers.offlineMembers.length > 0 && (
          <div className="mb-2 opacity-60">
            <div className="px-2 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
              离线 — {groupedMembers.offlineMembers.length}
            </div>
            <div className="space-y-0.5">
              {groupedMembers.offlineMembers.map(member => renderMember(member, false))}
            </div>
          </div>
        )}

        {/* 空状态 */}
        {filteredMembers.length === 0 && (
          <div className="flex items-center justify-center h-32 text-sm text-gray-400 dark:text-gray-500">
            {searchQuery ? '未找到匹配成员' : '暂无成员'}
          </div>
        )}
      </div>
    </div>
  );
}
