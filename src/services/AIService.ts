/**
 * AI 服务 - 调用后端API版本
 * 所有AI功能通过后端接口实现，支持SSE流式响应
 */

export interface AICompletionRequest {
  prompt: string;
  context?: string;
  maxTokens?: number;
  temperature?: number;
  model?: string;
}

export interface AICompletionResponse {
  text: string;
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
}

export interface AIStreamChunk {
  text: string;
  done: boolean;
}

class AIService {
  private abortController: AbortController | null = null;
  private baseUrl: string;

  constructor() {
    // 使用后端API地址
    this.baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    console.log('[AIService] 初始化，后端地址:', this.baseUrl);
  }

  /**
   * 获取认证 Token
   */
  private getAuthToken(): string {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('未登录，请先登录');
    }
    return token;
  }

  /**
   * 取消当前的 AI 请求
   */
  cancel() {
    if (this.abortController) {
      console.log('[AIService] 取消 AI 请求');
      this.abortController.abort();
      this.abortController = null;
    }
  }

  /**
   * AI 续写（流式）
   * @param request - 续写请求参数
   * @param onChunk - 接收到新文本块时的回调
   */
  async complete(
    request: AICompletionRequest,
    onChunk?: (chunk: string) => void
  ): Promise<string> {
    try {
      console.log('[AIService] 开始 AI 续写请求');
      console.log('[AIService] 请求参数:', request);

      const apiUrl = `${this.baseUrl}/ai/complete`;
      const token = this.getAuthToken();

      // 构建后端API请求参数
      // 确保max_tokens不小于100（后端最小值要求）
      const maxTokens = Math.max(request.maxTokens || 500, 100);
      const requestBody = {
        context: request.context || request.prompt,
        prompt: '续写',
        style: '',
        max_tokens: maxTokens,
      };

      console.log('[AIService] 请求体:', JSON.stringify(requestBody, null, 2));

      // 创建新的 AbortController
      this.abortController = new AbortController();

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify(requestBody),
        signal: this.abortController.signal,
      });

      console.log('[AIService] Response status:', response.status);

      if (!response.ok) {
        let errorMessage = `API 请求失败 (${response.status})`;
        try {
          const error = await response.json();
          console.error('[AIService] API 错误详情:', error);
          errorMessage = error.detail || error.message || errorMessage;
        } catch (e) {
          errorMessage = `${errorMessage}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法读取响应流');
      }

      const decoder = new TextDecoder();
      let result = '';
      let chunkCount = 0;

      console.log('[AIService] 开始读取SSE流式响应');

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          console.log('[AIService] 流式响应结束');
          break;
        }

        const chunk = decoder.decode(value);
        console.log(`[AIService] 收到原始 chunk ${++chunkCount}:`, chunk.substring(0, 100));

        const lines = chunk.split('\n').filter((line) => line.trim() !== '');
        console.log(`[AIService] 解析出 ${lines.length} 行数据`);

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6); // 移除 "data: "

            // 跳过 [DONE] 信号
            if (data === '[DONE]') {
              console.log('[AIService] 收到 [DONE] 信号');
              continue;
            }

            // 检查错误
            if (data.startsWith('[ERROR]')) {
              const errorMsg = data.slice(8);
              console.error('[AIService] 服务器错误:', errorMsg);
              throw new Error(errorMsg);
            }

            // 直接使用内容（后端已经过滤了think标签）
            const content = data;
            console.log('[AIService] 提取的 content:', content);

            if (content) {
              console.log('[AIService] 收到内容片段:', content);
              result += content;
              if (onChunk) {
                console.log('[AIService] 调用 onChunk 回调');
                onChunk(content);
              }
            }
          }
        }
      }

      console.log('[AIService] 总共接收到的内容长度:', result.length);
      console.log('[AIService] 最终结果:', result);

      // 清除 AbortController
      this.abortController = null;

      return result;
    } catch (error) {
      // 清除 AbortController
      this.abortController = null;

      // 如果是取消请求,抛出特殊错误
      if (error instanceof Error && error.name === 'AbortError') {
        console.log('[AIService] 请求已被用户取消');
        throw new Error('AI 生成已暂停');
      }

      console.error('AI API 请求失败:', error);
      throw error;
    }
  }

  /**
   * AI 续写（非流式）
   * @param request - 续写请求参数
   */
  async completeSync(
    request: AICompletionRequest
  ): Promise<AICompletionResponse> {
    // 使用流式API，只是不传递回调
    const text = await this.complete(request);
    return {
      text,
      usage: undefined,
    };
  }

  /**
   * 快速 AI 补全（用于实时自动补全）
   * @param context - 上下文文本
   */
  async quickComplete(context: string): Promise<string> {
    try {
      const result = await this.complete({
        prompt: context,
        context,
        maxTokens: 100,
      });
      return result.trim();
    } catch (error) {
      console.error('快速补全失败:', error);
      return '';
    }
  }

  /**
   * 获取 AI 建议（用于自动补全）
   * @param context - 上下文文本
   * @param position - 光标位置
   */
  async getSuggestions(context: string, position: number): Promise<string[]> {
    try {
      const result = await this.complete({
        prompt: `${context}\n\n请提供3个续写建议：`,
        context,
        maxTokens: 100,
      });

      // 解析返回的建议
      const suggestions = result
        .split('\n')
        .filter((line: string) => line.trim())
        .map((line: string) => line.replace(/^\d+\.?\s*/, '').trim())
        .slice(0, 3);

      return suggestions;
    } catch (error) {
      console.error('Get suggestions error:', error);
      return [];
    }
  }

  /**
   * AI 改写/润色
   * @param text - 要改写的文本
   * @param instruction - 改写指令
   */
  async rewrite(text: string, instruction: string): Promise<string> {
    const apiUrl = `${this.baseUrl}/ai/polish`;
    const token = this.getAuthToken();

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`API 请求失败 (${response.status})`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法读取响应流');
      }

      const decoder = new TextDecoder();
      let result = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter((line) => line.trim() !== '');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            if (data.startsWith('[ERROR]')) {
              throw new Error(data.slice(8));
            }
            result += data;
          }
        }
      }

      return result;
    } catch (error) {
      console.error('AI 润色失败:', error);
      throw error;
    }
  }

  /**
   * AI 扩写
   * @param text - 要扩写的文本
   */
  async expand(text: string): Promise<string> {
    const apiUrl = `${this.baseUrl}/ai/expand`;
    const token = this.getAuthToken();

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`API 请求失败 (${response.status})`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法读取响应流');
      }

      const decoder = new TextDecoder();
      let result = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter((line) => line.trim() !== '');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            if (data.startsWith('[ERROR]')) {
              throw new Error(data.slice(8));
            }
            result += data;
          }
        }
      }

      return result;
    } catch (error) {
      console.error('AI 扩写失败:', error);
      throw error;
    }
  }

  /**
   * AI 缩写/总结
   * @param text - 要缩写的文本
   */
  async summarize(text: string): Promise<string> {
    const apiUrl = `${this.baseUrl}/ai/summarize`;
    const token = this.getAuthToken();

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`API 请求失败 (${response.status})`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法读取响应流');
      }

      const decoder = new TextDecoder();
      let result = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter((line) => line.trim() !== '');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            if (data.startsWith('[ERROR]')) {
              throw new Error(data.slice(8));
            }
            result += data;
          }
        }
      }

      return result;
    } catch (error) {
      console.error('AI 总结失败:', error);
      throw error;
    }
  }

  /**
   * AI 润色
   * @param text - 要润色的文本
   */
  async polish(text: string): Promise<string> {
    return this.rewrite(text, '请润色以下文本，使其更加流畅和优美：');
  }

  /**
   * AI 翻译
   * @param text - 要翻译的文本
   * @param targetLang - 目标语言
   */
  async translate(text: string, targetLang: string = 'auto'): Promise<string> {
    const apiUrl = `${this.baseUrl}/ai/translate`;
    const token = this.getAuthToken();

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({ text, target_lang: targetLang }),
      });

      if (!response.ok) {
        throw new Error(`API 请求失败 (${response.status})`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法读取响应流');
      }

      const decoder = new TextDecoder();
      let result = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter((line) => line.trim() !== '');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            if (data.startsWith('[ERROR]')) {
              throw new Error(data.slice(8));
            }
            result += data;
          }
        }
      }

      return result;
    } catch (error) {
      console.error('AI 翻译失败:', error);
      throw error;
    }
  }
}

export default new AIService();
