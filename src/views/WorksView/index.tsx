import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Plus } from 'lucide-react';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import type { Work } from '../../types';
import { formatDate } from '../../utils/formatDate';
import styles from './WorksView.module.css';

/**
 * WorksView 组件 - 作品列表页面
 *
 * 功能：
 * - 显示用户的所有作品
 * - 创建新作品
 * - 使用 DataService.getWorks 获取数据
 * - Loading 状态
 */
const WorksView: React.FC = () => {
  const [works, setWorks] = useState<Work[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { showToast } = useGlobalStore();

  /**
   * 加载作品列表
   */
  useEffect(() => {
    const loadWorks = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await DataService.getWorks();
        setWorks(data);
      } catch (err) {
        const message = err instanceof Error ? err.message : '加载作品失败';
        setError(message);
        showToast('error', message);
      } finally {
        setIsLoading(false);
      }
    };

    loadWorks();
  }, [showToast]);

  /**
   * 处理创建新作品
   */
  const handleCreateWork = async () => {
    const title = prompt('请输入作品标题：');
    if (!title || !title.trim()) {
      showToast('warning', '作品标题不能为空');
      return;
    }

    const description = prompt('请输入作品简介（可选）：') || '暂无描述';

    try {
      const newWork = await DataService.createWork({
        title: title.trim(),
        description: description.trim(),
      });

      setWorks((prev) => [newWork, ...prev]);
      showToast('success', '作品创建成功');
    } catch (error) {
      showToast('error', '作品创建失败');
      console.error('Failed to create work:', error);
    }
  };

  if (isLoading) {
    return (
      <div className={styles.loading}>
        <p>加载中...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.empty}>
        <p className={styles.emptyTitle}>加载失败</p>
        <p className={styles.emptyDescription}>{error}</p>
        <button className={styles.button} onClick={() => window.location.reload()}>
          重新加载
        </button>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      {/* 页面标题 */}
      <div className={styles.header}>
        <h1 className={styles.title}>我的作品</h1>
        <p className={styles.subtitle}>管理和查看您的所有创作</p>
      </div>

      {/* 操作栏 */}
      <div className={styles.actionBar}>
        <div className={styles.filterGroup}>
          {/* 可以在这里添加筛选按钮 */}
        </div>
        <button className={styles.button} onClick={handleCreateWork}>
          <Plus size={16} style={{ marginRight: '8px', display: 'inline-block', verticalAlign: 'middle' }} />
          创建新作品
        </button>
      </div>

      {/* 作品列表 */}
      {works.length === 0 ? (
        <div className={styles.empty}>
          <div className={styles.emptyIcon}>
            <BookOpen size={48} />
          </div>
          <p className={styles.emptyTitle}>还没有作品</p>
          <p className={styles.emptyDescription}>点击上方按钮创建您的第一个作品</p>
        </div>
      ) : (
        <div className={styles.grid}>
          {works.map((work) => (
            <div key={work.id} className={styles.card}>
              <h3 className={styles.cardTitle}>{work.title}</h3>
              <p className={styles.cardDescription}>
                {work.description || '暂无描述'}
              </p>
              <div className={styles.cardMeta}>
                <span className={styles.cardMetaItem}>
                  {formatDate(work.created_at)}
                </span>
                <span className={styles.cardMetaItem}>
                  {work.total_chapters || 0} 章节
                </span>
                <span className={styles.cardMetaItem}>
                  {work.total_words?.toLocaleString() || 0} 字
                </span>
              </div>
              <div className={styles.cardActions}>
                <Link to={`/works/${work.id}`} className={styles.cardButton}>
                  查看详情
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default WorksView;
