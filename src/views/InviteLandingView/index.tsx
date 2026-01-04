import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getInvitePreview, joinByInviteCode, InvitePreview } from '@/services/channelApi';
import { useAuthStore } from '@/store/authStore';
import { savePendingInvite } from '@/utils/pendingInvite';

const InviteLandingView: React.FC = () => {
  const { code } = useParams<{ code: string }>();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuthStore();

  const [preview, setPreview] = useState<InvitePreview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [joining, setJoining] = useState(false);

  useEffect(() => {
    const fetchPreview = async () => {
      if (!code) {
        setError('无效的邀请链接');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const data = await getInvitePreview(code);
        setPreview(data);
      } catch (err: unknown) {
        const errorMessage = err instanceof Error ? err.message : '邀请链接无效或已过期';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchPreview();
  }, [code]);

  const handleAcceptInvite = async () => {
    if (!code || !preview || joining) return;

    // 未登录用户：保存邀请码到 localStorage，跳转到登录页
    if (!isAuthenticated) {
      savePendingInvite(code);
      navigate('/login');
      return;
    }

    // 已是成员，直接跳转到频道
    if (preview.isMember) {
      navigate(`/channels?channelId=${preview.channelId}`);
      return;
    }

    // 未加入，先加入再跳转
    try {
      setJoining(true);
      const result = await joinByInviteCode(code);
      // 加入成功，跳转到频道
      navigate(`/channels?channelId=${result.channelId}`);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : '加入失败';
      setError(errorMessage);
    } finally {
      setJoining(false);
    }
  };

  // 获取按钮文字
  const getButtonText = () => {
    if (!isAuthenticated) return '接受邀请';
    if (joining) return '加入中...';
    if (preview?.isMember) return '前往频道';
    return '加入频道';
  };

  // Logo + 网站名称组件
  const LogoHeader = () => (
    <div className="fixed top-0 left-0 z-50 p-4 lg:p-6">
      <button
        onClick={() => navigate('/')}
        className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
      >
        <div className="w-12 h-12 rounded-full bg-white flex items-center justify-center">
          <img
            src="/logo-icon.svg"
            alt="文枢AI"
            className="w-9 h-9"
          />
        </div>
        <span className="text-base tracking-wider font-medium text-white">
          文枢AI
        </span>
      </button>
    </div>
  );

  // 背景容器组件
  const BackgroundContainer = ({ children }: { children: React.ReactNode }) => (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-[#4a5568]">
      {/* 背景图片 */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: 'url(/images/invite-bg.jpg)' }}
      />
      {/* 半透明遮罩 */}
      <div className="absolute inset-0 bg-black/30" />
      {/* Logo */}
      <LogoHeader />
      {/* 内容 */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );

  // 加载状态
  if (loading) {
    return (
      <BackgroundContainer>
        <div className="w-[480px] bg-[#36393f] rounded-2xl p-8 text-center">
          <div className="w-20 h-20 rounded-2xl bg-[#2b2d31] mx-auto mb-4 animate-pulse" />
          <div className="h-4 bg-[#2b2d31] rounded w-32 mx-auto mb-2 animate-pulse" />
          <div className="h-6 bg-[#2b2d31] rounded w-48 mx-auto mb-4 animate-pulse" />
          <div className="h-4 bg-[#2b2d31] rounded w-40 mx-auto animate-pulse" />
        </div>
      </BackgroundContainer>
    );
  }

  // 错误状态
  if (error || !preview) {
    return (
      <BackgroundContainer>
        <div className="w-[480px] bg-[#36393f] rounded-2xl p-8 text-center">
          <div className="w-20 h-20 rounded-2xl bg-[#2b2d31] mx-auto mb-4 flex items-center justify-center">
            <svg className="w-10 h-10 text-[#80848e]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <p className="text-[#b5bac1] text-sm mb-2">邀请链接无效</p>
          <p className="text-[#f2f3f5] text-lg font-semibold mb-6">
            {error || '该邀请链接可能已过期或不存在'}
          </p>
          <button
            onClick={() => navigate('/')}
            className="w-full py-3 px-4 bg-[#5865f2] hover:bg-[#4752c4] text-white text-base font-medium rounded-lg transition-colors"
          >
            返回首页
          </button>
        </div>
      </BackgroundContainer>
    );
  }

  return (
    <BackgroundContainer>
      {/* 邀请卡片 */}
      <div className="w-[480px] bg-[#36393f] rounded-2xl p-8 text-center" style={{ boxShadow: '0 8px 32px rgba(0,0,0,0.3)' }}>
        {/* 频道图标 - 圆角方形 + 白色边框 */}
        <div className="w-20 h-20 rounded-2xl bg-white mx-auto mb-4 overflow-hidden flex items-center justify-center" style={{ border: '4px solid white', boxShadow: '0 4px 12px rgba(0,0,0,0.2)' }}>
          {preview.channelIcon ? (
            <img
              src={preview.channelIcon}
              alt={preview.channelName}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full bg-[#5865f2] flex items-center justify-center text-white text-3xl font-bold">
              {preview.channelName.charAt(0).toUpperCase()}
            </div>
          )}
        </div>

        {/* 提示文字 */}
        <p className="text-[#b5bac1] text-sm mb-2">您已被邀请加入</p>

        {/* 频道名称 */}
        <h1 className="text-[#f2f3f5] text-2xl font-bold mb-4">
          {preview.channelName}
        </h1>

        {/* 统计信息 */}
        <div className="flex items-center justify-center gap-6 mb-8">
          <span className="flex items-center gap-1.5 text-sm text-[#b5bac1]">
            <span className="w-2.5 h-2.5 rounded-full bg-[#23a55a]" />
            {preview.onlineCount.toLocaleString()} 人在线
          </span>
          <span className="flex items-center gap-1.5 text-sm text-[#b5bac1]">
            <span className="w-2.5 h-2.5 rounded-full bg-[#80848e]" />
            {preview.memberCount.toLocaleString()} 位成员
          </span>
        </div>

        {/* 接受邀请按钮 - 蓝紫色 */}
        <button
          onClick={handleAcceptInvite}
          disabled={joining}
          className="w-full py-3.5 px-4 bg-[#5865f2] hover:bg-[#4752c4] text-white text-base font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {getButtonText()}
        </button>

        {/* 登录提示（未登录时显示） */}
        {!isAuthenticated && (
          <p className="text-[#949ba4] text-xs mt-4">
            点击"接受邀请"将跳转到登录页面
          </p>
        )}
      </div>
    </BackgroundContainer>
  );
};

export default InviteLandingView;
