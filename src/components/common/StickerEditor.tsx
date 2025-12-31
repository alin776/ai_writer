import React, { useState, useRef, useCallback, useEffect } from 'react';
import { createPortal } from 'react-dom';
import Cropper from 'react-easy-crop';
import type { Area, Point } from 'react-easy-crop';
import { X, RotateCw, Minus, Plus } from 'lucide-react';
import { Button } from './index';

interface TextOverlay {
  id: string;
  text: string;
  x: number; // 百分比位置 0-100
  y: number;
  color: string;
  fontSize: number;
  fontWeight: 'normal' | 'bold';
  rotation: number; // 旋转角度
}

export interface StickerEditorProps {
  isOpen: boolean;
  imageSrc: string;
  onClose: () => void;
  onSave: (croppedImageBlob: Blob) => void;
  aspect?: number;
}

const COLORS = [
  '#ffffff', '#000000', '#ff0000', '#00ff00',
  '#0000ff', '#ffff00', '#ff00ff', '#00ffff',
  '#ff6600', '#9900ff'
];

const StickerEditor: React.FC<StickerEditorProps> = ({
  isOpen,
  imageSrc,
  onClose,
  onSave,
  aspect = 1,
}) => {
  const [crop, setCrop] = useState<Point>({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState<Area | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  // 文字叠加层
  const [textOverlays, setTextOverlays] = useState<TextOverlay[]>([]);
  const [selectedTextId, setSelectedTextId] = useState<string | null>(null);
  const [currentColor, setCurrentColor] = useState('#ffffff');
  const [isAddingText, setIsAddingText] = useState(false);
  const [newTextPosition, setNewTextPosition] = useState<{x: number, y: number} | null>(null);
  const [newTextValue, setNewTextValue] = useState('');
  const newTextInputRef = useRef<HTMLInputElement>(null);

  // 拖拽状态
  const [draggingId, setDraggingId] = useState<string | null>(null);
  const overlayRef = useRef<HTMLDivElement>(null);

  // 缩放拖拽状态
  const [resizingId, setResizingId] = useState<string | null>(null);
  const [rotatingId, setRotatingId] = useState<string | null>(null);
  const startPosRef = useRef<{x: number, y: number, fontSize: number, rotation: number}>({x: 0, y: 0, fontSize: 24, rotation: 0});

  const onCropComplete = useCallback((_croppedArea: Area, croppedAreaPixels: Area) => {
    setCroppedAreaPixels(croppedAreaPixels);
  }, []);

  // 点击图片区域添加文字
  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (draggingId) return;

    const rect = overlayRef.current?.getBoundingClientRect();
    if (!rect) return;

    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;

    // 检查是否点击在已有文字上
    const clickedOnText = textOverlays.some(text => {
      const textX = text.x;
      const textY = text.y;
      const threshold = 10; // 点击范围
      return Math.abs(x - textX) < threshold && Math.abs(y - textY) < threshold;
    });

    if (!clickedOnText) {
      setNewTextPosition({ x: Math.max(5, Math.min(95, x)), y: Math.max(5, Math.min(95, y)) });
      setIsAddingText(true);
      setNewTextValue('');
      setSelectedTextId(null);
      setTimeout(() => newTextInputRef.current?.focus(), 100);
    }
  };

  // 确认添加文字
  const handleConfirmNewText = () => {
    if (!newTextValue.trim() || !newTextPosition) {
      setIsAddingText(false);
      setNewTextPosition(null);
      return;
    }

    const newText: TextOverlay = {
      id: Date.now().toString(),
      text: newTextValue,
      x: newTextPosition.x,
      y: newTextPosition.y,
      color: currentColor,
      fontSize: 24,
      fontWeight: 'bold',
      rotation: 0,
    };
    setTextOverlays(prev => [...prev, newText]);
    setSelectedTextId(newText.id);
    setIsAddingText(false);
    setNewTextPosition(null);
    setNewTextValue('');
  };

  // 删除文字
  const handleDeleteText = (id: string) => {
    setTextOverlays(prev => prev.filter(t => t.id !== id));
    if (selectedTextId === id) {
      setSelectedTextId(null);
    }
  };

  // 选中文字
  const handleSelectText = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    setSelectedTextId(id);
    setIsAddingText(false);
  };

  // 更新选中文字的属性
  const updateSelectedText = (updates: Partial<TextOverlay>) => {
    if (!selectedTextId) return;
    setTextOverlays(prev => prev.map(t =>
      t.id === selectedTextId ? { ...t, ...updates } : t
    ));
  };

  // 更改颜色
  const handleColorChange = (color: string) => {
    setCurrentColor(color);
    if (selectedTextId) {
      updateSelectedText({ color });
    }
  };

  // 开始缩放
  const handleResizeStart = (e: React.MouseEvent | React.TouchEvent, id: string) => {
    e.preventDefault();
    e.stopPropagation();
    const text = textOverlays.find(t => t.id === id);
    if (!text || !overlayRef.current) return;

    const rect = overlayRef.current.getBoundingClientRect();
    const centerX = rect.left + (text.x / 100) * rect.width;
    const centerY = rect.top + (text.y / 100) * rect.height;

    let clientX: number, clientY: number;
    if ('touches' in e) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }

    // 记录起始距离
    const startDist = Math.sqrt(Math.pow(clientX - centerX, 2) + Math.pow(clientY - centerY, 2));
    startPosRef.current = { x: centerX, y: centerY, fontSize: text.fontSize, rotation: startDist };
    setResizingId(id);
    setSelectedTextId(id);
  };

  // 开始旋转
  const handleRotateStart = (e: React.MouseEvent | React.TouchEvent, id: string) => {
    e.preventDefault();
    e.stopPropagation();
    const text = textOverlays.find(t => t.id === id);
    if (!text || !overlayRef.current) return;

    const rect = overlayRef.current.getBoundingClientRect();
    const centerX = rect.left + (text.x / 100) * rect.width;
    const centerY = rect.top + (text.y / 100) * rect.height;

    let clientX: number, clientY: number;
    if ('touches' in e) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }

    const startAngle = Math.atan2(clientY - centerY, clientX - centerX) * 180 / Math.PI;
    startPosRef.current = { x: centerX, y: centerY, fontSize: text.fontSize, rotation: text.rotation - startAngle };
    setRotatingId(id);
    setSelectedTextId(id);
  };

  // 拖拽开始
  const handleDragStart = (e: React.MouseEvent | React.TouchEvent, id: string) => {
    e.preventDefault();
    e.stopPropagation();
    setDraggingId(id);
    setSelectedTextId(id);
  };

  // 拖拽/缩放/旋转移动
  const handleDragMove = useCallback((e: MouseEvent | TouchEvent) => {
    let clientX: number, clientY: number;
    if ('touches' in e) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }

    // 缩放 - 根据与中心点距离变化
    if (resizingId && overlayRef.current) {
      const currentDist = Math.sqrt(
        Math.pow(clientX - startPosRef.current.x, 2) +
        Math.pow(clientY - startPosRef.current.y, 2)
      );
      const startDist = startPosRef.current.rotation; // 存储在 rotation 字段
      const scale = currentDist / startDist;
      const newSize = Math.max(12, Math.min(72, startPosRef.current.fontSize * scale));
      setTextOverlays(prev => prev.map(t =>
        t.id === resizingId ? { ...t, fontSize: Math.round(newSize) } : t
      ));
      return;
    }

    // 旋转
    if (rotatingId && overlayRef.current) {
      const angle = Math.atan2(clientY - startPosRef.current.y, clientX - startPosRef.current.x) * 180 / Math.PI;
      const newRotation = (startPosRef.current.rotation + angle) % 360;
      setTextOverlays(prev => prev.map(t =>
        t.id === rotatingId ? { ...t, rotation: Math.round(newRotation) } : t
      ));
      return;
    }

    // 移动
    if (draggingId && overlayRef.current) {
      const rect = overlayRef.current.getBoundingClientRect();
      const x = ((clientX - rect.left) / rect.width) * 100;
      const y = ((clientY - rect.top) / rect.height) * 100;
      setTextOverlays(prev => prev.map(t =>
        t.id === draggingId
          ? { ...t, x: Math.max(5, Math.min(95, x)), y: Math.max(5, Math.min(95, y)) }
          : t
      ));
    }
  }, [draggingId, resizingId, rotatingId]);

  // 拖拽结束
  const handleDragEnd = useCallback(() => {
    setDraggingId(null);
    setResizingId(null);
    setRotatingId(null);
  }, []);

  // 绑定拖拽事件
  useEffect(() => {
    if (draggingId || resizingId || rotatingId) {
      document.addEventListener('mousemove', handleDragMove);
      document.addEventListener('mouseup', handleDragEnd);
      document.addEventListener('touchmove', handleDragMove);
      document.addEventListener('touchend', handleDragEnd);
    }
    return () => {
      document.removeEventListener('mousemove', handleDragMove);
      document.removeEventListener('mouseup', handleDragEnd);
      document.removeEventListener('touchmove', handleDragMove);
      document.removeEventListener('touchend', handleDragEnd);
    };
  }, [draggingId, resizingId, rotatingId, handleDragMove, handleDragEnd]);

  // 保存图片（包含文字）
  const handleSave = async () => {
    if (!croppedAreaPixels) return;

    setIsSaving(true);
    try {
      const blob = await createImageWithText(imageSrc, croppedAreaPixels, textOverlays);
      onSave(blob);
    } catch (error) {
      console.error('Failed to save image:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleClose = () => {
    setCrop({ x: 0, y: 0 });
    setZoom(1);
    setCroppedAreaPixels(null);
    setTextOverlays([]);
    setSelectedTextId(null);
    setIsAddingText(false);
    setNewTextPosition(null);
    onClose();
  };

  if (!isOpen) return null;

  const modalContent = (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
    >
      {/* Overlay */}
      <div className="fixed inset-0 bg-black/60" onClick={handleClose} />

      {/* Modal */}
      <div className="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            编辑表情包
          </h3>
          <button
            type="button"
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors p-1 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Crop Area with Text Overlay */}
        <div className="relative w-full" style={{ height: '300px' }}>
          <Cropper
            image={imageSrc}
            crop={crop}
            zoom={zoom}
            aspect={aspect}
            cropShape="rect"
            showGrid={false}
            onCropChange={setCrop}
            onCropComplete={onCropComplete}
            onZoomChange={setZoom}
            minZoom={0.6}
            maxZoom={3}
            style={{
              containerStyle: { background: '#1a1a2e' },
            }}
          />

          {/* 文字叠加层 - 可点击添加文字 */}
          <div
            ref={overlayRef}
            className="absolute inset-0 cursor-crosshair"
            style={{ zIndex: 10 }}
            onClick={handleOverlayClick}
          >
            {/* 已添加的文字 */}
            {textOverlays.map(text => (
              <div
                key={text.id}
                className="absolute"
                style={{
                  left: `${text.x}%`,
                  top: `${text.y}%`,
                  transform: `translate(-50%, -50%) rotate(${text.rotation}deg)`,
                }}
                onClick={(e) => handleSelectText(e, text.id)}
              >
                {/* 选中时的边框和手柄 */}
                {selectedTextId === text.id && (
                  <>
                    {/* 边框 */}
                    <div
                      className="absolute inset-[-4px] border-2 border-blue-500 pointer-events-none"
                      style={{ borderRadius: '2px' }}
                    />
                    {/* 右下角缩放手柄 */}
                    <div
                      className="absolute w-4 h-4 bg-blue-500 rounded-full cursor-nwse-resize flex items-center justify-center"
                      style={{ right: '-8px', bottom: '-8px' }}
                      onMouseDown={(e) => handleResizeStart(e, text.id)}
                      onTouchStart={(e) => handleResizeStart(e, text.id)}
                    >
                      <Plus className="w-2.5 h-2.5 text-white" />
                    </div>
                    {/* 左下角缩放手柄 */}
                    <div
                      className="absolute w-4 h-4 bg-blue-500 rounded-full cursor-nesw-resize flex items-center justify-center"
                      style={{ left: '-8px', bottom: '-8px' }}
                      onMouseDown={(e) => handleResizeStart(e, text.id)}
                      onTouchStart={(e) => handleResizeStart(e, text.id)}
                    >
                      <Minus className="w-2.5 h-2.5 text-white" />
                    </div>
                    {/* 顶部旋转手柄 */}
                    <div
                      className="absolute w-4 h-4 bg-green-500 rounded-full cursor-grab flex items-center justify-center"
                      style={{ left: '50%', top: '-20px', transform: 'translateX(-50%)' }}
                      onMouseDown={(e) => handleRotateStart(e, text.id)}
                      onTouchStart={(e) => handleRotateStart(e, text.id)}
                    >
                      <RotateCw className="w-2.5 h-2.5 text-white" />
                    </div>
                    {/* 连接线 */}
                    <div
                      className="absolute w-0.5 h-4 bg-green-500"
                      style={{ left: '50%', top: '-16px', transform: 'translateX(-50%)' }}
                    />
                    {/* 删除按钮 */}
                    <div
                      className="absolute w-4 h-4 bg-red-500 rounded-full cursor-pointer flex items-center justify-center"
                      style={{ right: '-8px', top: '-8px' }}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteText(text.id);
                      }}
                    >
                      <X className="w-2.5 h-2.5 text-white" />
                    </div>
                  </>
                )}
                {/* 文字内容 */}
                <div
                  className="cursor-move select-none px-1"
                  style={{
                    color: text.color,
                    fontSize: `${text.fontSize}px`,
                    fontWeight: text.fontWeight,
                    textShadow: '2px 2px 4px rgba(0,0,0,0.8), -1px -1px 2px rgba(0,0,0,0.5)',
                    whiteSpace: 'nowrap',
                  }}
                  onMouseDown={(e) => handleDragStart(e, text.id)}
                  onTouchStart={(e) => handleDragStart(e, text.id)}
                >
                  {text.text}
                </div>
              </div>
            ))}

            {/* 正在添加的文字输入框 - 从点击位置开始 */}
            {isAddingText && newTextPosition && (
              <div
                className="absolute"
                style={{
                  left: `${newTextPosition.x}%`,
                  top: `${newTextPosition.y}%`,
                }}
                onClick={(e) => e.stopPropagation()}
              >
                <input
                  ref={newTextInputRef}
                  type="text"
                  value={newTextValue}
                  onChange={(e) => setNewTextValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleConfirmNewText();
                    if (e.key === 'Escape') {
                      setIsAddingText(false);
                      setNewTextPosition(null);
                    }
                  }}
                  onBlur={handleConfirmNewText}
                  placeholder="输入文字"
                  className="px-2 py-1 text-sm border border-blue-400 rounded-lg bg-white/90 dark:bg-gray-800/90 text-gray-900 dark:text-white shadow-lg backdrop-blur-sm"
                  style={{
                    color: currentColor,
                    width: 'auto',
                    minWidth: '80px',
                    maxWidth: '150px',
                  }}
                  autoFocus
                />
              </div>
            )}
          </div>
        </div>

        {/* 工具栏 */}
        <div className="px-6 py-3 border-t border-gray-200 dark:border-gray-700">
          {/* 提示文字 */}
          <p className="text-xs text-gray-400 mb-2">
            点击图片任意位置添加文字，拖拽可移动
          </p>

          {/* 缩放控制 */}
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xs text-gray-500 dark:text-gray-400 w-8">缩放</span>
            <input
              type="range"
              min={0.6}
              max={3}
              step={0.1}
              value={zoom}
              onChange={(e) => setZoom(Number(e.target.value))}
              className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
          </div>

          {/* 颜色选择 - 带选中效果 */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-500 dark:text-gray-400 w-8">颜色</span>
            <div className="flex gap-1.5 flex-wrap">
              {COLORS.map(color => (
                <button
                  key={color}
                  className={`w-6 h-6 rounded-full transition-all ${
                    currentColor === color
                      ? 'ring-2 ring-offset-2 ring-blue-500 scale-110'
                      : 'hover:scale-105'
                  }`}
                  style={{
                    backgroundColor: color,
                    border: color === '#ffffff' ? '1px solid #ccc' : 'none',
                  }}
                  onClick={() => handleColorChange(color)}
                  title={color}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-center gap-4 px-6 py-4 border-t border-gray-200 dark:border-gray-700">
          <Button variant="outline" onClick={handleClose} disabled={isSaving}>
            取消
          </Button>
          <Button
            variant="primary"
            onClick={handleSave}
            disabled={isSaving || !croppedAreaPixels}
            className="bg-red-500 hover:bg-red-600 border-red-500"
          >
            {isSaving ? '保存中...' : '保存'}
          </Button>
        </div>
      </div>
    </div>
  );

  return createPortal(modalContent, document.body);
};

/**
 * 创建带文字的图片
 */
async function createImageWithText(
  imageSrc: string,
  pixelCrop: Area,
  textOverlays: TextOverlay[],
  outputSize: number = 256
): Promise<Blob> {
  const image = new Image();
  image.crossOrigin = 'anonymous';
  image.src = imageSrc;

  await new Promise((resolve) => {
    image.onload = resolve;
  });

  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');

  if (!ctx) {
    throw new Error('Failed to get canvas context');
  }

  canvas.width = outputSize;
  canvas.height = outputSize;

  // 绘制裁剪后的图片
  ctx.drawImage(
    image,
    pixelCrop.x,
    pixelCrop.y,
    pixelCrop.width,
    pixelCrop.height,
    0,
    0,
    outputSize,
    outputSize
  );

  // 绘制文字（支持旋转）
  textOverlays.forEach(text => {
    const x = (text.x / 100) * outputSize;
    const y = (text.y / 100) * outputSize;
    const fontSize = (text.fontSize / 300) * outputSize; // 按比例缩放字体

    ctx.save(); // 保存当前状态

    // 移动到文字位置并旋转
    ctx.translate(x, y);
    ctx.rotate((text.rotation * Math.PI) / 180);

    ctx.font = `${text.fontWeight} ${fontSize}px sans-serif`;
    ctx.fillStyle = text.color;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // 文字阴影效果
    ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
    ctx.shadowBlur = 4;
    ctx.shadowOffsetX = 2;
    ctx.shadowOffsetY = 2;

    ctx.fillText(text.text, 0, 0); // 在原点绘制（因为已经平移过了）

    ctx.restore(); // 恢复状态
  });

  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => {
        if (blob) {
          resolve(blob);
        } else {
          reject(new Error('Failed to create blob'));
        }
      },
      'image/png',
      1
    );
  });
}

export default StickerEditor;
