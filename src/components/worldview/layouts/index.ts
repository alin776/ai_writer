/**
 * 布局算法导出
 */
export { applyForceLayout, type LayoutConfig } from './ForceLayout';
export { applyHierarchicalLayout, type HierarchicalConfig } from './HierarchicalLayout';
export { applyCircularLayout } from './CircularLayout';
export { applyGridLayout } from './GridLayout';
export { applyTimelineLayout } from './TimelineLayout';

// 布局类型枚举
export type LayoutAlgorithm = 
  | 'force'
  | 'hierarchical'
  | 'circular'
  | 'grid'
  | 'timeline'
  | 'custom';

// 布局配置类型
export interface GlobalLayoutConfig {
  algorithm: LayoutAlgorithm;
  direction?: 'TB' | 'BT' | 'LR' | 'RL';
  spacing: {
    nodeX: number;
    nodeY: number;
  };
  animation: boolean;
  duration: number;
}

// 默认布局配置
export const DEFAULT_LAYOUT_CONFIG: GlobalLayoutConfig = {
  algorithm: 'force',
  direction: 'TB',
  spacing: {
    nodeX: 200,
    nodeY: 150,
  },
  animation: true,
  duration: 1000,
};
