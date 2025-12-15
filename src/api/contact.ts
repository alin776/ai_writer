/**
 * 联系表单 API
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.DEV ? '/api/v1' : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1');

// 创建axios实例（联系表单不需要认证）
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30秒超时
});

// 请求类型
export interface ContactMessageRequest {
  name: string;
  email: string;
  subject: string;
  message: string;
}

// 响应类型
export interface ContactMessageResponse {
  success: boolean;
  detail: string;
}

/**
 * 发送联系消息
 */
export const sendContactMessage = async (data: ContactMessageRequest): Promise<ContactMessageResponse> => {
  const response = await api.post<ContactMessageResponse>('/contact/send-message', data);
  return response.data;
};
