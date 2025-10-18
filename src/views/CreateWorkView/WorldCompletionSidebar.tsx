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
 * 世界观字段配置 - 按模块分组的31个字段
 */
const WORLD_FIELDS_GROUPS = [
  {
    title: '第一部分：创作规范',
    groups: [
      {
        name: '战略定位',
        color: 'blue',
        fields: [
          { key: 'businessGoal', label: '商业目标', required: true },
          { key: 'targetAudience', label: '目标读者', required: true },
          { key: 'commercialBenchmark', label: '商业对标', required: true },
          { key: 'highConcept', label: '高概念卖点', required: true },
        ]
      },
      {
        name: 'IP架构',
        color: 'purple',
        fields: [
          { key: 'coreParadox', label: '核心悖论/设定', required: true },
          { key: 'dominantEmotion', label: '主导情感', required: true },
          { key: 'coreIpSymbols', label: '核心IP符号', required: true },
        ]
      },
      {
        name: '叙事引擎',
        color: 'green',
        fields: [
          { key: 'protagonistArc', label: '主角弧光', required: true },
          { key: 'coreConflict', label: '核心关系冲突', required: true },
          { key: 'narrativeRhythm', label: '叙事节奏', required: true },
        ]
      },
      {
        name: '文字质感',
        color: 'amber',
        fields: [
          { key: 'writingStyle', label: '文笔风格', required: true },
          { key: 'styleNotes', label: '文风注意事项', required: false },
        ]
      },
      {
        name: '技术规范',
        color: 'red',
        fields: [
          { key: 'chapterLength', label: '章节长度', required: true },
          { key: 'contentTaboos', label: '内容禁忌', required: false },
        ]
      }
    ]
  },
  {
    title: '第二部分：核心设定（AI生成）',
    groups: [
      {
        name: '小说类型',
        color: 'indigo',
        fields: [
          { key: 'primaryGenre', label: '一级类型', required: false },
          { key: 'secondaryTags', label: '二级标签', required: false },
          { key: 'creativeTone', label: '创作基调', required: false },
        ]
      },
      {
        name: '世界背景',
        color: 'cyan',
        fields: [
          { key: 'worldIntro', label: '核心世界观简介', required: false },
          { key: 'mainLocations', label: '主要场景/地点', required: false },
          { key: 'worldRules', label: '世界规则', required: false },
        ]
      },
      {
        name: '力量体系',
        color: 'pink',
        fields: [
          { key: 'powerSystemName', label: '体系名称', required: false },
          { key: 'powerLevels', label: '等级划分', required: false },
          { key: 'powerCost', label: '代价与限制', required: false },
        ]
      },
      {
        name: '主角设定',
        color: 'teal',
        fields: [
          { key: 'protagonistName', label: '主角名字', required: false },
          { key: 'protagonistIdentity', label: '身份与背景', required: false },
          { key: 'protagonistTraits', label: '性格特点', required: false },
          { key: 'protagonistGoal', label: '终极目标', required: false },
        ]
      },
      {
        name: '剧情构思',
        color: 'orange',
        fields: [
          { key: 'conflictDesign', label: '冲突设计', required: false },
          { key: 'actOne', label: '第一幕', required: false },
          { key: 'actTwo', label: '第二幕', required: false },
          { key: 'actThree', label: '第三幕', required: false },
        ]
      }
    ]
  }
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
   * 获取所有字段（扁平化）
   */
  const getAllFields = () => {
    const allFields: any[] = [];
    WORLD_FIELDS_GROUPS.forEach(section => {
      section.groups.forEach(group => {
        allFields.push(...group.fields);
      });
    });
    return allFields;
  };

  /**
   * 计算完成度（基于必填字段）
   */
  const calculateCompletion = (): number => {
    const allFields = getAllFields();
    const requiredFields = allFields.filter(f => f.required);
    const completedRequired = requiredFields.filter(
      f => worldViewData[f.key] && worldViewData[f.key]!.trim() !== ''
    ).length;
    
    if (requiredFields.length === 0) return 0;
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

      {/* 字段列表 - 分组显示 */}
      <div className={styles.fieldsList}>
        {WORLD_FIELDS_GROUPS.map((section, sectionIndex) => (
          <div key={sectionIndex} className={styles.fieldSection}>
            {/* 部分标题 */}
            <div className={styles.sectionTitle}>{section.title}</div>
            
            {section.groups.map((group, groupIndex) => {
              // 检查该组是否有任何字段有内容
              const hasAnyContent = group.fields.some(f => worldViewData[f.key]);
              
              // 如果不在编辑状态且该组没有内容，则隐藏
              if (!isEditing && !hasAnyContent) {
                return null;
              }
              
              return (
                <div key={groupIndex} className={styles.fieldGroup}>
                  {/* 组标题 */}
                  <div className={`${styles.groupName} ${styles[`group${group.color.charAt(0).toUpperCase() + group.color.slice(1)}`]}`}>
                    {group.name}
                  </div>
                  
                  {/* 字段列表 */}
                  {group.fields.map((field) => {
                    const isComplete = isFieldComplete(field.key);
                    const value = worldViewData[field.key];
                    
                    // 如果没有内容且不在编辑状态，跳过
                    if (!isEditing && !value) {
                      return null;
                    }
                    
                    return (
                      <div key={field.key} className={`${styles.fieldItem} ${isComplete ? styles.fieldItemComplete : ''}`}>
                        <div className={styles.fieldHeader}>
                          {isComplete ? (
                            <CheckCircle size={12} className={styles.iconComplete} />
                          ) : (
                            <Circle size={12} className={styles.iconIncomplete} />
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
              );
            })}
          </div>
        ))}
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
