import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { BookOpen, Plus, Trash2, Upload } from 'lucide-react';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import { useConfirm } from '../../hooks/useConfirm';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import ImportDialog from '../../components/import/ImportDialog';
import type { Work } from '../../types';
import { formatDate } from '../../utils/formatDate';
import styles from './WorksView.module.css';
import { useWorkNavStore } from '@/store/workNavStore';

/**
 * WorksView 组件 - 作品管理列表页
 */
const WorksView: React.FC = () => {
  const navigate = useNavigate();
  const [works, setWorks] = useState<Work[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { showToast } = useGlobalStore();
  const { confirmState, confirm, closeConfirm } = useConfirm();
  const [showImportDialog, setShowImportDialog] = useState(false);
  const clearLastWork = useWorkNavStore((state) => state.clearLastWork);

  useEffect(() => {
    // 回到作品列表时，重置“最近作品”导航状态
    clearLastWork();

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
  }, [showToast, clearLastWork]);

  const handleCreateWork = () => {
    navigate('/works/create');
  };

  const handleDeleteWork = async (work: Work, event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();

    const confirmed = await confirm({
      title: '删除作品',
      message: `确定删除「${work.title}」吗？此操作不可撤销，将同时删除所有章节和设定。`,
      variant: 'danger',
    });

    if (!confirmed) return;

    try {
      await DataService.deleteWork(work.id);
      setWorks(works.filter((w) => w.id !== work.id));
      showToast('success', '作品已删除');
    } catch (error) {
      console.error('删除作品失败:', error);
      showToast('error', '删除作品失败');
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
      <ConfirmDialog
        isOpen={confirmState.isOpen}
        title={confirmState.title}
        message={confirmState.message}
        confirmText={confirmState.confirmText}
        cancelText={confirmState.cancelText}
        variant={confirmState.variant}
        onConfirm={confirmState.onConfirm}
        onCancel={closeConfirm}
      />
      
      {showImportDialog && (
        <ImportDialog
          onClose={() => setShowImportDialog(false)}
          onSuccess={(workId) => {
            setShowImportDialog(false);
            DataService.getWorks().then(setWorks);
            if (workId) {
              navigate(`/works/${workId}`);
            } else {
              navigate('/works');
            }
          }}
        />
      )}

      <div className={styles.header}>
        <h1 className={styles.title}>我的作品</h1>
        <p className={styles.subtitle}>管理并浏览你的所有创作</p>
      </div>

      <div className={styles.actionBar}>
        <div className={styles.filterGroup}>
          {/* 可在此添加筛选控件 */}
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button 
            className={styles.button} 
            onClick={() => setShowImportDialog(true)}
            style={{ background: '#059669', borderColor: '#059669' }}
          >
            <Upload size={16} style={{ marginRight: '8px', display: 'inline-block', verticalAlign: 'middle' }} />
            导入作品
          </button>
          <button className={styles.button} onClick={handleCreateWork}>
            <Plus size={16} style={{ marginRight: '8px', display: 'inline-block', verticalAlign: 'middle' }} />
            创建新作品
          </button>
        </div>
      </div>

      {works.length === 0 ? (
        <div className={styles.empty}>
          <div className={styles.emptyIcon}>
            <BookOpen size={48} />
          </div>
          <p className={styles.emptyTitle}>还没有作品</p>
          <p className={styles.emptyDescription}>点击上方按钮创建你的第一部作品</p>
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
                  {formatDate(work.createdAt)}
                </span>
                <span className={styles.cardMetaItem}>
                  {work.totalChapters || 0} 章节
                </span>
                <span className={styles.cardMetaItem}>
                  {(work.totalWords ?? 0).toLocaleString()} 字
                </span>
              </div>
              <div className={styles.cardActions}>
                <Link to={`/works/${work.id}`} className={styles.cardButton}>
                  查看详情
                </Link>
                <button
                  className={styles.cardButtonDanger}
                  onClick={(e) => handleDeleteWork(work, e)}
                  title="删除作品"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default WorksView;
