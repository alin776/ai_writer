/**
 * 层级布局算法
 * 使用 dagre 实现从上到下的层级结构布局
 */
import { Node, Edge } from '@xyflow/react';
import dagre from 'dagre';
import { LayoutConfig } from './ForceLayout';

export interface HierarchicalConfig extends LayoutConfig {
  direction?: 'TB' | 'BT' | 'LR' | 'RL';
}

/**
 * 层级布局
 * 从上到下排列层级关系，主要节点在顶部
 */
export function applyHierarchicalLayout(
  nodes: Node[],
  edges: Edge[],
  config: HierarchicalConfig = {}
): Node[] {
  const {
    direction = 'TB',
    spacing = { nodeX: 150, nodeY: 150 },
  } = config;

  // 如果没有节点，直接返回
  if (nodes.length === 0) return nodes;

  // 创建 dagre 图
  const g = new dagre.graphlib.Graph();

  // 设置图的默认配置
  g.setGraph({
    rankdir: direction,
    nodesep: spacing.nodeX || 150,
    ranksep: spacing.nodeY || 150,
    marginx: 50,
    marginy: 50,
  });

  // 设置默认边标签
  g.setDefaultEdgeLabel(() => ({}));

  // 添加节点（固定宽高）
  nodes.forEach(node => {
    g.setNode(node.id, { 
      width: 180, 
      height: 80,
    });
  });

  // 添加边
  edges.forEach(edge => {
    g.setEdge(edge.source, edge.target);
  });

  // 运行布局算法
  dagre.layout(g);

  // 将计算结果应用到节点
  return nodes.map(node => {
    const position = g.node(node.id);
    
    if (position) {
      return {
        ...node,
        position: {
          // dagre 返回的是节点中心点，需要转换为左上角坐标
          x: position.x - 90, // width / 2
          y: position.y - 40, // height / 2
        },
      };
    }
    
    return node;
  });
}
