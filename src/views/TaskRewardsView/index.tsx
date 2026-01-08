/**
 * 任务中心 - 用户界面
 */
import React, { useEffect } from 'react';
import { useUserTaskStore } from '../../stores/userTaskStore';
import { useAuthStore } from '../../store/authStore';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Progress } from '../../components/ui/progress';
import { Badge } from '../../components/ui/badge';
import { Loader2, Trophy, CheckCircle2, Clock, Coins } from 'lucide-react';
import { Alert, AlertDescription } from '../../components/ui/alert';

const TaskRewardsView: React.FC = () => {
  const { isAuthenticated } = useAuthStore();
  const {
    tasks,
    total,
    completedCount,
    totalCreditsEarned,
    isLoading,
    error,
    fetchTasks,
    clearError,
  } = useUserTaskStore();

  useEffect(() => {
    // 只在用户已登录时获取任务
    if (isAuthenticated) {
      fetchTasks();
    }
  }, [fetchTasks, isAuthenticated]);

  if (isLoading && tasks.length === 0) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto overflow-x-hidden bg-background">
      <div className="w-[1152px] mx-auto p-6">
      {/* 页面标题和统计 */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">任务中心</h1>
        <p className="text-muted-foreground">完成任务获得积分奖励</p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              总任务数
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{total}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              已完成
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{completedCount}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              累计获得积分
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <Coins className="w-5 h-5 text-yellow-500" />
              <div className="text-2xl font-bold">{totalCreditsEarned}</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 错误提示 */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* 任务列表 */}
      <div className="space-y-4">
        {tasks.map((taskItem) => {
          const { task, template, progress_percentage } = taskItem;
          const isCompleted = task.is_completed;
          const isClaimed = task.is_claimed;

          return (
            <Card key={task.id} className={isCompleted ? 'border-green-200 bg-green-50/30' : ''}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      {template.title}
                      {isCompleted && (
                        <CheckCircle2 className="w-5 h-5 text-green-600" />
                      )}
                    </CardTitle>
                    <CardDescription className="mt-1">
                      {template.description}
                    </CardDescription>
                  </div>

                  <div className="flex flex-col items-end gap-2">
                    {/* 任务类型标签 */}
                    {template.task_type === 'daily' && (
                      <Badge variant="outline" className="gap-1">
                        <Clock className="w-3 h-3" />
                        每日任务
                      </Badge>
                    )}
                    {template.task_type === 'once' && (
                      <Badge variant="outline" className="gap-1">
                        <Trophy className="w-3 h-3" />
                        一次性
                      </Badge>
                    )}

                    {/* 奖励积分 */}
                    <div className="flex items-center gap-1 text-yellow-600 font-semibold">
                      <Coins className="w-4 h-4" />
                      <span>+{template.reward_credits}</span>
                    </div>
                  </div>
                </div>
              </CardHeader>

              <CardContent>
                {/* 进度条 */}
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">
                      进度: {task.current_progress} / {task.target_progress}
                    </span>
                    <span className="font-medium">{progress_percentage}%</span>
                  </div>
                  <Progress value={progress_percentage} className="h-2" />
                </div>

                {/* 完成状态 */}
                {isCompleted && isClaimed && (
                  <div className="mt-4 flex items-center gap-2 text-sm text-green-600">
                    <CheckCircle2 className="w-4 h-4" />
                    <span>
                      已完成并领取 {task.claimed_credits} 积分
                      {task.claimed_at &&
                        ` (${new Date(task.claimed_at).toLocaleDateString()})`}
                    </span>
                  </div>
                )}

                {/* 重置提示（每日任务） */}
                {template.task_type === 'daily' && task.reset_date && (
                  <div className="mt-2 text-xs text-muted-foreground">
                    将于 {new Date(task.reset_date).toLocaleDateString()} 重置
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* 空状态 */}
      {tasks.length === 0 && !isLoading && (
        <div className="text-center py-12 text-muted-foreground">
          <Trophy className="w-16 h-16 mx-auto mb-4 opacity-20" />
          <p>暂无可用任务</p>
        </div>
      )}
      </div>
    </div>
  );
};

export default TaskRewardsView;
