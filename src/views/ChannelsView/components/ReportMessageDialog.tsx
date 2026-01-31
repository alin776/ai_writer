import { useState } from 'react';
import { X } from 'lucide-react';
import { reportMessage } from '@/services/channelApi';
import { useToast } from '@/hooks/useToast';

interface ReportMessageDialogProps {
  isOpen: boolean;
  onClose: () => void;
  channelId: string;
  messageId: string;
}

const REPORT_REASONS = [
  { value: 'spam', label: '垃圾信息' },
  { value: 'inappropriate', label: '不当内容' },
  { value: 'harassment', label: '骚扰谩骂' },
  { value: 'other', label: '其他' },
] as const;

export function ReportMessageDialog({
  isOpen,
  onClose,
  channelId,
  messageId,
}: ReportMessageDialogProps) {
  const { showToast } = useToast();
  const [reason, setReason] = useState<'spam' | 'inappropriate' | 'harassment' | 'other'>('spam');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      await reportMessage(channelId, messageId, reason, description);
      showToast('success', '举报已提交');
      onClose();
      setDescription('');
    } catch (error) {
      console.error('举报失败:', error);
      showToast('error', '举报失败');
    } finally {
      setSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 dark:bg-black/70 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-zinc-900 rounded-lg shadow-xl w-full max-w-md">
        {/* 标题栏 */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-zinc-800">
          <h3 className="text-base font-medium text-gray-900 dark:text-gray-100">举报消息</h3>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 dark:hover:bg-zinc-800 rounded transition-colors"
          >
            <X className="w-4 h-4 text-gray-600 dark:text-gray-400" />
          </button>
        </div>

        {/* 内容 */}
        <div className="p-4 space-y-4">
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
                    onChange={(e) => setReason(e.target.value as typeof reason)}
                    className="w-4 h-4 text-blue-600 dark:text-blue-500"
                  />
                  <span className="text-sm text-gray-900 dark:text-gray-100">{r.label}</span>
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
              className="w-full px-3 py-2 border border-gray-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 rounded-lg text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-600"
              rows={4}
            />
          </div>
        </div>

        {/* 按钮 */}
        <div className="flex items-center justify-end gap-2 p-4 border-t border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-800/50">
          <button
            onClick={onClose}
            disabled={submitting}
            className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-zinc-700 rounded transition-colors disabled:opacity-50"
          >
            取消
          </button>
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="px-4 py-2 text-sm bg-red-600 dark:bg-red-700 text-white rounded hover:bg-red-700 dark:hover:bg-red-800 transition-colors disabled:opacity-50"
          >
            {submitting ? '提交中...' : '提交举报'}
          </button>
        </div>
      </div>
    </div>
  );
}
