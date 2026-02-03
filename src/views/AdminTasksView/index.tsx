/**
 * 管理员任务配置界面
 */
import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Switch } from '../../components/ui/switch';
import { Label } from '../../components/ui/label';
import { Loader2, Save, Settings2, Coins, Eye, EyeOff } from 'lucide-react';
import { Alert, AlertDescription } from '../../components/ui/alert';
import { getAllTemplates, updateTemplate } from '../../api/userTasks';
import { TaskTemplate, TaskTemplateUpdate } from '../../types/userTask';

const AdminTasksView: React.FC = () => {
  const [templates, setTemplates] = useState<TaskTemplate[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [savingId, setSavingId] = useState<string | null>(null);

  // 本地编辑状态
  const [editValues, setEditValues] = useState<Record<string, TaskTemplateUpdate>>({});

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getAllTemplates();
      setTemplates(data);
      // 初始化编辑值
      const initialValues: Record<string, TaskTemplateUpdate> = {};
      data.forEach((template) => {
        initialValues[template.id] = {
          reward_credits: template.reward_credits,
          is_active: template.is_active,
          description: template.description,
        };
      });
      setEditValues(initialValues);
    } catch (err: any) {
      setError(err.response?.data?.detail || '获取任务模板失败');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdate = async (templateId: string) => {
    setSavingId(templateId);
    setError(null);
    setSuccess(null);
    try {
      const updateData = editValues[templateId];
      const updated = await updateTemplate(templateId, updateData);

      // 更新本地状态
      setTemplates((prev) =>
        prev.map((t) => (t.id === templateId ? updated : t))
      );

      setSuccess('任务配置已更新');
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) {
      setError(err.response?.data?.detail || '更新失败');
    } finally {
      setSavingId(null);
    }
  };

  const handleValueChange = (templateId: string, field: keyof TaskTemplateUpdate, value: any) => {
    setEditValues((prev) => ({
      ...prev,
      [templateId]: {
        ...prev[templateId],
        [field]: value,
      },
    }));
  };

  const getTaskTypeLabel = (type: string) => {
    switch (type) {
      case 'daily':
        return '每日任务';
      case 'once':
        return '一次性任务';
      case 'repeatable':
        return '可重复任务';
      default:
        return type;
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-6 pb-6 max-w-6xl">
      <div className="sticky top-0 z-10 bg-gray-50 dark:bg-gray-900 pt-6">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Settings2 className="w-8 h-8 text-primary" />
            <h1 className="text-3xl font-bold">任务配置管理</h1>
          </div>
          <p className="text-muted-foreground">管理系统任务及奖励积分</p>
        </div>
      </div>

      {/* 成功提示 */}
      {success && (
        <Alert className="mb-6 border-green-200 bg-green-50">
          <AlertDescription className="text-green-800">{success}</AlertDescription>
        </Alert>
      )}

      {/* 错误提示 */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* 任务模板列表 */}
      <div className="space-y-6">
        {templates.map((template) => {
          const editValue = editValues[template.id] || {};
          const isSaving = savingId === template.id;

          return (
            <Card key={template.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-3">
                      <span className="text-2xl">
                        {template.icon === 'edit' && '✍️'}
                        {template.icon === 'image' && '🖼️'}
                        {template.icon === 'user' && '✨'}
                      </span>
                      {template.title}
                    </CardTitle>
                    <CardDescription className="mt-2">
                      任务Key: <code className="text-xs bg-gray-100 px-2 py-1 rounded">{template.task_key}</code>
                      <span className="ml-4">类型: {getTaskTypeLabel(template.task_type)}</span>
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="space-y-6">
                {/* 任务描述 */}
                <div className="space-y-2">
                  <Label htmlFor={`desc-${template.id}`}>任务描述</Label>
                  <Input
                    id={`desc-${template.id}`}
                    value={editValue.description || ''}
                    onChange={(e) =>
                      handleValueChange(template.id, 'description', e.target.value)
                    }
                    placeholder="任务描述"
                  />
                </div>

                {/* 奖励积分 */}
                <div className="space-y-2">
                  <Label htmlFor={`credits-${template.id}`} className="flex items-center gap-2">
                    <Coins className="w-4 h-4 text-yellow-600" />
                    奖励积分
                  </Label>
                  <Input
                    id={`credits-${template.id}`}
                    type="number"
                    min="0"
                    value={editValue.reward_credits || 0}
                    onChange={(e) =>
                      handleValueChange(template.id, 'reward_credits', parseInt(e.target.value) || 0)
                    }
                    className="max-w-xs"
                  />
                </div>

                {/* 启用状态 */}
                <div className="flex items-center space-x-3">
                  <Switch
                    id={`active-${template.id}`}
                    checked={editValue.is_active ?? true}
                    onCheckedChange={(checked) =>
                      handleValueChange(template.id, 'is_active', checked)
                    }
                  />
                  <Label htmlFor={`active-${template.id}`} className="flex items-center gap-2 cursor-pointer">
                    {editValue.is_active ? (
                      <>
                        <Eye className="w-4 h-4 text-green-600" />
                        <span className="text-green-600">任务已启用</span>
                      </>
                    ) : (
                      <>
                        <EyeOff className="w-4 h-4 text-gray-400" />
                        <span className="text-gray-400">任务已禁用</span>
                      </>
                    )}
                  </Label>
                </div>

                {/* 保存按钮 */}
                <div className="flex justify-end pt-4 border-t">
                  <Button
                    onClick={() => handleUpdate(template.id)}
                    disabled={isSaving}
                    className="gap-2"
                  >
                    {isSaving ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        保存中...
                      </>
                    ) : (
                      <>
                        <Save className="w-4 h-4" />
                        保存更改
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* 空状态 */}
      {templates.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          <Settings2 className="w-16 h-16 mx-auto mb-4 opacity-20" />
          <p>暂无任务模板</p>
        </div>
      )}
    </div>
  );
};

export default AdminTasksView;
