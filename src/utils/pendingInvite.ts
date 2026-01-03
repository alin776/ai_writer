/**
 * 待处理的频道邀请工具函数
 * 用于处理未登录用户点击邀请链接后的延迟加入逻辑
 */

import { channelApi } from '@/services/channelApi';

const STORAGE_KEY = 'pending_channel_invite';
const EXPIRE_HOURS = 24;

interface PendingInvite {
  code: string;
  timestamp: number;
}

/**
 * 保存待处理的邀请码到 localStorage
 */
export function savePendingInvite(code: string): void {
  const data: PendingInvite = {
    code,
    timestamp: Date.now(),
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

/**
 * 获取待处理的邀请码
 * 如果已过期（超过24小时）则返回 null 并清除
 */
export function getPendingInvite(): string | null {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;

  try {
    const data: PendingInvite = JSON.parse(raw);
    const expireTime = data.timestamp + EXPIRE_HOURS * 60 * 60 * 1000;

    if (Date.now() > expireTime) {
      clearPendingInvite();
      return null;
    }

    return data.code;
  } catch {
    clearPendingInvite();
    return null;
  }
}

/**
 * 清除待处理的邀请码
 */
export function clearPendingInvite(): void {
  localStorage.removeItem(STORAGE_KEY);
}

/**
 * 处理待处理的邀请
 * 登录/注册成功后调用此函数
 * @returns 加入成功的频道ID，如果没有待处理邀请或加入失败则返回 null
 */
export async function processPendingInvite(): Promise<string | null> {
  const code = getPendingInvite();
  if (!code) return null;

  try {
    const result = await channelApi.joinByInviteCode(code);
    clearPendingInvite();
    return result.channelId;
  } catch (error) {
    console.error('处理待处理邀请失败:', error);
    clearPendingInvite();
    return null;
  }
}
