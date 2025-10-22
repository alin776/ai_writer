/**
 * 环形布局算法
 * 节点沿圆形排列，主要节点在中心
 */
import { Node, Edge } from '@xyflow/react';
import { LayoutConfig } from './ForceLayout';

/**
 * 环形布局
 * 节点沿圆形排列，根据连接数量决定位置
 */
export function applyCircularLayout(
  nodes: Node[],
  edges: Edge[],
  _config: LayoutConfig = {}
): Node[] {
  // 如果没有节点，直接返回
  if (nodes.length === 0) return nodes;

  // 计算每个节点的连接数量
  const connectionCounts = new Map<string, number>();
  nodes.forEach(node => connectionCounts.set(node.id, 0));

  edges.forEach(edge => {
    connectionCounts.set(
      edge.source,
      (connectionCounts.get(edge.source) || 0) + 1
    );
    connectionCounts.set(
      edge.target,
      (connectionCounts.get(edge.target) || 0) + 1
    );
  });

  // 找出连接最多的节点（作为中心节点）
  let maxConnections = 0;
  let centerNode: Node | null = null;

  nodes.forEach(node => {
    const count = connectionCounts.get(node.id) || 0;
    if (count > maxConnections) {
      maxConnections = count;
      centerNode = node;
    }
  });

  // 画布中心
  const centerX = 600;
  const centerY = 400;
  const radius = 300; // 圆形半径

  // 如果有中心节点，将其放在中心
  const layoutNodes = nodes.map(node => ({ ...node }));

  if (centerNode) {
    const centerIndex = layoutNodes.findIndex(n => n.id === centerNode!.id);
    if (centerIndex >= 0) {
      layoutNodes[centerIndex] = {
        ...layoutNodes[centerIndex],
        position: { x: centerX - 90, y: centerY - 40 },
      };
    }

    // 其他节点沿圆形排列
    const otherNodes = layoutNodes.filter(n => n.id !== centerNode!.id);
    const angleStep = (2 * Math.PI) / otherNodes.length;

    otherNodes.forEach((node, index) => {
      const angle = index * angleStep;
      const x = centerX + radius * Math.cos(angle) - 90; // 减去节点宽度的一半
      const y = centerY + radius * Math.sin(angle) - 40; // 减去节点高度的一半

      const nodeIndex = layoutNodes.findIndex(n => n.id === node.id);
      if (nodeIndex >= 0) {
        layoutNodes[nodeIndex] = {
          ...layoutNodes[nodeIndex],
          position: { x, y },
        };
      }
    });
  } else {
    // 没有明显的中心节点，所有节点均匀分布在圆上
    const angleStep = (2 * Math.PI) / nodes.length;

    layoutNodes.forEach((node, index) => {
      const angle = index * angleStep;
      const x = centerX + radius * Math.cos(angle) - 90;
      const y = centerY + radius * Math.sin(angle) - 40;

      layoutNodes[index] = {
        ...node,
        position: { x, y },
      };
    });
  }

  return layoutNodes;
}
