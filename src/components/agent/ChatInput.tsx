/**
 * ChatInput - 聊天输入框组件
 *
 * 功能:
 * - 多行输入
 * - Enter发送, Shift+Enter换行
 * - 字符计数
 * - 附加上下文
 * - 内嵌模式切换
 */

import React, { useState, useRef, KeyboardEvent } from 'react';
import ModeSelector, { type AgentMode } from './ModeSelector';

interface ChatInputProps {
  onSend: (message: string, context?: any) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
  mode: AgentMode;
  onModeChange: (mode: AgentMode) => void;
}

export default function ChatInput({
  onSend,
  disabled = false,
  placeholder = '输入消息...',
  maxLength = 2000,
  mode,
  onModeChange,
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [showContext, setShowContext] = useState(false);
  const [contextText, setContextText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // 自动调整高度
  const adjustHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    adjustHeight();
  };

  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (!trimmedMessage || disabled) return;

    // 构建上下文
    const context = contextText.trim()
      ? {
          text: contextText.trim(),
          chapter_context: contextText.trim(),
          current_content: contextText.trim(),
        }
      : undefined;

    onSend(trimmedMessage, context);

    // 清空输入
    setMessage('');
    setContextText('');
    setShowContext(false);

    // 重置高度
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Enter发送, Shift+Enter换行
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const charCount = message.length;
  const isNearLimit = charCount > maxLength * 0.8;
  const isOverLimit = charCount > maxLength;

  return (
    <div className="chat-input-wrapper space-y-2">
      {/* 上下文输入区 */}
      {showContext && (
        <div className="context-input p-3 bg-gray-50 border border-gray-200 rounded-xl">
          <div className="flex items-center justify-between mb-1.5">
            <label className="text-xs font-medium text-gray-700">附加上下文（可选）</label>
            <button
              onClick={() => setShowContext(false)}
              className="text-gray-400 hover:text-gray-600 text-xs"
            >
              关闭
            </button>
          </div>
          <textarea
            value={contextText}
            onChange={(e) => setContextText(e.target.value)}
            placeholder="输入章节内容、待分析文本等..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none text-xs bg-white"
            rows={3}
          />
          <div className="text-[10px] text-gray-500 mt-1">提示: 这些内容会作为额外上下文发送给AI</div>
        </div>
      )}

      <div className="rounded-2xl border border-gray-200 bg-white shadow-sm px-4 py-3 space-y-3">
        {/* 输入区 */}
        <div className="relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder={placeholder}
            className={`w-full px-1 py-1 pr-16 text-sm min-h-[72px] resize-none bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-primary-200 ${
              disabled ? 'text-gray-400 cursor-not-allowed' : 'text-gray-800'
            } ${isOverLimit ? 'focus:ring-red-400' : ''}`}
            rows={3}
            maxLength={maxLength}
          />

          {/* 字符计数 */}
          <div
            className={`absolute right-1 bottom-1 text-[11px] ${
              isOverLimit
                ? 'text-red-500 font-semibold'
                : isNearLimit
                ? 'text-orange-500'
                : 'text-gray-400'
            }`}
          >
            {charCount}/{maxLength}
          </div>
        </div>

        {/* 工具区 */}
        <div className="flex items-center justify-between gap-3">
          <ModeSelector
            mode={mode}
            onModeChange={onModeChange}
            disabled={disabled}
            compact
            className="shrink-0"
          />

          <div className="flex items-center gap-2">
            {/* 上下文按钮 */}
            <button
              onClick={() => setShowContext(!showContext)}
              disabled={disabled}
              className={`px-3 py-2 rounded-full border border-transparent text-sm transition-colors ${
                showContext
                  ? 'bg-primary-50 text-primary-700'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
              } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
              title="添加上下文"
            >
              上下文
            </button>

            {/* 发送按钮 */}
            <button
              onClick={handleSend}
              disabled={disabled || !message.trim() || isOverLimit}
              className={`px-4 py-2 rounded-full font-medium transition-all text-sm ${
                disabled || !message.trim() || isOverLimit
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-primary-600 text-white hover:bg-primary-700 active:scale-95 shadow-sm'
              }`}
            >
              {disabled ? '...等待' : '发送'}
            </button>
          </div>
        </div>

        {/* 提示文本 */}
        <div className="text-[11px] text-gray-500 flex items-center gap-2 pt-1">
          <span>按 Enter 发送</span>
          <span className="text-gray-300">•</span>
          <span>Shift + Enter 换行</span>
        </div>
      </div>
    </div>
  );
}
