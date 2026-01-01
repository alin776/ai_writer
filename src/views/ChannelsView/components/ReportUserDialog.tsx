import { useState } from 'react';
import { X } from 'lucide-react';
import { reportUser } from '@/services/friendApi';
import { useToast } from '@/hooks/useToast';

interface ReportUserDialogProps {
  isOpen: boolean;
  onClose: () => void;
  userId: string;
  userName: string;
}

const REPORT_REASONS = [
  { value: 'spam', label: '垃圾信息' },
  { value: 'inappropriate', label: '不当内容' },
  { value: 'harassment', label: '骚扰谩骂' },
  { value: 'impersonation', label: '冒充他人' },
  { value: 'other', label: '其他' },
] as const;

type ReportReason = typeof REPORT_REASONS[number]['value'];

export function ReportUserDialog({
  isOpen,
  onClose,
  userId,
  userName,
}: ReportUserDialogProps) {
  const { showToast } = useToast();
  const [reason, setReason] = useState<ReportReason>('spam');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      await reportUser(userId, reason, description || undefined);
      showToast('success', '举报已提交');
      onClose();
      setDescription('');
      setReason('spam');
    } catch (error: any) {
      console.error('举报失败:', error);
      if (error?.response?.data?.detail) {
        showToast('error', error.response.data.detail);
      } else {
        showToast('error', '举报失败');
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-[100]">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md">
        {/* 标题栏 */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-base font-medium dark:text-gray-100">举报用户</h3>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
          >
            <X className="w-4 h-4 dark:text-gray-400" />
          </button>
        </div>

        {/* 内容 */}
        <div className="p-4 space-y-4">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            您正在举报用户 <span className="font-medium text-gray-900 dark:text-gray-100">{userName}</span>
          </p>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              举报原因
            </label>
            <div className="space-y-2">
              {REPORT_REASONS.map((r) => (
                <label key={r.value} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="reason"
                    value={r.value}
                    checked={reason === r.value}
                    onChange={(e) => setReason(e.target.value as ReportReason)}
                    className="w-4 h-4"
                  />
                  <span className="text-sm dark:text-gray-200">{r.label}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              详细描述（选填）
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="请描述具体问题..."
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              rows={4}
            />
          </div>
        </div>

        {/* 按钮 */}
        <div className="flex items-center justify-end gap-2 p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
          <button
            onClick={onClose}
            disabled={submitting}
            className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors disabled:opacity-50"
          >
            取消
          </button>
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="px-4 py-2 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition-colors disabled:opacity-50"
          >
            {submitting ? '提交中...' : '提交举报'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ReportUserDialog;
