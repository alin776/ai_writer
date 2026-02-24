/**
 * 章节评论 API 服务
 * 支持章节级、段落级、句子级评论
 */
import axios from 'axios';
import { useAuthStore } from '@/store/authStore';

// ==================== API 配置 ====================

const getBaseUrl = () => {
  return import.meta.env.DEV ? '/api/v1' : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api');
};

const getAuthHeader = () => {
  const authStorage = localStorage.getItem('auth-storage');
  if (authStorage) {
    try {
      const authState = JSON.parse(authStorage);
      const token = authState.state?.token;
      if (token) {
        return { Authorization: `Bearer ${token}` };
      }
    } catch (error) {
      console.error('[chapterCommentApi] Failed to parse auth storage:', error);
    }
  }
  return {};
};

// snake_case 转 camelCase
const toCamelCase = (str: string): string => {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
};

const convertKeysToCamelCase = (obj: any): any => {
  if (obj === null || obj === undefined) return obj;
  if (typeof obj !== 'object') return obj;
  if (obj instanceof Date) return obj;
  if (Array.isArray(obj)) return obj.map(item => convertKeysToCamelCase(item));

  const result: any = {};
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      const camelKey = toCamelCase(key);
      result[camelKey] = convertKeysToCamelCase(obj[key]);
    }
  }
  return result;
};

// ==================== 类型定义 ====================

export interface UserInfo {
  id: string;
  username: string;
  avatar?: string;
}

export interface ChapterComment {
  id: string;
  workId: string;
  chapterNum: number;
  userId: string;
  content: string;
  locationType: 'chapter' | 'paragraph' | 'sentence';
  paragraphIndex?: number;
  sentenceIndex?: number;
  quotedText?: string;
  parentId?: string;
  replyToUserId?: string;
  likeCount: number;
  isDeleted: boolean;
  createdAt: string;
  updatedAt?: string;
  user?: UserInfo;
  replyToUser?: UserInfo;
  isLiked: boolean;
  replyCount: number;
  replies?: ChapterComment[];
}

export interface ChapterCommentWithReplies extends ChapterComment {
  replies: ChapterComment[];
}

export interface ChapterCommentListResponse {
  total: number;
  page: number;
  pageSize: number;
  items: ChapterCommentWithReplies[];
}

export interface CommentLocationStats {
  chapter: number;
  paragraphs: Record<string, number>;
  sentences: Record<string, number>;
  total: number;
}

export interface CreateChapterCommentData {
  content: string;
  locationType?: 'chapter' | 'paragraph' | 'sentence';
  paragraphIndex?: number;
  sentenceIndex?: number;
  quotedText?: string;
  parentId?: string;
  replyToUserId?: string;
}

export interface LikeResponse {
  success: boolean;
  likeCount: number;
  isLiked: boolean;
}

export type ReportReason = 'spam' | 'abuse' | 'porn' | 'illegal' | 'false' | 'other';

export interface ReportData {
  reason: ReportReason;
  description?: string;
}

// ==================== API 对象 ====================

export const chapterCommentApi = {
  getComments: async (
    workId: string,
    chapterNum: number,
    params?: {
      page?: number;
      pageSize?: number;
      locationType?: 'chapter' | 'paragraph' | 'sentence';
      paragraphIndex?: number;
      sentenceIndex?: number;
    }
  ): Promise<ChapterCommentListResponse> => {
    const queryParams = new URLSearchParams();
    if (params?.page !== undefined) queryParams.set('skip', ((params.page - 1) * (params.pageSize || 20)).toString());
    if (params?.pageSize !== undefined) queryParams.set('limit', params.pageSize.toString());
    if (params?.locationType) queryParams.set('location_type', params.locationType);
    if (params?.paragraphIndex !== undefined) queryParams.set('paragraph_index', params.paragraphIndex.toString());
    if (params?.sentenceIndex !== undefined) queryParams.set('sentence_index', params.sentenceIndex.toString());

    const url = `${getBaseUrl()}/chapter-comments/works/${workId}/chapters/${chapterNum}/comments${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    const response = await axios.get(url, { headers: getAuthHeader() });
    return convertKeysToCamelCase(response.data);
  },

  getStats: async (workId: string, chapterNum: number): Promise<CommentLocationStats> => {
    const url = `${getBaseUrl()}/chapter-comments/works/${workId}/chapters/${chapterNum}/comments/stats`;
    const response = await axios.get(url, { headers: getAuthHeader() });
    return convertKeysToCamelCase(response.data);
  },

  createComment: async (
    workId: string,
    chapterNum: number,
    data: CreateChapterCommentData
  ): Promise<ChapterComment> => {
    // 转换为 snake_case
    const payload = {
      content: data.content,
      location_type: data.locationType || 'chapter',
      paragraph_index: data.paragraphIndex,
      sentence_index: data.sentenceIndex,
      quoted_text: data.quotedText,
      parent_id: data.parentId,
      reply_to_user_id: data.replyToUserId,
    };
    const url = `${getBaseUrl()}/chapter-comments/works/${workId}/chapters/${chapterNum}/comments`;
    const response = await axios.post(url, payload, { headers: { ...getAuthHeader(), 'Content-Type': 'application/json' } });
    return convertKeysToCamelCase(response.data);
  },

  updateComment: async (commentId: string, content: string): Promise<ChapterComment> => {
    const url = `${getBaseUrl()}/chapter-comments/${commentId}`;
    const response = await axios.put(url, { content }, { headers: { ...getAuthHeader(), 'Content-Type': 'application/json' } });
    return convertKeysToCamelCase(response.data);
  },

  deleteComment: async (commentId: string): Promise<void> => {
    const url = `${getBaseUrl()}/chapter-comments/${commentId}`;
    await axios.delete(url, { headers: getAuthHeader() });
  },

  likeComment: async (commentId: string): Promise<LikeResponse> => {
    const url = `${getBaseUrl()}/chapter-comments/${commentId}/like`;
    const response = await axios.post(url, {}, { headers: getAuthHeader() });
    return convertKeysToCamelCase(response.data);
  },

  unlikeComment: async (commentId: string): Promise<LikeResponse> => {
    const url = `${getBaseUrl()}/chapter-comments/${commentId}/like`;
    const response = await axios.delete(url, { headers: getAuthHeader() });
    return convertKeysToCamelCase(response.data);
  },

  reportComment: async (commentId: string, data: ReportData): Promise<void> => {
    const url = `${getBaseUrl()}/chapter-comments/${commentId}/report`;
    await axios.post(url, data, { headers: { ...getAuthHeader(), 'Content-Type': 'application/json' } });
  },
};
