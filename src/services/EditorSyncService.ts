/**
 * 编辑器同步服务 - 事件总线 + 乐观更新
 * 使用浏览器兼容的简单事件系统
 */
import { DataService } from './DataService';

export interface EditorUpdateEvent {
  chapterId: string;
  content: string;
  operation: 'append' | 'replace' | 'insert';
  position?: { start: number; end: number };
  version: number;
  source: 'agent' | 'user' | 'sync';
}

type EventCallback<T = any> = (data: T) => void;

class EditorSyncService {
  private pendingUpdates: Map<string, EditorUpdateEvent[]> = new Map();
  private syncTimers: Map<string, NodeJS.Timeout> = new Map();
  private syncDelay: number = 1000; // 1秒防抖

  // 简单的事件监听器存储
  private listeners: Map<string, Set<EventCallback>> = new Map();

  /**
   * 乐观更新 - 立即更新UI，后台同步数据库
   */
  optimisticUpdate(event: EditorUpdateEvent) {
    // 1. 立即触发UI更新
    this.emit('chapter-updated', event);

    // 2. 记录待同步的更新
    const updates = this.pendingUpdates.get(event.chapterId) || [];
    updates.push(event);
    this.pendingUpdates.set(event.chapterId, updates);

    // 3. 防抖同步到后端
    this.debouncedSync(event.chapterId);
  }

  private debouncedSync(chapterId: string) {
    // 清除之前的定时器
    const existing = this.syncTimers.get(chapterId);
    if (existing) clearTimeout(existing);

    // 设置新的防抖定时器
    const timer = setTimeout(async () => {
      await this.syncToBackend(chapterId);
    }, this.syncDelay);

    this.syncTimers.set(chapterId, timer);
  }

  private async syncToBackend(chapterId: string) {
    const updates = this.pendingUpdates.get(chapterId);
    if (!updates || updates.length === 0) return;

    try {
      // 合并所有更新，只同步最终状态
      const finalUpdate = updates[updates.length - 1];

      await DataService.updateChapter(chapterId, {
        content: finalUpdate.content
      });

      // 清除已同步的更新
      this.pendingUpdates.delete(chapterId);

      // 触发同步成功事件
      this.emit('sync-success', { chapterId });

    } catch (error) {
      console.error('[EditorSync] 同步失败:', error);
      this.emit('sync-error', { chapterId, error });
    }
  }

  /**
   * 订阅章节更新
   */
  onUpdate(callback: (event: EditorUpdateEvent) => void): () => void {
    return this.on('chapter-updated', callback);
  }

  /**
   * 订阅同步错误
   */
  onSyncError(callback: (data: { chapterId: string; error: any }) => void): () => void {
    return this.on('sync-error', callback);
  }

  /**
   * 订阅同步成功
   */
  onSyncSuccess(callback: (data: { chapterId: string }) => void): () => void {
    return this.on('sync-success', callback);
  }

  /**
   * 强制立即同步
   */
  async forceSync(chapterId: string) {
    // 清除防抖定时器
    const timer = this.syncTimers.get(chapterId);
    if (timer) {
      clearTimeout(timer);
      this.syncTimers.delete(chapterId);
    }

    // 立即同步
    await this.syncToBackend(chapterId);
  }

  /**
   * 清除指定章节的待同步更新
   */
  clearPendingUpdates(chapterId: string) {
    this.pendingUpdates.delete(chapterId);
    const timer = this.syncTimers.get(chapterId);
    if (timer) {
      clearTimeout(timer);
      this.syncTimers.delete(chapterId);
    }
  }

  /**
   * 获取待同步更新数量
   */
  getPendingCount(chapterId: string): number {
    return this.pendingUpdates.get(chapterId)?.length || 0;
  }

  /**
   * 设置同步延迟
   */
  setSyncDelay(delay: number) {
    this.syncDelay = delay;
  }

  /**
   * 销毁服务
   */
  destroy() {
    // 清除所有定时器
    this.syncTimers.forEach(timer => clearTimeout(timer));
    this.syncTimers.clear();
    this.pendingUpdates.clear();
    this.listeners.clear();
  }

  // ==================== 简单的事件系统 ====================

  /**
   * 监听事件
   */
  private on(event: string, callback: EventCallback): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);

    // 返回取消订阅函数
    return () => this.off(event, callback);
  }

  /**
   * 取消监听
   */
  private off(event: string, callback: EventCallback) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.delete(callback);
    }
  }

  /**
   * 触发事件
   */
  private emit(event: string, data?: any) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`[EditorSync] Error in event handler for "${event}":`, error);
        }
      });
    }
  }
}

// 单例导出
export const editorSyncService = new EditorSyncService();
export default editorSyncService;
