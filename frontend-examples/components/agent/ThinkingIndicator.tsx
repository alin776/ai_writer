/**
 * ThinkingIndicator - AI思考中指示器
 */

import React from 'react';

export default function ThinkingIndicator() {
  return (
    <div className="thinking-indicator flex items-start gap-3">
      {/* Agent头像 */}
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-semibold">
        🤖
      </div>

      {/* 思考动画 */}
      <div className="flex-1">
        <div className="bg-gray-100 rounded-2xl rounded-tl-sm px-4 py-3 inline-block">
          <div className="flex items-center gap-2">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
            <span className="text-sm text-gray-600 ml-2">AI正在思考...</span>
          </div>
        </div>
      </div>
    </div>
  );
}
