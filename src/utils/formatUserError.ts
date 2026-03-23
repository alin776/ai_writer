/**
 * 将原始错误信息转为用户友好的中文提示。
 * 技术性错误按关键词匹配映射；短且无技术特征的业务错误（如「积分不足」）原样透传。
 * 原始错误仅打印到 console.warn 供开发调试。
 */
export function formatUserError(raw: string | undefined | null): string {
  if (!raw) return '服务暂时不可用，请稍后重试。';

  const text = String(raw);
  console.warn('[AppError]', text);

  const l = text.toLowerCase();

  // 网络 / 超时
  if (l.includes('timeout') || l.includes('timed out'))
    return '请求超时，请稍后重试。';
  if (l.includes('network') || l.includes('fetch') || l.includes('econnrefused') || l.includes('econnreset'))
    return '网络连接异常，请检查网络后重试。';

  // 认证 / 权限
  if (l.includes('not authenticated') || (l.includes('401') && l.includes('unauthorized')))
    return '登录已过期，请重新登录。';
  if (l.includes('forbidden') || l.includes('没有权限'))
    return '没有权限执行此操作。';

  // 限流 / 配额
  if (l.includes('rate limit') || l.includes('429') || l.includes('quota') || l.includes('too many request'))
    return '请求过于频繁，请稍后再试。';

  // AI 服务
  if (l.includes('openai') || l.includes('anthropic') || l.includes('deepseek') || l.includes('model_not_found'))
    return 'AI 服务暂时不可用，请稍后重试。';

  // 数据库 / 连接池
  if (l.includes('database') || l.includes('sqlalchemy') || l.includes('asyncpg') || l.includes('queuepool') || l.includes('connection pool'))
    return '服务器繁忙，请稍后重试。';

  // 通用服务器错误
  if (l.includes('internal server error'))
    return '服务器内部错误，请稍后重试。';

  // 长消息或含技术关键词 → 脱敏
  if (
    text.length > 100 ||
    l.includes('traceback') ||
    l.includes('typeerror') ||
    l.includes('valueerror') ||
    l.includes('keyerror') ||
    l.includes('attributeerror') ||
    l.includes('importerror') ||
    l.includes('exception')
  )
    return '遇到了一些问题，请稍后重试。';

  // 短且无技术特征 → 可能是后端已格式化的业务错误，原样透传
  return text;
}
