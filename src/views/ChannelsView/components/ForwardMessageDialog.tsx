/**
 * 消息转发对话框
 */
import { useState, useEffect } from 'react';
import { X, Forward, Search, Check, Loader2 } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import { channelApi, forwardMessage, getMyChannels, type Channel } from '@/services/channelApi';
import { useGlobalStore } from '@/store/globalStore';

interface ForwardMessageDialogProps {
  isOpen: boolean;
  onClose: () => void;
  sourceChannelId: string;
  messageId: string;
  messageContent: string;
  messageSender: string;
}

export function ForwardMessageDialog({
  isOpen,
  onClose,
  sourceChannelId,
  messageId,
  messageContent,
  messageSender,
}: ForwardMessageDialogProps) {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [selectedChannels, setSelectedChannels] = useState<Set<string>>(new Set());
  const [searchQuery, setSearchQuery] = useState('');
  const [comment, setComment] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isForwarding, setIsForwarding] = useState(false);
  const { success: showSuccess, error: showError, warning: showWarning } = useGlobalStore();

  // 加载可选频道
  useEffect(() => {
    if (isOpen) {
      loadChannels();
    }
  }, [isOpen]);

  const loadChannels = async () => {
    setIsLoading(true);
    try {
      const response = await getMyChannels();
      // 排除当前频道
      setChannels(response.channels.filter(c => c.id !== sourceChannelId));
    } catch (error) {
      console.error('加载频道列表失败:', error);
      showError('加载频道列表失败');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredChannels = channels.filter(channel =>
    channel.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const toggleChannel = (channelId: string) => {
    const newSelected = new Set(selectedChannels);
    if (newSelected.has(channelId)) {
      newSelected.delete(channelId);
    } else {
      if (newSelected.size >= 10) {
        showWarning('最多只能选择 10 个频道');
        return;
      }
      newSelected.add(channelId);
    }
    setSelectedChannels(newSelected);
  };

  const handleForward = async () => {
    if (selectedChannels.size === 0) {
      showWarning('请选择至少一个目标频道');
      return;
    }

    setIsForwarding(true);
    try {
      const response = await forwardMessage(sourceChannelId, messageId, {
        target_channel_ids: Array.from(selectedChannels),
        add_comment: comment || undefined,
      });

      if (response.forwarded_count > 0) {
        showSuccess(`成功转发到 ${response.forwarded_count} 个频道`);
      }
      if (response.failed_channels.length > 0) {
        showWarning(`${response.failed_channels.length} 个频道转发失败`);
      }

      onClose();
      setSelectedChannels(new Set());
      setComment('');
    } catch (error) {
      console.error('转发失败:', error);
      showError('转发失败，请稍后重试');
    } finally {
      setIsForwarding(false);
    }
  };

  const handleClose = () => {
    onClose();
    setSelectedChannels(new Set());
    setSearchQuery('');
    setComment('');
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Forward className="w-5 h-5" />
            转发消息
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {/* 消息预览 */}
          <div className="p-3 bg-gray-50 dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700">
            <div className="text-xs text-gray-500 dark:text-slate-400 mb-1">
              来自 {messageSender}
            </div>
            <div className="text-sm text-gray-700 dark:text-slate-300 line-clamp-3">
              {messageContent}
            </div>
          </div>

          {/* 添加评论 */}
          <div>
            <label className="text-sm text-gray-600 dark:text-slate-400 mb-1 block">
              添加评论（可选）
            </label>
            <Textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="写点什么..."
              className="resize-none h-16"
              maxLength={500}
            />
          </div>

          {/* 搜索频道 */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="搜索频道..."
              className="pl-9"
            />
          </div>

          {/* 频道列表 */}
          <ScrollArea className="h-64">
            {isLoading ? (
              <div className="flex items-center justify-center h-32">
                <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
              </div>
            ) : filteredChannels.length === 0 ? (
              <div className="text-center text-gray-500 dark:text-slate-400 py-8">
                {searchQuery ? '未找到匹配的频道' : '暂无可转发的频道'}
              </div>
            ) : (
              <div className="space-y-1">
                {filteredChannels.map((channel) => {
                  const isSelected = selectedChannels.has(channel.id);
                  return (
                    <button
                      key={channel.id}
                      onClick={() => toggleChannel(channel.id)}
                      className={cn(
                        "w-full flex items-center gap-3 p-2 rounded-lg transition-colors",
                        isSelected
                          ? "bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700"
                          : "hover:bg-gray-50 dark:hover:bg-slate-800"
                      )}
                    >
                      <Avatar className="w-8 h-8">
                        <AvatarImage src={channel.coverImage} />
                        <AvatarFallback className="text-xs">
                          {channel.name[0]}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1 text-left min-w-0">
                        <div className="text-sm font-medium truncate dark:text-slate-200">
                          {channel.name}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-slate-400">
                          {channel.type === 'official' ? '官方频道' :
                           channel.type === 'fangroup' ? '粉丝群' : '作品频道'}
                        </div>
                      </div>
                      {isSelected && (
                        <Check className="w-5 h-5 text-blue-500" />
                      )}
                    </button>
                  );
                })}
              </div>
            )}
          </ScrollArea>

          {/* 已选择计数 */}
          {selectedChannels.size > 0 && (
            <div className="text-sm text-gray-500 dark:text-slate-400">
              已选择 {selectedChannels.size} 个频道
            </div>
          )}

          {/* 操作按钮 */}
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={handleClose}>
              取消
            </Button>
            <Button
              onClick={handleForward}
              disabled={selectedChannels.size === 0 || isForwarding}
            >
              {isForwarding ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  转发中...
                </>
              ) : (
                <>
                  <Forward className="w-4 h-4 mr-2" />
                  转发 ({selectedChannels.size})
                </>
              )}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

export default ForwardMessageDialog;
