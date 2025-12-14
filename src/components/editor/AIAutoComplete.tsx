/**
 * AI 自动补全组件
 * 实时显示 AI 建议和补全文本
 */
import React, { useState, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { Editor } from '@tiptap/core';
import { ArrowUp, Sparkles, Loader2 } from 'lucide-react';
import AICompletionCommands from './AICompletionCommands';
import { useAI } from '@/hooks/useAI';
import { useToast } from '@/hooks/useToast';
import ReactMarkdown from 'react-markdown';

interface AIAutoCompleteProps {
  editor: Editor;
  onOpenChange: (open: boolean) => void;
}

type AIOption = 'continue' | 'improve' | 'shorter' | 'longer' | 'fix' | 'custom';

const AIAutoComplete: React.FC<AIAutoCompleteProps> = ({
  editor,
  onOpenChange,
}) => {
  const { t } = useTranslation();
  const [inputValue, setInputValue] = useState('');
  const [completion, setCompletion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();
  const { complete: aiComplete } = useAI();

  /**
   * 调用 AI 生成
   */
  const handleGenerate = useCallback(async (option: AIOption, customPrompt?: string) => {
    setIsLoading(true);
    setCompletion('');

    try {
      const { from, to } = editor.state.selection;
      const selectedText = editor.state.doc.textBetween(from, to, ' ');
      const contextText = selectedText || editor.getText().slice(-500);

      let prompt = '';

      switch (option) {
        case 'continue':
          prompt = `${t('editor.aiAutoComplete.promptContinue')}\n\n${contextText}`;
          break;
        case 'improve':
          prompt = `${t('editor.aiAutoComplete.promptImprove')}\n\n${contextText}`;
          break;
        case 'shorter':
          prompt = `${t('editor.aiAutoComplete.promptShorter')}\n\n${contextText}`;
          break;
        case 'longer':
          prompt = `${t('editor.aiAutoComplete.promptLonger')}\n\n${contextText}`;
          break;
        case 'fix':
          prompt = `${t('editor.aiAutoComplete.promptFix')}\n\n${contextText}`;
          break;
        case 'custom':
          prompt = `${customPrompt?.trim() || t('editor.aiAutoComplete.promptDefault')}\n\n${t('editor.aiAutoComplete.textContent')}${contextText}`;
          break;
      }

      // 高亮选中内容
      if (from !== to) {
        editor.chain().focus().setTextSelection({ from, to }).setMark('aiHighlight').run();
      }

      let fullCompletion = '';
      await aiComplete(
        {
          prompt,
          // 自动补全过程限制生成长度，确保走轻量模型路径
          maxTokens: 120,
          temperature: 0.7,
        },
        (chunk) => {
          fullCompletion += chunk;
          setCompletion(fullCompletion);
        }
      );
    } catch (error) {
      console.error('AI generation failed:', error);
      toast.error(t('editor.aiAutoComplete.generateFailed'), (error as Error).message);
    } finally {
      setIsLoading(false);
    }
  }, [editor, aiComplete, toast]);

  /**
   * 处理提交按钮点击
   */
  const handleSubmit = () => {
    if (completion) {
      // 如果已有补全内容，基于现有内容再次生成
      handleGenerate('custom', inputValue);
      setInputValue('');
    } else {
      // 首次生成
      handleGenerate('custom', inputValue);
      setInputValue('');
    }
  };

  /**
   * 处理丢弃
   */
  const handleDiscard = () => {
    setCompletion('');
    editor.chain().focus().unsetMark('aiHighlight').run();
    onOpenChange(false);
  };

  /**
   * 预设命令选项
   */
const getQuickOptions = (t: (key: string) => string): Array<{ label: string; option: AIOption; icon: string }> => [
  { label: t('editor.aiAutoComplete.continueWriting'), option: 'continue', icon: '\u270d' },
  { label: t('editor.aiAutoComplete.improveText'), option: 'improve', icon: '\u2728' },
  { label: t('editor.aiAutoComplete.shortenContent'), option: 'shorter', icon: '\ud83d\udcc9' },
  { label: t('editor.aiAutoComplete.expandContent'), option: 'longer', icon: '\ud83d\udcd6' },
  { label: t('editor.aiAutoComplete.fixErrors'), option: 'fix', icon: '\ud83d\udee0' },
];

  const quickOptions = getQuickOptions(t);

  const hasCompletion = completion.length > 0;

  return (
    <div className="ai-autocomplete-container">
      {/* 显示生成的内容 */}
      {hasCompletion && (
        <div className="ai-autocomplete-completion">
          <div className="ai-autocomplete-completion-content">
            <ReactMarkdown>{completion}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* 加载状态 */}
      {isLoading && (
        <div className="ai-autocomplete-loading">
          <Sparkles className="w-4 h-4 text-purple-500" />
          <span>{t('editor.aiAutoComplete.thinking')}</span>
          <Loader2 className="w-4 h-4 animate-spin" />
        </div>
      )}

      {/* 输入框和提交按钮 */}
      {!isLoading && (
        <div className="ai-autocomplete-input-container">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit();
              }
            }}
            placeholder={hasCompletion ? t('editor.aiAutoComplete.placeholderNext') : t('editor.aiAutoComplete.placeholderFirst')}
            className="ai-autocomplete-input"
            autoFocus
          />
          <button
            onClick={handleSubmit}
            className="ai-autocomplete-submit"
            type="button"
            disabled={!inputValue.trim()}
          >
            <ArrowUp className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* 命令选项 */}
      {hasCompletion ? (
        <AICompletionCommands
          editor={editor}
          completion={completion}
          onDiscard={handleDiscard}
        />
      ) : (
        !isLoading && (
          <div className="ai-autocomplete-quick-options">
            {quickOptions.map((item) => (
              <button
                key={item.option}
                onClick={() => handleGenerate(item.option)}
                className="ai-autocomplete-quick-option"
                type="button"
              >
                <span className="ai-autocomplete-quick-option-icon">{item.icon}</span>
                <span className="ai-autocomplete-quick-option-label">{item.label}</span>
              </button>
            ))}
          </div>
        )
      )}
    </div>
  );
};

export default AIAutoComplete;


