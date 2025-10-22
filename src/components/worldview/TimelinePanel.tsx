/**
 * 时间线面板组件
 * 显示角色成长、关系变化、地点变化的时间线视图
 */
import React, { useState, useMemo } from 'react';
import { Clock, Plus, Edit2, Trash2, ChevronLeft, ChevronRight } from 'lucide-react';
import type { TimelineEvent, TimelineTrack, ChapterAnchor, EntityType } from '@/types/timeline';
import type { Character, Location, Setting } from '@/types';
import type { Relationship } from '@/types/relationship';

interface TimelinePanelProps {
  workId: string;
  events: TimelineEvent[];
  chapters: ChapterAnchor[];
  characters: Character[];
  locations: Location[];
  settings: Setting[];
  relationships: Relationship[];
  onAddEvent?: () => void;
  onEditEvent?: (event: TimelineEvent) => void;
  onDeleteEvent?: (eventId: string) => void;
  onEventClick?: (event: TimelineEvent) => void;
}

export const TimelinePanel: React.FC<TimelinePanelProps> = ({
  workId,
  events,
  chapters,
  characters,
  locations,
  settings,
  relationships,
  onAddEvent,
  onEditEvent,
  onDeleteEvent,
  onEventClick,
}) => {
  const [selectedChapter, setSelectedChapter] = useState(0);
  // 默认展开所有轨道，提升用户体验
  const [expandedTracks, setExpandedTracks] = useState<Set<string>>(
    new Set(['character', 'relationship', 'location', 'setting'])
  );

  // 构建时间线轨道数据
  const tracks = useMemo(() => {
    const tracksMap = new Map<string, TimelineTrack>();

    // 按实体分组事件
    events.forEach(event => {
      const key = `${event.entityType}-${event.entityId}`;
      
      if (!tracksMap.has(key)) {
        // 获取实体标签
        let label = '未知';
        let color = '#6b7280';
        
        if (event.entityType === 'character') {
          const char = characters.find(c => c.id === event.entityId);
          label = char?.name || '未知角色';
          color = '#3b82f6';
        } else if (event.entityType === 'location') {
          const loc = locations.find(l => l.id === event.entityId);
          label = loc?.name || '未知地点';
          color = '#10b981';
        } else if (event.entityType === 'setting') {
          const set = settings.find(s => s.id === event.entityId);
          label = set?.title || '未知设定';
          color = '#f59e0b';
        } else if (event.entityType === 'relationship') {
          const rel = relationships.find(r => r.id === event.entityId);
          label = rel?.label || '未知关系';
          color = '#8b5cf6';
        }
        
        tracksMap.set(key, {
          entityId: event.entityId,
          entityType: event.entityType,
          entityLabel: label,
          color,
          events: [],
        });
      }
      
      tracksMap.get(key)!.events.push(event);
    });

    // 排序事件
    tracksMap.forEach(track => {
      track.events.sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));
    });

    return Array.from(tracksMap.values());
  }, [events, characters, locations, settings, relationships]);

  // 按类型分组轨道
  const groupedTracks = useMemo(() => {
    const groups: Record<EntityType, TimelineTrack[]> = {
      character: [],
      location: [],
      setting: [],
      relationship: [],
    };
    
    tracks.forEach(track => {
      groups[track.entityType].push(track);
    });
    
    return groups;
  }, [tracks]);

  // 切换轨道展开/折叠
  const toggleTrack = (entityType: EntityType) => {
    setExpandedTracks(prev => {
      const next = new Set(prev);
      if (next.has(entityType)) {
        next.delete(entityType);
      } else {
        next.add(entityType);
      }
      return next;
    });
  };

  // 计算事件在时间线上的位置（基于章节）
  const calculateEventPosition = (event: TimelineEvent): number => {
    if (!event.chapterNumber || chapters.length === 0) {
      // 如果没有章节信息，使用原始timestamp
      return Math.min((event.timestamp || 0) / 10, 100);
    }
    
    // 基于章节数量计算每个章节占据的百分比宽度
    const chapterWidth = 100 / chapters.length;
    
    // 找到事件所在章节的索引
    const chapterIndex = chapters.findIndex(ch => ch.chapterNumber === event.chapterNumber);
    
    if (chapterIndex === -1) {
      // 如果找不到章节，使用章节号直接计算
      return Math.min((event.chapterNumber - 1) * chapterWidth + chapterWidth / 2, 100);
    }
    
    // 事件位于该章节的中间位置
    return chapterIndex * chapterWidth + chapterWidth / 2;
  };

  // 渲染事件标记
  const renderEvent = (event: TimelineEvent) => {
    const eventTypeColors: Record<string, string> = {
      milestone: '#f59e0b',
      change: '#3b82f6',
      created: '#10b981',
      removed: '#ef4444',
    };
    
    const color = event.color || eventTypeColors[event.eventType] || '#6b7280';
    const position = calculateEventPosition(event);
    
    return (
      <div
        key={event.id}
        className="timeline-event"
        style={{
          left: `${position}%`,
        }}
        onClick={() => onEventClick?.(event)}
        title={event.title}
      >
        <div
          className="event-marker"
          style={{ backgroundColor: color }}
        >
          {event.icon && <span className="event-icon">{event.icon}</span>}
        </div>
        <div className="event-label">{event.title}</div>
        <div className="event-actions">
          <button onClick={(e) => { e.stopPropagation(); onEditEvent?.(event); }}>
            <Edit2 className="w-3 h-3" />
          </button>
          <button onClick={(e) => { e.stopPropagation(); onDeleteEvent?.(event.id); }}>
            <Trash2 className="w-3 h-3" />
          </button>
        </div>
      </div>
    );
  };

  // 渲染章节分隔线
  const renderChapterMarkers = () => {
    if (chapters.length === 0) return null;
    
    const chapterWidth = 100 / chapters.length;
    
    return (
      <>
        {chapters.map((chapter, index) => (
          <div
            key={chapter.id}
            className="chapter-marker"
            style={{ left: `${index * chapterWidth}%` }}
            title={`第${chapter.chapterNumber}章：${chapter.chapterTitle}`}
          >
            <div className="chapter-marker-line" />
            <div className="chapter-marker-label">Ch{chapter.chapterNumber}</div>
          </div>
        ))}
      </>
    );
  };

  // 渲染时间线轨道
  const renderTrack = (track: TimelineTrack) => {
    return (
      <div key={`${track.entityType}-${track.entityId}`} className="timeline-track">
        <div className="track-header" style={{ borderLeftColor: track.color }}>
          <span className="track-label">{track.entityLabel}</span>
          <span className="track-count">({track.events.length})</span>
        </div>
        <div className="track-line">
          {renderChapterMarkers()}
          {track.events.map(renderEvent)}
        </div>
      </div>
    );
  };

  // 渲染分组标题
  const renderGroupHeader = (entityType: EntityType, count: number) => {
    const isExpanded = expandedTracks.has(entityType);
    const labels: Record<EntityType, string> = {
      character: '角色成长',
      location: '地点变化',
      setting: '设定变化',
      relationship: '关系变化',
    };
    
    return (
      <div
        className="timeline-group-header"
        onClick={() => toggleTrack(entityType)}
      >
        <Clock className="w-4 h-4" />
        <span>{labels[entityType]}</span>
        <span className="group-count">({count})</span>
        <button className="expand-btn">
          {isExpanded ? '▼' : '▶'}
        </button>
      </div>
    );
  };

  return (
    <div className="timeline-panel">
      {/* 顶部章节选择器 */}
      <div className="timeline-header">
        <button
          className="chapter-nav-btn"
          onClick={() => setSelectedChapter(Math.max(0, selectedChapter - 1))}
          disabled={selectedChapter === 0}
        >
          <ChevronLeft className="w-4 h-4" />
        </button>
        
        <div className="chapter-anchors">
          {chapters.map((chapter, index) => (
            <button
              key={chapter.id}
              className={`chapter-anchor ${index === selectedChapter ? 'active' : ''}`}
              onClick={() => setSelectedChapter(index)}
              title={`第${chapter.chapterNumber}章：${chapter.chapterTitle}`}
            >
              <span className="chapter-number">第{chapter.chapterNumber}章</span>
              <span className="chapter-title">{chapter.chapterTitle}</span>
            </button>
          ))}
        </div>
        
        <button
          className="chapter-nav-btn"
          onClick={() => setSelectedChapter(Math.min(chapters.length - 1, selectedChapter + 1))}
          disabled={selectedChapter >= chapters.length - 1}
        >
          <ChevronRight className="w-4 h-4" />
        </button>
        
        {onAddEvent && (
          <button className="btn-add-event" onClick={onAddEvent}>
            <Plus className="w-4 h-4" />
            添加事件
          </button>
        )}
      </div>

      {/* 时间线轨道区域 */}
      <div className="timeline-content">
        {/* 角色成长轨道 */}
        {groupedTracks.character.length > 0 && (
          <div className="timeline-group">
            {renderGroupHeader('character', groupedTracks.character.length)}
            {expandedTracks.has('character') && (
              <div className="timeline-tracks">
                {groupedTracks.character.map(renderTrack)}
              </div>
            )}
          </div>
        )}

        {/* 关系变化轨道 */}
        {groupedTracks.relationship.length > 0 && (
          <div className="timeline-group">
            {renderGroupHeader('relationship', groupedTracks.relationship.length)}
            {expandedTracks.has('relationship') && (
              <div className="timeline-tracks">
                {groupedTracks.relationship.map(renderTrack)}
              </div>
            )}
          </div>
        )}

        {/* 地点变化轨道 */}
        {groupedTracks.location.length > 0 && (
          <div className="timeline-group">
            {renderGroupHeader('location', groupedTracks.location.length)}
            {expandedTracks.has('location') && (
              <div className="timeline-tracks">
                {groupedTracks.location.map(renderTrack)}
              </div>
            )}
          </div>
        )}

        {/* 设定变化轨道 */}
        {groupedTracks.setting.length > 0 && (
          <div className="timeline-group">
            {renderGroupHeader('setting', groupedTracks.setting.length)}
            {expandedTracks.has('setting') && (
              <div className="timeline-tracks">
                {groupedTracks.setting.map(renderTrack)}
              </div>
            )}
          </div>
        )}

        {/* 空状态 */}
        {events.length === 0 && (
          <div className="timeline-empty">
            <Clock className="w-12 h-12 text-gray-400" />
            <p className="text-gray-500 mt-4">暂无时间线事件</p>
            {onAddEvent && (
              <button className="btn-primary mt-4" onClick={onAddEvent}>
                <Plus className="w-4 h-4" />
                创建第一个事件
              </button>
            )}
          </div>
        )}
      </div>

      {/* CSS样式 */}
      <style jsx>{`
        .timeline-panel {
          height: 100%;
          display: flex;
          flex-direction: column;
          background: #1a1a1a;
        }

        .timeline-header {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 1rem;
          border-bottom: 1px solid #2a2a2a;
          background: #0f0f0f;
        }

        .chapter-nav-btn {
          padding: 0.5rem;
          background: #2a2a2a;
          border: none;
          border-radius: 4px;
          color: #fff;
          cursor: pointer;
          transition: all 0.2s;
        }

        .chapter-nav-btn:hover:not(:disabled) {
          background: #3a3a3a;
        }

        .chapter-nav-btn:disabled {
          opacity: 0.3;
          cursor: not-allowed;
        }

        .chapter-anchors {
          flex: 1;
          display: flex;
          gap: 0.5rem;
          overflow-x: auto;
          padding: 0.5rem 0;
        }

        .chapter-anchor {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 0.5rem 1rem;
          background: #2a2a2a;
          border: 2px solid transparent;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s;
          white-space: nowrap;
        }

        .chapter-anchor:hover {
          background: #3a3a3a;
        }

        .chapter-anchor.active {
          border-color: #3b82f6;
          background: #1e3a8a;
        }

        .chapter-number {
          font-size: 0.75rem;
          color: #9ca3af;
        }

        .chapter-title {
          font-size: 0.875rem;
          color: #fff;
          margin-top: 0.25rem;
        }

        .btn-add-event {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          background: #3b82f6;
          color: #fff;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.875rem;
          transition: all 0.2s;
        }

        .btn-add-event:hover {
          background: #2563eb;
        }

        .timeline-content {
          flex: 1;
          overflow-y: auto;
          padding: 1rem;
        }

        .timeline-group {
          margin-bottom: 2rem;
        }

        .timeline-group-header {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1rem;
          background: #2a2a2a;
          border-radius: 8px;
          cursor: pointer;
          user-select: none;
          transition: all 0.2s;
        }

        .timeline-group-header:hover {
          background: #3a3a3a;
        }

        .group-count {
          color: #9ca3af;
          font-size: 0.875rem;
        }

        .expand-btn {
          margin-left: auto;
          background: none;
          border: none;
          color: #9ca3af;
          cursor: pointer;
          font-size: 0.875rem;
        }

        .timeline-tracks {
          margin-top: 1rem;
          padding-left: 1rem;
        }

        .timeline-track {
          position: relative;
          margin-bottom: 1.5rem;
        }

        .track-header {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding-left: 1rem;
          border-left: 3px solid #3b82f6;
          margin-bottom: 0.5rem;
        }

        .track-label {
          font-weight: 500;
          color: #fff;
        }

        .track-count {
          color: #9ca3af;
          font-size: 0.875rem;
        }

        .track-line {
          position: relative;
          height: 40px;
          background: linear-gradient(90deg, #2a2a2a 0%, #1a1a1a 100%);
          border-radius: 20px;
          overflow: visible;
        }

        .chapter-marker {
          position: absolute;
          top: 0;
          height: 100%;
          pointer-events: none;
          z-index: 0;
        }

        .chapter-marker-line {
          width: 1px;
          height: 100%;
          background: rgba(59, 130, 246, 0.3);
        }

        .chapter-marker-label {
          position: absolute;
          top: -20px;
          left: 0;
          transform: translateX(-50%);
          font-size: 0.625rem;
          color: rgba(59, 130, 246, 0.6);
          white-space: nowrap;
          font-weight: 500;
        }

        .timeline-event {
          position: absolute;
          top: 50%;
          transform: translate(-50%, -50%);
          cursor: pointer;
          z-index: 10;
        }

        .timeline-event:hover .event-actions {
          opacity: 1;
        }

        .event-marker {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          border: 3px solid #1a1a1a;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.75rem;
        }

        .event-label {
          position: absolute;
          top: -30px;
          left: 50%;
          transform: translateX(-50%);
          white-space: nowrap;
          font-size: 0.75rem;
          color: #9ca3af;
          background: #0f0f0f;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
        }

        .event-actions {
          position: absolute;
          top: 30px;
          left: 50%;
          transform: translateX(-50%);
          display: flex;
          gap: 0.25rem;
          opacity: 0;
          transition: opacity 0.2s;
        }

        .event-actions button {
          padding: 0.25rem;
          background: #2a2a2a;
          border: none;
          border-radius: 4px;
          color: #fff;
          cursor: pointer;
          transition: all 0.2s;
        }

        .event-actions button:hover {
          background: #3a3a3a;
        }

        .timeline-empty {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 400px;
          color: #6b7280;
        }

        .btn-primary {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          background: #3b82f6;
          color: #fff;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.875rem;
        }

        .btn-primary:hover {
          background: #2563eb;
        }
      `}</style>
    </div>
  );
};
