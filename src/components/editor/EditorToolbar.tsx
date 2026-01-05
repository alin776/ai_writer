/**
 * 编辑器工具栏组件
 */
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Editor } from '@tiptap/react';
import {
  Undo,
  Redo,
  Wand2,
  PanelLeftOpen,
  PanelRightOpen,
  Replace,
  Sparkles,
} from 'lucide-react';
import FindReplaceDialog from './FindReplaceDialog';
import SmartFormatDialog from './SmartFormatDialog';

interface EditorToolbarProps {
  editor: Editor;
  aiAutoCompleteEnabled?: boolean;
  onToggleAIAutoComplete?: () => void;
  isLeftPanelCollapsed?: boolean;
  onExpandLeftPanel?: () => void;
  isRightPanelCollapsed?: boolean;
  onExpandRightPanel?: () => void;
  saveStatus?: 'saved' | 'saving' | 'unsaved';
}

const EditorToolbar: React.FC<EditorToolbarProps> = ({
  editor,
  aiAutoCompleteEnabled = false,
  onToggleAIAutoComplete,
  isLeftPanelCollapsed = false,
  onExpandLeftPanel,
  isRightPanelCollapsed = false,
  onExpandRightPanel,
  saveStatus = 'saved',
}) => {
  const { t } = useTranslation();
  const [showFindReplace, setShowFindReplace] = useState(false);
  const [showSmartFormat, setShowSmartFormat] = useState(false);

  if (!editor) {
    return null;
  }

  /**
   * 工具栏按钮组件
   */
  const ToolbarButton: React.FC<{
    onClick: () => void;
    isActive?: boolean;
    disabled?: boolean;
    children: React.ReactNode;
    title: string;
  }> = ({ onClick, isActive, disabled, children, title }) => (
    <button
      type="button"
      onMouseDown={(e) => {
        e.preventDefault(); // 阻止按钮获取焦点，保持编辑器选区
      }}
      onClick={onClick}
      disabled={disabled}
      title={title}
      className={`h-7 w-7 p-0 flex items-center justify-center rounded transition-all ${
        isActive
          ? 'bg-zinc-100 text-zinc-900 dark:bg-slate-700 dark:text-slate-100'
          : 'text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-700'
      } ${disabled ? 'opacity-30 cursor-not-allowed' : 'cursor-pointer'}`}
    >
      {children}
    </button>
  );

  return (
    <div className="px-3 py-1.5 flex items-center gap-1.5 border-b border-zinc-100 bg-white shadow-sm shadow-zinc-100/50 dark:bg-slate-900 dark:border-slate-700 dark:shadow-none">
      {/* 展开目录按钮（仅当目录收起时显示）+ AI 自动补全 + 撤销/重做 */}
      <div className="flex items-center gap-0.5">
        {isLeftPanelCollapsed && (
          <ToolbarButton
            onClick={() => onExpandLeftPanel?.()}
            title={t('editor.toolbar.expandChapterList')}
          >
            <PanelLeftOpen className="h-3.5 w-3.5" />
          </ToolbarButton>
        )}
        <ToolbarButton
          onClick={() => onToggleAIAutoComplete?.()}
          isActive={aiAutoCompleteEnabled}
          title={aiAutoCompleteEnabled ? t('editor.toolbar.aiAutoCompleteEnabled') : t('editor.toolbar.aiAutoCompleteDisabled')}
        >
          <Wand2 className="h-3.5 w-3.5" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().undo().run()}
          disabled={!editor.can().undo()}
          title={`${t('editor.toolbar.undo')} (Ctrl+Z)`}
        >
          <Undo className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => editor.chain().focus().redo().run()}
          disabled={!editor.can().redo()}
          title={`${t('editor.toolbar.redo')} (Ctrl+Y)`}
        >
          <Redo className="h-3 w-3" />
        </ToolbarButton>
      </div>

      {/* 全文替换和智能排版 */}
      <div className="flex items-center">
        <ToolbarButton
          onClick={() => setShowFindReplace(true)}
          title="全文替换 (Ctrl+H)"
        >
          <Replace className="h-3 w-3" />
        </ToolbarButton>
        <ToolbarButton
          onClick={() => setShowSmartFormat(true)}
          title="智能排版"
        >
          <Sparkles className="h-3 w-3" />
        </ToolbarButton>
      </div>

      {/* 全文替换对话框 */}
      <FindReplaceDialog
        editor={editor}
        isOpen={showFindReplace}
        onClose={() => setShowFindReplace(false)}
      />

      {/* 智能排版对话框 */}
      <SmartFormatDialog
        editor={editor}
        isOpen={showSmartFormat}
        onClose={() => setShowSmartFormat(false)}
      />

      {/* 保存状态 - 放在工具栏右侧 */}
      <div className="flex-1" />
      <div className="flex items-center">
        {saveStatus === 'saved' && (
          <div className="flex items-center gap-1 text-green-600 dark:text-green-500">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="text-[11px]">{t('editor.saved')}</span>
          </div>
        )}
        {saveStatus === 'saving' && (
          <div className="flex items-center gap-1 text-blue-600 dark:text-blue-400">
            <svg className="animate-spin w-3.5 h-3.5" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <span className="text-[11px]">{t('editor.saving')}</span>
          </div>
        )}
        {saveStatus === 'unsaved' && (
          <div className="flex items-center gap-1 text-orange-600 dark:text-orange-400">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span className="text-[11px]">{t('editor.unsaved')}</span>
          </div>
        )}
      </div>

      {/* 右侧展开按钮（仅当右侧面板收起时显示） */}
      {isRightPanelCollapsed && (
        <ToolbarButton
          onClick={() => onExpandRightPanel?.()}
          title={t('editor.toolbar.expandRightPanel')}
        >
          <PanelRightOpen className="h-3.5 w-3.5" />
        </ToolbarButton>
      )}
    </div>
  );
};

export default EditorToolbar;
