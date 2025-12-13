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
  featured?: boolean;
}

interface FeaturedActivityProps {
  activity: Activity;
}

export function FeaturedActivity({ activity }: FeaturedActivityProps) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/activities/${activity.id}`);
  };

  return (
    <div
      onClick={handleClick}
      className="group relative overflow-hidden rounded-3xl bg-black dark:bg-gray-800 text-white h-96 cursor-pointer"
    >
      {/* Background Image */}
      <div className="absolute inset-0 opacity-50">
        <ImageWithFallback
          src={activity.image}
          alt={activity.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
        />
      </div>

      {/* Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent" />

      {/* Content */}
      <div className="relative h-full flex flex-col justify-between p-8">
        <div className="flex items-start justify-between">
          <span className="bg-white text-black px-3 py-1 rounded-full text-xs font-medium">
            {activity.category}
          </span>
          <div className="w-8 h-8 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center group-hover:bg-white/30 transition-colors">
            <span className="text-xs">{activity.id}</span>
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-medium mb-6 text-white">
            {activity.title}
          </h2>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-2 text-gray-300">
                <Calendar className="w-4 h-4" />
                <span className="text-sm">{activity.startTime} - {activity.endTime}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-300">
                <MapPin className="w-4 h-4" />
                <span className="text-sm">线上活动</span>
              </div>
            </div>

            <button className="flex items-center gap-2 bg-white text-black px-5 py-2 rounded-full text-sm hover:gap-3 transition-all">
              <span>了解详情</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
