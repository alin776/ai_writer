import { useState } from 'react';
import { X, ChevronDown, Check } from 'lucide-react';

interface InviteLinkSettingsDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onGenerate: (options: { expiresHours: number | null; maxUses: number | null }) => void;
  initialExpiresHours?: number | null;
  initialMaxUses?: number | null;
}

// 过期时间选项
const EXPIRE_OPTIONS = [
  { label: '30 分钟', value: 0.5 },
  { label: '1 小时', value: 1 },
  { label: '6 小时', value: 6 },
  { label: '12 小时', value: 12 },
  { label: '1 天', value: 24 },
  { label: '7 天', value: 168 },
  { label: '永不', value: null },
];

// 最大使用次数选项
const MAX_USES_OPTIONS = [
  { label: '无限制', value: null },
  { label: '1 次使用', value: 1 },
  { label: '5 次使用', value: 5 },
  { label: '10 次使用', value: 10 },
  { label: '25 次使用', value: 25 },
  { label: '50 次使用', value: 50 },
  { label: '100 次使用', value: 100 },
];

export function InviteLinkSettingsDialog({
  isOpen,
  onClose,
  onGenerate,
  initialExpiresHours = 0.5,
  initialMaxUses = null,
}: InviteLinkSettingsDialogProps) {
  const [expiresHours, setExpiresHours] = useState<number | null>(initialExpiresHours);
  const [maxUses, setMaxUses] = useState<number | null>(initialMaxUses);
  const [showExpiresDropdown, setShowExpiresDropdown] = useState(false);
  const [showMaxUsesDropdown, setShowMaxUsesDropdown] = useState(false);

  if (!isOpen) return null;

  const handleGenerate = () => {
    onGenerate({ expiresHours, maxUses });
    onClose();
  };

  const getExpiresLabel = () => {
    const option = EXPIRE_OPTIONS.find(opt => opt.value === expiresHours);
    return option?.label || '30 分钟';
  };

  const getMaxUsesLabel = () => {
    const option = MAX_USES_OPTIONS.find(opt => opt.value === maxUses);
    return option?.label || '无限制';
  };

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center">
      {/* 遮罩 */}
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
      />

      {/* 弹窗 - 与邀请对话框样式统一 */}
      <div className="relative w-full max-w-md bg-white dark:bg-gray-800 rounded-xl shadow-xl">
        {/* 头部 */}
        <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between rounded-t-xl">
          <h3 className="text-base font-medium text-gray-900 dark:text-white">
            服务器邀请链接设置
          </h3>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* 内容 */}
        <div className="px-4 py-4 space-y-4">
          {/* 过期时间选择 */}
          <div>
            <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2">
              在此时间后过期
            </label>
            <div className="relative">
              <button
                onClick={() => {
                  setShowExpiresDropdown(!showExpiresDropdown);
                  setShowMaxUsesDropdown(false);
                }}
                className="w-full flex items-center justify-between px-3 py-2.5 bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white hover:border-gray-300 dark:hover:border-gray-500 transition-colors"
              >
                <span>{getExpiresLabel()}</span>
                <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${showExpiresDropdown ? 'rotate-180' : ''}`} />
              </button>

              {showExpiresDropdown && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg overflow-hidden z-10">
                  {EXPIRE_OPTIONS.map((option) => (
                    <button
                      key={option.label}
                      onClick={() => {
                        setExpiresHours(option.value);
                        setShowExpiresDropdown(false);
                      }}
                      className={`w-full flex items-center justify-between px-3 py-2.5 text-left hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors ${
                        expiresHours === option.value ? 'text-gray-900 dark:text-white' : 'text-gray-700 dark:text-gray-300'
                      }`}
                    >
                      <span>{option.label}</span>
                      {expiresHours === option.value && (
                        <Check className="w-5 h-5 text-[#5865f2]" />
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* 最大使用次数选择 */}
          <div>
            <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2">
              最大使用次数
            </label>
            <div className="relative">
              <button
                onClick={() => {
                  setShowMaxUsesDropdown(!showMaxUsesDropdown);
                  setShowExpiresDropdown(false);
                }}
                className="w-full flex items-center justify-between px-3 py-2.5 bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white hover:border-gray-300 dark:hover:border-gray-500 transition-colors"
              >
                <span>{getMaxUsesLabel()}</span>
                <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${showMaxUsesDropdown ? 'rotate-180' : ''}`} />
              </button>

              {showMaxUsesDropdown && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg overflow-hidden z-10 max-h-64 overflow-y-auto">
                  {MAX_USES_OPTIONS.map((option) => (
                    <button
                      key={option.label}
                      onClick={() => {
                        setMaxUses(option.value);
                        setShowMaxUsesDropdown(false);
                      }}
                      className={`w-full flex items-center justify-between px-3 py-2.5 text-left hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors ${
                        maxUses === option.value ? 'text-gray-900 dark:text-white' : 'text-gray-700 dark:text-gray-300'
                      }`}
                    >
                      <span>{option.label}</span>
                      {maxUses === option.value && (
                        <Check className="w-5 h-5 text-[#5865f2]" />
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* 底部按钮 */}
        <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700 flex items-center justify-end gap-3 rounded-b-xl">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            取消
          </button>
          <button
            onClick={handleGenerate}
            className="px-4 py-2 text-sm font-medium bg-[#5865f2] hover:bg-[#4752c4] text-white rounded-lg transition-colors"
          >
            生成新的链接
          </button>
        </div>
      </div>
    </div>
  );
}
