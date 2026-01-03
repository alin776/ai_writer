import React, { useState, useRef, useEffect } from 'react';
import { ImportOptions, ImportPreviewResponse } from '@/types/export';
import type { Work } from '@/types';
import { DataService } from '@/services/DataService';
import { Upload, X, FileText, Loader2, AlertCircle } from 'lucide-react';
import FilePicker from '@/components/common/FilePicker';
import './ImportDialog.css';

interface ImportDialogProps {
  onClose: () => void;
  onSuccess?: (workId: string) => void;
}

const detectFormat = (filename: string): 'json' | 'markdown' | 'txt' => {
  const ext = filename.split('.').pop()?.toLowerCase();
  if (ext === 'json') return 'json';
  if (ext === 'md' || ext === 'markdown') return 'markdown';
  return 'txt';
};

// 检查文件类型是否被接受
const isFileAccepted = (file: File, accept: string): boolean => {
  if (!accept) return true;
  const acceptedTypes = accept.split(',').map(t => t.trim().toLowerCase());
  const fileName = file.name.toLowerCase();
  return acceptedTypes.some(accepted => {
    if (accepted.startsWith('.')) {
      return fileName.endsWith(accepted);
    }
    return false;
  });
};

const ACCEPTED_EXTENSIONS = '.json,.md,.markdown,.txt';

const ImportDialog: React.FC<ImportDialogProps> = ({ onClose, onSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [format, setFormat] = useState<'json' | 'markdown' | 'txt'>('json');
  const [preview, setPreview] = useState<ImportPreviewResponse | null>(null);
  const [options, setOptions] = useState({
    includeWorldview: true,
    includeGuidelines: true,
    autoExtractWorldview: true,
  });
  const [importMode, setImportMode] = useState<'new' | 'existing'>('new');
  const [targetWorkId, setTargetWorkId] = useState<string>('');
  const [works, setWorks] = useState<Work[]>([]);
  const [worksLoading, setWorksLoading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [previewing, setPreviewing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDraggingOver, setIsDraggingOver] = useState(false);

  const dialogRef = useRef<HTMLDivElement>(null);
  const dragCounterRef = useRef(0);
  const stateRef = useRef({ previewing, loading, importMode });

  // 保持 ref 与 state 同步
  useEffect(() => {
    stateRef.current = { previewing, loading, importMode };
  }, [previewing, loading, importMode]);

  const loadWorks = async () => {
    try {
      setWorksLoading(true);
      const list = await DataService.getWorks();
      setWorks(list.items || []);
    } catch (err) {
      console.error('加载作品列表失败:', err);
      setError('加载作品列表失败，请稍后重试');
    } finally {
      setWorksLoading(false);
    }
  };

  useEffect(() => {
    if (importMode === 'existing' && works.length === 0 && !worksLoading) {
      loadWorks();
    }
  }, [importMode, works.length, worksLoading]);

  const handlePreview = async (fileToPreview?: File, formatToUse?: 'json' | 'markdown' | 'txt') => {
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
      setError(err.detail || err.message || '预览失败，请检查文件格式');
      setPreview(null);
    } finally {
      setPreviewing(false);
    }
  };

  const handleFileChange = async (selectedFile: File | null) => {
    setPreview(null);
    setError(null);
    setFile(selectedFile);

    if (!selectedFile) {
      return;
    }

    const detectedFormat = detectFormat(selectedFile.name);
    if (importMode === 'existing' && detectedFormat === 'json') {
      setError('追加到已有作品暂不支持 JSON 文件，请选择 Markdown 或 TXT');
      setFile(null);
      setFormat('markdown');
      return;
    }

    const nextFormat = detectedFormat;
    setFormat(nextFormat);
    await handlePreview(selectedFile, nextFormat);
  };

  const handleFormatChange = async (next: 'json' | 'markdown' | 'txt') => {
    setFormat(next);
    if (file) {
      await handlePreview(file, next);
    }
  };

  const handleImport = async () => {
    if (!file || !preview) return;
    if (importMode === 'existing' && !targetWorkId) {
      setError('请选择要追加的作品');
      return;
    }
    if (importMode === 'existing' && format === 'json') {
      setError('追加到已有作品暂不支持 JSON 文件，请改用 Markdown 或 TXT');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const importOptions: ImportOptions = {
        format,
        createNew: importMode === 'new',
        includeWorldview: options.includeWorldview,
        includeGuidelines: options.includeGuidelines,
        autoExtractWorldview: options.autoExtractWorldview,
        workId: importMode === 'existing' ? targetWorkId : undefined,
      };

      const result = await DataService.importWork(file, importOptions);

      onSuccess?.(result.workId);
      onClose();
    } catch (err: any) {
      console.error('导入失败:', err);
      setError(err.detail || err.message || '导入失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  // 处理拖拽文件 - 使用原生事件监听器
  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    const handleDragEnter = (e: DragEvent) => {
      e.preventDefault();
      e.stopPropagation();

      if (stateRef.current.previewing || stateRef.current.loading) return;

      dragCounterRef.current++;
      if (e.dataTransfer?.items && e.dataTransfer.items.length > 0) {
        setIsDraggingOver(true);
      }
    };

    const handleDragLeave = (e: DragEvent) => {
      e.preventDefault();
      e.stopPropagation();

      dragCounterRef.current--;
      if (dragCounterRef.current === 0) {
        setIsDraggingOver(false);
      }
    };

    const handleDragOver = (e: DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      if (e.dataTransfer) {
        e.dataTransfer.dropEffect = 'copy';
      }
    };

    const handleDrop = (e: DragEvent) => {
      e.preventDefault();
      e.stopPropagation();

      setIsDraggingOver(false);
      dragCounterRef.current = 0;

      if (stateRef.current.previewing || stateRef.current.loading) return;

      const droppedFile = e.dataTransfer?.files?.[0];
      if (droppedFile) {
        // 检查文件类型
        if (!isFileAccepted(droppedFile, ACCEPTED_EXTENSIONS)) {
          setError('不支持的文件格式，请选择 .json、.md 或 .txt 文件');
          return;
        }

        // 处理文件
        setPreview(null);
        setError(null);
        setFile(droppedFile);

        const detectedFormat = detectFormat(droppedFile.name);
        if (stateRef.current.importMode === 'existing' && detectedFormat === 'json') {
          setError('追加到已有作品暂不支持 JSON 文件，请选择 Markdown 或 TXT');
          setFile(null);
          setFormat('markdown');
          return;
        }

        setFormat(detectedFormat);
        // 延迟触发预览，确保 state 更新
        setTimeout(() => {
          handlePreview(droppedFile, detectedFormat);
        }, 0);
      }
    };

    // 绑定原生事件
    dialog.addEventListener('dragenter', handleDragEnter);
    dialog.addEventListener('dragleave', handleDragLeave);
    dialog.addEventListener('dragover', handleDragOver);
    dialog.addEventListener('drop', handleDrop);

    return () => {
      dialog.removeEventListener('dragenter', handleDragEnter);
      dialog.removeEventListener('dragleave', handleDragLeave);
      dialog.removeEventListener('dragover', handleDragOver);
      dialog.removeEventListener('drop', handleDrop);
    };
  }, []);

  // 全局阻止浏览器默认拖拽行为
  useEffect(() => {
    const preventDefaults = (e: DragEvent) => {
      e.preventDefault();
    };

    // 在 window 级别阻止，确保最早捕获
    window.addEventListener('dragover', preventDefaults, true);
    window.addEventListener('drop', preventDefaults, true);

    return () => {
      window.removeEventListener('dragover', preventDefaults, true);
      window.removeEventListener('drop', preventDefaults, true);
    };
  }, []);

  return (
    <div
      className="import-dialog-overlay"
      onClick={onClose}
    >
      <div
        ref={dialogRef}
        className={`import-dialog ${isDraggingOver ? 'is-dragging-over' : ''}`}
        onClick={e => e.stopPropagation()}
      >
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

        {/* 可滚动的内容区域 */}
        <div className="import-dialog-body">
        {/* 文件上传区域 */}
        <div className="form-section">
          <h3>选择文件</h3>

          <div className="import-mode">
            <label>
              <input
                type="radio"
                name="importMode"
                value="new"
                checked={importMode === 'new'}
                onChange={() => {
                  setImportMode('new');
                  setTargetWorkId('');
                }}
              />
              创建新作品
            </label>
            <label>
              <input
                type="radio"
                name="importMode"
                value="existing"
                checked={importMode === 'existing'}
                onChange={() => {
                  setImportMode('existing');
                  if (format === 'json') {
                    setFormat('markdown');
                  }
                  if (file && detectFormat(file.name) === 'json') {
                    setFile(null);
                    setPreview(null);
                    setError('追加到已有作品暂不支持 JSON 文件，请重新选择 Markdown 或 TXT');
                  }
                }}
              />
              追加到已有作品
            </label>
          </div>

          {importMode === 'existing' && (
            <div className="form-section" style={{ paddingTop: '8px' }}>
              {worksLoading ? (
                <p style={{ color: '#6b7280' }}>正在加载作品列表...</p>
              ) : works.length === 0 ? (
                <p style={{ color: '#6b7280' }}>暂无可用作品，先创建一个吧</p>
              ) : (
                <label className="select-work">
                  选择作品：
                  <select
                    value={targetWorkId}
                    onChange={(e) => setTargetWorkId(e.target.value)}
                  >
                    <option value="">请选择</option>
                    {works.map((w) => (
                      <option key={w.id} value={w.id}>
                        {w.title}
                      </option>
                    ))}
                  </select>
                </label>
              )}
            </div>
          )}

          <FilePicker
            file={file}
            onChange={handleFileChange}
            accept={ACCEPTED_EXTENSIONS}
            placeholder="点击选择文件或拖拽到此处"
            description="支持 .json / .md / .txt 格式"
            note={importMode === 'existing' ? '追加模式仅支持 Markdown/TXT' : undefined}
            disabled={previewing || loading}
          />

          {file && (
            <div className="format-selector">
              <label>
                <input
                  type="radio"
                  name="format"
                  value="json"
                  checked={format === 'json'}
                  onChange={() => handleFormatChange('json')}
                  disabled={importMode === 'existing'}
                />
                JSON（完整导入）{importMode === 'existing' ? '（仅限新建）' : ''}
              </label>
              <label>
                <input
                  type="radio"
                  name="format"
                  value="markdown"
                  checked={format === 'markdown'}
                  onChange={() => handleFormatChange('markdown')}
                />
                Markdown（智能分段）
              </label>
              <label>
                <input
                  type="radio"
                  name="format"
                  value="txt"
                  checked={format === 'txt'}
                  onChange={() => handleFormatChange('txt')}
                />
                TXT（智能分段）
              </label>
            </div>
          )}
        </div>

        {/* 导入选项（仅 JSON 格式） */}
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

        {/* 自动解析选项（仅 Markdown/TXT 格式） */}
        {(format === 'markdown' || format === 'txt') && file && (
          <div className="form-section">
            <h3>智能解析</h3>
            <div className="import-options">
              <label>
                <input
                  type="checkbox"
                  checked={options.autoExtractWorldview}
                  onChange={e =>
                    setOptions({ ...options, autoExtractWorldview: e.target.checked })
                  }
                />
                自动解析世界观（AI 提取人物/地点/设定）
              </label>
              <p className="option-hint">
                开启后将使用 AI 分析章节内容，自动创建人物、地点、设定卡片
              </p>
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
        </div>

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
