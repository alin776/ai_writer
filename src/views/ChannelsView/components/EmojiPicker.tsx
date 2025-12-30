import React, { useState, useEffect, useMemo } from 'react';
import { Search, Clock, Smile, Heart, ThumbsUp, Star, Coffee, Flag } from 'lucide-react';

// 表情分类数据
const EMOJI_CATEGORIES = {
  recent: {
    name: '最近使用',
    icon: Clock,
    emojis: [] // 动态加载
  },
  smileys: {
    name: '表情',
    icon: Smile,
    emojis: [
      '😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂',
      '🙂', '🙃', '😉', '😊', '😇', '🥰', '😍', '🤩',
      '😘', '😗', '😚', '😙', '😋', '😛', '😜', '🤪',
      '😝', '🤗', '🤭', '🤔', '🤨', '😐', '😑', '😶',
      '😏', '😒', '🙄', '😬', '🤥', '😌', '😔', '😪',
      '🤤', '😴', '😷', '🤒', '🤕', '🤢', '🤮', '🤧',
      '🥵', '🥶', '😱', '😨', '😰', '😥', '😢', '😭',
      '😤', '😠', '😡', '🤬', '😈', '👿', '💀', '☠️',
      '🤡', '👻', '👽', '🤖', '💩', '😺', '😸', '😹'
    ]
  },
  gestures: {
    name: '手势',
    icon: ThumbsUp,
    emojis: [
      '👍', '👎', '👏', '🙌', '👐', '🤲', '🤝', '🙏',
      '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆',
      '👇', '☝️', '✋', '🤚', '🖐️', '🖖', '👋', '🤏',
      '✍️', '🤳', '💪', '🦾', '🦿', '🦵', '🦶', '👂',
      '🦻', '👃', '🧠', '🫀', '🫁', '🦷', '🦴', '👀',
      '👁️', '👅', '👄', '💋', '🩸', '👶', '🧒', '👦'
    ]
  },
  hearts: {
    name: '爱心',
    icon: Heart,
    emojis: [
      '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍',
      '🤎', '💔', '❣️', '💕', '💞', '💓', '💗', '💖',
      '💘', '💝', '💟', '♥️', '💌', '💐', '🌹', '🥀',
      '🌺', '🌸', '🌷', '🌻', '🌼', '💮', '🏵️', '🎀'
    ]
  },
  symbols: {
    name: '符号',
    icon: Star,
    emojis: [
      '⭐', '🌟', '✨', '💫', '🔥', '💯', '💢', '💥',
      '💦', '💨', '🕳️', '💣', '💬', '👁️‍🗨️', '🗨️', '🗯️',
      '💭', '💤', '🎵', '🎶', '🎼', '🎹', '🥁', '🎷',
      '✅', '❌', '❓', '❗', '💲', '🔴', '🟠', '🟡',
      '🟢', '🔵', '🟣', '⚫', '⚪', '🟤', '🔶', '🔷'
    ]
  },
  food: {
    name: '食物',
    icon: Coffee,
    emojis: [
      '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓',
      '🫐', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝',
      '🍔', '🍟', '🍕', '🌭', '🥪', '🌮', '🌯', '🥗',
      '🍜', '🍝', '🍣', '🍱', '🍛', '🍚', '🍙', '🍘',
      '☕', '🍵', '🧃', '🥤', '🧋', '🍺', '🍻', '🥂',
      '🍷', '🥃', '🍸', '🍹', '🧉', '🍾', '🍶', '🧊'
    ]
  },
  activities: {
    name: '活动',
    icon: Flag,
    emojis: [
      '⚽', '🏀', '🏈', '⚾', '🥎', '🎾', '🏐', '🏉',
      '🥏', '🎱', '🪀', '🏓', '🏸', '🏒', '🏑', '🥍',
      '🏏', '🪃', '🥅', '⛳', '🪁', '🏹', '🎣', '🤿',
      '🎮', '🕹️', '🎲', '🧩', '♟️', '🎭', '🎨', '🎬',
      '🎤', '🎧', '🎷', '🪘', '🎸', '🪕', '🎻', '🎺'
    ]
  }
};

// Emoji 搜索关键词映射（简化版）
const EMOJI_KEYWORDS: Record<string, string[]> = {
  '😀': ['笑', '开心', '高兴', 'smile', 'happy'],
  '😂': ['笑哭', '哈哈', 'laugh', 'cry'],
  '🤣': ['笑死', '太好笑', 'rofl'],
  '😍': ['爱', '喜欢', '心', 'love', 'heart'],
  '🥰': ['爱', '幸福', 'love', 'happy'],
  '😘': ['亲', '么么哒', 'kiss'],
  '😭': ['哭', '难过', 'cry', 'sad'],
  '😱': ['惊', '吓', 'shock', 'scared'],
  '😡': ['生气', '愤怒', 'angry'],
  '🤔': ['思考', '想', 'think'],
  '👍': ['赞', '好', '棒', 'good', 'like', 'thumb'],
  '👎': ['差', '不好', 'bad', 'dislike'],
  '👏': ['鼓掌', '棒', 'clap', 'applause'],
  '🙏': ['谢谢', '拜托', '祈祷', 'thanks', 'pray'],
  '❤️': ['爱', '心', '喜欢', 'love', 'heart', 'red'],
  '💔': ['心碎', '伤心', 'broken', 'sad'],
  '🔥': ['火', '热', '厉害', 'fire', 'hot'],
  '💯': ['满分', '完美', '百分', 'perfect', 'hundred'],
  '✅': ['对', '正确', '完成', 'check', 'done', 'yes'],
  '❌': ['错', '不对', '取消', 'cross', 'no', 'wrong'],
  '⭐': ['星', '收藏', 'star', 'favorite'],
  '✨': ['闪', '亮', '新', 'sparkle', 'new'],
};

const RECENT_EMOJIS_KEY = 'channel_recent_emojis';
const MAX_RECENT_EMOJIS = 16;

interface EmojiPickerProps {
  onSelect: (emoji: string) => void;
  onClose?: () => void;
}

const EmojiPicker: React.FC<EmojiPickerProps> = ({ onSelect, onClose }) => {
  const [activeCategory, setActiveCategory] = useState<string>('smileys');
  const [searchQuery, setSearchQuery] = useState('');
  const [recentEmojis, setRecentEmojis] = useState<string[]>([]);

  // 加载最近使用的表情
  useEffect(() => {
    try {
      const saved = localStorage.getItem(RECENT_EMOJIS_KEY);
      if (saved) {
        setRecentEmojis(JSON.parse(saved));
      }
    } catch (e) {
      console.error('加载最近表情失败:', e);
    }
  }, []);

  // 保存最近使用的表情
  const saveRecentEmoji = (emoji: string) => {
    const updated = [emoji, ...recentEmojis.filter(e => e !== emoji)].slice(0, MAX_RECENT_EMOJIS);
    setRecentEmojis(updated);
    try {
      localStorage.setItem(RECENT_EMOJIS_KEY, JSON.stringify(updated));
    } catch (e) {
      console.error('保存最近表情失败:', e);
    }
  };

  // 选择表情
  const handleSelect = (emoji: string) => {
    saveRecentEmoji(emoji);
    onSelect(emoji);
  };

  // 搜索结果
  const searchResults = useMemo(() => {
    if (!searchQuery.trim()) return null;

    const query = searchQuery.toLowerCase();
    const results: string[] = [];

    // 搜索所有分类
    Object.values(EMOJI_CATEGORIES).forEach(category => {
      if (category.emojis) {
        category.emojis.forEach(emoji => {
          // 检查关键词
          const keywords = EMOJI_KEYWORDS[emoji] || [];
          if (keywords.some(kw => kw.includes(query))) {
            if (!results.includes(emoji)) {
              results.push(emoji);
            }
          }
        });
      }
    });

    return results;
  }, [searchQuery]);

  // 当前显示的表情列表
  const currentEmojis = useMemo(() => {
    if (searchResults !== null) {
      return searchResults;
    }
    if (activeCategory === 'recent') {
      return recentEmojis;
    }
    return EMOJI_CATEGORIES[activeCategory as keyof typeof EMOJI_CATEGORIES]?.emojis || [];
  }, [activeCategory, recentEmojis, searchResults]);

  const categoryKeys = Object.keys(EMOJI_CATEGORIES) as (keyof typeof EMOJI_CATEGORIES)[];

  return (
    <div className="w-80 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl overflow-hidden">
      {/* 搜索框 */}
      <div className="p-2 border-b border-gray-100 dark:border-gray-700">
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="搜索表情..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-3 py-1.5 text-sm border border-gray-200 dark:border-gray-600 rounded-md bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* 分类导航 */}
      {!searchQuery && (
        <div className="flex items-center gap-1 px-2 py-1.5 border-b border-gray-100 dark:border-gray-700 overflow-x-auto">
          {categoryKeys.map((key) => {
            const category = EMOJI_CATEGORIES[key];
            const Icon = category.icon;
            const isActive = activeCategory === key;
            const hasEmojis = key === 'recent' ? recentEmojis.length > 0 : true;

            if (!hasEmojis && key === 'recent') return null;

            return (
              <button
                key={key}
                onClick={() => setActiveCategory(key)}
                className={`p-1.5 rounded transition-colors flex-shrink-0 ${
                  isActive
                    ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400'
                    : 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
                title={category.name}
              >
                <Icon className="w-4 h-4" />
              </button>
            );
          })}
        </div>
      )}

      {/* 表情网格 */}
      <div className="p-2 max-h-56 overflow-y-auto">
        {currentEmojis.length > 0 ? (
          <div className="grid grid-cols-8 gap-0.5">
            {currentEmojis.map((emoji, index) => (
              <button
                key={`${emoji}-${index}`}
                onClick={() => handleSelect(emoji)}
                className="w-8 h-8 flex items-center justify-center text-xl hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                title={emoji}
              >
                {emoji}
              </button>
            ))}
          </div>
        ) : (
          <div className="text-center py-6 text-sm text-gray-400 dark:text-gray-500">
            {searchQuery ? '未找到匹配的表情' : '暂无最近使用的表情'}
          </div>
        )}
      </div>
    </div>
  );
};

export default EmojiPicker;
