/**
 * Agent编辑确认对话框 - 用户确认AI修改
 */
import React, { useEffect, useState } from 'react';
import { X, Check, AlertTriangle, FileText, Wand2 } from 'lucide-react';
import { DiffViewer } from './DiffViewer';

// ✅ P0-6修复：使用approvalRequest对象接收数据
interface RewriteVersion {
  style?: string;
  style_name: string;
  reason?: string;
  content?: string;  // ✅ 新增：实际改写内容
}

interface ApprovalRequest {
  request_id: string;
  action_type: 'edit' | 'rewrite' | 'insert';
  operation?: string;
  original_content?: string;
  new_content?: string;
  description?: string;
  versions?: RewriteVersion[];
  chapter_id?: string;
}

interface AgentEditConfirmDialogProps {
  isOpen: boolean;
  approvalRequest: ApprovalRequest;
  onApprove: (selectedVersion?: number) => void;
  onReject: () => void;
  onClose: () => void;
}

export const AgentEditConfirmDialog: React.FC<AgentEditConfirmDialogProps> = ({
  isOpen,
  approvalRequest,
  onApprove,
  onReject,
  onClose
}) => {
  // ✅ 从approvalRequest中解构数据
  const {
    action_type: actionType = 'edit',
    operation,
    original_content: originalContent = '',
    new_content: newContent = '',
    description,
    versions
  } = approvalRequest || {};

  // ✅ 兼容旧的回调名称
  const onConfirm = onApprove;
  const onCancel = onReject;
  const [selectedVersion, setSelectedVersion] = useState<number>(0);

  // 快捷键支持
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return;

      switch (e.key) {
        case 'Enter':
          if (!e.shiftKey) {
            e.preventDefault();
            onConfirm(actionType === 'rewrite' ? selectedVersion : undefined);
          }
          break;
        case 'Escape':
          e.preventDefault();
          onCancel();
          break;
        case '1':
        case '2':
        case '3':
          if (actionType === 'rewrite' && versions) {
            const index = parseInt(e.key) - 1;
            if (versions[index]) {
              e.preventDefault();
              setSelectedVersion(index);
            }
          }
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, actionType, versions, selectedVersion, onConfirm, onCancel]);

  if (!isOpen) return null;

  const getTitle = () => {
    switch (actionType) {
      case 'edit':
        return operation === 'append' ? 'AI续写确认' : 'AI编辑确认';
      case 'rewrite':
        return 'AI改写 - 选择版本';
      case 'insert':
        return 'AI插入确认';
      default:
        return 'AI操作确认';
    }
  };

  const getIcon = () => {
    switch (actionType) {
      case 'edit':
        return <FileText className="w-5 h-5 text-blue-500" />;
      case 'rewrite':
        return <Wand2 className="w-5 h-5 text-purple-500" />;
      case 'insert':
        return <FileText className="w-5 h-5 text-green-500" />;
      default:
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* 背景遮罩 */}
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onCancel}
      />

      {/* 对话框 */}
      <div className="relative bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[80vh] overflow-hidden">
        {/* 头部 */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <div className="flex items-center gap-3">
            {getIcon()}
            <h3 className="text-lg font-semibold text-gray-900">{getTitle()}</h3>
          </div>
          <button
            onClick={onCancel}
            className="p-1 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* 内容区域 */}
        <div className="p-6 overflow-y-auto" style={{ maxHeight: 'calc(80vh - 140px)' }}>
          {/* 操作描述 */}
          {description && (
            <p className="text-sm text-gray-600 mb-4">{description}</p>
          )}

          {/* 改写版本选择 - 显示实际改写内容 */}
          {actionType === 'rewrite' && versions && versions.length > 0 && (
            <div className="space-y-4">
              <p className="text-sm text-gray-600">请选择一个改写版本：</p>

              {/* 版本选择标签 */}
              <div className="flex gap-2 flex-wrap">
                {versions.map((version, index) => (
                  <button
                    key={`tab-${index}`}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      selectedVersion === index
                        ? 'bg-blue-500 text-white shadow-md'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                    onClick={() => setSelectedVersion(index)}
                  >
                    {index + 1}. {version.style_name || `版本${index + 1}`}
                  </button>
                ))}
              </div>

              {/* 选中版本的描述 */}
              {versions[selectedVersion]?.reason && (
                <p className="text-sm text-gray-500 italic">
                  {versions[selectedVersion].reason}
                </p>
              )}

              {/* ✅ 显示选中版本的Diff对比 */}
              {versions[selectedVersion]?.content ? (
                <div className="mt-2">
                  <DiffViewer
                    original={originalContent}
                    modified={versions[selectedVersion].content}
                    maxHeight={300}
                  />
                </div>
              ) : (
                /* 如果没有content，显示原文 */
                <div className="p-3 bg-gray-50 rounded-lg border border-gray-200 text-sm text-gray-700 max-h-48 overflow-y-auto">
                  {originalContent}
                </div>
              )}
            </div>
          )}

          {/* 非改写操作的Diff视图 */}
          {actionType !== 'rewrite' && (
            <DiffViewer
              original={originalContent}
              modified={operation === 'append' ? originalContent + newContent : newContent}
              maxHeight={300}
            />
          )}
        </div>

        {/* 底部按钮 */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-gray-200 bg-gray-50">
          <span className="text-xs text-gray-500">
            Enter 确认 · Esc 取消
            {actionType === 'rewrite' && ' · 1-3 选择版本'}
          </span>
          <div className="flex items-center gap-3">
            <button
              onClick={onCancel}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              onClick={() => onConfirm(actionType === 'rewrite' ? selectedVersion : undefined)}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors flex items-center gap-2"
            >
              <Check className="w-4 h-4" />
              确认应用
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentEditConfirmDialog;
