// src/views/HumanizeView/components/StatsBar.tsx

import React from 'react';
import { TrendingDown, Clock, Activity } from 'lucide-react';
import type { UserProfile } from '@/types/humanize';

interface StatsBarProps {
  userProfile: UserProfile;
}

export const StatsBar: React.FC<StatsBarProps> = ({ userProfile }) => {
  return (
    <div className="bg-white border-t border-gray-200 px-6 py-3">
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-gray-400" />
            <span className="text-gray-600">总使用:</span>
            <span className="font-semibold text-gray-900">
              {userProfile.total_uses} 次
            </span>
          </div>
          <div className="flex items-center gap-2">
            <TrendingDown className="w-4 h-4 text-green-500" />
            <span className="text-gray-600">接受率:</span>
            <span className="font-semibold text-green-600">
              {(userProfile.accept_rate * 100).toFixed(1)}%
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-blue-500" />
            <span className="text-gray-600">偏好强度:</span>
            <span className="font-semibold text-blue-600">
              {userProfile.preferred_intensity === 'light' && '轻度'}
              {userProfile.preferred_intensity === 'medium' && '中度'}
              {userProfile.preferred_intensity === 'strong' && '强度'}
              {!userProfile.preferred_intensity && '中度'}
            </span>
          </div>
        </div>
        <div className="text-xs text-gray-500">
          上次更新: {new Date(userProfile.updated_at).toLocaleString('zh-CN')}
        </div>
      </div>
    </div>
  );
};
