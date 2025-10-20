/**
 * 导入对话框组件
 */
import React, { useState, useRef } from 'react';
import { ImportOptions, ImportPreviewResponse } from '@/types/export';
import { DataService } from '@/services/DataService';
import { Upload, X, FileJson, FileText, File, Loader2, AlertCircle } from 'lucide-react';
import './ImportDialog.css';

interface ImportDialogProps {
  onClose: () => void;
  onSuccess?: (workId: string) => void;
}

const ImportDialog: React.FC<ImportDialogProps> = ({ onClose, onSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [format, setFormat] = useState<'json' | 'markdown' | 'txt'>('json');
  const [preview, setPreview] = useState<ImportPreviewResponse | null>(null);
  const [options, setOptions] = useState({
    includeWorldview: true,
    includeGuidelines: true,
  });
  const [loading, setLoading] = useState(false);
  const [previewing, setPreviewing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // 自动检测文件格式
  const detectFormat = (filename: string): 'json' | 'markdown' | 'txt' => {
    const ext = filename.split('.').pop()?.toLowerCase();
    if (ext === 'json') return 'json';
    if (ext === 'md' || ext === 'markdown') return 'markdown';
    return 'txt';
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setError(null);
    setPreview(null);

    // 自动检测格式
    const detectedFormat = detectFormat(selectedFile.name);
    setFormat(detectedFormat);

    // 自动预览
    await handlePreview(selectedFile, detectedFormat);
  };

  const handlePreview = async (fileToPreview?: File, formatToUse?: string) => {
    const targetFile = fileToPreview || file;
    const targetFormat = formatToUse || format;

    if (!targetFile) return;

    try {
      setPreviewing(true);
      setError(null);

      const previewData = await DataService.previewImport(targetFile, targetFormat);
      setPreview(previewData);
    } catch (err: any) {
      console.error('预览失败:', err);
      setError(err.message || '预览失败，请检查文件格式');
      setPreview(null);
    } finally {
      setPreviewing(false);
    }
  };

  const handleImport = async () => {
    if (!file || !preview) return;

    try {
      setLoading(true);
      setError(null);

      const importOptions: ImportOptions = {
        format,
        createNew: true,
        includeWorldview: options.includeWorldview,
        includeGuidelines: options.includeGuidelines,
      };

      const result = await DataService.importWork(file, importOptions);

      // 显示成功消息
      alert(
        `导入成功！\n` +
        `作品ID: ${result.workId}\n` +
        `章节: ${result.chaptersCreated}个\n` +
        `人物: ${result.charactersCreated}个\n` +
        `地点: ${result.locationsCreated}个`
      );

      // 关闭对话框并回调
      onSuccess?.(result.workId);
      onClose();
    } catch (err: any) {
      console.error('导入失败:', err);
      setError(err.message || '导入失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="import-dialog-overlay" onClick={onClose}>
      <div className="import-dialog" onClick={e => e.stopPropagation()}>
        {/* 标题栏 */}
        <div className="import-dialog-header">
          <h2>
            <Upload size={20} />
            导入作品
          </h2>
          <button onClick={onClose} className="close-button">
            <X size={20} />
          </button>
        </div>

        {/* 文件上传区域 */}
        <div className="form-section">
          <h3>选择文件</h3>
          
          <div
            className="file-upload-area"
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".json,.md,.markdown,.txt"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            
            {file ? (
              <div className="file-selected">
                {format === 'json' ? <FileJson size={32} /> : <FileText size={32} />}
                <div className="file-info">
                  <strong>{file.name}</strong>
                  <span>{formatFileSize(file.size)}</span>
                </div>
              </div>
            ) : (
              <div className="file-placeholder">
                <File size={48} />
                <p>点击选择文件或拖拽到此处</p>
                <span>支持格式：JSON、Markdown、TXT</span>
              </div>
            )}
          </div>

          {file && (
            <div className="format-selector">
              <label>
                <input
                  type="radio"
                  name="format"
                  value="json"
                  checked={format === 'json'}
                  onChange={e => setFormat('json')}
                />
                JSON（完整导入）
              </label>
              <label>
                <input
                  type="radio"
                  name="format"
                  value="markdown"
                  checked={format === 'markdown'}
                  onChange={e => setFormat('markdown')}
                />
                Markdown（智能分割）
              </label>
              <label>
                <input
                  type="radio"
                  name="format"
                  value="txt"
                  checked={format === 'txt'}
                  onChange={e => setFormat('txt')}
                />
                TXT（智能分割）
              </label>
            </div>
          )}
        </div>

        {/* 导入选项（仅JSON格式） */}
        {format === 'json' && file && (
          <div className="form-section">
            <h3>导入选项</h3>
            <div className="import-options">
              <label>
                <input
                  type="checkbox"
                  checked={options.includeWorldview}
                  onChange={e =>
                    setOptions({ ...options, includeWorldview: e.target.checked })
                  }
                />
                导入世界观数据（人物/地点/设定）
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={options.includeGuidelines}
                  onChange={e =>
                    setOptions({ ...options, includeGuidelines: e.target.checked })
                  }
                />
                导入创作规范
              </label>
            </div>
          </div>
        )}

        {/* 预览加载中 */}
        {previewing && (
          <div className="preview-loading">
            <Loader2 size={24} className="spinner" />
            <p>正在分析文件...</p>
          </div>
        )}

        {/* 预览信息 */}
        {preview && !previewing && (
          <div className="form-section preview-section">
            <h3>导入预览</h3>
            
            <div className="preview-info">
              <div className="preview-item">
                <span className="label">作品标题：</span>
                <strong>{preview.work.title}</strong>
              </div>
              
              {preview.work.description && (
                <div className="preview-item">
                  <span className="label">简介：</span>
                  <span>{preview.work.description}</span>
                </div>
              )}
              
              <div className="preview-stats">
                <div className="stat">
                  <strong>{preview.chapters.length}</strong>
                  <span>章节</span>
                </div>
                <div className="stat">
                  <strong>{preview.work.totalWords.toLocaleString()}</strong>
                  <span>字数</span>
                </div>
                {preview.charactersCount > 0 && (
                  <div className="stat">
                    <strong>{preview.charactersCount}</strong>
                    <span>人物</span>
                  </div>
                )}
                {preview.locationsCount > 0 && (
                  <div className="stat">
                    <strong>{preview.locationsCount}</strong>
                    <span>地点</span>
                  </div>
                )}
                {preview.settingsCount > 0 && (
                  <div className="stat">
                    <strong>{preview.settingsCount}</strong>
                    <span>设定</span>
                  </div>
                )}
              </div>

              {/* 章节列表预览（前5章） */}
              {preview.chapters.length > 0 && (
                <div className="chapters-preview">
                  <h4>章节列表</h4>
                  <div className="chapter-list">
                    {preview.chapters.slice(0, 5).map((chapter, idx) => (
                      <div key={idx} className="chapter-item">
                        <span className="chapter-title">{chapter.title}</span>
                        <span className="chapter-words">
                          {chapter.wordCount.toLocaleString()}字
                        </span>
                      </div>
                    ))}
                    {preview.chapters.length > 5 && (
                      <div className="chapter-item more">
                        <span>...还有 {preview.chapters.length - 5} 章</span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* 警告信息 */}
              {preview.warnings.length > 0 && (
                <div className="warnings">
                  <AlertCircle size={16} />
                  <div>
                    {preview.warnings.map((warning, idx) => (
                      <p key={idx}>{warning}</p>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* 错误提示 */}
        {error && (
          <div className="error-message">
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        {/* 操作按钮 */}
        <div className="import-dialog-footer">
          <button
            onClick={onClose}
            className="button button-secondary"
            disabled={loading || previewing}
          >
            取消
          </button>
          
          {file && !preview && !previewing && (
            <button
              onClick={() => handlePreview()}
              className="button button-secondary"
            >
              <FileText size={16} />
              预览
            </button>
          )}
          
          <button
            onClick={handleImport}
            className="button button-primary"
            disabled={!preview || loading || previewing}
          >
            {loading ? (
              <>
                <Loader2 size={16} className="spinner" />
                导入中...
              </>
            ) : (
              <>
                <Upload size={16} />
                确认导入
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImportDialog;
