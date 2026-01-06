import { BaseEdge, EdgeProps, EdgeLabelRenderer, getSmoothStepPath, Position } from '@xyflow/react';
import { useMemo } from 'react';

/**
 * 自定义贝塞尔曲线边组件
 * 使用 ReactFlow 的 getSmoothStepPath 来正确处理 Handle 位置
 * 支持多关系自动偏移
 */
type CustomEdgeData = {
  edgeCount?: number;
  edgeIndex?: number;
};

export default function CustomBezierEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
  markerEnd,
  markerStart,
  style,
  label,
}: EdgeProps) {

  const edgeData = (data ?? {}) as CustomEdgeData;
  const edgeCount = edgeData.edgeCount ?? 1;
  const edgeIndex = edgeData.edgeIndex ?? 1;

  // 计算多边偏移量
  let offsetY = 0;
  if (edgeCount > 1) {
    const maxOffset = Math.min(edgeCount * 15, 60);
    const step = (maxOffset * 2) / (edgeCount - 1);
    offsetY = (edgeIndex - 1) * step - maxOffset;
  }

  // 使用 ReactFlow 的 getSmoothStepPath 函数来正确处理 Handle 位置
  const [path, labelX, labelY] = getSmoothStepPath({
    sourceX,
    sourceY,
    sourcePosition: sourcePosition || Position.Right,
    targetX,
    targetY,
    targetPosition: targetPosition || Position.Left,
    borderRadius: 16,
    offset: offsetY,
  });

  // 计算标签角度（使文字平行于连线）
  const angleRad = Math.atan2(targetY - sourceY, targetX - sourceX);
  let angleDeg = angleRad * 180 / Math.PI;

  // 调整角度，避免文字倒置（保持在-90到90度之间）
  if (angleDeg > 90) angleDeg -= 180;
  if (angleDeg < -90) angleDeg += 180;

  return (
    <>
      {/* 渲染边的路径 */}
      <BaseEdge
        id={id}
        path={path}
        markerEnd={markerEnd}
        markerStart={markerStart}
        style={style}
      />

      {/* 渲染标签（如果存在）- 样式由CSS控制以支持暗色模式 */}
      {label && (
        <EdgeLabelRenderer>
          <div
            style={{
              position: 'absolute',
              transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
              pointerEvents: 'all',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
            }}
            className="custom-edge-label"
          >
            {label}
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
}
