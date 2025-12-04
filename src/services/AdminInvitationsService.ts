/**
 * 管理员邀请码服务
 *
 * 封装所有管理员邀请码相关 API 调用
 */
import { ApiAdapter } from './ApiAdapter';

/**
 * 生成邀请码请求
 */
export interface AdminGenerateInvitationRequest {
  /** 自定义邀请码 (3-8 位 可选) */
  customCode?: string;
  /** 最大使用次数(1-100) */
  maxUses: number;
  /** 有效期天数(1-365) */
  expiresDays: number;
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
  maxUses: number;
  /** 已使用次数 */
  usedCount: number;
  /** 已激活次数 */
  activatedCount: number;
  /** 累计奖励 */
  totalRewards: number;
  /** 使用率百分比 */
  usageRate?: number;
  /** 过期时间 (可选) */
  expiresAt?: string;
  /** 备注 */
  remark?: string;
  /** 创建者用户名 */
  creatorUsername?: string;
  /** 创建时间 */
  createdAt: string;
  /** 状态(active/expired/exhausted) */
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
  pageSize: number;
  /** 总页数 */
  totalPages: number;
  /** 统计信息 */
  stats: AdminInvitationStats;
}

/**
 * 邀请码统计信息
 */
export interface AdminInvitationStats {
  /** 邀请码总数 */
  totalCodes: number;
  /** 有效邀请码数 */
  activeCodes: number;
  /** 已过期邀请码数 */
  expiredCodes: number;
  /** 已用完邀请码数 */
  exhaustedCodes: number;
  /** 总使用次数 */
  totalUsages: number;
  /** 总激活次数 */
  totalActivated: number;
  /** 总奖励积分 */
  totalRewards: number;
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
    pageSize?: number;
    status?: string;
    creatorId?: string;
    search?: string;
  }): Promise<AdminInvitationListResponse> {
    const apiParams: Record<string, any> = {};
    if (params?.page !== undefined) apiParams.page = params.page;
    if (params?.pageSize !== undefined) apiParams.page_size = params.pageSize;
    if (params?.status) apiParams.status = params.status;
    if (params?.creatorId) apiParams.creator_id = params.creatorId;
    if (params?.search) apiParams.search = params.search;

    return this.adapter.get<AdminInvitationListResponse>('/admin/invitations/list', apiParams);
  }

  /**
   * 删除邀请码
   */
  static async delete(invitationId: string): Promise<AdminDeleteInvitationResponse> {
    return this.adapter.delete(`/admin/invitations/${invitationId}`);
  }
}
