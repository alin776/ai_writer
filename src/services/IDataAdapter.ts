/**
 * 数据适配器接口
 *
 * 定义统一的数据访问接口，支持 Mock 和真实 API 两种实现
 */
export interface IDataAdapter {
  /**
   * GET 请求
   * @param url 请求路径
   * @param params 查询参数
   * @returns Promise<T>
   */
  get<T>(url: string, params?: any): Promise<T>;

  /**
   * POST 请求
   * @param url 请求路径
   * @param data 请求数据
   * @returns Promise<T>
   */
  post<T>(url: string, data?: any): Promise<T>;

  /**
   * PUT 请求
   * @param url 请求路径
   * @param data 请求数据
   * @returns Promise<T>
   */
  put<T>(url: string, data?: any): Promise<T>;

  /**
   * DELETE 请求
   * @param url 请求路径
   * @returns Promise<T>
   */
  delete<T>(url: string): Promise<T>;
}
