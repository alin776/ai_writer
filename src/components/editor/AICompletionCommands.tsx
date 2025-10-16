/**
 * AI 补全命令组件
 * 显示替换/插入选项
 */
import React from 'react';
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
        <span>替换选中内容</span>
      </button>
      <button
        onClick={handleInsert}
        className="ai-completion-command-item"
        type="button"
      >
        <TextQuote className="w-4 h-4" />
        <span>在下方插入</span>
      </button>
      <div className="ai-completion-separator" />
      <button
        onClick={onDiscard}
        className="ai-completion-command-item discard"
        type="button"
      >
        <Trash2 className="w-4 h-4" />
        <span>丢弃</span>
      </button>
    </div>
  );
};

export default AICompletionCommands;
