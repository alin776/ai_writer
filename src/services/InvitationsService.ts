/**
 * 邀请服务
 *
 * 封装所有邀请相关的 API 调用
 */
import { ApiAdapter } from './ApiAdapter';
import type {
  InvitationStats,
  InvitationCodeDetail,
  ValidateInvitationResponse,
} from '../types/invitations';

/**
 * 邀请服务
 */
export class InvitationsService {
  private static adapter = new ApiAdapter();

  /**
   * 获取邀请统计信息
   */
  static async getStats(): Promise<InvitationStats> {
    return this.adapter.get<InvitationStats>('/invitations/stats');
  }

  /**
   * 获取我的邀请码列表
   *
   * 注意: API 直接返回 InvitationCodeDetail 数组，不包装
   */
  static async getMyCodes(): Promise<InvitationCodeDetail[]> {
    return this.adapter.get<InvitationCodeDetail[]>('/invitations/my-codes');
  }

  /**
   * 生成新的邀请码
   *
   * 注意: API 直接返回 InvitationCodeDetail 对象，不包装
   */
  static async generate(params?: {
    max_uses?: number;
    expires_days?: number;
  }): Promise<InvitationCodeDetail> {
    return this.adapter.post<InvitationCodeDetail>('/invitations/generate', params);
  }

  /**
   * 验证邀请码 (公开接口，用于注册页面)
   */
  static async validate(code: string): Promise<ValidateInvitationResponse> {
    return this.adapter.post<ValidateInvitationResponse>('/invitations/validate', { code });
  }
}
