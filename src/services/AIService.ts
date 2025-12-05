/**
 * AI 鏈嶅姟 - 璋冪敤鍚庣API鐗堟湰
 * 鎵€鏈堿I鍔熻兘閫氳繃鍚庣鎺ュ彛瀹炵幇锛屾敮鎸丼SE娴佸紡鍝嶅簲
 */

export interface AICompletionRequest {
  prompt: string;
  context?: string;
  maxTokens?: number;
  temperature?: number;
  model?: string;
  // ===== Context-Aware 鍏冩暟鎹弬鏁?=====
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
    // 浣跨敤鍚庣API鍦板潃
    this.baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    console.log('[AIService] 鍒濆鍖栵紝鍚庣鍦板潃:', this.baseUrl);
  }

  /**
   * 鑾峰彇璁よ瘉 Token
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

  /**
   * 鍙栨秷褰撳墠鐨?AI 璇锋眰
   */
  cancel() {
    if (this.abortController) {
      console.log('[AIService] 鍙栨秷 AI 璇锋眰');
      this.abortController.abort();
      this.abortController = null;
    }
  }

  /**
   * AI鐢熸垚闃舵浜屽唴瀹癸紙鍒涗綔瑙勮寖鈫掓牳蹇冭瀹氾級
   * @param phase1Data - 闃舵涓€鐢ㄦ埛杈撳叆鐨?5涓瓧娈?   * @returns 闃舵浜孉I鐢熸垚鐨?7涓瓧娈?   */
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
      console.log('[AIService] 寮€濮嬬敓鎴愰樁娈典簩鍐呭');
      
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
        throw new Error(`API璇锋眰澶辫触: ${response.status}`);
      }

      const data = await response.json();
      
      // 杞崲瀛楁鍚嶏細snake_case -> camelCase
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
      console.error('[AIService] 鐢熸垚闃舵浜屽唴瀹瑰け璐?', error);
      throw error;
    }
  }

  /**
   * AI 缁啓锛堟祦寮忥級
   * @param request - 缁啓璇锋眰鍙傛暟
   * @param onChunk - 鎺ユ敹鍒版柊鏂囨湰鍧楁椂鐨勫洖璋?   */
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
        throw new Error('AI 生成已暂停');
      }

      console.error('AI API 请求失败:', error);
      throw error;
    }
  }

  /**
   * AI 缁啓锛堥潪娴佸紡锛?   * @param request - 缁啓璇锋眰鍙傛暟
   */
  async completeSync(
    request: AICompletionRequest
  ): Promise<AICompletionResponse> {
    // 浣跨敤娴佸紡API锛屽彧鏄笉浼犻€掑洖璋?    const text = await this.complete(request);
    return {
      text,
      usage: undefined,
    };
  }

  /**
   * 蹇€?AI 琛ュ叏锛堢敤浜庡疄鏃惰嚜鍔ㄨˉ鍏級
   * @param context - 涓婁笅鏂囨枃鏈?   * @param workId - 浣滃搧ID锛堝彲閫夛紝鐢ㄤ簬Context-Aware琛ュ叏锛?   * @param chapterId - 绔犺妭ID锛堝彲閫夛紝鐢ㄤ簬鍔犺浇绔犺妭姒傝锛?   */
  async quickComplete(
    context: string,
    workId?: string,
    chapterId?: string
  ): Promise<string> {
    try {
      const result = await this.complete({
        prompt: context,
        context,
        maxTokens: 100,
        // ===== Context-Aware 鍏冩暟鎹?=====
        workId,
        chapterId,
        enableRag: false,  // 自动补全默认关闭 RAG（速度优先）
      });
      return result.trim();
    } catch (error) {
      console.error('蹇€熻ˉ鍏ㄥけ璐?', error);
      return '';
    }
  }

  /**
   * 鑾峰彇 AI 寤鸿锛堢敤浜庤嚜鍔ㄨˉ鍏級
   * @param context - 涓婁笅鏂囨枃鏈?   * @param position - 鍏夋爣浣嶇疆
   */
  async getSuggestions(context: string, position: number): Promise<string[]> {
    try {
      const result = await this.complete({
        // 避免模板字符串解析问题，直接拼接
        prompt: context + '\n\n请提供3个续写建议：',
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
   * AI 鏀瑰啓/娑﹁壊
   * @param text - 瑕佹敼鍐欑殑鏂囨湰
   * @param instruction - 鏀瑰啓鎸囦护
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
        throw new Error(`API 璇锋眰澶辫触 (${response.status})`);
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
      console.error('AI 娑﹁壊澶辫触:', error);
      throw error;
    }
  }

  /**
   * AI 鎵╁啓
   * @param text - 瑕佹墿鍐欑殑鏂囨湰
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
        throw new Error(`API 璇锋眰澶辫触 (${response.status})`);
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
      console.error('AI 鎵╁啓澶辫触:', error);
      throw error;
    }
  }

  /**
   * AI 缂╁啓/鎬荤粨
   * @param text - 瑕佺缉鍐欑殑鏂囨湰
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
        throw new Error(`API 璇锋眰澶辫触 (${response.status})`);
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
      console.error('AI 鎬荤粨澶辫触:', error);
      throw error;
    }
  }

  /**
   * AI 娑﹁壊
   * @param text - 瑕佹鼎鑹茬殑鏂囨湰
   */
  async polish(text: string): Promise<string> {
    return this.rewrite(text, '璇锋鼎鑹蹭互涓嬫枃鏈紝浣垮叾鏇村姞娴佺晠鍜屼紭缇庯細');
  }

  /**
   * 棰勫姞杞藉厓鏁版嵁鍒扮紦瀛橈紙闄嶄綆棣栨鑷姩琛ュ叏寤惰繜锛?   * @param workId - 浣滃搧ID
   * @param chapterId - 绔犺妭ID
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
   * AI 缈昏瘧
   * @param text - 瑕佺炕璇戠殑鏂囨湰
   * @param targetLang - 鐩爣璇█
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
        throw new Error(`API 璇锋眰澶辫触 (${response.status})`);
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
      console.error('AI 缈昏瘧澶辫触:', error);
      throw error;
    }
  }
}

export default new AIService();


