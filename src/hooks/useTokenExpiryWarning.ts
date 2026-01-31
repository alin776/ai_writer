import { useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import { useGlobalStore } from '@/store/globalStore';

/**
 * Token 过期提醒 Hook
 *
 * 功能：
 * - 每小时检查一次 refreshToken 剩余有效期
 * - 剩余时间 <= 1 天时，显示警告提醒
 * - 使用 localStorage 记录已提醒状态，避免重复提醒
 */
export const useTokenExpiryWarning = () => {
  const { refreshTokenExpiresAt, isAuthenticated } = useAuthStore();
  const { warning } = useGlobalStore();

  useEffect(() => {
    if (!isAuthenticated || !refreshTokenExpiresAt) {
      return;
    }

    const checkExpiry = () => {
      const now = Date.now();
      const timeLeft = refreshTokenExpiresAt - now;
      const oneDayInMs = 24 * 60 * 60 * 1000;

      // 如果剩余时间 <= 1天
      if (timeLeft > 0 && timeLeft <= oneDayInMs) {
        const hasWarned = localStorage.getItem('token_expiry_warned');
        const currentTokenKey = `warned_${refreshTokenExpiresAt}`;

        // 避免重复提醒（每个 token 只提醒一次）
        if (hasWarned !== currentTokenKey) {
          const hoursLeft = Math.ceil(timeLeft / (60 * 60 * 1000));

          let message = '';
          if (hoursLeft <= 24 && hoursLeft > 0) {
            message = `您的登录状态将在 ${hoursLeft} 小时后过期，请及时保存工作`;
          } else {
            message = '您的登录状态即将过期，请及时保存工作';
          }

          // 使用全局 Toast 系统显示警告
          warning(message, 10000); // 显示10秒

          // 标记已提醒
          localStorage.setItem('token_expiry_warned', currentTokenKey);
        }
      } else if (timeLeft <= 0) {
        // Token 已过期，清除提醒标记
        localStorage.removeItem('token_expiry_warned');
      }
    };

    // 立即检查一次
    checkExpiry();

    // 每小时检查一次
    const interval = setInterval(checkExpiry, 60 * 60 * 1000);

    return () => clearInterval(interval);
  }, [refreshTokenExpiresAt, isAuthenticated, warning]);
};
