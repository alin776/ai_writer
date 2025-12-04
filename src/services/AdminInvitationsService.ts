/**
 * 管理员邀请码服务
 *
 * 封装所有管理员邀请码相关的 API 调用
 */
import { ApiAdapter } from './ApiAdapter';

/**
 * 生成邀请码请求
 */
export interface AdminGenerateInvitationRequest {
  /** 自定义邀请码 (3-8位, 可选) */
  custom_code?: string;
  /** 最大使用次数 (1-100) */
  max_uses: number;
  /** 有效期天数 (1-365) */
  expires_days: number;
  /** 备注信息 (可选) */
  remark?: string;
}

/**
 * 邀请码信息
 */
export interface AdminInvitationInfo {
  /** ID */
  id: string;
  /** 邀请码 */
  code: string;
  /** 最大使用次数 */
  max_uses: number;
  /** 已使用次数 */
  used_count: number;
  /** 已激活次数 */
  activated_count: number;
  /** 累计奖励 */
  total_rewards: number;
  /** 使用率(百分比) */
  usage_rate?: number;
  /** 过期时间 (可选) */
  expires_at?: string;
  /** 备注 */
  remark?: string;
  /** 创建者用户名 */
  creator_username?: string;
  /** 创建时间 */
  created_at: string;
  /** 状态 (active/expired/exhausted) */
  status: string;
}

/**
 * 邀请码列表响应
 */
export interface AdminInvitationListResponse {
  /** 数据项 */
  items: AdminInvitationInfo[];
  /** 总数 */
  total: number;
  /** 当前页码 */
  page: number;
  /** 每页数量 */
  page_size: number;
  /** 总页数 */
  total_pages: number;
  /** 统计信息 */
  stats: AdminInvitationStats;
}

/**
 * 邀请码统计信息
 */
export interface AdminInvitationStats {
  /** 邀请码总数 */
  total_codes: number;
  /** 有效邀请码数 */
  active_codes: number;
  /** 已过期邀请码数 */
  expired_codes: number;
  /** 已用完邀请码数 */
  exhausted_codes: number;
  /** 总使用次数 */
  total_usages: number;
  /** 总激活次数 */
  total_activated: number;
  /** 总奖励积分 */
  total_rewards: number;
}

/**
 * 删除邀请码响应
 */
export interface AdminDeleteInvitationResponse {
  /** 是否成功 */
  success: boolean;
  /** 消息 */
  message: string;
}

/**
 * 管理员邀请码服务
 */
export class AdminInvitationsService {
  private static adapter = new ApiAdapter();

  /**
   * 生成邀请码
   */
  static async generate(request: AdminGenerateInvitationRequest): Promise<AdminInvitationInfo> {
    return this.adapter.post<AdminInvitationInfo>('/admin/invitations/generate', request);
  }

  /**
   * 查询邀请码列表
   */
  static async list(params?: {
    page?: number;
    page_size?: number;
    status?: string;
    creator_id?: string;
    search?: string;
  }): Promise<AdminInvitationListResponse> {
    return this.adapter.get<AdminInvitationListResponse>('/admin/invitations/list', params);
  }

  /**
   * 删除邀请码
   */
  static async delete(invitationId: string): Promise<AdminDeleteInvitationResponse> {
    return this.adapter.delete(`/admin/invitations/${invitationId}`);
  }
}
