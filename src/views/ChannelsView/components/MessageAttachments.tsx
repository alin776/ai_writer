/**
 * 消息附件显示组件
 * 用于在消息气泡中显示附件（图片、文件等）
 */
import { useState } from 'react';
import { File, Image, FileText, Archive, Video, Music, Download, ExternalLink, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { MessageAttachment as AttachmentType } from '@/services/channelApi';

interface MessageAttachmentProps {
  attachments: AttachmentType[];
  className?: string;
}

// 获取文件图标
const getFileIcon = (fileType: string | undefined) => {
  if (!fileType) return File;
  if (fileType.startsWith('image/')) return Image;
  if (fileType.startsWith('video/')) return Video;
  if (fileType.startsWith('audio/')) return Music;
  if (fileType.includes('pdf') || fileType.includes('document') || fileType.includes('text')) return FileText;
  if (fileType.includes('zip') || fileType.includes('rar') || fileType.includes('7z')) return Archive;
  return File;
};

// 格式化文件大小
const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
};

// 图片预览模态框
function ImagePreviewModal({ src, alt, onClose }: { src: string; alt: string; onClose: () => void }) {
  return (
    <div
      className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <button
        onClick={onClose}
        className="absolute top-4 right-4 p-2 bg-white/10 hover:bg-white/20 rounded-full text-white transition-colors"
      >
        <X className="w-6 h-6" />
      </button>
      <img
        src={src}
        alt={alt}
        className="max-w-full max-h-full object-contain rounded-lg"
        onClick={(e) => e.stopPropagation()}
      />
    </div>
  );
}

// 在新标签页中打开图片（避免被浏览器当作下载）
const openImageInNewTab = (imageUrl: string, fileName: string) => {
  // 创建一个包含图片的 HTML 页面
  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>${fileName}</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          background: #1a1a1a;
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }
        img {
          max-width: 100%;
          max-height: 100vh;
          object-fit: contain;
          border-radius: 8px;
          box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
      </style>
    </head>
    <body>
      <img src="${imageUrl}" alt="${fileName}" />
    </body>
    </html>
  `;

  const blob = new Blob([htmlContent], { type: 'text/html' });
  const blobUrl = URL.createObjectURL(blob);
  window.open(blobUrl, '_blank');

  // 延迟清理 Blob URL
  setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
};

// 单个图片附件
function ImageAttachment({ attachment }: { attachment: AttachmentType }) {
  const [showPreview, setShowPreview] = useState(false);
  const [imageError, setImageError] = useState(false);

  if (imageError) {
    // 图片加载失败，显示为文件
    return <FileAttachment attachment={attachment} />;
  }

  return (
    <>
      <div className="relative group/image cursor-pointer inline-block" onClick={() => setShowPreview(true)}>
        <img
          src={attachment.thumbnailUrl || attachment.fileUrl}
          alt={attachment.fileName}
          className="max-w-[500px] max-h-[300px] rounded-lg object-cover block"
          onError={() => setImageError(true)}
        />
        {/* 悬浮操作 */}
        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover/image:opacity-100 transition-opacity rounded-lg flex items-center justify-center gap-2">
          <button
            onClick={(e) => {
              e.stopPropagation();
              openImageInNewTab(attachment.fileUrl, attachment.fileName);
            }}
            className="p-2 bg-white/20 hover:bg-white/30 rounded-full text-white transition-colors"
            title="在新窗口打开"
          >
            <ExternalLink className="w-4 h-4" />
          </button>
          <a
            href={attachment.fileUrl}
            download={attachment.fileName}
            onClick={(e) => e.stopPropagation()}
            className="p-2 bg-white/20 hover:bg-white/30 rounded-full text-white transition-colors"
            title="下载"
          >
            <Download className="w-4 h-4" />
          </a>
        </div>
      </div>

      {/* 图片预览模态框 */}
      {showPreview && (
        <ImagePreviewModal
          src={attachment.fileUrl}
          alt={attachment.fileName}
          onClose={() => setShowPreview(false)}
        />
      )}
    </>
  );
}

// 视频附件
function VideoAttachment({ attachment }: { attachment: AttachmentType }) {
  return (
    <div className="max-w-[400px]">
      <video
        src={attachment.fileUrl}
        controls
        className="rounded-lg w-full"
        preload="metadata"
      >
        您的浏览器不支持视频播放
      </video>
      <div className="text-[10px] text-gray-500 dark:text-slate-400 mt-1">
        {attachment.fileName} ({formatFileSize(attachment.fileSize)})
      </div>
    </div>
  );
}

// 音频附件
function AudioAttachment({ attachment }: { attachment: AttachmentType }) {
  return (
    <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-slate-800/50 rounded-lg max-w-[300px]">
      <Music className="w-8 h-8 text-purple-500" />
      <div className="flex-1 min-w-0">
        <div className="text-sm font-medium truncate dark:text-slate-200">
          {attachment.fileName}
        </div>
        <audio
          src={attachment.fileUrl}
          controls
          className="w-full h-8 mt-1"
          preload="metadata"
        />
      </div>
    </div>
  );
}

// 普通文件附件
function FileAttachment({ attachment }: { attachment: AttachmentType }) {
  const FileIcon = getFileIcon(attachment.fileType);

  return (
    <a
      href={attachment.fileUrl}
      download={attachment.fileName}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-slate-800/50 hover:bg-gray-100 dark:hover:bg-slate-700/50 rounded-lg max-w-[300px] transition-colors group"
    >
      <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center flex-shrink-0">
        <FileIcon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-sm font-medium truncate dark:text-slate-200 group-hover:text-blue-600 dark:group-hover:text-blue-400">
          {attachment.fileName}
        </div>
        <div className="text-xs text-gray-500 dark:text-slate-400">
          {formatFileSize(attachment.fileSize)}
        </div>
      </div>
      <Download className="w-4 h-4 text-gray-400 group-hover:text-blue-500 transition-colors flex-shrink-0" />
    </a>
  );
}

export function MessageAttachments({ attachments, className }: MessageAttachmentProps) {
  if (!attachments || attachments.length === 0) {
    return null;
  }

  // 分离图片和其他文件
  const images = attachments.filter(a => a.fileType?.startsWith('image/'));
  const videos = attachments.filter(a => a.fileType?.startsWith('video/'));
  const audios = attachments.filter(a => a.fileType?.startsWith('audio/'));
  const files = attachments.filter(a =>
    !a.fileType?.startsWith('image/') &&
    !a.fileType?.startsWith('video/') &&
    !a.fileType?.startsWith('audio/')
  );

  return (
    <div className={cn("space-y-2 mt-2 w-fit", className)}>
      {/* 图片网格 */}
      {images.length > 0 && (
        <div className={cn(
          "inline-flex flex-wrap gap-2 w-fit",
          images.length > 1 && "max-w-[400px]"
        )}>
          {images.map((img) => (
            <ImageAttachment key={img.id} attachment={img} />
          ))}
        </div>
      )}

      {/* 视频列表 */}
      {videos.map((video) => (
        <VideoAttachment key={video.id} attachment={video} />
      ))}

      {/* 音频列表 */}
      {audios.map((audio) => (
        <AudioAttachment key={audio.id} attachment={audio} />
      ))}

      {/* 文件列表 */}
      {files.length > 0 && (
        <div className="space-y-1">
          {files.map((file) => (
            <FileAttachment key={file.id} attachment={file} />
          ))}
        </div>
      )}
    </div>
  );
}

export default MessageAttachments;
