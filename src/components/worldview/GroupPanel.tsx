import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Plus, Edit, Trash2, Users, ChevronDown, X, UserPlus } from 'lucide-react';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import type { EntityGroup, CreateEntityGroupData } from '@/types/group';
import type { Character, Location, Setting } from '@/types/novel';

interface GroupPanelProps {
  workId: string;
  groups: EntityGroup[];
  characters: Character[];
  locations: Location[];
  settings: Setting[];
  onCreateGroup: (data: CreateEntityGroupData) => Promise<void>;
  onUpdateGroup: (groupId: string, data: Partial<CreateEntityGroupData>) => Promise<void>;
  onDeleteGroup: (groupId: string) => Promise<void>;
  onAddMembers: (groupId: string, members: { entityId: string; entityType: 'character' | 'location' | 'setting' }[]) => Promise<void>;
  onRemoveMember: (groupId: string, memberId: string) => Promise<void>;
}

interface Entity {
  id: string;
  name?: string;
  title?: string;
}

export function GroupPanel({
  workId,
  groups,
  characters,
  locations,
  settings,
  onCreateGroup,
  onUpdateGroup,
  onDeleteGroup,
  onAddMembers,
  onRemoveMember
}: GroupPanelProps) {
  const [expandedGroupId, setExpandedGroupId] = useState<string | null>(null);

  // 创建分组表单
  const [isCreating, setIsCreating] = useState(false);
  const [createFormData, setCreateFormData] = useState({ name: '', description: '', color: '#3b82f6' });

  // 编辑分组对话框
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editingGroup, setEditingGroup] = useState<EntityGroup | null>(null);
  const [editFormData, setEditFormData] = useState({ name: '', description: '', color: '#3b82f6' });

  // 添加成员对话框
  const [addMemberDialogOpen, setAddMemberDialogOpen] = useState(false);
  const [addMemberGroupId, setAddMemberGroupId] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'character' | 'location' | 'setting'>('character');
  const [selectedEntityIds, setSelectedEntityIds] = useState<string[]>([]);

  // 合并所有实体
  const allEntities: (Entity & { type: 'character' | 'location' | 'setting' })[] = [
    ...characters.map(c => ({ ...c, type: 'character' as const })),
    ...locations.map(l => ({ ...l, type: 'location' as const })),
    ...settings.map(s => ({ ...s, type: 'setting' as const }))
  ];

  const toggleGroup = (groupId: string) => {
    setExpandedGroupId(expandedGroupId === groupId ? null : groupId);
  };

  const getMemberEntity = (memberId: string) => {
    return allEntities.find(e => e.id === memberId);
  };

  const getAvailableEntities = (group: EntityGroup) => {
    return allEntities.filter(e => !group.members?.some(m => m.entityId === e.id));
  };

  // 打开创建表单
  const handleOpenCreateForm = () => {
    setCreateFormData({ name: '', description: '', color: '#3b82f6' });
    setIsCreating(true);
  };

  // 取消创建
  const handleCancelCreate = () => {
    setIsCreating(false);
    setCreateFormData({ name: '', description: '', color: '#3b82f6' });
  };

  // 提交创建分组
  const handleSubmitCreate = async () => {
    if (!createFormData.name.trim()) return;
    await onCreateGroup({
      workId,
      name: createFormData.name,
      description: createFormData.description || undefined,
      color: createFormData.color,
      groupType: 'manual'
    });
    setIsCreating(false);
    setCreateFormData({ name: '', description: '', color: '#3b82f6' });
  };

  // 打开编辑对话框
  const handleOpenEditDialog = (group: EntityGroup) => {
    setEditingGroup(group);
    setEditFormData({
      name: group.name,
      description: group.description || '',
      color: group.color || '#3b82f6'
    });
    setEditDialogOpen(true);
  };

  // 提交编辑分组
  const handleSubmitEdit = async () => {
    if (!editingGroup || !editFormData.name.trim()) return;
    await onUpdateGroup(editingGroup.id, editFormData);
    setEditDialogOpen(false);
  };

  // 打开添加成员对话框
  const handleOpenAddMemberDialog = (groupId: string) => {
    setAddMemberGroupId(groupId);
    setSelectedEntityIds([]);
    setActiveTab('character');
    setAddMemberDialogOpen(true);
  };

  // 提交添加成员
  const handleSubmitAddMember = async () => {
    if (selectedEntityIds.length === 0) return;
    const members = selectedEntityIds.map(entityId => {
      const entity = allEntities.find(e => e.id === entityId);
      return {
        entityId,
        entityType: entity?.type || 'character',
        orderIndex: 0
      };
    });
    await onAddMembers(addMemberGroupId, members);
    setAddMemberDialogOpen(false);
  };

  // 切换实体选择
  const toggleEntitySelection = (entityId: string) => {
    setSelectedEntityIds(prev =>
      prev.includes(entityId)
        ? prev.filter(id => id !== entityId)
        : [...prev, entityId]
    );
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
    const group = groups.find(g => g.id === addMemberGroupId);
    return group?.members?.some(m => m.entityId === entityId) || false;
  };

  const predefinedColors = [
    '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6',
    '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'
  ];

  return (
    <div className="flex flex-col h-full text-sm">
      {/* 顶部操作栏 */}
      <div className="p-3 border-b border-border-light">
        <Button onClick={handleOpenCreateForm} className="w-full shadow-sm h-8 text-sm">
          <Plus className="w-3.5 h-3.5 mr-1.5" />
          创建分组
        </Button>
      </div>

      {/* 创建分组表单 */}
      {isCreating && (
        <div className="p-4 border-b border-border-light bg-accent/10 space-y-3.5 animate-in slide-in-from-top-2 duration-200">
          <div className="space-y-2">
            <Label htmlFor="create-name" className="text-xs text-muted-foreground">
              分组名称 <span className="text-destructive">*</span>
            </Label>
            <Input
              id="create-name"
              value={createFormData.name}
              onChange={(e) => setCreateFormData({ ...createFormData, name: e.target.value })}
              placeholder="输入分组名称"
              className="h-9 text-sm bg-background/80 transition-colors shadow-none"
              autoFocus
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="create-description" className="text-xs text-muted-foreground">
              描述
            </Label>
            <Textarea
              id="create-description"
              value={createFormData.description}
              onChange={(e) => setCreateFormData({ ...createFormData, description: e.target.value })}
              placeholder="输入分组描述（可选）"
              rows={2}
              className="text-sm resize-none bg-background/80 transition-colors"
            />
          </div>
          <div className="space-y-2">
            <Label className="text-xs text-muted-foreground">
              颜色标识
            </Label>
            <div className="flex gap-2">
              {predefinedColors.map(color => (
                <button
                  key={color}
                  type="button"
                  onClick={() => setCreateFormData({ ...createFormData, color })}
                  className={`w-7 h-7 rounded-full transition-all ${
                    createFormData.color === color
                      ? 'scale-110'
                      : 'hover:scale-105 opacity-60'
                  }`}
                  style={{ backgroundColor: color }}
                />
              ))}
            </div>
          </div>
          <div className="flex gap-2 pt-1">
            <Button
              variant="outline"
              size="sm"
              onClick={handleCancelCreate}
              className="flex-1 h-8 text-xs"
            >
              <X className="w-3 h-3 mr-1" />
              取消
            </Button>
            <Button
              size="sm"
              onClick={handleSubmitCreate}
              disabled={!createFormData.name.trim()}
              className="flex-1 h-8 text-xs"
            >
              <Plus className="w-3 h-3 mr-1" />
              创建
            </Button>
          </div>
        </div>
      )}

      {/* 分组列表 */}
      <ScrollArea className="flex-1 custom-scrollbar">
        <div className="p-3 space-y-2">
          {groups.length === 0 ? (
            <div className="text-center text-muted-foreground py-10">
              <div className="w-12 h-12 mx-auto mb-3 rounded-full bg-accent flex items-center justify-center">
                <Users className="w-6 h-6 text-muted-foreground/50" />
              </div>
              <p className="text-xs">暂无分组</p>
              <p className="mt-1 text-xs">点击上方按钮创建分组</p>
            </div>
          ) : (
            groups.map(group => {
              const isExpanded = expandedGroupId === group.id;
              return (
                <div
                  key={group.id}
                  className="rounded-md hover:bg-accent/40 transition-all duration-200 bg-muted/20 hover:shadow-[0_1px_3px_rgba(0,0,0,0.06)] group"
                >
                  <div className="p-3">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2 flex-1">
                        {group.color && (
                          <div
                            className="w-3 h-3 rounded-full flex-shrink-0 ring-2 ring-offset-1 ring-offset-white"
                            style={{
                              backgroundColor: group.color,
                              boxShadow: `0 0 0 2px ${group.color}33`,
                            }}
                          />
                        )}
                        <span className="truncate text-foreground text-sm">{group.name}</span>
                      </div>
                      <div className="flex gap-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => toggleGroup(group.id)}
                          className="h-6 w-6 p-0 opacity-0 group-hover:opacity-100 transition-all"
                        >
                          <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isExpanded ? '' : '-rotate-90'}`} />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleOpenEditDialog(group)}
                          className="h-6 w-6 p-0 opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          <Edit className="w-3 h-3" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => onDeleteGroup(group.id)}
                          className="h-6 w-6 p-0 hover:text-destructive opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          <Trash2 className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                    {group.description && (
                      <p className="text-muted-foreground text-xs mb-2">{group.description}</p>
                    )}
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary" className="shadow-sm h-4 text-xs">
                        {group.members?.length || 0} 个成员
                      </Badge>
                    </div>
                  </div>

                  {/* 成员列表 */}
                  {isExpanded && (
                    <div className="border-t border-border-light px-3 pb-3 pt-2 space-y-1 bg-accent/20">
                      {(!group.members || group.members.length === 0) ? (
                        <div className="text-center text-muted-foreground py-4 text-xs">
                          暂无成员
                        </div>
                      ) : (
                        group.members.map(member => {
                          const entity = getMemberEntity(member.entityId);
                          if (!entity) return null;
                          const entityName = entity.name || entity.title || '未知';
                          return (
                            <div
                              key={member.id}
                              className="flex items-center justify-between p-2 rounded hover:bg-background/50 transition-colors group/member"
                            >
                              <span className="text-xs text-foreground truncate flex-1">{entityName}</span>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => onRemoveMember(group.id, member.id)}
                                className="h-5 w-5 p-0 opacity-0 group-hover/member:opacity-100 transition-opacity hover:text-destructive"
                              >
                                <X className="w-3 h-3" />
                              </Button>
                            </div>
                          );
                        })
                      )}

                      {/* 添加成员按钮 */}
                      {getAvailableEntities(group).length > 0 && (
                        <div className="pt-1">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleOpenAddMemberDialog(group.id)}
                            className="w-full h-7 text-xs"
                          >
                            <UserPlus className="w-3 h-3 mr-1.5" />
                            添加成员
                          </Button>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      </ScrollArea>

      {/* 编辑分组对话框 */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>编辑分组</DialogTitle>
            <DialogDescription>
              修改分组的名称、描述和颜色
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="edit-name">分组名称 *</Label>
              <Input
                id="edit-name"
                value={editFormData.name}
                onChange={(e) => setEditFormData({ ...editFormData, name: e.target.value })}
                placeholder="输入分组名称"
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="edit-description">描述</Label>
              <Textarea
                id="edit-description"
                value={editFormData.description}
                onChange={(e) => setEditFormData({ ...editFormData, description: e.target.value })}
                placeholder="输入分组描述（可选）"
                rows={3}
              />
            </div>
            <div className="grid gap-2">
              <Label>颜色标识</Label>
              <div className="flex gap-2">
                {predefinedColors.map(color => (
                  <button
                    key={color}
                    type="button"
                    onClick={() => setEditFormData({ ...editFormData, color })}
                    className={`w-8 h-8 rounded-full transition-all ${
                      editFormData.color === color
                        ? 'ring-2 ring-offset-2 ring-primary scale-110'
                        : 'hover:scale-105'
                    }`}
                    style={{ backgroundColor: color }}
                  />
                ))}
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditDialogOpen(false)}>
              取消
            </Button>
            <Button onClick={handleSubmitEdit} disabled={!editFormData.name.trim()}>
              保存
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* 添加成员对话框 */}
      <Dialog open={addMemberDialogOpen} onOpenChange={setAddMemberDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>添加成员</DialogTitle>
            <DialogDescription>
              选择要添加到分组的实体
            </DialogDescription>
          </DialogHeader>

          {/* 标签页 */}
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('character')}
              className={`flex-1 py-2 text-sm font-medium transition-colors ${
                activeTab === 'character'
                  ? 'border-b-2 border-primary text-primary'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              角色 ({characters.length})
            </button>
            <button
              onClick={() => setActiveTab('location')}
              className={`flex-1 py-2 text-sm font-medium transition-colors ${
                activeTab === 'location'
                  ? 'border-b-2 border-primary text-primary'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              地点 ({locations.length})
            </button>
            <button
              onClick={() => setActiveTab('setting')}
              className={`flex-1 py-2 text-sm font-medium transition-colors ${
                activeTab === 'setting'
                  ? 'border-b-2 border-primary text-primary'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              设定 ({settings.length})
            </button>
          </div>

          <ScrollArea className="max-h-[300px] py-4">
            <div className="space-y-2 pr-4">
              {getCurrentEntities().length === 0 ? (
                <div className="text-center text-muted-foreground py-8 text-sm">
                  没有可添加的{activeTab === 'character' ? '角色' : activeTab === 'location' ? '地点' : '设定'}
                </div>
              ) : (
                getCurrentEntities().map((entity: any) => {
                  const entityId = entity.id;
                  const entityName = activeTab === 'setting' ? entity.title : entity.name;
                  const isInGroup = isEntityInGroup(entityId);

                  return (
                    <div
                      key={entityId}
                      className={`flex items-center space-x-3 p-2 rounded hover:bg-accent cursor-pointer ${
                        isInGroup ? 'opacity-50 cursor-not-allowed' : ''
                      }`}
                      onClick={() => !isInGroup && toggleEntitySelection(entityId)}
                    >
                      <Checkbox
                        checked={selectedEntityIds.includes(entityId)}
                        onCheckedChange={() => !isInGroup && toggleEntitySelection(entityId)}
                        disabled={isInGroup}
                      />
                      <div className="flex-1">
                        <div className="text-sm">{entityName}</div>
                        <div className="text-xs text-muted-foreground">
                          {activeTab === 'character' && '角色'}
                          {activeTab === 'location' && '地点'}
                          {activeTab === 'setting' && '设定'}
                          {isInGroup && ' • 已在分组'}
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </ScrollArea>
          <DialogFooter>
            <Button variant="outline" onClick={() => setAddMemberDialogOpen(false)}>
              取消
            </Button>
            <Button
              onClick={handleSubmitAddMember}
              disabled={selectedEntityIds.length === 0}
            >
              添加 ({selectedEntityIds.length})
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
