/**
 * ChatInput - 聊天输入框组件
 *
 * 功能:
 * - 多行输入
 * - Enter发送, Shift+Enter换行
 * - 字符计数
 * - 禁用状态
 * - 附加上下文
 */

import React, { useState, useRef, KeyboardEvent } from 'react';

interface ChatInputProps {
  onSend: (message: string, context?: any) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
}

export default function ChatInput({
  onSend,
  disabled = false,
  placeholder = '输入消息...',
  maxLength = 2000
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
          current_content: contextText.trim()
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
    <div className="chat-input-wrapper">
      {/* 上下文输入区 */}
      {showContext && (
        <div className="context-input mb-2 p-2 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between mb-1.5">
            <label className="text-xs font-medium text-gray-700">
              附加上下文（可选）
            </label>
            <button
              onClick={() => setShowContext(false)}
              className="text-gray-400 hover:text-gray-600 text-xs"
            >
              ✕
            </button>
          </div>
          <textarea
            value={contextText}
            onChange={(e) => setContextText(e.target.value)}
            placeholder="输入章节内容、待分析文本等..."
            className="w-full px-2 py-1.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-xs"
            rows={3}
          />
          <div className="text-[10px] text-gray-500 mt-1">
            提示: 这些内容会作为额外上下文发送给AI
          </div>
        </div>
      )}

      {/* 主输入框 */}
      <div className="flex items-end gap-2">
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder={placeholder}
            className={`w-full px-3 py-2 pr-16 border rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors text-xs ${
              disabled
                ? 'bg-gray-100 cursor-not-allowed'
                : 'bg-white'
            } ${
              isOverLimit
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300'
            }`}
            rows={1}
            maxLength={maxLength}
          />

          {/* 字符计数 */}
          <div
            className={`absolute right-2 bottom-2 text-[10px] ${
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

        {/* 工具按钮 */}
        <div className="flex gap-1.5">
          {/* 上下文按钮 */}
          <button
            onClick={() => setShowContext(!showContext)}
            disabled={disabled}
            className={`p-2 rounded-lg transition-colors text-sm ${
              showContext
                ? 'bg-blue-100 text-blue-600'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
            title="添加上下文"
          >
            📎
          </button>

          {/* 发送按钮 */}
          <button
            onClick={handleSend}
            disabled={disabled || !message.trim() || isOverLimit}
            className={`px-4 py-2 rounded-lg font-medium transition-all text-xs ${
              disabled || !message.trim() || isOverLimit
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600 active:scale-95'
            }`}
          >
            {disabled ? '⏳' : '发送'}
          </button>
        </div>
      </div>

      {/* 提示文本 */}
      <div className="mt-1.5 text-[10px] text-gray-500">
        <span>按 Enter 发送</span>
        <span className="mx-1.5">·</span>
        <span>Shift + Enter 换行</span>
      </div>
    </div>
  );
}
