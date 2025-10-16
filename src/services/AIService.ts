/**
 * AI 服务
 * 处理 AI 相关的 API 请求
 */
import { getAIConfig, validateAIConfig } from '@/config/ai.config';

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
  private config = getAIConfig();
  private abortController: AbortController | null = null;

  constructor() {
    // 验证配置
    const validation = validateAIConfig();
    if (!validation.valid) {
      console.warn('AI 配置验证失败:', validation.errors);
    }
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

      const apiUrl = `${this.config.apiUrl}/v1/chat/completions`;
      console.log('[AIService] API URL:', apiUrl);
      console.log('[AIService] 模型:', request.model || this.config.openai.model);

      const requestBody = {
        model: request.model || this.config.openai.model,
        messages: [
          {
            role: 'system',
            content: '你是一个专业的写作助手。用户会给你一段文本，你需要直接续写这段文本，不要添加任何前缀或说明，直接输出续写的内容即可。',
          },
          {
            role: 'user',
            content: request.prompt,
          },
        ],
        max_tokens: request.maxTokens || this.config.continue.maxTokens,
        temperature: request.temperature || this.config.continue.temperature,
        stream: true,
      };

      console.log('[AIService] 请求体:', JSON.stringify(requestBody, null, 2));

      // 创建新的 AbortController
      this.abortController = new AbortController();

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.config.apiKey}`,
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
          errorMessage = error.error?.message || error.message || errorMessage;
        } catch (e) {
          // 如果解析 JSON 失败，使用状态文本
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

      console.log('[AIService] 开始读取流式响应');

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
            const data = line.slice(6);

            // 跳过 [DONE] 信号
            if (data === '[DONE]') {
              console.log('[AIService] 收到 [DONE] 信号');
              continue;
            }

            // 跳过非 JSON 数据（如 ": OPENROUTER PROCESSING"）
            if (!data.startsWith('{')) {
              console.log('[AIService] 跳过非 JSON 数据:', data);
              continue;
            }

            try {
              const json = JSON.parse(data);
              console.log('[AIService] 解析的 JSON 对象:', json);

              // 只提取 content 字段，忽略 reasoning（思考过程）
              const content = json.choices?.[0]?.delta?.content
                           || json.choices?.[0]?.message?.content
                           || json.delta?.content
                           || json.content
                           || '';

              // 获取 reasoning 字段用于调试（但不输出）
              const reasoning = json.choices?.[0]?.delta?.reasoning || '';
              if (reasoning) {
                console.log('[AIService] 跳过 reasoning（思考过程）:', reasoning);
              }

              console.log('[AIService] 提取的 content:', content);

              if (content) {
                console.log('[AIService] 收到内容片段:', content);
                // 直接输出内容
                result += content;
                if (onChunk) {
                  console.log('[AIService] 调用 onChunk 回调');
                  onChunk(content);
                }
              } else if (!reasoning) {
                // 如果既没有 content 也没有 reasoning，说明是其他数据
                console.log('[AIService] content 为空，JSON 结构:', JSON.stringify(json, null, 2));
              }
            } catch (e) {
              console.error('[AIService] 解析 JSON 失败:', e, '原始数据:', data);
            }
          }
        }
      }

      console.log('[AIService] 总共接收到的内容长度:', result.length);
      console.log('[AIService] 原始结果:', result);

      // 最后过滤掉所有 think 标签内容
      result = this.filterThinkTags(result);
      console.log('[AIService] 过滤后结果长度:', result.length);
      console.log('[AIService] 过滤后结果:', result);

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

      console.error('OpenAI API 流式请求失败:', error);
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
    const apiUrl = `${this.config.apiUrl}/v1/chat/completions`;
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
      },
      body: JSON.stringify({
        model: request.model || this.config.openai.model,
        messages: [
          {
            role: 'system',
            content: '你是一个专业的写作助手。直接输出处理后的内容，不要添加任何前缀、说明或额外的话。',
          },
          {
            role: 'user',
            content: request.prompt,
          },
        ],
        max_tokens: request.maxTokens || this.config.openai.maxTokens,
        temperature: request.temperature || this.config.openai.temperature,
        stream: false,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error?.message || 'OpenAI API 请求失败');
    }

    const data = await response.json();
    return {
      text: data.choices[0]?.message?.content || '',
      usage: data.usage
        ? {
            promptTokens: data.usage.prompt_tokens,
            completionTokens: data.usage.completion_tokens,
            totalTokens: data.usage.total_tokens,
          }
        : undefined,
    };
  }

  /**
   * 快速 AI 补全（用于实时自动补全）
   * @param context - 上下文文本
   */
  async quickComplete(context: string): Promise<string> {
    try {
      const apiUrl = `${this.config.apiUrl}/v1/chat/completions`;
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.config.apiKey}`,
        },
        body: JSON.stringify({
          model: this.config.openai.model,
          messages: [
            {
              role: 'system',
              content: '你是一个写作助手。根据上下文，提供简短的续写建议（不超过30个字）。只输出续写内容，不要添加任何前缀或说明。',
            },
            {
              role: 'user',
              content: `继续写作：${context}`,
            },
          ],
          max_tokens: 50,
          temperature: 0.7,
        }),
      });

      if (!response.ok) {
        throw new Error('快速补全请求失败');
      }

      const data = await response.json();
      const suggestion = data.choices[0]?.message?.content || '';

      // 过滤掉 think 标签内容
      return this.filterThinkTags(suggestion).trim();
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
    const apiUrl = `${this.config.apiUrl}/v1/chat/completions`;
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
      },
      body: JSON.stringify({
        model: this.config.openai.model,
        messages: [
          {
            role: 'system',
            content: '你是一个写作助手。根据上下文，提供3个简短的续写建议，每个建议不超过15个字。',
          },
          {
            role: 'user',
            content: `上下文：${context}\n\n请提供3个续写建议：`,
          },
        ],
        max_tokens: 100,
        temperature: 0.7,
        n: 1,
      }),
    });

    if (!response.ok) {
      throw new Error('获取建议失败');
    }

    const data = await response.json();
    const text = data.choices[0]?.message?.content || '';

    // 解析返回的建议（假设返回格式为每行一个建议）
    const suggestions = text
      .split('\n')
      .filter((line: string) => line.trim())
      .map((line: string) => line.replace(/^\d+\.?\s*/, '').trim())
      .slice(0, this.config.completion.maxSuggestions);

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
    const request: AICompletionRequest = {
      prompt: `${instruction}\n\n原文：\n${text}\n\n改写后：`,
      maxTokens: 1000,
      temperature: 0.7,
    };

    const response = await this.completeSync(request);
    return response.text;
  }

  /**
   * AI 扩写
   * @param text - 要扩写的文本
   */
  async expand(text: string): Promise<string> {
    return this.rewrite(text, '请扩写以下内容，增加更多细节和描述：');
  }

  /**
   * AI 缩写/总结
   * @param text - 要缩写的文本
   */
  async summarize(text: string): Promise<string> {
    return this.rewrite(text, '请总结以下内容，保留关键信息：');
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
  async translate(text: string, targetLang: string): Promise<string> {
    return this.rewrite(text, `请将以下文本翻译成${targetLang}：`);
  }

  /**
   * 检查内容是否在 think 标签内
   */
  private isThinkContent(text: string): boolean {
    const thinkOpenCount = (text.match(/<think>/g) || []).length;
    const thinkCloseCount = (text.match(/<\/think>/g) || []).length;
    return thinkOpenCount > thinkCloseCount;
  }

  /**
   * 过滤 think 标签及其内容
   */
  private filterThinkTags(content: string): string {
    // 移除 <think> 和 </think> 标签及其之间的内容
    return content.replace(/<think>[\s\S]*?<\/think>/g, '');
  }
}

export default new AIService();
