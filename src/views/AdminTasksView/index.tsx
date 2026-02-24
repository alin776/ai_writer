/**
 * 管理员任务配置界面
 */
import React, { useEffect, useState } from 'react';
import { Switch } from '../../components/ui/switch';
import { Loader2, Save, Settings2, Coins, Eye, EyeOff, Trophy } from 'lucide-react';
import { ADMIN_STYLES } from '../../styles/adminStyles';
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
      <div className={ADMIN_STYLES.page}>
        <div className={ADMIN_STYLES.loadingContainer}>
          <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        </div>
      </div>
    );
  }

  return (
    <div className={ADMIN_STYLES.page}>
      <div className={ADMIN_STYLES.stickyHeader}>
        <div className={ADMIN_STYLES.titleSection}>
          <h1 className={ADMIN_STYLES.title}>
            <Trophy className={ADMIN_STYLES.titleIcon} />
            任务配置管理
          </h1>
          <p className={ADMIN_STYLES.subtitle}>管理系统任务及奖励积分</p>
        </div>
      </div>

      {/* 成功提示 */}
      {success && (
        <div className="mb-6 p-4 rounded-lg border bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800 text-green-800 dark:text-green-300 text-sm">{success}</div>
      )}

      {/* 错误提示 */}
      {error && (
        <div className="mb-6 p-4 rounded-lg border bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-800 dark:text-red-300 text-sm">{error}</div>
      )}

      {/* 任务模板列表 */}
      <div className="space-y-6">
        {templates.map((template) => {
          const editValue = editValues[template.id] || {};
          const isSaving = savingId === template.id;

          return (
            <div key={template.id} className={ADMIN_STYLES.tableContainer}>
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-3">
                      <span className="text-2xl">
                        {template.icon === 'edit' && '✍️'}
                        {template.icon === 'image' && '🖼️'}
                        {template.icon === 'user' && '✨'}
                      </span>
                      {template.title}
                    </h3>
                    <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                      任务Key: <code className="text-xs bg-gray-100 px-2 py-1 rounded">{template.task_key}</code>
                      <span className="ml-4">类型: {getTaskTypeLabel(template.task_type)}</span>
                    </p>
                  </div>
                </div>
              </div>

              <div className="p-6 space-y-6">
                {/* 任务描述 */}
                <div className="space-y-2">
                  <label htmlFor={`desc-${template.id}`} className={ADMIN_STYLES.modalLabel}>任务描述</label>
                  <input
                    id={`desc-${template.id}`}
                    value={editValue.description || ''}
                    onChange={(e) =>
                      handleValueChange(template.id, 'description', e.target.value)
                    }
                    placeholder="任务描述"
                    className={ADMIN_STYLES.modalInput}
                  />
                </div>

                {/* 奖励积分 */}
                <div className="space-y-2">
                  <label htmlFor={`credits-${template.id}`} className={ADMIN_STYLES.modalLabel + ' flex items-center gap-2'}>
                    <Coins className="w-4 h-4 text-yellow-600" />
                    奖励积分
                  </label>
                  <input
                    id={`credits-${template.id}`}
                    type="number"
                    min="0"
                    value={editValue.reward_credits || 0}
                    onChange={(e) =>
                      handleValueChange(template.id, 'reward_credits', parseInt(e.target.value) || 0)
                    }
                    className={ADMIN_STYLES.modalInput + ' max-w-xs'}
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
                  <label htmlFor={`active-${template.id}`} className="flex items-center gap-2 cursor-pointer text-sm">
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
                  </label>
                </div>

                {/* 保存按钮 */}
                <div className="flex justify-end pt-4 border-t">
                  <button
                    onClick={() => handleUpdate(template.id)}
                    disabled={isSaving}
                    className={ADMIN_STYLES.btnPrimary + ' flex items-center gap-2'}
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
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* 空状态 */}
      {templates.length === 0 && (
        <div className={ADMIN_STYLES.emptyContainer}>
          <Settings2 className={ADMIN_STYLES.emptyIcon} />
          <p className={ADMIN_STYLES.emptyText}>暂无任务模板</p>
        </div>
      )}
    </div>
  );
};

export default AdminTasksView;
