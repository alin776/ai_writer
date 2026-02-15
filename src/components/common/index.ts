/**
 * 通用组件导出文件
 *
 * 该文件统一导出所有通用组件，方便在其他模块中导入使用
 *
 * @example
 * ```tsx
 * import { Button, Input, Modal, Loading, Toast, Card } from '@/components/common';
 * ```
 */

export { default as Button } from './Button';
export type { ButtonProps, ButtonVariant, ButtonSize } from './Button';

export { default as Input } from './Input';
export type { InputProps, InputType } from './Input';

export { default as Modal } from './Modal';
export type { ModalProps } from './Modal';

export { default as Loading } from './Loading';
export type { LoadingProps, LoadingSize } from './Loading';

export { default as Toast } from './Toast';

export { default as Card, CardHeader, CardContent, CardFooter } from './Card';
export type { CardProps, CardHeaderProps, CardContentProps, CardFooterProps } from './Card';

export { default as ConfirmDialog } from './ConfirmDialog';
export { default as ErrorBoundary } from './ErrorBoundary';

export { default as ImageCropper } from './ImageCropper';
export type { ImageCropperProps } from './ImageCropper';
