import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { TimelineNotification } from '../components/notifications/TimelineNotification';
import { InteractionNotificationItem } from '../components/notifications/InteractionNotificationItem';
import { FeaturedActivity } from '../components/notifications/FeaturedActivity';
import { CompactActivity } from '../components/notifications/CompactActivity';
import { Bell, Sparkles, Check, Trash2, X, CheckSquare, MessageCircle } from 'lucide-react';
import { ImageWithFallback } from '../components/notifications/ImageWithFallback';
import { getUserNotifications, markNotificationsAsRead, dismissNotification } from '../services/notificationApi';
import { NotificationType, type UserNotification } from '../types/notification';
import { useNotificationStore } from '../store/notificationStore';

interface Activity {
  id: string;  // 修改为 string 以匹配通知ID类型
  title: string;
  description: string;
  startTime: string;
  endTime: string;
  image: string;
  category: string;
  featured?: boolean;
  notification?: UserNotification;
}

export default function NotificationCenter() {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<'notifications' | 'activities' | 'interactions'>('activities');
  const [notifications, setNotifications] = useState<UserNotification[]>([]);
  const [interactions, setInteractions] = useState<UserNotification[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  const [batchDeleteMode, setBatchDeleteMode] = useState(false);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  const { fetchUnreadCount } = useNotificationStore();
  const unreadCount = notifications.filter(n => !n.isRead).length;
  const interactionUnreadCount = interactions.filter(n => !n.isRead).length;

  // 从后端加载通知和活动
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const response = await getUserNotifications({
        page: 1,
        pageSize: 100
      });

      const allNotifications = response.items;
      const eventNotifications = allNotifications.filter(n => n.type === NotificationType.EVENT);
      // 互动通知：评论回复和作品被收藏
      const interactionNotifications = allNotifications.filter(n =>
        n.type === NotificationType.COMMENT_REPLY || n.type === NotificationType.WORK_FAVORITED
      );
      // 普通通知：排除活动和互动
      const regularNotifications = allNotifications.filter(n =>
        n.type !== NotificationType.EVENT &&
        n.type !== NotificationType.COMMENT_REPLY &&
        n.type !== NotificationType.WORK_FAVORITED
      );

      setNotifications(regularNotifications);
      setInteractions(interactionNotifications);

      const convertedActivities: Activity[] = eventNotifications.map((n, index) => {
        // 只显示第一段作为简短描述，或截取前100个字符
        const shortDescription = n.content
          ? n.content.split('\n\n')[0].substring(0, 100) + (n.content.length > 100 ? '...' : '')
          : '';

        return {
          id: n.id,  // 使用通知的真实ID而不是索引
          title: n.title,
          description: shortDescription,
          startTime: formatEventTime(n.validFrom || n.createdAt),
          endTime: formatEventTime(n.validUntil || n.createdAt),
          image: n.coverImageUrl || getDefaultActivityImage(index),
          category: getActivityCategory(n),
          featured: index === 0,
          notification: n
        };
      });

      setActivities(convertedActivities);
    } catch (error) {
      console.error('加载通知失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatEventTime = (dateStr: string): string => {
    // 统一使用 new Date() 解析，它会自动处理时区
    // 如果字符串带时区标记（如 Z），会转换为本地时间
    // 如果不带时区标记，会按本地时间解析
    const date = new Date(dateStr);
    return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;
  };

  const getActivityCategory = (notification: UserNotification): string => {
    if (notification.title.includes('工作坊') || notification.title.toLowerCase().includes('workshop')) return t('notifications.category.workshop');
    if (notification.title.includes('大会') || notification.title.toLowerCase().includes('conference')) return t('notifications.category.conference');
    return t('notifications.category.event');
  };

  const getDefaultActivityImage = (index: number): string => {
    const images = [
      'https://images.unsplash.com/photo-1627860572942-27bc789d94bf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtaW5pbWFsJTIwYWJzdHJhY3QlMjBhcnR8ZW58MXx8fHwxNzY1MTYwMzgyfDA&ixlib=rb-4.1.0&q=80&w=1080',
      'https://images.unsplash.com/photo-1758973602156-1e3d6473b87d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzaW1wbGUlMjBsaW5lJTIwZHJhd2luZyUyMGlsbHVzdHJhdGlvbnxlbnwxfHx8fDE3NjUxNzk5MDl8MA&ixlib=rb-4.1.0&q=80&w=1080',
      'https://images.unsplash.com/photo-1651761292876-fcf8b98db945?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtaW5pbWFsaXN0JTIwZ2VvbWV0cmljJTIwYXJ0fGVufDF8fHx8MTc2NTE3OTkwOXww&ixlib=rb-4.1.0&q=80&w=1080',
    ];
    return images[index % images.length];
  };

  const convertToTimelineFormat = (n: UserNotification): any => {
    const getIconType = () => {
      if (n.type === NotificationType.FEATURE) return 'update';
      if (n.type === NotificationType.EVENT) return 'event';
      if (n.type === NotificationType.COMMENT_REPLY) return 'comment';
      if (n.type === NotificationType.WORK_FAVORITED) return 'favorite';
      return 'info';
    };

    return {
      id: n.id,
      title: n.title,
      content: n.content || '',
      time: formatRelativeTime(n.createdAt),
      type: getIconType(),
      read: n.isRead
    };
  };

  const formatRelativeTime = (dateStr: string): string => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffHours < 1) return t('notifications.time.justNow');
    if (diffHours < 24) return t('notifications.time.hoursAgo', { n: diffHours });
    if (diffDays < 7) return t('notifications.time.daysAgo', { n: diffDays });
    return t('notifications.time.weeksAgo', { n: Math.floor(diffDays / 7) });
  };

  const toggleBatchMode = () => {
    setBatchDeleteMode(!batchDeleteMode);
    setSelectedIds([]);
  };

  const toggleSelection = (id: string) => {
    setSelectedIds(prev =>
      prev.includes(id)
        ? prev.filter(i => i !== id)
        : [...prev, id]
    );
  };

  const selectAll = () => {
    if (selectedIds.length === notifications.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(notifications.map(n => n.id));
    }
  };

  const deleteSelected = async () => {
    try {
      // 批量调用 dismiss API
      await Promise.all(
        selectedIds.map(id => dismissNotification(id))
      );

      // 更新本地状态，移除已删除的通知
      setNotifications(prev => prev.filter(n => !selectedIds.includes(n.id)));
      setSelectedIds([]);
      setBatchDeleteMode(false);
    } catch (error) {
      console.error('删除通知失败:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      await markNotificationsAsRead();
      setNotifications(prev => prev.map(n => ({ ...n, isRead: true })));
      // 同步更新侧边栏的未读数量
      fetchUnreadCount();
    } catch (error) {
      console.error('标记已读失败:', error);
    }
  };

  const markSingleAsRead = async (notificationId: string) => {
    try {
      await markNotificationsAsRead([notificationId]);
      setNotifications(prev => prev.map(n =>
        n.id === notificationId ? { ...n, isRead: true } : n
      ));
      // 同步更新侧边栏的未读数量
      fetchUnreadCount();
    } catch (error) {
      console.error('标记已读失败:', error);
    }
  };

  if (loading) {
    return (
      <div className="h-full bg-white dark:bg-gray-900 flex items-center justify-center">
        <div className="text-gray-500 dark:text-gray-400">{t('notifications.loading')}</div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-white dark:bg-gray-900 overflow-hidden">
      <div className="flex-1 max-w-7xl mx-auto px-8 py-8 w-full overflow-hidden">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 h-full">
          <div className="lg:col-span-3 flex flex-col overflow-hidden">
            <div className="flex justify-between items-center gap-8 mb-8 border-b border-gray-100 dark:border-gray-700 flex-shrink-0">
              <div className="flex gap-8">
                <button
                  onClick={() => setActiveTab('activities')}
                  className={`pb-3 px-2 transition-all relative text-sm ${
                    activeTab === 'activities'
                      ? 'text-black dark:text-white'
                      : 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4" />
                    <span>{t('notifications.activities')}</span>
                  </div>
                  {activeTab === 'activities' && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-black dark:bg-white" />
                  )}
                </button>
                <button
                  onClick={() => setActiveTab('notifications')}
                  className={`pb-3 px-2 transition-all relative text-sm ${
                    activeTab === 'notifications'
                      ? 'text-black dark:text-white'
                      : 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <Bell className="w-4 h-4" />
                    <span>{t('notifications.title')}</span>
                    {unreadCount > 0 && (
                      <span className="bg-black dark:bg-white text-white dark:text-gray-900 rounded-full w-4 h-4 flex items-center justify-center text-xs">
                        {unreadCount}
                      </span>
                    )}
                  </div>
                  {activeTab === 'notifications' && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-black dark:bg-white" />
                  )}
                </button>
                <button
                  onClick={() => setActiveTab('interactions')}
                  className={`pb-3 px-2 transition-all relative text-sm ${
                    activeTab === 'interactions'
                      ? 'text-black dark:text-white'
                      : 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <MessageCircle className="w-4 h-4" />
                    <span>{t('notifications.interactions')}</span>
                    {interactionUnreadCount > 0 && (
                      <span className="bg-black dark:bg-white text-white dark:text-gray-900 rounded-full w-4 h-4 flex items-center justify-center text-xs">
                        {interactionUnreadCount}
                      </span>
                    )}
                  </div>
                  {activeTab === 'interactions' && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-black dark:bg-white" />
                  )}
                </button>
              </div>

              {activeTab === 'notifications' && (
                <div className="flex items-center gap-2 pb-3">
                  {!batchDeleteMode ? (
                    <>
                      <button
                        onClick={markAllAsRead}
                        className="px-3 py-1.5 text-xs text-gray-600 dark:text-gray-400 hover:text-black dark:hover:text-white border border-gray-200 dark:border-gray-600 rounded-full hover:border-gray-300 dark:hover:border-gray-500 transition-all flex items-center gap-1.5"
                      >
                        <Check className="w-3.5 h-3.5" />
                        {t('notifications.markAllRead')}
                      </button>
                      <button
                        onClick={toggleBatchMode}
                        className="px-3 py-1.5 text-xs text-gray-600 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 border border-gray-200 dark:border-gray-600 rounded-full hover:border-red-300 dark:hover:border-red-500 transition-all flex items-center gap-1.5"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                        {t('notifications.batchDelete')}
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        onClick={selectAll}
                        className="px-3 py-1.5 text-xs text-gray-600 dark:text-gray-400 hover:text-black dark:hover:text-white border border-gray-200 dark:border-gray-600 rounded-full hover:border-gray-300 dark:hover:border-gray-500 transition-all flex items-center gap-1.5"
                      >
                        <CheckSquare className="w-3.5 h-3.5" />
                        {selectedIds.length === notifications.length ? t('notifications.deselectAll') : t('notifications.selectAll')}
                      </button>
                      {selectedIds.length > 0 && (
                        <span className="text-xs text-gray-500 dark:text-gray-400 px-2">
                          {t('notifications.selectedCount', { count: selectedIds.length })}
                        </span>
                      )}
                      <button
                        onClick={deleteSelected}
                        disabled={selectedIds.length === 0}
                        className="px-3 py-1.5 text-xs text-white bg-red-600 hover:bg-red-700 disabled:bg-gray-300 dark:disabled:bg-gray-600 disabled:cursor-not-allowed rounded-full transition-all flex items-center gap-1.5"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                        {t('notifications.deleteSelected')}
                      </button>
                      <button
                        onClick={toggleBatchMode}
                        className="px-3 py-1.5 text-xs text-gray-600 dark:text-gray-400 hover:text-black dark:hover:text-white border border-gray-200 dark:border-gray-600 rounded-full hover:border-gray-300 dark:hover:border-gray-500 transition-all flex items-center gap-1.5"
                      >
                        <X className="w-3.5 h-3.5" />
                        {t('notifications.cancel')}
                      </button>
                    </>
                  )}
                </div>
              )}
            </div>

            <div className="overflow-y-auto pr-4 scrollbar-auto-hide">
              {activeTab === 'notifications' && (
                <div className="relative">
                  <div className={`absolute ${batchDeleteMode ? 'left-12' : 'left-4'} top-0 bottom-0 w-px bg-gray-200 dark:bg-gray-700 transition-all`} />
                  <div className="space-y-0">
                    {notifications.length === 0 ? (
                      <div className="flex flex-col items-center justify-center py-12">
                        <Bell className="w-12 h-12 text-gray-300 dark:text-gray-600 mb-3" />
                        <p className="text-sm text-gray-500 dark:text-gray-400">{t('notifications.empty')}</p>
                      </div>
                    ) : (
                      notifications.map((notification, index) => (
                        <TimelineNotification
                          key={notification.id}
                          notification={convertToTimelineFormat(notification)}
                          isLast={index === notifications.length - 1}
                          batchDeleteMode={batchDeleteMode}
                          isSelected={selectedIds.includes(notification.id)}
                          onToggleSelect={() => toggleSelection(notification.id)}
                          onMarkAsRead={() => markSingleAsRead(notification.id)}
                        />
                      ))
                    )}
                  </div>
                </div>
              )}

              {activeTab === 'interactions' && (
                <div className="space-y-0">
                  {interactions.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-12">
                      <MessageCircle className="w-12 h-12 text-gray-300 dark:text-gray-600 mb-3" />
                      <p className="text-sm text-gray-500 dark:text-gray-400">{t('notifications.emptyInteractions')}</p>
                    </div>
                  ) : (
                    interactions.map((notification) => (
                      <InteractionNotificationItem
                        key={notification.id}
                        notification={notification}
                        onReplySuccess={() => loadData()}
                      />
                    ))
                  )}
                </div>
              )}

              {activeTab === 'activities' && (
                <div className="space-y-6">
                  {activities.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-12">
                      <Sparkles className="w-12 h-12 text-gray-300 dark:text-gray-600 mb-3" />
                      <p className="text-sm text-gray-500 dark:text-gray-400">{t('notifications.emptyActivities')}</p>
                    </div>
                  ) : (
                    <>
                      {/* Featured activity */}
                      {activities.filter(a => a.featured).map(activity => (
                        <FeaturedActivity key={activity.id} activity={activity} />
                      ))}

                      {/* Compact activities in grid */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {activities.filter(a => !a.featured).map(activity => (
                          <CompactActivity key={activity.id} activity={activity} />
                        ))}
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>

          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-6">
              <div className="border-l-4 border-black dark:border-gray-400 pl-4 py-2">
                <p className="text-sm text-gray-600 dark:text-gray-400 italic mb-1">
                  {t('notifications.sidebar.quote')}
                </p>
                <span className="text-xs text-gray-400 dark:text-gray-500">{t('notifications.sidebar.quoteAuthor')}</span>
              </div>

              <div className="bg-black dark:bg-gray-800 text-white rounded-3xl p-6">
                <h3 className="text-base font-medium mb-4 text-white">{t('notifications.sidebar.monthlyStats')}</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between pb-3 border-b border-gray-700 dark:border-gray-600">
                    <span className="text-sm text-gray-300 dark:text-gray-400">{t('notifications.sidebar.unreadNotifications')}</span>
                    <span className="text-xl font-medium">{unreadCount}</span>
                  </div>
                  <div className="flex items-center justify-between pb-3 border-b border-gray-700 dark:border-gray-600">
                    <span className="text-sm text-gray-300 dark:text-gray-400">{t('notifications.sidebar.upcomingActivities')}</span>
                    <span className="text-xl font-medium">{activities.length}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-300 dark:text-gray-400">{t('notifications.sidebar.participatedActivities')}</span>
                    <span className="text-xl font-medium">{activities.filter(a => a.notification?.isRead).length}</span>
                  </div>
                </div>
              </div>

              <div className="relative rounded-3xl overflow-hidden border border-gray-100 dark:border-gray-700 aspect-[4/3]">
                <ImageWithFallback
                  src="https://images.unsplash.com/photo-1627860572942-27bc789d94bf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtaW5pbWFsJTIwYWJzdHJhY3QlMjBhcnR8ZW58MXx8fHwxNzY1MTYwMzgyfDA&ixlib=rb-4.1.0&q=80&w=1080"
                  alt="艺术插画"
                  className="absolute inset-0 w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/70" />
                <div className="relative h-full p-6 flex flex-col justify-between">
                  <div>
                    <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center mb-3">
                      <Sparkles className="w-5 h-5 text-black" />
                    </div>
                  </div>
                  <div>
                    <h3 className="text-base font-medium mb-2 text-white">{t('notifications.sidebar.stayInspired')}</h3>
                    <p className="text-sm text-white/80">
                      {t('notifications.sidebar.stayInspiredDesc')}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
