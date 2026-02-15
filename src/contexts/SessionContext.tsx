/**
 * SessionContext - 会话上下文管理
 *
 * 功能:
 * - 为每个标签页提供独立的会话上下文
 * - 管理 SessionStateManager 实例
 * - 提供会话状态和操作方法
 */

import React, { createContext, useContext, useEffect, useMemo } from 'react';
import { SessionStateManager } from '@/hooks/SessionStateManager';

interface SessionContextValue {
  sessionId: string;
  sessionManager: SessionStateManager;
}

const SessionContext = createContext<SessionContextValue | null>(null);

// 全局单例 SessionStateManager（跨所有标签页共享）
let globalSessionManager: SessionStateManager | null = null;

function getGlobalSessionManager(): SessionStateManager {
  if (!globalSessionManager) {
    globalSessionManager = new SessionStateManager();
    console.log('[SessionContext] 创建全局 SessionStateManager');
  }
  return globalSessionManager;
}

interface SessionProviderProps {
  sessionId: string;
  children: React.ReactNode;
}

export const SessionProvider: React.FC<SessionProviderProps> = ({ sessionId, children }) => {
  const sessionManager = useMemo(() => getGlobalSessionManager(), []);

  // 设置当前活跃会话
  useEffect(() => {
    sessionManager.setActiveSession(sessionId);
    console.log('[SessionContext] 设置活跃会话:', sessionId);

    return () => {
      console.log('[SessionContext] 会话卸载:', sessionId);
    };
  }, [sessionId, sessionManager]);

  const value = useMemo(() => ({
    sessionId,
    sessionManager
  }), [sessionId, sessionManager]);

  return (
    <SessionContext.Provider value={value}>
      {children}
    </SessionContext.Provider>
  );
};

export function useSessionContext(): SessionContextValue {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error('useSessionContext must be used within SessionProvider');
  }
  return context;
}

// 导出全局 SessionStateManager 访问函数（用于非 React 组件）
export { getGlobalSessionManager };
