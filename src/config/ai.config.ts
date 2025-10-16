/**
 * AI 配置文件
 * 统一管理所有 AI 相关的配置项
 */

export interface AIConfig {
  // API 配置
  apiUrl: string;
  apiKey: string;

  // OpenAI 配置
  openai: {
    model: string;
    maxTokens: number;
    temperature: number;
    streamEnabled: boolean;
  };

  // 补全配置
  completion: {
    enabled: boolean;
    debounceDelay: number; // 防抖延迟（毫秒）
    minCharacters: number; // 触发补全的最小字符数
    maxSuggestions: number; // 最大建议数
  };

  // 续写配置
  continue: {
    maxTokens: number;
    temperature: number;
    contextLength: number; // 上下文长度（字符数）
  };

  // 其他操作配置
  rewrite: {
    maxTokens: number;
    temperature: number;
  };
}

/**
 * 默认配置
 */
const defaultConfig: AIConfig = {
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  apiKey: import.meta.env.VITE_OPENAI_API_KEY || '',

  openai: {
    model: import.meta.env.VITE_OPENAI_MODEL || 'gpt-4-turbo-preview',
    maxTokens: 2000,
    temperature: 0.7,
    streamEnabled: true,
  },

  completion: {
    enabled: true,
    debounceDelay: 300,
    minCharacters: 3,
    maxSuggestions: 3,
  },

  continue: {
    maxTokens: 500,
    temperature: 0.8,
    contextLength: 500,
  },

  rewrite: {
    maxTokens: 1000,
    temperature: 0.7,
  },
};

/**
 * 获取 AI 配置
 */
export function getAIConfig(): AIConfig {
  return { ...defaultConfig };
}

/**
 * 更新 AI 配置
 * @param config - 部分配置更新
 */
export function updateAIConfig(config: Partial<AIConfig>): void {
  Object.assign(defaultConfig, config);
}

/**
 * 验证 API 配置是否完整
 */
export function validateAIConfig(): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  const config = getAIConfig();

  if (!config.apiKey) {
    errors.push('缺少 OpenAI API Key，请在 .env 文件中设置 VITE_OPENAI_API_KEY');
  }

  if (!config.apiUrl) {
    errors.push('缺少 API URL，请在 .env 文件中设置 VITE_API_URL');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

export default getAIConfig();
