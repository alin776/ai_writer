import React from 'react';
import { ArrowLeft, BookOpen, Sparkles } from 'lucide-react';
import styles from './CreateWorkView.module.css';

interface CreateWorkChoiceProps {
  onSelect: (mode: 'manual' | 'ai') => void;
  onBack: () => void;
}

/**
 * CreateWorkChoice 组件 - 选择创建模式
 * 
 * 两个选项：
 * 1. 已有剧情想法和世界观思路 - 手动填写
 * 2. 需要AI创建世界观和思路 - AI辅助
 */
const CreateWorkChoice: React.FC<CreateWorkChoiceProps> = ({ onSelect, onBack }) => {
  return (
    <div className={styles.choiceContainer}>
      {/* 返回按钮 */}
      <button className={styles.backButton} onClick={onBack}>
        <ArrowLeft size={20} />
        <span>返回作品列表</span>
      </button>

      {/* 标题 */}
      <div className={styles.header}>
        <h1 className={styles.title}>开启你的创作之旅</h1>
        <p className={styles.subtitle}>选择你喜欢的创作方式</p>
      </div>

      {/* 选项卡片 */}
      <div className={styles.choiceGrid}>
        {/* 手动创建 */}
        <div 
          className={styles.choiceCard}
          onClick={() => onSelect('manual')}
        >
          <div className={styles.choiceIcon}>
            <BookOpen size={48} />
          </div>
          <h2 className={styles.choiceTitle}>已有清晰思路</h2>
          <p className={styles.choiceDescription}>
            我已经有了剧情想法和世界观设定，直接开始创作
          </p>
          <ul className={styles.choiceFeatures}>
            <li>快速创建</li>
            <li>自由发挥</li>
            <li>完全掌控</li>
          </ul>
          <button className={styles.choiceButton}>
            开始创作
          </button>
        </div>

        {/* AI辅助创建 */}
        <div 
          className={styles.choiceCard}
          onClick={() => onSelect('ai')}
        >
          <div className={`${styles.choiceIcon} ${styles.aiIcon}`}>
            <Sparkles size={48} />
          </div>
          <h2 className={styles.choiceTitle}>需要 AI 协作构建</h2>
          <p className={styles.choiceDescription}>
            让 AI 通过对话引导，实时构建结构化世界观
          </p>
          <ul className={styles.choiceFeatures}>
            <li>智能引导</li>
            <li>灵感激发</li>
            <li>专业建议</li>
          </ul>
          <button className={styles.choiceButton}>
            开始创作
          </button>
          <p className={styles.hint}>AI 将通过对话引导，实时构建结构化世界观</p>
        </div>
      </div>


    </div>
  );
};

export default CreateWorkChoice;
