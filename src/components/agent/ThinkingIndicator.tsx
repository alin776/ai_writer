/**
 * ThinkingIndicator - AI思考中指示器
 */

import React from 'react';

export default function ThinkingIndicator() {
  return (
    <div className="thinking-indicator flex items-start gap-2">
      {/* Agent头像 */}
      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-xs">
        🤖
      </div>

      {/* 思考动画 */}
      <div className="flex-1">
        <div className="bg-gray-100 rounded-2xl rounded-tl-sm px-3 py-2 inline-block">
          <div className="flex items-center gap-1.5">
            <div className="flex gap-0.5">
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
            <span className="text-xs text-gray-600 ml-1.5">AI正在思考...</span>
          </div>
        </div>
      </div>
    </div>
  );
}
