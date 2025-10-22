/**
 * 力导向布局算法
 * 使用 d3-force 实现节点相互排斥达到平衡的布局
 */
import { Node, Edge } from '@xyflow/react';
import * as d3 from 'd3-force';

export interface LayoutConfig {
  spacing?: {
    nodeX?: number;
    nodeY?: number;
  };
  animation?: boolean;
  duration?: number;
}

/**
 * 力导向布局
 * 节点相互排斥，关系像弹簧拉伸，自动达到平衡状态
 */
export function applyForceLayout(
  nodes: Node[],
  edges: Edge[],
  config: LayoutConfig = {}
): Node[] {
  const { spacing = { nodeX: 200, nodeY: 200 } } = config;

  // 如果没有节点，直接返回
  if (nodes.length === 0) return nodes;

  // 创建节点副本，添加 d3-force 需要的属性
  const d3Nodes = nodes.map((node, index) => ({
    ...node,
    index,
    x: node.position.x,
    y: node.position.y,
    vx: 0,
    vy: 0,
  }));

  // 创建边数据
  const d3Links = edges.map(edge => ({
    source: nodes.findIndex(n => n.id === edge.source),
    target: nodes.findIndex(n => n.id === edge.target),
  }));

  // 计算画布中心
  const centerX = 500;
  const centerY = 400;

  // 创建力导向模拟
  const simulation = d3
    .forceSimulation(d3Nodes as any)
    .force(
      'link',
      d3
        .forceLink(d3Links)
        .id((d: any) => d.index)
        .distance(spacing.nodeX || 200)
        .strength(0.5)
    )
    .force('charge', d3.forceManyBody().strength(-500))
    .force('center', d3.forceCenter(centerX, centerY))
    .force('collision', d3.forceCollide().radius(100))
    .stop();

  // 运行模拟直到稳定（300次迭代）
  for (let i = 0; i < 300; i++) {
    simulation.tick();
  }

  // 将计算结果应用到节点
  return nodes.map((node, index) => ({
    ...node,
    position: {
      x: (d3Nodes[index] as any).x || node.position.x,
      y: (d3Nodes[index] as any).y || node.position.y,
    },
  }));
}
