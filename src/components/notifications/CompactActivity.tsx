import { Calendar, MapPin, ArrowRight } from 'lucide-react';
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
      className="group border border-gray-100 rounded-2xl overflow-hidden hover:shadow-md transition-all duration-300 bg-white cursor-pointer"
    >
      {/* Image */}
      <div className="relative overflow-hidden aspect-video">
        <ImageWithFallback
          src={activity.image}
          alt={activity.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <div className="absolute top-3 left-3">
          <span className="bg-black text-white px-3 py-1 rounded-full text-xs">
            {activity.category}
          </span>
        </div>
        <div className="absolute top-3 right-3">
          <div className="w-7 h-7 bg-white rounded-full flex items-center justify-center shadow-sm">
            <span className="text-xs text-gray-600">{activity.id}</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="text-sm font-medium mb-4 group-hover:text-gray-600 transition-colors line-clamp-1">
          {activity.title}
        </h3>

        <div className="flex items-center justify-between text-gray-500">
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
