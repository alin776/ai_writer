/**
 * AI 自动补全组件
 * 实时显示 AI 建议和补全内容
 */
import React, { useState, useCallback } from 'react';
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

      let prompt = '';

      switch (option) {
        case 'continue':
          prompt = `继续写作以下内容，给出自然流畅的续写：\n\n${selectedText || editor.getText().slice(-500)}`;
          break;
        case 'improve':
          prompt = `改进以下文本，使其更加优美流畅：\n\n${selectedText}`;
          break;
        case 'shorter':
          prompt = `缩短以下文本，保留关键信息：\n\n${selectedText}`;
          break;
        case 'longer':
          prompt = `扩展以下文本，增加更多细节：\n\n${selectedText}`;
          break;
        case 'fix':
          prompt = `修正以下文本的语法和拼写错误：\n\n${selectedText}`;
          break;
        case 'custom':
          prompt = `${customPrompt}\n\n文本内容：${selectedText}`;
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
          maxTokens: 1000,
          temperature: 0.7,
        },
        (chunk) => {
          fullCompletion += chunk;
          setCompletion(fullCompletion);
        }
      );
    } catch (error) {
      console.error('AI 生成失败:', error);
      toast.error('AI 生成失败', (error as Error).message);
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
  const quickOptions = [
    { label: '继续写作', option: 'continue' as AIOption, icon: '✍️' },
    { label: '改进文本', option: 'improve' as AIOption, icon: '✨' },
    { label: '缩短内容', option: 'shorter' as AIOption, icon: '📏' },
    { label: '扩展内容', option: 'longer' as AIOption, icon: '📖' },
    { label: '修正错误', option: 'fix' as AIOption, icon: '🔧' },
  ];

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
          <span>AI 正在思考...</span>
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
            placeholder={hasCompletion ? '告诉 AI 接下来要做什么...' : '让 AI 帮你编辑或生成...'}
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
