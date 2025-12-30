/**
 * 频道 WebSocket Hook
 *
 * 用于频道实时消息推送、正在输入指示器、在线状态
 */

import { useEffect, useRef, useCallback, useState } from 'react';
import { useAuthStore } from '../store/authStore';

// 消息类型
export interface ChannelMessage {
  id: string;
  channel_id: string;
  user_id: string;
  content: string;
  type: string;
  is_pinned: boolean;
  reply_to_id: string | null;
  forwarded_from_id?: string | null;  // 转发来源消息ID
  reaction_count: number;
  created_at: string;
  user_name: string;
  user_avatar: string | null;
  user_honor: string | null;
  user_title: string | null;
  user_title_color: string | null;
  attachments?: {  // 附件列表（使用 camelCase）
    id: string;
    fileName: string;
    fileType: string;
    fileSize: number;
    fileUrl: string;
    thumbnailUrl?: string;
  }[];
}

export interface TypingUser {
  user_id: string;
  username: string;
  timestamp: number;
}

export interface ChannelWebSocketEvent {
  type: 'MESSAGE_NEW' | 'MESSAGE_DELETE' | 'MESSAGE_EDIT' | 'MESSAGE_PIN' | 'MESSAGE_UNPIN' | 'TYPING' | 'PRESENCE' | 'ONLINE_USERS' | 'REACTION_ADD' | 'REACTION_REMOVE' | 'heartbeat' | 'pong';
  payload?: any;
}

export interface ReactionEvent {
  message_id: string;
  emoji: string;
  user_id: string;
  username?: string;
}

export interface MessageEditEvent {
  channel_id: string;
  message_id: string;
  content: string;
  user_id: string;
  user_name: string;
  edited_at: string;
  is_edited: boolean;
}

export interface MessagePinEvent {
  message_id: string;
  pinned_by: string;
  pinned_by_name: string;
  pinned_at: string;
}

export interface MessageUnpinEvent {
  message_id: string;
  unpinned_by: string;
}

interface UseChannelWebSocketOptions {
  channelId: string | null;
  onMessage?: (message: ChannelMessage) => void;
  onMessageDelete?: (messageId: string) => void;
  onMessageEdit?: (event: MessageEditEvent) => void;
  onMessagePin?: (event: MessagePinEvent) => void;
  onMessageUnpin?: (event: MessageUnpinEvent) => void;
  onTyping?: (userId: string, username: string) => void;
  onPresence?: (userId: string, status: 'online' | 'offline') => void;
  onReactionAdd?: (event: ReactionEvent) => void;
  onReactionRemove?: (event: ReactionEvent) => void;
}

export const useChannelWebSocket = (options: UseChannelWebSocketOptions) => {
  const { channelId, onMessage, onMessageDelete, onMessageEdit, onMessagePin, onMessageUnpin, onTyping, onPresence, onReactionAdd, onReactionRemove } = options;

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const heartbeatIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;

  // 使用 ref 存储回调，避免依赖变化导致重连
  const callbacksRef = useRef({ onMessage, onMessageDelete, onMessageEdit, onMessagePin, onMessageUnpin, onTyping, onPresence, onReactionAdd, onReactionRemove });
  useEffect(() => {
    callbacksRef.current = { onMessage, onMessageDelete, onMessageEdit, onMessagePin, onMessageUnpin, onTyping, onPresence, onReactionAdd, onReactionRemove };
  }, [onMessage, onMessageDelete, onMessageEdit, onMessagePin, onMessageUnpin, onTyping, onPresence, onReactionAdd, onReactionRemove]);

  const [isConnected, setIsConnected] = useState(false);
  const [typingUsers, setTypingUsers] = useState<TypingUser[]>([]);
  const [onlineUsers, setOnlineUsers] = useState<string[]>([]);

  const token = useAuthStore((state) => state.token);
  const user = useAuthStore((state) => state.user);

  // 清理 typing 用户（3秒超时）
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      setTypingUsers(prev => prev.filter(u => now - u.timestamp < 3000));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // 连接 WebSocket
  const connect = useCallback(() => {
    if (!channelId || !token) return;

    // 清理旧连接
    if (wsRef.current) {
      wsRef.current.close();
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/api/v1/ws/channels/${channelId}?token=${token}`;

    console.log('[Channel WS] 连接中...', channelId);
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('[Channel WS] 连接成功');
      setIsConnected(true);
      reconnectAttempts.current = 0;

      // 心跳
      heartbeatIntervalRef.current = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'ping' }));
        }
      }, 25000);
    };

    ws.onmessage = (event) => {
      try {
        const data: ChannelWebSocketEvent = JSON.parse(event.data);

        switch (data.type) {
          case 'MESSAGE_NEW':
            if (data.payload && callbacksRef.current.onMessage) {
              callbacksRef.current.onMessage(data.payload);
            }
            break;

          case 'MESSAGE_DELETE':
            if (data.payload?.message_id && callbacksRef.current.onMessageDelete) {
              callbacksRef.current.onMessageDelete(data.payload.message_id);
            }
            break;

          case 'MESSAGE_EDIT':
            if (data.payload && callbacksRef.current.onMessageEdit) {
              callbacksRef.current.onMessageEdit(data.payload);
            }
            break;

          case 'TYPING':
            if (data.payload) {
              const { user_id, username } = data.payload;
              if (callbacksRef.current.onTyping) callbacksRef.current.onTyping(user_id, username);
              // 更新 typing 用户列表
              setTypingUsers(prev => {
                const filtered = prev.filter(u => u.user_id !== user_id);
                return [...filtered, { user_id, username, timestamp: Date.now() }];
              });
            }
            break;

          case 'PRESENCE':
            if (data.payload) {
              const { user_id, status } = data.payload;
              if (callbacksRef.current.onPresence) callbacksRef.current.onPresence(user_id, status);
              // 更新在线用户列表
              setOnlineUsers(prev => {
                if (status === 'online') {
                  return prev.includes(user_id) ? prev : [...prev, user_id];
                } else {
                  return prev.filter(id => id !== user_id);
                }
              });
            }
            break;

          case 'ONLINE_USERS':
            // 初始化在线用户列表
            if (data.payload?.users) {
              setOnlineUsers(data.payload.users);
            }
            break;

          case 'REACTION_ADD':
            if (data.payload && callbacksRef.current.onReactionAdd) {
              callbacksRef.current.onReactionAdd(data.payload);
            }
            break;

          case 'REACTION_REMOVE':
            if (data.payload && callbacksRef.current.onReactionRemove) {
              callbacksRef.current.onReactionRemove(data.payload);
            }
            break;

          case 'MESSAGE_PIN':
            if (data.payload && callbacksRef.current.onMessagePin) {
              callbacksRef.current.onMessagePin(data.payload);
            }
            break;

          case 'MESSAGE_UNPIN':
            if (data.payload && callbacksRef.current.onMessageUnpin) {
              callbacksRef.current.onMessageUnpin(data.payload);
            }
            break;

          case 'heartbeat':
          case 'pong':
            // 忽略
            break;
        }
      } catch (error) {
        console.error('[Channel WS] 解析消息失败:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('[Channel WS] 错误:', error);
    };

    ws.onclose = (event) => {
      console.log('[Channel WS] 连接关闭:', event.code, event.reason);
      setIsConnected(false);

      // 清理心跳
      if (heartbeatIntervalRef.current) {
        clearInterval(heartbeatIntervalRef.current);
      }

      // 自动重连（非主动关闭且未超过最大重试次数）
      if (event.code !== 1000 && reconnectAttempts.current < maxReconnectAttempts) {
        const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 30000);
        console.log(`[Channel WS] ${delay}ms 后重连...`);
        reconnectTimeoutRef.current = setTimeout(() => {
          reconnectAttempts.current++;
          connect();
        }, delay);
      }
    };

    wsRef.current = ws;
  }, [channelId, token]); // 只依赖 channelId 和 token，回调通过 ref 获取

  // 断开连接
  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close(1000, 'Component unmounted');
      wsRef.current = null;
    }
    setIsConnected(false);
    setTypingUsers([]);
    setOnlineUsers([]);
  }, []);

  // 发送正在输入事件（节流）
  const lastTypingSent = useRef(0);
  const sendTyping = useCallback(() => {
    const now = Date.now();
    if (now - lastTypingSent.current < 1000) return; // 1秒节流

    if (wsRef.current?.readyState === WebSocket.OPEN && user) {
      wsRef.current.send(JSON.stringify({
        type: 'TYPING',
        username: user.username
      }));
      lastTypingSent.current = now;
    }
  }, [user]);

  // 频道变化时重新连接
  useEffect(() => {
    if (channelId && token) {
      connect();
    }
    return () => {
      disconnect();
    };
  }, [channelId, token, connect, disconnect]);

  return {
    isConnected,
    typingUsers,
    onlineUsers,
    sendTyping,
    disconnect
  };
};
