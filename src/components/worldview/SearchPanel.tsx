/**
 * 搜索过滤面板组件
 * 支持按名称、类型、标签搜索节点，以及焦点模式
 */
import React, { useState, useEffect } from 'react';
import { Search, X, Filter, Target } from 'lucide-react';

export interface SearchFilter {
  searchText: string;
  nodeTypes: {
    character: boolean;
    location: boolean;
    setting: boolean;
  };
  tags: string[];
}

interface SearchPanelProps {
  onSearchChange: (filter: SearchFilter) => void;
  onFocusModeToggle: (enabled: boolean) => void;
  focusModeEnabled: boolean;
  availableTags?: string[]; // 可选：可用的标签列表
}

export const SearchPanel: React.FC<SearchPanelProps> = ({
  onSearchChange,
  onFocusModeToggle,
  focusModeEnabled,
  availableTags = [],
}) => {
  const [searchText, setSearchText] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [nodeTypes, setNodeTypes] = useState({
    character: true,
    location: true,
    setting: true,
  });
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  // 当过滤条件变化时，通知父组件
  useEffect(() => {
    onSearchChange({
      searchText,
      nodeTypes,
      tags: selectedTags,
    });
  }, [searchText, nodeTypes, selectedTags]);

  const handleNodeTypeToggle = (type: keyof typeof nodeTypes) => {
    setNodeTypes(prev => ({
      ...prev,
      [type]: !prev[type],
    }));
  };

  const handleTagToggle = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag)
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  const handleClearSearch = () => {
    setSearchText('');
    setNodeTypes({
      character: true,
      location: true,
      setting: true,
    });
    setSelectedTags([]);
  };

  const hasActiveFilters = searchText || 
    !nodeTypes.character || 
    !nodeTypes.location || 
    !nodeTypes.setting ||
    selectedTags.length > 0;

  return (
    <div className="search-panel">
      {/* 搜索框 */}
      <div className="search-box">
        <Search className="search-icon w-4 h-4" />
        <input
          type="text"
          placeholder="搜索角色、地点、设定..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          className="search-input"
        />
        {searchText && (
          <button
            onClick={() => setSearchText('')}
            className="clear-btn"
            title="清除搜索"
          >
            <X className="w-4 h-4" />
          </button>
        )}
        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`filter-btn ${showFilters ? 'active' : ''}`}
          title="过滤选项"
        >
          <Filter className="w-4 h-4" />
        </button>
        <button
          onClick={() => onFocusModeToggle(!focusModeEnabled)}
          className={`focus-btn ${focusModeEnabled ? 'active' : ''}`}
          title={focusModeEnabled ? '退出焦点模式' : '启用焦点模式'}
        >
          <Target className="w-4 h-4" />
        </button>
      </div>

      {/* 过滤选项面板 */}
      {showFilters && (
        <div className="filter-panel">
          {/* 节点类型过滤 */}
          <div className="filter-section">
            <div className="filter-label">节点类型</div>
            <div className="filter-options">
              <label className="filter-checkbox">
                <input
                  type="checkbox"
                  checked={nodeTypes.character}
                  onChange={() => handleNodeTypeToggle('character')}
                />
                <span className="type-badge character">角色</span>
              </label>
              <label className="filter-checkbox">
                <input
                  type="checkbox"
                  checked={nodeTypes.location}
                  onChange={() => handleNodeTypeToggle('location')}
                />
                <span className="type-badge location">地点</span>
              </label>
              <label className="filter-checkbox">
                <input
                  type="checkbox"
                  checked={nodeTypes.setting}
                  onChange={() => handleNodeTypeToggle('setting')}
                />
                <span className="type-badge setting">设定</span>
              </label>
            </div>
          </div>

          {/* 标签过滤 */}
          {availableTags.length > 0 && (
            <div className="filter-section">
              <div className="filter-label">标签</div>
              <div className="filter-tags">
                {availableTags.map(tag => (
                  <button
                    key={tag}
                    onClick={() => handleTagToggle(tag)}
                    className={`tag-btn ${selectedTags.includes(tag) ? 'active' : ''}`}
                  >
                    {tag}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* 清除按钮 */}
          {hasActiveFilters && (
            <div className="filter-actions">
              <button onClick={handleClearSearch} className="clear-all-btn">
                清除所有过滤条件
              </button>
            </div>
          )}
        </div>
      )}

      <style>{`
        .search-panel {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          background: #ffffff;
          border-radius: 8px;
          border: 1px solid #e5e7eb;
        }

        .search-box {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: #f9fafb;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          padding: 0.5rem 0.75rem;
        }

        .search-icon {
          color: #9ca3af;
          flex-shrink: 0;
        }

        .search-input {
          flex: 1;
          background: transparent;
          border: none;
          outline: none;
          color: #111827;
          font-size: 0.875rem;
        }

        .search-input::placeholder {
          color: #9ca3af;
        }

        .clear-btn,
        .filter-btn,
        .focus-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 0.25rem;
          background: transparent;
          border: none;
          color: #9ca3af;
          cursor: pointer;
          border-radius: 4px;
          transition: all 0.2s;
          flex-shrink: 0;
        }

        .clear-btn:hover,
        .filter-btn:hover,
        .focus-btn:hover {
          background: #f3f4f6;
          color: #111827;
        }

        .filter-btn.active {
          background: #3b82f6;
          color: #fff;
        }

        .focus-btn.active {
          background: #10b981;
          color: #fff;
        }

        .filter-panel {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          padding: 0.75rem;
          background: #f9fafb;
          border-radius: 6px;
          border: 1px solid #d1d5db;
        }

        .filter-section {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .filter-label {
          font-size: 0.75rem;
          font-weight: 600;
          color: #9ca3af;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .filter-options {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }

        .filter-checkbox {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          cursor: pointer;
        }

        .filter-checkbox input[type="checkbox"] {
          cursor: pointer;
        }

        .type-badge {
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.75rem;
          font-weight: 500;
        }

        .type-badge.character {
          background: #3b82f6;
          color: #fff;
        }

        .type-badge.location {
          background: #10b981;
          color: #fff;
        }

        .type-badge.setting {
          background: #f59e0b;
          color: #fff;
        }

        .filter-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }

        .tag-btn {
          padding: 0.25rem 0.75rem;
          background: #f3f4f6;
          border: 1px solid #d1d5db;
          border-radius: 4px;
          color: #9ca3af;
          font-size: 0.75rem;
          cursor: pointer;
          transition: all 0.2s;
        }

        .tag-btn:hover {
          background: #e5e7eb;
          border-color: #9ca3af;
          color: #111827;
        }

        .tag-btn.active {
          background: #3b82f6;
          border-color: #3b82f6;
          color: #fff;
        }

        .filter-actions {
          padding-top: 0.5rem;
          border-top: 1px solid #e5e7eb;
        }

        .clear-all-btn {
          width: 100%;
          padding: 0.5rem;
          background: #f3f4f6;
          border: 1px solid #d1d5db;
          border-radius: 4px;
          color: #9ca3af;
          font-size: 0.875rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
        }

        .clear-all-btn:hover {
          background: #e5e7eb;
          border-color: #9ca3af;
          color: #111827;
        }
      `}</style>
    </div>
  );
};
