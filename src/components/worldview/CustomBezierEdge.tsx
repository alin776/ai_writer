import { BaseEdge, EdgeProps, EdgeLabelRenderer } from '@xyflow/react';
import { useMemo } from 'react';

/**
 * 计算二次贝塞尔曲线路径
 * @param sourceX 源节点连接点X坐标（ReactFlow计算的节点边界点）
 * @param sourceY 源节点连接点Y坐标
 * @param targetX 目标节点连接点X坐标
 * @param targetY 目标节点连接点Y坐标
 * @param edgeCount 该节点对之间的边总数
 * @param edgeIndex 当前边的索引（从1开始）
 * @returns 路径字符串、标签位置、切线角度
 */
function getQuadraticBezierPath(
  sourceX: number,
  sourceY: number,
  targetX: number,
  targetY: number,
  edgeCount: number,
  edgeIndex: number
): { path: string; labelX: number; labelY: number; angle: number } {
  
  // 计算连线向量
  const deltaX = targetX - sourceX;
  const deltaY = targetY - sourceY;
  const length = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

  // 处理零长度情况
  if (length === 0) {
    return {
      path: `M ${sourceX},${sourceY} L ${targetX},${targetY}`,
      labelX: sourceX,
      labelY: sourceY,
      angle: 0,
    };
  }

  // 计算法线向量（垂直于连线方向的单位向量）
  const normX = -deltaY / length;
  const normY = deltaX / length;

  // 计算中点
  const midX = (sourceX + targetX) / 2;
  const midY = (sourceY + targetY) / 2;

  // 计算偏移量
  let offset = 0;
  
  if (edgeCount === 1) {
    // 单条边：给予基础弧度，避免纯直线
    offset = 20;
  } else {
    // 多条边：计算分散偏移
    const maxOffset = Math.min(edgeCount * 12, 60);
    const step = (maxOffset * 2) / (edgeCount - 1);
    offset = (edgeIndex - 1) * step - maxOffset;
  }

  // 控制点（在中点的法线方向上偏移）
  const controlX = midX + normX * offset;
  const controlY = midY + normY * offset;

  // 计算贝塞尔曲线t=0.5时的精确位置（标签位置）
  // 公式: B(t) = (1-t)² * P0 + 2(1-t)t * P1 + t² * P2
  const t = 0.5;
  const labelX = (1-t)*(1-t)*sourceX + 2*(1-t)*t*controlX + t*t*targetX;
  const labelY = (1-t)*(1-t)*sourceY + 2*(1-t)*t*controlY + t*t*targetY;

  // 计算标签角度（使文字平行于连线）
  const angleRad = Math.atan2(targetY - sourceY, targetX - sourceX);
  let angleDeg = angleRad * 180 / Math.PI;
  
  // 调整角度，避免文字倒置（保持在-90到90度之间）
  if (angleDeg > 90) angleDeg -= 180;
  if (angleDeg < -90) angleDeg += 180;

  // 生成SVG路径字符串（Q = 二次贝塞尔曲线）
  const path = `M ${sourceX},${sourceY} Q ${controlX},${controlY} ${targetX},${targetY}`;

  return { path, labelX, labelY, angle: angleDeg };
}

/**
 * 自定义贝塞尔曲线边组件
 * 使用二次贝塞尔曲线替代smoothstep，提供更平滑的视觉效果
 * 支持多关系自动偏移，形成优雅的曲线束
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
  data,
  markerEnd,
  markerStart,
  style,
  label,
}: EdgeProps) {

  const edgeData = (data ?? {}) as CustomEdgeData;
  const edgeCount = edgeData.edgeCount ?? 1;
  const edgeIndex = edgeData.edgeIndex ?? 1;

  // 使用useMemo缓存路径计算（性能优化）
  const { path, labelX, labelY, angle } = useMemo(
    () => getQuadraticBezierPath(
      sourceX, 
      sourceY, 
      targetX, 
      targetY, 
      edgeCount, 
      edgeIndex
    ),
    [sourceX, sourceY, targetX, targetY, edgeCount, edgeIndex]
  );

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
      
      {/* 渲染标签（如果存在）*/}
      {label && (
        <EdgeLabelRenderer>
          <div
            style={{
              position: 'absolute',
              // 标签位置和旋转
              transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px) rotate(${angle}deg)`,
              fontSize: 11,
              fontWeight: 600,
              background: 'rgba(255, 255, 255, 0.9)',
              padding: '2px 6px',
              borderRadius: 4,
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
