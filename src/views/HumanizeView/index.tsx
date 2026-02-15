// src/views/HumanizeView/index.tsx

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { InputPanel } from './components/InputPanel';
import { OutputPanel } from './components/OutputPanel';
import { HistoryPanel } from './components/HistoryPanel';
import HumanizeService from '@/services/HumanizeService';
import type {
  HumanizeIntensity,
  HumanizeStreamEvent,
  HumanizeStage,
  UserProfile
} from '@/types/humanize';
import { useGlobalStore } from '@/store/globalStore';
import { useNavigate } from 'react-router-dom';
import { useTypewriter } from '@/hooks/useTypewriter';

/**
 * HumanizeView - AI去痕主页面
 *
 * 布局结构:
 * ┌──────────┬──────────┬──────────────┐
 * │ 输入面板  │ 输出面板  │ 历史面板      │
 * │   40%    │   40%    │   20%        │
 * └──────────┴──────────┴──────────────┘
 */
export const HumanizeView: React.FC = () => {
  const { showToast } = useGlobalStore();
  const navigate = useNavigate();

  // ==================== 用户画像 ====================
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);

  // ==================== 输入状态 ====================
  const [inputText, setInputText] = useState('');
  const [intensity, setIntensity] = useState<HumanizeIntensity>('medium');

  // ==================== 输出状态 ====================
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStage, setCurrentStage] = useState<HumanizeStage>('idle');

  // ==================== 检测结果 ====================
  const [detectionScore, setDetectionScore] = useState<number | null>(null);

  // ==================== 会话结果 ====================
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [improvement, setImprovement] = useState<number | null>(null);
  const [processingTime, setProcessingTime] = useState<number | null>(null);
  const [tokensUsed, setTokensUsed] = useState<number | null>(null);
  const [skipped, setSkipped] = useState(false);

  // ==================== 错误状态 ====================
  const [error, setError] = useState<string | null>(null);

  // ==================== 历史刷新 ====================
  const [historyRefreshKey, setHistoryRefreshKey] = useState(0);
  const [isHistoryCollapsed, setIsHistoryCollapsed] = useState(false);

  // ==================== 中断控制 ====================
  const abortControllerRef = useRef<AbortController | null>(null);
  const toastShownRef = useRef<boolean>(false);
  const stopRequestedRef = useRef<boolean>(false); // 防止已停止请求继续处理
  const requestIdRef = useRef<string | null>(null); // 防止竞态条件
  const [renderComplete, setRenderComplete] = useState(false);

  // ==================== 打字机效果 ====================
  // 使用 useCallback 稳定 onComplete 回调，避免闭包捕获过时状态
  const handleTypewriterComplete = useCallback(() => {
    // 不依赖外部状态，直接设置 renderComplete
    // currentStage 的检查移到 useEffect 中
    setRenderComplete(true);
  }, []);

  const {
    displayText: outputText,
    appendChunk,
    markComplete,
    reset: resetTypewriter,
    isTyping,
  } = useTypewriter({
    speed: 10, // 10ms/字，与 AI 助手一致
    onComplete: handleTypewriterComplete
  });

  // ==================== 生命周期 ====================

  /**
   * 组件挂载时加载用户画像
   */
  useEffect(() => {
    const loadProfile = async () => {
      try {
        const profile = await HumanizeService.getUserProfile();
        setUserProfile(profile);
        // 使用用户偏好强度
        if (profile.preferred_intensity) {
          setIntensity(profile.preferred_intensity);
        }
      } catch (err) {
        console.error('Failed to load profile:', err);
        showToast('error', '加载用户画像失败');
      }
    };
    loadProfile();

    return () => {
      // 组件卸载时停止处理并清理资源
      stopRequestedRef.current = true;
      abortControllerRef.current?.abort();
      resetTypewriter(''); // 清理打字机状态
    };
  }, [showToast, resetTypewriter]);

  const resetStreamOutput = useCallback((text: string = '') => {
    toastShownRef.current = false;
    setRenderComplete(false);
    resetTypewriter(text);
  }, [resetTypewriter]);

  // 渲染完成后再弹成功提示
  useEffect(() => {
    if (
      currentStage === 'done' &&
      renderComplete &&
      !skipped &&
      !toastShownRef.current
    ) {
      toastShownRef.current = true;
      showToast('success', '改写完成！');
    }
  }, [currentStage, renderComplete, skipped, showToast]);

  // ==================== 核心逻辑 ====================

  /**
   * 处理改写请求
   */
  const handleRewrite = async () => {
    // 输入验证
    if (!inputText.trim()) {
      showToast('error', '请输入文本');
      return;
    }
    if (inputText.trim().length < 10) {
      showToast('error', '请输入至少10个字符');
      return;
    }

    if (inputText.length > 5000) {
      showToast('error', '文本长度超过限制（最多5000字符）');
      return;
    }

    // 生成新请求ID，用于防止竞态条件（使用时间戳+随机数确保唯一性）
    const currentRequestId = `${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;
    requestIdRef.current = currentRequestId;
    stopRequestedRef.current = false;

    // 重置状态
    setIsProcessing(true);
    setError(null);
    resetStreamOutput('');
    setDetectionScore(null);
    setSessionId(null);
    setImprovement(null);
    setProcessingTime(null);
    setTokensUsed(null);
    setSkipped(false);
    setCurrentStage('detecting');

    // 终止上一条请求，避免泄露
    abortControllerRef.current?.abort();
    abortControllerRef.current = new AbortController();

    try {
      // 流式改写
      await HumanizeService.rewriteStream(
        inputText,
        intensity,
        'rewrite',
        (event: HumanizeStreamEvent) => {
          // 过滤已停止或过期的请求事件
          if (stopRequestedRef.current || requestIdRef.current !== currentRequestId) {
            return;
          }
          handleStreamEvent(event);
        },
        abortControllerRef.current.signal
      );
    } catch (err: any) {
      console.error('Rewrite error:', err);

      // 只在是当前请求时才处理错误
      if (requestIdRef.current === currentRequestId && !stopRequestedRef.current) {
        if (err?.name === 'AbortError') {
          resetStreamOutput('');
          return;
        }
        setError(err.message || '处理失败，请稍后重试');
        setCurrentStage('idle');
        showToast('error', err.message || '网络错误');
      }
    } finally {
      setIsProcessing(false);
    }
  };

  /**
   * 处理SSE流式事件
   */
  const handleStreamEvent = (event: HumanizeStreamEvent) => {
    switch (event.type) {
      case 'progress':
        // 进度更新
        if (event.stage) {
          setCurrentStage(event.stage);
        }
        if (event.score !== undefined) {
          setDetectionScore(event.score);
        }
        break;

      case 'chunk':
        // 打字机效果：将 chunk 加入队列，逐字显示
        if (event.content) {
          appendChunk(event.content);
        }
        break;

      case 'info':
        // 信息提示（跳过去痕迹）
        if (event.message) {
          resetTypewriter(inputText); // 返回原文
          setSkipped(true);
          setCurrentStage('detected');
          setRenderComplete(true); // 直接标记完成
          showToast('info', event.message);
        }
        break;

      case 'done':
        // 标记流式输入完成
        setCurrentStage('done');
        if (event.session_id) setSessionId(event.session_id);
        if (event.improvement !== undefined) setImprovement(event.improvement);
        if (event.processing_time !== undefined) setProcessingTime(event.processing_time);
        if (event.tokens_used !== undefined) setTokensUsed(event.tokens_used);

        if (event.skipped) {
          setSkipped(true);
          setSessionId(null);
          // 无条件返回原文，因为跳过就是不改写
          resetTypewriter(inputText);
          showToast('info', '文本AI特征较低，未执行改写');
          setRenderComplete(true); // 跳过时直接完成
        } else {
          // 通知打字机流式输入已完成，等待队列清空后触发 onComplete
          markComplete();
        }
        break;

      case 'error':
        // 错误时应该 reset 而不是 flush，避免显示不完整内容
        resetTypewriter('');
        setRenderComplete(false);
        setError(event.message || '处理失败');
        setCurrentStage('idle');
        showToast('error', event.message || '处理失败');
        break;
    }
  };

  /**
   * 提交用户反馈
   */
  const handleFeedback = async (accepted: boolean) => {
    if (!sessionId) return;

    try {
      await HumanizeService.submitFeedback(sessionId, accepted);
      showToast('success', accepted ? '已接受改写结果' : '已拒绝改写结果');

      // 反馈成功后隐藏按钮以避免重复提交，但保留当前结果供用户查看/复制
      if (accepted) {
        setHistoryRefreshKey((prev) => prev + 1);
      }
      // 无论接受/拒绝，都会隐藏按钮避免重复提交
      setSessionId(null);
    } catch (err) {
      console.error('Failed to submit feedback:', err);
      showToast('error', '反馈提交失败');
    }
  };

  // ==================== 渲染 ====================

  return (
    <div className="h-full flex flex-col bg-gray-50 dark:bg-gray-900 overflow-hidden">
      {/* 主工作区 - 响应式布局 */}
      <div className="flex-1 flex flex-col min-h-0 p-4 lg:p-6">
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-6 min-h-0">
          {/* 左列：输入面板 */}
          <div className={isHistoryCollapsed ? 'lg:col-span-6 min-h-0 flex' : 'lg:col-span-5 min-h-0 flex'}>
            <InputPanel
              inputText={inputText}
              intensity={intensity}
              isProcessing={isProcessing}
              currentStage={currentStage}
              detectionScore={detectionScore}
              error={error}
              onInputChange={setInputText}
              onIntensityChange={setIntensity}
              onRewrite={handleRewrite}
            />
          </div>

          {/* 中列：输出面板 */}
          <div className={isHistoryCollapsed ? 'lg:col-span-6 min-h-0 flex' : 'lg:col-span-5 min-h-0 flex'}>
            <OutputPanel
              outputText={outputText}
              isProcessing={isProcessing}
              currentStage={currentStage}
              improvement={improvement}
              processingTime={processingTime}
              tokensUsed={tokensUsed}
              sessionId={sessionId}
              skipped={skipped}
              renderComplete={renderComplete}
              onFeedback={handleFeedback}
              isHistoryCollapsed={isHistoryCollapsed}
              onExpandHistory={() => setIsHistoryCollapsed(false)}
            />
          </div>

          {/* 右列：历史面板 - 小屏时隐藏 */}
          {!isHistoryCollapsed && (
            <div className="hidden lg:flex lg:col-span-2 min-h-0">
              <HistoryPanel
                refreshKey={historyRefreshKey}
                onOpenFullHistory={() => navigate('/humanize/history')}
                onSelectSession={(id) => navigate(`/humanize/history/${id}`)}
                onCollapse={() => setIsHistoryCollapsed(true)}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HumanizeView;
