/**
 * 导出对话框组件
 */
import React, { useState } from 'react';
import { ExportOptions } from '@/types/export';
import { DataService } from '@/services/DataService';
import { Download, X, FileJson, FileText, Loader2 } from 'lucide-react';
import './ExportDialog.css';

interface ExportDialogProps {
  workId: string;
  workTitle: string;
  onClose: () => void;
}

const ExportDialog: React.FC<ExportDialogProps> = ({ workId, workTitle, onClose }) => {
  const [format, setFormat] = useState<'json' | 'markdown' | 'docx'>('json');
  const [options, setOptions] = useState({
    includeChapters: true,
    includeWorldview: true,
    includeGuidelines: true,
    includeAnalysis: false,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleExport = async () => {
    try {
      setLoading(true);
      setError(null);

      const exportOptions: ExportOptions = {
        format,
        ...options
      };

      // 调用导出API
      const response = await DataService.exportWork(workId, exportOptions);

      console.log('✓ 导出响应:', response);

      // 提取file_id（response.downloadUrl格式: "/api/v1/downloads/{file_id}"）
      const fileId = response.downloadUrl.split('/').pop();
      console.log('✓ 提取的file_id:', fileId);
      
      // 获取完整下载URL
      const downloadUrl = DataService.getDownloadUrl(fileId!);
      console.log('✓ 完整下载URL:', downloadUrl);
      console.log('✓ 开始触发下载...');
      
      // 创建隐藏的下载链接
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = response.fileName;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      // 显示成功消息
      alert(`导出成功！文件大小: ${(response.fileSize / 1024).toFixed(2)} KB`);
      
      // 关闭对话框
      onClose();
    } catch (err: any) {
      console.error('导出失败:', err);
      setError(err.message || '导出失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="export-dialog-overlay" onClick={onClose}>
      <div className="export-dialog" onClick={e => e.stopPropagation()}>
        {/* 标题栏 */}
        <div className="export-dialog-header">
          <h2>
            <Download size={20} />
            导出作品
          </h2>
          <button onClick={onClose} className="close-button">
            <X size={20} />
          </button>
        </div>

        {/* 作品信息 */}
        <div className="work-info">
          <p><strong>{workTitle}</strong></p>
        </div>

        {/* 格式选择 */}
        <div className="form-section">
          <h3>导出格式</h3>
          <div className="format-options">
            <label className={`format-option ${format === 'json' ? 'active' : ''}`}>
              <input
                type="radio"
                name="format"
                value="json"
                checked={format === 'json'}
                onChange={e => setFormat('json')}
              />
              <FileJson size={24} />
              <div className="format-info">
                <strong>JSON</strong>
                <span>完整备份（含所有数据和关系）</span>
              </div>
            </label>

            <label className={`format-option ${format === 'markdown' ? 'active' : ''}`}>
              <input
                type="radio"
                name="format"
                value="markdown"
                checked={format === 'markdown'}
                onChange={e => setFormat('markdown')}
              />
              <FileText size={24} />
              <div className="format-info">
                <strong>Markdown</strong>
                <span>可读格式（正文+世界观附录）</span>
              </div>
            </label>

            <label className={`format-option ${format === 'docx' ? 'active' : ''}`} title="即将支持">
              <input
                type="radio"
                name="format"
                value="docx"
                disabled
                checked={format === 'docx'}
                onChange={e => setFormat('docx')}
              />
              <FileText size={24} />
              <div className="format-info">
                <strong>DOCX</strong>
                <span>出版格式（即将支持）</span>
              </div>
            </label>
          </div>
        </div>

        {/* 导出选项 */}
        <div className="form-section">
          <h3>导出内容</h3>
          <div className="export-options">
            <label>
              <input
                type="checkbox"
                checked={options.includeChapters}
                onChange={e =>
                  setOptions({ ...options, includeChapters: e.target.checked })
                }
              />
              包含章节内容
            </label>

            <label>
              <input
                type="checkbox"
                checked={options.includeWorldview}
                onChange={e =>
                  setOptions({ ...options, includeWorldview: e.target.checked })
                }
              />
              包含世界观设定（人物/地点/设定）
            </label>

            <label>
              <input
                type="checkbox"
                checked={options.includeGuidelines}
                onChange={e =>
                  setOptions({ ...options, includeGuidelines: e.target.checked })
                }
              />
              包含创作规范
            </label>

            <label>
              <input
                type="checkbox"
                checked={options.includeAnalysis}
                onChange={e =>
                  setOptions({ ...options, includeAnalysis: e.target.checked })
                }
              />
              包含小说分析报告
            </label>
          </div>
        </div>

        {/* 错误提示 */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* 操作按钮 */}
        <div className="export-dialog-footer">
          <button
            onClick={onClose}
            className="button button-secondary"
            disabled={loading}
          >
            取消
          </button>
          <button
            onClick={handleExport}
            className="button button-primary"
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 size={16} className="spinner" />
                导出中...
              </>
            ) : (
              <>
                <Download size={16} />
                开始导出
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExportDialog;
