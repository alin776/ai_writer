import React, { useState, useEffect } from 'react';

// 表情分类数据
const EMOJI_CATEGORIES = {
  smileys: {
    name: '表情',
    emojis: [
      '😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂',
      '🙂', '🙃', '😉', '😊', '😇', '🥰', '😍', '🤩',
      '😘', '😗', '😚', '😙', '😋', '😛', '😜', '🤪',
      '😝', '🤗', '🤭', '🤔', '🤨', '😐', '😑', '😶',
      '😏', '😒', '🙄', '😬', '🤥', '😌', '😔', '😪',
      '🤤', '😴', '😷', '🤒', '🤕', '🤢', '🤮', '🤧',
      '🥵', '🥶', '😱', '😨', '😰', '😥', '😢', '😭',
      '😤', '😠', '😡', '🤬', '😈', '👿', '💀', '☠️'
    ]
  },
  gestures: {
    name: '手势',
    emojis: [
      '👍', '👎', '👏', '🙌', '👐', '🤲', '🤝', '🙏',
      '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆',
      '👇', '☝️', '✋', '🤚', '🖐️', '🖖', '👋', '🤏',
      '✍️', '🤳', '💪', '🦾', '🦿', '🦵', '🦶', '👂'
    ]
  },
  hearts: {
    name: '爱心',
    emojis: [
      '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍',
      '🤎', '💔', '❣️', '💕', '💞', '💓', '💗', '💖',
      '💘', '💝', '💟', '♥️', '💌', '💐', '🌹', '🥀'
    ]
  },
  symbols: {
    name: '符号',
    emojis: [
      '⭐', '🌟', '✨', '💫', '🔥', '💯', '💢', '💥',
      '💦', '💨', '🕳️', '💣', '💬', '👁️‍🗨️', '🗨️', '🗯️',
      '💭', '💤', '🎵', '🎶', '🎼', '🎹', '🥁', '🎷',
      '✅', '❌', '❓', '❗', '💲', '🔴', '🟠', '🟡'
    ]
  }
};

const RECENT_EMOJIS_KEY = 'channel_recent_emojis';
const MAX_RECENT_EMOJIS = 16;

interface MiniEmojiPickerProps {
  onSelect: (emoji: string) => void;
  onClose: () => void;
}

const MiniEmojiPicker: React.FC<MiniEmojiPickerProps> = ({ onSelect, onClose }) => {
  const [recentEmojis, setRecentEmojis] = useState<string[]>([]);

  // 加载最近使用的 emoji
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

  const saveRecentEmoji = (emoji: string) => {
    const updated = [emoji, ...recentEmojis.filter(e => e !== emoji)].slice(0, MAX_RECENT_EMOJIS);
    setRecentEmojis(updated);
    try {
      localStorage.setItem(RECENT_EMOJIS_KEY, JSON.stringify(updated));
    } catch (e) {
      console.error('保存最近表情失败:', e);
    }
  };

  const handleEmojiSelect = (emoji: string) => {
    saveRecentEmoji(emoji);
    onSelect(emoji);
  };

  return (
    <div
      className="w-72 h-80 !bg-white dark:!bg-[#232428] border border-gray-200 dark:border-[#36393f] rounded-lg overflow-hidden flex flex-col"
      style={{ boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)' }}
    >
      {/* 内容区域 */}
      <div className="flex-1 overflow-y-auto">
        {/* 最近使用 */}
        {recentEmojis.length > 0 && (
          <div className="p-2">
            <div className="text-xs text-gray-500 dark:text-[#b9bbbe] mb-1">最近使用</div>
            <div className="grid grid-cols-8 gap-0.5">
              {recentEmojis.map((emoji, index) => (
                <button
                  key={`recent-${index}`}
                  onClick={() => handleEmojiSelect(emoji)}
                  className="w-8 h-8 flex items-center justify-center text-xl hover:bg-gray-100 dark:hover:bg-[#36393f] rounded transition-colors"
                >
                  {emoji}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Emoji 分类 */}
        {Object.entries(EMOJI_CATEGORIES).map(([key, category]) => (
          <div key={key} className="p-2 border-t border-gray-200 dark:border-[#36393f]">
            <div className="text-xs text-gray-500 dark:text-[#b9bbbe] mb-1">{category.name}</div>
            <div className="grid grid-cols-8 gap-0.5">
              {category.emojis.map((emoji, index) => (
                <button
                  key={`${key}-${index}`}
                  onClick={() => handleEmojiSelect(emoji)}
                  className="w-8 h-8 flex items-center justify-center text-xl hover:bg-gray-100 dark:hover:bg-[#36393f] rounded transition-colors"
                >
                  {emoji}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MiniEmojiPicker;
