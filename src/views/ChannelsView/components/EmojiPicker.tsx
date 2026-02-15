import React, { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import { Search, Smile, Heart, Plus, X, Loader2 } from 'lucide-react';
import {
  searchStickers,
  getMyStickers,
  getFavoriteStickers,
  addFavoriteSticker,
  removeFavoriteSticker,
  uploadSticker,
  deleteSticker,
  TenorSticker,
  UserSticker,
  FavoriteSticker
} from '../../../services/stickerApi';
import StickerEditor from '@/components/common/StickerEditor';

// ==================== 常量定义 ====================

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

// Tab 类型
type TabType = 'search' | 'emoji' | 'favorite';

interface EmojiPickerProps {
  onSelect: (emoji: string) => void;
  onSelectSticker?: (url: string) => void;
  onClose?: () => void;
}

const EmojiPicker: React.FC<EmojiPickerProps> = ({ onSelect, onSelectSticker, onClose }) => {
  // ==================== 状态 ====================
  const [activeTab, setActiveTab] = useState<TabType>('emoji');
  const [searchQuery, setSearchQuery] = useState('');
  const [recentEmojis, setRecentEmojis] = useState<string[]>([]);

  // 搜索相关状态
  const [searchResults, setSearchResults] = useState<TenorSticker[]>([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchNextPos, setSearchNextPos] = useState<string | undefined>();

  // 自定义贴图状态
  const [myStickers, setMyStickers] = useState<UserSticker[]>([]);
  const [myStickersLoading, setMyStickersLoading] = useState(false);

  // 收藏贴图状态
  const [favorites, setFavorites] = useState<FavoriteSticker[]>([]);
  const [favoritesLoading, setFavoritesLoading] = useState(false);

  // 上传状态
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // 图片裁剪状态
  const [showCropper, setShowCropper] = useState(false);
  const [cropperImageSrc, setCropperImageSrc] = useState<string>('');

  // 搜索防抖
  const searchTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // ==================== 初始化 ====================

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

  // 加载自定义贴图
  useEffect(() => {
    if (activeTab === 'emoji') {
      loadMyStickers();
    }
  }, [activeTab]);

  // 组件初始化时加载收藏列表（用于搜索结果判断是否已收藏）
  useEffect(() => {
    loadFavorites();
  }, []);

  // 切换到收藏 Tab 时刷新
  useEffect(() => {
    if (activeTab === 'favorite') {
      loadFavorites();
    }
  }, [activeTab]);

  // 快速查找是否已收藏（基于 tenorId）
  const favoriteIds = useMemo(() => {
    return new Set(favorites.filter(f => f.tenorId).map(f => f.tenorId));
  }, [favorites]);

  // ==================== 数据加载函数 ====================

  const loadMyStickers = async () => {
    if (myStickersLoading) return;
    setMyStickersLoading(true);
    try {
      const data = await getMyStickers();
      setMyStickers(data);
    } catch (e) {
      console.error('加载自定义贴图失败:', e);
    } finally {
      setMyStickersLoading(false);
    }
  };

  const loadFavorites = async () => {
    if (favoritesLoading) return;
    setFavoritesLoading(true);
    try {
      const data = await getFavoriteStickers();
      setFavorites(data);
    } catch (e) {
      console.error('加载收藏贴图失败:', e);
    } finally {
      setFavoritesLoading(false);
    }
  };

  // ==================== 搜索功能 ====================

  const handleSearch = useCallback(async (query: string, append = false) => {
    if (!query.trim()) {
      setSearchResults([]);
      setSearchNextPos(undefined);
      return;
    }

    setSearchLoading(true);
    try {
      const pos = append ? searchNextPos : undefined;
      const data = await searchStickers(query, 20, pos);
      console.log('[EmojiPicker] 搜索结果:', data);  // 调试

      if (append) {
        setSearchResults(prev => [...prev, ...data.stickers]);
      } else {
        setSearchResults(data.stickers);
      }
      setSearchNextPos(data.next);
    } catch (e) {
      console.error('搜索贴图失败:', e);
    } finally {
      setSearchLoading(false);
    }
  }, [searchNextPos]);

  // 搜索输入防抖
  useEffect(() => {
    if (activeTab !== 'search') return;

    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    searchTimeoutRef.current = setTimeout(() => {
      handleSearch(searchQuery);
    }, 500);

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [searchQuery, activeTab, handleSearch]);

  // ==================== Emoji 选择 ====================

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

  // ==================== 贴图选择 ====================

  const handleStickerSelect = (url: string) => {
    if (onSelectSticker) {
      onSelectSticker(url);
    }
  };

  // ==================== 收藏功能 ====================

  const handleAddFavorite = async (sticker: TenorSticker) => {
    try {
      const favorite = await addFavoriteSticker({
        stickerUrl: sticker.url,
        previewUrl: sticker.previewUrl,
        source: 'tenor',
        tenorId: sticker.id
      });
      setFavorites(prev => [favorite, ...prev]);
    } catch (e) {
      console.error('收藏失败:', e);
    }
  };

  const handleRemoveFavorite = async (favoriteId: string) => {
    try {
      await removeFavoriteSticker(favoriteId);
      setFavorites(prev => prev.filter(f => f.id !== favoriteId));
    } catch (e) {
      console.error('取消收藏失败:', e);
    }
  };

  // 切换收藏状态（用于搜索结果）
  const handleToggleFavorite = async (sticker: TenorSticker) => {
    const existingFavorite = favorites.find(f => f.tenorId === sticker.id);
    if (existingFavorite) {
      await handleRemoveFavorite(existingFavorite.id);
    } else {
      await handleAddFavorite(sticker);
    }
  };

  // ==================== 上传功能 ====================

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      alert('请选择图片文件');
      return;
    }

    // 验证文件大小 (2MB)
    if (file.size > 2 * 1024 * 1024) {
      alert('文件大小不能超过 2MB');
      return;
    }

    // 读取文件并打开裁剪器
    const reader = new FileReader();
    reader.onload = () => {
      setCropperImageSrc(reader.result as string);
      setShowCropper(true);
    };
    reader.readAsDataURL(file);

    // 清空 input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // 裁剪完成后上传
  const handleCropComplete = async (croppedBlob: Blob) => {
    setShowCropper(false);
    setCropperImageSrc('');
    setUploading(true);

    try {
      // 将 Blob 转换为 File
      const file = new File([croppedBlob], 'sticker.png', { type: 'image/png' });
      const sticker = await uploadSticker(file);
      setMyStickers(prev => [sticker, ...prev]);
    } catch (e) {
      console.error('上传失败:', e);
      alert('上传失败，请重试');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteSticker = async (stickerId: string) => {
    if (!confirm('确定要删除这个表情吗？')) return;

    try {
      await deleteSticker(stickerId);
      setMyStickers(prev => prev.filter(s => s.id !== stickerId));
    } catch (e) {
      console.error('删除失败:', e);
    }
  };

  // ==================== 渲染函数 ====================

  // 渲染搜索 Tab
  const renderSearchTab = () => (
    <div className="flex flex-col h-full">
      {/* 搜索输入框 */}
      <div className="p-2 border-b border-gray-100 dark:border-gray-700">
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="搜索表情包..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-3 py-1.5 text-sm border border-gray-200 dark:border-gray-600 rounded-md bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500"
            autoFocus
          />
        </div>
      </div>

      {/* 搜索结果 */}
      <div className="flex-1 overflow-y-auto p-2">
        {searchLoading && searchResults.length === 0 ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
          </div>
        ) : searchResults.length > 0 ? (
          <>
            <div className="grid grid-cols-4 gap-1">
              {searchResults.map((sticker) => {
                const isFavorited = favoriteIds.has(sticker.id);
                return (
                  <div
                    key={sticker.id}
                    className="relative group aspect-square rounded overflow-hidden cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700"
                    onClick={() => handleStickerSelect(sticker.url)}
                  >
                    <img
                      src={sticker.previewUrl}
                      alt={sticker.description || '贴图'}
                      className="w-full h-full object-contain"
                      loading="lazy"
                      onError={(e) => {
                        console.error('[EmojiPicker] 图片加载失败:', sticker.previewUrl);
                        const target = e.target as HTMLImageElement;
                        if (target.src !== sticker.url) {
                          target.src = sticker.url;
                        }
                      }}
                    />
                    {/* 收藏按钮 - 已收藏显示红心 */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleToggleFavorite(sticker);
                      }}
                      className={`absolute top-0.5 right-0.5 p-1 rounded transition-opacity ${
                        isFavorited
                          ? 'bg-red-500 opacity-100'
                          : 'bg-black/50 opacity-0 group-hover:opacity-100'
                      }`}
                      title={isFavorited ? '取消收藏' : '收藏'}
                    >
                      <Heart
                        className={`w-3 h-3 ${isFavorited ? 'text-white fill-white' : 'text-white'}`}
                      />
                    </button>
                  </div>
                );
              })}
            </div>
            {/* 加载更多 */}
            {searchNextPos && (
              <button
                onClick={() => handleSearch(searchQuery, true)}
                disabled={searchLoading}
                className="w-full mt-2 py-2 text-sm text-blue-500 hover:text-blue-600 disabled:opacity-50"
              >
                {searchLoading ? '加载中...' : '加载更多'}
              </button>
            )}
          </>
        ) : searchQuery ? (
          <div className="text-center py-8 text-sm text-gray-400">
            未找到相关表情包
          </div>
        ) : (
          <div className="text-center py-8 text-sm text-gray-400">
            输入关键词搜索表情包
          </div>
        )}
      </div>
    </div>
  );

  // 渲染表情 Tab
  const renderEmojiTab = () => (
    <div className="flex flex-col h-full overflow-y-auto">
      {/* 最近使用 */}
      {recentEmojis.length > 0 && (
        <div className="p-2">
          <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">最近使用</div>
          <div className="grid grid-cols-8 gap-0.5">
            {recentEmojis.map((emoji, index) => (
              <button
                key={`recent-${index}`}
                onClick={() => handleEmojiSelect(emoji)}
                className="w-8 h-8 flex items-center justify-center text-xl hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                {emoji}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Emoji 分类 */}
      {Object.entries(EMOJI_CATEGORIES).map(([key, category]) => (
        <div key={key} className="p-2 border-t border-gray-100 dark:border-gray-700">
          <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">{category.name}</div>
          <div className="grid grid-cols-8 gap-0.5">
            {category.emojis.map((emoji, index) => (
              <button
                key={`${key}-${index}`}
                onClick={() => handleEmojiSelect(emoji)}
                className="w-8 h-8 flex items-center justify-center text-xl hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                {emoji}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );

  // 渲染收藏 Tab
  const renderFavoriteTab = () => (
    <div className="flex-1 overflow-y-auto p-2">
      {/* 隐藏的文件输入 */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
      />

      {favoritesLoading || myStickersLoading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
        </div>
      ) : (
        <div className="grid grid-cols-4 gap-1">
          {/* 添加按钮 - 第一个位置 */}
          <button
            onClick={handleUploadClick}
            disabled={uploading}
            className="aspect-square rounded flex items-center justify-center transition-colors disabled:opacity-50"
            style={{
              border: '2px dashed #9ca3af',
            }}
            title="添加自定义表情"
          >
            {uploading ? (
              <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
            ) : (
              <Plus className="w-6 h-6 text-gray-400" />
            )}
          </button>

          {/* 自定义表情 */}
          {myStickers.map((sticker) => (
            <div
              key={`my-${sticker.id}`}
              className="relative group aspect-square rounded overflow-hidden cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700"
              onClick={() => handleStickerSelect(sticker.imageUrl)}
            >
              <img
                src={sticker.previewUrl || sticker.imageUrl}
                alt={sticker.name || '贴图'}
                className="w-full h-full object-cover"
              />
              {/* 删除按钮 */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteSticker(sticker.id);
                }}
                className="absolute top-0.5 right-0.5 p-1 bg-black/50 rounded opacity-0 group-hover:opacity-100 transition-opacity"
                title="删除"
              >
                <X className="w-3 h-3 text-white" />
              </button>
            </div>
          ))}

          {/* 收藏的表情 */}
          {favorites.map((favorite) => (
            <div
              key={`fav-${favorite.id}`}
              className="relative group aspect-square rounded overflow-hidden cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700"
              onClick={() => handleStickerSelect(favorite.stickerUrl)}
            >
              <img
                src={favorite.previewUrl || favorite.stickerUrl}
                alt="收藏贴图"
                className="w-full h-full object-cover"
                loading="lazy"
              />
              {/* 取消收藏按钮 */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleRemoveFavorite(favorite.id);
                }}
                className="absolute top-0.5 right-0.5 p-1 bg-black/50 rounded opacity-0 group-hover:opacity-100 transition-opacity"
                title="取消收藏"
              >
                <X className="w-3 h-3 text-white" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* 空状态提示 */}
      {!favoritesLoading && !myStickersLoading && myStickers.length === 0 && favorites.length === 0 && (
        <div className="text-center py-4 text-xs text-gray-400">
          点击 + 添加自定义表情，或在搜索中收藏表情
        </div>
      )}
    </div>
  );

  return (
    <div className="w-80 h-96 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl overflow-hidden flex flex-col">
      {/* 内容区域 */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'search' && renderSearchTab()}
        {activeTab === 'emoji' && renderEmojiTab()}
        {activeTab === 'favorite' && renderFavoriteTab()}
      </div>

      {/* 底部 Tab 导航 */}
      <div className="flex items-center justify-around border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
        <button
          onClick={() => setActiveTab('search')}
          className={`flex-1 py-2.5 flex items-center justify-center transition-colors ${
            activeTab === 'search'
              ? 'text-blue-500 bg-blue-50 dark:bg-blue-900/30'
              : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
          }`}
          title="搜索表情"
        >
          <Search className="w-5 h-5" />
        </button>
        <button
          onClick={() => setActiveTab('emoji')}
          className={`flex-1 py-2.5 flex items-center justify-center transition-colors ${
            activeTab === 'emoji'
              ? 'text-blue-500 bg-blue-50 dark:bg-blue-900/30'
              : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
          }`}
          title="表情"
        >
          <Smile className="w-5 h-5" />
        </button>
        <button
          onClick={() => setActiveTab('favorite')}
          className={`flex-1 py-2.5 flex items-center justify-center transition-colors ${
            activeTab === 'favorite'
              ? 'text-blue-500 bg-blue-50 dark:bg-blue-900/30'
              : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
          }`}
          title="收藏"
        >
          <Heart className="w-5 h-5" />
        </button>
      </div>

      {/* 表情包编辑器（支持添加文字） */}
      <StickerEditor
        isOpen={showCropper}
        imageSrc={cropperImageSrc}
        onClose={() => {
          setShowCropper(false);
          setCropperImageSrc('');
        }}
        onSave={handleCropComplete}
        aspect={1}
      />
    </div>
  );
};

export default EmojiPicker;
