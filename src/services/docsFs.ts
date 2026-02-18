/**
 * docsFs — 文件树 API 客户端
 *
 * 复用已有的 /files/{path} 端点进行读写，新增 /tree 端点获取文件树。
 */
import { sharedApi as api } from './ApiAdapter';

export interface FileNode {
  name: string;
  path: string;
  type: 'file' | 'dir';
  size: number;
  children?: FileNode[];
}

async function tree(workId: string): Promise<FileNode[]> {
  return api.get<FileNode[]>(`/v2/works/${workId}/tree`);
}

async function read(workId: string, path: string): Promise<{ path: string; content: string }> {
  return api.get(`/v2/works/${workId}/files/${path}`);
}

async function write(workId: string, path: string, content: string): Promise<void> {
  await api.put(`/v2/works/${workId}/files/${path}`, { content });
}

async function createFile(workId: string, path: string): Promise<FileNode[]> {
  await api.put(`/v2/works/${workId}/files/${path}`, { content: '' });
  return tree(workId);
}

async function createDir(workId: string, path: string): Promise<FileNode[]> {
  return api.post<FileNode[]>(`/v2/works/${workId}/dirs/${path}`);
}

async function remove(workId: string, path: string): Promise<FileNode[]> {
  return api.delete<FileNode[]>(`/v2/works/${workId}/files/${path}`);
}

async function rename(workId: string, path: string, newName: string): Promise<FileNode[]> {
  return api.patch<FileNode[]>(`/v2/works/${workId}/files/${path}`, { new_name: newName });
}

export const docsFs = { tree, read, write, createFile, createDir, remove, rename };
