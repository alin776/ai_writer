/**
 * AI 菜单组件
 * 选中文本时显示 AI 操作菜单
 */
import React, { useState, useEffect } from 'react';
import { BubbleMenu as TiptapBubbleMenu } from '@tiptap/react/menus';
import { Editor } from '@tiptap/core';
import {
  Wand2,
  Sparkles,
  FileText,
  Minimize2,
  Languages,
  Loader2,
  Check,
  X,
  Pause,
} from 'lucide-react';
import { useAI } from '@/hooks/useAI';
import { useToast } from '@/hooks/useToast';
import AIContinueDrawer, { AIContinueConfig } from './AIContinueDrawer';

interface AIMenuProps {
  editor: Editor;
}

/**
 * AI 菜单组件
 */
const AIMenu: React.FC<AIMenuProps> = ({ editor }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [aiGeneratedRange, setAiGeneratedRange] = useState<{ from: number; to: number } | null>(null);
  const [originalContent, setOriginalContent] = useState<string>('');
  const [showContinueDialog, setShowContinueDialog] = useState(false);
  const { complete, expand, summarize, polish, translate, cancel, loading } = useAI();
  const toast = useToast();

  // 监听 Slash 命令触发的 AI 事件
  useEffect(() => {
    const handleAIContinue = (e: Event) => {
      const customEvent = e as CustomEvent;
      if (customEvent.detail.editor === editor) {
        // 打开配置弹窗
        setShowContinueDialog(true);
      }
    };

    const handleAIExpand = (e: Event) => {
      const customEvent = e as CustomEvent;
      if (customEvent.detail.editor === editor) {
        handleExpand();
      }
    };

    const handleAISummarize = (e: Event) => {
      const customEvent = e as CustomEvent;
      if (customEvent.detail.editor === editor) {
        handleSummarize();
      }
    };

    const handleAIPolish = (e: Event) => {
      const customEvent = e as CustomEvent;
      if (customEvent.detail.editor === editor) {
        handlePolish();
      }
    };

    window.addEventListener('ai-continue', handleAIContinue);
    window.addEventListener('ai-expand', handleAIExpand);
    window.addEventListener('ai-summarize', handleAISummarize);
    window.addEventListener('ai-polish', handleAIPolish);

    return () => {
      window.removeEventListener('ai-continue', handleAIContinue);
      window.removeEventListener('ai-expand', handleAIExpand);
      window.removeEventListener('ai-summarize', handleAISummarize);
      window.removeEventListener('ai-polish', handleAIPolish);
    };
  }, [editor]);

  if (!editor) {
    return null;
  }

  /**
   * 获取选中的文本
   */
  const getSelectedText = (): string => {
    const { from, to } = editor.state.selection;
    return editor.state.doc.textBetween(from, to, ' ');
  };

  /**
   * 替换选中的文本
   */
  const replaceSelectedText = (newText: string) => {
    const { from, to } = editor.state.selection;
    editor.chain().focus().deleteRange({ from, to }).insertContent(newText).run();
  };

  /**
   * 在选中文本后插入 AI 生成的内容
   */
  const insertAfterSelection = (text: string) => {
    const { to } = editor.state.selection;
    editor
      .chain()
      .focus()
      .setTextSelection(to)
      .insertContent(' ' + text)
      .run();
  };

  /**
   * 同意 AI 生成的内容
   */
  const handleAccept = () => {
    if (aiGeneratedRange) {
      // 移除黄色高亮
      editor
        .chain()
        .focus()
        .setTextSelection({ from: aiGeneratedRange.from, to: aiGeneratedRange.to })
        .unsetMark('aiHighlight')
        .run();

      setAiGeneratedRange(null);
      setOriginalContent('');
      toast.success('已接受 AI 生成的内容');
    }
  };

  /**
   * 撤销 AI 生成的内容
   */
  const handleReject = () => {
    if (aiGeneratedRange && originalContent !== undefined) {
      console.log('[AIMenu] handleReject 开始');
      console.log('[AIMenu] 撤销范围:', aiGeneratedRange);
      console.log('[AIMenu] 原始内容:', originalContent);

      const { from, to } = aiGeneratedRange;

      // 先清除范围内的 AI 高亮标记
      editor
        .chain()
        .focus()
        .setTextSelection({ from, to })
        .unsetMark('aiHighlight')
        .run();

      // 删除 AI 生成的内容
      editor
        .chain()
        .focus()
        .setTextSelection({ from, to })
        .deleteSelection()
        .run();

      // 插入原始内容（如果有）
      if (originalContent) {
        editor
          .chain()
          .focus()
          .setTextSelection(from)
          .insertContent(originalContent)
          .run();
      }

      // 将光标移到插入内容的末尾，避免标记传染
      const newPosition = from + originalContent.length;
      editor
        .chain()
        .focus()
        .setTextSelection(newPosition)
        .run();

      console.log('[AIMenu] 撤销后光标位置:', newPosition);

      setAiGeneratedRange(null);
      setOriginalContent('');
      toast.info('已撤销 AI 生成的内容');
    }
  };

  /**
   * 暂停 AI 生成
   */
  const handleStop = () => {
    console.log('[AIMenu] 暂停 AI 生成');
    cancel();
    setIsProcessing(false);
    // 暂停后保留当前的 aiGeneratedRange，这样用户可以选择同意或撤销
    toast.info('已暂停 AI 生成', '您可以选择同意或撤销已生成的内容');
  };

  /**
   * 构建AI续写提示词
   */
  const buildContinuePrompt = (config: AIContinueConfig): string => {
    let prompt = '# 角色与核心指令\n';
    prompt += '你是一位经验丰富、风格多变、叙事技巧高超的职业小说家和文字工程师。你的任务是严格根据下方提供的上下文、世界观限制和精确指令，创作一段高质量的续写内容。\n\n';
    prompt += '核心要求：续写内容必须与前文的风格、语调、人物逻辑和剧情走向保持**百分之百的无缝衔接**。\n';
    prompt += '输出格式：输出必须为纯文本，仅包含续写内容，**禁止包含任何解释、总结、标题或评论**。\n\n';

    prompt += '# 背景与上下文\n\n';

    // A. 最新章节结尾
    if (config.lastChapterContext) {
      prompt += '## A. 最新章节结尾 (Last Chapter Context)\n';
      prompt += config.lastChapterContext + '\n\n';
    }

    // B. 关键世界观与人物状态
    if (config.focusCharacter || config.coreLocation || config.settingConstraints) {
      prompt += '## B. 关键世界观与人物状态 (Core Lore & Status)\n';
      if (config.focusCharacter) {
        prompt += `1. **焦点人物：** ${config.focusCharacter}`;
        if (config.characterStatus) {
          prompt += `（当前情绪/状态：${config.characterStatus}）`;
        }
        prompt += '\n';
      }
      if (config.coreLocation) {
        prompt += `2. **核心地点：** ${config.coreLocation}`;
        if (config.environmentStatus) {
          prompt += `（当前环境：${config.environmentStatus}）`;
        }
        prompt += '\n';
      }
      if (config.settingConstraints) {
        prompt += `3. **关键设定限制：** ${config.settingConstraints}\n`;
      }
      prompt += '\n';
    }

    // C. 文风与语气
    if (config.styleAdjectives || config.emotionalTone) {
      prompt += '## C. 文风与语气 (Tone & Style)\n';
      if (config.styleAdjectives) {
        prompt += `文风形容词：${config.styleAdjectives}\n`;
      }
      if (config.emotionalTone) {
        prompt += `本段落的情绪基调：${config.emotionalTone}\n`;
      }
      prompt += '\n';
    }

    // D. 叙事视角
    prompt += '## D. 叙事视角\n';
    prompt += `请使用 ${config.narrativePerspective}`;
    if (config.narrativePerspective === '第三人称受限视角' && config.perspectiveFocusCharacter) {
      prompt += `，焦点角色为 ${config.perspectiveFocusCharacter}`;
    }
    prompt += '。\n\n';

    // 模块三：精确续写要求
    prompt += '# 精确续写要求\n\n';

    // 目标长度
    prompt += '## 目标长度与收束\n';
    prompt += `续写内容的长度必须控制在 ${config.targetLength} 字左右。\n`;
    if (config.endingStyle) {
      prompt += `续写必须以 ${config.endingStyle} 来结束。\n`;
    }
    prompt += '\n';

    // 关键情节目标
    const validPlotPoints = config.plotPoints.filter(p => p.trim());
    if (validPlotPoints.length > 0) {
      prompt += '## 关键情节目标 (Key Plot Points)\n';
      validPlotPoints.forEach((point, index) => {
        prompt += `${index + 1}. **[任务 ${index + 1}]：** ${point}\n`;
      });
      prompt += '\n';
    }

    // 限制与禁止内容
    const validProhibited = config.prohibitedContent.filter(p => p.trim());
    if (validProhibited.length > 0) {
      prompt += '## 限制与禁止内容\n';
      validProhibited.forEach((item, index) => {
        prompt += `${index + 1}. **禁止** ${item}\n`;
      });
      prompt += '\n';
    }

    prompt += '\n请开始续写：';

    return prompt;
  };

  /**
   * AI 续写（使用配置）
   */
  const handleContinueWithConfig = async (config: AIContinueConfig) => {
    console.log('[AIMenu] handleContinueWithConfig 开始');
    console.log('[AIMenu] 配置:', config);
    setShowContinueDialog(false);
    setIsProcessing(true);

    // 使用 let 声明在 try 块外部，以便在 catch 中访问
    let startPosition = 0;
    let insertPosition = 0;

    try {
      const { to } = editor.state.selection;

      console.log('[AIMenu] 光标位置:', to);

      // 保存原始内容（空）
      setOriginalContent('');

      let generatedText = '';

      // 不插入空格，直接从光标位置开始
      startPosition = to;
      insertPosition = startPosition;

      console.log('[AIMenu] 开始位置:', startPosition);

      // 构建提示词
      const prompt = buildContinuePrompt(config);
      console.log('[AIMenu] 完整提示词:', prompt);

      console.log('[AIMenu] 开始调用 complete API');

      // 根据目标长度计算 max tokens（中文约 1.5-2 个字符 = 1 token）
      const maxTokens = Math.ceil(config.targetLength * 2);

      await complete(
        {
          prompt,
          maxTokens,
          temperature: 0.8,
        },
        (chunk) => {
          console.log('[AIMenu] 收到 chunk:', chunk);
          console.log('[AIMenu] 插入前位置:', insertPosition);
          generatedText += chunk;

          // 实时更新编辑器 - 在当前位置插入新字符并添加高亮
          editor
            .chain()
            .focus()
            .setTextSelection(insertPosition)
            .insertContent(chunk)
            .run();

          // 更新 insertPosition
          insertPosition += chunk.length;

          // 在插入完成后，对整个范围设置高亮标记
          editor
            .chain()
            .focus()
            .setTextSelection({ from: startPosition, to: insertPosition })
            .setMark('aiHighlight')
            .setTextSelection(insertPosition) // 将光标移到末尾
            .run();

          console.log('[AIMenu] 插入后位置:', insertPosition);
          console.log('[AIMenu] 高亮范围:', { from: startPosition, to: insertPosition });
        }
      );

      console.log('[AIMenu] complete API 调用完成');
      console.log('[AIMenu] 生成文本总长度:', generatedText.length);

      // 设置生成内容的范围（正常完成）
      setAiGeneratedRange({ from: startPosition, to: insertPosition });
      console.log('[AIMenu] 设置生成范围:', { from: startPosition, to: insertPosition });
    } catch (error) {
      console.error('[AIMenu] AI 续写失败:', error);
      const errorMessage = (error as Error).message;

      // 如果是用户主动暂停，设置已生成内容的范围
      if (errorMessage.includes('已暂停')) {
        // 暂停时也要设置生成范围，让用户可以选择同意或撤销
        if (insertPosition > startPosition) {
          setAiGeneratedRange({ from: startPosition, to: insertPosition });
          console.log('[AIMenu] 暂停时设置生成范围:', { from: startPosition, to: insertPosition });
        }
      } else {
        toast.error('AI 续写失败', errorMessage);
      }
    } finally {
      setIsProcessing(false);
      console.log('[AIMenu] handleContinueWithConfig 结束');
    }
  };

  /**
   * AI 扩写
   */
  const handleExpand = async () => {
    setIsProcessing(true);
    try {
      const selectedText = getSelectedText();
      if (!selectedText) {
        toast.warning('请先选中文本', '请选中要扩写的文本内容');
        setIsProcessing(false);
        return;
      }

      const { from, to } = editor.state.selection;
      setOriginalContent(selectedText);

      const expandedText = await expand(selectedText);

      // 替换选中文本并添加高亮
      editor
        .chain()
        .focus()
        .deleteRange({ from, to })
        .insertContent(expandedText)
        .setTextSelection({ from, to: from + expandedText.length })
        .setMark('aiHighlight')
        .run();

      setAiGeneratedRange({ from, to: from + expandedText.length });
      toast.success('扩写完成');
    } catch (error) {
      console.error('AI 扩写失败:', error);
      toast.error('AI 扩写失败', (error as Error).message);
    } finally {
      setIsProcessing(false);
    }
  };

  /**
   * AI 缩写/总结
   */
  const handleSummarize = async () => {
    setIsProcessing(true);
    try {
      const selectedText = getSelectedText();
      if (!selectedText) {
        toast.warning('请先选中文本', '请选中要总结的文本内容');
        setIsProcessing(false);
        return;
      }

      const { from, to } = editor.state.selection;
      setOriginalContent(selectedText);

      const summarizedText = await summarize(selectedText);

      // 替换选中文本并添加高亮
      editor
        .chain()
        .focus()
        .deleteRange({ from, to })
        .insertContent(summarizedText)
        .setTextSelection({ from, to: from + summarizedText.length })
        .setMark('aiHighlight')
        .run();

      setAiGeneratedRange({ from, to: from + summarizedText.length });
      toast.success('总结完成');
    } catch (error) {
      console.error('AI 总结失败:', error);
      toast.error('AI 总结失败', (error as Error).message);
    } finally {
      setIsProcessing(false);
    }
  };

  /**
   * AI 润色
   */
  const handlePolish = async () => {
    setIsProcessing(true);
    try {
      const selectedText = getSelectedText();
      if (!selectedText) {
        toast.warning('请先选中文本', '请选中要润色的文本内容');
        setIsProcessing(false);
        return;
      }

      const { from, to } = editor.state.selection;
      setOriginalContent(selectedText);

      const polishedText = await polish(selectedText);

      // 替换选中文本并添加高亮
      editor
        .chain()
        .focus()
        .deleteRange({ from, to })
        .insertContent(polishedText)
        .setTextSelection({ from, to: from + polishedText.length })
        .setMark('aiHighlight')
        .run();

      setAiGeneratedRange({ from, to: from + polishedText.length });
      toast.success('润色完成');
    } catch (error) {
      console.error('AI 润色失败:', error);
      toast.error('AI 润色失败', (error as Error).message);
    } finally {
      setIsProcessing(false);
    }
  };

  /**
   * AI 翻译
   */
  const handleTranslate = async () => {
    setIsProcessing(true);
    try {
      const selectedText = getSelectedText();
      if (!selectedText) {
        toast.warning('请先选中文本', '请选中要翻译的文本内容');
        setIsProcessing(false);
        return;
      }

      const { from, to } = editor.state.selection;
      setOriginalContent(selectedText);

      // 简单判断：如果包含中文，翻译成英文；否则翻译成中文
      const hasChinese = /[\u4e00-\u9fa5]/.test(selectedText);
      const targetLang = hasChinese ? '英文' : '中文';

      const translatedText = await translate(selectedText, targetLang);

      // 替换选中文本并添加高亮
      editor
        .chain()
        .focus()
        .deleteRange({ from, to })
        .insertContent(translatedText)
        .setTextSelection({ from, to: from + translatedText.length })
        .setMark('aiHighlight')
        .run();

      setAiGeneratedRange({ from, to: from + translatedText.length });
      toast.success('翻译完成', `已翻译为${targetLang}`);
    } catch (error) {
      console.error('AI 翻译失败:', error);
      toast.error('AI 翻译失败', (error as Error).message);
    } finally {
      setIsProcessing(false);
    }
  };

  /**
   * AI 菜单按钮
   */
  const AIButton: React.FC<{
    onClick: () => void;
    icon: React.ReactNode;
    label: string;
    disabled?: boolean;
  }> = ({ onClick, icon, label, disabled }) => (
    <button
      onClick={onClick}
      disabled={disabled || isProcessing}
      className="ai-menu-button"
      title={label}
      type="button"
    >
      {icon}
      <span className="ai-menu-label">{label}</span>
    </button>
  );

  // 只在选中文本时显示
  const shouldShow = () => {
    const { from, to } = editor.state.selection;
    return to - from > 0;
  };

  return (
    <>
      {/* AI 操作按钮（暂停/同意/撤销） */}
      {isProcessing && (
        <div
          className="ai-actions-container"
          style={{
            bottom: '20px',
            right: '20px',
          }}
        >
          <button onClick={handleStop} className="ai-action-button stop">
            <Pause className="w-4 h-4" />
            <span>暂停</span>
          </button>
        </div>
      )}

      {aiGeneratedRange && !isProcessing && (
        <div
          className="ai-actions-container"
          style={{
            bottom: '20px',
            right: '20px',
          }}
        >
          <button onClick={handleAccept} className="ai-action-button accept">
            <Check className="w-4 h-4" />
            <span>同意</span>
          </button>
          <button onClick={handleReject} className="ai-action-button reject">
            <X className="w-4 h-4" />
            <span>撤销</span>
          </button>
        </div>
      )}

      {/* AI 菜单 */}
      <TiptapBubbleMenu
        editor={editor}
        shouldShow={shouldShow}
        className="ai-menu-container"
      >
        {isProcessing ? (
          <div className="ai-menu-loading">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span className="ai-menu-loading-text">AI 处理中...</span>
          </div>
        ) : (
          <>
            <AIButton
              onClick={() => setShowContinueDialog(true)}
              icon={<Wand2 className="w-4 h-4" />}
              label="续写"
            />
            <AIButton
              onClick={handleExpand}
              icon={<FileText className="w-4 h-4" />}
              label="扩写"
            />
            <AIButton
              onClick={handleSummarize}
              icon={<Minimize2 className="w-4 h-4" />}
              label="总结"
            />
            <AIButton
              onClick={handlePolish}
              icon={<Sparkles className="w-4 h-4" />}
              label="润色"
            />
            <AIButton
              onClick={handleTranslate}
              icon={<Languages className="w-4 h-4" />}
              label="翻译"
            />
          </>
        )}
      </TiptapBubbleMenu>

      {/* AI 续写配置抽屉 */}
      <AIContinueDrawer
        isOpen={showContinueDialog}
        onClose={() => setShowContinueDialog(false)}
        onConfirm={handleContinueWithConfig}
        editorContent={editor.getText()}
      />
    </>
  );
};

export default AIMenu;
