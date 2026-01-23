/**
 * localStorage 使用情况调试工具
 * 用于诊断存储配额问题
 */

interface StorageStats {
  key: string;
  size: number;
  sizeFormatted: string;
  percentage: number;
}

interface StorageSummary {
  total: number;
  totalFormatted: string;
  quota: number;
  quotaFormatted: string;
  usage: number;
  items: StorageStats[];
  largestItems: StorageStats[];
}

/**
 * 格式化字节数为可读格式
 */
function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
}

/**
 * 计算字符串的字节大小（UTF-8 编码）
 */
function getStringSize(str: string): number {
  return new Blob([str]).size;
}

/**
 * 获取 localStorage 配额（估算）
 * 大多数浏览器为 5-10MB
 */
function getStorageQuota(): number {
  // 估算配额为 10MB
  return 10 * 1024 * 1024;
}

/**
 * 分析 localStorage 使用情况
 */
export function analyzeLocalStorage(): StorageSummary {
  const items: StorageStats[] = [];
  let totalSize = 0;

  // 遍历所有 localStorage 项
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (!key) continue;

    const value = localStorage.getItem(key);
    if (!value) continue;

    // 计算大小（key + value）
    const size = getStringSize(key) + getStringSize(value);
    totalSize += size;

    items.push({
      key,
      size,
      sizeFormatted: formatBytes(size),
      percentage: 0, // 稍后计算
    });
  }

  // 计算百分比
  items.forEach((item) => {
    item.percentage = (item.size / totalSize) * 100;
  });

  // 按大小排序
  const sortedItems = [...items].sort((a, b) => b.size - a.size);
  const largestItems = sortedItems.slice(0, 10);

  const quota = getStorageQuota();

  return {
    total: totalSize,
    totalFormatted: formatBytes(totalSize),
    quota,
    quotaFormatted: formatBytes(quota),
    usage: (totalSize / quota) * 100,
    items: sortedItems,
    largestItems,
  };
}

/**
 * 打印 localStorage 使用情况到控制台
 */
export function printStorageStats(): void {
  const stats = analyzeLocalStorage();

  console.group('📊 localStorage 使用情况分析');
  console.log(`总使用量: ${stats.totalFormatted} / ${stats.quotaFormatted} (${stats.usage.toFixed(2)}%)`);
  console.log(`存储项数量: ${stats.items.length}`);
  console.log('');

  console.group('🔝 占用最大的 10 项:');
  stats.largestItems.forEach((item, index) => {
    console.log(
      `${index + 1}. ${item.key}:`,
      item.sizeFormatted,
      `(${item.percentage.toFixed(2)}%)`
    );
  });
  console.groupEnd();

  console.groupEnd();

  // 如果使用率超过 80%，显示警告
  if (stats.usage > 80) {
    console.warn(
      '⚠️ localStorage 使用率超过 80%，建议清理以下大项：',
      stats.largestItems.slice(0, 3).map((item) => item.key)
    );
  }
}

/**
 * 清理旧的 Agent 会话（保留最近的 N 个）
 */
export function cleanupOldAgentSessions(keepCount: number = 5): number {
  const SESSIONS_LIST_KEY = 'agent_conversation_sessions';
  const STORAGE_KEY_PREFIX = 'agent_conversation_';

  try {
    const stored = localStorage.getItem(SESSIONS_LIST_KEY);
    if (!stored) return 0;

    const sessions: string[] = JSON.parse(stored);
    const toDelete = sessions.slice(keepCount);

    toDelete.forEach((sessionId) => {
      localStorage.removeItem(`${STORAGE_KEY_PREFIX}${sessionId}`);
    });

    // 更新会话列表
    const kept = sessions.slice(0, keepCount);
    localStorage.setItem(SESSIONS_LIST_KEY, JSON.stringify(kept));

    console.log(`🧹 已清理 ${toDelete.length} 个旧的 Agent 会话`);
    return toDelete.length;
  } catch (error) {
    console.error('清理 Agent 会话失败:', error);
    return 0;
  }
}

/**
 * 清理编辑器草稿缓存
 */
export function cleanupEditorDrafts(): number {
  let cleaned = 0;

  try {
    const keys = Object.keys(localStorage);
    const draftKeys = keys.filter(
      (key) => key.startsWith('chapter_content_') || key.startsWith('chapter_json_')
    );

    // 保留最近修改的 5 个草稿
    const draftsWithTime: Array<{ key: string; time: number }> = [];

    draftKeys.forEach((key) => {
      try {
        const value = localStorage.getItem(key);
        if (!value) return;

        // 尝试从 JSON 中提取时间戳（如果有的话）
        let time = 0;
        try {
          const parsed = JSON.parse(value);
          if (parsed.time) {
            time = parsed.time;
          }
        } catch {
          // 不是 JSON，使用当前时间
        }

        draftsWithTime.push({ key, time });
      } catch (error) {
        // 忽略错误
      }
    });

    // 按时间排序，删除旧的
    draftsWithTime.sort((a, b) => b.time - a.time);
    const toDelete = draftsWithTime.slice(5);

    toDelete.forEach(({ key }) => {
      localStorage.removeItem(key);
      cleaned++;
    });

    if (cleaned > 0) {
      console.log(`🧹 已清理 ${cleaned} 个编辑器草稿缓存`);
    }

    return cleaned;
  } catch (error) {
    console.error('清理编辑器草稿失败:', error);
    return 0;
  }
}

/**
 * 全自动清理 localStorage
 * 会智能清理旧数据但保留重要信息
 */
export function autoCleanupStorage(): void {
  console.group('🧹 开始自动清理 localStorage');

  const beforeStats = analyzeLocalStorage();
  console.log(`清理前使用量: ${beforeStats.totalFormatted} (${beforeStats.usage.toFixed(2)}%)`);

  const sessionsCleaned = cleanupOldAgentSessions(3);
  const draftsCleaned = cleanupEditorDrafts();

  const afterStats = analyzeLocalStorage();
  const saved = beforeStats.total - afterStats.total;

  console.log(`清理后使用量: ${afterStats.totalFormatted} (${afterStats.usage.toFixed(2)}%)`);
  console.log(`释放空间: ${formatBytes(saved)}`);
  console.log(`清理项目: ${sessionsCleaned + draftsCleaned} 项`);

  console.groupEnd();
}

/**
 * 在开发模式下将诊断函数暴露到全局
 */
if (import.meta.env.DEV) {
  (window as any).storageDebug = {
    analyze: analyzeLocalStorage,
    print: printStorageStats,
    cleanup: autoCleanupStorage,
    cleanupSessions: cleanupOldAgentSessions,
    cleanupDrafts: cleanupEditorDrafts,
  };

  console.log(
    '💡 开发模式：可在控制台使用 storageDebug.print() 查看存储使用情况'
  );
}
