import { useState, useEffect } from 'react';
import {
  Flag,
  MessageSquare,
  Book,
  MessageCircle,
  CheckCircle,
  XCircle,
  Trash2,
  AlertTriangle,
  Ban,
  Clock,
} from 'lucide-react';
import { DataService } from '../services/DataService';
import { useGlobalStore } from '../store/globalStore';

interface ReportSummary {
  messageReports: { total: number; pending: number; processedToday: number };
  commentReports: { total: number; pending: number; processedToday: number };
  workReports: { total: number; pending: number; processedToday: number };
}

interface MessageReport {
  id: string;
  messageId: string;
  reporterId: string;
  reason: string;
  description: string | null;
  status: string;
  createdAt: string;
  reviewedAt: string | null;
  reviewedBy: string | null;
  messageContent: string | null;
  channelName: string | null;
  reporterName: string | null;
  reportedUserName: string | null;
}

interface CommentReport {
  id: string;
  commentId: string;
  userId: string;
  reason: string;
  description: string | null;
  isProcessed: boolean;
  processedAt: string | null;
  processedBy: string | null;
  createdAt: string;
  commentContent: string | null;
  workTitle: string | null;
  reporterName: string | null;
  commentedUserName: string | null;
}

interface WorkReport {
  id: string;
  workId: string;
  reporterId: string;
  reason: string;
  description: string | null;
  status: string;
  actionTaken: string | null;
  adminNote: string | null;
  reviewedAt: string | null;
  reviewedBy: string | null;
  createdAt: string;
  workTitle: string | null;
  workAuthorName: string | null;
  reporterName: string | null;
}

type TabType = 'messages' | 'comments' | 'works';

const REASON_MAP: Record<string, string> = {
  spam: '垃圾广告',
  abuse: '辱骂攻击',
  porn: '色情低俗',
  illegal: '违法违规',
  plagiarism: '抄袭剽窃',
  false: '虚假信息',
  harassment: '骚扰',
  inappropriate: '不当内容',
  other: '其他',
};

const STATUS_MAP: Record<string, { label: string; color: string }> = {
  pending: { label: '待处理', color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' },
  reviewed: { label: '已审核', color: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400' },
  dismissed: { label: '已驳回', color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-400' },
  actioned: { label: '已处理', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' },
};

export default function AdminReportsView() {
  const { success, error } = useGlobalStore();
  const [activeTab, setActiveTab] = useState<TabType>('messages');
  const [summary, setSummary] = useState<ReportSummary>({
    messageReports: { total: 0, pending: 0, processedToday: 0 },
    commentReports: { total: 0, pending: 0, processedToday: 0 },
    workReports: { total: 0, pending: 0, processedToday: 0 },
  });
  const [messageReports, setMessageReports] = useState<MessageReport[]>([]);
  const [commentReports, setCommentReports] = useState<CommentReport[]>([]);
  const [workReports, setWorkReports] = useState<WorkReport[]>([]);
  const [loading, setLoading] = useState(false);
  const [processingId, setProcessingId] = useState<string | null>(null);

  // 加载统计数据
  const loadSummary = async () => {
    try {
      const data = await DataService.getReportsSummary();
      setSummary(data);
    } catch (err) {
      console.error('加载统计数据失败:', err);
    }
  };

  // 加载消息举报
  const loadMessageReports = async () => {
    try {
      setLoading(true);
      const data = await DataService.getMessageReports();
      setMessageReports(data);
    } catch (err) {
      console.error('加载消息举报失败:', err);
      error('加载消息举报失败');
    } finally {
      setLoading(false);
    }
  };

  // 加载评论举报
  const loadCommentReports = async () => {
    try {
      setLoading(true);
      const data = await DataService.getCommentReports();
      setCommentReports(data);
    } catch (err) {
      console.error('加载评论举报失败:', err);
      error('加载评论举报失败');
    } finally {
      setLoading(false);
    }
  };

  // 加载小说举报
  const loadWorkReports = async () => {
    try {
      setLoading(true);
      const data = await DataService.getWorkReports();
      setWorkReports(data);
    } catch (err) {
      console.error('加载小说举报失败:', err);
      error('加载小说举报失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSummary();
  }, []);

  useEffect(() => {
    if (activeTab === 'messages') {
      loadMessageReports();
    } else if (activeTab === 'comments') {
      loadCommentReports();
    } else if (activeTab === 'works') {
      loadWorkReports();
    }
  }, [activeTab]);

  // 处理举报
  const handleProcess = async (
    type: TabType,
    reportId: string,
    action: string,
    adminNote?: string
  ) => {
    try {
      setProcessingId(reportId);

      if (type === 'messages') {
        await DataService.processMessageReport(reportId, action, adminNote);
        loadMessageReports();
      } else if (type === 'comments') {
        await DataService.processCommentReport(reportId, action, adminNote);
        loadCommentReports();
      } else if (type === 'works') {
        await DataService.processWorkReport(reportId, action, adminNote);
        loadWorkReports();
      }

      loadSummary();
      success('处理成功');
    } catch (err: any) {
      console.error('处理举报失败:', err);
      error(err.response?.data?.detail || '处理失败');
    } finally {
      setProcessingId(null);
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="px-6 pb-6">
      <div className="sticky top-0 z-10 bg-gray-50 dark:bg-gray-900 pt-6">
        {/* 页头 */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Flag className="w-7 h-7" />
            举报管理
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            处理用户提交的举报，包括消息、评论和小说举报
          </p>
        </div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                <MessageSquare className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <div className="text-sm text-gray-500 dark:text-gray-400">消息举报</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">
                    {summary.messageReports.pending}
                  </span>
                  <span className="text-sm text-gray-500">待处理</span>
                  <span className="text-sm text-gray-400">/ {summary.messageReports.total} 总计</span>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
                <MessageCircle className="w-5 h-5 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <div className="text-sm text-gray-500 dark:text-gray-400">评论举报</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">
                    {summary.commentReports.pending}
                  </span>
                  <span className="text-sm text-gray-500">待处理</span>
                  <span className="text-sm text-gray-400">/ {summary.commentReports.total} 总计</span>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-orange-100 dark:bg-orange-900/30 rounded-lg">
                <Book className="w-5 h-5 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <div className="text-sm text-gray-500 dark:text-gray-400">小说举报</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">
                    {summary.workReports.pending}
                  </span>
                  <span className="text-sm text-gray-500">待处理</span>
                  <span className="text-sm text-gray-400">/ {summary.workReports.total} 总计</span>
                </div>
              </div>
            </div>
          </div>
      </div>

        {/* Tab 切换 */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="flex -mb-px">
            <button
              onClick={() => setActiveTab('messages')}
              className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'messages'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
              }`}
            >
              <MessageSquare className="w-4 h-4 inline-block mr-2" />
              消息举报
              {summary.messageReports.pending > 0 && (
                <span className="ml-2 px-2 py-0.5 text-xs bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400 rounded-full">
                  {summary.messageReports.pending}
                </span>
              )}
            </button>
            <button
              onClick={() => setActiveTab('comments')}
              className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'comments'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
              }`}
            >
              <MessageCircle className="w-4 h-4 inline-block mr-2" />
              评论举报
              {summary.commentReports.pending > 0 && (
                <span className="ml-2 px-2 py-0.5 text-xs bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400 rounded-full">
                  {summary.commentReports.pending}
                </span>
              )}
            </button>
            <button
              onClick={() => setActiveTab('works')}
              className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'works'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
              }`}
            >
              <Book className="w-4 h-4 inline-block mr-2" />
              小说举报
              {summary.workReports.pending > 0 && (
                <span className="ml-2 px-2 py-0.5 text-xs bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400 rounded-full">
                  {summary.workReports.pending}
                </span>
              )}
            </button>
          </nav>
        </div>
      </div>
    </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        {/* 列表内容 */}
        <div className="p-4">
          {loading ? (
            <div className="flex items-center justify-center py-20">
              <div className="text-gray-500 dark:text-gray-400">加载中...</div>
            </div>
          ) : (
            <>
              {/* 消息举报列表 */}
              {activeTab === 'messages' && (
                <div className="space-y-4">
                  {messageReports.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-20">
                      <CheckCircle className="w-12 h-12 text-green-400 mb-4" />
                      <p className="text-gray-500 dark:text-gray-400">暂无消息举报</p>
                    </div>
                  ) : (
                    messageReports.map((report) => (
                      <div
                        key={report.id}
                        className="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <span className={`px-2 py-0.5 rounded text-xs font-medium ${STATUS_MAP[report.status]?.color || STATUS_MAP.pending.color}`}>
                                {STATUS_MAP[report.status]?.label || report.status}
                              </span>
                              <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs text-gray-600 dark:text-gray-400">
                                {REASON_MAP[report.reason] || report.reason}
                              </span>
                              <span className="text-xs text-gray-400 flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {formatDate(report.createdAt)}
                              </span>
                            </div>
                            <div className="text-sm text-gray-900 dark:text-white mb-1">
                              <span className="text-gray-500 dark:text-gray-400">频道：</span>
                              {report.channelName || '未知频道'}
                            </div>
                            <div className="text-sm text-gray-600 dark:text-gray-300 mb-2 bg-gray-50 dark:bg-gray-900/50 p-2 rounded">
                              {report.messageContent || '消息已删除'}
                            </div>
                            <div className="text-xs text-gray-500 dark:text-gray-400">
                              举报人: {report.reporterName || '未知'} | 被举报人: {report.reportedUserName || '未知'}
                            </div>
                            {report.description && (
                              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                描述: {report.description}
                              </div>
                            )}
                          </div>
                          {report.status === 'pending' && (
                            <div className="flex gap-2 ml-4">
                              <button
                                onClick={() => handleProcess('messages', report.id, 'dismiss')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                                title="驳回"
                              >
                                <XCircle className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleProcess('messages', report.id, 'delete')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors"
                                title="删除消息"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleProcess('messages', report.id, 'warn')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-yellow-600 dark:hover:text-yellow-400 hover:bg-yellow-50 dark:hover:bg-yellow-900/20 rounded transition-colors"
                                title="警告用户"
                              >
                                <AlertTriangle className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleProcess('messages', report.id, 'ban')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors"
                                title="禁言用户"
                              >
                                <Ban className="w-4 h-4" />
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* 评论举报列表 */}
              {activeTab === 'comments' && (
                <div className="space-y-4">
                  {commentReports.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-20">
                      <CheckCircle className="w-12 h-12 text-green-400 mb-4" />
                      <p className="text-gray-500 dark:text-gray-400">暂无评论举报</p>
                    </div>
                  ) : (
                    commentReports.map((report) => (
                      <div
                        key={report.id}
                        className="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                                report.isProcessed
                                  ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                                  : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                              }`}>
                                {report.isProcessed ? '已处理' : '待处理'}
                              </span>
                              <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs text-gray-600 dark:text-gray-400">
                                {REASON_MAP[report.reason] || report.reason}
                              </span>
                              <span className="text-xs text-gray-400 flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {formatDate(report.createdAt)}
                              </span>
                            </div>
                            <div className="text-sm text-gray-900 dark:text-white mb-1">
                              <span className="text-gray-500 dark:text-gray-400">小说：</span>
                              {report.workTitle || '未知小说'}
                            </div>
                            <div className="text-sm text-gray-600 dark:text-gray-300 mb-2 bg-gray-50 dark:bg-gray-900/50 p-2 rounded">
                              {report.commentContent || '评论已删除'}
                            </div>
                            <div className="text-xs text-gray-500 dark:text-gray-400">
                              举报人: {report.reporterName || '未知'} | 评论者: {report.commentedUserName || '未知'}
                            </div>
                            {report.description && (
                              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                描述: {report.description}
                              </div>
                            )}
                          </div>
                          {!report.isProcessed && (
                            <div className="flex gap-2 ml-4">
                              <button
                                onClick={() => handleProcess('comments', report.id, 'dismiss')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                                title="驳回"
                              >
                                <XCircle className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleProcess('comments', report.id, 'delete')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors"
                                title="删除评论"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleProcess('comments', report.id, 'warn')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-yellow-600 dark:hover:text-yellow-400 hover:bg-yellow-50 dark:hover:bg-yellow-900/20 rounded transition-colors"
                                title="警告用户"
                              >
                                <AlertTriangle className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleProcess('comments', report.id, 'ban')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors"
                                title="封禁用户"
                              >
                                <Ban className="w-4 h-4" />
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* 小说举报列表 */}
              {activeTab === 'works' && (
                <div className="space-y-4">
                  {workReports.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-20">
                      <CheckCircle className="w-12 h-12 text-green-400 mb-4" />
                      <p className="text-gray-500 dark:text-gray-400">暂无小说举报</p>
                    </div>
                  ) : (
                    workReports.map((report) => (
                      <div
                        key={report.id}
                        className="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <span className={`px-2 py-0.5 rounded text-xs font-medium ${STATUS_MAP[report.status]?.color || STATUS_MAP.pending.color}`}>
                                {STATUS_MAP[report.status]?.label || report.status}
                              </span>
                              <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs text-gray-600 dark:text-gray-400">
                                {REASON_MAP[report.reason] || report.reason}
                              </span>
                              <span className="text-xs text-gray-400 flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {formatDate(report.createdAt)}
                              </span>
                            </div>
                            <div className="text-sm text-gray-900 dark:text-white mb-1">
                              <span className="text-gray-500 dark:text-gray-400">小说：</span>
                              {report.workTitle || '未知小说'}
                            </div>
                            <div className="text-xs text-gray-500 dark:text-gray-400">
                              作者: {report.workAuthorName || '未知'} | 举报人: {report.reporterName || '未知'}
                            </div>
                            {report.description && (
                              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                描述: {report.description}
                              </div>
                            )}
                            {report.actionTaken && (
                              <div className="text-xs text-green-600 dark:text-green-400 mt-1">
                                处理结果: {report.actionTaken}
                              </div>
                            )}
                            {report.adminNote && (
                              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                管理员备注: {report.adminNote}
                              </div>
                            )}
                          </div>
                          {report.status === 'pending' && (
                            <div className="flex gap-2 ml-4">
                              <button
                                onClick={() => handleProcess('works', report.id, 'dismiss')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                                title="驳回"
                              >
                                <XCircle className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleProcess('works', report.id, 'delete')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors"
                                title="下架小说"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleProcess('works', report.id, 'warn')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-yellow-600 dark:hover:text-yellow-400 hover:bg-yellow-50 dark:hover:bg-yellow-900/20 rounded transition-colors"
                                title="警告作者"
                              >
                                <AlertTriangle className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleProcess('works', report.id, 'ban')}
                                disabled={processingId === report.id}
                                className="p-1.5 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors"
                                title="封禁作者"
                              >
                                <Ban className="w-4 h-4" />
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
