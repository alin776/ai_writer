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
}

export function TimelineNotification({
  notification,
  isLast,
  batchDeleteMode = false,
  isSelected = false,
  onToggleSelect
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
            style={{ border: isSelected ? '2px solid black' : '2px solid rgb(209, 213, 219)' }}
            className={`w-5 h-5 rounded transition-all flex items-center justify-center ${
              isSelected
                ? 'bg-black'
                : 'bg-white hover:border-black'
            }`}
          >
            {isSelected && (
              <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>
        </div>
      )}

      {/* Timeline Dot */}
      <div className={`absolute ${batchDeleteMode ? 'left-12' : 'left-4'} top-2 -translate-x-1/2 transition-all`}>
        <div className={`w-3 h-3 rounded-full border-2 border-white transition-colors ${
          !notification.read ? 'bg-black' : 'bg-gray-300'
        } group-hover:bg-black`} />
      </div>

      {/* Content */}
      <div className="space-y-1">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-2">
            {getIcon()}
            <h3 className="text-xs font-medium group-hover:text-gray-600 transition-colors">
              {notification.title}
            </h3>
            {!notification.read && (
              <Circle className="w-1.5 h-1.5 fill-black flex-shrink-0" />
            )}
          </div>
          <span className="text-xs text-gray-400 whitespace-nowrap">{notification.time}</span>
        </div>

        <p className="text-xs text-gray-600 leading-relaxed pr-4">
          {notification.content}
        </p>

        {!batchDeleteMode && (
          <button className="text-xs text-gray-400 hover:text-black transition-colors opacity-0 group-hover:opacity-100">
            标记已读
          </button>
        )}
      </div>
    </div>
  );
}
