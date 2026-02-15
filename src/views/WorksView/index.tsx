/**
 * WorksView 组件 - 重构后的作品列表页面
 *
 * 特点：
 * - 现代化倾斜(skew)设计风格
 * - 统计卡片展示
 * - 搜索、筛选、排序功能
 * - 进度条动画效果
 * - 悬停交互动画
 * - 编辑弹窗
 */

import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { chaptersFs } from '../../services/chaptersFs';
import { fsToChapter } from '../../utils/fsChapterAdapter';
import { useTranslation } from 'react-i18next';
import {
  Plus,
  Upload,
  MoreVertical,
  Clock,
  BookOpen,
  FileText,
  Edit3,
  Trash2,
  Download,
  TrendingUp,
  Search,
  Pin,
  Circle,
  X,
  File,
  AlertCircle,
  CheckCircle,
  Globe,
  Eye as EyeIcon
} from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../components/ui/select';
import { DataService } from '../../services/DataService';
import { TxtExportService, type TxtExportResult } from '../../services/TxtExportService';
import { useGlobalStore } from '../../store/globalStore';
import { useWorkNavStore } from '../../store/workNavStore';
import { useConfirm } from '../../hooks/useConfirm';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import { ActivityModal } from '../../components/notifications/ActivityModal';
import { getUserNotifications, markNotificationsAsRead } from '../../services/notificationApi';
import { NotificationType } from '../../types/notification';
import type { Work, WorkStatus, WorkGenre, WorkSummary } from '../../types';
import type { ImportOptions, ImportPreviewResponse } from '../../types/export';
import type { UserNotification } from '../../types/notification';
import type { WorldviewScanProgress } from '../../types/novel';

// 默认封面路径
const DEFAULT_COVER_IMAGE = '/default-cover.jpg';

// 模拟章节数据(用于发布弹窗)
const mockChaptersForPublish = Array.from({ length: 10 }, (_, i) => ({
  id: String(i + 1),
  title: `第${i + 1}章 ${['初入江湖', '剑道传承', '山雨欲来', '危机四伏', '绝地反击', '破而后立', '天降奇缘', '修炼神功', '血战群雄', '成就霸业'][i]}`,
  wordCount: 2000 + Math.floor(Math.random() * 1000),
  updateTime: `2024-12-${String(14 - Math.floor(i / 3)).padStart(2, '0')}`
}));

const WorksView: React.FC = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { showToast } = useGlobalStore();
  const clearLastWork = useWorkNavStore((state) => state.clearLastWork);
  const { confirmState, confirm, closeConfirm } = useConfirm();

  // 数据状态
  const [works, setWorks] = useState<Work[]>([]);
  const [summary, setSummary] = useState<WorkSummary | null>(null);
  const [totalWorksCount, setTotalWorksCount] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  // 筛选和搜索状态
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStatus, setSelectedStatus] = useState<string>('all');
  const [selectedGenre, setSelectedGenre] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'date' | 'words' | 'title'>('date');

  // 编辑弹窗状态
  const [editingWork, setEditingWork] = useState<Work | null>(null);
  const [editFormData, setEditFormData] = useState({
    title: '',
    description: '',
    genre: '' as WorkGenre | '',
    status: 'draft' as WorkStatus,
    coverImage: ''
  });
  const [pendingCoverFile, setPendingCoverFile] = useState<File | null>(null);
  const [coverPreview, setCoverPreview] = useState<string>('');

  // 导入弹窗状态
  const [showImportModal, setShowImportModal] = useState(false);
  const [importFile, setImportFile] = useState<File | null>(null);
  const [importFormat, setImportFormat] = useState<'json' | 'markdown' | 'txt'>('json');
  const [importPreview, setImportPreview] = useState<ImportPreviewResponse | null>(null);
  const [isImporting, setIsImporting] = useState(false);
  const [isPreviewing, setIsPreviewing] = useState(false);
  const [isDraggingFile, setIsDraggingFile] = useState(false);
  const [importCompleted, setImportCompleted] = useState(false);
  const [importedWorkId, setImportedWorkId] = useState<string | null>(null);
  const [importedChaptersCount, setImportedChaptersCount] = useState<number | null>(null);
  const [importAutoExtracted, setImportAutoExtracted] = useState(false);
  const [scanProgress, setScanProgress] = useState<WorldviewScanProgress | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const dragCounterRef = useRef(0);
  const autoNavigateEnabledRef = useRef(true);
  const hasAutoNavigatedRef = useRef(false);

  // 导出弹窗状态
  const [exportingWork, setExportingWork] = useState<Work | null>(null);
  const [showExportModal, setShowExportModal] = useState(false);
  const [exportMode, setExportMode] = useState<'full' | 'range'>('full');
  const [exportStartChapter, setExportStartChapter] = useState('');
  const [exportEndChapter, setExportEndChapter] = useState('');
  const [isExporting, setIsExporting] = useState(false);
  const [exportError, setExportError] = useState<string | null>(null);

  // 活动/公告弹窗状态
  const [activityNotification, setActivityNotification] = useState<UserNotification | null>(null);
  const [showActivityModal, setShowActivityModal] = useState(false);

  // 发布弹窗状态
  const [publishingWork, setPublishingWork] = useState<Work | null>(null);
  const [showPublishModal, setShowPublishModal] = useState(false);
  const [selectedChapters, setSelectedChapters] = useState<Set<string>>(new Set());
  const [isPublishing, setIsPublishing] = useState(false);
  const [chaptersForPublish, setChaptersForPublish] = useState<any[]>([]);

  // 进入作品管理页面时，清除记住的作品详情路径
  // 这样导航栏的"作品详情"会变回"作品管理"
  useEffect(() => {
    clearLastWork();
  }, [clearLastWork]);

  // 加载作品列表
  useEffect(() => {
    loadWorks();
  }, []);

  // 检查并显示活动/公告弹窗（仅在登录后首次进入时）
  useEffect(() => {
    checkForActivityNotifications();
  }, []);

  const checkForActivityNotifications = async () => {
    try {
      // 检查本次会话是否已经显示过弹窗
      const hasShownModal = sessionStorage.getItem('activity_modal_shown');

      // 如果本次会话已经显示过，直接返回
      if (hasShownModal === 'true') {
        return;
      }

      // 获取用户的通知列表
      const response = await getUserNotifications({
        page: 1,
        pageSize: 10
      });

      // 筛选出需要弹窗显示的通知：
      // 1. 未读的
      // 2. 类型是活动或公告
      // 3. displayType 包含 'modal'
      const modalNotifications = response.items.filter(n =>
        !n.isRead &&
        (n.type === NotificationType.EVENT || n.type === NotificationType.ANNOUNCEMENT) &&
        n.displayType?.includes('modal')
      );

      // 如果有需要显示的通知，显示第一个
      if (modalNotifications.length > 0) {
        const notification = modalNotifications[0];
        setActivityNotification(notification);
        setShowActivityModal(true);

        // 标记本次会话已显示弹窗
        sessionStorage.setItem('activity_modal_shown', 'true');

        // 标记为已读
        await markNotificationsAsRead([notification.id]);
      }
    } catch (error) {
      console.error('检查活动通知失败:', error);
    }
  };

  const handleCloseActivityModal = () => {
    setShowActivityModal(false);
    setActivityNotification(null);
  };

  // 打开发布弹窗
  const openPublishModal = async (work: Work) => {
    setPublishingWork(work);
    setShowPublishModal(true);

    try {
      // 从后端加载该作品的所有章节
      const fsList = await chaptersFs.list(work.id);
      const chapters = fsList.map(fs => fsToChapter(fs, work.id));
      setChaptersForPublish(chapters);

      // 如果作品已发布，预选已发布的章节
      if (work.isPublished) {
        const publishedChapterIds = chapters
          .filter((ch: any) => ch.isPublished)
          .map((ch: any) => ch.id);
        setSelectedChapters(new Set(publishedChapterIds));
      } else {
        setSelectedChapters(new Set());
      }
    } catch (error: any) {
      console.error('加载章节失败:', error);
      showToast('error', '加载章节失败');
      setChaptersForPublish([]);
      setSelectedChapters(new Set());
    }
  };

  // 关闭发布弹窗
  const closePublishModal = () => {
    setShowPublishModal(false);
    setPublishingWork(null);
    setSelectedChapters(new Set());
  };

  // 切换章节选择
  const toggleChapter = (chapterId: string) => {
    const newSelected = new Set(selectedChapters);
    if (newSelected.has(chapterId)) {
      newSelected.delete(chapterId);
    } else {
      newSelected.add(chapterId);
    }
    setSelectedChapters(newSelected);
  };

  // 全选/取消全选
  const toggleAllChapters = (chapters: any[]) => {
    if (selectedChapters.size === chapters.length) {
      setSelectedChapters(new Set());
    } else {
      setSelectedChapters(new Set(chapters.map(c => c.id)));
    }
  };

  // 处理发布/更新
  const handlePublish = async () => {
    if (!publishingWork) return;

    // 如果没有选中任何章节，说明要取消发布
    if (selectedChapters.size === 0) {
      const confirmed = await confirm({
        title: '取消发布',
        message: `确定要将《${publishingWork.title}》从小说广场下架吗？`,
        variant: 'warning',
      });

      if (!confirmed) return;

      try {
        setIsPublishing(true);
        const response = await DataService.unpublishWork(publishingWork.id);
        showToast('success', response.message);
        closePublishModal();
        await loadWorks();
      } catch (error: any) {
        console.error('取消发布失败:', error);
        showToast('error', error?.message || '取消发布失败');
      } finally {
        setIsPublishing(false);
      }
      return;
    }

    try {
      setIsPublishing(true);
      // 调用后端API发布作品和章节
      const response = await DataService.publishWork(publishingWork.id, Array.from(selectedChapters));

      showToast('success', response.message);
      closePublishModal();
      await loadWorks();
    } catch (error: any) {
      console.error('发布失败:', error);
      showToast('error', error?.message || '发布失败');
    } finally {
      setIsPublishing(false);
    }
  };


  const loadWorks = async (silent = false) => {
    try {
      if (!silent) {
        setIsLoading(true);
      }
      const data = await DataService.getWorks();
      setWorks(data.items || []);
      setSummary(data.summary || null);
      setTotalWorksCount(data.total ?? (data.items ? data.items.length : 0));
    } catch (error) {
      console.error('加载作品失败:', error);
      showToast('error', t('works.messages.loadError'));
    } finally {
      if (!silent) {
        setIsLoading(false);
      }
    }
  };

  // 状态文本映射
  const getStatusText = (status: WorkStatus) => {
    return t(`works.status.${status}`);
  };

  // 状态颜色映射
  const getStatusColor = (status: WorkStatus) => {
    const map: Record<WorkStatus, string> = {
      writing: 'bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300',
      completed: 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300',
      draft: 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300',
      abandoned: 'bg-red-100 dark:bg-red-900/50 text-red-600 dark:text-red-400'
    };
    return map[status] || 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300';
  };

  // 相对时间格式化
  const getRelativeTime = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return t('works.time.today');
    if (diffDays === 1) return t('works.time.yesterday');
    if (diffDays < 7) return t('works.time.daysAgo', { n: diffDays });
    if (diffDays < 30) return t('works.time.weeksAgo', { n: Math.floor(diffDays / 7) });
    if (diffDays < 365) return t('works.time.monthsAgo', { n: Math.floor(diffDays / 30) });
    return t('works.time.yearsAgo', { n: Math.floor(diffDays / 365) });
  };

  const cleanupCoverPreview = () => {
    if (coverPreview && coverPreview.startsWith('blob:')) {
      URL.revokeObjectURL(coverPreview);
    }
  };

  // 打开编辑弹窗
  const openEditModal = (work: Work) => {
    cleanupCoverPreview();
    setEditingWork(work);
    setEditFormData({
      title: work.title,
      description: work.description || '',
      genre: work.genre,
      status: work.status,
      coverImage: work.coverImage || ''
    });
    setPendingCoverFile(null);
    setCoverPreview(work.coverImage || '');
  };

  // 关闭编辑弹窗
  const closeEditModal = () => {
    cleanupCoverPreview();
    setPendingCoverFile(null);
    setCoverPreview('');
    setEditingWork(null);
  };

  // 保存编辑
  const saveEdit = async () => {
    if (!editingWork) return;

    try {
      let coverUrl = editFormData.coverImage;
      if (pendingCoverFile) {
        coverUrl = await DataService.uploadWorkCover(editingWork.id, pendingCoverFile);
      }

      await DataService.updateWork(editingWork.id, {
        title: editFormData.title,
        description: editFormData.description,
        genre: editFormData.genre as WorkGenre,
        status: editFormData.status,
        coverImage: coverUrl
      });

      // 重新加载数据
      await loadWorks();
      closeEditModal();
      showToast('success', t('works.edit.saveSuccess'));
    } catch (error) {
      console.error('保存失败:', error);
      showToast('error', t('works.edit.saveError'));
    }
  };

  // 删除作品
  const handleDelete = async (id: string, title: string) => {
    const confirmed = await confirm({
      title: t('works.delete.title'),
      message: t('works.delete.confirm', { title }),
      variant: 'danger',
    });

    if (!confirmed) return;

    try {
      await DataService.deleteWork(id);
      await loadWorks();
      showToast('success', t('works.delete.success'));
    } catch (error) {
      console.error('删除失败:', error);
      showToast('error', t('works.delete.error'));
    }
  };

  // 打开导出弹窗
  const openExportModal = (work: Work) => {
    const endChapter = work.totalChapters > 0 ? work.totalChapters : 1;
    setExportingWork(work);
    setExportMode('full');
    setExportStartChapter('1');
    setExportEndChapter(String(endChapter));
    setExportError(null);
    setShowExportModal(true);
  };

  const closeExportModal = () => {
    setShowExportModal(false);
    setExportingWork(null);
    setExportError(null);
    setIsExporting(false);
  };

  // 导出作品为TXT
  const handleExport = async () => {
    if (!exportingWork) return;

    try {
      setIsExporting(true);
      setExportError(null);

      let rangeLabel = '';
      let result: TxtExportResult;

      if (exportMode === 'range') {
        const start = parseInt(exportStartChapter, 10);
        const end = parseInt(exportEndChapter, 10);
        const total = exportingWork.totalChapters || 0;

        if (Number.isNaN(start) || Number.isNaN(end)) {
          const message = t('works.export.invalidNumber');
          setExportError(message);
          showToast('error', message);
          setIsExporting(false);
          return;
        }

        if (start < 1 || end < 1) {
          const message = t('works.export.minChapter');
          setExportError(message);
          showToast('error', message);
          setIsExporting(false);
          return;
        }

        if (start > end) {
          const message = t('works.export.startGreaterThanEnd');
          setExportError(message);
          showToast('error', message);
          setIsExporting(false);
          return;
        }

        if (total > 0 && (start > total || end > total)) {
          const message = t('works.export.exceedTotal', { count: total });
          setExportError(message);
          showToast('error', message);
          setIsExporting(false);
          return;
        }

        rangeLabel = start === end ? `（第${start}章）` : `（第${start}-${end}章）`;

        showToast('info', t('common.processing'));
        result = await TxtExportService.export(exportingWork, {
          includeDescription: true,
          chapterRange: { start, end },
        });
      } else {
        showToast('info', t('common.processing'));
        result = await TxtExportService.export(exportingWork, { includeDescription: true });
      }

      if (result.chapterCount === 0) {
        showToast('success', t('works.export.successEmpty', { title: exportingWork.title }));
      } else {
        showToast('success', t('works.export.success', { title: exportingWork.title, count: result.chapterCount, range: rangeLabel }));
      }

      closeExportModal();
    } catch (error: any) {
      console.error('导出失败:', error);
      const message = error?.message || t('works.export.error');
      setExportError(message);
      showToast('error', message);
    } finally {
      setIsExporting(false);
    }
  };

  // 打开导入弹窗
  const openImportModal = () => {
    setShowImportModal(true);
    setImportFile(null);
    setImportPreview(null);
    setImportFormat('json');
    setImportCompleted(false);
    setImportedWorkId(null);
    setImportedChaptersCount(null);
    setImportAutoExtracted(false);
    setScanProgress(null);
    autoNavigateEnabledRef.current = true;
    hasAutoNavigatedRef.current = false;
  };

  // 关闭导入弹窗
  const closeImportModal = () => {
    setShowImportModal(false);
    setImportFile(null);
    setImportPreview(null);
    setIsDraggingFile(false);
    dragCounterRef.current = 0;
    setImportCompleted(false);
    setImportedWorkId(null);
    setImportedChaptersCount(null);
    setImportAutoExtracted(false);
    setScanProgress(null);
    autoNavigateEnabledRef.current = false;
    hasAutoNavigatedRef.current = false;
  };

  // 处理文件选择
  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setImportFile(file);
    setImportPreview(null);

    // 根据文件扩展名自动选择格式
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext === 'json') {
      setImportFormat('json');
    } else if (ext === 'md' || ext === 'markdown') {
      setImportFormat('markdown');
    } else if (ext === 'txt') {
      setImportFormat('txt');
    }

    // 自动预览
    try {
      setIsPreviewing(true);
      const format = ext === 'json' ? 'json' : ext === 'md' || ext === 'markdown' ? 'markdown' : 'txt';
      const preview = await DataService.previewImport(file, format);
      setImportPreview(preview);
    } catch (error: any) {
      console.error('预览失败:', error);
      showToast('error', error?.message || t('works.import.previewError'));
    } finally {
      setIsPreviewing(false);
    }
  };

  // 检查文件类型是否被接受
  const isFileAccepted = (file: File, accept: string): boolean => {
    if (!accept) return true;
    const acceptedTypes = accept.split(',').map(t => t.trim().toLowerCase());
    const fileName = file.name.toLowerCase();
    return acceptedTypes.some(accepted => {
      if (accepted.startsWith('.')) {
        return fileName.endsWith(accepted);
      }
      return false;
    });
  };

  // 处理拖拽文件
  const handleFileDrop = async (file: File) => {
    if (!isFileAccepted(file, '.json,.md,.markdown,.txt')) {
      showToast('error', '不支持的文件格式，请选择 .json、.md 或 .txt 文件');
      return;
    }

    setImportFile(file);
    setImportPreview(null);

    // 根据文件扩展名自动选择格式
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext === 'json') {
      setImportFormat('json');
    } else if (ext === 'md' || ext === 'markdown') {
      setImportFormat('markdown');
    } else if (ext === 'txt') {
      setImportFormat('txt');
    }

    // 自动预览
    try {
      setIsPreviewing(true);
      const format = ext === 'json' ? 'json' : ext === 'md' || ext === 'markdown' ? 'markdown' : 'txt';
      const preview = await DataService.previewImport(file, format);
      setImportPreview(preview);
    } catch (error: any) {
      console.error('预览失败:', error);
      showToast('error', error?.message || t('works.import.previewError'));
    } finally {
      setIsPreviewing(false);
    }
  };

  // 拖拽事件处理
  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (isImporting || isPreviewing || importCompleted) return;

    dragCounterRef.current++;
    if (e.dataTransfer?.items && e.dataTransfer.items.length > 0) {
      setIsDraggingFile(true);
    }
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();

    dragCounterRef.current--;
    if (dragCounterRef.current === 0) {
      setIsDraggingFile(false);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer) {
      e.dataTransfer.dropEffect = 'copy';
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();

    setIsDraggingFile(false);
    dragCounterRef.current = 0;

    if (isImporting || isPreviewing || importCompleted) return;

    const droppedFile = e.dataTransfer?.files?.[0];
    if (droppedFile) {
      handleFileDrop(droppedFile);
    }
  };

  // 执行导入
  const handleImport = async () => {
    if (!importFile) {
      showToast('error', t('works.import.selectFileError'));
      return;
    }
    if (importCompleted) return;

    try {
      setIsImporting(true);
      setImportCompleted(false);
      setScanProgress(null);
      const options: ImportOptions = {
        format: importFormat,
        createNew: true,
        includeGuidelines: true,
      };

      const result = await DataService.importWork(importFile, options);
      console.log('[导入结果]', result);
      const chaptersCount = result.chaptersCreated ?? 0;
      const workId = result.workId;
      autoNavigateEnabledRef.current = false;
      hasAutoNavigatedRef.current = false;

      // 导入成功提示改为静默，避免弹窗遮挡进度
      loadWorks(true); // 静默刷新作品列表，避免全屏 loading 覆盖弹窗
      setImportCompleted(true);
      setImportedWorkId(workId);
      setImportedChaptersCount(chaptersCount);
      setImportAutoExtracted(false);

      // 预加载作品详情页需要的数据，避免跳转后再等待
      console.log('[导入] 预加载作品数据...');
      const [workData, fsList, worldData] = await Promise.all([
        DataService.getWork(workId),
        chaptersFs.list(workId),
        DataService.getWorldData(workId),
      ]);
      const chaptersData = fsList.map(fs => fsToChapter(fs, workId));

      closeImportModal();
      navigate(`/works/${workId}`, {
        state: {
          preloadedData: {
            work: workData,
            chapters: chaptersData,
            worldData: worldData,
          },
        }
      });
    } catch (error: any) {
      console.error('导入失败:', error);
      showToast('error', error?.message || t('works.import.error'));
    } finally {
      setIsImporting(false);
    }
  };

  const handleCloseAfterImport = () => {
    autoNavigateEnabledRef.current = false;
    closeImportModal();
  };

  const handleGoToImportedWork = () => {
    if (!importedWorkId) return;
    autoNavigateEnabledRef.current = false;
    hasAutoNavigatedRef.current = true;
    closeImportModal();
    navigate(`/works/${importedWorkId}`, {
      state: {}
    });
  };

  useEffect(() => {
    if (!showImportModal || !importCompleted || !importAutoExtracted || !importedWorkId) return;

    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | null = null;

    const poll = async () => {
      if (cancelled) return;
      try {
        const progress = await DataService.getWorldviewScanProgress(importedWorkId);
        if (cancelled) return;
        setScanProgress(progress);
        if (progress?.status === 'completed' && autoNavigateEnabledRef.current && !hasAutoNavigatedRef.current) {
          hasAutoNavigatedRef.current = true;
          handleGoToImportedWork();
        }
        return progress;
      } catch (error) {
        console.warn('[WorksView] 获取世界观解析进度失败:', error);
        return null;
      }
    };

    const scheduleNext = async () => {
      const progress = await poll();
      if (cancelled) return;
      const status = progress?.status || 'idle';
      if (status === 'completed' || status === 'failed') {
        return;
      }
      const delay = (status === 'running' || status === 'preparing' || status === 'applying') ? 5000 : 8000;
      timer = setTimeout(scheduleNext, delay);
    };

    scheduleNext();

    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [showImportModal, importCompleted, importAutoExtracted, importedWorkId]);

  const isImportLocked = isPreviewing || isImporting || importCompleted;
  const shouldShowScanProgress = importCompleted && importAutoExtracted && Boolean(importedWorkId);
  const scanStatus = scanProgress?.status ?? 'idle';
  const scanPercent = Math.min(Math.max(scanProgress?.progressPercentage ?? 0, 0), 100);
  const scanChaptersTotal = scanProgress?.chaptersTotal || importedChaptersCount || 0;
  const scanChaptersProcessed = scanProgress?.chaptersProcessed ?? 0;
  const scanBatchesTotal = scanProgress?.batchesTotal ?? 0;
  const scanBatchesCompleted = scanProgress?.batchesCompleted ?? 0;
  const scanStatusLabel =
    scanStatus === 'completed'
      ? '解析完成'
      : scanStatus === 'failed'
        ? '解析失败'
        : scanStatus === 'applying'
          ? '应用中'
          : scanStatus === 'running'
            ? '解析中'
            : scanStatus === 'preparing'
              ? '准备中'
              : '排队中';
  const scanStatusColor =
    scanStatus === 'completed'
      ? 'bg-green-500'
      : scanStatus === 'failed'
        ? 'bg-red-500'
        : scanStatus === 'applying'
          ? 'bg-indigo-500'
          : 'bg-blue-500';
  const scanChaptersLabel =
    scanChaptersTotal
      ? `已处理 ${scanChaptersProcessed}/${scanChaptersTotal} 章`
      : scanStatus === 'preparing'
        ? '准备中'
        : '等待开始';
  const hasBatchInfo = scanBatchesCompleted > 0 || scanBatchesTotal > 0;

  // 筛选和排序
  const filteredWorks = works
    .filter(work => {
      const matchesSearch = work.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           (work.description && work.description.toLowerCase().includes(searchQuery.toLowerCase()));
      const matchesStatus = selectedStatus === 'all' || work.status === selectedStatus;
      const matchesGenre = selectedGenre === 'all' || work.genre === selectedGenre;
      return matchesSearch && matchesStatus && matchesGenre;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
        case 'words':
          return b.totalWords - a.totalWords;
        case 'title':
          return a.title.localeCompare(b.title, 'zh-CN');
        default:
          return 0;
      }
    });

  // 统计数据
  const totalWords = summary?.totalWords ?? works.reduce((sum, work) => sum + work.totalWords, 0);
  const writingCount = summary?.writingCount ?? works.filter(work => work.status === 'writing').length;

  // 获取本周新增字数（示例：使用最近7天内更新的作品字数）
  const weekNewWords = summary?.weeklyNewWords ?? 0;

  // 所有类型列表
  const allGenres = ['all', ...Array.from(new Set(works.map(work => work.genre).filter(Boolean)))];

  // 类型显示名称映射
  const getGenreDisplayName = (genre: string) => {
    if (genre === 'all') return t('works.genre.all');
    return t(`works.genre.${genre}`, { defaultValue: genre });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#fafafa] dark:bg-gray-900 flex items-center justify-center">
        <div className="text-gray-500 dark:text-gray-400">{t('common.loading')}</div>
      </div>
    );
  }

  return (
    <div className="bg-[#fafafa] dark:bg-gray-900 flex flex-col overflow-hidden h-full min-h-full">
      {/* Header */}
      <header className="bg-[#fafafa] dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
        <div className="w-full max-w-[1400px] mx-auto px-12 py-4">
          {/* 第一行：标题和按钮 */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-6">
              <div className="relative">
                <div className="bg-black text-white dark:bg-gray-800 dark:text-gray-100 px-6 py-2.5 rounded-lg" style={{ transform: 'skewX(-2deg)' }}>
                  <h1 className="text-xl font-medium" style={{ transform: 'skewX(2deg)' }}>{t('works.title')}</h1>
                </div>
              </div>
              <div className="flex items-center gap-1" style={{ fontSize: '13px' }}>
                <span className="text-gray-400 dark:text-gray-500">{t('works.totalWorks', { count: totalWorksCount }).split(String(totalWorksCount))[0]}</span>
                <span className="text-gray-900 dark:text-gray-100 font-medium">{totalWorksCount}</span>
                <span className="text-gray-400 dark:text-gray-500">{t('works.totalWorks', { count: totalWorksCount }).split(String(totalWorksCount))[1] || ''}</span>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={openImportModal}
                className="px-5 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-800 hover:border-gray-900 dark:hover:border-gray-400 transition-colors flex items-center gap-2 rounded-lg"
                style={{ transform: 'skewX(-2deg)', fontSize: '13px' }}
              >
                <Upload className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                <span style={{ transform: 'skewX(2deg)' }}>{t('works.import.button')}</span>
              </button>
              <button
                onClick={() => navigate('/works/create')}
                className="px-5 py-2.5 bg-black dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-white transition-colors flex items-center gap-2 rounded-lg"
                style={{ transform: 'skewX(-2deg)', fontSize: '13px' }}
              >
                <Plus className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                <span style={{ transform: 'skewX(2deg)' }}>{t('works.create')}</span>
              </button>
            </div>
          </div>

          {/* 第二行：统计卡片 */}
          <div className="flex gap-4 mb-4">
            <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-5 py-3 flex-1 rounded-lg" style={{ transform: 'skewX(-2deg)' }}>
              <div style={{ transform: 'skewX(2deg)' }}>
                <div className="text-gray-400 dark:text-gray-500 mb-1" style={{ fontSize: '11px' }}>{t('works.stats.totalWords')}</div>
                <div className="text-2xl text-gray-900 dark:text-gray-100 font-medium">{totalWords.toLocaleString()}</div>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-5 py-3 flex-1 rounded-lg" style={{ transform: 'skewX(-2deg)' }}>
              <div style={{ transform: 'skewX(2deg)' }}>
                <div className="text-gray-400 dark:text-gray-500 mb-1" style={{ fontSize: '11px' }}>{t('works.stats.weeklyNew')}</div>
                <div className="text-2xl text-gray-900 dark:text-gray-100 font-medium">{weekNewWords > 0 ? '+' : ''}{weekNewWords.toLocaleString()}</div>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-5 py-3 flex-1 rounded-lg" style={{ transform: 'skewX(-2deg)' }}>
              <div style={{ transform: 'skewX(2deg)' }}>
                <div className="text-gray-400 dark:text-gray-500 mb-1" style={{ fontSize: '11px' }}>{t('works.stats.ongoing')}</div>
                <div className="text-2xl text-gray-900 dark:text-gray-100 font-medium">{writingCount}</div>
              </div>
            </div>
          </div>

          {/* 第三行：搜索和筛选 */}
          <div className="flex items-center gap-3">
            {/* 搜索框 */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder={t('works.search.placeholder')}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none focus:border-gray-900 dark:focus:border-gray-400 transition-colors rounded-lg"
                style={{ fontSize: '13px' }}
              />
            </div>

            {/* 状态筛选 */}
            <div className="flex gap-1">
              {['all', 'writing', 'draft', 'completed'].map(status => (
                <button
                  key={status}
                  onClick={() => setSelectedStatus(status)}
                  className={`px-3 py-2 border transition-colors rounded-lg ${
                    selectedStatus === status
                      ? 'bg-black dark:bg-gray-100 text-white dark:text-gray-900 border-black dark:border-gray-100'
                      : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-700 hover:border-gray-900 dark:hover:border-gray-400'
                  }`}
                  style={{ transform: 'skewX(-2deg)', fontSize: '10px' }}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>
                    {status === 'all' ? t('works.status.all') : getStatusText(status as WorkStatus)}
                  </span>
                </button>
              ))}
            </div>

            {/* 类型筛选 */}
            <Select value={selectedGenre} onValueChange={setSelectedGenre}>
              <SelectTrigger
                className="w-[90px] bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700"
                size="sm"
                style={{ transform: 'skewX(-2deg)', fontSize: '10px' }}
              >
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {allGenres.map(genre => (
                  <SelectItem key={genre} value={genre}>
                    {getGenreDisplayName(genre)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* 排序 */}
            <Select value={sortBy} onValueChange={(value) => setSortBy(value as any)}>
              <SelectTrigger
                className="w-[90px] bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700"
                size="sm"
                style={{ transform: 'skewX(-2deg)', fontSize: '10px' }}
              >
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="date">{t('works.sort.date')}</SelectItem>
                <SelectItem value="words">{t('works.sort.words')}</SelectItem>
                <SelectItem value="title">{t('works.sort.title')}</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="w-full max-w-[1400px] mx-auto px-12 pt-8 overflow-y-auto scrollbar-hide flex-1">
        {filteredWorks.length === 0 ? (
          // 空状态
          <div className="flex flex-col items-center justify-center h-full">
            <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 p-12 text-center rounded-lg" style={{ transform: 'skewX(-2deg)' }}>
              <div style={{ transform: 'skewX(2deg)' }}>
                <BookOpen className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                <h3 className="text-lg text-gray-900 dark:text-gray-100 mb-2">{t('works.empty')}</h3>
                <p className="text-gray-400 dark:text-gray-500 mb-6" style={{ fontSize: '11px' }}>
                  {searchQuery || selectedStatus !== 'all' || selectedGenre !== 'all'
                    ? t('works.emptyFilterDesc')
                    : t('works.emptyDesc')}
                </p>
                {!searchQuery && selectedStatus === 'all' && selectedGenre === 'all' && (
                  <button
                    onClick={() => navigate('/works/create')}
                    className="px-6 py-2.5 bg-black dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-white transition-colors inline-flex items-center gap-2 rounded-lg"
                    style={{ transform: 'skewX(-2deg)', fontSize: '11px' }}
                  >
                    <Plus className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                    <span style={{ transform: 'skewX(2deg)' }}>{t('works.create')}</span>
                  </button>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredWorks.map((work) => (
              <div
                key={work.id}
                className="group bg-white dark:bg-gray-800 overflow-hidden transition-all duration-300 ease-out border border-gray-100 dark:border-gray-700 hover:border-gray-900 dark:hover:border-gray-400 h-[140px] hover:h-[160px] hover:my-4 hover:shadow-2xl relative cursor-pointer rounded-lg"
                style={{ transform: 'skewX(-2deg)', transitionProperty: 'all' }}
                onClick={() => navigate(`/works/${work.id}`)}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'skewX(-3deg)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'skewX(-2deg)';
                }}
              >
                <div className="flex h-full">
                  {/* Cover - 左侧封面 */}
                  <div className="w-[200px] flex-shrink-0 overflow-hidden" style={{ height: '100%' }}>
                    <img
                      src={work.coverImage || DEFAULT_COVER_IMAGE}
                      alt={work.title}
                      className="object-cover transition-transform duration-300 ease-out group-hover:scale-105"
                      style={{ width: '200px', height: '100%', display: 'block' }}
                      onError={(e) => {
                        // 如果图片加载失败，显示默认图标
                        e.currentTarget.style.display = 'none';
                        const parent = e.currentTarget.parentElement;
                        if (parent && !parent.querySelector('.fallback-icon')) {
                          const fallback = document.createElement('div');
                          fallback.className = 'fallback-icon absolute inset-0 w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center';
                          fallback.innerHTML = '<svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>';
                          parent.appendChild(fallback);
                        }
                      }}
                    />
                  </div>

                  {/* Content - 右侧信息 */}
                  <div className="flex-1 p-5 flex items-center transition-all duration-300 ease-out" style={{ transform: 'skewX(2deg)' }}>
                    <div className="flex-1 transition-transform duration-300 ease-out group-hover:scale-105" style={{ transformOrigin: 'left center' }}>
                      {/* Title & Status */}
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 group-hover:text-black dark:group-hover:text-white transition-colors">
                          {work.title}
                        </h3>
                        <span className={`px-2 py-0.5 rounded ${getStatusColor(work.status)}`} style={{ fontSize: '11px' }}>
                          {getStatusText(work.status)}
                        </span>
                        {work.genre && (
                          <span className="px-2 py-0.5 bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded" style={{ fontSize: '11px' }}>
                            {getGenreDisplayName(work.genre)}
                          </span>
                        )}
                      </div>

                      {/* Description */}
                      {work.description && (
                        <p className="text-gray-500 dark:text-gray-400 mb-2 line-clamp-1" style={{ fontSize: '13px' }}>
                          {work.description}
                        </p>
                      )}

                      {/* Progress Bar - 进度条 */}
                      {work.totalWords > 0 && (
                        <div className="mb-2">
                          <div className="flex items-center gap-2 mb-0.5">
                            <span className="text-gray-400 dark:text-gray-500" style={{ fontSize: '10px' }}>{t('works.stats.progress')}</span>
                            <span className="text-gray-500 dark:text-gray-400" style={{ fontSize: '10px' }}>
                              {work.totalWords.toLocaleString()} / {(100000).toLocaleString()} {t('works.stats.words')}
                            </span>
                          </div>
                          <div className="w-2/3 bg-gray-200 dark:bg-gray-700 h-1 overflow-hidden rounded" style={{ transform: 'skewX(-2deg)' }}>
                            <div
                              className={`h-1 transition-all ${work.status === 'writing' ? 'bg-black dark:bg-gray-100 progress-stripes' : 'bg-black dark:bg-gray-100'}`}
                              style={{
                                width: `${Math.min((work.totalWords / 100000) * 100, 100)}%`,
                                boxShadow: '0 0 6px rgba(0, 0, 0, 0.2)'
                              }}
                            ></div>
                          </div>
                        </div>
                      )}

                      {/* Stats */}
                      <div className="flex items-center gap-4 text-gray-400 dark:text-gray-500" style={{ fontSize: '13px' }}>
                        <div className="flex items-center gap-1.5">
                          <Clock className="w-3.5 h-3.5" />
                          <span>{getRelativeTime(work.updatedAt)}</span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <BookOpen className="w-3.5 h-3.5" />
                          <span>{work.totalChapters} {t('works.stats.chapters')}</span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <FileText className="w-3.5 h-3.5" />
                          <span>{work.totalWords.toLocaleString()} {t('works.stats.words')}</span>
                        </div>
                        {work.status === 'writing' && (
                          <div className="flex items-center gap-1.5 text-green-600">
                            <TrendingUp className="w-3.5 h-3.5" />
                            <span>{t('works.stats.updating')}</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Actions - 右侧操作按钮 */}
                    <div className="flex items-center gap-2 ml-4 flex-shrink-0">
                      {/* 发布状态指示器 */}
                      {work.isPublished && (
                        <div className="flex items-center gap-1 text-green-600 dark:text-green-400 text-xs px-2 py-1 bg-green-50 dark:bg-green-900/30 rounded">
                          <Globe className="w-3 h-3" />
                          <span>已发布</span>
                        </div>
                      )}

                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/works/${work.id}`);
                        }}
                        className="px-4 py-1.5 bg-black dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-white transition-colors rounded-lg"
                        style={{ transform: 'skewX(-2deg)', fontSize: '13px' }}
                      >
                        <span style={{ transform: 'skewX(2deg)', display: 'inline-block' }}>{t('works.viewDetails')}</span>
                      </button>

                      {/* Quick Actions - hover时显示 */}
                      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        {/* 发布管理按钮 */}
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            openPublishModal(work);
                          }}
                          className="p-2 hover:bg-green-50 dark:hover:bg-green-900/30 transition-colors rounded-lg"
                          title={work.isPublished ? "管理发布" : "发布到小说广场"}
                        >
                          <Globe className="w-3.5 h-3.5 text-green-600 dark:text-green-400" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            openEditModal(work);
                          }}
                          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors rounded-lg"
                          title={t('works.editInfo')}
                        >
                          <Edit3 className="w-3.5 h-3.5 text-gray-600 dark:text-gray-400" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            openExportModal(work);
                          }}
                          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors rounded-lg"
                          title={t('works.export.button')}
                        >
                          <Download className="w-3.5 h-3.5 text-gray-600 dark:text-gray-400" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDelete(work.id, work.title);
                          }}
                          className="p-2 hover:bg-red-50 dark:hover:bg-red-900/30 transition-colors rounded-lg"
                          title={t('works.delete.button')}
                        >
                          <Trash2 className="w-3.5 h-3.5 text-red-500" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* 编辑弹窗 */}
      {editingWork && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={closeEditModal}>
          <div className="bg-white dark:bg-gray-800 w-[500px] max-h-[600px] overflow-y-auto scrollbar-hide rounded-xl" style={{ transform: 'skewX(-2deg)' }} onClick={(e) => e.stopPropagation()}>
            <div style={{ transform: 'skewX(2deg)' }} className="p-6">
              {/* 标题栏 */}
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg text-gray-900 dark:text-gray-100">{t('works.edit.title')}</h2>
                <button onClick={closeEditModal} className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors rounded-lg">
                  <X className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                </button>
              </div>

              {/* 表单 */}
              <div className="space-y-3">
                {/* 标题 */}
                <div>
                  <label className="block text-gray-700 dark:text-gray-300 mb-1" style={{ fontSize: '11px' }}>{t('works.edit.workTitle')}</label>
                  <input
                    type="text"
                    value={editFormData.title}
                    onChange={(e) => setEditFormData({ ...editFormData, title: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:border-gray-900 dark:focus:border-gray-400 transition-colors rounded-lg"
                    style={{ fontSize: '12px' }}
                    placeholder={t('works.edit.workTitlePlaceholder')}
                  />
                </div>

                {/* 简介 */}
                <div>
                  <label className="block text-gray-700 dark:text-gray-300 mb-1" style={{ fontSize: '11px' }}>{t('works.edit.description')}</label>
                  <textarea
                    value={editFormData.description}
                    onChange={(e) => setEditFormData({ ...editFormData, description: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:border-gray-900 dark:focus:border-gray-400 transition-colors resize-none rounded-lg"
                    style={{ fontSize: '12px' }}
                    rows={2}
                    placeholder={t('works.edit.descriptionPlaceholder')}
                  />
                </div>

                {/* 类型和状态 */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-gray-700 dark:text-gray-300 mb-1" style={{ fontSize: '11px' }}>{t('works.edit.genre')}</label>
                    <Select
                      value={editFormData.genre || 'none'}
                      onValueChange={(value) => setEditFormData({ ...editFormData, genre: value === 'none' ? '' : value as WorkGenre })}
                    >
                      <SelectTrigger className="w-full" size="sm">
                        <SelectValue placeholder={t('works.genre.selectGenre')} />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="none">{t('works.genre.selectGenre')}</SelectItem>
                        {['fantasy', 'urban', 'romance', 'scifi', 'wuxia', 'game', 'history', 'military', 'other'].map((genre) => (
                          <SelectItem key={genre} value={genre}>{t(`works.genre.${genre}`)}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="block text-gray-700 dark:text-gray-300 mb-1" style={{ fontSize: '11px' }}>{t('works.edit.status')}</label>
                    <Select
                      value={editFormData.status}
                      onValueChange={(value) => setEditFormData({ ...editFormData, status: value as WorkStatus })}
                    >
                      <SelectTrigger className="w-full" size="sm">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="draft">{t('works.status.draft')}</SelectItem>
                        <SelectItem value="writing">{t('works.status.writing')}</SelectItem>
                        <SelectItem value="completed">{t('works.status.completed')}</SelectItem>
                        <SelectItem value="abandoned">{t('works.status.abandoned')}</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {/* 封面图片上传 */}
                <div>
                  <label className="block text-gray-700 dark:text-gray-300 mb-1" style={{ fontSize: '11px' }}>{t('works.edit.cover')}</label>
                  <input
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (!file) return;

                      cleanupCoverPreview();
                      const previewUrl = URL.createObjectURL(file);
                      setCoverPreview(previewUrl);
                      setPendingCoverFile(file);
                    }}
                    className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:border-gray-900 dark:focus:border-gray-400 transition-colors cursor-pointer"
                    style={{ fontSize: '12px' }}
                  />
                  {(coverPreview || editFormData.coverImage) && (
                    <div className="mt-2">
                      <img
                        src={coverPreview || editFormData.coverImage}
                        alt={t('works.edit.coverPreview')}
                        className="w-full h-32 object-cover border border-gray-200 dark:border-gray-600 rounded-lg"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none';
                        }}
                      />
                    </div>
                  )}
                </div>
              </div>

              {/* 底部按钮 */}
              <div className="flex items-center gap-2 mt-6">
                <button
                  onClick={closeEditModal}
                  className="flex-1 px-4 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-700 hover:border-gray-900 dark:hover:border-gray-400 transition-colors rounded-lg"
                  style={{ transform: 'skewX(-2deg)', fontSize: '11px' }}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>{t('works.edit.cancel')}</span>
                </button>
                <button
                  onClick={saveEdit}
                  className="flex-1 px-4 py-2.5 bg-black dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-white transition-colors rounded-lg"
                  style={{ transform: 'skewX(-2deg)', fontSize: '11px' }}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>{t('works.edit.save')}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 导入弹窗 */}
      {showImportModal && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
          onClick={closeImportModal}
          onDragOver={(e) => { e.preventDefault(); e.stopPropagation(); }}
          onDrop={(e) => { e.preventDefault(); e.stopPropagation(); }}
        >
          <div className="bg-white dark:bg-gray-800 w-[550px] max-h-[80vh] overflow-hidden rounded-2xl flex flex-col" onClick={(e) => e.stopPropagation()}>
            <div className="p-6 overflow-y-auto scrollbar-hide">
              {/* 标题栏 */}
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-base text-gray-900 dark:text-gray-100">{t('works.import.title')}</h2>
                <button onClick={closeImportModal} className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors rounded-lg">
                  <X className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                </button>
              </div>

              {/* 文件选择区域 */}
              <div className="mb-3">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".json,.md,.markdown,.txt"
                  onChange={handleFileSelect}
                  className="hidden"
                  disabled={isImportLocked}
                />
                <div
                  onClick={() => {
                    if (isImportLocked) return;
                    fileInputRef.current?.click();
                  }}
                  onDragEnter={handleDragEnter}
                  onDragLeave={handleDragLeave}
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  className={`border-2 border-dashed rounded-2xl p-8 text-center transition-colors ${
                    isImportLocked
                      ? 'opacity-50 cursor-not-allowed border-gray-300 dark:border-gray-600'
                      : isDraggingFile
                        ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 cursor-pointer'
                        : 'border-gray-300 dark:border-gray-600 hover:border-gray-900 dark:hover:border-gray-400 cursor-pointer'
                  }`}
                >
                  {importFile ? (
                    <div className="flex items-center justify-center gap-2">
                      <File className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                      <span className="text-gray-900 dark:text-gray-100" style={{ fontSize: '12px' }}>{importFile.name}</span>
                      <span className="text-gray-400 dark:text-gray-500" style={{ fontSize: '11px' }}>
                        ({(importFile.size / 1024).toFixed(1)} KB)
                      </span>
                    </div>
                  ) : (
                    <div>
                      <Upload className={`w-8 h-8 mx-auto mb-2 ${isDraggingFile ? 'text-blue-500' : 'text-gray-400 dark:text-gray-500'}`} />
                      <p className={`${isDraggingFile ? 'text-blue-600 dark:text-blue-400' : 'text-gray-600 dark:text-gray-400'}`} style={{ fontSize: '13px' }}>
                        {isDraggingFile ? '松开鼠标导入文件' : t('works.import.dropHint')}
                      </p>
                      <p className="text-gray-400 dark:text-gray-500 mt-1" style={{ fontSize: '11px' }}>{t('works.import.formatHint')}</p>
                    </div>
                  )}
                </div>
              </div>

              {/* 格式说明 */}
              <div className="mb-3 p-2.5 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg" style={{ fontSize: '11px' }}>
                <p className="text-gray-600 dark:text-gray-400 mb-1"><strong>JSON</strong>：{t('works.import.jsonFormat').replace('JSON格式：', '').replace('JSON: ', '')}</p>
                <p className="text-gray-600 dark:text-gray-400 mb-1"><strong>Markdown</strong>：{t('works.import.markdownFormat').replace('Markdown格式：', '').replace('Markdown: ', '')}</p>
                <p className="text-gray-600 dark:text-gray-400"><strong>TXT</strong>：{t('works.import.txtFormat').replace('TXT格式：', '').replace('TXT: ', '')}</p>
              </div>

              {/* 预览加载中 */}
              {isPreviewing && (
                <div className="mb-3 p-3 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-center rounded-lg">
                  <div className="animate-spin w-6 h-6 border-2 border-gray-300 dark:border-gray-500 border-t-gray-900 dark:border-t-gray-100 rounded-full mx-auto mb-2"></div>
                  <p className="text-gray-600 dark:text-gray-400" style={{ fontSize: '12px' }}>{t('works.import.parsing')}</p>
                </div>
              )}

              {/* 预览结果 */}
              {importPreview && !isPreviewing && (
                <div className="mb-3 p-3 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg">
                  <h3 className="text-gray-900 dark:text-gray-100 font-medium mb-2" style={{ fontSize: '12px' }}>{t('works.import.preview')}</h3>

                  <div className="space-y-1" style={{ fontSize: '12px' }}>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">{t('works.import.workTitle')}</span>
                      <span className="text-gray-900 dark:text-gray-100 font-medium">{importPreview.work.title}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">{t('works.import.chapterCount')}</span>
                      <span className="text-gray-900 dark:text-gray-100">{importPreview.work.totalChapters} {t('works.stats.chapters')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">{t('works.import.totalWords')}</span>
                      <span className="text-gray-900 dark:text-gray-100">{importPreview.work.totalWords.toLocaleString()} {t('works.stats.words')}</span>
                    </div>
                  </div>

                  {/* 章节列表 */}
                  {importPreview.chapters.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-600">
                      <div className="space-y-1">
                        {importPreview.chapters.slice(0, 3).map((chapter, idx) => (
                          <div key={idx} className="flex justify-between text-gray-500 dark:text-gray-400" style={{ fontSize: '11px' }}>
                            <span className="truncate flex-1 mr-2">{chapter.title}</span>
                            <span>{chapter.wordCount.toLocaleString()} {t('works.stats.words')}</span>
                          </div>
                        ))}
                        {importPreview.chapters.length > 3 && (
                          <p className="text-gray-400 dark:text-gray-500" style={{ fontSize: '11px' }}>
                            {t('works.import.moreChapters', { count: importPreview.chapters.length - 3 })}
                          </p>
                        )}
                      </div>
                    </div>
                  )}

                  {/* 警告信息 */}
                  {importPreview.warnings.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-600">
                      {importPreview.warnings.map((warning, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-yellow-600 dark:text-yellow-400" style={{ fontSize: '11px' }}>
                          <AlertCircle className="w-3.5 h-3.5" />
                          <span>{warning}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {shouldShowScanProgress && (
                <div className="mb-3 p-3 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg">
                  <div className="flex items-center justify-between">
                    <h3 className="text-gray-900 dark:text-gray-100 font-medium" style={{ fontSize: '12px' }}>世界观解析进度</h3>
                    <span className="text-gray-500 dark:text-gray-400" style={{ fontSize: '11px' }}>{scanStatusLabel}</span>
                  </div>
                  <div className="mt-2 w-full bg-gray-200 dark:bg-gray-600 h-2 rounded-full overflow-hidden">
                    <div
                      className={`h-2 transition-all ${scanStatusColor}`}
                      style={{ width: `${scanStatus === 'completed' ? 100 : scanPercent}%` }}
                    ></div>
                  </div>
                  <div className="mt-1 flex items-center justify-between text-gray-500 dark:text-gray-400" style={{ fontSize: '11px' }}>
                    <span>{scanChaptersLabel}</span>
                    {hasBatchInfo && (
                      <span>
                        {scanBatchesTotal > 0
                          ? `批次 ${scanBatchesCompleted}/${scanBatchesTotal}`
                          : `批次 ${scanBatchesCompleted}`}
                      </span>
                    )}
                  </div>
                  {scanStatus === 'failed' && scanProgress?.lastError && (
                    <div className="mt-1 text-red-500" style={{ fontSize: '11px' }}>
                      {scanProgress.lastError}
                    </div>
                  )}
                </div>
              )}

              {/* 底部按钮 */}
              <div className="flex items-center gap-2 mt-4">
                {importCompleted && importAutoExtracted ? (
                  <>
                    <button
                      onClick={handleCloseAfterImport}
                      className="flex-1 px-4 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-700 hover:border-gray-900 dark:hover:border-gray-400 transition-colors rounded-lg"
                      style={{ transform: 'skewX(-2deg)', fontSize: '12px' }}
                    >
                      <span style={{ transform: 'skewX(2deg)' }}>继续后台解析</span>
                    </button>
                    <button
                      onClick={handleGoToImportedWork}
                      className="flex-1 px-4 py-2.5 transition-colors flex items-center justify-center gap-2 bg-black dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-white rounded-lg"
                      style={{ transform: 'skewX(-2deg)', fontSize: '12px' }}
                      disabled={!importedWorkId}
                    >
                      <EyeIcon className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                      <span style={{ transform: 'skewX(2deg)' }}>查看作品详情</span>
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      onClick={closeImportModal}
                      className="flex-1 px-4 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-700 hover:border-gray-900 dark:hover:border-gray-400 transition-colors rounded-lg"
                      style={{ transform: 'skewX(-2deg)', fontSize: '12px' }}
                      disabled={isImporting}
                    >
                      <span style={{ transform: 'skewX(2deg)' }}>{t('works.import.cancel')}</span>
                    </button>
                    <button
                      onClick={handleImport}
                      disabled={!importFile || !importPreview || isImporting}
                      className={`flex-1 px-4 py-2.5 transition-colors flex items-center justify-center gap-2 ${
                        !importFile || !importPreview || isImporting
                          ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                          : 'bg-black dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-white'
                      } rounded-lg`}
                      style={{ transform: 'skewX(-2deg)', fontSize: '12px' }}
                    >
                      {isImporting ? (
                        <>
                          <div className="animate-spin w-4 h-4 border-2 border-white/30 border-t-white rounded-full"></div>
                          <span style={{ transform: 'skewX(2deg)' }}>{t('works.import.importing')}</span>
                        </>
                      ) : (
                        <>
                          <CheckCircle className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                          <span style={{ transform: 'skewX(2deg)' }}>{t('works.import.confirm')}</span>
                        </>
                      )}
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 导出弹窗 */}
      {showExportModal && exportingWork && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={closeExportModal}>
          <div className="bg-white dark:bg-gray-800 w-[520px] max-h-[640px] overflow-y-auto scrollbar-hide rounded-xl" style={{ transform: 'skewX(-2deg)' }} onClick={(e) => e.stopPropagation()}>
            <div style={{ transform: 'skewX(2deg)' }} className="p-6 space-y-5">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg text-gray-900 dark:text-gray-100">{t('works.export.title')}</h2>
                  <p className="text-[12px] text-gray-500 dark:text-gray-400 mt-1">《{exportingWork.title}》 · {t('works.export.totalChapters', { count: exportingWork.totalChapters })}</p>
                </div>
                <button onClick={closeExportModal} className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors rounded-lg">
                  <X className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                </button>
              </div>

              <div className="space-y-2">
                <label className="text-[12px] text-gray-700 dark:text-gray-300">{t('works.export.mode')}</label>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => setExportMode('full')}
                    className={`px-4 py-3 border text-sm transition-colors rounded-lg ${
                      exportMode === 'full'
                        ? 'bg-black dark:bg-gray-100 text-white dark:text-gray-900 border-black dark:border-gray-100'
                        : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-600 hover:border-gray-900 dark:hover:border-gray-400'
                    }`}
                    style={{ transform: 'skewX(-2deg)' }}
                  >
                    <span style={{ transform: 'skewX(2deg)' }} className="block text-left">
                      <span className="font-medium">{t('works.export.fullExport')}</span>
                      <span className="block text-[11px] text-gray-400 dark:text-gray-500">{t('works.export.fullExportDesc')}</span>
                    </span>
                  </button>
                  <button
                    onClick={() => setExportMode('range')}
                    className={`px-4 py-3 border text-sm transition-colors rounded-lg ${
                      exportMode === 'range'
                        ? 'bg-black dark:bg-gray-100 text-white dark:text-gray-900 border-black dark:border-gray-100'
                        : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-600 hover:border-gray-900 dark:hover:border-gray-400'
                    }`}
                    style={{ transform: 'skewX(-2deg)' }}
                  >
                    <span style={{ transform: 'skewX(2deg)' }} className="block text-left">
                      <span className="font-medium">{t('works.export.rangeExport')}</span>
                      <span className="block text-[11px] text-gray-400 dark:text-gray-500">{t('works.export.rangeExportDesc')}</span>
                    </span>
                  </button>
                </div>
              </div>

              {exportMode === 'range' && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-[12px] text-gray-500 dark:text-gray-400">
                    <span>{t('works.export.selectRange')}</span>
                    <span>{t('works.export.totalChapters', { count: exportingWork.totalChapters })}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-gray-700 dark:text-gray-300 mb-1" style={{ fontSize: '12px' }}>{t('works.export.fromChapter')}</label>
                      <input
                        type="number"
                        min={1}
                        value={exportStartChapter}
                        onChange={(e) => setExportStartChapter(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:border-gray-900 dark:focus:border-gray-400 transition-colors rounded-lg"
                        style={{ fontSize: '13px' }}
                      />
                    </div>
                    <div>
                      <label className="block text-gray-700 dark:text-gray-300 mb-1" style={{ fontSize: '12px' }}>{t('works.export.toChapter')}</label>
                      <input
                        type="number"
                        min={1}
                        value={exportEndChapter}
                        onChange={(e) => setExportEndChapter(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:border-gray-900 dark:focus:border-gray-400 transition-colors rounded-lg"
                        style={{ fontSize: '13px' }}
                      />
                    </div>
                  </div>
                  <p className="text-[11px] text-gray-400 dark:text-gray-500">
                    {t('works.export.rangeHint')}
                  </p>
                </div>
              )}

              {exportError && (
                <div className="bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 text-[12px] px-3 py-2 border border-red-100 dark:border-red-800 rounded-lg">
                  {exportError}
                </div>
              )}

              <div className="flex items-center gap-2 pt-2">
                <button
                  onClick={closeExportModal}
                  className="flex-1 px-4 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-700 hover:border-gray-900 dark:hover:border-gray-400 transition-colors rounded-lg"
                  style={{ transform: 'skewX(-2deg)', fontSize: '12px' }}
                  disabled={isExporting}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>{t('works.export.cancel')}</span>
                </button>
                <button
                  onClick={handleExport}
                  disabled={isExporting}
                  className={`flex-1 px-4 py-2.5 text-white transition-colors rounded-lg ${
                    isExporting ? 'bg-gray-400 dark:bg-gray-600 cursor-not-allowed' : 'bg-black dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-white'
                  }`}
                  style={{ transform: 'skewX(-2deg)', fontSize: '12px' }}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>{isExporting ? t('works.export.exporting') : t('works.export.start')}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 发布弹窗 */}
      {showPublishModal && publishingWork && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={closePublishModal}>
          <div className="bg-white dark:bg-gray-800 w-[600px] max-h-[700px] overflow-y-auto scrollbar-hide rounded-xl" style={{ transform: 'skewX(-2deg)' }} onClick={(e) => e.stopPropagation()}>
            <div style={{ transform: 'skewX(2deg)' }} className="p-6">
              {/* 标题栏 */}
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-lg text-gray-900 dark:text-gray-100">
                    {publishingWork.isPublished ? '管理发布章节' : '发布到小说广场'}
                  </h2>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {publishingWork.isPublished
                      ? '勾选要发布的章节，取消全部勾选将下架作品'
                      : '选择要发布的章节'}
                  </p>
                </div>
                <button onClick={closePublishModal} className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors rounded-lg">
                  <X className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                </button>
              </div>

              {/* 作品信息 */}
              <div className="mb-4 p-4 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg">
                <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">{publishingWork.title}</h3>
                <div className="flex items-center gap-4 text-xs text-gray-600 dark:text-gray-400">
                  <span>共 {publishingWork.totalChapters} 章</span>
                  <span>{publishingWork.totalWords.toLocaleString()} 字</span>
                  {publishingWork.genre && <span>{publishingWork.genre}</span>}
                </div>
              </div>

              {/* 章节选择说明 */}
              <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 text-xs text-blue-700 dark:text-blue-300 rounded-lg">
                {publishingWork.isPublished ? (
                  <div className="space-y-1">
                    <p>• 勾选新章节可以添加到发布列表</p>
                    <p>• 取消勾选章节将从小说广场移除该章节</p>
                    <p>• 取消全部勾选将下架整个作品</p>
                  </div>
                ) : (
                  <p>选择要发布到小说广场的章节。读者将只能看到已发布的章节。</p>
                )}
              </div>

              {/* 全选按钮 */}
              <div className="mb-3 flex items-center justify-between">
                <button
                  onClick={() => toggleAllChapters(chaptersForPublish)}
                  className="px-3 py-1.5 text-xs border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors rounded-lg"
                  style={{ transform: 'skewX(-2deg)' }}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>
                    {selectedChapters.size === chaptersForPublish.length ? '取消全选' : '全选'}
                  </span>
                </button>
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  已选择 {selectedChapters.size} / {chaptersForPublish.length} 章
                </span>
              </div>

              {/* 章节列表 */}
              <div className="space-y-1 mb-4 max-h-[300px] overflow-y-auto border border-gray-200 dark:border-gray-600 rounded-lg">
                {chaptersForPublish.map((chapter) => (
                  <label
                    key={chapter.id}
                    className="flex items-center p-3 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={selectedChapters.has(chapter.id)}
                      onChange={() => toggleChapter(chapter.id)}
                      className="w-4 h-4 mr-3"
                    />
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-900 dark:text-gray-100">{chapter.title}</span>
                        <span className="text-xs text-gray-500 dark:text-gray-400">{chapter.wordCount || 0} 字</span>
                      </div>
                      <div className="text-xs text-gray-400 dark:text-gray-500 mt-0.5">
                        {chapter.updatedAt ? new Date(chapter.updatedAt).toLocaleDateString() : ''}
                      </div>
                    </div>
                  </label>
                ))}
              </div>

              {/* 底部按钮 */}
              <div className="flex items-center gap-2">
                <button
                  onClick={closePublishModal}
                  className="flex-1 px-4 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-700 hover:border-gray-900 dark:hover:border-gray-400 transition-colors rounded-lg"
                  style={{ transform: 'skewX(-2deg)', fontSize: '12px' }}
                  disabled={isPublishing}
                >
                  <span style={{ transform: 'skewX(2deg)' }}>取消</span>
                </button>
                <button
                  onClick={handlePublish}
                  disabled={isPublishing}
                  className={`flex-1 px-4 py-2.5 transition-colors flex items-center justify-center gap-2 ${
                    isPublishing
                      ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                      : selectedChapters.size === 0
                      ? 'bg-orange-600 text-white hover:bg-orange-700'
                      : 'bg-green-600 text-white hover:bg-green-700'
                  }`}
                  style={{ transform: 'skewX(-2deg)', fontSize: '12px' }}
                >
                  {isPublishing ? (
                    <>
                      <div className="animate-spin w-4 h-4 border-2 border-white/30 border-t-white rounded-full"></div>
                      <span style={{ transform: 'skewX(2deg)' }}>处理中...</span>
                    </>
                  ) : selectedChapters.size === 0 ? (
                    <>
                      <EyeIcon className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                      <span style={{ transform: 'skewX(2deg)' }}>取消发布</span>
                    </>
                  ) : (
                    <>
                      <Globe className="w-4 h-4" style={{ transform: 'skewX(2deg)' }} />
                      <span style={{ transform: 'skewX(2deg)' }}>
                        {publishingWork.isPublished ? '更新发布' : '发布到广场'}
                      </span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 确认对话框 */}
      <ConfirmDialog
        isOpen={confirmState.isOpen}
        title={confirmState.title}
        message={confirmState.message}
        variant={confirmState.variant}
        onConfirm={confirmState.onConfirm}
        onCancel={closeConfirm}
      />

      {/* 活动/公告弹窗 */}
      {showActivityModal && activityNotification && (
        <ActivityModal
          notification={activityNotification}
          onClose={handleCloseActivityModal}
        />
      )}
    </div>
  );
};

export default WorksView;
