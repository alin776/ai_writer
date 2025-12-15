// src/hooks/useTypewriter.ts

import { useState, useRef, useCallback, useEffect } from 'react';

interface UseTypewriterOptions {
  /** 每个字符显示间隔（毫秒），默认 10ms（约 100 字/秒） */
  speed?: number;
  /** 完成后的回调 */
  onComplete?: () => void;
}

interface UseTypewriterReturn {
  /** 当前显示的文本 */
  displayText: string;
  /** 追加内容到打字机队列 */
  appendChunk: (chunk: string) => void;
  /** 标记流式输入完成（等待队列清空后触发 onComplete） */
  markComplete: () => void;
  /** 重置打字机状态 */
  reset: (initialText?: string) => void;
  /** 是否正在打字（队列中有内容或正在处理） */
  isTyping: boolean;
  /** 强制完成（立即显示所有队列内容） */
  flush: () => void;
}

/**
 * 通用打字机效果 Hook
 *
 * 复用 AI 助手的打字机逻辑：队列 + 定时器
 *
 * @example
 * ```tsx
 * const { displayText, appendChunk, markComplete, reset, isTyping } = useTypewriter({ speed: 10 });
 *
 * // SSE 流式接收
 * onChunk: (chunk) => appendChunk(chunk),
 * onDone: () => markComplete(),
 *
 * // 渲染
 * <div>{displayText}{isTyping && <Cursor />}</div>
 * ```
 */
export function useTypewriter(options: UseTypewriterOptions = {}): UseTypewriterReturn {
  const { speed = 10, onComplete } = options;

  const [displayText, setDisplayText] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  // 队列和定时器引用
  const queueRef = useRef<string[]>([]);
  const timerRef = useRef<number | null>(null);
  const isCompleteRef = useRef(false);
  const onCompleteRef = useRef(onComplete);

  // 更新回调引用
  useEffect(() => {
    onCompleteRef.current = onComplete;
  }, [onComplete]);

  // 清理定时器
  useEffect(() => {
    return () => {
      if (timerRef.current !== null) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    };
  }, []);

  // 启动打字机定时器
  const startTimer = useCallback(() => {
    if (timerRef.current !== null) return;

    const processQueue = () => {
      // 队列为空
      if (queueRef.current.length === 0) {
        // 清理定时器（无论是否标记完成都停止，避免空转）
        if (timerRef.current !== null) {
          clearInterval(timerRef.current);
          timerRef.current = null;
        }

        // 检查是否已标记完成
        if (isCompleteRef.current) {
          setIsTyping(false);
          onCompleteRef.current?.();
        }
        // 如果未标记完成，定时器停止，等待 appendChunk 重新启动
        return;
      }

      // 从队列取出一个字符
      const char = queueRef.current.shift();
      if (char) {
        setDisplayText(prev => prev + char);
      }
    };

    timerRef.current = window.setInterval(processQueue, speed);
  }, [speed]);

  // 追加内容到队列
  const appendChunk = useCallback((chunk: string) => {
    if (!chunk) return;

    // 将 chunk 中的每个字符加入队列
    for (const char of chunk) {
      queueRef.current.push(char);
    }

    setIsTyping(true);
    startTimer();
  }, [startTimer]);

  // 标记流式输入完成
  const markComplete = useCallback(() => {
    isCompleteRef.current = true;

    // 如果队列已空且定时器未运行，直接触发回调
    if (queueRef.current.length === 0 && timerRef.current === null) {
      setIsTyping(false);
      onCompleteRef.current?.();
    }
    // 否则等待队列清空后由 processQueue 触发
  }, []);

  // 强制完成（立即显示所有队列内容）
  const flush = useCallback(() => {
    // 清理定时器
    if (timerRef.current !== null) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    // 一次性追加所有队列内容
    if (queueRef.current.length > 0) {
      const remaining = queueRef.current.join('');
      queueRef.current.length = 0; // 清空数组而不是重新分配
      setDisplayText(prev => prev + remaining);
    }

    setIsTyping(false);

    // 如果已标记完成，触发回调
    if (isCompleteRef.current) {
      onCompleteRef.current?.();
    }
  }, []);

  // 重置状态
  const reset = useCallback((initialText: string = '') => {
    // 清理定时器
    if (timerRef.current !== null) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    // 清空数组而不是重新分配（减少 GC 压力）
    queueRef.current.length = 0;
    isCompleteRef.current = false;
    setDisplayText(initialText);
    setIsTyping(false);
  }, []);

  return {
    displayText,
    appendChunk,
    markComplete,
    reset,
    isTyping,
    flush,
  };
}

export default useTypewriter;
