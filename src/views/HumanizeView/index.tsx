// src/views/HumanizeView/index.tsx

import React, { useState, useEffect } from 'react';
import { Wand2, Info, TrendingDown, Clock, History } from 'lucide-react';
import { InputPanel } from './components/InputPanel';
import { OutputPanel } from './components/OutputPanel';
import { HistoryPanel } from './components/HistoryPanel';
import { StatsBar } from './components/StatsBar';
import HumanizeService from '@/services/HumanizeService';
import type {
  HumanizeIntensity,
  HumanizeStreamEvent,
  UserProfile
} from '@/types/humanize';
import { useGlobalStore } from '@/store/globalStore';
import { useNavigate } from 'react-router-dom';

/**
 * HumanizeView - AI去痕迹主页面
 *
 * 布局结构:
 * ┌────────────────────────────────────┐
 * │  顶部标题栏 + 快速统计              │
 * ├──────────┬──────────┬──────────────┤
 * │ 输入面板  │ 输出面板  │ 历史面板      │
 * │   40%    │   40%    │   20%        │
 * └──────────┴──────────┴──────────────┘
 * │  底部统计栏                         │
 * └────────────────────────────────────┘
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
    'idle' | 'detecting' | 'rewriting' | 'verifying' | 'done'
  >('idle');

  // ==================== 检测结果 ====================
  const [detectionScore, setDetectionScore] = useState<number | null>(null);

  // ==================== 会话结果 ====================
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [improvement, setImprovement] = useState<number | null>(null);
  const [processingTime, setProcessingTime] = useState<number | null>(null);
  const [tokensUsed, setTokensUsed] = useState<number | null>(null);

  // ==================== 错误状态 ====================
  const [error, setError] = useState<string | null>(null);

  // ==================== 历史刷新 ====================
  const [historyRefreshKey, setHistoryRefreshKey] = useState(0);
  const [isHistoryCollapsed, setIsHistoryCollapsed] = useState(false);

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
  }, [showToast]);

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

    if (inputText.length > 50000) {
      showToast('error', '文本长度超过限制（最多50000字符）');
      return;
    }

    // 重置状态
    setIsProcessing(true);
    setError(null);
    setOutputText('');
    setDetectionScore(null);
    setSessionId(null);
    setImprovement(null);
    setProcessingTime(null);
    setTokensUsed(null);
    setCurrentStage('detecting');

    try {
      // 流式改写
      await HumanizeService.rewriteStream(
        inputText,
        intensity,
        'rewrite',
        (event: HumanizeStreamEvent) => {
          handleStreamEvent(event);
        }
      );
    } catch (err: any) {
      console.error('Rewrite error:', err);
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
        // 文本片段
        if (event.content) {
          setOutputText((prev) => prev + event.content);
        }
        break;

      case 'info':
        // 信息提示（跳过去痕迹）
        if (event.message) {
          setOutputText(inputText); // 返回原文
          showToast('info', '文本AI特征较低，无需处理');
        }
        break;

      case 'done':
        // 处理完成
        setCurrentStage('done');
        if (event.session_id) setSessionId(event.session_id);
        if (event.improvement !== undefined) setImprovement(event.improvement);
        if (event.processing_time !== undefined) setProcessingTime(event.processing_time);
        if (event.tokens_used !== undefined) setTokensUsed(event.tokens_used);

        // 刷新历史记录
        setHistoryRefreshKey((prev) => prev + 1);
        showToast('success', '改写完成！');
        break;

      case 'error':
        // 错误
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

      // 如果接受，清空输入区
      if (accepted) {
        setInputText('');
        setOutputText('');
        setCurrentStage('idle');
        setSessionId(null);
      }
    } catch (err) {
      console.error('Failed to submit feedback:', err);
      showToast('error', '反馈提交失败');
    }
  };

  /**
   * 应用结果到输入区（重新改写）
   */
  const handleApplyToInput = () => {
    setInputText(outputText);
    setOutputText('');
    setCurrentStage('idle');
    setSessionId(null);
    showToast('info', '已将结果应用到输入区');
  };

  // ==================== 渲染 ====================

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* 顶部标题区 */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          {/* 左侧：标题 */}
          <div>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-600 rounded-lg flex items-center justify-center">
                <Wand2 className="w-4 h-4 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-semibold text-gray-900">AI去痕迹</h1>
                <p className="text-sm text-gray-500">将AI生成内容转化为自然表达</p>
              </div>
            </div>
          </div>

          {/* 右侧：快速统计 */}
          {userProfile && (
            <div className="flex items-center gap-6 text-sm">
              <div className="flex items-center gap-1.5">
                <TrendingDown className="w-4 h-4 text-green-600" />
                <span className="text-gray-600">接受率</span>
                <span className="font-semibold text-gray-900">
                  {(userProfile.accept_rate * 100).toFixed(0)}%
                </span>
              </div>
              <div className="flex items-center gap-1.5">
                <Clock className="w-4 h-4 text-blue-600" />
                <span className="text-gray-600">总使用</span>
                <span className="font-semibold text-gray-900">
                  {userProfile.total_uses}次
                </span>
              </div>
            </div>
          )}
        </div>

        {/* 功能说明 */}
        <div className="mt-3 flex items-start gap-2 bg-blue-50 border border-blue-100 rounded-lg p-3">
          <Info className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-blue-700">
            本工具采用<span className="font-semibold">三阶段处理</span>：
            <span className="text-blue-600">检测AI痕迹</span> →
            <span className="text-blue-600">智能改写</span> →
            <span className="text-blue-600">效果验证</span>，
            支持轻度(5%)、中度(20%)、强度(40%)三种改写强度。
          </p>
        </div>
      </div>

      {/* 主工作区 - 三列布局 */}
      <div className="flex-1 overflow-auto">
        <div className="min-h-full p-6 space-y-3">
          <div className="flex justify-end">
            <button
              onClick={() => setIsHistoryCollapsed((v) => !v)}
              className="inline-flex items-center gap-2 text-xs text-gray-600 hover:text-gray-900 border border-gray-200 px-3 py-1.5 rounded-md bg-white shadow-sm"
            >
              <History className="w-4 h-4" />
              {isHistoryCollapsed ? '展开历史记录' : '收起历史记录'}
            </button>
          </div>

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
                onFeedback={handleFeedback}
                onApplyToInput={handleApplyToInput}
              />
            </div>

            {/* 右列：历史面板 (20%) */}
            {!isHistoryCollapsed && (
              <div className="col-span-2 h-full">
                <HistoryPanel
                  refreshKey={historyRefreshKey}
                  onOpenFullHistory={() => navigate('/humanize/history')}
                  onSelectSession={(id) => navigate(`/humanize/history/${id}`)}
                />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 底部统计栏 */}
      {userProfile && <StatsBar userProfile={userProfile} />}
    </div>
  );
};

export default HumanizeView;
