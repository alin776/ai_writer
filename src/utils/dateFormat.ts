import { format, formatDistanceToNow, isValid, parseISO, type Locale } from 'date-fns';
import { zhCN, zhTW, enUS } from 'date-fns/locale';
import type { LanguageCode } from '../i18n';

/**
 * date-fns locale 映射
 */
const localeMap: Record<LanguageCode, Locale> = {
  'zh-CN': zhCN,
  'zh-TW': zhTW,
  'en-US': enUS,
};

/**
 * 日期格式配置
 */
const dateFormats: Record<LanguageCode, {
  date: string;
  dateTime: string;
  time: string;
  shortDate: string;
  monthDay: string;
}> = {
  'zh-CN': {
    date: 'yyyy年M月d日',
    dateTime: 'yyyy年M月d日 HH:mm',
    time: 'HH:mm',
    shortDate: 'M月d日',
    monthDay: 'M月d日',
  },
  'zh-TW': {
    date: 'yyyy年M月d日',
    dateTime: 'yyyy年M月d日 HH:mm',
    time: 'HH:mm',
    shortDate: 'M月d日',
    monthDay: 'M月d日',
  },
  'en-US': {
    date: 'MMM d, yyyy',
    dateTime: 'MMM d, yyyy h:mm a',
    time: 'h:mm a',
    shortDate: 'MMM d',
    monthDay: 'MMM d',
  },
};

/**
 * 获取 date-fns locale
 */
export const getDateLocale = (language: LanguageCode): Locale => {
  return localeMap[language] || zhCN;
};

/**
 * 解析日期字符串或 Date 对象
 */
const parseDate = (date: string | Date): Date | null => {
  if (date instanceof Date) {
    return isValid(date) ? date : null;
  }

  if (typeof date === 'string') {
    const parsed = parseISO(date);
    return isValid(parsed) ? parsed : null;
  }

  return null;
};

/**
 * 格式化日期
 *
 * @example
 * ```ts
 * formatDate(new Date(), 'zh-CN') // "2024年12月14日"
 * formatDate('2024-12-14', 'en-US') // "Dec 14, 2024"
 * ```
 */
export const formatDate = (
  date: string | Date,
  language: LanguageCode,
  formatType: 'date' | 'dateTime' | 'time' | 'shortDate' | 'monthDay' = 'date'
): string => {
  const parsedDate = parseDate(date);
  if (!parsedDate) return '';

  const locale = getDateLocale(language);
  const formatStr = dateFormats[language]?.[formatType] || dateFormats['zh-CN'][formatType];

  return format(parsedDate, formatStr, { locale });
};

/**
 * 格式化相对时间
 *
 * @example
 * ```ts
 * formatRelativeTime(new Date(), 'zh-CN') // "不到 1 分钟前"
 * formatRelativeTime(yesterday, 'en-US') // "1 day ago"
 * ```
 */
export const formatRelativeTime = (
  date: string | Date,
  language: LanguageCode,
  options?: { addSuffix?: boolean }
): string => {
  const parsedDate = parseDate(date);
  if (!parsedDate) return '';

  const locale = getDateLocale(language);

  return formatDistanceToNow(parsedDate, {
    locale,
    addSuffix: options?.addSuffix ?? true,
  });
};

/**
 * 格式化时间戳为本地时间字符串
 *
 * @example
 * ```ts
 * formatTimestamp('2024-12-14T10:30:00Z', 'zh-CN') // "2024年12月14日 18:30"
 * formatTimestamp('2024-12-14T10:30:00Z', 'en-US') // "Dec 14, 2024 6:30 PM"
 * ```
 */
export const formatTimestamp = (
  timestamp: string | Date | undefined | null,
  language: LanguageCode
): string => {
  if (!timestamp) {
    const unknownTexts: Record<LanguageCode, string> = {
      'zh-CN': '未知时间',
      'zh-TW': '未知時間',
      'en-US': 'Unknown time',
    };
    return unknownTexts[language] || '未知时间';
  }

  return formatDate(timestamp, language, 'dateTime');
};

/**
 * 格式化时间（仅时分）
 *
 * @example
 * ```ts
 * formatTime(new Date(), 'zh-CN') // "18:30"
 * formatTime(new Date(), 'en-US') // "6:30 PM"
 * ```
 */
export const formatTime = (
  date: string | Date,
  language: LanguageCode
): string => {
  return formatDate(date, language, 'time');
};

/**
 * 智能格式化日期
 * - 今天：显示时间
 * - 今年：显示月日
 * - 其他：显示完整日期
 *
 * @example
 * ```ts
 * formatSmartDate(today, 'zh-CN') // "18:30"
 * formatSmartDate(thisYear, 'zh-CN') // "12月14日"
 * formatSmartDate(lastYear, 'zh-CN') // "2023年12月14日"
 * ```
 */
export const formatSmartDate = (
  date: string | Date,
  language: LanguageCode
): string => {
  const parsedDate = parseDate(date);
  if (!parsedDate) return '';

  const now = new Date();
  const isToday =
    parsedDate.getDate() === now.getDate() &&
    parsedDate.getMonth() === now.getMonth() &&
    parsedDate.getFullYear() === now.getFullYear();

  const isThisYear = parsedDate.getFullYear() === now.getFullYear();

  if (isToday) {
    return formatDate(parsedDate, language, 'time');
  }

  if (isThisYear) {
    return formatDate(parsedDate, language, 'monthDay');
  }

  return formatDate(parsedDate, language, 'date');
};

/**
 * 使用原生 toLocaleString 格式化日期
 * 用于简单场景，避免引入 date-fns 的复杂度
 */
export const toLocaleDate = (
  date: string | Date,
  language: LanguageCode,
  options?: Intl.DateTimeFormatOptions
): string => {
  const parsedDate = parseDate(date);
  if (!parsedDate) return '';

  const localeMap: Record<LanguageCode, string> = {
    'zh-CN': 'zh-CN',
    'zh-TW': 'zh-TW',
    'en-US': 'en-US',
  };

  return parsedDate.toLocaleString(localeMap[language], options);
};

/**
 * 使用原生 toLocaleTimeString 格式化时间
 */
export const toLocaleTime = (
  date: string | Date,
  language: LanguageCode,
  options?: Intl.DateTimeFormatOptions
): string => {
  const parsedDate = parseDate(date);
  if (!parsedDate) return '';

  const localeMap: Record<LanguageCode, string> = {
    'zh-CN': 'zh-CN',
    'zh-TW': 'zh-TW',
    'en-US': 'en-US',
  };

  const defaultOptions: Intl.DateTimeFormatOptions = {
    hour: '2-digit',
    minute: '2-digit',
  };

  return parsedDate.toLocaleTimeString(localeMap[language], options || defaultOptions);
};
