import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronRight, Pencil, User, LogOut, LayoutDashboard } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { useAuthStore, type OnlineStatus } from '@/store/authStore';
import { DataService } from '@/services/DataService';

export interface UserCardPopoverProps {
  isOpen: boolean;
  onClose: () => void;
}

interface StatusOption {
  value: OnlineStatus;
  label: string;
  color: string;
}

const statusOptions: StatusOption[] = [
  { value: 'online', label: '在线', color: '#23a55a' },
  { value: 'idle', label: '闲置', color: '#f0b232' },
  { value: 'dnd', label: '请勿打扰', color: '#f23f43' },
  { value: 'offline', label: '隐身', color: '#80848e' },
];

export function UserCardPopover({ isOpen, onClose }: UserCardPopoverProps) {
  const navigate = useNavigate();
  const { user, logout, onlineStatus, setOnlineStatus } = useAuthStore();
  const popoverRef = useRef<HTMLDivElement>(null);
  const [isStatusDropdownOpen, setIsStatusDropdownOpen] = useState(false);

  // 点击外部关闭
  useEffect(() => {
    if (!isOpen) return;

    const handleClickOutside = (e: MouseEvent) => {
      if (popoverRef.current && !popoverRef.current.contains(e.target as Node)) {
        onClose();
      }
    };

    const timer = setTimeout(() => {
      document.addEventListener('mousedown', handleClickOutside);
    }, 100);

    return () => {
      clearTimeout(timer);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose]);

  // ESC 关闭
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (isStatusDropdownOpen) {
          setIsStatusDropdownOpen(false);
        } else {
          onClose();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose, isStatusDropdownOpen]);

  if (!isOpen || !user) return null;

  const currentStatusOption = statusOptions.find(s => s.value === onlineStatus) || statusOptions[0];

  const handleEditProfile = () => {
    navigate('/settings');
    onClose();
  };

  const handleSwitchAccount = () => {
    navigate(`/user/${user.id}`);
    onClose();
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    onClose();
  };

  const handleGoToAdmin = () => {
    navigate('/admin/dashboard');
    onClose();
  };

  const handleSelectStatus = async (status: OnlineStatus) => {
    setOnlineStatus(status);
    setIsStatusDropdownOpen(false);
    // 同步用户在线状态到服务器
    try {
      await DataService.updateOnlineStatus(status);
    } catch (error) {
      console.error('更新在线状态失败:', error);
    }
  };

  return (
    <div
      ref={popoverRef}
      style={{
        position: 'fixed',
        zIndex: 100,
        width: '340px',
        borderRadius: '8px',
        overflow: 'visible',
        bottom: '70px',
        left: '12px',
        boxShadow: '0 8px 16px rgba(0, 0, 0, 0.24)',
      }}
      className="bg-white dark:bg-[#1e293b]"
    >
      {/* 顶部横幅 - 品红色 */}
      <div
        style={{
          height: '60px',
          background: '#a33a6e',
          borderRadius: '8px 8px 0 0',
        }}
      />

      {/* 头像区域容器 */}
      <div
        style={{
          position: 'relative',
          height: '60px',
          padding: '0 16px',
        }}
      >
        {/* 头像区域 */}
        <div
          style={{
            position: 'absolute',
            top: '-40px',
            left: '16px',
          }}
        >
          <div style={{ position: 'relative' }}>
              <Avatar
                style={{
                  width: '92px',
                  height: '92px',
                  borderRadius: '50%',
                  overflow: 'visible',
                }}
              className="border-[7px] border-white dark:border-[#1e293b]"
            >
              <AvatarImage
                src={user.avatar}
                style={{
                  width: '100%',
                  height: '100%',
                  borderRadius: '50%',
                  objectFit: 'cover',
                }}
              />
              <AvatarFallback
                style={{
                  fontSize: '24px',
                  background: '#5865f2',
                  color: '#fff',
                }}
              >
                {user.username?.[0]?.toUpperCase() || 'U'}
              </AvatarFallback>
            </Avatar>
            {/* 在线状态指示器 */}
            <div
              style={{
                position: 'absolute',
                bottom: '2px',
                right: '2px',
                width: '20px',
                height: '20px',
                borderRadius: '50%',
                background: currentStatusOption.color,
                zIndex: 6,
              }}
              className="border-4 border-white dark:border-[#1e293b]"
            />
          </div>
        </div>
      </div>

      {/* 用户信息区域 */}
      <div style={{ padding: '24px 16px 16px' }}>
        {/* 用户名 */}
        <div
          style={{
            fontSize: '20px',
            fontWeight: 600,
            lineHeight: 1.2,
            marginBottom: '4px',
          }}
          className="text-[#060607] dark:text-[#f2f3f5]"
        >
          {user.fullName || user.username}
        </div>
        {/* 个人简介 */}
        <div
          style={{
            fontSize: '14px',
            marginBottom: 0,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            lineHeight: '1.4',
          }}
          className="text-[#80848e] dark:text-[#b5bac1]"
          title={user.bio || ''}
        >
          {user.bio || '这个人很懒，什么都没写~'}
        </div>

        {/* 分隔线 */}
        <div
          style={{ height: '1px', margin: '12px 0' }}
          className="bg-[#e1e2e4] dark:bg-[#334155]"
        />

        {/* 编辑个人资料 */}
        <div
          onClick={handleEditProfile}
          style={{
            display: 'flex',
            alignItems: 'center',
            padding: '8px 8px',
            margin: '0 -8px',
            borderRadius: '4px',
            cursor: 'pointer',
            transition: 'background 0.15s',
          }}
          className="hover:bg-[#e8e9eb] dark:hover:bg-[#334155]"
        >
          <div
            style={{
              width: '20px',
              height: '20px',
              marginRight: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
            className="text-[#4e5058] dark:text-[#b5bac1]"
          >
            <Pencil style={{ width: '18px', height: '18px' }} />
          </div>
          <span
            style={{ flex: 1, fontSize: '14px', fontWeight: 500 }}
            className="text-[#313338] dark:text-[#dbdee1]"
          >
            编辑个人资料
          </span>
          <span
            style={{
              background: '#f23f43',
              color: '#fff',
              fontSize: '12px',
              fontWeight: 700,
              padding: '3px 8px',
              borderRadius: '4px',
              marginRight: '8px',
            }}
          >
            新的
          </span>
        </div>

        {/* 在线状态 */}
        <div style={{ position: 'relative' }}>
          <div
            onClick={() => setIsStatusDropdownOpen(!isStatusDropdownOpen)}
            style={{
              display: 'flex',
              alignItems: 'center',
              padding: '8px 8px',
              margin: '0 -8px',
              borderRadius: '4px',
              cursor: 'pointer',
              transition: 'background 0.15s',
            }}
            className="hover:bg-[#e8e9eb] dark:hover:bg-[#334155]"
          >
            <div
              style={{
                width: '12px',
                height: '12px',
                borderRadius: '50%',
                marginRight: '12px',
                background: currentStatusOption.color,
              }}
            />
            <span
              style={{ flex: 1, fontSize: '14px', fontWeight: 500 }}
              className="text-[#313338] dark:text-[#dbdee1]"
            >
              {currentStatusOption.label}
            </span>
            <ChevronRight
              style={{ width: '18px', height: '18px' }}
              className="text-[#80848e] dark:text-[#b5bac1]"
            />
          </div>

          {/* 状态下拉菜单 */}
          {isStatusDropdownOpen && (
            <div
              style={{
                position: 'absolute',
                left: '8px',
                right: '8px',
                marginTop: '4px',
                borderRadius: '4px',
                padding: '6px',
                boxShadow: '0 8px 16px rgba(0, 0, 0, 0.18)',
                zIndex: 10,
              }}
              className="bg-white dark:bg-[#0f172a] border border-[#e1e2e4] dark:border-[#334155]"
            >
              {statusOptions.map((option) => (
                <div
                  key={option.value}
                  onClick={() => handleSelectStatus(option.value)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    padding: '10px 8px',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    transition: 'background 0.1s',
                  }}
                  className="group hover:bg-[#5865f2]"
                >
                  <div
                    style={{
                      width: '12px',
                      height: '12px',
                      borderRadius: '50%',
                      marginRight: '10px',
                      background: option.color,
                    }}
                  />
                  <span
                    style={{ fontSize: '14px', fontWeight: 500 }}
                    className="text-[#313338] dark:text-[#dbdee1] group-hover:text-white"
                  >
                    {option.label}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 分隔线 */}
        <div
          style={{ height: '1px', margin: '8px 0' }}
          className="bg-[#e1e2e4] dark:bg-[#334155]"
        />

        {/* 个人主页 */}
        <div
          onClick={handleSwitchAccount}
          style={{
            display: 'flex',
            alignItems: 'center',
            padding: '8px 8px',
            margin: '0 -8px',
            borderRadius: '4px',
            cursor: 'pointer',
            transition: 'background 0.15s',
          }}
          className="hover:bg-[#e8e9eb] dark:hover:bg-[#334155]"
        >
          <div
            style={{
              width: '20px',
              height: '20px',
              marginRight: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
            className="text-[#4e5058] dark:text-[#b5bac1]"
          >
            <User style={{ width: '18px', height: '18px' }} />
          </div>
          <span
            style={{ flex: 1, fontSize: '14px', fontWeight: 500 }}
            className="text-[#313338] dark:text-[#dbdee1]"
          >
            个人主页
          </span>
          <ChevronRight
            style={{ width: '18px', height: '18px' }}
            className="text-[#80848e] dark:text-[#b5bac1]"
          />
        </div>

        {/* 分隔线 */}
        <div
          style={{ height: '1px', margin: '8px 0' }}
          className="bg-[#e1e2e4] dark:bg-[#334155]"
        />

        {/* 管理后台入口 - 仅管理员可见 */}
        {(user.role === 'admin' || user.isAdmin) && (
          <div
            onClick={handleGoToAdmin}
            style={{
              display: 'flex',
              alignItems: 'center',
              padding: '8px 8px',
              margin: '0 -8px',
              borderRadius: '4px',
              cursor: 'pointer',
              transition: 'background 0.15s',
            }}
            className="hover:bg-[#e8e9eb] dark:hover:bg-[#334155]"
          >
            <div
              style={{
                width: '20px',
                height: '20px',
                marginRight: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
              className="text-[#4e5058] dark:text-[#b5bac1]"
            >
              <LayoutDashboard style={{ width: '18px', height: '18px' }} />
            </div>
            <span
              style={{ flex: 1, fontSize: '14px', fontWeight: 500 }}
              className="text-[#313338] dark:text-[#dbdee1]"
            >
              管理后台
            </span>
            <ChevronRight
              style={{ width: '18px', height: '18px' }}
              className="text-[#80848e] dark:text-[#b5bac1]"
            />
          </div>
        )}

        {/* 退出登录 */}
        <div
          onClick={handleLogout}
          style={{
            display: 'flex',
            alignItems: 'center',
            padding: '8px 8px',
            margin: '0 -8px',
            borderRadius: '4px',
            cursor: 'pointer',
            transition: 'background 0.15s',
          }}
          className="hover:bg-[#e8e9eb] dark:hover:bg-[#334155]"
        >
          <div
            style={{
              width: '20px',
              height: '20px',
              marginRight: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
            className="text-[#4e5058] dark:text-[#b5bac1]"
          >
            <LogOut style={{ width: '18px', height: '18px' }} />
          </div>
          <span
            style={{ flex: 1, fontSize: '14px', fontWeight: 500 }}
            className="text-[#313338] dark:text-[#dbdee1]"
          >
            退出登录
          </span>
        </div>
      </div>
    </div>
  );
}

export default UserCardPopover;
