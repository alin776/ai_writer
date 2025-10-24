/**
 * 世界观图谱导出工具
 * 支持导出为 PNG、SVG、JSON 格式
 */
import { toPng, toSvg } from 'html-to-image';

/**
 * 导出为 PNG 图片
 * @param element HTML 元素
 * @param filename 文件名
 */
export async function exportGraphAsPng(element: HTMLElement, filename: string = 'worldview-graph.png'): Promise<void> {
  try {
    const dataUrl = await toPng(element, {
      quality: 1.0,
      backgroundColor: '#ffffff',
      pixelRatio: 2, // 2倍分辨率，更清晰
    });

    // 触发下载
    const link = document.createElement('a');
    link.download = filename;
    link.href = dataUrl;
    link.click();
  } catch (error) {
    console.error('导出 PNG 失败:', error);
    throw new Error('导出 PNG 失败');
  }
}

/**
 * 导出为 SVG 矢量图
 * @param element HTML 元素
 * @param filename 文件名
 */
export async function exportGraphAsSvg(element: HTMLElement, filename: string = 'worldview-graph.svg'): Promise<void> {
  try {
    const dataUrl = await toSvg(element, {
      backgroundColor: '#ffffff',
    });

    // 触发下载
    const link = document.createElement('a');
    link.download = filename;
    link.href = dataUrl;
    link.click();
  } catch (error) {
    console.error('导出 SVG 失败:', error);
    throw new Error('导出 SVG 失败');
  }
}

/**
 * 导出为 JSON 数据
 * @param data 数据对象
 * @param filename 文件名
 */
export function exportGraphAsJson(data: any, filename: string = 'worldview-data.json'): void {
  try {
    const jsonString = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    // 触发下载
    const link = document.createElement('a');
    link.download = filename;
    link.href = url;
    link.click();

    // 清理 URL 对象
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('导出 JSON 失败:', error);
    throw new Error('导出 JSON 失败');
  }
}
