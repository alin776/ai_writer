# AI指纹消融 - API服务文档

## 文档说明

本文档描述HumanizeService的完整实现，负责与后端API通信。

**文件路径**: `src/services/HumanizeService.ts`
**前缀说明**: HumanizeService 依赖 VITE_API_BASE_URL，请与后端挂载保持一致（如 /api 或 /api/v1）。

---

## 完整代码

```typescript
// src/services/HumanizeService.ts

import axios, { AxiosInstance } from 'axios';
import type {
  HumanizeIntensity,
  HumanizeSession,
  HumanizeHistoryResponse,
  HumanizeStatsResponse,
  UserProfile,
  UserProfileUpdateRequest,
  HumanizeStreamEvent
} from '@/types/humanize';

/**
 * HumanizeService - AI指纹消融API服务
 *
 * 功能:
 * - 用户画像管理
 * - 去痕迹改写 (流式/非流式)
 * - 历史记录查询
 * - 统计数据获取
 * - 用户反馈提交
 */
class HumanizeService {
  private api: AxiosInstance;

  constructor() {
    // 创建Axios实例
    this.api = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
      timeout: 60000, // 60秒超时
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 添加请求拦截器 - 自动添加token
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // 添加响应拦截器 - 统一错误处理
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token过期，清除本地存储并跳转登录
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // ==================== 用户画像相关 ====================

  /**
   * 获取用户画像
   * @returns 用户画像数据
   */
  async getUserProfile(): Promise<UserProfile> {
    const { data } = await this.api.get<UserProfile>('/humanize/profile');
    return data;
  }

  /**
   * 更新用户画像设置
   * @param settings 更新的设置项
   * @returns 更新后的用户画像
   */
  async updateUserProfile(
    settings: UserProfileUpdateRequest
  ): Promise<UserProfile> {
    const { data } = await this.api.put<UserProfile>(
      '/humanize/profile/settings',
      settings
    );
    return data;
  }

  // ==================== 去痕迹改写相关 ====================

  /**
   * 非流式去痕迹化（用于测试或特殊场景）
   *
   * @param text 待去痕迹的文本
   * @param intensity 改写强度
   * @param ai_function AI功能类型
   * @returns 完整的会话记录
   */
  async rewrite(
    text: string,
    intensity: HumanizeIntensity = 'medium',
    ai_function: string = 'rewrite'
  ): Promise<HumanizeSession> {
    const { data } = await this.api.post<HumanizeSession>('/humanize/rewrite', {
      text,
      intensity,
      ai_function,
    });
    return data;
  }

  /**
   * 流式去痕迹化（推荐使用）
   *
   * 使用SSE (Server-Sent Events) 协议实时接收改写内容
   *
   * @param text 待去痕迹的文本
   * @param intensity 改写强度
   * @param ai_function AI功能类型
   * @param onChunk 事件回调函数
   *
   * @example
   * ```typescript
   * await HumanizeService.rewriteStream(
   *   text,
   *   'medium',
   *   'rewrite',
   *   (event) => {
   *     if (event.type === 'chunk') {
   *       console.log('Received:', event.content);
   *     }
   *   }
   * );
   * ```
   */
  async rewriteStream(
    text: string,
    intensity: HumanizeIntensity = 'medium',
    ai_function: string = 'rewrite',
    onChunk: (event: HumanizeStreamEvent) => void
  ): Promise<void> {
    const token = localStorage.getItem('token');
    const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

    // 使用Fetch API进行SSE请求
    const response = await fetch(
      `${baseURL}/humanize/rewrite/stream`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
        body: JSON.stringify({
          text,
          intensity,
          ai_function,
        }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 读取流式响应
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) {
      throw new Error('No response body');
    }

    try {
      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        // 解码数据
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        // 解析SSE格式
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonStr = line.slice(6); // 移除 "data: " 前缀
              const event: HumanizeStreamEvent = JSON.parse(jsonStr);
              onChunk(event);
            } catch (e) {
              console.warn('Failed to parse SSE data:', line, e);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }

  // ==================== 历史记录相关 ====================

  /**
   * 获取历史记录 (分页)
   *
   * @param page 页码 (从1开始)
   * @param pageSize 每页数量
   * @returns 分页的历史记录
   */
  async getHistory(
    page: number = 1,
    pageSize: number = 20
  ): Promise<HumanizeHistoryResponse> {
    const { data } = await this.api.get<HumanizeHistoryResponse>(
      '/humanize/history',
      {
        params: { page, page_size: pageSize },
      }
    );
    return data;
  }

  /**
   * 获取单条会话详情
   *
   * @param sessionId 会话ID
   * @returns 会话详情
   */
  async getSession(sessionId: string): Promise<HumanizeSession> {
    const { data } = await this.api.get<HumanizeSession>(
      `/humanize/history/${sessionId}`
    );
    return data;
  }

  // ==================== 统计数据相关 ====================

  /**
   * 获取统计数据
   *
   * @returns 统计数据（总使用次数、接受率、平均改进等）
   */
  async getStats(): Promise<HumanizeStatsResponse> {
    const { data } = await this.api.get<HumanizeStatsResponse>('/humanize/stats');
    return data;
  }

  // ==================== 用户反馈相关 ====================

  /**
   * 提交用户反馈
   *
   * @param sessionId 会话ID
   * @param accepted 是否接受结果
   */
  async submitFeedback(sessionId: string, accepted: boolean): Promise<void> {
    await this.api.post('/humanize/feedback', {
      session_id: sessionId,
      accepted,
    });
  }
}

// 导出单例
export default new HumanizeService();
```

---

## API接口说明

### 1. 用户画像接口

#### GET /humanize/profile

获取当前用户的去痕迹画像。

**响应示例**:
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "humanize_enabled_global": true,
  "preferred_intensity": "medium",
  "total_uses": 42,
  "accept_rate": 0.85,
  "created_at": "2025-12-04T10:00:00Z"
}
```

#### PUT /humanize/profile/settings

更新用户画像设置。

**请求体**:
```json
{
  "humanize_enabled_global": true,
  "preferred_intensity": "strong",
  "display_mode": "detailed"
}
```

### 2. 去痕迹改写接口

#### POST /humanize/rewrite

非流式改写（同步返回）。

**请求体**:
```json
{
  "text": "待去痕迹的文本...",
  "intensity": "medium",
  "ai_function": "rewrite"
}
```

**响应示例**:
```json
{
  "id": "uuid",
  "score_before": 75.0,
  "score_after": 42.0,
  "improvement": 33.0,
  "processing_time": 4.5,
  "tokens_used": 2500,
  "cost": 0.001,
  "detail": {
    "original_preview": "原文前200字...",
    "humanized_preview": "改写后前200字..."
  }
}
```

#### POST /humanize/rewrite/stream

流式改写（SSE格式）。

**SSE事件格式**:
```
data: {"type": "progress", "stage": "detecting", "message": "正在检测..."}

data: {"type": "progress", "stage": "detected", "score": 75}

data: {"type": "chunk", "content": "改写的"}

data: {"type": "chunk", "content": "文本"}

data: {"type": "done", "session_id": "uuid", "improvement": 33}
```

### 3. 历史记录接口

#### GET /humanize/history

获取历史记录（分页）。

**查询参数**:
- `page`: 页码 (默认1)
- `page_size`: 每页数量 (默认20)

**响应示例**:
```json
{
  "total": 100,
  "items": [...],
  "page": 1,
  "page_size": 20
}
```

#### GET /humanize/history/{session_id}

获取单条会话详情。

### 4. 统计数据接口

#### GET /humanize/stats

获取统计数据。

**响应示例**:
```json
{
  "total_uses": 100,
  "avg_improvement": 28.5,
  "accept_rate": 0.85,
  "total_tokens": 250000,
  "total_cost": 0.125,
  "most_used_function": "rewrite"
}
```

### 5. 用户反馈接口

#### POST /humanize/feedback

提交用户反馈。

**请求体**:
```json
{
  "session_id": "uuid",
  "accepted": true
}
```

---

## 使用示例

### 1. 基础用法

```typescript
import HumanizeService from '@/services/HumanizeService';

// 获取用户画像
const profile = await HumanizeService.getUserProfile();
console.log('接受率:', profile.accept_rate);

// 非流式改写
const result = await HumanizeService.rewrite(
  '待改写的文本',
  'medium',
  'rewrite'
);
console.log('改进:', result.improvement);
```

### 2. 流式改写（推荐）

```typescript
import HumanizeService from '@/services/HumanizeService';
import type { HumanizeStreamEvent } from '@/types/humanize';

// 流式改写
await HumanizeService.rewriteStream(
  inputText,
  intensity,
  'rewrite',
  (event: HumanizeStreamEvent) => {
    switch (event.type) {
      case 'progress':
        console.log('阶段:', event.stage);
        if (event.score) {
          console.log('检测分数:', event.score);
        }
        break;

      case 'chunk':
        // 实时显示改写内容
        setOutputText((prev) => prev + event.content);
        break;

      case 'done':
        console.log('完成! session_id:', event.session_id);
        console.log('改进:', event.improvement);
        break;

      case 'error':
        console.error('错误:', event.message);
        break;
    }
  }
);
```

### 3. 在React组件中使用

```typescript
import { useState } from 'react';
import HumanizeService from '@/services/HumanizeService';

function MyComponent() {
  const [outputText, setOutputText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleRewrite = async () => {
    setIsProcessing(true);
    setOutputText('');

    try {
      await HumanizeService.rewriteStream(
        inputText,
        'medium',
        'rewrite',
        (event) => {
          if (event.type === 'chunk') {
            setOutputText((prev) => prev + event.content);
          }
        }
      );
    } catch (error) {
      console.error('改写失败:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <button onClick={handleRewrite} disabled={isProcessing}>
      开始改写
    </button>
  );
}
```

---

## 错误处理

### 常见错误码

| 状态码 | 说明 | 处理方式 |
|-------|------|---------|
| 401 | 未授权 | 自动跳转登录页 |
| 413 | 文本过大 | 提示用户减少字符数 |
| 429 | 请求过频 | 提示用户稍后重试 |
| 500 | 服务器错误 | 显示错误信息 |

### 错误处理示例

```typescript
try {
  const result = await HumanizeService.rewrite(text, 'medium');
} catch (error: any) {
  if (error.response?.status === 413) {
    showToast('error', '文本过长，请减少字符数');
  } else if (error.response?.status === 429) {
    showToast('error', '请求过于频繁，请稍后重试');
  } else {
    showToast('error', error.message || '处理失败');
  }
}
```

---

## 性能优化建议

### 1. 使用流式API

流式API可以让用户实时看到改写进度，大幅提升体验:

```typescript
// 不推荐: 非流式（需要等待完成才能看到结果）
const result = await HumanizeService.rewrite(text, 'medium');

// 推荐: 流式（实时显示）
await HumanizeService.rewriteStream(text, 'medium', 'rewrite', onChunk);
```

### 2. 缓存用户画像

```typescript
// 缓存用户画像，避免重复请求
let cachedProfile: UserProfile | null = null;

async function getProfile() {
  if (!cachedProfile) {
    cachedProfile = await HumanizeService.getUserProfile();
  }
  return cachedProfile;
}
```

### 3. 防抖处理

对于实时检测等功能，使用防抖避免频繁请求:

```typescript
import { useDebouncedCallback } from 'use-debounce';

const debouncedDetect = useDebouncedCallback(
  async (text: string) => {
    // 实时检测逻辑
  },
  500 // 500ms防抖
);
```

---

## 相关文档

- 上一篇: [类型定义](./02-类型定义.md)
- 下一篇: [主视图组件](./04-主视图组件.md)

---

**创建日期**: 2025-12-04
**最后更新**: 2025-12-04
