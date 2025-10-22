/**
 * 关系创建/编辑对话框
 */
import React, { useState, useEffect } from 'react';
import { X, Save } from 'lucide-react';
import {
  RelationshipFormData,
  RELATIONSHIP_TYPES,
  RELATIONSHIP_COLORS,
  RelationshipDirection,
  RelationshipLineStyle,
} from '@/types/relationship';

interface RelationshipDialogProps {
  open: boolean;
  mode: 'create' | 'edit';
  initialData?: Partial<RelationshipFormData>;
  sourceLabel?: string;
  targetLabel?: string;
  onClose: () => void;
  onSave: (data: RelationshipFormData) => void;
}

const RelationshipDialog: React.FC<RelationshipDialogProps> = ({
  open,
  mode,
  initialData,
  sourceLabel,
  targetLabel,
  onClose,
  onSave,
}) => {
  const [formData, setFormData] = useState<RelationshipFormData>({
    relationshipType: RELATIONSHIP_TYPES.CUSTOM,
    label: '',
    description: '',
    strength: 5,
    direction: 'one-way',
    lineStyle: 'solid',
  });

  useEffect(() => {
    if (initialData) {
      setFormData((prev) => ({ ...prev, ...initialData }));
    }
  }, [initialData]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleTypeChange = (type: string) => {
    setFormData((prev) => ({
      ...prev,
      relationshipType: type,
      color: RELATIONSHIP_COLORS[type] || RELATIONSHIP_COLORS.DEFAULT,
      label: prev.label || type, // 如果label为空，自动填充类型名
    }));
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-lg max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            {mode === 'create' ? '创建关系' : '编辑关系'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto px-6 py-4">
          {/* 连接提示 */}
          {sourceLabel && targetLabel && (
            <div className="mb-4 p-3 bg-blue-50 rounded-lg text-sm text-blue-900">
              <div className="flex items-center gap-2">
                <span className="font-medium">{sourceLabel}</span>
                <span>→</span>
                <span className="font-medium">{targetLabel}</span>
              </div>
            </div>
          )}

          {/* 关系类型 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              关系类型 <span className="text-red-500">*</span>
            </label>
            <select
              value={formData.relationshipType}
              onChange={(e) => handleTypeChange(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <optgroup label="角色关系">
                <option value={RELATIONSHIP_TYPES.CHARACTER_FAMILY}>
                  {RELATIONSHIP_TYPES.CHARACTER_FAMILY}
                </option>
                <option value={RELATIONSHIP_TYPES.CHARACTER_MENTOR}>
                  {RELATIONSHIP_TYPES.CHARACTER_MENTOR}
                </option>
                <option value={RELATIONSHIP_TYPES.CHARACTER_FRIEND}>
                  {RELATIONSHIP_TYPES.CHARACTER_FRIEND}
                </option>
                <option value={RELATIONSHIP_TYPES.CHARACTER_ALLY}>
                  {RELATIONSHIP_TYPES.CHARACTER_ALLY}
                </option>
                <option value={RELATIONSHIP_TYPES.CHARACTER_ENEMY}>
                  {RELATIONSHIP_TYPES.CHARACTER_ENEMY}
                </option>
                <option value={RELATIONSHIP_TYPES.CHARACTER_COLLEAGUE}>
                  {RELATIONSHIP_TYPES.CHARACTER_COLLEAGUE}
                </option>
                <option value={RELATIONSHIP_TYPES.CHARACTER_LOVER}>
                  {RELATIONSHIP_TYPES.CHARACTER_LOVER}
                </option>
                <option value={RELATIONSHIP_TYPES.CHARACTER_RIVAL}>
                  {RELATIONSHIP_TYPES.CHARACTER_RIVAL}
                </option>
              </optgroup>
              <optgroup label="角色与地点">
                <option value={RELATIONSHIP_TYPES.CHARACTER_LOCATION_LIVE}>
                  {RELATIONSHIP_TYPES.CHARACTER_LOCATION_LIVE}
                </option>
                <option value={RELATIONSHIP_TYPES.CHARACTER_LOCATION_BORN}>
                  {RELATIONSHIP_TYPES.CHARACTER_LOCATION_BORN}
                </option>
                <option value={RELATIONSHIP_TYPES.CHARACTER_LOCATION_WORK}>
                  {RELATIONSHIP_TYPES.CHARACTER_LOCATION_WORK}
                </option>
              </optgroup>
              <optgroup label="地点关系">
                <option value={RELATIONSHIP_TYPES.LOCATION_CONTAIN}>
                  {RELATIONSHIP_TYPES.LOCATION_CONTAIN}
                </option>
                <option value={RELATIONSHIP_TYPES.LOCATION_ADJACENT}>
                  {RELATIONSHIP_TYPES.LOCATION_ADJACENT}
                </option>
              </optgroup>
              <option value={RELATIONSHIP_TYPES.CUSTOM}>自定义</option>
            </select>
          </div>

          {/* 关系标签 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              关系标签 <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={formData.label}
              onChange={(e) => setFormData({ ...formData, label: e.target.value })}
              placeholder="例如: 师徒、父子、好友等"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          {/* 描述 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              关系描述
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="详细描述这段关系的背景和发展..."
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
          </div>

          {/* 关系强度 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              关系强度: {formData.strength}
            </label>
            <input
              type="range"
              min="1"
              max="10"
              value={formData.strength}
              onChange={(e) =>
                setFormData({ ...formData, strength: parseInt(e.target.value) })
              }
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>弱</span>
              <span>中</span>
              <span>强</span>
            </div>
          </div>

          {/* 关系方向 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              关系方向
            </label>
            <div className="flex gap-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="direction"
                  value="one-way"
                  checked={formData.direction === 'one-way'}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      direction: e.target.value as RelationshipDirection,
                    })
                  }
                  className="mr-2"
                />
                <span className="text-sm">单向 (A → B)</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="direction"
                  value="two-way"
                  checked={formData.direction === 'two-way'}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      direction: e.target.value as RelationshipDirection,
                    })
                  }
                  className="mr-2"
                />
                <span className="text-sm">双向 (A ↔ B)</span>
              </label>
            </div>
          </div>

          {/* 线条样式 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              线条样式
            </label>
            <div className="flex gap-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="lineStyle"
                  value="solid"
                  checked={formData.lineStyle === 'solid'}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      lineStyle: e.target.value as RelationshipLineStyle,
                    })
                  }
                  className="mr-2"
                />
                <span className="text-sm">实线</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="lineStyle"
                  value="dashed"
                  checked={formData.lineStyle === 'dashed'}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      lineStyle: e.target.value as RelationshipLineStyle,
                    })
                  }
                  className="mr-2"
                />
                <span className="text-sm">虚线</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="lineStyle"
                  value="dotted"
                  checked={formData.lineStyle === 'dotted'}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      lineStyle: e.target.value as RelationshipLineStyle,
                    })
                  }
                  className="mr-2"
                />
                <span className="text-sm">点线</span>
              </label>
            </div>
          </div>
        </form>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 bg-gray-50">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            取消
          </button>
          <button
            type="submit"
            onClick={handleSubmit}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            {mode === 'create' ? '创建' : '保存'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default RelationshipDialog;
