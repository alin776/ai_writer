import React, { useState, useCallback } from 'react';
import { createPortal } from 'react-dom';
import Cropper from 'react-easy-crop';
import type { Area, Point } from 'react-easy-crop';
import { useTranslation } from 'react-i18next';
import { X } from 'lucide-react';
import { Button } from './index';

/**
 * ImageCropper Props
 */
export interface ImageCropperProps {
  /**
   * Whether the cropper modal is open
   */
  isOpen: boolean;

  /**
   * Image source URL (can be a data URL or blob URL)
   */
  imageSrc: string;

  /**
   * Called when the modal is closed without saving
   */
  onClose: () => void;

  /**
   * Called when the cropped image is saved
   */
  onSave: (croppedImageBlob: Blob) => void;

  /**
   * Aspect ratio of the crop area (default: 1 for square/circle)
   */
  aspect?: number;

  /**
   * Shape of the crop area
   */
  cropShape?: 'rect' | 'round';

  /**
   * Minimum zoom level
   */
  minZoom?: number;

  /**
   * Maximum zoom level
   */
  maxZoom?: number;
}

/**
 * Create a cropped image from the source image and crop area
 */
const createCroppedImage = async (
  imageSrc: string,
  pixelCrop: Area,
  outputSize: number = 256
): Promise<Blob> => {
  const image = new Image();
  image.src = imageSrc;

  await new Promise((resolve) => {
    image.onload = resolve;
  });

  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');

  if (!ctx) {
    throw new Error('Failed to get canvas context');
  }

  // Set canvas size to the desired output size
  canvas.width = outputSize;
  canvas.height = outputSize;

  // Draw the cropped image onto the canvas
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

  // Convert canvas to blob
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
};

/**
 * ImageCropper Component
 *
 * A modal component that allows users to crop images with zoom and pan controls.
 * Perfect for avatar uploads where circular cropping is needed.
 */
const ImageCropper: React.FC<ImageCropperProps> = ({
  isOpen,
  imageSrc,
  onClose,
  onSave,
  aspect = 1,
  cropShape = 'round',
  minZoom = 0.6,
  maxZoom = 3,
}) => {
  const { t } = useTranslation();
  const [crop, setCrop] = useState<Point>({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState<Area | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const onCropComplete = useCallback((_croppedArea: Area, croppedAreaPixels: Area) => {
    setCroppedAreaPixels(croppedAreaPixels);
  }, []);

  const handleSave = async () => {
    if (!croppedAreaPixels) return;

    setIsSaving(true);
    try {
      const croppedImageBlob = await createCroppedImage(imageSrc, croppedAreaPixels);
      onSave(croppedImageBlob);
    } catch (error) {
      console.error('Failed to crop image:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleClose = () => {
    // Reset state when closing
    setCrop({ x: 0, y: 0 });
    setZoom(1);
    setCroppedAreaPixels(null);
    onClose();
  };

  if (!isOpen) {
    return null;
  }

  const modalContent = (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="image-cropper-title"
    >
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black/60 transition-opacity"
        onClick={handleClose}
      />

      {/* Modal */}
      <div className="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md animate-scaleIn">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3
            id="image-cropper-title"
            className="text-lg font-semibold text-gray-900 dark:text-gray-100"
          >
            {t('settings.profile.editImage', '编辑图片')}
          </h3>
          <button
            type="button"
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 rounded-lg p-1"
            aria-label={t('common.close')}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Crop Area */}
        <div className="relative w-full" style={{ height: '300px' }}>
          <Cropper
            image={imageSrc}
            crop={crop}
            zoom={zoom}
            aspect={aspect}
            cropShape={cropShape}
            showGrid={false}
            onCropChange={setCrop}
            onCropComplete={onCropComplete}
            onZoomChange={setZoom}
            minZoom={minZoom}
            maxZoom={maxZoom}
            style={{
              containerStyle: {
                background: '#1a1a2e',
              },
            }}
          />
        </div>

        {/* Zoom Slider */}
        <div className="px-6 py-4">
          <input
            type="range"
            min={minZoom}
            max={maxZoom}
            step={0.1}
            value={zoom}
            onChange={(e) => setZoom(Number(e.target.value))}
            className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2 text-center">
            {t('settings.profile.dragToMove', '*鼠标放置在图片上可拖拽移动图片位置')}
          </p>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-center gap-4 px-6 py-4 border-t border-gray-200 dark:border-gray-700">
          <Button
            variant="outline"
            onClick={handleClose}
            disabled={isSaving}
            className="min-w-[100px]"
          >
            {t('common.cancel')}
          </Button>
          <Button
            variant="primary"
            onClick={handleSave}
            disabled={isSaving || !croppedAreaPixels}
            className="min-w-[100px] bg-red-500 hover:bg-red-600 border-red-500 hover:border-red-600"
          >
            {isSaving ? t('common.saving') : t('common.save', '保存')}
          </Button>
        </div>
      </div>
    </div>
  );

  return createPortal(modalContent, document.body);
};

export default ImageCropper;
