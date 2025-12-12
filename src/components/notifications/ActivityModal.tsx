import { X, Calendar, MapPin, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { ImageWithFallback } from './ImageWithFallback';
import type { UserNotification } from '../../types/notification';

interface ActivityModalProps {
  notification: UserNotification;
  onClose: () => void;
}

export function ActivityModal({ notification, onClose }: ActivityModalProps) {
  const navigate = useNavigate();

  const formatEventTime = (dateStr: string): string => {
    const date = new Date(dateStr);
    return `${date.getMonth() + 1}月${date.getDate()}日`;
  };

  const handleViewDetails = () => {
    // 假设活动ID就是通知ID，或者从通知中提取
    navigate(`/activities/${notification.id}`);
    onClose();
  };

  const handleClickOutside = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
      onClick={handleClickOutside}
    >
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden animate-in fade-in zoom-in duration-200">
        {/* 关闭按钮 */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-10 p-2 bg-white/90 hover:bg-white rounded-full shadow-lg transition-all"
        >
          <X className="w-5 h-5 text-gray-600" />
        </button>

        {/* 封面图片 */}
        {notification.coverImageUrl && (
          <div className="relative aspect-[21/9] overflow-hidden">
            <ImageWithFallback
              src={notification.coverImageUrl}
              alt={notification.title}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
          </div>
        )}

        {/* 内容区域 */}
        <div className="p-8">
          {/* 标题 */}
          <div className="mb-6">
            <div className="inline-block px-3 py-1 bg-black text-white text-xs rounded-full mb-3">
              {notification.type === 'event' ? '活动通知' : '系统公告'}
            </div>
            <h2 className="text-2xl font-medium text-black mb-2">
              {notification.title}
            </h2>
          </div>

          {/* 活动信息 */}
          {notification.validFrom && notification.validUntil && (
            <div className="flex items-center gap-6 mb-6 pb-6 border-b border-gray-100">
              <div className="flex items-center gap-2 text-gray-600">
                <Calendar className="w-4 h-4" />
                <span className="text-sm">
                  {formatEventTime(notification.validFrom)} - {formatEventTime(notification.validUntil)}
                </span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <MapPin className="w-4 h-4" />
                <span className="text-sm">线上活动</span>
              </div>
            </div>
          )}

          {/* 内容描述 */}
          {notification.content && (
            <div className="mb-6">
              <p className="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">
                {notification.content.split('\n\n')[0]}
              </p>
            </div>
          )}

          {/* 操作按钮 */}
          <div className="flex items-center gap-3">
            <button
              onClick={handleViewDetails}
              className="flex-1 flex items-center justify-center gap-2 bg-black text-white px-6 py-3 rounded-xl text-sm font-medium hover:bg-gray-800 transition-colors"
            >
              <span>查看详情</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={onClose}
              className="px-6 py-3 border border-gray-200 text-gray-600 rounded-xl text-sm font-medium hover:bg-gray-50 transition-colors"
            >
              稍后查看
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
