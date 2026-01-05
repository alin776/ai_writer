import React, { useState, useEffect } from 'react';
import { X, Megaphone } from 'lucide-react';
import { getChannelAnnouncements } from '../../../services/channelApi';
import type { ChannelMessage } from '../../../types';

interface AnnouncementListDialogProps {
  channelId: string;
  channelName: string;
  onClose: () => void;
}

export const AnnouncementListDialog: React.FC<AnnouncementListDialogProps> = ({
  channelId,
  channelName,
  onClose,
}) => {
  const [announcements, setAnnouncements] = useState<ChannelMessage[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadAnnouncements();
  }, [channelId]);

  const loadAnnouncements = async () => {
    setLoading(true);
    try {
      const response = await getChannelAnnouncements(channelId, {
        skip: 0,
        limit: 100 // 获取所有公告
      });
      setAnnouncements(response.messages);
    } catch (error) {
      console.error('Failed to load announcements:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return '刚刚';
    if (diffMins < 60) return `${diffMins}分钟前`;
    if (diffHours < 24) return `${diffHours}小时前`;
    if (diffDays < 7) return `${diffDays}天前`;

    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-zinc-900 rounded-lg shadow-xl max-w-3xl w-full max-h-[80vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-zinc-800">
          <div className="flex items-center gap-2">
            <Megaphone className="w-5 h-5 text-orange-500" />
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              {channelName} - 公告列表
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-zinc-800 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-gray-500 dark:text-gray-400">加载中...</div>
            </div>
          ) : announcements.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-gray-500 dark:text-gray-400">
              <Megaphone className="w-12 h-12 mb-3 opacity-30" />
              <p>暂无公告</p>
            </div>
          ) : (
            <div className="space-y-4">
              {announcements.map((announcement) => (
                <div
                  key={announcement.id}
                  className="bg-orange-50 dark:bg-orange-900/10 border border-orange-200 dark:border-orange-800/30 rounded-lg p-4"
                >
                  {/* Author and Time */}
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {announcement.userAvatar ? (
                        <img
                          src={announcement.userAvatar}
                          alt={announcement.userName}
                          className="w-6 h-6 rounded-full"
                        />
                      ) : (
                        <div className="w-6 h-6 rounded-full bg-orange-200 dark:bg-orange-800 flex items-center justify-center">
                          <span className="text-xs font-medium text-orange-700 dark:text-orange-300">
                            {announcement.userName?.charAt(0) || '?'}
                          </span>
                        </div>
                      )}
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {announcement.userName}
                        </span>
                        {announcement.userHonor && (
                          <span className="text-xs px-1.5 py-0.5 rounded bg-gradient-to-r from-yellow-400 to-orange-500 text-white font-medium">
                            {announcement.userHonor}
                          </span>
                        )}
                        {announcement.userTitle && (
                          <span
                            className="text-xs px-1.5 py-0.5 rounded font-medium"
                            style={{
                              backgroundColor: announcement.userTitleColor
                                ? `${announcement.userTitleColor}20`
                                : '#e5e7eb',
                              color: announcement.userTitleColor || '#6b7280'
                            }}
                          >
                            {announcement.userTitle}
                          </span>
                        )}
                      </div>
                    </div>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {formatDate(announcement.createdAt)}
                    </span>
                  </div>

                  {/* Content */}
                  <div className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap break-words">
                    {announcement.content}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 dark:border-zinc-800 p-4">
          <button
            onClick={onClose}
            className="w-full px-4 py-2 bg-gray-100 dark:bg-zinc-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-zinc-700 transition-colors"
          >
            关闭
          </button>
        </div>
      </div>
    </div>
  );
};
