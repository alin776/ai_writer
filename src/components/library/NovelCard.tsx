import { Eye, Heart, Star } from 'lucide-react';
import { ImageWithFallback } from './ImageWithFallback';

export interface Novel {
  id: string;
  title: string;
  author: string;
  authorId?: string;
  authorAvatar?: string;
  category: string;
  description: string;
  cover: string;
  views: number;
  likes: number;
  rating: number;
  chapters: number;
  status: '连载中' | '已完结' | '其他';
  isFeatured?: boolean;
}

interface NovelCardProps {
  novel: Novel;
  onViewDetail?: () => void;
}

export function NovelCard({ novel, onViewDetail }: NovelCardProps) {
  return (
    <div
      className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 hover:border-gray-300 dark:hover:border-slate-600 transition-all duration-200 cursor-pointer overflow-hidden flex flex-col h-[360px]"
      onClick={onViewDetail}
    >
      <div className="relative">
        <ImageWithFallback
          src={novel.cover}
          alt={novel.title}
          className="w-full rounded-lg"
          style={{ height: '220px', objectFit: 'cover', objectPosition: 'center' }}
        />
        {/* 左上角评分 */}
        {novel.rating > 0 && (
          <div className="absolute top-2 left-2 flex items-center gap-0.5 px-1.5 py-0.5 bg-yellow-500 text-white text-xs rounded">
            <Star className="w-3 h-3 fill-white" />
            <span className="font-semibold">{novel.rating.toFixed(1)}</span>
          </div>
        )}
        {/* 右上角状态 */}
        <div className="absolute top-2 right-2">
          <span
            className={`px-1.5 py-0.5 text-white text-xs rounded ${
              novel.status === '连载中' ? 'bg-green-600' : 'bg-blue-600'
            }`}
          >
            {novel.status}
          </span>
        </div>
      </div>

      <div className="p-2 flex flex-col flex-1">
        <h3 className="text-sm mb-1 line-clamp-1 text-gray-900 dark:text-white">{novel.title}</h3>

        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-slate-400 mb-2">
          <span className="line-clamp-1">{novel.author}</span>
        </div>

        <p className="text-xs text-gray-600 dark:text-slate-400 line-clamp-2 mb-2">{novel.description}</p>

        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-slate-400 pt-2 border-t border-gray-100 dark:border-slate-700 mt-auto">
          <div className="flex items-center gap-0.5">
            <Heart className="w-3 h-3" />
            <span>{novel.likes}</span>
          </div>

          <div className="flex items-center gap-0.5">
            <Eye className="w-3 h-3" />
            <span>{novel.views > 10000 ? `${(novel.views / 10000).toFixed(1)}万` : novel.views}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
