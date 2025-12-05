/**
 * 邀请系统类型定义
 *
 * 包含邀请码、邀请统计、被邀请人等相关类型
 */

// ============================================
// 邀请码状态
// ============================================
export type InvitationStatus = 'pending' | 'active' | 'expired';

// ============================================
// 邀请码
// ============================================
export interface InvitationCode {
  /** 邀请码ID */
  id: string;
  /** 邀请码 */
  code: string;
  /** 最大使用次数 */
  maxUses: number;
  /** 已使用次数 */
  usedCount: number;
  /** 已激活人数 */
  activatedCount: number;
  /** 总奖励积分 */
  totalRewards: number;
  /** 过期时间 */
  expiresAt: string | null;
  /** 创建时间 */
  createdAt: string;
}

// ============================================
// 被邀请人
// ============================================
export interface Invitee {
  /** 用户名 */
  username: string;
  /** 邀请状态 */
  status: InvitationStatus;
  /** 注册时间 */
  registeredAt: string;
  /** 激活时间 */
  activatedAt: string | null;
}

// ============================================
// 邀请码详情 (含被邀请人列表)
// ============================================
export interface InvitationCodeDetail extends InvitationCode {
  /** 被邀请人列表 */
  invitees: Invitee[];
}

// ============================================
// 邀请统计
// ============================================
export interface InvitationStats {
  /** 总邀请数 */
  totalInvitations: number;
  /** 已使用数 */
  totalUsed: number;
  /** 已激活数 */
  totalActivated: number;
  /** 总奖励积分 */
  totalRewards: number;
  /** 是否可以生成更多邀请码 */
  canGenerateMore: boolean;
  /** 剩余生成配额 */
  remainingQuota: number;
}

// ============================================
// 生成邀请码请求
// ============================================
export interface GenerateInvitationRequest {
  /** 最大使用次数 (默认10) */
  maxUses?: number;
  /** 有效期(天数), 留空表示永不过期 */
  expiresDays?: number;
}

// 注意: generate 接口直接返回 InvitationCodeDetail，不再包装

// ============================================
// 验证邀请码请求和响应
// ============================================
export interface ValidateInvitationRequest {
  /** 邀请码 */
  code: string;
}

export interface ValidateInvitationResponse {
  /** 是否有效 */
  valid: boolean;
  /** 提示信息 */
  message: string;
}

// ============================================
// 注册请求 (含邀请码)
// ============================================
export interface RegisterRequest {
  /** 用户名 */
  username: string;
  /** 邮箱 */
  email: string;
  /** 密码 */
  password: string;
  /** 邀请码 */
  invitationCode: string;
}

// ============================================
// 批量生成邀请码请求 (管理端)
// ============================================
export interface BatchGenerateInvitationsRequest {
  /** 生成数量 */
  count: number;
  /** 最大使用次数 */
  maxUses?: number;
  /** 有效期(天数) */
  expiresDays?: number;
  /** 备注 */
  remark?: string;
}

export interface BatchGenerateInvitationsResponse {
  /** 生成的邀请码列表 */
  codes: InvitationCode[];
}

// ============================================
// 邀请码查询参数 (管理端)
// ============================================
export interface InvitationQueryParams {
  /** 页码 */
  page?: number;
  /** 每页数量 */
  pageSize?: number;
  /** 状态筛选 */
  status?: InvitationStatus;
  /** 创建者ID */
  userId?: string;
}

// ============================================
// 邀请状态配置
// ============================================
export interface InvitationStatusConfig {
  /** 显示文本 */
  label: string;
  /** 颜色类名 */
  color: string;
  /** 图标 */
  icon: string;
}

export const INVITATION_STATUS_CONFIG: Record<InvitationStatus, InvitationStatusConfig> = {
  pending: {
    label: '待激活',
    color: 'text-orange-600 bg-orange-50',
    icon: '⏳',
  },
  active: {
    label: '已激活',
    color: 'text-green-600 bg-green-50',
    icon: '✅',
  },
  expired: {
    label: '已过期',
    color: 'text-gray-600 bg-gray-50',
    icon: '❌',
  },
};
