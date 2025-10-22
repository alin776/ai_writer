/**
 * 时间线布局算法
 * 按时间顺序从左到右排列（如果有时间信息）
 */
import { Node, Edge } from '@xyflow/react';
import { LayoutConfig } from './ForceLayout';

/**
 * 时间线布局
 * 按创建时间或其他时间属性从左到右排列
 */
export function applyTimelineLayout(
  nodes: Node[],
  _edges: Edge[],
  config: LayoutConfig = {}
): Node[] {
  const { spacing = { nodeX: 250, nodeY: 200 } } = config;

  // 如果没有节点，直接返回
  if (nodes.length === 0) return nodes;

  // 按类型分组
  const characterNodes = nodes.filter(n => n.type === 'character');
  const locationNodes = nodes.filter(n => n.type === 'location');
  const settingNodes = nodes.filter(n => n.type === 'setting');

  // 每种类型一行
  const rows = [
    { type: 'character', nodes: characterNodes, y: 100 },
    { type: 'location', nodes: locationNodes, y: 300 },
    { type: 'setting', nodes: settingNodes, y: 500 },
  ];

  const layoutNodes: Node[] = [];
  const xSpacing = spacing.nodeX || 250;

  rows.forEach(row => {
    // 尝试按创建时间排序（如果有的话）
    const sortedNodes = [...row.nodes].sort((a, b) => {
      const aTime = (a.data as any)?.createdAt;
      const bTime = (b.data as any)?.createdAt;

      if (aTime && bTime) {
        return new Date(aTime).getTime() - new Date(bTime).getTime();
      }

      // 如果没有时间信息，保持原顺序
      return 0;
    });

    // 从左到右排列
    sortedNodes.forEach((node, index) => {
      layoutNodes.push({
        ...node,
        position: {
          x: 50 + index * xSpacing,
          y: row.y,
        },
      });
    });
  });

  return layoutNodes;
}
