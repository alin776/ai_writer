import { Calendar, MapPin, ArrowRight, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { ImageWithFallback } from './ImageWithFallback';

interface Activity {
  id: string;  // 修改为 string 以匹配通知ID类型
  title: string;
  description: string;
  startTime: string;
  endTime: string;
  image: string;
  category: string;
}

interface CompactActivityProps {
  activity: Activity;
}

export function CompactActivity({ activity }: CompactActivityProps) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/activities/${activity.id}`);
  };

  return (
    <div
      onClick={handleClick}
      className="group border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden hover:shadow-md dark:hover:shadow-lg dark:hover:shadow-black/20 transition-all duration-300 bg-white dark:bg-gray-800 cursor-pointer"
    >
      {/* Image */}
      <div className="relative overflow-hidden aspect-video">
        <ImageWithFallback
          src={activity.image}
          alt={activity.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <div className="absolute top-3 left-3">
          <span className="bg-black dark:bg-white text-white dark:text-gray-900 px-3 py-1 rounded-full text-xs">
            {activity.category}
          </span>
        </div>
        <div className="absolute top-3 right-3">
          <div className="w-7 h-7 bg-white dark:bg-gray-800 rounded-full flex items-center justify-center shadow-sm">
            <Sparkles className="w-3.5 h-3.5 text-gray-600 dark:text-gray-400" />
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-4 group-hover:text-gray-600 dark:group-hover:text-gray-300 transition-colors line-clamp-1">
          {activity.title}
        </h3>

        <div className="flex items-center justify-between text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-1.5">
            <Calendar className="w-3 h-3" />
            <span className="text-xs">{activity.startTime} - {activity.endTime}</span>
          </div>
          <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
        </div>
      </div>
    </div>
  );
}
