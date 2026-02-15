/**
 * 文件系统章节服务
 *
 * 对接后端 chapters_fs API（/v2/works/{workId}/chapters）
 * 复用 ApiAdapter 获取认证 token 和 snake_case 转换能力
 */
import { sharedApi as api } from './ApiAdapter';
import type { FSChapter } from '../types/novel';

/** 列出所有章节（不含正文） */
async function list(workId: string): Promise<FSChapter[]> {
  return api.get<FSChapter[]>(`/v2/works/${workId}/chapters`);
}

/** 获取单个章节（含正文） */
async function get(workId: string, num: number): Promise<FSChapter> {
  return api.get<FSChapter>(`/v2/works/${workId}/chapters/${num}`);
}

/** 创建章节 */
async function create(
  workId: string,
  data: { title: string; content?: string; status?: string }
): Promise<FSChapter> {
  return api.post<FSChapter>(`/v2/works/${workId}/chapters`, data);
}

/** 更新章节 */
async function update(
  workId: string,
  num: number,
  data: { title?: string; content?: string; status?: string }
): Promise<FSChapter> {
  return api.put<FSChapter>(`/v2/works/${workId}/chapters/${num}`, data);
}

/** 删除章节 */
async function remove(workId: string, num: number): Promise<void> {
  return api.delete<void>(`/v2/works/${workId}/chapters/${num}`);
}

export const chaptersFs = { list, get, create, update, remove };
