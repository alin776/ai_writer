import { useState, useEffect } from 'react';
import { X, Crown, UserX, VolumeX, Volume2 } from 'lucide-react';
import { getChannelMembers, kickMember, muteMember, unmuteMember, type ChannelMember } from '@/services/channelApi';
import { useToast } from '@/hooks/useToast';
import { Avatar } from '@/components/ui/avatar';

interface MemberManagementDialogProps {
  isOpen: boolean;
  onClose: () => void;
  channelId: string;
  channelName: string;
  currentUserId: string;
  isCreator: boolean;
  userRole: 'owner' | 'admin' | 'member';
}

export function MemberManagementDialog({
  isOpen,
  onClose,
  channelId,
  channelName,
  currentUserId,
  isCreator,
  userRole,
}: MemberManagementDialogProps) {
  const { showToast } = useToast();
  const [members, setMembers] = useState<ChannelMember[]>([]);
  const [loading, setLoading] = useState(false);
  const [muteTarget, setMuteTarget] = useState<{ userId: string; username: string } | null>(null);
  const [muteDuration, setMuteDuration] = useState(10); // 默认10分钟
  const [kickTarget, setKickTarget] = useState<{ userId: string; username: string } | null>(null);

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

  const handleKick = async () => {
    if (!kickTarget) return;

    try {
      await kickMember(channelId, kickTarget.userId);
      showToast('success', `已踢出 ${kickTarget.username}`);
      // 从列表中移除
      setMembers(prev => prev.filter(m => m.userId !== kickTarget.userId));
      setKickTarget(null);
    } catch (error) {
      console.error('踢出成员失败:', error);
      showToast('error', '踢出成员失败');
    }
  };

  // 禁言成员
  const handleMute = async () => {
    if (!muteTarget) return;

    try {
      await muteMember(channelId, muteTarget.userId, muteDuration);
      showToast('success', `已禁言 ${muteTarget.username} ${muteDuration} 分钟`);
      // 更新列表中的禁言状态
      setMembers(prev => prev.map(m =>
        m.userId === muteTarget.userId
          ? { ...m, isMuted: true, mutedUntil: new Date(Date.now() + muteDuration * 60000).toISOString() }
          : m
      ));
      setMuteTarget(null);
      setMuteDuration(10);
    } catch (error) {
      console.error('禁言失败:', error);
      showToast('error', '禁言失败');
    }
  };

  // 取消禁言
  const handleUnmute = async (userId: string, username: string) => {
    try {
      await unmuteMember(channelId, userId);
      showToast('success', `已取消禁言 ${username}`);
      // 更新列表中的禁言状态
      setMembers(prev => prev.map(m =>
        m.userId === userId
          ? { ...m, isMuted: false, mutedUntil: undefined }
          : m
      ));
    } catch (error) {
      console.error('取消禁言失败:', error);
      showToast('error', '取消禁言失败');
    }
  };

  // 判断当前用户是否可以管理目标成员
  const canManage = (targetRole: string) => {
    if (userRole === 'member') return false;
    if (userRole === 'owner') return targetRole !== 'owner';
    if (userRole === 'admin') return targetRole === 'member';
    return false;
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

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md max-h-[80vh] flex flex-col">
        {/* 标题栏 */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <div>
            <h3 className="text-base font-medium dark:text-gray-100">成员管理</h3>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{channelName}</p>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
          >
            <X className="w-4 h-4 dark:text-gray-400" />
          </button>
        </div>

        {/* 成员列表 */}
        <div className="flex-1 overflow-y-auto p-4">
          {loading ? (
            <div className="text-center py-8 text-sm text-gray-500 dark:text-gray-400">
              加载中...
            </div>
          ) : members.length === 0 ? (
            <div className="text-center py-8 text-sm text-gray-500 dark:text-gray-400">
              暂无成员
            </div>
          ) : (
            <div className="space-y-2">
              {members.map((member) => (
                <div
                  key={member.id}
                  className="flex items-center justify-between p-2 hover:bg-gray-50 dark:hover:bg-gray-700 rounded"
                >
                  <div className="flex items-center gap-2 flex-1">
                    <Avatar className="w-8 h-8">
                      {member.avatar ? (
                        <img src={member.avatar} alt={member.username} />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white text-xs">
                          {member.username[0]?.toUpperCase() || 'U'}
                        </div>
                      )}
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium truncate dark:text-gray-100">
                          {member.username}
                        </span>
                        {member.role === 'owner' && (
                          <Crown className="w-3.5 h-3.5 text-yellow-500 flex-shrink-0" />
                        )}
                        {member.isMuted && (
                          <span className="text-xs text-red-500 bg-red-50 dark:bg-red-900/30 px-1.5 py-0.5 rounded">
                            禁言中
                          </span>
                        )}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {getRoleName(member.role)}
                      </div>
                    </div>
                  </div>

                  {/* 操作按钮 - owner/admin 可管理 */}
                  {member.userId !== currentUserId && canManage(member.role) && (
                    <div className="flex items-center gap-1">
                      {/* 禁言/取消禁言按钮 */}
                      {member.isMuted ? (
                        <button
                          onClick={() => handleUnmute(member.userId, member.username)}
                          className="p-1.5 hover:bg-green-50 dark:hover:bg-green-900/30 rounded text-green-600 dark:text-green-400 transition-colors"
                          title="取消禁言"
                        >
                          <Volume2 className="w-4 h-4" />
                        </button>
                      ) : (
                        <button
                          onClick={() => setMuteTarget({ userId: member.userId, username: member.username })}
                          className="p-1.5 hover:bg-orange-50 dark:hover:bg-orange-900/30 rounded text-orange-600 dark:text-orange-400 transition-colors"
                          title="禁言"
                        >
                          <VolumeX className="w-4 h-4" />
                        </button>
                      )}
                      {/* 踢出按钮 */}
                      <button
                        onClick={() => setKickTarget({ userId: member.userId, username: member.username })}
                        className="p-1.5 hover:bg-red-50 dark:hover:bg-red-900/30 rounded text-red-600 dark:text-red-400 transition-colors"
                        title="踢出成员"
                      >
                        <UserX className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 底部统计 */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
            共 {members.length} 名成员
          </p>
        </div>
      </div>

      {/* 禁言时长选择弹窗 */}
      {muteTarget && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-[60]">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-4 w-72">
            <h4 className="text-sm font-medium dark:text-gray-100 mb-3">
              禁言 {muteTarget.username}
            </h4>
            <div className="space-y-2 mb-4">
              <label className="text-xs text-gray-500 dark:text-gray-400">选择时长</label>
              <select
                value={muteDuration}
                onChange={(e) => setMuteDuration(Number(e.target.value))}
                className="w-full px-3 py-2 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              >
                <option value={1}>1 分钟</option>
                <option value={5}>5 分钟</option>
                <option value={10}>10 分钟</option>
                <option value={30}>30 分钟</option>
                <option value={60}>1 小时</option>
                <option value={360}>6 小时</option>
                <option value={1440}>1 天</option>
                <option value={10080}>7 天</option>
              </select>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => { setMuteTarget(null); setMuteDuration(10); }}
                className="flex-1 px-3 py-2 text-sm border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                取消
              </button>
              <button
                onClick={handleMute}
                className="flex-1 px-3 py-2 text-sm bg-orange-600 text-white rounded-lg hover:bg-orange-700"
              >
                确认禁言
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 踢出确认弹窗 */}
      {kickTarget && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-[60]">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-4 w-72">
            <h4 className="text-sm font-medium dark:text-gray-100 mb-3">
              踢出成员
            </h4>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              确定要将 <span className="font-medium text-gray-900 dark:text-gray-100">{kickTarget.username}</span> 踢出频道吗？
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => setKickTarget(null)}
                className="flex-1 px-3 py-2 text-sm border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                取消
              </button>
              <button
                onClick={handleKick}
                className="flex-1 px-3 py-2 text-sm bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                确认踢出
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
