/**
 * 任务奖励系统类型定义
 */

export interface TaskTemplate {
  id: string;
  task_key: string;
  title: string;
  description?: string;
  icon?: string;
  task_type: 'once' | 'daily' | 'repeatable';
  reward_credits: number;
  target_config?: string;
  is_active: boolean;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

export interface UserTask {
  id: string;
  user_id: string;
  template_id: string;
  current_progress: number;
  target_progress: number;
  is_completed: boolean;
  completed_at?: string;
  is_claimed: boolean;
  claimed_at?: string;
  claimed_credits: number;
  reset_date?: string;
  created_at: string;
  updated_at: string;
  template?: TaskTemplate;
}

export interface UserTaskWithTemplate {
  task: UserTask;
  template: TaskTemplate;
  progress_percentage: number;
}

export interface TaskListResponse {
  tasks: UserTaskWithTemplate[];
  total: number;
  completed_count: number;
  total_credits_earned: number;
}

export interface TaskTemplateUpdate {
  reward_credits?: number;
  is_active?: boolean;
  description?: string;
}
