import { useState, useEffect, useRef } from 'react';
import {
  MessageSquare,
  Search,
  MoreVertical,
  Lock,
  Unlock,
  AlertTriangle,
  Users,
  MessageCircle,
  Calendar,
  Eye,
} from 'lucide-react';
import { DataService } from '@/services/DataService';
import { useToast } from '@/hooks/useToast';
import { ADMIN_STYLES } from '@/styles/adminStyles';

interface AdminChannel {
  id: string;
  name: string;
  description?: string;
  type: string;
  status: string;
  creatorId?: string;
  workId?: string;
  memberCount: number;
  messageCount: number;
  isPermanent: boolean;
  warningDays?: number;
  createdAt: string;
  updatedAt?: string;
  lockedAt?: string;
  bookTitle?: string;
}

const TYPE_MAP: Record<string, string> = {
  official: '官方频道',
  fangroup: '粉丝群',
  work: '作品频道',
};

const STATUS_MAP: Record<string, string> = {
  active: '正常',
  warning: '警告',
  locked: '已折叠',
};

const STATUS_COLOR_MAP: Record<string, string> = {
  active: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
  warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
  locked: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300',
};

export default function AdminChannelsView() {
  const { showToast } = useToast();
  const [channels, setChannels] = useState<AdminChannel[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('');
  const [filterStatus, setFilterStatus] = useState<string>('');
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [openMenu, setOpenMenu] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  // 点击外部关闭菜单
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpenMenu(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // 加载频道列表
  const loadChannels = async () => {
    try {
      setLoading(true);
      const response = await DataService.getAdminChannels({
        channel_type: filterType || undefined,
        channel_status: filterStatus || undefined,
        search: searchQuery || undefined,
      });
      setChannels(response.channels);
      setTotal(response.total);
    } catch (err) {
      console.error('加载频道列表失败:', err);
      showToast('error', '加载频道列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadChannels();
  }, [filterType, filterStatus]);

  // 搜索防抖
  useEffect(() => {
    const timer = setTimeout(() => {
      loadChannels();
    }, 300);
    return () => clearTimeout(timer);
  }, [searchQuery]);

  // 处理状态切换
  const handleToggleStatus = async (channelId: string, currentStatus: string) => {
    const newStatus = currentStatus === 'locked' ? 'active' : 'locked';
    const action = newStatus === 'locked' ? '折叠' : '激活';

    if (!confirm(`确定要${action}该频道吗？`)) {
      return;
    }

    try {
      setActionLoading(channelId);
      await DataService.updateChannelStatus(channelId, newStatus);
      showToast('success', `频道已${action}`);
      await loadChannels();
    } catch (err) {
      const message = err instanceof Error ? err.message : `${action}失败`;
      showToast('error', message);
    } finally {
      setActionLoading(null);
    }
  };

  // 设置警告状态
  const handleSetWarning = async (channelId: string) => {
    if (!confirm('确定要将该频道设为警告状态吗？')) {
      return;
    }

    try {
      setActionLoading(channelId);
      await DataService.updateChannelStatus(channelId, 'warning');
      showToast('success', '频道已设为警告状态');
      setOpenMenu(null);
      await loadChannels();
    } catch (err) {
      const message = err instanceof Error ? err.message : '操作失败';
      showToast('error', message);
    } finally {
      setActionLoading(null);
    }
  };

  // 恢复正常状态
  const handleSetActive = async (channelId: string) => {
    try {
      setActionLoading(channelId);
      await DataService.updateChannelStatus(channelId, 'active');
      showToast('success', '频道已恢复正常');
      setOpenMenu(null);
      await loadChannels();
    } catch (err) {
      const message = err instanceof Error ? err.message : '操作失败';
      showToast('error', message);
    } finally {
      setActionLoading(null);
    }
  };

  // 格式化日期
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    });
  };

  return (
    <div className={ADMIN_STYLES.page}>
      <div className={ADMIN_STYLES.stickyHeader}>
        <div className={ADMIN_STYLES.titleSection}>
          <div className="flex items-center justify-between">
            <div>
              <h1 className={ADMIN_STYLES.title}>
                <MessageSquare className={ADMIN_STYLES.titleIcon} />
                频道管理
              </h1>
              <p className={ADMIN_STYLES.subtitle}>管理所有频道，包括官方频道、粉丝群和作品频道</p>
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-300">
              共 <span className="font-semibold text-blue-600">{total}</span> 个频道
            </div>
          </div>
        </div>

        <div className={ADMIN_STYLES.filterCard}>
          <div className="flex items-center gap-3">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="搜索频道名称..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className={ADMIN_STYLES.searchInput}
              />
            </div>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="w-28 shrink-0 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">所有类型</option>
              <option value="official">官方频道</option>
              <option value="fangroup">粉丝群</option>
              <option value="work">作品频道</option>
            </select>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="w-28 shrink-0 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">所有状态</option>
              <option value="active">正常</option>
              <option value="warning">警告</option>
              <option value="locked">已折叠</option>
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <div className={ADMIN_STYLES.loadingContainer}>
          <div className={ADMIN_STYLES.loadingText}>加载中...</div>
        </div>
      ) : channels.length === 0 ? (
        <div className={ADMIN_STYLES.emptyContainer}>
          <MessageSquare className={ADMIN_STYLES.emptyIcon} />
          <p className={ADMIN_STYLES.emptyText}>没有找到频道</p>
        </div>
      ) : (
        <div className={ADMIN_STYLES.tableContainer}>
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className={ADMIN_STYLES.tableHead}>
              <tr>
                <th className={ADMIN_STYLES.th}>
                  频道信息
                </th>
                <th className={ADMIN_STYLES.th}>
                  类型
                </th>
                <th className={ADMIN_STYLES.th}>
                  状态
                </th>
                <th className={ADMIN_STYLES.th}>
                  成员数
                </th>
                <th className={ADMIN_STYLES.th}>
                  消息数
                </th>
                <th className={ADMIN_STYLES.th}>
                  创建时间
                </th>
                <th className={ADMIN_STYLES.th}>
                  操作
                </th>
              </tr>
            </thead>
            <tbody className={ADMIN_STYLES.tbody}>
              {channels.map((channel) => (
                <tr key={channel.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                  <td className="px-4 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                        <MessageSquare className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {channel.name}
                        </div>
                        {channel.description && (
                          <div className="text-sm text-gray-500 dark:text-gray-400 truncate max-w-xs">
                            {channel.description}
                          </div>
                        )}
                        {channel.type === 'work' && channel.bookTitle && (
                          <div className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                            作品：{channel.bookTitle}
                          </div>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                      {TYPE_MAP[channel.type] || channel.type}
                    </span>
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded ${STATUS_COLOR_MAP[channel.status] || STATUS_COLOR_MAP.active}`}>
                        {STATUS_MAP[channel.status] || channel.status}
                      </span>
                      {channel.status === 'warning' && channel.warningDays && (
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          {channel.warningDays}天
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap">
                    <div className="flex items-center text-sm text-gray-900 dark:text-gray-100">
                      <Users className="w-4 h-4 mr-1 text-gray-400" />
                      {channel.memberCount ?? 0}
                    </div>
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap">
                    <div className="flex items-center text-sm text-gray-900 dark:text-gray-100">
                      <MessageCircle className="w-4 h-4 mr-1 text-gray-400" />
                      {channel.messageCount ?? 0}
                    </div>
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    <div className="flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {channel.createdAt ? formatDate(channel.createdAt) : '-'}
                    </div>
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex items-center space-x-2">
                      {channel.status === 'locked' ? (
                        <button
                          onClick={() => handleToggleStatus(channel.id, channel.status)}
                          disabled={actionLoading === channel.id}
                          className="p-1.5 text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors disabled:opacity-50"
                          title="激活频道"
                        >
                          <Unlock className="w-4 h-4" />
                        </button>
                      ) : (
                        <button
                          onClick={() => handleToggleStatus(channel.id, channel.status)}
                          disabled={actionLoading === channel.id}
                          className="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors disabled:opacity-50"
                          title="折叠频道"
                        >
                          <Lock className="w-4 h-4" />
                        </button>
                      )}

                      {/* 更多操作下拉菜单 */}
                      <div className="relative" ref={openMenu === channel.id ? menuRef : null}>
                        <button
                          onClick={() => setOpenMenu(openMenu === channel.id ? null : channel.id)}
                          className="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                          title="更多操作"
                        >
                          <MoreVertical className="w-4 h-4" />
                        </button>

                        {openMenu === channel.id && (
                          <div className="absolute right-0 mt-2 w-40 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-10">
                            {channel.status !== 'warning' && channel.status !== 'locked' && (
                              <button
                                onClick={() => handleSetWarning(channel.id)}
                                disabled={actionLoading === channel.id}
                                className="w-full flex items-center px-4 py-2 text-sm text-yellow-600 dark:text-yellow-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50"
                              >
                                <AlertTriangle className="w-4 h-4 mr-2" />
                                设为警告
                              </button>
                            )}
                            {channel.status === 'warning' && (
                              <button
                                onClick={() => handleSetActive(channel.id)}
                                disabled={actionLoading === channel.id}
                                className="w-full flex items-center px-4 py-2 text-sm text-green-600 dark:text-green-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50"
                              >
                                <Eye className="w-4 h-4 mr-2" />
                                恢复正常
                              </button>
                            )}
                            {channel.status === 'locked' && (
                              <button
                                onClick={() => handleSetActive(channel.id)}
                                disabled={actionLoading === channel.id}
                                className="w-full flex items-center px-4 py-2 text-sm text-green-600 dark:text-green-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50"
                              >
                                <Unlock className="w-4 h-4 mr-2" />
                                解除折叠
                              </button>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
