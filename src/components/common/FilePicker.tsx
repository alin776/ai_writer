import React, { useRef } from 'react';
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

  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] || null;
    onChange(selected);
  };

  const handleRemove = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (disabled) return;
    onChange(null);
  };

  return (
    <div
      className={`file-picker ${disabled ? 'is-disabled' : ''}`}
      onClick={() => {
        if (disabled) return;
        inputRef.current?.click();
      }}
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
