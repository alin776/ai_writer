/**
 * ActivityStream - ReAct模式实时活动流组件
 *
 * 显示Agent执行过程中的实时活动，包括：
 * - 意图分析
 * - 思考过程
 * - 工具调用
 * - 内容生成
 *
 * 设计：简约专业，动画流畅，状态清晰
 */

import React from 'react';
import { Brain, Wrench, Sparkles, CheckCircle, Loader2, Clock } from 'lucide-react';
import type { ActivityItem, ActivityType, ActivityStatus } from '@/types/agent';  // ✅ 从类型文件导入
import styles from './ActivityStream.module.css';

interface ActivityStreamProps {
  activities: ActivityItem[];
  className?: string;
}

/**
 * 获取活动图标
 */
const getActivityIcon = (type: ActivityType, status: ActivityStatus) => {
  const iconClass = status === 'active' ? styles.iconActive : styles.iconCompleted;

  switch (type) {
    case 'intent_analysis':
      return <Brain className={`${iconClass} ${status === 'active' ? styles.pulse : ''}`} size={18} />;
    case 'thinking':
      return <Sparkles className={`${iconClass} ${status === 'active' ? styles.pulse : ''}`} size={18} />;
    case 'tool_execution':
      return <Wrench className={`${iconClass} ${status === 'active' ? styles.spin : ''}`} size={18} />;
    case 'generating':
      return <Loader2 className={`${iconClass} ${status === 'active' ? styles.spin : ''}`} size={18} />;
    default:
      return <Sparkles className={iconClass} size={18} />;
  }
};

/**
 * 获取活动类型的中文名称
 */
const getActivityTypeName = (type: ActivityType): string => {
  const typeNames = {
    intent_analysis: '意图分析',
    thinking: '思考中',
    tool_execution: '工具调用',
    generating: '生成内容'
  };
  return typeNames[type] || type;
};

/**
 * 格式化时间差（相对于当前时间）
 */
const formatTimeAgo = (timestamp: string): string => {
  const now = new Date();
  const time = new Date(timestamp);
  const diffMs = now.getTime() - time.getTime();
  const diffSec = Math.floor(diffMs / 1000);

  if (diffSec < 1) return '刚刚';
  if (diffSec < 60) return `${diffSec}秒前`;
  if (diffSec < 3600) return `${Math.floor(diffSec / 60)}分钟前`;
  return `${Math.floor(diffSec / 3600)}小时前`;
};

/**
 * ActivityStream 组件
 */
export default function ActivityStream({ activities, className = '' }: ActivityStreamProps) {
  console.log('🟠 [ActivityStream] 渲染！activities.length =', activities.length);
  console.log('🟠 [ActivityStream] activities =', activities);

  if (activities.length === 0) {
    console.log('🟠 [ActivityStream] activities为空，返回null');
    return null;
  }

  // 统计
  const activeCount = activities.filter(a => a.status === 'active').length;
  const completedCount = activities.filter(a => a.status === 'completed').length;

  return (
    <div className={`${styles.activityStream} ${className}`}>
      {/* 头部 */}
      <div className={styles.header}>
        <h3 className={styles.title}>执行过程</h3>
        <div className={styles.stats}>
          {activeCount > 0 && (
            <span className={styles.statActive}>
              <Loader2 size={14} className={styles.spin} />
              进行中
            </span>
          )}
          {completedCount > 0 && (
            <span className={styles.statCompleted}>
              <CheckCircle size={14} />
              {completedCount}
            </span>
          )}
        </div>
      </div>

      {/* 活动列表 */}
      <div className={styles.activityList}>
        {activities.map((activity) => (
          <div
            key={activity.id}
            className={`
              ${styles.activityItem}
              ${activity.status === 'active' ? styles.active : ''}
              ${activity.status === 'completed' ? styles.completed : ''}
              ${activity.status === 'failed' ? styles.failed : ''}
            `}
          >
            {/* 左侧图标 */}
            <div className={styles.activityIcon}>
              {getActivityIcon(activity.type, activity.status)}
            </div>

            {/* 中间内容 */}
            <div className={styles.activityContent}>
              <div className={styles.activityDescription}>
                {activity.description}
              </div>

              <div className={styles.activityMeta}>
                {/* 类型标签 */}
                <span className={styles.activityType}>
                  {getActivityTypeName(activity.type)}
                </span>

                {/* 工具名称 */}
                {activity.tool && (
                  <span className={styles.toolName}>
                    {activity.tool}
                  </span>
                )}

                {/* 时间信息 */}
                <span className={styles.activityTime}>
                  <Clock size={12} />
                  {activity.status === 'completed' && activity.elapsedTime !== undefined
                    ? `${activity.elapsedTime.toFixed(1)}s`
                    : formatTimeAgo(activity.timestamp)
                  }
                </span>
              </div>
            </div>

            {/* 右侧状态 */}
            <div className={styles.activityStatus}>
              {activity.status === 'active' && (
                <Loader2 size={16} className={styles.spin} />
              )}
              {activity.status === 'completed' && (
                <CheckCircle size={16} className={styles.checkIcon} />
              )}
            </div>
          </div>
        ))}
      </div>

      {/* 进度条（可选） */}
      {activities.length > 0 && (
        <div className={styles.progressBar}>
          <div
            className={styles.progressFill}
            style={{ width: `${(completedCount / activities.length) * 100}%` }}
          />
        </div>
      )}
    </div>
  );
}
