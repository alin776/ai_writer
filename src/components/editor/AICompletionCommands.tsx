/**
 * AI 补全命令组件
 * 显示替换/插入选项
 */
import React from 'react';
import { useTranslation } from 'react-i18next';
import { Editor } from '@tiptap/core';
import { Check, TextQuote, Trash2 } from 'lucide-react';

interface AICompletionCommandsProps {
  editor: Editor;
  completion: string;
  onDiscard: () => void;
}

const AICompletionCommands: React.FC<AICompletionCommandsProps> = ({
  editor,
  completion,
  onDiscard,
}) => {
  const { t } = useTranslation();

  const handleReplace = () => {
    const { from, to } = editor.state.selection;
    editor
      .chain()
      .focus()
      .deleteRange({ from, to })
      .insertContent(completion)
      .run();
  };

  const handleInsert = () => {
    const { to } = editor.state.selection;
    editor
      .chain()
      .focus()
      .setTextSelection(to)
      .insertContent(' ' + completion)
      .run();
  };

  return (
    <div className="ai-completion-commands">
      <button
        onClick={handleReplace}
        className="ai-completion-command-item"
        type="button"
      >
        <Check className="w-4 h-4" />
        <span>{t('editor.aiCompletion.replaceSelection')}</span>
      </button>
      <button
        onClick={handleInsert}
        className="ai-completion-command-item"
        type="button"
      >
        <TextQuote className="w-4 h-4" />
        <span>{t('editor.aiCompletion.insertBelow')}</span>
      </button>
      <div className="ai-completion-separator" />
      <button
        onClick={onDiscard}
        className="ai-completion-command-item discard"
        type="button"
      >
        <Trash2 className="w-4 h-4" />
        <span>{t('editor.aiCompletion.discard')}</span>
      </button>
    </div>
  );
};

export default AICompletionCommands;
