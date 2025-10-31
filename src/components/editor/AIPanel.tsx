import React, { useState, useRef, useEffect } from 'react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Bot, Send, Loader2 } from 'lucide-react';
import { useAgentChat } from '../../hooks/useAgentChat';
import type { AgentChatRequest } from '../../types/agent';

interface AIPanelProps {
  workId: string;
  chapterId?: string;
}

export function AIPanel({ workId, chapterId }: AIPanelProps) {
  const {
    messages,
    isLoading,
    error,
    suggestedActions,
    tasks,
    currentTaskId,
    sendMessageStream,
  } = useAgentChat();

  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, tasks]);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const request: AgentChatRequest = {
      message: inputValue.trim(),
      work_id: workId,
      chapter_id: chapterId,
      context: {
        chapter_context: chapterId ? `当前章节ID: ${chapterId}` : undefined,
      },
    };

    setInputValue('');

    try {
      await sendMessageStream(request);
    } catch (err) {
      console.error('Failed to send message:', err);
    }
  };

  return (
    <div className="p-3 h-full flex flex-col">
      <div className="flex-1 mb-3 space-y-2.5 overflow-y-auto custom-scrollbar">
        {/* 欢迎消息 */}
        {messages.length === 0 && (
          <div className="flex items-start gap-2">
            <div className="h-6 w-6 rounded-full bg-zinc-900 flex items-center justify-center flex-shrink-0">
              <Bot className="h-3.5 w-3.5 text-white" />
            </div>
            <div className="flex-1 p-2.5 rounded-lg bg-zinc-50/70 border border-zinc-100">
              <p className="text-[11px] leading-relaxed text-zinc-500">
                你好！我是你的写作助手。我可以帮你续写故事情节、优化文字表达、分析人物关系，以及提供创作建议。
              </p>
            </div>
          </div>
        )}

        {/* 消息列表 */}
        {messages.map((message, index) => (
          <div key={index} className={`flex items-start gap-2 ${message.role === 'user' ? 'justify-end' : ''}`}>
            {message.role === 'agent' && (
              <div className="h-6 w-6 rounded-full bg-zinc-900 flex items-center justify-center flex-shrink-0">
                <Bot className="h-3.5 w-3.5 text-white" />
              </div>
            )}

            <div
              className={`flex-1 max-w-[85%] p-2.5 rounded-lg ${
                message.role === 'user'
                  ? 'bg-zinc-800 text-zinc-50 shadow-sm ml-auto'
                  : 'bg-zinc-50/70 border border-zinc-100'
              }`}
            >
              <p className="text-[11px] leading-relaxed whitespace-pre-wrap" style={{ color: message.role === 'user' ? 'inherit' : 'rgb(113, 113, 122)' }}>
                {message.content}
              </p>

              {/* Agent步骤展示（可选） */}
              {message.role === 'agent' && message.agentSteps && message.agentSteps.length > 0 && (
                <div className="mt-2 pt-2 border-t border-zinc-200/50">
                  <details className="text-[10px] text-zinc-400">
                    <summary className="cursor-pointer hover:text-zinc-600">查看执行步骤</summary>
                    <div className="mt-1 space-y-1">
                      {message.agentSteps.map((step, idx) => (
                        <div key={idx} className="pl-2 border-l-2 border-zinc-200">
                          <div className="font-medium">{step.step}</div>
                          <div className="text-zinc-500">{step.result}</div>
                        </div>
                      ))}
                    </div>
                  </details>
                </div>
              )}
            </div>
          </div>
        ))}

        {/* 任务执行进度 */}
        {isLoading && tasks.length > 0 && (
          <div className="flex items-start gap-2">
            <div className="h-6 w-6 rounded-full bg-zinc-900 flex items-center justify-center flex-shrink-0">
              <Bot className="h-3.5 w-3.5 text-white" />
            </div>
            <div className="flex-1 space-y-3">
              {/* 标题与进度 */}
              <div className="flex items-center gap-2">
                <span className="text-[11px] text-zinc-400">执行中</span>
                <div className="flex-1 h-px bg-zinc-200"></div>
                <span className="text-[10px] text-zinc-300 font-mono">
                  {tasks.filter(t => t.status === 'completed').length}/{tasks.length}
                </span>
              </div>

              {/* 步骤列表 */}
              <div className="space-y-2">
                {tasks.map((task) => (
                  <div key={task.task_id} className="flex items-start gap-2.5">
                    {/* 状态指示器 */}
                    {task.status === 'completed' ? (
                      <div className="h-1 w-1 rounded-full bg-zinc-300 flex-shrink-0 mt-1.5"></div>
                    ) : task.status === 'running' ? (
                      <div className="relative flex-shrink-0 mt-1.5 w-3 h-3 flex items-center justify-center">
                        <div className="absolute inset-0 rounded-full border border-zinc-900 animate-[ripple_2s_ease-out_infinite]"></div>
                        <div className="h-1 w-1 rounded-full bg-zinc-900 relative z-10"></div>
                      </div>
                    ) : (
                      <div className="h-1 w-1 rounded-full bg-zinc-200 flex-shrink-0 mt-1.5"></div>
                    )}

                    <div className="flex-1 min-w-0 flex items-baseline justify-between gap-2">
                      <p className={`text-[11px] leading-relaxed ${
                        task.status === 'running' ? 'text-zinc-700' : 'text-zinc-400'
                      }`}>
                        {task.description}
                      </p>
                      {task.status === 'completed' && task.elapsed_time !== undefined && (
                        <span className="text-[10px] text-zinc-300 font-mono flex-shrink-0">
                          {task.elapsed_time.toFixed(1)}s
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* 进度条 */}
              <div className="relative h-px bg-zinc-100 overflow-hidden">
                <div
                  className="absolute left-0 top-0 h-full bg-zinc-400 transition-all duration-500"
                  style={{ width: `${(tasks.filter(t => t.status === 'completed').length / tasks.length) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        )}

        {/* 思考状态（无任务时） */}
        {isLoading && tasks.length === 0 && (
          <div className="flex items-start gap-2">
            <div className="h-6 w-6 rounded-full bg-zinc-900 flex items-center justify-center flex-shrink-0">
              <Bot className="h-3.5 w-3.5 text-white" />
            </div>
            <div className="flex-1 p-2.5 rounded-lg bg-zinc-50/70 border border-zinc-100">
              <div className="flex items-center gap-1.5 h-5">
                <div className="w-1 h-1 rounded-full bg-zinc-400 animate-[bounce_1.4s_ease-in-out_infinite]"></div>
                <div className="w-1 h-1 rounded-full bg-zinc-400 animate-[bounce_1.4s_ease-in-out_0.2s_infinite]"></div>
                <div className="w-1 h-1 rounded-full bg-zinc-400 animate-[bounce_1.4s_ease-in-out_0.4s_infinite]"></div>
              </div>
            </div>
          </div>
        )}

        {/* 错误提示 */}
        {error && (
          <div className="flex items-start gap-2">
            <div className="h-6 w-6 rounded-full bg-red-500 flex items-center justify-center flex-shrink-0">
              <Bot className="h-3.5 w-3.5 text-white" />
            </div>
            <div className="flex-1 p-2.5 rounded-lg bg-red-50 border border-red-200">
              <p className="text-[11px] leading-relaxed text-red-600">
                ❌ {error}
              </p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* 建议操作 */}
      {suggestedActions.length > 0 && !isLoading && (
        <div className="mb-2 flex flex-wrap gap-1.5">
          {suggestedActions.map((action, idx) => (
            <button
              key={idx}
              onClick={() => {
                setInputValue(action);
              }}
              className="px-2 py-1 text-[10px] bg-zinc-100 hover:bg-zinc-200 text-zinc-600 rounded transition-colors"
            >
              {action}
            </button>
          ))}
        </div>
      )}

      {/* 输入框 */}
      <div className="flex gap-2">
        <Input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="输入问题或指令..."
          className="flex-1 h-8 text-[11px] border-zinc-200 focus-visible:ring-1 focus-visible:ring-zinc-300 transition-all"
          disabled={isLoading}
        />
        <Button
          onClick={handleSend}
          disabled={isLoading || !inputValue.trim()}
          className="h-8 w-8 p-0 bg-zinc-900 hover:bg-zinc-800 transition-all disabled:opacity-50"
        >
          {isLoading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Send className="h-3.5 w-3.5" />}
        </Button>
      </div>
    </div>
  );
}
