import React from 'react';
import { CheckCircle, Circle, Edit2, Save, X } from 'lucide-react';
import type { WorldViewData } from './index';
import styles from './CreateWorkView.module.css';

interface WorldCompletionSidebarProps {
  worldViewData: WorldViewData;
  isEditing: boolean;
  onEdit: () => void;
  onSave: () => void;
  onCancel: () => void;
  onChange: (field: string, value: string) => void;
}

/**
 * 世界观字段配置
 */
const WORLD_FIELDS = [
  { key: 'genre', label: '小说类型', required: true },
  { key: 'setting', label: '背景设定', required: true },
  { key: 'powerSystem', label: '力量体系', required: false },
  { key: 'mainCharacter', label: '主角设定', required: true },
  { key: 'plotIdea', label: '剧情构思', required: true },
  { key: 'worldRules', label: '世界规则', required: false },
];

/**
 * WorldCompletionSidebar 组件 - 世界观完成度侧边栏
 * 
 * 功能：
 * - 显示世界观各项内容的完成情况
 * - 计算完成度百分比
 * - 允许用户编辑世界观内容
 */
const WorldCompletionSidebar: React.FC<WorldCompletionSidebarProps> = ({
  worldViewData,
  isEditing,
  onEdit,
  onSave,
  onCancel,
  onChange,
}) => {
  /**
   * 计算完成度
   */
  const calculateCompletion = (): number => {
    const requiredFields = WORLD_FIELDS.filter(f => f.required);
    const completedRequired = requiredFields.filter(
      f => worldViewData[f.key] && worldViewData[f.key]!.trim() !== ''
    ).length;
    
    return Math.round((completedRequired / requiredFields.length) * 100);
  };

  /**
   * 检查字段是否已完成
   */
  const isFieldComplete = (key: string): boolean => {
    return !!(worldViewData[key] && worldViewData[key]!.trim() !== '');
  };

  const completion = calculateCompletion();

  return (
    <div className={styles.sidebar}>
      {/* 头部 - 简洁版 */}
      <div className={styles.sidebarHeader}>
        <div>
          <h3 className={styles.sidebarTitle}>世界观</h3>
          <div className={styles.completionBadge}>{completion}% 完成</div>
        </div>
        {!isEditing && (
          <button onClick={onEdit} className={styles.editButton} title="编辑">
            <Edit2 size={16} />
          </button>
        )}
      </div>

      {/* 字段列表 - 紧凑版 */}
      <div className={styles.fieldsList}>
        {WORLD_FIELDS.map((field) => {
          const isComplete = isFieldComplete(field.key);
          const value = worldViewData[field.key];
          
          // 如果没有内容且不在编辑状态，显示简化版
          if (!isEditing && !value) {
            return (
              <div key={field.key} className={styles.fieldItemCompact}>
                <Circle size={14} className={styles.iconIncomplete} />
                <span className={styles.fieldLabelCompact}>
                  {field.label}
                  {field.required && <span className={styles.requiredMark}>*</span>}
                </span>
              </div>
            );
          }
          
          return (
            <div key={field.key} className={`${styles.fieldItem} ${isComplete ? styles.fieldItemComplete : ''}`}>
              <div className={styles.fieldHeader}>
                {isComplete ? (
                  <CheckCircle size={14} className={styles.iconComplete} />
                ) : (
                  <Circle size={14} className={styles.iconIncomplete} />
                )}
                <span className={styles.fieldLabel}>
                  {field.label}
                  {field.required && <span className={styles.requiredMark}>*</span>}
                </span>
              </div>
              
              {isEditing ? (
                <textarea
                  value={value || ''}
                  onChange={(e) => onChange(field.key, e.target.value)}
                  placeholder={`输入${field.label}...`}
                  className={styles.fieldTextarea}
                  rows={2}
                />
              ) : (
                <div className={styles.fieldContent}>
                  {value}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* 编辑操作按钮 */}
      {isEditing && (
        <div className={styles.sidebarActions}>
          <button onClick={onCancel} className={styles.btnSecondary}>
            取消
          </button>
          <button onClick={onSave} className={styles.btnPrimary}>
            保存
          </button>
        </div>
      )}
    </div>
  );
};

export default WorldCompletionSidebar;
