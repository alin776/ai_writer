/**
 * V2 Changes API 服务
 *
 * 对接后端 /agent/v2/changes/{conversationId} 端点
 * 用于批量审批 Agent 产生的文件变更
 */
import { agentApi } from './agentApi';

// 复用 agentApi 的 axios 实例（已配置认证，baseURL 为 /agent）
const client = agentApi.client;

export interface FileChange {
  path: string;
  op: string; // create | modify | delete
  diff?: string;
  content?: string;
}

export interface ChangesResponse {
  conversationId: string;
  changes: FileChange[];
}

/** 获取待审批的变更列表 */
async function list(conversationId: string): Promise<ChangesResponse> {
  const res = await client.get(`/v2/changes/${conversationId}`);
  return res.data;
}

/** 全部接受 */
async function acceptAll(conversationId: string): Promise<{ status: string; affectedPaths: string[] }> {
  const res = await client.post(`/v2/changes/${conversationId}/accept`);
  return res.data;
}

/** 全部拒绝 */
async function rejectAll(conversationId: string): Promise<{ status: string }> {
  const res = await client.post(`/v2/changes/${conversationId}/reject`);
  return res.data;
}

/** 单个接受 */
async function acceptOne(conversationId: string, index: number): Promise<{ status: string; path: string }> {
  const res = await client.post(`/v2/changes/${conversationId}/accept/${index}`);
  return res.data;
}

/** 单个拒绝 */
async function rejectOne(conversationId: string, index: number): Promise<{ status: string }> {
  const res = await client.post(`/v2/changes/${conversationId}/reject/${index}`);
  return res.data;
}

export const changesApi = { list, acceptAll, rejectAll, acceptOne, rejectOne };
