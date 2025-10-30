/**
 * TaskListPanel - 任务清单面板
 *
 * 显示Agent的Planning + Execution工作流中的任务列表和实时进度
 * 设计：简约专业，无emoji，使用圆圈图标
 */

import React from 'react';
import styles from './TaskListPanel.module.css';

interface Task {
  task_id: number;
  description: string;
  tool?: string;
  estimated_time?: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  elapsed_time?: number;
}

interface TaskListPanelProps {
  tasks: Task[];
  currentTaskId: number | null;
}

const TaskListPanel: React.FC<TaskListPanelProps> = ({ tasks, currentTaskId }) => {
  if (tasks.length === 0) {
    return null;
  }

  const getStatusIcon = (status: Task['status'], isActive: boolean) => {
    if (status === 'running' || isActive) {
      // 转圈加载图标
      return <div className={styles.spinnerIcon}></div>;
    } else if (status === 'completed') {
      // 实心圆圈
      return <div className={styles.completedIcon}></div>;
    } else if (status === 'failed') {
      // 失败图标
      return <div className={styles.failedIcon}></div>;
    } else {
      // 空心圆圈
      return <div className={styles.pendingIcon}></div>;
    }
  };

  const completedCount = tasks.filter(t => t.status === 'completed').length;
  const progressPercent = (completedCount / tasks.length) * 100;

  return (
    <div className={styles.taskListPanel}>
      <div className={styles.header}>
        <h3>执行计划</h3>
        <span className={styles.taskCount}>{completedCount} / {tasks.length}</span>
      </div>

      <div className={styles.taskList}>
        {tasks.map((task) => {
          const isActive = task.task_id === currentTaskId;

          return (
            <div
              key={task.task_id}
              className={`
                ${styles.taskItem}
                ${isActive ? styles.active : ''}
                ${task.status === 'completed' ? styles.completed : ''}
                ${task.status === 'failed' ? styles.failed : ''}
              `}
            >
              <div className={styles.taskIcon}>
                {getStatusIcon(task.status, isActive)}
              </div>

              <div className={styles.taskContent}>
                <div className={styles.taskDescription}>
                  {task.description}
                </div>

                <div className={styles.taskMeta}>
                  {task.tool && (
                    <span className={styles.toolName}>
                      {task.tool.replace('_tool', '')}
                    </span>
                  )}

                  {task.status === 'completed' && task.elapsed_time !== undefined && (
                    <span className={styles.elapsedTime}>
                      {task.elapsed_time.toFixed(1)}s
                    </span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className={styles.progressBar}>
        <div
          className={styles.progressFill}
          style={{ width: `${progressPercent}%` }}
        />
      </div>
    </div>
  );
};

export default TaskListPanel;
