/**
 * AgentMessage - 消息显示组件
 *
 * 支持:
 * - Markdown渲染
 * - 思考过程展开/折叠
 * - Token统计显示
 * - 复制消息
 */

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface Message {
  role: 'user' | 'agent';
  content: string;
  agentSteps?: Array<{
    step: string;
    result: string;
    usage?: {
      prompt_tokens: number;
      completion_tokens: number;
      total_tokens: number;
    };
  }>;
  metadata?: {
    intent?: string;
    timestamp: string;
  };
  timestamp: string;
}

interface AgentMessageProps {
  message: Message;
  isLatest?: boolean;
}

export default function AgentMessage({ message, isLatest = false }: AgentMessageProps) {
  const [showSteps, setShowSteps] = useState(false);
  const [copied, setCopied] = useState(false);

  const isUser = message.role === 'user';

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // 获取意图图标
  const getIntentIcon = (intent?: string) => {
    const icons: Record<string, string> = {
      writing: '✍️',
      planning: '📋',
      analysis: '🔍',
      stuck: '💫',
      general: '💬'
    };
    return intent ? icons[intent] || '💬' : '💬';
  };

  // 获取步骤图标
  const getStepIcon = (step: string) => {
    const icons: Record<string, string> = {
      context_retrieval: '📚',
      ai_generation: '✨',
      writing_complete: '✅',
      planning_generation: '📋',
      planning_complete: '✅',
      text_analysis: '🔍',
      analysis_complete: '✅',
      stuck_analysis: '💡',
      stuck_help_complete: '✅',
      general_chat: '💬'
    };
    return icons[step] || '📌';
  };

  return (
    <div
      className={`message flex gap-3 ${
        isUser ? 'justify-end' : 'justify-start'
      } ${isLatest ? 'animate-fade-in' : ''}`}
    >
      {/* Agent头像 */}
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-semibold">
            🤖
        </div>
      )}

      {/* 消息内容 */}
      <div
        className={`message-content max-w-[80%] ${
          isUser
            ? 'bg-blue-500 text-white rounded-2xl rounded-tr-sm'
            : 'bg-gray-100 text-gray-800 rounded-2xl rounded-tl-sm'
        } px-4 py-3 shadow-sm`}
      >
        {/* 用户消息 - 简单文本 */}
        {isUser && (
          <div className="whitespace-pre-wrap break-words">{message.content}</div>
        )}

        {/* Agent消息 - Markdown渲染 */}
        {!isUser && (
          <div className="prose prose-sm max-w-none">
            <ReactMarkdown
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '');
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={vscDarkPlus}
                      language={match[1]}
                      PreTag="div"
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                }
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}

        {/* Agent思考过程 */}
        {!isUser && message.agentSteps && message.agentSteps.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <button
              onClick={() => setShowSteps(!showSteps)}
              className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
            >
              <span className={`transform transition-transform ${showSteps ? 'rotate-90' : ''}`}>
                ▶
              </span>
              <span>查看思考过程 ({message.agentSteps.length}步)</span>
            </button>

            {showSteps && (
              <div className="mt-3 space-y-2">
                {message.agentSteps.map((step, idx) => (
                  <div
                    key={idx}
                    className="flex items-start gap-2 p-2 bg-yellow-50 rounded-lg text-sm"
                  >
                    <span className="text-lg">{getStepIcon(step.step)}</span>
                    <div className="flex-1">
                      <div className="font-medium text-gray-700">
                        步骤 {idx + 1}: {step.step}
                      </div>
                      <div className="text-gray-600 mt-1">{step.result}</div>

                      {/* Token统计 */}
                      {step.usage && (
                        <div className="mt-2 text-xs text-gray-500 font-mono">
                          📊 Token使用: {step.usage.total_tokens}
                          (输入: {step.usage.prompt_tokens},
                          输出: {step.usage.completion_tokens})
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* 元数据 */}
        {!isUser && message.metadata && (
          <div className="mt-2 flex items-center gap-3 text-xs text-gray-500">
            {message.metadata.intent && (
              <span className="flex items-center gap-1">
                {getIntentIcon(message.metadata.intent)}
                <span className="capitalize">{message.metadata.intent}</span>
              </span>
            )}
            <span>
              {new Date(message.metadata.timestamp).toLocaleTimeString('zh-CN', {
                hour: '2-digit',
                minute: '2-digit'
              })}
            </span>
          </div>
        )}
      </div>

      {/* 复制按钮 */}
      {!isUser && (
        <button
          onClick={handleCopy}
          className="flex-shrink-0 w-8 h-8 rounded-full hover:bg-gray-100 flex items-center justify-center text-gray-500 hover:text-gray-700 transition-colors"
          title="复制消息"
        >
          {copied ? '✓' : '📋'}
        </button>
      )}

      {/* 用户头像 */}
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-gray-500 to-gray-700 flex items-center justify-center text-white font-semibold">
          👤
        </div>
      )}
    </div>
  );
}
