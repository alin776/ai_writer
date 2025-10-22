/**
 * 网格布局算法
 * 整齐的网格排列，便于对比
 */
import { Node, Edge } from '@xyflow/react';
import { LayoutConfig } from './ForceLayout';

/**
 * 网格布局
 * 节点按网格整齐排列
 */
export function applyGridLayout(
  nodes: Node[],
  _edges: Edge[],
  config: LayoutConfig = {}
): Node[] {
  const { spacing = { nodeX: 250, nodeY: 150 } } = config;

  // 如果没有节点，直接返回
  if (nodes.length === 0) return nodes;

  // 计算网格列数（尽量接近正方形）
  const columns = Math.ceil(Math.sqrt(nodes.length));

  // 起始位置
  const startX = 50;
  const startY = 50;

  // 节点间距
  const xSpacing = spacing.nodeX || 250;
  const ySpacing = spacing.nodeY || 150;

  // 按类型分组排列（角色、地点、设定）
  const characterNodes = nodes.filter(n => n.type === 'character');
  const locationNodes = nodes.filter(n => n.type === 'location');
  const settingNodes = nodes.filter(n => n.type === 'setting');

  const layoutNodes: Node[] = [];
  let currentRow = 0;

  // 排列角色节点
  characterNodes.forEach((node, index) => {
    const col = index % columns;
    const row = Math.floor(index / columns) + currentRow;

    layoutNodes.push({
      ...node,
      position: {
        x: startX + col * xSpacing,
        y: startY + row * ySpacing,
      },
    });
  });

  if (characterNodes.length > 0) {
    currentRow += Math.ceil(characterNodes.length / columns);
  }

  // 排列地点节点
  locationNodes.forEach((node, index) => {
    const col = index % columns;
    const row = Math.floor(index / columns) + currentRow;

    layoutNodes.push({
      ...node,
      position: {
        x: startX + col * xSpacing,
        y: startY + row * ySpacing,
      },
    });
  });

  if (locationNodes.length > 0) {
    currentRow += Math.ceil(locationNodes.length / columns);
  }

  // 排列设定节点
  settingNodes.forEach((node, index) => {
    const col = index % columns;
    const row = Math.floor(index / columns) + currentRow;

    layoutNodes.push({
      ...node,
      position: {
        x: startX + col * xSpacing,
        y: startY + row * ySpacing,
      },
    });
  });

  return layoutNodes;
}
