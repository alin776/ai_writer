/**
 * Tab Identifier - 标签页唯一标识符工具
 *
 * 用途：
 * - 为每个浏览器标签页生成唯一ID
 * - 使用 sessionStorage 存储，标签页关闭后自动清除
 * - 解决跨标签页会话泄漏问题
 *
 * 原理：
 * - sessionStorage 是标签页级别隔离的
 * - 每个标签页有独立的 sessionStorage 空间
 * - 刷新页面后 tabId 保持不变（除非强制重新生成）
 */

const TAB_ID_KEY = 'agent_tab_id';
const TAB_CREATED_AT_KEY = 'agent_tab_created_at';

/**
 * 生成唯一的标签页ID
 */
function generateTabId(): string {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substr(2, 9);
  return `tab_${timestamp}_${random}`;
}

/**
 * 获取当前标签页的唯一ID
 *
 * @param forceNew 是否强制生成新的 tabId（默认 false）
 * @returns 标签页ID
 */
export function getTabId(forceNew: boolean = false): string {
  // 检查是否支持 sessionStorage
  if (typeof window === 'undefined' || !window.sessionStorage) {
    console.warn('[TabIdentifier] sessionStorage not available, using fallback');
    return `tab_fallback_${Date.now()}`;
  }

  try {
    // 如果强制生成新ID，清除旧的
    if (forceNew) {
      sessionStorage.removeItem(TAB_ID_KEY);
      sessionStorage.removeItem(TAB_CREATED_AT_KEY);
    }

    // 尝试从 sessionStorage 读取
    let tabId = sessionStorage.getItem(TAB_ID_KEY);

    if (!tabId) {
      // 首次访问，生成新的 tabId
      tabId = generateTabId();
      sessionStorage.setItem(TAB_ID_KEY, tabId);
      sessionStorage.setItem(TAB_CREATED_AT_KEY, new Date().toISOString());

      console.log('[TabIdentifier] 新标签页创建:', {
        tabId,
        createdAt: new Date().toISOString()
      });
    }

    return tabId;
  } catch (error) {
    console.error('[TabIdentifier] Failed to get/set tabId:', error);
    return `tab_error_${Date.now()}`;
  }
}

/**
 * 获取标签页创建时间
 *
 * @returns ISO 时间字符串，如果不存在返回 null
 */
export function getTabCreatedAt(): string | null {
  if (typeof window === 'undefined' || !window.sessionStorage) {
    return null;
  }

  try {
    return sessionStorage.getItem(TAB_CREATED_AT_KEY);
  } catch (error) {
    console.error('[TabIdentifier] Failed to get tab created time:', error);
    return null;
  }
}

/**
 * 检查是否是新标签页（创建时间小于10秒）
 *
 * @returns 是否是新标签页
 */
export function isNewTab(): boolean {
  const createdAt = getTabCreatedAt();
  if (!createdAt) return true;

  try {
    const createdTime = new Date(createdAt).getTime();
    const now = Date.now();
    const ageInSeconds = (now - createdTime) / 1000;

    return ageInSeconds < 10; // 10秒内认为是新标签页
  } catch (error) {
    return true;
  }
}

/**
 * 获取标签页年龄（秒）
 *
 * @returns 标签页存在的时长（秒），如果无法计算返回 null
 */
export function getTabAge(): number | null {
  const createdAt = getTabCreatedAt();
  if (!createdAt) return null;

  try {
    const createdTime = new Date(createdAt).getTime();
    const now = Date.now();
    return (now - createdTime) / 1000;
  } catch (error) {
    return null;
  }
}

/**
 * 重置标签页ID（用于测试或特殊场景）
 */
export function resetTabId(): string {
  return getTabId(true);
}

/**
 * 获取标签页信息（调试用）
 */
export function getTabInfo() {
  return {
    tabId: getTabId(),
    createdAt: getTabCreatedAt(),
    age: getTabAge(),
    isNew: isNewTab()
  };
}

// 调试模式：在控制台打印标签页信息
if (process.env.NODE_ENV === 'development') {
  if (typeof window !== 'undefined') {
    // 将工具函数挂载到 window 对象，方便调试
    (window as any).__tabDebug = {
      getTabInfo,
      getTabId,
      resetTabId,
      isNewTab,
      getTabAge
    };

    console.log('[TabIdentifier] 调试工具已挂载到 window.__tabDebug');
    console.log('[TabIdentifier] 当前标签页信息:', getTabInfo());
  }
}
