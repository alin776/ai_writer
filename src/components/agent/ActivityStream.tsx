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

import { Brain, Wrench, Sparkles, CheckCircle, Loader2, Clock } from 'lucide-react';
import type { ActivityItem, AgentActivityType, ActivityStatus, ProgressData } from '@/types/agent';  // ✅ 从类型文件导入
import ProgressBar from './ProgressBar';  // ✅ 导入ProgressBar
import styles from './ActivityStream.module.css';

interface ActivityStreamProps {
  activities: ActivityItem[];
  progressData?: ProgressData | null;  // ✅ 新增：进度数据（可选）
  className?: string;
}

/**
 * 获取活动图标
 */
const getActivityIcon = (type: AgentActivityType, status: ActivityStatus) => {
  const iconClass = status === 'active' ? styles.iconActive : styles.iconCompleted;

  switch (type) {
    case 'intent_analysis':
      return <Brain className={`${iconClass} ${status === 'active' ? styles.pulse : ''}`} size={14} />;
    case 'thinking':
      return <Sparkles className={`${iconClass} ${status === 'active' ? styles.pulse : ''}`} size={14} />;
    case 'tool_execution':
      return <Wrench className={`${iconClass} ${status === 'active' ? styles.spin : ''}`} size={14} />;
    case 'generating':
      return <Loader2 className={`${iconClass} ${status === 'active' ? styles.spin : ''}`} size={14} />;
    default:
      return <Sparkles className={iconClass} size={14} />;
  }
};

/**
 * 获取活动类型的中文名称
 */
const getActivityTypeName = (type: AgentActivityType): string => {
  const typeNames: Record<AgentActivityType, string> = {
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
 * 验证ActivityItem数据完整性
 */
const isValidActivity = (activity: any): activity is ActivityItem => {
  return (
    activity &&
    typeof activity === 'object' &&
    typeof activity.id === 'string' &&
    typeof activity.type === 'string' &&
    typeof activity.description === 'string' &&
    typeof activity.timestamp === 'string' &&
    typeof activity.status === 'string'
  );
};

/**
 * 验证ProgressData数据完整性
 */
const isValidProgressData = (data: any): data is ProgressData => {
  return (
    data &&
    typeof data === 'object' &&
    typeof data.progress === 'number' &&
    data.progress >= 0 &&
    data.progress <= 100
  );
};

/**
 * ActivityStream 组件
 */
export default function ActivityStream({
  activities,
  progressData,  // ✅ 接收progressData
  className = ''
}: ActivityStreamProps) {
  // ✅ 类型检查和数据验证
  if (!Array.isArray(activities)) {
    if (process.env.NODE_ENV === 'development') {
      console.warn('[ActivityStream] activities不是数组:', typeof activities);
    }
    return null;
  }

  // 过滤出有效的活动项
  const validActivities = activities.filter(isValidActivity);

  if (validActivities.length !== activities.length && process.env.NODE_ENV === 'development') {
    console.warn(
      `[ActivityStream] ${activities.length - validActivities.length}个无效活动被过滤`
    );
  }

  // 空数据直接返回
  if (validActivities.length === 0) {
    return null;
  }

  // 验证progressData
  const validProgressData = progressData && isValidProgressData(progressData) ? progressData : null;

  if (progressData && !validProgressData && process.env.NODE_ENV === 'development') {
    console.warn('[ActivityStream] progressData无效:', progressData);
  }

  // 统计
  const activeCount = validActivities.filter(a => a.status === 'active').length;
  const completedCount = validActivities.filter(a => a.status === 'completed').length;

  return (
    <div className={`${styles.activityStream} ${className}`}>
      {/* 头部 */}
      <div className={styles.header}>
        <h3 className={styles.title}>执行过程</h3>
        <div className={styles.stats}>
          {activeCount > 0 && (
            <span className={styles.statActive}>
              <Loader2 size={10} className={styles.spin} />
              进行中
            </span>
          )}
          {completedCount > 0 && (
            <span className={styles.statCompleted}>
              <CheckCircle size={10} />
              {completedCount}
            </span>
          )}
        </div>
      </div>

      {/* ✅ 新增：进度条（如果有progressData）*/}
      {validProgressData && (
        <div className="mb-4 px-4 py-3 bg-blue-50 rounded-lg border border-blue-100">
          <ProgressBar
            progress={validProgressData.progress}
            etaDisplay={validProgressData.eta_display}
            etaConfidence={validProgressData.eta_confidence}
            stepDescription={validProgressData.step_description}
            currentNodeDescription={validProgressData.current_node_description}
          />
        </div>
      )}

      {/* 活动列表 */}
      <div className={styles.activityList}>
        {validActivities.map((activity) => (
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
              <div className={`${styles.activityDescription} ${activity.status === 'active' ? styles.pulse : ''}`}>
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
                  <Clock size={9} />
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
                <Loader2 size={12} className={styles.spin} />
              )}
              {activity.status === 'completed' && (
                <CheckCircle size={12} className={styles.checkIcon} />
              )}
            </div>
          </div>
        ))}
      </div>

      {/* 进度条（可选） */}
      {validActivities.length > 0 && (
        <div className={styles.progressBar}>
          <div
            className={styles.progressFill}
            style={{ width: `${(completedCount / validActivities.length) * 100}%` }}
          />
        </div>
      )}
    </div>
  );
}
