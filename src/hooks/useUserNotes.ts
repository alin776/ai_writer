import { useState, useEffect, useCallback } from 'react';

// 用户备注存储 key 前缀
const USER_NOTE_PREFIX = 'user_note_';

// 全局事件名（用于跨组件同步备注更新）
const USER_NOTE_CHANGED_EVENT = 'userNoteChanged';

/**
 * 用户备注管理 Hook
 * 支持跨组件同步备注更新
 */
export function useUserNotes() {
  const [notes, setNotes] = useState<Record<string, string>>({});

  // 初始化加载所有备注
  useEffect(() => {
    const loadedNotes: Record<string, string> = {};
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith(USER_NOTE_PREFIX)) {
        const userId = key.replace(USER_NOTE_PREFIX, '');
        const note = localStorage.getItem(key);
        if (note) {
          loadedNotes[userId] = note;
        }
      }
    }
    setNotes(loadedNotes);
  }, []);

  // 监听其他组件的备注更新
  useEffect(() => {
    const handleNoteChange = (event: CustomEvent<{ userId: string; note: string | null }>) => {
      const { userId, note } = event.detail;
      setNotes(prev => {
        if (note) {
          return { ...prev, [userId]: note };
        } else {
          const newNotes = { ...prev };
          delete newNotes[userId];
          return newNotes;
        }
      });
    };

    window.addEventListener(USER_NOTE_CHANGED_EVENT, handleNoteChange as EventListener);
    return () => {
      window.removeEventListener(USER_NOTE_CHANGED_EVENT, handleNoteChange as EventListener);
    };
  }, []);

  // 获取用户备注
  const getNote = useCallback((userId: string): string | null => {
    return notes[userId] || null;
  }, [notes]);

  // 设置用户备注
  const setNote = useCallback((userId: string, note: string) => {
    const trimmedNote = note.trim();
    if (trimmedNote) {
      localStorage.setItem(`${USER_NOTE_PREFIX}${userId}`, trimmedNote);
      setNotes(prev => ({ ...prev, [userId]: trimmedNote }));
    } else {
      localStorage.removeItem(`${USER_NOTE_PREFIX}${userId}`);
      setNotes(prev => {
        const newNotes = { ...prev };
        delete newNotes[userId];
        return newNotes;
      });
    }

    // 触发全局事件通知其他组件
    window.dispatchEvent(new CustomEvent(USER_NOTE_CHANGED_EVENT, {
      detail: { userId, note: trimmedNote || null }
    }));
  }, []);

  // 获取显示名称（优先使用备注，否则使用原始名称）
  const getDisplayName = useCallback((userId: string, originalName: string): string => {
    return notes[userId] || originalName;
  }, [notes]);

  return {
    notes,
    getNote,
    setNote,
    getDisplayName,
  };
}

export default useUserNotes;
