/// <reference types="vite/client" />

/**
 * Vite Worker 模块声明
 */
declare module '*?worker' {
  const workerConstructor: {
    new (): Worker;
  };
  export default workerConstructor;
}

declare module '@/workers/typewriterWorker?worker' {
  const workerConstructor: {
    new (): Worker;
  };
  export default workerConstructor;
}

/**
 * 环境变量类型定义
 */
interface ImportMetaEnv {
  /**
   * API 基础 URL
   */
  readonly VITE_API_BASE_URL: string;

  /**
   * 应用标题
   */
  readonly VITE_APP_TITLE?: string;

  /**
   * 应用版本
   */
  readonly VITE_APP_VERSION?: string;

  /**
   * 是否为生产环境
   */
  readonly PROD: boolean;

  /**
   * 是否为开发环境
   */
  readonly DEV: boolean;

  /**
   * 应用模式
   */
  readonly MODE: string;
}

/**
 * 扩展 ImportMeta 接口
 */
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
