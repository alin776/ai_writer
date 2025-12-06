/**
 * AI 服务 - 调用后端 API 版本
 * AI 功能通过后端接口实现，支持 SSE 流式响应
 */

export interface AICompletionRequest {
  prompt: string;
  context?: string;
  maxTokens?: number;
  temperature?: number;
  model?: string;
  // ===== Context-Aware 元数据 =====
  workId?: string;
  chapterId?: string;
  enableRag?: boolean;
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
    // 使用后端 API 地址
    this.baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    console.log('[AIService] 初始化,后端地址:', this.baseUrl);
  }

  /**
   * 获取认证 Token
   */
  private getAuthToken(): string {
    const authStorage = localStorage.getItem("auth-storage");
    if (!authStorage) {
      console.error('[AIService] No auth-storage in localStorage');
      throw new Error('Not logged in, please sign in first');
    }

    try {
      const authState = JSON.parse(authStorage);
      const token = authState.state?.token;

      if (!token) {
        console.error('[AIService] No token in auth-storage');
        throw new Error('Auth token not found');
      }

      console.log('[AIService] Token retrieved successfully');
      return token;
    } catch (error) {
      console.error('[AIService] Failed to parse auth storage:', error);
      throw new Error('Auth storage parse error');
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

  async generatePhase2Content(phase1Data: {
    businessGoal?: string;
    targetAudience?: string;
    commercialBenchmark?: string;
    highConcept?: string;
    coreParadox?: string;
    dominantEmotion?: string;
    coreIpSymbols?: string;
    protagonistArc?: string;
    coreConflict?: string;
    narrativeRhythm?: string;
    writingStyle?: string;
    styleNotes?: string;
    chapterLength?: string;
    contentTaboos?: string;
  }): Promise<{
    primaryGenre?: string;
    secondaryTags?: string;
    creativeTone?: string;
    worldIntro?: string;
    mainLocations?: string;
    worldRules?: string;
    powerSystemName?: string;
    powerLevels?: string;
    powerCost?: string;
    protagonistName?: string;
    protagonistIdentity?: string;
    protagonistTraits?: string;
    protagonistGoal?: string;
    conflictDesign?: string;
    actOne?: string;
    actTwo?: string;
    actThree?: string;
  }> {
    try {
      console.log('[AIService] 开始生成阶段二内容');
      
      const apiUrl = `${this.baseUrl}/worldview/ai-guidelines/generate`;
      const token = this.getAuthToken();

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          business_goal: phase1Data.businessGoal,
          target_audience: phase1Data.targetAudience,
          commercial_benchmark: phase1Data.commercialBenchmark,
          high_concept: phase1Data.highConcept,
          core_paradox: phase1Data.coreParadox,
          dominant_emotion: phase1Data.dominantEmotion,
          core_ip_symbols: phase1Data.coreIpSymbols,
          protagonist_arc: phase1Data.protagonistArc,
          core_conflict: phase1Data.coreConflict,
          narrative_rhythm: phase1Data.narrativeRhythm,
          writing_style: phase1Data.writingStyle,
          style_notes: phase1Data.styleNotes,
          chapter_length: phase1Data.chapterLength,
          content_taboos: phase1Data.contentTaboos,
        })
      });

      if (!response.ok) {
        throw new Error(`API请求失败: ${response.status}`);
      }

      const data = await response.json();
      
      // 字段名: snake_case -> camelCase
      return {
        primaryGenre: data.primary_genre,
        secondaryTags: data.secondary_tags,
        creativeTone: data.creative_tone,
        worldIntro: data.world_intro,
        mainLocations: data.main_locations,
        worldRules: data.world_rules,
        powerSystemName: data.power_system_name,
        powerLevels: data.power_levels,
        powerCost: data.power_cost,
        protagonistName: data.protagonist_name,
        protagonistIdentity: data.protagonist_identity,
        protagonistTraits: data.protagonist_traits,
        protagonistGoal: data.protagonist_goal,
        conflictDesign: data.conflict_design,
        actOne: data.act_one,
        actTwo: data.act_two,
        actThree: data.act_three,
      };
    } catch (error) {
      console.error('[AIService] 生成阶段二内容失败', error);
      throw error;
    }
  }

  /**
   * AI 补全（流式）
   * @param request - 补全请求参数
   * @param onChunk - 接收到新文本块时的回调
   */
  async complete(
    request: AICompletionRequest,
    onChunk?: (chunk: string) => void
  ): Promise<string> {
    try {
      console.log('[AIService] Starting AI complete request');
      console.log('[AIService] Request params:', request);

      const apiUrl = `${this.baseUrl}/ai/complete`;
      const token = this.getAuthToken();

      const maxTokens = Math.max(request.maxTokens || 500, 100);
      const requestBody = {
        context: request.context || request.prompt,
        prompt: request.prompt || '续写',
        style: '',
        max_tokens: maxTokens,
        work_id: request.workId || null,
        chapter_id: request.chapterId || null,
        enable_rag: request.enableRag || false,
      };

      console.log('[AIService] Request body:', JSON.stringify(requestBody, null, 2));

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
        let errorMessage = `API请求失败 (${response.status})`;
        try {
          const error = await response.json();
          console.error('[AIService] API 错误:', error);
          errorMessage = error.detail || error.message || errorMessage;
        } catch (e) {
          errorMessage = `${errorMessage}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法获取响应流');
      }

      const decoder = new TextDecoder();
      let result = '';
      let chunkCount = 0;

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }

        const chunk = decoder.decode(value);
        console.log(`[AIService] Received raw chunk ${++chunkCount}:`, chunk.substring(0, 100));

        const lines = chunk.split('\n').filter((line) => line.trim() !== '');

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;

          const data = line.slice(6);

          if (data === '[DONE]') {
            continue;
          }

          if (data.startsWith('[ERROR]')) {
            const errorMsg = data.slice(8);
            console.error('[AIService] Server error:', errorMsg);
            throw new Error(errorMsg);
          }

          const content = data;
          console.log('[AIService] Extracted content:', content);

          if (content) {
            result += content;
            if (onChunk) {
              onChunk(content);
            }
          }
        }
      }

      this.abortController = null;

      return result;
    } catch (error) {
      this.abortController = null;

      if (error instanceof Error && error.name === 'AbortError') {
        console.log('[AIService] Request cancelled by user');
        throw new Error('AI 请求已取消');
      }

      console.error('AI API 调用失败:', error);
      throw error;
    }
  }

  /**
   * AI 补全(非流式)
   * @param request - 补全请求参数
   */
  async completeSync(
    request: AICompletionRequest
  ): Promise<AICompletionResponse> {
    // 使用流式API,只是不传回调
    const text = await this.complete(request);
    return {
      text,
      usage: undefined,
    };
  }

  /**
   * 快速 AI 补全(用于实时自动补全)
   * @param context - 上下文文本
   * @param workId - 作品ID(可选,用于Context-Aware补全)
   * @param chapterId - 章节ID(可选,用于加载章节概要)
   */
  async quickComplete(
    context: string,
    workId?: string,
    chapterId?: string,
    enableRag: boolean = true
  ): Promise<string> {
    try {
      const result = await this.complete({
        prompt: context,
        context,
        maxTokens: 100,
        // ===== Context-Aware 元数据 =====
        workId,
        chapterId,
        // 默认开启 RAG 保证一致性,可传 false 关闭
        enableRag,
      });
      return result.trim();
    } catch (error) {
      console.error('快速补全失败:', error);
      return '';
    }
  }

  /**
   * 获取 AI 建议(用于自动补全)
   * @param context - 上下文文本
   * @param position - 光标位置
   */
  async getSuggestions(context: string, position: number): Promise<string[]> {
    try {
      const result = await this.complete({
        // 模拟分析请求,直接拼接
        prompt: context + '\n\n请提供3个续写建议:',
        context,
        maxTokens: 100,
      });
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
    const apiUrl = this.baseUrl + '/ai/polish';
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
        throw new Error('无法获取响应流');
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
        throw new Error('无法获取响应流');
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
        throw new Error('无法获取响应流');
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
    return this.rewrite(text, '请润色以下文本,使其更加流畅和优美:');
  }

  /**
   * 预加载元数据到缓存(降低首次补全延迟)
   * @param workId - 作品ID
   * @param chapterId - 章节ID
   */
  async preloadMetadata(workId: string, chapterId: string): Promise<void> {
    try {
      console.log('[AIService] preload metadata:', { workId, chapterId });
      const apiUrl = `${this.baseUrl}/ai/preload-metadata`;
      const token = this.getAuthToken();

      await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ work_id: workId, chapter_id: chapterId }),
      });

      console.log('[AIService] metadata preload complete');
    } catch (error) {
      console.error('[AIService] metadata preload failed:', error);
      // preload failures are non-blocking; ignore errors
    }
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
        throw new Error('无法获取响应流');
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


