/**
 * 文件上传组件
 * 支持拖拽上传和点击上传
 */
import { useState, useRef, useCallback } from 'react';
import { Upload, X, File, Image, FileText, Archive, Video, Music, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { uploadAttachment, type AttachmentUploadResponse } from '@/services/channelApi';
import { useGlobalStore } from '@/store/globalStore';

export interface UploadedFile {
  id: string;
  fileName: string;
  fileType?: string;
  fileSize: number;
  fileUrl: string;
  thumbnailUrl?: string;
  uploading?: boolean;
  error?: string;
}

interface FileUploaderProps {
  channelId: string;
  onFilesUploaded: (files: UploadedFile[]) => void;
  uploadedFiles: UploadedFile[];
  disabled?: boolean;
  maxFiles?: number;
  maxFileSize?: number; // 字节
}

// 允许的文件类型
export const ALLOWED_TYPES = [
  // 图片
  'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp',
  // 文档
  'application/pdf', 'text/plain',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  // 压缩包
  'application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed',
  // 视频
  'video/mp4', 'video/webm',
  // 音频
  'audio/mpeg', 'audio/wav', 'audio/ogg',
];

// 获取文件图标
export const getFileIcon = (fileType: string | undefined) => {
  if (!fileType) return File;
  if (fileType.startsWith('image/')) return Image;
  if (fileType.startsWith('video/')) return Video;
  if (fileType.startsWith('audio/')) return Music;
  if (fileType.includes('pdf') || fileType.includes('document') || fileType.includes('text')) return FileText;
  if (fileType.includes('zip') || fileType.includes('rar') || fileType.includes('7z')) return Archive;
  return File;
};

// 格式化文件大小
export const formatFileSize = (bytes: number): string => {
  if (!bytes || isNaN(bytes)) return '0 B';
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
};

/**
 * 文件预览组件 - 用于在输入框上方显示已上传的文件
 */
export function FilePreview({
  files,
  onRemove,
}: {
  files: UploadedFile[];
  onRemove: (fileId: string) => void;
}) {
  if (files.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2 mb-2">
      {files.map((file) => {
        const FileIcon = getFileIcon(file.fileType);
        const isImage = file.fileType?.startsWith('image/') ?? false;

        return (
          <div
            key={file.id}
            className="relative group"
          >
            {/* 图片缩略图 */}
            {isImage && (file.thumbnailUrl || file.fileUrl) ? (
              <div className="relative w-16 h-16 rounded-lg overflow-hidden border border-gray-200 dark:border-slate-600">
                <img
                  src={file.thumbnailUrl || file.fileUrl}
                  alt={file.fileName}
                  className="w-full h-full object-cover"
                />
                {/* 删除按钮 */}
                <button
                  onClick={() => onRemove(file.id)}
                  className="absolute -top-1.5 -right-1.5 w-5 h-5 bg-black/70 hover:bg-black text-white rounded-full flex items-center justify-center transition-colors z-10"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>
            ) : (
              /* 文件卡片 */
              <div className="flex items-center gap-2 px-3 py-2 bg-gray-100 dark:bg-slate-700 rounded-lg border border-gray-200 dark:border-slate-600">
                <FileIcon className="w-5 h-5 text-gray-500 dark:text-slate-400 flex-shrink-0" />
                <div className="min-w-0 max-w-[100px]">
                  <div className="text-xs font-medium truncate dark:text-slate-200">
                    {file.fileName}
                  </div>
                  <div className="text-[10px] text-gray-500 dark:text-slate-400">
                    {formatFileSize(file.fileSize)}
                  </div>
                </div>
                {/* 删除按钮 */}
                <button
                  onClick={() => onRemove(file.id)}
                  className="w-5 h-5 bg-gray-200 dark:bg-slate-600 hover:bg-red-500 hover:text-white text-gray-500 dark:text-slate-400 rounded-full flex items-center justify-center transition-colors flex-shrink-0"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

/**
 * 文件上传按钮组件 - 只包含上传按钮
 */
export function FileUploader({
  channelId,
  onFilesUploaded,
  uploadedFiles,
  disabled = false,
  maxFiles = 5,
  maxFileSize = 10 * 1024 * 1024 // 10MB
}: FileUploaderProps) {
  const [uploadingFiles, setUploadingFiles] = useState<Map<string, number>>(new Map());
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { error: showError, warning: showWarning } = useGlobalStore();

  const validateFile = (file: File): string | null => {
    if (!ALLOWED_TYPES.includes(file.type)) {
      return `不支持的文件类型: ${file.type || '未知'}`;
    }
    if (file.size > maxFileSize) {
      return `文件大小超过限制（最大 ${formatFileSize(maxFileSize)}）`;
    }
    return null;
  };

  const uploadFile = async (file: File): Promise<UploadedFile | null> => {
    const tempId = `temp-${Date.now()}-${Math.random().toString(36).slice(2)}`;

    try {
      const error = validateFile(file);
      if (error) {
        showError(error);
        return null;
      }

      setUploadingFiles(prev => new Map(prev).set(tempId, 0));

      const response = await uploadAttachment(channelId, file);
      console.log('[FileUploader] Upload response:', response);

      setUploadingFiles(prev => {
        const newMap = new Map(prev);
        newMap.delete(tempId);
        return newMap;
      });

      // ApiAdapter 已经转换为 camelCase
      return {
        id: response.id,
        fileName: response.fileName || file.name,
        fileType: response.fileType || file.type,
        fileSize: response.fileSize || file.size,
        fileUrl: response.fileUrl || '',
        thumbnailUrl: response.thumbnailUrl,
      };
    } catch (err) {
      setUploadingFiles(prev => {
        const newMap = new Map(prev);
        newMap.delete(tempId);
        return newMap;
      });
      showError(`上传失败: ${file.name}`);
      return null;
    }
  };

  const handleFiles = async (files: FileList | File[]) => {
    const fileArray = Array.from(files);
    const remainingSlots = maxFiles - uploadedFiles.length;

    if (remainingSlots <= 0) {
      showWarning(`最多只能上传 ${maxFiles} 个文件`);
      return;
    }

    if (fileArray.length > remainingSlots) {
      showWarning(`最多只能上传 ${maxFiles} 个文件，已自动截取前 ${remainingSlots} 个`);
    }

    const filesToUpload = fileArray.slice(0, remainingSlots);
    const uploadedResults: UploadedFile[] = [];

    for (const file of filesToUpload) {
      const result = await uploadFile(file);
      if (result) {
        uploadedResults.push(result);
      }
    }

    if (uploadedResults.length > 0) {
      onFilesUploaded(uploadedResults);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFiles(files);
    }
    e.target.value = '';
  };

  const isUploading = uploadingFiles.size > 0;

  return (
    <>
      <button
        type="button"
        onClick={() => fileInputRef.current?.click()}
        disabled={disabled || uploadedFiles.length >= maxFiles || isUploading}
        className={cn(
          "p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg text-gray-500 dark:text-slate-400 transition-colors",
          "disabled:opacity-30 disabled:cursor-not-allowed"
        )}
        title={isUploading ? '正在上传...' : '上传文件'}
      >
        {isUploading ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : (
          <Upload className="w-4 h-4" />
        )}
      </button>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept={ALLOWED_TYPES.join(',')}
        onChange={handleInputChange}
        className="hidden"
      />
    </>
  );
}

export default FileUploader;
