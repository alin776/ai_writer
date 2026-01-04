import React, { useState, useEffect } from 'react';
import { getInvitePreview, joinByInviteCode, InvitePreview } from '@/services/channelApi';
import { useNavigate } from 'react-router-dom';

interface InviteLinkPreviewProps {
  inviteCode: string;
  inviteUrl: string;
}

const InviteLinkPreview: React.FC<InviteLinkPreviewProps> = ({ inviteCode, inviteUrl }) => {
  const [preview, setPreview] = useState<InvitePreview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [joining, setJoining] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPreview = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getInvitePreview(inviteCode);
        setPreview(data);
      } catch (err: unknown) {
        const errorMessage = err instanceof Error ? err.message : '无法加载预览';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchPreview();
  }, [inviteCode]);

  const handleClick = async () => {
    if (!preview || joining) return;

    // 已是成员，直接跳转到频道
    if (preview.isMember) {
      navigate(`/channels?channelId=${preview.channelId}`);
      return;
    }

    // 未加入，先加入再跳转
    try {
      setJoining(true);
      const result = await joinByInviteCode(inviteCode);
      // 加入成功，跳转到频道
      navigate(`/channels?channelId=${result.channelId}`);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : '加入失败';
      setError(errorMessage);
    } finally {
      setJoining(false);
    }
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return `${date.getFullYear()}年${date.getMonth() + 1}月`;
  };

  // 获取按钮文字
  const getButtonText = () => {
    if (joining) return '加入中...';
    if (preview?.isMember) return '前往频道';
    return '加入';
  };

  // 加载状态
  if (loading) {
    return (
      <div className="mt-2 max-w-[320px] rounded-xl overflow-hidden bg-[#2b2d31] dark:bg-[#2b2d31]">
        <div className="h-[50px] bg-[#f2f3f5] dark:bg-[#1e1f22]" />
        <div className="px-4 pb-4 bg-white dark:bg-[#2b2d31]">
          <div className="w-14 h-14 rounded-full bg-[#e3e5e8] dark:bg-[#36393f] -mt-6 mb-3 animate-pulse" />
          <div className="h-4 bg-[#e3e5e8] dark:bg-[#36393f] rounded w-32 mb-2 animate-pulse" />
          <div className="h-3 bg-[#e3e5e8] dark:bg-[#36393f] rounded w-48 animate-pulse" />
        </div>
      </div>
    );
  }

  // 错误状态
  if (error || !preview) {
    return (
      <a
        href={inviteUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-400 hover:underline"
        onClick={(e) => e.stopPropagation()}
      >
        {inviteUrl}
      </a>
    );
  }

  return (
    <div className="mt-2 max-w-[320px] rounded-xl overflow-hidden bg-white dark:bg-[#2b2d31]">
      {/* 横幅 */}
      <div className="h-[50px] bg-[#f2f3f5] dark:bg-[#1e1f22]" />

      {/* 内容区 */}
      <div className="px-4 pb-4 relative">
        {/* 频道图标 - 悬浮效果 */}
        <div className="w-14 h-14 rounded-full bg-white flex items-center justify-content -mt-6 mb-3 overflow-hidden shadow-md">
          {preview.channelIcon ? (
            <img
              src={preview.channelIcon}
              alt={preview.channelName}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full bg-[#5865f2] flex items-center justify-center text-white text-xl font-bold">
              {preview.channelName.charAt(0).toUpperCase()}
            </div>
          )}
        </div>

        {/* 频道名称 */}
        <div className="flex items-center gap-1.5 mb-1">
          <span className="text-[16px] font-semibold text-gray-900 dark:text-[#f2f3f5]">
            {preview.channelName}
          </span>
          <span className="text-[#23a55a]" title="首页">🏠</span>
        </div>

        {/* 统计信息 */}
        <div className="flex gap-3 text-[12px] text-gray-500 dark:text-[#b5bac1] mb-1">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-[#23a55a]" />
            {preview.onlineCount.toLocaleString()} 人在线
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-[#80848e]" />
            {preview.memberCount.toLocaleString()} 位成员
          </span>
        </div>

        {/* 创建日期 */}
        {preview.createdAt && (
          <div className="text-[12px] text-gray-400 dark:text-[#949ba4]">
            创建日期: {formatDate(preview.createdAt)}
          </div>
        )}

        {/* 按钮 - 根据成员状态显示不同文字 */}
        <button
          onClick={handleClick}
          disabled={joining}
          className="w-full mt-3 py-[7px] px-4 bg-[#248046] hover:bg-[#1a6334] text-white text-[14px] font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {getButtonText()}
        </button>
      </div>
    </div>
  );
};

export default InviteLinkPreview;
