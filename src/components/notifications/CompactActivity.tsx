import { Calendar, MapPin, ArrowRight } from 'lucide-react';
import { ImageWithFallback } from './ImageWithFallback';

interface Activity {
  id: number;
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
  return (
    <div className="group border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden hover:shadow-md dark:hover:shadow-lg dark:hover:shadow-black/20 transition-all duration-300 bg-white dark:bg-gray-800">
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
            <span className="text-xs text-gray-600 dark:text-gray-400">{activity.id}</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2 group-hover:text-gray-600 dark:group-hover:text-gray-300 transition-colors line-clamp-1">
          {activity.title}
        </h3>
        <p className="text-xs text-gray-600 dark:text-gray-400 mb-4 line-clamp-2 leading-relaxed">
          {activity.description}
        </p>

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
