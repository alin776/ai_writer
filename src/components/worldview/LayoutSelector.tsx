/**
 * 布局选择器组件
 * 用于切换不同的布局算法
 */
import React, { useState } from 'react';
import { LayoutAlgorithm, GlobalLayoutConfig, DEFAULT_LAYOUT_CONFIG } from './layouts';

interface LayoutSelectorProps {
  currentLayout: LayoutAlgorithm;
  onLayoutChange: (layout: LayoutAlgorithm) => void;
  config: GlobalLayoutConfig;
  onConfigChange: (config: Partial<GlobalLayoutConfig>) => void;
}

const LAYOUT_OPTIONS = [
  {
    value: 'force' as LayoutAlgorithm,
    label: '力导向布局',
    icon: '🌐',
    description: '节点相互排斥，自动达到平衡',
  },
  {
    value: 'hierarchical' as LayoutAlgorithm,
    label: '层级布局',
    icon: '📊',
    description: '从上到下的层级结构',
  },
  {
    value: 'circular' as LayoutAlgorithm,
    label: '环形布局',
    icon: '⭕',
    description: '沿圆形排列，主节点居中',
  },
  {
    value: 'grid' as LayoutAlgorithm,
    label: '网格布局',
    icon: '📐',
    description: '整齐的网格排列',
  },
  {
    value: 'timeline' as LayoutAlgorithm,
    label: '时间线布局',
    icon: '📅',
    description: '按时间顺序排列',
  },
];

export const LayoutSelector: React.FC<LayoutSelectorProps> = ({
  currentLayout,
  onLayoutChange,
  config,
  onConfigChange,
}) => {
  const [showConfig, setShowConfig] = useState(false);

  return (
    <div className="layout-selector">
      {/* 布局按钮组 */}
      <div className="layout-buttons">
        {LAYOUT_OPTIONS.map(option => (
          <button
            key={option.value}
            className={`layout-btn ${currentLayout === option.value ? 'active' : ''}`}
            onClick={() => onLayoutChange(option.value)}
            title={option.description}
          >
            <span className="layout-icon">{option.icon}</span>
            <span className="layout-label">{option.label}</span>
          </button>
        ))}
        
        {/* 配置按钮 */}
        <button
          className="layout-config-btn"
          onClick={() => setShowConfig(!showConfig)}
          title="布局配置"
        >
          ⚙️
        </button>
      </div>

      {/* 配置面板 */}
      {showConfig && (
        <div className="layout-config-panel">
          <div className="config-header">
            <h4>布局配置</h4>
            <button onClick={() => setShowConfig(false)}>✕</button>
          </div>

          <div className="config-section">
            <label>方向（层级布局）</label>
            <select
              value={config.direction}
              onChange={e => onConfigChange({ direction: e.target.value as any })}
              disabled={currentLayout !== 'hierarchical'}
            >
              <option value="TB">从上到下 (TB)</option>
              <option value="BT">从下到上 (BT)</option>
              <option value="LR">从左到右 (LR)</option>
              <option value="RL">从右到左 (RL)</option>
            </select>
          </div>

          <div className="config-section">
            <label>
              横向间距: {config.spacing.nodeX}px
            </label>
            <input
              type="range"
              min="100"
              max="400"
              step="50"
              value={config.spacing.nodeX}
              onChange={e => onConfigChange({
                spacing: { ...config.spacing, nodeX: Number(e.target.value) },
              })}
            />
          </div>

          <div className="config-section">
            <label>
              纵向间距: {config.spacing.nodeY}px
            </label>
            <input
              type="range"
              min="100"
              max="400"
              step="50"
              value={config.spacing.nodeY}
              onChange={e => onConfigChange({
                spacing: { ...config.spacing, nodeY: Number(e.target.value) },
              })}
            />
          </div>

          <div className="config-section">
            <label>
              <input
                type="checkbox"
                checked={config.animation}
                onChange={e => onConfigChange({ animation: e.target.checked })}
              />
              启用动画过渡
            </label>
          </div>

          {config.animation && (
            <div className="config-section">
              <label>
                动画时长: {config.duration}ms
              </label>
              <input
                type="range"
                min="300"
                max="2000"
                step="100"
                value={config.duration}
                onChange={e => onConfigChange({ duration: Number(e.target.value) })}
              />
            </div>
          )}

          <div className="config-actions">
            <button
              className="reset-btn"
              onClick={() => onConfigChange(DEFAULT_LAYOUT_CONFIG)}
            >
              重置为默认值
            </button>
          </div>
        </div>
      )}

      <style>{`
        .layout-selector {
          position: relative;
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .layout-buttons {
          display: flex;
          gap: 0.5rem;
          flex-wrap: wrap;
          padding: 0.5rem;
          background: #1a1a1a;
          border-radius: 8px;
          border: 1px solid #2a2a2a;
        }

        .layout-btn {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0.25rem;
          padding: 0.5rem 0.75rem;
          background: #2a2a2a;
          border: 1px solid #3a3a3a;
          border-radius: 6px;
          color: #9ca3af;
          font-size: 0.875rem;
          cursor: pointer;
          transition: all 0.2s;
          min-width: 90px;
        }

        .layout-btn:hover {
          background: #3a3a3a;
          border-color: #4a4a4a;
          color: #e5e7eb;
        }

        .layout-btn.active {
          background: #3b82f6;
          border-color: #3b82f6;
          color: #fff;
        }

        .layout-icon {
          font-size: 1.5rem;
        }

        .layout-label {
          font-size: 0.75rem;
          font-weight: 500;
          white-space: nowrap;
        }

        .layout-config-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 0.5rem;
          background: #2a2a2a;
          border: 1px solid #3a3a3a;
          border-radius: 6px;
          font-size: 1.25rem;
          cursor: pointer;
          transition: all 0.2s;
          min-width: 45px;
        }

        .layout-config-btn:hover {
          background: #3a3a3a;
          border-color: #4a4a4a;
        }

        .layout-config-panel {
          position: absolute;
          top: 100%;
          right: 0;
          margin-top: 0.5rem;
          width: 320px;
          background: #1a1a1a;
          border: 1px solid #2a2a2a;
          border-radius: 8px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
          z-index: 1000;
        }

        .config-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem;
          border-bottom: 1px solid #2a2a2a;
        }

        .config-header h4 {
          margin: 0;
          font-size: 0.9375rem;
          font-weight: 600;
          color: #e5e7eb;
        }

        .config-header button {
          background: none;
          border: none;
          color: #9ca3af;
          font-size: 1.25rem;
          cursor: pointer;
          padding: 0.25rem;
          line-height: 1;
        }

        .config-header button:hover {
          color: #e5e7eb;
        }

        .config-section {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid #2a2a2a;
        }

        .config-section:last-child {
          border-bottom: none;
        }

        .config-section label {
          display: block;
          margin-bottom: 0.5rem;
          font-size: 0.875rem;
          font-weight: 500;
          color: #e5e7eb;
        }

        .config-section select,
        .config-section input[type="range"] {
          width: 100%;
          padding: 0.5rem;
          background: #2a2a2a;
          border: 1px solid #3a3a3a;
          border-radius: 4px;
          color: #e5e7eb;
          font-size: 0.875rem;
        }

        .config-section input[type="range"] {
          padding: 0;
          cursor: pointer;
        }

        .config-section input[type="checkbox"] {
          margin-right: 0.5rem;
          cursor: pointer;
        }

        .config-section select:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .config-actions {
          padding: 1rem;
        }

        .reset-btn {
          width: 100%;
          padding: 0.5rem;
          background: #2a2a2a;
          border: 1px solid #3a3a3a;
          border-radius: 4px;
          color: #9ca3af;
          font-size: 0.875rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
        }

        .reset-btn:hover {
          background: #3a3a3a;
          border-color: #4a4a4a;
          color: #e5e7eb;
        }
      `}</style>
    </div>
  );
};
