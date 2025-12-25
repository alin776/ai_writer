import { useState, useEffect } from 'react';
import { X, Crown, UserX, Search, Edit2, Volume2, VolumeX } from 'lucide-react';
import { getChannelMembers, kickMember, muteMember, unmuteMember, channelApi, type ChannelMember } from '@/services/channelApi';
import { useToast } from '@/hooks/useToast';
import { Avatar } from '@/components/ui/avatar';

interface MemberManagementDialogProps {
  isOpen: boolean;
  onClose: () => void;
  channelId: string;
  channelName: string;
  currentUserId: string;
  isCreator: boolean;
}

interface EditTitleDialogProps {
  isOpen: boolean;
  onClose: () => void;
  member: ChannelMember;
  channelId: string;
  onSave: (customTitle: string | null, titleColor: string) => void;
}

interface MuteDurationDialogProps {
  isOpen: boolean;
  onClose: () => void;
  member: ChannelMember;
  onConfirm: (durationMinutes: number) => void;
}

function EditTitleDialog({ isOpen, onClose, member, channelId, onSave }: EditTitleDialogProps) {
  const [title, setTitle] = useState(member.customTitle || '');
  const [color, setColor] = useState(member.titleColor || '#FF6B6B');

  const handleSave = () => {
    onSave(title.trim() || null, color);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 dark:bg-black/70 flex items-center justify-center z-[60]" onClick={onClose}>
      <div className="bg-white dark:bg-zinc-900 rounded-lg shadow-xl w-full max-w-sm p-4" onClick={e => e.stopPropagation()}>
        <h4 className="text-sm font-medium mb-3 text-gray-900 dark:text-gray-100">编辑头衔 - {member.username}</h4>

        <div className="space-y-3">
          <div>
            <label className="text-xs text-gray-600 dark:text-gray-400 mb-1 block">头衔文字</label>
            <input
              type="text"
              placeholder="输入头衔（留空则清除）"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              maxLength={50}
              className="w-full px-3 py-2 text-sm border border-gray-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 rounded focus:outline-none focus:border-blue-400 dark:focus:border-blue-500"
            />
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">{title.length}/50</p>
          </div>

          <div>
            <label className="text-xs text-gray-600 dark:text-gray-400 mb-1 block">头衔颜色</label>
            <div className="flex items-center gap-2">
              <input
                type="color"
                value={color}
                onChange={(e) => setColor(e.target.value)}
                className="w-12 h-9 rounded cursor-pointer border border-gray-200 dark:border-zinc-700"
              />
              <input
                type="text"
                value={color}
                onChange={(e) => setColor(e.target.value)}
                placeholder="#FF6B6B"
                className="flex-1 px-3 py-2 text-sm border border-gray-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 rounded focus:outline-none focus:border-blue-400 dark:focus:border-blue-500"
              />
            </div>
          </div>

          {title && (
            <div>
              <label className="text-xs text-gray-600 dark:text-gray-400 mb-1 block">预览效果</label>
              <div className="p-2 bg-gray-50 dark:bg-zinc-800 rounded">
                <span
                  className="text-xs px-2 py-1 rounded inline-block"
                  style={{
                    backgroundColor: `${color}20`,
                    color: color
                  }}
                >
                  {title}
                </span>
              </div>
            </div>
          )}
        </div>

        <div className="flex gap-2 mt-4">
          <button
            onClick={onClose}
            className="flex-1 px-3 py-2 text-sm bg-gray-100 dark:bg-zinc-800 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-zinc-700 transition-colors"
          >
            取消
          </button>
          <button
            onClick={handleSave}
            className="flex-1 px-3 py-2 text-sm bg-blue-500 dark:bg-blue-600 text-white rounded hover:bg-blue-600 dark:hover:bg-blue-700 transition-colors"
          >
            保存
          </button>
        </div>
      </div>
    </div>
  );
}

function MuteDurationDialog({ isOpen, onClose, member, onConfirm }: MuteDurationDialogProps) {
  const [customDuration, setCustomDuration] = useState('');
  const [useCustom, setUseCustom] = useState(false);

  const presetDurations = [
    { label: '1小时', minutes: 60 },
    { label: '6小时', minutes: 360 },
    { label: '1天', minutes: 1440 },
    { label: '7天', minutes: 10080 },
    { label: '30天', minutes: 43200 },
  ];

  const handlePresetClick = (minutes: number) => {
    onConfirm(minutes);
    onClose();
  };

  const handleCustomConfirm = () => {
    const minutes = parseInt(customDuration);
    if (isNaN(minutes) || minutes < 1) {
      return;
    }
    onConfirm(minutes);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 dark:bg-black/70 flex items-center justify-center z-[60]" onClick={onClose}>
      <div className="bg-white dark:bg-zinc-900 rounded-lg shadow-xl w-full max-w-sm p-4" onClick={e => e.stopPropagation()}>
        <h4 className="text-sm font-medium mb-3 text-gray-900 dark:text-gray-100">禁言 - {member.username}</h4>

        {!useCustom ? (
          <div className="space-y-2">
            <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">选择禁言时长:</p>
            {presetDurations.map((duration) => (
              <button
                key={duration.minutes}
                onClick={() => handlePresetClick(duration.minutes)}
                className="w-full px-4 py-2.5 text-sm bg-gray-50 dark:bg-zinc-800 text-gray-900 dark:text-gray-100 rounded hover:bg-orange-50 dark:hover:bg-orange-900/30 hover:border-orange-400 dark:hover:border-orange-500 border border-gray-200 dark:border-zinc-700 transition-colors"
              >
                {duration.label}
              </button>
            ))}
            <button
              onClick={() => setUseCustom(true)}
              className="w-full px-4 py-2.5 text-sm bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded hover:bg-blue-100 dark:hover:bg-blue-900/50 border border-blue-200 dark:border-blue-800 transition-colors"
            >
              自定义时长
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <div>
              <label className="text-xs text-gray-600 dark:text-gray-400 mb-1 block">禁言时长（分钟）</label>
              <input
                type="number"
                placeholder="输入分钟数"
                value={customDuration}
                onChange={(e) => setCustomDuration(e.target.value)}
                min="1"
                className="w-full px-3 py-2 text-sm border border-gray-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 rounded focus:outline-none focus:border-blue-400 dark:focus:border-blue-500"
                autoFocus
              />
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => { setUseCustom(false); setCustomDuration(''); }}
                className="flex-1 px-3 py-2 text-sm bg-gray-100 dark:bg-zinc-800 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-zinc-700 transition-colors"
              >
                返回
              </button>
              <button
                onClick={handleCustomConfirm}
                disabled={!customDuration || parseInt(customDuration) < 1}
                className="flex-1 px-3 py-2 text-sm bg-orange-500 dark:bg-orange-600 text-white rounded hover:bg-orange-600 dark:hover:bg-orange-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                确认
              </button>
            </div>
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full mt-3 px-3 py-2 text-sm bg-gray-100 dark:bg-zinc-800 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-zinc-700 transition-colors"
        >
          取消
        </button>
      </div>
    </div>
  );
}

export function MemberManagementDialog({
  isOpen,
  onClose,
  channelId,
  channelName,
  currentUserId,
  isCreator,
}: MemberManagementDialogProps) {
  const { showToast } = useToast();
  const [members, setMembers] = useState<ChannelMember[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [editingMember, setEditingMember] = useState<ChannelMember | null>(null);
  const [mutingMember, setMutingMember] = useState<ChannelMember | null>(null);

  useEffect(() => {
    if (isOpen) {
      loadMembers();
    }
  }, [isOpen, channelId]);

  const loadMembers = async () => {
    try {
      setLoading(true);
      const response = await getChannelMembers(channelId);
      setMembers(response.members);
    } catch (error) {
      console.error('加载成员列表失败:', error);
      showToast('error', '加载成员列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleKick = async (userId: string, username: string) => {
    if (!confirm(`确定要踢出 ${username} 吗？`)) {
      return;
    }

    try {
      await kickMember(channelId, userId);
      showToast('success', `已踢出 ${username}`);
      setMembers(prev => prev.filter(m => m.userId !== userId));
    } catch (error) {
      console.error('踢出成员失败:', error);
      showToast('error', '踢出成员失败');
    }
  };

  const handleSaveTitle = async (customTitle: string | null, titleColor: string) => {
    if (!editingMember) return;

    try {
      const response = await channelApi.updateMemberTitle(channelId, editingMember.userId, {
        customTitle,
        titleColor,
      });

      showToast('success', '头衔已更新');

      setMembers(prev => prev.map(m =>
        m.userId === editingMember.userId
          ? { ...m, customTitle: response.customTitle, titleColor: response.titleColor }
          : m
      ));

      setEditingMember(null);
    } catch (error) {
      console.error('更新头衔失败:', error);
      showToast('error', '更新头衔失败');
    }
  };

  const handleMuteConfirm = async (durationMinutes: number) => {
    if (!mutingMember) return;

    try {
      await muteMember(channelId, mutingMember.userId, durationMinutes);
      showToast('success', `已禁言 ${mutingMember.username}`);
      await loadMembers(); // 重新加载成员列表
      setMutingMember(null);
    } catch (error) {
      console.error('禁言失败:', error);
      showToast('error', '禁言失败');
    }
  };

  const handleUnmute = async (userId: string, username: string) => {
    try {
      await unmuteMember(channelId, userId);
      showToast('success', `已解除 ${username} 的禁言`);
      await loadMembers(); // 重新加载成员列表
    } catch (error) {
      console.error('解除禁言失败:', error);
      showToast('error', '解除禁言失败');
    }
  };

  const getRoleName = (role: string) => {
    switch (role) {
      case 'owner':
        return '创建者';
      case 'admin':
        return '管理员';
      default:
        return '成员';
    }
  };

  // 计算禁言剩余时间
  const getMuteTimeRemaining = (mutedUntil?: string | null) => {
    if (!mutedUntil) return null;

    const now = new Date();
    const muteEnd = new Date(mutedUntil);
    const diff = muteEnd.getTime() - now.getTime();

    if (diff <= 0) return null; // 禁言已过期

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

    if (days > 0) return `${days}天${hours}小时`;
    if (hours > 0) return `${hours}小时${minutes}分钟`;
    return `${minutes}分钟`;
  };

  const filteredMembers = members.filter(member =>
    member.username.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 bg-black/50 dark:bg-black/70 flex items-center justify-center z-50">
        <div className="bg-white dark:bg-zinc-900 rounded-lg shadow-xl w-full max-w-2xl max-h-[80vh] flex flex-col">
          {/* 标题栏 */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-zinc-800">
            <div>
              <h3 className="text-base font-medium text-gray-900 dark:text-gray-100">成员管理</h3>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{channelName}</p>
            </div>
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 dark:hover:bg-zinc-800 rounded transition-colors"
            >
              <X className="w-4 h-4 text-gray-600 dark:text-gray-400" />
            </button>
          </div>

          {/* 搜索框 */}
          <div className="p-4 border-b border-gray-200 dark:border-zinc-800">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 dark:text-gray-500" />
              <input
                type="text"
                placeholder="搜索成员..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 rounded focus:outline-none focus:border-gray-300 dark:focus:border-zinc-600"
              />
            </div>
          </div>

          {/* 成员列表 */}
          <div className="flex-1 overflow-y-auto p-4">
            {loading ? (
              <div className="text-center py-8 text-sm text-gray-500 dark:text-gray-400">
                加载中...
              </div>
            ) : filteredMembers.length === 0 ? (
              <div className="text-center py-8 text-sm text-gray-500 dark:text-gray-400">
                {searchQuery ? '未找到匹配的成员' : '暂无成员'}
              </div>
            ) : (
              <div className="space-y-2">
                {filteredMembers.map((member) => (
                  <div
                    key={member.id}
                    className="flex items-center gap-3 p-3 hover:bg-gray-50 dark:hover:bg-zinc-800 rounded border border-transparent hover:border-gray-200 dark:hover:border-zinc-700 transition-all"
                  >
                    {/* 头像 */}
                    <Avatar className="w-10 h-10 flex-shrink-0">
                      {member.avatar ? (
                        <img src={member.avatar} alt={member.username} />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white text-sm">
                          {member.username[0]?.toUpperCase() || 'U'}
                        </div>
                      )}
                    </Avatar>

                    {/* 用户信息 */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-0.5">
                        <span className="text-sm font-medium truncate text-gray-900 dark:text-gray-100">
                          {member.username}
                        </span>
                        {member.role === 'owner' && (
                          <Crown className="w-4 h-4 text-yellow-500 dark:text-yellow-400 flex-shrink-0" />
                        )}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {getRoleName(member.role)}
                        {member.isMuted && getMuteTimeRemaining(member.mutedUntil) && (
                          <span className="ml-2 text-orange-600 dark:text-orange-400">
                            · 禁言中（剩余 {getMuteTimeRemaining(member.mutedUntil)}）
                          </span>
                        )}
                      </div>
                    </div>

                    {/* 头衔显示 */}
                    <div className="flex items-center gap-2 flex-shrink-0">
                      {member.customTitle ? (
                        <span
                          className="text-xs px-2 py-1 rounded"
                          style={{
                            backgroundColor: `${member.titleColor}20`,
                            color: member.titleColor
                          }}
                        >
                          {member.customTitle}
                        </span>
                      ) : (
                        <span className="text-xs text-gray-400 dark:text-gray-500">无头衔</span>
                      )}

                      {/* 编辑按钮 */}
                      {isCreator && (
                        <button
                          onClick={() => setEditingMember(member)}
                          className="p-1.5 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded text-blue-600 dark:text-blue-400 transition-colors"
                          title="编辑头衔"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                      )}

                      {/* 禁言/解禁按钮 */}
                      {isCreator && member.userId !== currentUserId && member.role !== 'owner' && (
                        member.isMuted ? (
                          <button
                            onClick={() => handleUnmute(member.userId, member.username)}
                            className="p-1.5 hover:bg-green-50 dark:hover:bg-green-900/30 rounded text-green-600 dark:text-green-400 transition-colors"
                            title="解除禁言"
                          >
                            <Volume2 className="w-4 h-4" />
                          </button>
                        ) : (
                          <button
                            onClick={() => setMutingMember(member)}
                            className="p-1.5 hover:bg-orange-50 dark:hover:bg-orange-900/30 rounded text-orange-600 dark:text-orange-400 transition-colors"
                            title="禁言"
                          >
                            <VolumeX className="w-4 h-4" />
                          </button>
                        )
                      )}

                      {/* 踢出按钮 */}
                      {isCreator && member.userId !== currentUserId && member.role !== 'owner' && (
                        <button
                          onClick={() => handleKick(member.userId, member.username)}
                          className="p-1.5 hover:bg-red-50 dark:hover:bg-red-900/30 rounded text-red-600 dark:text-red-400 transition-colors"
                          title="踢出成员"
                        >
                          <UserX className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* 底部统计 */}
          <div className="p-4 border-t border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-800/50">
            <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
              共 {members.length} 名成员
              {searchQuery && ` · 显示 ${filteredMembers.length} 个结果`}
            </p>
          </div>
        </div>
      </div>

      {/* 编辑头衔对话框 */}
      {editingMember && (
        <EditTitleDialog
          isOpen={!!editingMember}
          onClose={() => setEditingMember(null)}
          member={editingMember}
          channelId={channelId}
          onSave={handleSaveTitle}
        />
      )}

      {/* 禁言时长对话框 */}
      {mutingMember && (
        <MuteDurationDialog
          isOpen={!!mutingMember}
          onClose={() => setMutingMember(null)}
          member={mutingMember}
          onConfirm={handleMuteConfirm}
        />
      )}
    </>
  );
}
