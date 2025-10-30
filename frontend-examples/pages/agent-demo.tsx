/**
 * Agent智能助手 - 完整示例页面
 *
 * 这是一个完整的示例，展示如何在实际项目中使用Agent组件
 */

import React, { useState } from 'react';
import AgentChatPanel from '@/components/agent/AgentChatPanel';

export default function AgentDemoPage() {
  const [activeTab, setActiveTab] = useState<'scenario-a' | 'scenario-b' | 'scenario-c' | 'scenario-d'>('scenario-a');

  // 示例数据
  const workId = 'example-work-123';
  const chapterId = 'example-chapter-456';

  // 不同场景的初始消息
  const scenarios = {
    'scenario-a': {
      title: '场景A: 帮我写第三章',
      message: '帮我写第三章，主角需要突破境界',
      description: 'Agent会自动检索章节上下文、续写内容、评估质量'
    },
    'scenario-b': {
      title: '场景B: 我想写玄幻小说',
      message: '我想写一部玄幻小说，主角是一个废柴逆袭的故事',
      description: 'Agent会规划世界观、人物设定、大纲结构'
    },
    'scenario-c': {
      title: '场景C: 分析这段文字',
      message: '分析这段文字哪里不好',
      description: 'Agent会从语言、情节、人物、节奏等维度进行专业分析'
    },
    'scenario-d': {
      title: '场景D: 我卡文了',
      message: '我卡文了，不知道该怎么继续写下去',
      description: 'Agent会分析原因、提供3个续写方向建议'
    }
  };

  return (
    <div className="agent-demo-page min-h-screen bg-gray-50">
      {/* 头部 */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🤖 Agent智能助手演示
          </h1>
          <p className="text-gray-600">
            体验AI驱动的智能写作助手 - 4个核心场景全面展示
          </p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* 左侧：场景选择 */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-sm p-4 sticky top-4">
              <h2 className="text-lg font-semibold mb-4">选择场景</h2>

              <div className="space-y-2">
                {Object.entries(scenarios).map(([key, scenario]) => (
                  <button
                    key={key}
                    onClick={() => setActiveTab(key as any)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
                      activeTab === key
                        ? 'bg-blue-500 text-white shadow-md'
                        : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                    }`}
                  >
                    <div className="font-medium">{scenario.title}</div>
                    <div className={`text-sm mt-1 ${
                      activeTab === key ? 'text-blue-100' : 'text-gray-500'
                    }`}>
                      {scenario.description}
                    </div>
                  </button>
                ))}
              </div>

              {/* 功能说明 */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h3 className="text-sm font-semibold text-gray-700 mb-3">
                  ✨ 核心功能
                </h3>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li className="flex items-start gap-2">
                    <span>✅</span>
                    <span>智能意图识别</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span>✅</span>
                    <span>上下文记忆</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span>✅</span>
                    <span>思考过程展示</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span>✅</span>
                    <span>建议操作</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span>✅</span>
                    <span>Markdown渲染</span>
                  </li>
                </ul>
              </div>

              {/* 技术栈 */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h3 className="text-sm font-semibold text-gray-700 mb-3">
                  🛠️ 技术栈
                </h3>
                <div className="flex flex-wrap gap-2">
                  {['React', 'TypeScript', 'TailwindCSS', 'Axios'].map((tech) => (
                    <span
                      key={tech}
                      className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
                    >
                      {tech}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* 右侧：Agent对话面板 */}
          <div className="lg:col-span-9">
            <div className="bg-white rounded-lg shadow-sm overflow-hidden">
              <AgentChatPanel
                workId={workId}
                chapterId={chapterId}
                key={activeTab}
              />
            </div>

            {/* 使用提示 */}
            <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-semibold text-blue-900 mb-2">💡 使用提示</h3>
              <ul className="space-y-1 text-sm text-blue-800">
                <li>• 点击快捷按钮可快速开始对话</li>
                <li>• 点击"查看思考过程"可展开Agent的执行步骤</li>
                <li>• 点击建议操作按钮可直接发送对应消息</li>
                <li>• 支持附加上下文（点击📎按钮）</li>
                <li>• 按Enter发送，Shift+Enter换行</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* 底部信息 */}
      <footer className="max-w-7xl mx-auto px-4 py-8 text-center text-sm text-gray-500">
        <p>
          Agent智能助手 v1.0 · 后端集成完成 ✅ · 前端开发完成 ✅
        </p>
        <p className="mt-2">
          查看{' '}
          <a
            href="/docs/agent"
            className="text-blue-600 hover:underline"
          >
            完整文档
          </a>
          {' '}了解更多功能
        </p>
      </footer>
    </div>
  );
}
