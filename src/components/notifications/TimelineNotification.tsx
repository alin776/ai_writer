import { Info, Zap, Calendar, Circle } from 'lucide-react';

interface Notification {
  id: number;
  title: string;
  content: string;
  time: string;
  type: 'info' | 'update' | 'event';
  read: boolean;
}

interface TimelineNotificationProps {
  notification: Notification;
  isLast: boolean;
  batchDeleteMode?: boolean;
  isSelected?: boolean;
  onToggleSelect?: () => void;
  onMarkAsRead?: () => void;
}

export function TimelineNotification({
  notification,
  isLast,
  batchDeleteMode = false,
  isSelected = false,
  onToggleSelect,
  onMarkAsRead
}: TimelineNotificationProps) {
  const getIcon = () => {
    switch (notification.type) {
      case 'update':
        return <Zap className="w-4 h-4" />;
      case 'event':
        return <Calendar className="w-4 h-4" />;
      default:
        return <Info className="w-4 h-4" />;
    }
  };

  return (
    <div className={`group relative ${batchDeleteMode ? 'pl-20' : 'pl-12'} ${!isLast ? 'pb-8' : 'pb-0'} transition-all`}>
      {/* Checkbox - Only show in batch delete mode */}
      {batchDeleteMode && (
        <div className="absolute left-0 top-2">
          <button
            onClick={onToggleSelect}
            style={{ border: isSelected ? '2px solid currentColor' : '2px solid rgb(209, 213, 219)' }}
            className={`w-5 h-5 rounded transition-all flex items-center justify-center ${
              isSelected
                ? 'bg-black dark:bg-white text-white dark:text-gray-900 border-black dark:border-white'
                : 'bg-white dark:bg-gray-800 hover:border-black dark:hover:border-gray-400 border-gray-300 dark:border-gray-600'
            }`}
          >
            {isSelected && (
              <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>
        </div>
      )}

      {/* Timeline Dot */}
      <div className={`absolute ${batchDeleteMode ? 'left-12' : 'left-4'} top-2 -translate-x-1/2 transition-all`}>
        <div className={`w-3 h-3 rounded-full border-2 border-white dark:border-gray-900 transition-colors ${
          !notification.read ? 'bg-black dark:bg-white' : 'bg-gray-300 dark:bg-gray-600'
        } group-hover:bg-black dark:group-hover:bg-white`} />
      </div>

      {/* Content */}
      <div className="space-y-1">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-2 text-gray-700 dark:text-gray-300">
            {getIcon()}
            <h3 className="text-xs font-medium group-hover:text-gray-600 dark:group-hover:text-gray-200 transition-colors">
              {notification.title}
            </h3>
            {!notification.read && (
              <Circle className="w-1.5 h-1.5 fill-black dark:fill-white flex-shrink-0" />
            )}
          </div>
          <span className="text-xs text-gray-400 dark:text-gray-500 whitespace-nowrap">{notification.time}</span>
        </div>

        <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed pr-4 whitespace-pre-line">
          {notification.content}
        </p>

        {!batchDeleteMode && !notification.read && onMarkAsRead && (
          <button
            onClick={onMarkAsRead}
            className="text-xs text-gray-400 dark:text-gray-500 hover:text-black dark:hover:text-white transition-colors opacity-0 group-hover:opacity-100"
          >
            标记已读
          </button>
        )}
      </div>
    </div>
  );
}
