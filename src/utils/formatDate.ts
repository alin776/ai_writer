import {
  format,
  formatDistanceToNow,
  isToday,
  isYesterday,
  isThisYear,
  parseISO,
  isValid,
} from 'date-fns';
import { zhCN } from 'date-fns/locale';

/**
 * 将输入安全地转换为 Date，无法解析时返回 null。
 */
const toDate = (date?: string | Date | null): Date | null => {
  if (!date) return null;
  const parsed = typeof date === 'string' ? parseISO(date) : date;
  return isValid(parsed) ? parsed : null;
};

const fallbackText = '未知时间';

/**
 * 格式化日期为相对时间
 * 例如："刚刚"、"5分钟前"、"2天前"、"2024-01-15"
 *
 * @param date 日期字符串或 Date 对象
 * @returns 格式化后的相对时间字符串
 */
export const formatRelativeTime = (date?: string | Date | null): string => {
  const dateObj = toDate(date);
  if (!dateObj) return fallbackText;
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - dateObj.getTime()) / 1000);

  // 1 分钟内：刚刚
  if (diffInSeconds < 60) {
    return '刚刚';
  }

  // 1 小时内：X分钟前
  if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes}分钟前`;
  }

  // 今天：X小时前
  if (isToday(dateObj)) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours}小时前`;
  }

  // 昨天：昨天 HH:mm
  if (isYesterday(dateObj)) {
    return `昨天 ${format(dateObj, 'HH:mm')}`;
  }

  // 7 天内：X天前
  if (diffInSeconds < 7 * 24 * 3600) {
    const days = Math.floor(diffInSeconds / (24 * 3600));
    return `${days}天前`;
  }

  // 今年：MM-DD HH:mm
  if (isThisYear(dateObj)) {
    return format(dateObj, 'MM-dd HH:mm');
  }

  // 更早：YYYY-MM-DD
  return format(dateObj, 'yyyy-MM-dd');
};

/**
 * 格式化日期为完整时间
 * 例如："2024年1月15日 14:30:45"
 *
 * @param date 日期字符串或 Date 对象
 * @returns 格式化后的完整时间字符串
 */
export const formatFullDate = (date?: string | Date | null): string => {
  const dateObj = toDate(date);
  if (!dateObj) return fallbackText;
  return format(dateObj, 'yyyy年MM月dd日 HH:mm:ss', { locale: zhCN });
};

/**
 * 格式化日期为短日期
 * 例如："2024-01-15"
 *
 * @param date 日期字符串或 Date 对象
 * @returns 格式化后的短日期字符串
 */
export const formatShortDate = (date?: string | Date | null): string => {
  const dateObj = toDate(date);
  if (!dateObj) return fallbackText;
  return format(dateObj, 'yyyy-MM-dd');
};

/**
 * 格式化日期为时间
 * 例如："14:30"
 *
 * @param date 日期字符串或 Date 对象
 * @returns 格式化后的时间字符串
 */
export const formatTime = (date?: string | Date | null): string => {
  const dateObj = toDate(date);
  if (!dateObj) return fallbackText;
  return format(dateObj, 'HH:mm');
};

/**
 * 格式化日期为距离现在的时间
 * 例如："2天前"、"3小时前"
 *
 * @param date 日期字符串或 Date 对象
 * @returns 格式化后的距离时间字符串
 */
export const formatDistanceToNowCN = (date?: string | Date | null): string => {
  const dateObj = toDate(date);
  if (!dateObj) return fallbackText;
  return formatDistanceToNow(dateObj, {
    addSuffix: true,
    locale: zhCN,
  });
};

/**
 * 自定义格式化日期
 *
 * @param date 日期字符串或 Date 对象
 * @param formatStr 格式字符串（遵循 date-fns 格式）
 * @returns 格式化后的日期字符串
 */
export const formatCustomDate = (
  date: string | Date | null | undefined,
  formatStr: string
): string => {
  const dateObj = toDate(date);
  if (!dateObj) return fallbackText;
  return format(dateObj, formatStr, { locale: zhCN });
};

/**
 * 格式化日期为文件名安全的字符串
 * 例如："20240115_143045"
 *
 * @param date 日期字符串或 Date 对象
 * @returns 格式化后的文件名安全字符串
 */
export const formatDateForFilename = (date: string | Date | null | undefined = new Date()): string => {
  const dateObj = toDate(date) || new Date();
  return format(dateObj, 'yyyyMMdd_HHmmss');
};

/**
 * 默认导出 formatRelativeTime
 * 用于支持 import formatDate 的导入方式
 */
export default formatRelativeTime;

/**
 * 通用格式化函数别名
 * 根据时间距离自动选择合适的格式
 */
export const formatDate = formatRelativeTime;
