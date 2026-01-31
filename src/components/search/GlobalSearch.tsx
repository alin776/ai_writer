import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, FileText, BookOpen, User, MapPin, Lightbulb, Loader } from 'lucide-react';
import { DataService } from '@/services/DataService';
import type { SearchResponse } from '@/types/search';
import './GlobalSearch.css';

interface GlobalSearchProps {
  isOpen: boolean;
  onClose: () => void;
}

export const GlobalSearch: React.FC<GlobalSearchProps> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const navigate = useNavigate();

  // 搜索函数（防抖）
  const handleSearch = useCallback(
    async (q: string) => {
      if (q.length < 2) {
        setResults(null);
        return;
      }

      setLoading(true);
      try {
        const data = await DataService.globalSearch(q);
        setResults(data);
        setSelectedIndex(0);
      } catch (error) {
        console.error('[GlobalSearch] 搜索失败:', error);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  // 防抖搜索
  useEffect(() => {
    const timer = setTimeout(() => {
      handleSearch(query);
    }, 300);

    return () => clearTimeout(timer);
  }, [query, handleSearch]);

  // 键盘快捷键
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) {
        // Cmd+K 或 Ctrl+K 打开搜索
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
          e.preventDefault();
          // 由父组件处理打开
        }
        return;
      }

      // ESC 关闭
      if (e.key === 'Escape') {
        onClose();
      }

      // 上下键导航
      if (!results) return;

      const allResults = [
        ...results.works.map((w) => ({ type: 'work', data: w })),
        ...results.chapters.map((c) => ({ type: 'chapter', data: c })),
        ...results.characters.map((c) => ({ type: 'character', data: c })),
        ...results.locations.map((l) => ({ type: 'location', data: l })),
        ...results.settings.map((s) => ({ type: 'setting', data: s })),
      ];

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex((prev) => (prev + 1) % allResults.length);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex((prev) => (prev - 1 + allResults.length) % allResults.length);
      } else if (e.key === 'Enter' && allResults[selectedIndex]) {
        e.preventDefault();
        handleSelect(allResults[selectedIndex]);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, results, selectedIndex, onClose]);

  // 选择结果
  const handleSelect = (item: any) => {
    const { type, data } = item;

    switch (type) {
      case 'work':
        navigate(`/works/${data.id}`);
        break;
      case 'chapter':
        // 跳转到作品详情页，并定位到指定章节
        navigate(`/works/${data.workId}`, {
          state: { targetChapterId: data.id }
        });
        break;
      case 'character':
        // 跳转到作品详情页，打开世界观面板并定位到角色
        navigate(`/works/${data.workId}`, {
          state: {
            openWorldview: true,
            worldviewTab: 'characters',
            targetItemId: data.id
          }
        });
        break;
      case 'location':
        // 跳转到作品详情页，打开世界观面板并定位到地点
        navigate(`/works/${data.workId}`, {
          state: {
            openWorldview: true,
            worldviewTab: 'locations',
            targetItemId: data.id
          }
        });
        break;
      case 'setting':
        // 跳转到作品详情页，打开世界观面板并定位到设定
        navigate(`/works/${data.workId}`, {
          state: {
            openWorldview: true,
            worldviewTab: 'settings',
            targetItemId: data.id
          }
        });
        break;
    }

    onClose();
  };

  // 高亮匹配文本
  const highlightText = (text: string, query: string) => {
    if (!query) return text;

    const parts = text.split(new RegExp(`(${query})`, 'gi'));
    return parts.map((part, i) =>
      part.toLowerCase() === query.toLowerCase() ? (
        <mark key={i} className="search-highlight">
          {part}
        </mark>
      ) : (
        part
      )
    );
  };

  if (!isOpen) return null;

  return (
    <div className="search-overlay" onClick={onClose}>
      <div className="search-dialog" onClick={(e) => e.stopPropagation()}>
        {/* 搜索框 */}
        <div className="search-input-wrapper">
          <Search className="search-icon" size={20} />
          <input
            type="text"
            className="search-input"
            placeholder="搜索作品、章节、角色、地点、设定..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
          />
          {loading && <Loader className="search-loading" size={20} />}
          <button className="search-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        {/* 搜索结果 */}
        {results && results.total > 0 && (
          <div className="search-results">
            {/* 作品 */}
            {results.works.length > 0 && (
              <div className="search-section">
                <div className="search-section-title">
                  <BookOpen size={16} />
                  <span>作品 ({results.works.length})</span>
                </div>
                {results.works.map((work, index) => (
                  <div
                    key={work.id}
                    className={`search-item ${selectedIndex === index ? 'selected' : ''}`}
                    onClick={() => handleSelect({ type: 'work', data: work })}
                  >
                    <div className="search-item-icon">
                      <BookOpen size={18} />
                    </div>
                    <div className="search-item-content">
                      <div className="search-item-title">
                        {highlightText(work.title, query)}
                      </div>
                      {work.description && (
                        <div className="search-item-description">
                          {highlightText(work.description.slice(0, 80), query)}
                          {work.description.length > 80 && '...'}
                        </div>
                      )}
                      <div className="search-item-meta">
                        {work.wordCount.toLocaleString()}字 · {work.chapterCount}章
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* 章节 */}
            {results.chapters.length > 0 && (
              <div className="search-section">
                <div className="search-section-title">
                  <FileText size={16} />
                  <span>章节 ({results.chapters.length})</span>
                </div>
                {results.chapters.map((chapter, index) => (
                  <div
                    key={chapter.id}
                    className={`search-item ${
                      selectedIndex === results.works.length + index ? 'selected' : ''
                    }`}
                    onClick={() => handleSelect({ type: 'chapter', data: chapter })}
                  >
                    <div className="search-item-icon">
                      <FileText size={18} />
                    </div>
                    <div className="search-item-content">
                      <div className="search-item-title">
                        {highlightText(chapter.title, query)}
                      </div>
                      {chapter.contentSnippet && (
                        <div className="search-item-description">
                          {highlightText(chapter.contentSnippet, query)}
                        </div>
                      )}
                      <div className="search-item-meta">
                        {chapter.workTitle} · {chapter.wordCount.toLocaleString()}字
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* 角色 */}
            {results.characters.length > 0 && (
              <div className="search-section">
                <div className="search-section-title">
                  <User size={16} />
                  <span>角色 ({results.characters.length})</span>
                </div>
                {results.characters.map((character, index) => (
                  <div
                    key={character.id}
                    className={`search-item ${
                      selectedIndex ===
                      results.works.length + results.chapters.length + index
                        ? 'selected'
                        : ''
                    }`}
                    onClick={() => handleSelect({ type: 'character', data: character })}
                  >
                    <div className="search-item-icon">
                      <User size={18} />
                    </div>
                    <div className="search-item-content">
                      <div className="search-item-title">
                        {highlightText(character.name, query)}
                        {character.role && <span className="character-role"> · {character.role}</span>}
                      </div>
                      {character.description && (
                        <div className="search-item-description">
                          {highlightText(character.description.slice(0, 80), query)}
                        </div>
                      )}
                      <div className="search-item-meta">{character.workTitle}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* 地点 */}
            {results.locations.length > 0 && (
              <div className="search-section">
                <div className="search-section-title">
                  <MapPin size={16} />
                  <span>地点 ({results.locations.length})</span>
                </div>
                {results.locations.map((location, index) => (
                  <div
                    key={location.id}
                    className={`search-item ${
                      selectedIndex ===
                      results.works.length +
                        results.chapters.length +
                        results.characters.length +
                        index
                        ? 'selected'
                        : ''
                    }`}
                    onClick={() => handleSelect({ type: 'location', data: location })}
                  >
                    <div className="search-item-icon">
                      <MapPin size={18} />
                    </div>
                    <div className="search-item-content">
                      <div className="search-item-title">
                        {highlightText(location.name, query)}
                        {location.type && <span className="location-type"> · {location.type}</span>}
                      </div>
                      {location.description && (
                        <div className="search-item-description">
                          {highlightText(location.description.slice(0, 80), query)}
                        </div>
                      )}
                      <div className="search-item-meta">{location.workTitle}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* 设定 */}
            {results.settings.length > 0 && (
              <div className="search-section">
                <div className="search-section-title">
                  <Lightbulb size={16} />
                  <span>设定 ({results.settings.length})</span>
                </div>
                {results.settings.map((setting, index) => (
                  <div
                    key={setting.id}
                    className={`search-item ${
                      selectedIndex ===
                      results.works.length +
                        results.chapters.length +
                        results.characters.length +
                        results.locations.length +
                        index
                        ? 'selected'
                        : ''
                    }`}
                    onClick={() => handleSelect({ type: 'setting', data: setting })}
                  >
                    <div className="search-item-icon">
                      <Lightbulb size={18} />
                    </div>
                    <div className="search-item-content">
                      <div className="search-item-title">
                        {highlightText(setting.title, query)}
                        {setting.category && (
                          <span className="setting-category"> · {setting.category}</span>
                        )}
                      </div>
                      {setting.content && (
                        <div className="search-item-description">
                          {highlightText(setting.content.slice(0, 80), query)}
                        </div>
                      )}
                      <div className="search-item-meta">{setting.workTitle}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* 无结果 */}
        {results && results.total === 0 && query.length >= 2 && (
          <div className="search-empty">
            <Search size={48} />
            <p>没有找到匹配的结果</p>
            <p className="search-empty-hint">试试其他关键词</p>
          </div>
        )}

        {/* 提示 */}
        {!query && (
          <div className="search-hints">
            <div className="search-hint">
              <kbd>↑</kbd> <kbd>↓</kbd> 导航
            </div>
            <div className="search-hint">
              <kbd>Enter</kbd> 选择
            </div>
            <div className="search-hint">
              <kbd>Esc</kbd> 关闭
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
