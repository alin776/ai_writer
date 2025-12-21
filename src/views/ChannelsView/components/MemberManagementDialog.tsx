import { useState, useEffect } from 'react';
import { X, Crown, UserX } from 'lucide-react';
import { getChannelMembers, kickMember, type ChannelMember } from '@/services/channelApi';
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
      // 从列表中移除
      setMembers(prev => prev.filter(m => m.userId !== userId));
    } catch (error) {
      console.error('踢出成员失败:', error);
      showToast('error', '踢出成员失败');
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

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md max-h-[80vh] flex flex-col">
        {/* 标题栏 */}
        <div className="flex items-center justify-between p-4 border-b">
          <div>
            <h3 className="text-base font-medium">成员管理</h3>
            <p className="text-xs text-gray-500 mt-0.5">{channelName}</p>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* 成员列表 */}
        <div className="flex-1 overflow-y-auto p-4">
          {loading ? (
            <div className="text-center py-8 text-sm text-gray-500">
              加载中...
            </div>
          ) : members.length === 0 ? (
            <div className="text-center py-8 text-sm text-gray-500">
              暂无成员
            </div>
          ) : (
            <div className="space-y-2">
              {members.map((member) => (
                <div
                  key={member.id}
                  className="flex items-center justify-between p-2 hover:bg-gray-50 rounded"
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
                        <span className="text-sm font-medium truncate">
                          {member.username}
                        </span>
                        {member.role === 'owner' && (
                          <Crown className="w-3.5 h-3.5 text-yellow-500 flex-shrink-0" />
                        )}
                      </div>
                      <div className="text-xs text-gray-500">
                        {getRoleName(member.role)}
                      </div>
                    </div>
                  </div>

                  {/* 操作按钮 */}
                  {isCreator && member.userId !== currentUserId && member.role !== 'owner' && (
                    <button
                      onClick={() => handleKick(member.userId, member.username)}
                      className="p-1.5 hover:bg-red-50 rounded text-red-600 transition-colors"
                      title="踢出成员"
                    >
                      <UserX className="w-4 h-4" />
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 底部统计 */}
        <div className="p-4 border-t bg-gray-50">
          <p className="text-xs text-gray-500 text-center">
            共 {members.length} 名成员
          </p>
        </div>
      </div>
    </div>
  );
}
