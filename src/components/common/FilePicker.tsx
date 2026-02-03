import React, { useRef, useState, useCallback } from 'react';
import { Upload, File as FileIcon, X } from 'lucide-react';
import './FilePicker.css';

interface FilePickerProps {
  file: File | null;
  onChange: (file: File | null) => void;
  accept?: string;
  placeholder?: string;
  description?: string;
  note?: string;
  disabled?: boolean;
}

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
};

// 检查文件类型是否符合 accept 规则
const isFileAccepted = (file: File, accept: string): boolean => {
  if (!accept) return true;

  const acceptedTypes = accept.split(',').map(t => t.trim().toLowerCase());
  const fileName = file.name.toLowerCase();
  const fileType = file.type.toLowerCase();

  return acceptedTypes.some(accepted => {
    // 扩展名匹配 (如 .json, .md)
    if (accepted.startsWith('.')) {
      return fileName.endsWith(accepted);
    }
    // MIME 类型匹配 (如 text/plain, image/*)
    if (accepted.includes('/')) {
      if (accepted.endsWith('/*')) {
        const baseType = accepted.slice(0, -2);
        return fileType.startsWith(baseType);
      }
      return fileType === accepted;
    }
    return false;
  });
};

const FilePicker: React.FC<FilePickerProps> = ({
  file,
  onChange,
  accept = '',
  placeholder = '点击选择文件',
  description,
  note,
  disabled = false,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const dragCounterRef = useRef(0);

  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] || null;
    onChange(selected);
  };

  const handleRemove = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (disabled) return;
    onChange(null);
  };

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (disabled) return;

    dragCounterRef.current++;
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setIsDragging(true);
    }
  }, [disabled]);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (disabled) return;

    dragCounterRef.current--;
    if (dragCounterRef.current === 0) {
      setIsDragging(false);
    }
  }, [disabled]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (disabled) return;

    setIsDragging(false);
    dragCounterRef.current = 0;

    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile) {
      // 检查文件类型是否被接受
      if (accept && !isFileAccepted(droppedFile, accept)) {
        console.warn('文件类型不符合要求:', droppedFile.type, droppedFile.name);
        return;
      }
      onChange(droppedFile);
    }
  }, [disabled, accept, onChange]);

  return (
    <div
      className={`file-picker ${disabled ? 'is-disabled' : ''} ${isDragging ? 'is-dragging' : ''}`}
      onClick={() => {
        if (disabled) return;
        inputRef.current?.click();
      }}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleSelect}
        className="file-picker-input"
        disabled={disabled}
      />

      {file ? (
        <div className="file-picked">
          <FileIcon size={20} />
          <div className="file-picked-info">
            <span className="file-picked-name">{file.name}</span>
            <span className="file-picked-size">{formatFileSize(file.size)}</span>
          </div>
          <button
            type="button"
            className="file-remove"
            onClick={handleRemove}
            aria-label="移除文件"
          >
            <X size={16} />
          </button>
        </div>
      ) : (
        <div className="file-placeholder">
          <Upload size={28} />
          <p className="file-placeholder-title">{placeholder}</p>
          {description && <p className="file-placeholder-desc">{description}</p>}
          {note && <p className="file-placeholder-note">{note}</p>}
        </div>
      )}
    </div>
  );
};

export default FilePicker;
