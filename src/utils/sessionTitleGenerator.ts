/**
 * 会话标题生成工具
 *
 * 功能：
 * - 从用户首条消息自动提取标题
 * - 智能截断避免断词
 * - 提取关键词作为标题
 */

/**
 * 从用户消息生成会话标题
 * @param message 用户消息内容
 * @param maxLength 最大标题长度（默认20字符）
 * @returns 生成的标题
 */
export function generateSessionTitle(message: string, maxLength: number = 20): string {
  if (!message || message.trim().length === 0) {
    return '新对话';
  }

  // 清理消息内容
  let cleaned = message
    .trim()
    .replace(/\n+/g, ' ')  // 换行转空格
    .replace(/\s+/g, ' ')  // 多空格合并
    .replace(/["""'']/g, '') // 移除引号
    .replace(/^(帮我|请|麻烦|我想|我要|能不能|可以|你能)/g, ''); // 移除常见开头词

  cleaned = cleaned.trim();

  if (cleaned.length === 0) {
    return '新对话';
  }

  // 如果内容短于最大长度，直接返回
  if (cleaned.length <= maxLength) {
    return cleaned;
  }

  // 智能截断：尽量在标点或空格处截断
  const breakPoints = [
    cleaned.lastIndexOf('，', maxLength),
    cleaned.lastIndexOf('。', maxLength),
    cleaned.lastIndexOf('、', maxLength),
    cleaned.lastIndexOf(' ', maxLength),
    cleaned.lastIndexOf('？', maxLength),
    cleaned.lastIndexOf('！', maxLength),
  ].filter(i => i > maxLength * 0.5);  // 至少保留一半长度

  const breakPoint = breakPoints.length > 0 ? Math.max(...breakPoints) : maxLength;

  return cleaned.substring(0, breakPoint) + '...';
}

/**
 * 从消息提取关键词作为标题（备选方案）
 * @param message 用户消息内容
 * @returns 关键词组成的标题，如果没有找到返回null
 */
export function extractKeywordsAsTitle(message: string): string | null {
  // 常见的小说/写作相关关键词
  const novelKeywords = [
    '章节', '大纲', '人物', '角色', '剧情', '情节', '世界观', '设定',
    '开头', '结尾', '转折', '高潮', '冲突', '对话', '描写', '场景',
    '玄幻', '都市', '言情', '悬疑', '科幻', '历史', '武侠', '修仙',
    '主角', '反派', '配角', '女主', '男主', 'boss', 'npc',
    '写', '改', '续写', '扩写', '分析', '优化', '润色', '规划'
  ];

  const lowerMessage = message.toLowerCase();
  const foundKeywords = novelKeywords.filter(kw => lowerMessage.includes(kw));

  if (foundKeywords.length > 0) {
    // 取前3个关键词
    return foundKeywords.slice(0, 3).join('·');
  }

  // 🔧 修复：没有找到关键词返回null，而不是递归调用
  return null;
}

/**
 * 根据会话模式生成默认标题
 * @param mode 会话模式（支持新旧命名）
 * @returns 带模式前缀的默认标题
 */
export function getDefaultTitleByMode(mode?: 'plan' | 'chat' | 'planning'): string {
  const timestamp = new Date().toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  });

  switch (mode) {
    case 'plan':
    case 'planning':
      return `规划对话 ${timestamp}`;
    case 'chat':
      return `对话 ${timestamp}`;
    default:
      return `新对话 ${timestamp}`;
  }
}

/**
 * 智能生成标题（综合方案）
 * 1. 优先使用关键词提取
 * 2. 其次使用智能截断
 * 3. 兜底使用模式+时间戳
 *
 * @param message 用户消息
 * @param mode 会话模式（支持新旧命名）
 * @returns 生成的标题
 */
export function smartGenerateTitle(message: string, mode?: 'plan' | 'chat' | 'planning'): string {
  if (!message || message.trim().length === 0) {
    return getDefaultTitleByMode(mode);
  }

  // 🔧 修复：优先尝试提取关键词
  const keywordTitle = extractKeywordsAsTitle(message);
  if (keywordTitle) {
    return keywordTitle;
  }

  // 使用智能截断
  return generateSessionTitle(message);
}
