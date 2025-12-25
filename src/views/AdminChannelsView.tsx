import { useState, useEffect } from 'react';
import {
  MessageSquare,
  Search,
  Filter,
  MoreVertical,
  Lock,
  Unlock,
  AlertTriangle,
  Users,
  MessageCircle,
  Calendar,
} from 'lucide-react';
import { getMyChannels, type Channel as ApiChannel } from '@/services/channelApi';
import { useToast } from '@/hooks/useToast';

interface Channel extends ApiChannel {
  // 扩展类型以包含所有需要的字段
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
  const [channels, setChannels] = useState<Channel[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('');
  const [filterStatus, setFilterStatus] = useState<string>('');

  // 加载频道列表
  const loadChannels = async () => {
    try {
      setLoading(true);
      const response = await getMyChannels();
      setChannels(response.channels as Channel[]);
    } catch (err) {
      console.error('加载频道列表失败:', err);
      showToast('error', '加载频道列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadChannels();
  }, []);

  // 筛选频道
  const filteredChannels = channels.filter((channel) => {
    if (searchQuery && !channel.name.toLowerCase().includes(searchQuery.toLowerCase())) {
      return false;
    }
    if (filterType && channel.type !== filterType) {
      return false;
    }
    if (filterStatus && channel.status !== filterStatus) {
      return false;
    }
    return true;
  });

  // 处理状态切换
  const handleToggleStatus = async (channelId: string, currentStatus: string) => {
    // TODO: 调用后端 API 更新频道状态
    showToast('info', '状态更新功能待实现');
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
    <div className="h-full flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* 头部 */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">频道管理</h1>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              管理所有频道，包括官方频道、粉丝群和作品频道
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <div className="text-sm text-gray-600 dark:text-gray-300">
              共 <span className="font-semibold text-blue-600">{filteredChannels.length}</span> 个频道
            </div>
          </div>
        </div>
      </div>

      {/* 搜索和筛选栏 */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="flex items-center space-x-4">
          {/* 搜索框 */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="搜索频道名称..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>

          {/* 类型筛选 */}
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          >
            <option value="">所有类型</option>
            <option value="official">官方频道</option>
            <option value="fangroup">粉丝群</option>
            <option value="work">作品频道</option>
          </select>

          {/* 状态筛选 */}
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          >
            <option value="">所有状态</option>
            <option value="active">正常</option>
            <option value="warning">警告</option>
            <option value="locked">已折叠</option>
          </select>
        </div>
      </div>

      {/* 频道列表 */}
      <div className="flex-1 overflow-auto p-6">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-gray-500 dark:text-gray-400">加载中...</div>
          </div>
        ) : filteredChannels.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64">
            <MessageSquare className="w-16 h-16 text-gray-300 dark:text-gray-600 mb-4" />
            <p className="text-gray-500 dark:text-gray-400">没有找到频道</p>
          </div>
        ) : (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-900">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    频道信息
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    类型
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    状态
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    成员数
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    消息数
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    创建时间
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    操作
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {filteredChannels.map((channel) => (
                  <tr key={channel.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                    <td className="px-6 py-4 whitespace-nowrap">
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
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                        {TYPE_MAP[channel.type]}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${STATUS_COLOR_MAP[channel.status]}`}>
                          {STATUS_MAP[channel.status]}
                        </span>
                        {channel.status === 'warning' && channel.warningDays && (
                          <span className="text-xs text-gray-500 dark:text-gray-400">
                            {channel.warningDays}天
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center text-sm text-gray-900 dark:text-gray-100">
                        <Users className="w-4 h-4 mr-1 text-gray-400" />
                        {channel.memberCount}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center text-sm text-gray-900 dark:text-gray-100">
                        <MessageCircle className="w-4 h-4 mr-1 text-gray-400" />
                        {channel.messageCount}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      <div className="flex items-center">
                        <Calendar className="w-4 h-4 mr-1" />
                        {formatDate(channel.createdAt)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex items-center space-x-2">
                        {channel.status === 'locked' ? (
                          <button
                            onClick={() => handleToggleStatus(channel.id, channel.status)}
                            className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300"
                            title="激活频道"
                          >
                            <Unlock className="w-4 h-4" />
                          </button>
                        ) : (
                          <button
                            onClick={() => handleToggleStatus(channel.id, channel.status)}
                            className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300"
                            title="折叠频道"
                          >
                            <Lock className="w-4 h-4" />
                          </button>
                        )}
                        <button
                          className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                          title="更多操作"
                        >
                          <MoreVertical className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
