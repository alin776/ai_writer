import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Bot, Send, Loader2 } from 'lucide-react';
import { useAgentChat } from '../../hooks/useAgentChat';
import type { AgentChatRequest } from '../../types/agent';
import ModeSelector, { type AgentMode } from '../agent/ModeSelector';
import ActivityStream from '../agent/ActivityStream';  // ✅ 导入ActivityStream
import TaskListPanel from '../agent/TaskListPanel';    // ✅ 导入TaskListPanel
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import rehypeRaw from 'rehype-raw';

interface AIPanelProps {
  workId: string;
  chapterId?: string;
}

// Markdown渲染组件
const MarkdownContent: React.FC<{ content: string }> = ({ content }) => {
  return (
    <div className="text-[11px] leading-relaxed markdown-content">
      <ReactMarkdown
        rehypePlugins={[rehypeRaw]}
        components={{
          // 代码块
          code({ node, inline, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
              <SyntaxHighlighter
                style={vscDarkPlus}
                language={match[1]}
                PreTag="div"
                className="rounded-md text-[9px] my-1.5"
                {...props}
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            ) : (
              <code className="bg-zinc-100 text-zinc-800 px-1 py-0.5 rounded text-[9px] font-mono" {...props}>
                {children}
              </code>
            );
          },
          // 段落
          p({ children }) {
            return <p className="mb-1.5 last:mb-0 text-[11px]">{children}</p>;
          },
          // 标题
          h1({ children }) {
            return <h1 className="text-[12px] font-semibold mb-1.5 mt-2 first:mt-0">{children}</h1>;
          },
          h2({ children }) {
            return <h2 className="text-[11px] font-semibold mb-1.5 mt-2 first:mt-0">{children}</h2>;
          },
          h3({ children }) {
            return <h3 className="text-[11px] font-medium mb-1 mt-1.5 first:mt-0">{children}</h3>;
          },
          // 列表
          ul({ children }) {
            return <ul className="list-disc list-inside mb-1.5 space-y-0.5 text-[11px]">{children}</ul>;
          },
          ol({ children }) {
            return <ol className="list-decimal list-inside mb-1.5 space-y-0.5 text-[11px]">{children}</ol>;
          },
          li({ children }) {
            return <li className="text-[11px]">{children}</li>;
          },
          // 链接
          a({ href, children }) {
            return (
              <a href={href} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline text-[11px]">
                {children}
              </a>
            );
          },
          // 引用
          blockquote({ children }) {
            return <blockquote className="border-l-2 border-zinc-300 pl-2 my-1.5 text-zinc-600 text-[11px]">{children}</blockquote>;
          },
          // 分割线
          hr() {
            return <hr className="my-2 border-zinc-200" />;
          },
          // 表格
          table({ children }) {
            return <table className="border-collapse border border-zinc-200 my-1.5 text-[9px]">{children}</table>;
          },
          thead({ children }) {
            return <thead className="bg-zinc-50">{children}</thead>;
          },
          th({ children }) {
            return <th className="border border-zinc-200 px-1.5 py-0.5 font-semibold text-[9px]">{children}</th>;
          },
          td({ children }) {
            return <td className="border border-zinc-200 px-1.5 py-0.5 text-[9px]">{children}</td>;
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export function AIPanel({ workId, chapterId }: AIPanelProps) {
  const {
    messages,
    isLoading,
    error,
    suggestedActions,
    tasks,
    currentTaskId,
    activities,  // ✅ 添加activities
    sendMessageStream,
  } = useAgentChat();

  const [inputValue, setInputValue] = useState('');
  const [mode, setMode] = useState<AgentMode>('planning'); // ✅ Agent执行模式
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const shouldAutoScrollRef = useRef(true); // 用于追踪是否应该自动滚动

  // 🔍 调试：组件挂载/卸载监听
  useEffect(() => {
    console.log('🔴 [AIPanel] 组件已挂载！');
    return () => console.log('🔴 [AIPanel] 组件卸载');
  }, []);

  // 🔍 调试：activities变化监听
  useEffect(() => {
    console.log('🔴 [AIPanel] activities变化！', {
      length: activities.length,
      activities: activities,
      timestamp: new Date().toISOString()
    });
  }, [activities]);

  // 🔍 调试：mode变化监听
  useEffect(() => {
    console.log('🔴 [AIPanel] mode变化！', mode);
  }, [mode]);

  // 检测用户是否在底部
  const checkIfAtBottom = useCallback(() => {
    const container = messagesContainerRef.current;
    if (!container) return false;

    // 检测滚动位置是否接近底部（允许50px的误差）
    const threshold = 50;
    const isAtBottom = container.scrollHeight - container.scrollTop - container.clientHeight < threshold;
    return isAtBottom;
  }, []);

  // 滚动到底部
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  // 监听滚动事件，更新是否应该自动滚动的标志
  useEffect(() => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      shouldAutoScrollRef.current = checkIfAtBottom();
    };

    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, [checkIfAtBottom]);

  // 当消息或任务更新时，如果用户在底部就自动滚动
  useEffect(() => {
    if (shouldAutoScrollRef.current) {
      scrollToBottom();
    }
  }, [messages, tasks, scrollToBottom]);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const request: AgentChatRequest = {
      message: inputValue.trim(),
      mode,  // ✅ 使用用户选择的模式（动态）
      work_id: workId,
      chapter_id: chapterId,
      context: {
        chapter_context: chapterId ? `当前章节ID: ${chapterId}` : undefined,
      },
    };

    setInputValue('');

    // 用户发送消息时，标记应该自动滚动
    shouldAutoScrollRef.current = true;

    try {
      await sendMessageStream(request);
    } catch (err) {
      console.error('Failed to send message:', err);
    }
  };

  return (
    <div className="p-3 h-full flex flex-col">
      <div ref={messagesContainerRef} className="flex-1 mb-3 space-y-2.5 overflow-y-auto custom-scrollbar">
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
        {messages.map((message, index) => {
          // 判断是否是最后一条消息
          const isLastMessage = index === messages.length - 1;
          // 判断这条消息是否是正在streaming的agent消息
          const isStreamingMessage = isLastMessage && message.role === 'agent' && isLoading;

          // 如果是正在streaming的消息，先不渲染它，等渲染完todolist后再渲染
          if (isStreamingMessage) {
            return null;
          }

          return (
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
                {message.role === 'agent' ? (
                  <div style={{ color: 'rgb(113, 113, 122)' }}>
                    <MarkdownContent content={message.content} />
                  </div>
                ) : (
                  <p className="text-[11px] leading-relaxed whitespace-pre-wrap">
                    {message.content}
                  </p>
                )}

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
          );
        })}

        {/* ReAct模式活动流 - 显示在所有历史消息之后，streaming消息之前 */}
        {console.log('🟣 [AIPanel] 渲染检查:', {
          mode,
          activitiesLength: activities.length,
          条件满足: mode === 'react' && activities.length > 0
        })}
        {mode === 'react' && activities.length > 0 && (
          <>
            {console.log('🟣 [AIPanel] 准备渲染ActivityStream，activities.length =', activities.length)}
            <div className="flex items-start gap-2">
              <div className="h-6 w-6 rounded-full bg-zinc-900 flex items-center justify-center flex-shrink-0">
                <Bot className="h-3.5 w-3.5 text-white" />
              </div>
              <div className="flex-1">
                <ActivityStream
                  key={`activities-${activities.length}`}
                  activities={activities}
                />
              </div>
            </div>
          </>
        )}

        {/* Planning模式任务执行进度（todolist）- 显示在所有历史消息之后，streaming消息之前 */}
        {mode === 'planning' && isLoading && tasks.length > 0 && (
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

        {/* 正在streaming的agent消息 - 显示在todolist之后 */}
        {isLoading && messages.length > 0 && messages[messages.length - 1].role === 'agent' && messages[messages.length - 1].content && (
          <div className="flex items-start gap-2">
            <div className="h-6 w-6 rounded-full bg-zinc-900 flex items-center justify-center flex-shrink-0">
              <Bot className="h-3.5 w-3.5 text-white" />
            </div>
            <div className="flex-1 max-w-[85%] p-2.5 rounded-lg bg-zinc-50/70 border border-zinc-100">
              <div style={{ color: 'rgb(113, 113, 122)' }}>
                <MarkdownContent content={messages[messages.length - 1].content} />
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

      {/* 模式选择器 */}
      <div className="mb-2 flex items-center gap-2">
        <ModeSelector
          mode={mode}
          onModeChange={setMode}
          disabled={isLoading}
        />
        <span className="text-[10px] text-zinc-400">
          {mode === 'planning' ? '规划模式：先规划再执行' : 'ReAct模式：边思考边执行'}
        </span>
      </div>

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
