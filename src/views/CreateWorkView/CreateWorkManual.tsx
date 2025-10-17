import React, { useState, useEffect } from 'react';
import { ArrowLeft, Save, BookOpen } from 'lucide-react';
import type { CreateWorkData } from '../../types';
import type { WorldViewData } from './index';
import styles from './CreateWorkView.module.css';

interface CreateWorkManualProps {
  onSubmit: (data: CreateWorkData, worldView: WorldViewData) => void;
  onBack: () => void;
}

/**
 * CreateWorkManual 组件 - 手动创建作品表单
 * 
 * 包含：
 * - 作品基本信息（标题、简介）
 * - 世界观设定（类型、背景、力量体系等）
 */
const CreateWorkManual: React.FC<CreateWorkManualProps> = ({ onSubmit, onBack }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    genre: '',
    setting: '',
    powerSystem: '',
    mainCharacter: '',
    plotIdea: '',
    worldRules: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  /**
   * 组件加载时滚动到顶部
   */
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  /**
   * 处理输入变化
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // 清除错误
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  /**
   * 验证表单
   */
  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = '请输入作品标题';
    } else if (formData.title.length < 2) {
      newErrors.title = '标题至少需要2个字符';
    }

    if (!formData.description.trim()) {
      newErrors.description = '请输入作品简介';
    } else if (formData.description.length < 10) {
      newErrors.description = '简介至少需要10个字符';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * 处理提交
   */
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    // 分离基本信息和世界观数据
    const workData: CreateWorkData = {
      title: formData.title.trim(),
      description: formData.description.trim(),
    };

    const worldViewData: WorldViewData = {
      genre: formData.genre,
      setting: formData.setting,
      powerSystem: formData.powerSystem,
      mainCharacter: formData.mainCharacter,
      plotIdea: formData.plotIdea,
      worldRules: formData.worldRules,
    };

    onSubmit(workData, worldViewData);
  };

  return (
    <div className={styles.formContainer}>
      {/* 返回按钮 */}
      <button className={styles.backButton} onClick={onBack}>
        <ArrowLeft size={20} />
        <span>返回</span>
      </button>

      {/* 标题区域 */}
      <div className={styles.header}>
        <div className={styles.iconWrapper}>
          <BookOpen size={40} />
        </div>
        <h1 className={styles.title}>创建你的作品</h1>
        <p className={styles.subtitle}>详细描述你的创作世界，让故事更加立体生动</p>
      </div>

      {/* 表单 */}
      <form onSubmit={handleSubmit} className={styles.form}>
        {/* 基本信息 */}
        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>基本信息</h2>
          
          <div className={styles.formGroup}>
            <label htmlFor="title" className={styles.label}>
              作品标题 <span className={styles.required}>*</span>
            </label>
            <input
              id="title"
              name="title"
              type="text"
              value={formData.title}
              onChange={handleChange}
              placeholder="请输入作品标题"
              className={`${styles.input} ${errors.title ? styles.inputError : ''}`}
            />
            {errors.title && <span className={styles.errorMessage}>{errors.title}</span>}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="description" className={styles.label}>
              作品简介 <span className={styles.required}>*</span>
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="简要描述您的作品内容、主题或特色"
              className={`${styles.textarea} ${errors.description ? styles.inputError : ''}`}
              rows={4}
            />
            {errors.description && <span className={styles.errorMessage}>{errors.description}</span>}
          </div>
        </div>

        {/* 世界观设定（可选） */}
        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>世界观设定</h2>
          <p className={styles.sectionHint}>详细的世界观设定能让你的故事更加立体和真实，这些信息可以随时补充和修改</p>

          {/* 两栏布局 */}
          <div className={styles.worldGrid}>
            <div className={styles.formGroup}>
              <label htmlFor="genre" className={styles.label}>
                小说类型
              </label>
              <select
                id="genre"
                name="genre"
                value={formData.genre}
                onChange={handleChange}
                className={styles.select}
              >
                <option value="">请选择类型</option>
                <option value="fantasy">玄幻奇幻</option>
                <option value="urban">现代都市</option>
                <option value="scifi">科幻未来</option>
                <option value="historical">历史穿越</option>
                <option value="romance">言情浪漫</option>
                <option value="martial">武侠仙侠</option>
                <option value="gaming">游戏竞技</option>
                <option value="other">其他类型</option>
              </select>
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="setting" className={styles.label}>
                背景设定
              </label>
              <textarea
                id="setting"
                name="setting"
                value={formData.setting}
                onChange={handleChange}
                placeholder="描述故事发生的时代、地点、社会背景等..."
                className={styles.textarea}
                rows={4}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="powerSystem" className={styles.label}>
                力量体系
              </label>
              <textarea
                id="powerSystem"
                name="powerSystem"
                value={formData.powerSystem}
                onChange={handleChange}
                placeholder="如：修仙等级、魔法体系、科技水平等..."
                className={styles.textarea}
                rows={4}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="mainCharacter" className={styles.label}>
                主角设定
              </label>
              <textarea
                id="mainCharacter"
                name="mainCharacter"
                value={formData.mainCharacter}
                onChange={handleChange}
                placeholder="主角的性格、背景、特殊能力、成长轨迹..."
                className={styles.textarea}
                rows={4}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="plotIdea" className={styles.label}>
                剧情构思
              </label>
              <textarea
                id="plotIdea"
                name="plotIdea"
                value={formData.plotIdea}
                onChange={handleChange}
                placeholder="主线剧情、重要事件、故事走向、情节发展..."
                className={styles.textarea}
                rows={4}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="worldRules" className={styles.label}>
                世界规则
              </label>
              <textarea
                id="worldRules"
                name="worldRules"
                value={formData.worldRules}
                onChange={handleChange}
                placeholder="特殊的世界规则、法则、限制、禁忌..."
                className={styles.textarea}
                rows={4}
              />
            </div>
          </div>
        </div>

        {/* 提交按钮 */}
        <div className={styles.formActions}>
          <button type="button" onClick={onBack} className={styles.cancelButton}>
            取消
          </button>
          <button type="submit" className={styles.submitButton}>
            <Save size={18} />
            <span>创建作品</span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateWorkManual;
