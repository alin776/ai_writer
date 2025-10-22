/**
 * 图表导出工具函数
 */
import { toPng, toSvg } from 'html-to-image';
import { Node, Edge } from '@xyflow/react';

export interface ExportOptions {
  format: 'png' | 'svg' | 'json';
  filename?: string;
  quality?: number; // 0-1, for PNG
  backgroundColor?: string;
}

/**
 * 导出为PNG图片
 */
export async function exportToPng(
  element: HTMLElement,
  options: ExportOptions = { format: 'png' }
): Promise<void> {
  try {
    const dataUrl = await toPng(element, {
      quality: options.quality || 0.95,
      backgroundColor: options.backgroundColor || '#111827',
      cacheBust: true,
      pixelRatio: 2, // 2x resolution for better quality
    });

    // 下载图片
    const link = document.createElement('a');
    link.download = options.filename || `worldview-graph-${Date.now()}.png`;
    link.href = dataUrl;
    link.click();
  } catch (error) {
    console.error('导出PNG失败:', error);
    throw error;
  }
}

/**
 * 导出为SVG图片
 */
export async function exportToSvg(
  element: HTMLElement,
  options: ExportOptions = { format: 'svg' }
): Promise<void> {
  try {
    const dataUrl = await toSvg(element, {
      backgroundColor: options.backgroundColor || '#111827',
      cacheBust: true,
    });

    // 下载SVG
    const link = document.createElement('a');
    link.download = options.filename || `worldview-graph-${Date.now()}.svg`;
    link.href = dataUrl;
    link.click();
  } catch (error) {
    console.error('导出SVG失败:', error);
    throw error;
  }
}

/**
 * 导出为JSON数据
 */
export function exportToJson(
  nodes: Node[],
  edges: Edge[],
  options: ExportOptions = { format: 'json' }
): void {
  try {
    const data = {
      exportTime: new Date().toISOString(),
      version: '1.0',
      nodes: nodes.map(node => ({
        id: node.id,
        type: node.type,
        position: node.position,
        data: node.data,
      })),
      edges: edges.map(edge => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        type: edge.type,
        data: edge.data,
        style: edge.style,
      })),
    };

    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.download = options.filename || `worldview-graph-${Date.now()}.json`;
    link.href = url;
    link.click();

    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('导出JSON失败:', error);
    throw error;
  }
}
