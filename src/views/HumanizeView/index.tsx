// src/views/HumanizeView/index.tsx

import React, { useState, useEffect, useRef } from 'react';
import { InputPanel } from './components/InputPanel';
import { OutputPanel } from './components/OutputPanel';
import { HistoryPanel } from './components/HistoryPanel';
import HumanizeService from '@/services/HumanizeService';
import type {
  HumanizeIntensity,
  HumanizeStreamEvent,
  UserProfile
} from '@/types/humanize';
import { useGlobalStore } from '@/store/globalStore';
import { useNavigate } from 'react-router-dom';

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
  const [outputText, setOutputText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStage, setCurrentStage] = useState<
    'idle' | 'detecting' | 'detected' | 'rewriting' | 'verifying' | 'done'
  >('idle');

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
  // ✅ 简化：移除打字机队列，后端已实现逐字发送（15ms/字）
  const toastShownRef = useRef<boolean>(false);
  const [renderComplete, setRenderComplete] = useState(false);

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
      abortControllerRef.current?.abort();
    };
  }, [showToast]);

  // ✅ 简化：移除前端打字机循环，后端已实现逐字发送

  const resetStreamOutput = (text: string = '') => {
    toastShownRef.current = false;
    setRenderComplete(false);
    setOutputText(text);
  };

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
          handleStreamEvent(event);
        },
        abortControllerRef.current.signal
      );
    } catch (err: any) {
      console.error('Rewrite error:', err);
      if (err?.name === 'AbortError') {
        resetStreamOutput('');
        return;
      }
      setError(err.message || '处理失败，请稍后重试');
      setCurrentStage('idle');
      showToast('error', err.message || '网络错误');
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
          setCurrentStage(event.stage as any);
        }
        if (event.score !== undefined) {
          setDetectionScore(event.score);
        }
        break;

      case 'chunk':
        // ✅ 简化：后端逐字发送，前端直接追加显示
        if (event.content) {
          setOutputText((prev) => prev + event.content);
        }
        break;

      case 'info':
        // 信息提示（跳过去痕迹）
        if (event.message) {
          resetStreamOutput(inputText); // 返回原文
          setSkipped(true);
          setCurrentStage('detected');
          showToast('info', event.message);
        }
        break;

      case 'done':
        // ✅ 简化：后端逐字发送完成后，直接标记完成
        setCurrentStage('done');
        if (event.session_id) setSessionId(event.session_id);
        if (event.improvement !== undefined) setImprovement(event.improvement);
        if (event.processing_time !== undefined) setProcessingTime(event.processing_time);
        if (event.tokens_used !== undefined) setTokensUsed(event.tokens_used);

        if (event.skipped) {
          setSkipped(true);
          setSessionId(null);
          if (!outputText) {
            resetStreamOutput(inputText);
          }
          showToast('info', '文本AI特征较低，未执行改写');
        }
        // 直接标记渲染完成（后端已逐字发送完毕）
        setRenderComplete(true);
        break;

      case 'error':
        // ✅ 简化：错误处理
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
    <div className="h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* 主工作区 - 三列布局 */}
      <div className="flex-1 overflow-auto">
        <div className="min-h-full pt-4 px-6 pb-6">
          <div className="grid grid-cols-12 gap-6 auto-rows-min">
            {/* 左列：输入面板 (40%) */}
            <div className={isHistoryCollapsed ? 'col-span-6 h-full' : 'col-span-5 h-full'}>
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

            {/* 中列：输出面板 (40%) */}
            <div className={isHistoryCollapsed ? 'col-span-6 h-full' : 'col-span-5 h-full'}>
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

            {/* 右列：历史面板 (20%) */}
            {!isHistoryCollapsed && (
              <div className="col-span-2 h-full">
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
    </div>
  );
};

export default HumanizeView;
