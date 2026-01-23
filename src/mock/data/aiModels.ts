/**
 * Mock AI 模型数据
 */
import type { AIModel } from '@/types';

export const mockAIModels: AIModel[] = [
  {
    id: 'model-1',
    name: 'Gemini 2.5 Pro',
    type: 'gemini-2.5-pro',
    provider: 'Google',
    apiKey: 'sk-*********************abc123',
    apiEndpoint: 'https://204992.xyz:8443/v1',
    usageLimit: 10000,
    usedCount: 3547,
    inputPricePerMillion: 1.25,   // 输入：$1.25/百万tokens
    outputPricePerMillion: 10.0,  // 输出：$10.0/百万tokens
    status: 'active',
    description: '复杂任务专用模型，适合内容创作、故事规划、深度分析',
    createTime: '2025-01-01T00:00:00Z',
  },
  {
    id: 'model-2',
    name: 'Gemini 2.5 Flash',
    type: 'gemini-2.5-flash',
    provider: 'Google',
    apiKey: 'sk-*********************xyz789',
    apiEndpoint: 'https://204992.xyz:8443/v1',
    usageLimit: 50000,
    usedCount: 25680,
    inputPricePerMillion: 0.30,   // 输入：$0.30/百万tokens
    outputPricePerMillion: 2.50,  // 输出：$2.50/百万tokens
    status: 'active',
    description: '中等任务模型，适合文本润色、扩写、摘要、翻译、评审分析',
    createTime: '2025-01-01T00:00:00Z',
  },
  {
    id: 'model-3',
    name: 'Gemini 2.5 Flash Lite',
    type: 'gemini-2.5-flash-lite',
    provider: 'Google',
    apiKey: 'sk-*********************lite123',
    apiEndpoint: 'https://204992.xyz:8443/v1',
    usageLimit: 100000,
    usedCount: 45230,
    inputPricePerMillion: 0.10,   // 输入：$0.10/百万tokens
    outputPricePerMillion: 0.40,  // 输出：$0.40/百万tokens
    status: 'active',
    description: '简单任务模型，最快最便宜，适合质量评估、AI痕迹检测、文本分类',
    createTime: '2025-01-01T00:00:00Z',
  },
];
