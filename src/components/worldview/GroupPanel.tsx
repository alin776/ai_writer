/**
 * 分组管理面板组件
 * 用于世界观关系图的节点分组管理
 */
import React, { useState } from 'react';
import { Plus, Folder, FolderOpen, Edit2, Trash2, Users, X } from 'lucide-react';
import type { EntityGroup, CreateEntityGroupData, GROUP_COLORS, GROUP_ICONS } from '@/types/group';
import type { Character, Location, Setting } from '@/types';

interface GroupPanelProps {
  workId: string;
  groups: EntityGroup[];
  characters: Character[];
  locations: Location[];
  settings: Setting[];
  onCreateGroup: (data: CreateEntityGroupData) => Promise<void>;
  onUpdateGroup: (groupId: string, data: any) => Promise<void>;
  onDeleteGroup: (groupId: string) => Promise<void>;
  onAddMembers: (groupId: string, members: any[]) => Promise<void>;
  onRemoveMember: (groupId: string, memberId: string) => Promise<void>;
}

export const GroupPanel: React.FC<GroupPanelProps> = ({
  workId,
  groups,
  characters,
  locations,
  settings,
  onCreateGroup,
  onUpdateGroup,
  onDeleteGroup,
  onAddMembers,
  onRemoveMember,
}) => {
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showAddMemberDialog, setShowAddMemberDialog] = useState(false);
  const [selectedGroupId, setSelectedGroupId] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'character' | 'location' | 'setting'>('character');
  const [selectedEntities, setSelectedEntities] = useState<Set<string>>(new Set());
  const [expandedGroups, setExpandedGroups] = useState<Set<string>>(new Set());
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    color: '#3b82f6',
    icon: '📁',
  });

  // 切换分组展开/折叠
  const toggleGroup = (groupId: string) => {
    setExpandedGroups(prev => {
      const next = new Set(prev);
      if (next.has(groupId)) {
        next.delete(groupId);
      } else {
        next.add(groupId);
      }
      return next;
    });
  };

  // 创建分组
  const handleCreateGroup = async () => {
    if (!formData.name.trim()) return;

    await onCreateGroup({
      workId,
      name: formData.name,
      description: formData.description || undefined,
      color: formData.color,
      icon: formData.icon,
      groupType: 'manual',
    });

    // 重置表单
    setFormData({
      name: '',
      description: '',
      color: '#3b82f6',
      icon: '📁',
    });
    setShowCreateDialog(false);
  };

  // 获取实体标签
  const getEntityLabel = (entityId: string, entityType: string): string => {
    if (entityType === 'character') {
      return characters.find(c => c.id === entityId)?.name || '未知角色';
    } else if (entityType === 'location') {
      return locations.find(l => l.id === entityId)?.name || '未知地点';
    } else if (entityType === 'setting') {
      return settings.find(s => s.id === entityId)?.title || '未知设定';
    }
    return '未知';
  };

  // 打开添加成员对话框
  const handleOpenAddMember = (groupId: string) => {
    setSelectedGroupId(groupId);
    setSelectedEntities(new Set());
    setActiveTab('character');
    setShowAddMemberDialog(true);
  };

  // 切换实体选择
  const handleToggleEntity = (entityId: string) => {
    setSelectedEntities(prev => {
      const next = new Set(prev);
      if (next.has(entityId)) {
        next.delete(entityId);
      } else {
        next.add(entityId);
      }
      return next;
    });
  };

  // 添加成员
  const handleAddMembers = async () => {
    if (selectedEntities.size === 0) return;

    const members = Array.from(selectedEntities).map(entityId => ({
      entityId,
      entityType: activeTab,
      orderIndex: 0,
    }));

    await onAddMembers(selectedGroupId, members);

    // 重置状态
    setShowAddMemberDialog(false);
    setSelectedEntities(new Set());
    setSelectedGroupId('');
  };

  // 获取当前标签页的实体列表
  const getCurrentEntities = () => {
    switch (activeTab) {
      case 'character':
        return characters;
      case 'location':
        return locations;
      case 'setting':
        return settings;
      default:
        return [];
    }
  };

  // 检查实体是否已在分组中
  const isEntityInGroup = (entityId: string): boolean => {
    const group = groups.find(g => g.id === selectedGroupId);
    return group?.members?.some(m => m.entityId === entityId) || false;
  };

  return (
    <div className="group-panel">
      {/* 头部 */}
      <div className="group-panel-header">
        <h3 className="text-sm font-medium text-gray-900 flex items-center gap-2">
          <Folder className="w-4 h-4" />
          分组管理
        </h3>
        <button
          onClick={() => setShowCreateDialog(true)}
          className="p-1 hover:bg-gray-100 rounded transition-colors"
          title="创建分组"
        >
          <Plus className="w-4 h-4 text-gray-600" />
        </button>
      </div>

      {/* 分组列表 */}
      <div className="group-list">
        {groups.length === 0 ? (
          <div className="empty-state">
            <Folder className="w-12 h-12 text-gray-400" />
            <p className="text-sm text-gray-400 mt-2">暂无分组</p>
            <button
              onClick={() => setShowCreateDialog(true)}
              className="mt-3 px-3 py-1.5 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
            >
              创建第一个分组
            </button>
          </div>
        ) : (
          groups.map(group => {
            const isExpanded = expandedGroups.has(group.id);
            return (
              <div key={group.id} className="group-item">
                {/* 分组头部 */}
                <div
                  className="group-item-header"
                  style={{ borderLeftColor: group.color }}
                >
                  <button
                    onClick={() => toggleGroup(group.id)}
                    className="flex-1 flex items-center gap-2 text-left"
                  >
                    {isExpanded ? (
                      <FolderOpen className="w-4 h-4" style={{ color: group.color }} />
                    ) : (
                      <Folder className="w-4 h-4" style={{ color: group.color }} />
                    )}
                    <span className="group-icon">{group.icon}</span>
                    <span className="group-name">{group.name}</span>
                    <span className="group-count">({group.members?.length || 0})</span>
                  </button>
                  
                  <div className="group-actions">
                    <button
                      onClick={() => {
                        // TODO: 实现编辑功能
                      }}
                      className="p-1 hover:bg-gray-700 rounded"
                      title="编辑分组"
                    >
                      <Edit2 className="w-3 h-3" />
                    </button>
                    <button
                      onClick={async () => {
                        if (confirm(`确定要删除分组"${group.name}"吗？`)) {
                          await onDeleteGroup(group.id);
                        }
                      }}
                      className="p-1 hover:bg-gray-100 rounded text-red-600"
                      title="删除分组"
                    >
                      <Trash2 className="w-3 h-3" />
                    </button>
                  </div>
                </div>

                {/* 分组成员 */}
                {isExpanded && (
                  <div className="group-members">
                    {group.members && group.members.length > 0 ? (
                      <>
                        {group.members.map(member => (
                          <div key={member.id} className="member-item">
                            <span className="member-type-icon">
                              {member.entityType === 'character' && '👤'}
                              {member.entityType === 'location' && '📍'}
                              {member.entityType === 'setting' && '📖'}
                            </span>
                            <span className="member-label">
                              {getEntityLabel(member.entityId, member.entityType)}
                            </span>
                            <button
                              onClick={async () => {
                                await onRemoveMember(group.id, member.id);
                              }}
                              className="member-remove"
                              title="移除"
                            >
                              <X className="w-3 h-3" />
                            </button>
                          </div>
                        ))}
                        <button
                          onClick={() => handleOpenAddMember(group.id)}
                          className="add-member-btn"
                        >
                          <Plus className="w-4 h-4" />
                          添加成员
                        </button>
                      </>
                    ) : (
                      <div className="empty-members">
                        <Users className="w-8 h-8 text-gray-400" />
                        <p className="text-xs text-gray-400 mt-1">暂无成员</p>
                        <button
                          onClick={() => handleOpenAddMember(group.id)}
                          className="add-member-btn-primary"
                        >
                          <Plus className="w-4 h-4" />
                          添加成员
                        </button>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* 创建分组对话框 */}
      {showCreateDialog && (
        <div className="dialog-overlay" onClick={() => setShowCreateDialog(false)}>
          <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
            <div className="dialog-header">
              <h3>创建分组</h3>
              <button onClick={() => setShowCreateDialog(false)}>
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="dialog-body">
              {/* 分组名称 */}
              <div className="form-field">
                <label>分组名称 *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="例如：主要角色、重要地点..."
                  className="form-input"
                  autoFocus
                />
              </div>

              {/* 分组描述 */}
              <div className="form-field">
                <label>分组描述</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="可选：描述这个分组的用途..."
                  className="form-textarea"
                  rows={2}
                />
              </div>

              {/* 颜色和图标 */}
              <div className="form-row">
                <div className="form-field">
                  <label>颜色</label>
                  <input
                    type="color"
                    value={formData.color}
                    onChange={(e) => setFormData({ ...formData, color: e.target.value })}
                    className="form-color"
                  />
                </div>
                <div className="form-field">
                  <label>图标</label>
                  <input
                    type="text"
                    value={formData.icon}
                    onChange={(e) => setFormData({ ...formData, icon: e.target.value })}
                    placeholder="📁"
                    className="form-input text-center"
                    maxLength={2}
                  />
                </div>
              </div>
            </div>

            <div className="dialog-footer">
              <button
                onClick={() => setShowCreateDialog(false)}
                className="btn-cancel"
              >
                取消
              </button>
              <button
                onClick={handleCreateGroup}
                disabled={!formData.name.trim()}
                className="btn-primary"
              >
                创建
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 添加成员对话框 */}
      {showAddMemberDialog && (
        <div className="dialog-overlay" onClick={() => setShowAddMemberDialog(false)}>
          <div className="dialog-content dialog-content-large" onClick={(e) => e.stopPropagation()}>
            <div className="dialog-header">
              <h3>添加成员</h3>
              <button onClick={() => setShowAddMemberDialog(false)}>
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="dialog-body">
              {/* 标签页 */}
              <div className="tabs">
                <button
                  onClick={() => setActiveTab('character')}
                  className={`tab ${activeTab === 'character' ? 'tab-active' : ''}`}
                >
                  👤 角色 ({characters.length})
                </button>
                <button
                  onClick={() => setActiveTab('location')}
                  className={`tab ${activeTab === 'location' ? 'tab-active' : ''}`}
                >
                  📍 地点 ({locations.length})
                </button>
                <button
                  onClick={() => setActiveTab('setting')}
                  className={`tab ${activeTab === 'setting' ? 'tab-active' : ''}`}
                >
                  📖 设定 ({settings.length})
                </button>
              </div>

              {/* 实体列表 */}
              <div className="entity-list">
                {getCurrentEntities().length > 0 ? (
                  getCurrentEntities().map((entity: any) => {
                    const entityId = entity.id;
                    const entityLabel = activeTab === 'setting' ? entity.title : entity.name;
                    const isChecked = selectedEntities.has(entityId);
                    const isInGroup = isEntityInGroup(entityId);

                    return (
                      <label
                        key={entityId}
                        className={`entity-item ${isInGroup ? 'entity-item-disabled' : ''}`}
                      >
                        <input
                          type="checkbox"
                          checked={isChecked}
                          disabled={isInGroup}
                          onChange={() => handleToggleEntity(entityId)}
                          className="entity-checkbox"
                        />
                        <span className="entity-icon">
                          {activeTab === 'character' && '👤'}
                          {activeTab === 'location' && '📍'}
                          {activeTab === 'setting' && '📖'}
                        </span>
                        <span className="entity-label">
                          {entityLabel}
                          {isInGroup && <span className="entity-badge">已在分组</span>}
                        </span>
                      </label>
                    );
                  })
                ) : (
                  <div className="empty-state">
                    <Users className="w-12 h-12 text-gray-400" />
                    <p className="text-sm text-gray-400 mt-2">暂无{
                      activeTab === 'character' ? '角色' :
                      activeTab === 'location' ? '地点' : '设定'
                    }</p>
                  </div>
                )}
              </div>
            </div>

            <div className="dialog-footer">
              <button
                onClick={() => setShowAddMemberDialog(false)}
                className="btn-cancel"
              >
                取消
              </button>
              <button
                onClick={handleAddMembers}
                disabled={selectedEntities.size === 0}
                className="btn-primary"
              >
                添加 ({selectedEntities.size})
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 样式 */}
      <style jsx>{`
        .group-panel {
          height: 100%;
          display: flex;
          flex-direction: column;
          background: #ffffff;
        }

        .group-panel-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 1rem;
          border-bottom: 1px solid #e5e7eb;
        }

        .group-list {
          flex: 1;
          overflow-y: auto;
          padding: 0.5rem;
        }

        .empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 300px;
          color: #9ca3af;
        }

        .group-item {
          margin-bottom: 0.5rem;
          background: #f9fafb;
          border-radius: 8px;
          overflow: hidden;
        }

        .group-item-header {
          display: flex;
          align-items: center;
          padding: 0.75rem;
          border-left: 3px solid #3b82f6;
          background: #f3f4f6;
        }

        .group-item-header button {
          background: none;
          border: none;
          color: #111827;
          cursor: pointer;
        }

        .group-icon {
          font-size: 1rem;
        }

        .group-name {
          font-size: 0.875rem;
          font-weight: 500;
          color: #111827;
        }

        .group-count {
          margin-left: auto;
          font-size: 0.75rem;
          color: #9ca3af;
        }

        .group-actions {
          display: flex;
          gap: 0.25rem;
          margin-left: 0.5rem;
        }

        .group-actions button {
          padding: 0.25rem;
          color: #9ca3af;
          transition: all 0.2s;
        }

        .group-actions button:hover {
          background: #e5e7eb;
        }

        .group-members {
          padding: 0.5rem;
        }

        .member-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem;
          margin-bottom: 0.25rem;
          background: #ffffff;
          border-radius: 4px;
          font-size: 0.875rem;
          color: #111827;
        }

        .member-type-icon {
          font-size: 1rem;
        }

        .member-label {
          flex: 1;
        }

        .member-remove {
          padding: 0.25rem;
          background: none;
          border: none;
          color: #9ca3af;
          cursor: pointer;
          opacity: 0;
          transition: all 0.2s;
        }

        .member-item:hover .member-remove {
          opacity: 1;
        }

        .member-remove:hover {
          color: #ef4444;
        }

        .empty-members {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 2rem 1rem;
          color: #9ca3af;
        }

        .dialog-overlay {
          position: fixed;
          inset: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
        }

        .dialog-content {
          background: #ffffff;
          border-radius: 12px;
          width: 90%;
          max-width: 500px;
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }

        .dialog-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 1.25rem;
          border-bottom: 1px solid #e5e7eb;
        }

        .dialog-header h3 {
          font-size: 1.125rem;
          font-weight: 600;
          color: #111827;
        }

        .dialog-header button {
          padding: 0.25rem;
          background: none;
          border: none;
          color: #9ca3af;
          cursor: pointer;
          transition: color 0.2s;
        }

        .dialog-header button:hover {
          color: #111827;
        }

        .dialog-body {
          padding: 1.25rem;
        }

        .form-field {
          margin-bottom: 1rem;
        }

        .form-field label {
          display: block;
          margin-bottom: 0.5rem;
          font-size: 0.875rem;
          font-weight: 500;
          color: #111827;
        }

        .form-input,
        .form-textarea {
          width: 100%;
          padding: 0.625rem;
          background: #f3f4f6;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          color: #111827;
          font-size: 0.875rem;
          transition: border-color 0.2s;
        }

        .form-input:focus,
        .form-textarea:focus {
          outline: none;
          border-color: #3b82f6;
        }

        .form-textarea {
          resize: vertical;
        }

        .form-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1rem;
        }

        .form-color {
          width: 100%;
          height: 40px;
          padding: 0.25rem;
          background: #f3f4f6;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          cursor: pointer;
        }

        .dialog-footer {
          display: flex;
          gap: 0.75rem;
          padding: 1rem 1.25rem;
          border-top: 1px solid #e5e7eb;
          justify-content: flex-end;
        }

        .btn-cancel,
        .btn-primary {
          padding: 0.625rem 1.25rem;
          border: none;
          border-radius: 6px;
          font-size: 0.875rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
        }

        .btn-cancel {
          background: #f3f4f6;
          color: #111827;
        }

        .btn-cancel:hover {
          background: #e5e7eb;
        }

        .btn-primary {
          background: #3b82f6;
          color: #ffffff;
        }

        .btn-primary:hover:not(:disabled) {
          background: #2563eb;
        }

        .btn-primary:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        /* 添加成员按钮 */
        .add-member-btn,
        .add-member-btn-primary {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          width: 100%;
          padding: 0.625rem;
          margin-top: 0.5rem;
          border: none;
          border-radius: 6px;
          font-size: 0.875rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
        }

        .add-member-btn {
          background: #f3f4f6;
          color: #9ca3af;
          border: 1px dashed #3a3a3a;
        }

        .add-member-btn:hover {
          background: #e5e7eb;
          color: #111827;
          border-color: #4a4a4a;
        }

        .add-member-btn-primary {
          background: #3b82f6;
          color: #ffffff;
          margin-top: 1rem;
        }

        .add-member-btn-primary:hover {
          background: #2563eb;
        }

        /* 更大的对话框 */
        .dialog-content-large {
          max-width: 600px;
          max-height: 80vh;
        }

        /* 标签页 */
        .tabs {
          display: flex;
          gap: 0.5rem;
          margin-bottom: 1rem;
          border-bottom: 2px solid #2a2a2a;
        }

        .tab {
          padding: 0.75rem 1rem;
          background: none;
          border: none;
          border-bottom: 2px solid transparent;
          color: #9ca3af;
          font-size: 0.875rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          margin-bottom: -2px;
        }

        .tab:hover {
          color: #111827;
          background: #f3f4f6;
        }

        .tab-active {
          color: #3b82f6;
          border-bottom-color: #3b82f6;
        }

        /* 实体列表 */
        .entity-list {
          max-height: 400px;
          overflow-y: auto;
          padding: 0.5rem;
          background: #f9fafb;
          border-radius: 8px;
        }

        .entity-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.75rem;
          margin-bottom: 0.25rem;
          background: #ffffff;
          border-radius: 6px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .entity-item:hover:not(.entity-item-disabled) {
          background: #f3f4f6;
        }

        .entity-item-disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .entity-checkbox {
          width: 18px;
          height: 18px;
          cursor: pointer;
          accent-color: #3b82f6;
        }

        .entity-checkbox:disabled {
          cursor: not-allowed;
        }

        .entity-icon {
          font-size: 1.25rem;
        }

        .entity-label {
          flex: 1;
          font-size: 0.875rem;
          color: #111827;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .entity-badge {
          padding: 0.125rem 0.5rem;
          background: #374151;
          color: #9ca3af;
          font-size: 0.75rem;
          border-radius: 4px;
        }
      `}</style>
    </div>
  );
};
