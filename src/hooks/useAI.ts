/**
 * AI Hook
 * 提供 AI 功能的 React Hook
 */
import { useState, useCallback } from 'react';
import AIService, {
  AICompletionRequest,
  AICompletionResponse,
} from '@/services/AIService';

export interface UseAIOptions {
  onError?: (error: Error) => void;
}

export interface UseAIReturn {
  // 状态
  loading: boolean;
  error: Error | null;
  streaming: boolean;

  // AI 续写（流式）
  complete: (
    request: AICompletionRequest,
    onChunk?: (chunk: string) => void
  ) => Promise<string>;

  // AI 续写（同步）
  completeSync: (request: AICompletionRequest) => Promise<AICompletionResponse>;

  // 获取建议
  getSuggestions: (context: string, position: number) => Promise<string[]>;

  // 改写/润色
  rewrite: (text: string, instruction: string) => Promise<string>;

  // 扩写
  expand: (text: string) => Promise<string>;

  // 缩写/总结
  summarize: (text: string) => Promise<string>;

  // 润色
  polish: (text: string) => Promise<string>;

  // 翻译
  translate: (text: string, targetLang: string) => Promise<string>;

  // 取消当前请求
  cancel: () => void;

  // 清除错误
  clearError: () => void;
}

/**
 * useAI Hook
 * 提供 AI 相关功能
 */
export function useAI(options?: UseAIOptions): UseAIReturn {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [streaming, setStreaming] = useState(false);

  const handleError = useCallback(
    (err: Error) => {
      setError(err);
      if (options?.onError) {
        options.onError(err);
      }
    },
    [options]
  );

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const cancel = useCallback(() => {
    AIService.cancel();
    setLoading(false);
    setStreaming(false);
  }, []);

  const complete = useCallback(
    async (
      request: AICompletionRequest,
      onChunk?: (chunk: string) => void
    ): Promise<string> => {
      setLoading(true);
      setStreaming(true);
      setError(null);

      try {
        const result = await AIService.complete(request, onChunk);
        return result;
      } catch (err) {
        const error = err instanceof Error ? err : new Error('AI 请求失败');
        handleError(error);
        throw error;
      } finally {
        setLoading(false);
        setStreaming(false);
      }
    },
    [handleError]
  );

  const completeSync = useCallback(
    async (request: AICompletionRequest): Promise<AICompletionResponse> => {
      setLoading(true);
      setError(null);

      try {
        const result = await AIService.completeSync(request);
        return result;
      } catch (err) {
        const error = err instanceof Error ? err : new Error('AI 请求失败');
        handleError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [handleError]
  );

  const getSuggestions = useCallback(
    async (context: string, position: number): Promise<string[]> => {
      setError(null);

      try {
        const suggestions = await AIService.getSuggestions(context, position);
        return suggestions;
      } catch (err) {
        const error = err instanceof Error ? err : new Error('获取建议失败');
        handleError(error);
        return [];
      }
    },
    [handleError]
  );

  const rewrite = useCallback(
    async (text: string, instruction: string): Promise<string> => {
      setLoading(true);
      setError(null);

      try {
        const result = await AIService.rewrite(text, instruction);
        return result;
      } catch (err) {
        const error = err instanceof Error ? err : new Error('AI 改写失败');
        handleError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [handleError]
  );

  const expand = useCallback(
    async (text: string): Promise<string> => {
      setLoading(true);
      setError(null);

      try {
        const result = await AIService.expand(text);
        return result;
      } catch (err) {
        const error = err instanceof Error ? err : new Error('AI 扩写失败');
        handleError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [handleError]
  );

  const summarize = useCallback(
    async (text: string): Promise<string> => {
      setLoading(true);
      setError(null);

      try {
        const result = await AIService.summarize(text);
        return result;
      } catch (err) {
        const error = err instanceof Error ? err : new Error('AI 总结失败');
        handleError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [handleError]
  );

  const polish = useCallback(
    async (text: string): Promise<string> => {
      setLoading(true);
      setError(null);

      try {
        const result = await AIService.polish(text);
        return result;
      } catch (err) {
        const error = err instanceof Error ? err : new Error('AI 润色失败');
        handleError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [handleError]
  );

  const translate = useCallback(
    async (text: string, targetLang: string): Promise<string> => {
      setLoading(true);
      setError(null);

      try {
        const result = await AIService.translate(text, targetLang);
        return result;
      } catch (err) {
        const error = err instanceof Error ? err : new Error('AI 翻译失败');
        handleError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [handleError]
  );

  return {
    loading,
    error,
    streaming,
    complete,
    completeSync,
    getSuggestions,
    rewrite,
    expand,
    summarize,
    polish,
    translate,
    cancel,
    clearError,
  };
}
