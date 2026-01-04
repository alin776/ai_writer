import { useState } from 'react';
import { Plus, Minus, ChevronRight, ChevronDown, X, Edit2 } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import type { ChannelMember } from '@/services/channelApi';
import type { Channel } from './ChannelList';
import ConfirmDialog from '@/components/common/ConfirmDialog';

interface ChannelSettingsPanelProps {
  channel: Channel;
  members: ChannelMember[];
  currentUser: {
    id: string;
    name: string;
    avatar?: string;
    isCreator?: boolean;
    role?: 'owner' | 'admin' | 'member';
  };
  isMuted?: boolean;  // 静音状态
  onToggleMute?: () => void;  // 切换静音
  onClose: () => void;
  onSearchChat: () => void;
  onManageMembers: () => void;
  onAddMember?: () => void;
  onRemoveMember?: () => void;
  onClearHistory?: () => void;
  onDissolveChannel?: () => void;
  onLeaveChannel?: () => void;
  onMemberClick?: (member: ChannelMember, event: React.MouseEvent) => void;
  onViewMoreMembers?: () => void;
  onEditAnnouncement?: () => void;
  onEditChannelName?: () => void;
  announcement?: {
    content: string;
    authorName?: string;
    authorAvatar?: string;
    updatedAt?: string;
  };
}

export function ChannelSettingsPanel({
  channel,
  members,
  currentUser,
  isMuted = false,
  onToggleMute,
  onClose,
  onSearchChat,
  onManageMembers,
  onAddMember,
  onRemoveMember,
  onClearHistory,
  onDissolveChannel,
  onLeaveChannel,
  onMemberClick,
  onViewMoreMembers,
  onEditAnnouncement,
  onEditChannelName,
  announcement,
}: ChannelSettingsPanelProps) {
  const [showDissolveConfirm, setShowDissolveConfirm] = useState(false);
  const [showLeaveConfirm, setShowLeaveConfirm] = useState(false);
  const [showAnnouncementDetail, setShowAnnouncementDetail] = useState(false);

  // 是否是群主或管理员
  const isOwnerOrAdmin = currentUser.role === 'owner' || currentUser.role === 'admin';
  const isOwner = currentUser.role === 'owner';

  // 官方频道的管理员也有管理权限
  const canManageChannel = isOwner || (channel.type === 'official' && currentUser.role === 'admin');

  // 显示前6个成员
  const visibleMembers = members.slice(0, 6);
  const hasMoreMembers = members.length > 6;

  return (
    <div className="w-60 bg-white dark:bg-gray-900 flex flex-col h-full overflow-hidden relative border-l border-gray-200 dark:border-gray-700">
      {/* 可滚动内容区域 */}
      <div className="flex-1 overflow-y-auto">
        {/* 成员网格 */}
        <div className="px-3 py-3 bg-white dark:bg-gray-900">
          <div className="grid grid-cols-4 gap-2">
            {visibleMembers.map((member) => (
              <div
                key={member.id}
                className="flex flex-col items-center gap-1 cursor-pointer"
                onClick={(e) => onMemberClick?.(member, e)}
              >
                <Avatar className="w-8 h-8 rounded-full">
                  <AvatarImage src={member.avatar} alt={member.username} />
                  <AvatarFallback className="rounded-full bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-white text-[10px]">
                    {member.username?.[0]?.toUpperCase() || 'U'}
                  </AvatarFallback>
                </Avatar>
                <span className="text-[11px] text-gray-500 dark:text-gray-400 w-full text-center truncate">
                  {member.fullName || member.username}
                </span>
              </div>
            ))}

            {/* 添加成员按钮 */}
            {onAddMember && (
              <div
                className="flex flex-col items-center gap-1 cursor-pointer"
                onClick={onAddMember}
              >
                <div className="w-8 h-8 rounded-full border-2 border-dashed border-gray-400 dark:border-gray-500 flex items-center justify-center hover:border-gray-500 dark:hover:border-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                  <Plus className="w-4 h-4 text-gray-500 dark:text-gray-400" />
                </div>
                <span className="text-[10px] text-gray-500 dark:text-gray-400">添加</span>
              </div>
            )}

            {/* 移出成员按钮 - 管理员可见 */}
            {isOwnerOrAdmin && onRemoveMember && (
              <div
                className="flex flex-col items-center gap-1 cursor-pointer"
                onClick={onRemoveMember}
              >
                <div className="w-8 h-8 rounded-full border-2 border-dashed border-gray-400 dark:border-gray-500 flex items-center justify-center hover:border-gray-500 dark:hover:border-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                  <Minus className="w-4 h-4 text-gray-500 dark:text-gray-400" />
                </div>
                <span className="text-[10px] text-gray-500 dark:text-gray-400">移出</span>
              </div>
            )}
          </div>

          {/* 查看更多按钮 */}
          {hasMoreMembers && onViewMoreMembers && (
            <button
              onClick={onViewMoreMembers}
              className="w-full mt-2 py-1.5 flex items-center justify-center gap-1 text-[11px] text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
            >
              <span>查看更多</span>
              <ChevronDown className="w-3 h-3" />
            </button>
          )}
        </div>

        {/* 分隔线 */}
        <div className="h-px bg-gray-200 dark:bg-gray-700" />

        {/* 群聊信息 */}
        <div className="px-2 py-2 bg-white dark:bg-gray-900">
          {/* 群聊名称 */}
          <div
            className={cn(
              "py-3 px-2 rounded-lg",
              canManageChannel && onEditChannelName && "cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700/80 transition-colors"
            )}
            onClick={() => canManageChannel && onEditChannelName?.()}
          >
            <div className="flex items-center justify-between">
              <div className="text-sm font-medium text-gray-900 dark:text-gray-200">群聊名称</div>
              {canManageChannel && onEditChannelName && (
                <ChevronRight className="w-4 h-4 text-gray-400 dark:text-gray-500" />
              )}
            </div>
            <div className="text-[13px] text-gray-500 dark:text-gray-400 mt-1">{channel.name}</div>
          </div>

          {/* 群公告 */}
          <div
            className="py-3 px-2 rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700/80 transition-colors"
            onClick={() => setShowAnnouncementDetail(true)}
          >
            <div className="flex items-center justify-between">
              <div className="text-sm font-medium text-gray-900 dark:text-gray-200">群公告</div>
              <ChevronRight className="w-4 h-4 text-gray-400 dark:text-gray-500" />
            </div>
            <div className="text-[13px] text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">
              {announcement?.content || channel.description || '暂无公告，点击查看'}
            </div>
          </div>
        </div>

        {/* 分隔线 */}
        <div className="h-px bg-gray-200 dark:bg-gray-700" />

        {/* 查找聊天内容 */}
        <div className="px-2 py-2 bg-white dark:bg-gray-900">
          <button
            onClick={onSearchChat}
            className="w-full px-3 py-3 flex items-center justify-between text-sm font-medium text-gray-900 dark:text-gray-200 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-xl transition-colors"
          >
            <span>查找聊天内容</span>
            <ChevronRight className="w-4 h-4 text-gray-400 dark:text-gray-500" />
          </button>
        </div>

        {/* 分隔线 */}
        <div className="h-px bg-gray-200 dark:bg-gray-700" />

        {/* 频道静音 */}
        <div className="px-2 py-2 bg-white dark:bg-gray-900">
          <div className="py-3 px-2 flex items-center justify-between rounded-lg">
            <span className="text-sm font-medium text-gray-900 dark:text-gray-200">消息免打扰</span>
            <button
              onClick={onToggleMute}
              className={cn(
                "relative w-10 h-[22px] rounded-full transition-colors",
                isMuted ? "bg-[#07c160]" : "bg-gray-300 dark:bg-gray-600"
              )}
            >
              <span
                className={cn(
                  "absolute top-0.5 left-0.5 w-[18px] h-[18px] bg-white rounded-full shadow transition-transform",
                  isMuted && "translate-x-[18px]"
                )}
              />
            </button>
          </div>
        </div>

        {/* 分隔线 */}
        <div className="h-px bg-gray-200 dark:bg-gray-700" />

        {/* 管理成员 - 管理员可见 */}
        {isOwnerOrAdmin && (
          <>
            <div className="px-2 py-2 bg-white dark:bg-gray-900">
              <button
                onClick={onManageMembers}
                className="w-full px-2 py-3 flex items-center justify-between text-sm font-medium text-gray-900 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700/80 rounded-lg transition-colors"
              >
                <span>管理成员</span>
                <ChevronRight className="w-4 h-4 text-gray-400 dark:text-gray-500" />
              </button>
            </div>
            <div className="h-px bg-gray-200 dark:bg-gray-700" />
          </>
        )}

        {/* 底部操作按钮 */}
        <div className="p-4 space-y-2.5 bg-white dark:bg-gray-900">
          {/* 清空聊天记录 */}
          {onClearHistory && (
            <button
              onClick={onClearHistory}
              className="w-full py-3 text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              清空聊天记录
            </button>
          )}

          {/* 解散频道 - 群主可见，官方频道管理员也可见 */}
          {canManageChannel && onDissolveChannel && (
            <button
              onClick={() => setShowDissolveConfirm(true)}
              className="w-full py-3 text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-lg transition-colors"
            >
              解散频道
            </button>
          )}

          {/* 退出频道 - 非管理者可见（官方频道除外） */}
          {!canManageChannel && onLeaveChannel && channel.type !== 'official' && (
            <button
              onClick={() => setShowLeaveConfirm(true)}
              className="w-full py-3 text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-lg transition-colors"
            >
              退出频道
            </button>
          )}

          {/* 官方频道提示 - 仅对非管理者显示 */}
          {channel.type === 'official' && !canManageChannel && (
            <p className="text-center text-xs text-gray-400 dark:text-gray-500 py-2">
              官方频道无法退出
            </p>
          )}
        </div>
      </div>

      {/* 解散频道确认弹窗 */}
      <ConfirmDialog
        isOpen={showDissolveConfirm}
        title="解散频道"
        message={`确定要解散「${channel.name}」吗？解散后所有聊天记录将被删除，此操作不可恢复。`}
        confirmText="解散"
        cancelText="取消"
        variant="danger"
        onConfirm={() => {
          setShowDissolveConfirm(false);
          onDissolveChannel?.();
        }}
        onCancel={() => setShowDissolveConfirm(false)}
      />

      {/* 退出频道确认弹窗 */}
      <ConfirmDialog
        isOpen={showLeaveConfirm}
        title="退出频道"
        message={`确定要退出「${channel.name}」吗？退出后将无法查看频道内的聊天记录。`}
        confirmText="退出"
        cancelText="取消"
        variant="danger"
        onConfirm={() => {
          setShowLeaveConfirm(false);
          onLeaveChannel?.();
        }}
        onCancel={() => setShowLeaveConfirm(false)}
      />

      {/* 群公告详情弹窗 */}
      {showAnnouncementDetail && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
          onClick={() => setShowAnnouncementDetail(false)}
        >
          <div
            className="bg-white dark:bg-gray-900 rounded-lg shadow-xl w-full max-w-md mx-4 h-[400px] flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            {/* 弹窗头部 */}
            <div className="flex-shrink-0 flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-base font-medium text-gray-900 dark:text-gray-100">
                「{channel.name}」的群公告
              </h3>
              <button
                onClick={() => setShowAnnouncementDetail(false)}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>

            {/* 弹窗内容 */}
            <div className="flex-1 overflow-y-auto p-4">
              {(announcement?.content || channel.description) ? (
                <>
                  {/* 发布者信息 */}
                  {announcement?.authorName && (
                    <div className="flex items-center gap-3 mb-4">
                      <Avatar className="w-10 h-10">
                        <AvatarImage src={announcement.authorAvatar} />
                        <AvatarFallback className="bg-gradient-to-br from-blue-400 to-purple-500 text-white text-sm">
                          {announcement.authorName?.[0]?.toUpperCase() || 'U'}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {announcement.authorName}
                        </div>
                        {announcement.updatedAt && (
                          <div className="text-xs text-gray-500 dark:text-gray-400">
                            {announcement.updatedAt}
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* 公告内容 */}
                  <div className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">
                    {announcement?.content || channel.description}
                  </div>
                </>
              ) : (
                <div className="text-center text-gray-500 dark:text-gray-400 py-8">
                  暂无公告
                </div>
              )}
            </div>

            {/* 弹窗底部 */}
            <div className="flex-shrink-0 px-4 py-3 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <span className="text-xs text-gray-400 dark:text-gray-500">
                {channel.type === 'official' ? '仅群主和管理员可编辑' : '仅群主可编辑'}
              </span>
              {canManageChannel && onEditAnnouncement && (
                <button
                  onClick={() => {
                    setShowAnnouncementDetail(false);
                    onEditAnnouncement();
                  }}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded transition-colors"
                >
                  <Edit2 className="w-4 h-4" />
                  <span>编辑</span>
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
