/**
 * 订阅视图 - 敬请期待页面
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Sparkles, Clock } from 'lucide-react';

const SubscriptionView: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-950">
      {/* Header */}
      <div className="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>返回首页</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Title Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            会员订阅
          </h1>

          {/* Coming Soon Badge */}
          <div className="inline-flex items-center gap-2 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 px-6 py-3 rounded-full mb-8">
            <Clock className="w-5 h-5" />
            <span className="font-medium">敬请期待</span>
          </div>

          {/* Description */}
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            我们正在精心打造会员订阅服务，为您带来更强大的 AI 写作体验。
            <br />
            即将推出多种订阅计划，满足您的不同需求。
          </p>
        </div>

        {/* Features Preview */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center mb-4 mx-auto">
              <Sparkles className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2 text-center">
              无限创作
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
              解锁无限 AI 写作次数，让创作不受限制
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center mb-4 mx-auto">
              <Sparkles className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2 text-center">
              高级模型
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
              访问最先进的 AI 模型，提升创作质量
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center mb-4 mx-auto">
              <Sparkles className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2 text-center">
              专属功能
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
              享受会员专属功能和优先支持服务
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubscriptionView;
