/**
 * AI 高亮扩展
 * 用于标记 AI 生成的内容
 */
import { Mark } from '@tiptap/core';

export interface AIHighlightOptions {
  HTMLAttributes: Record<string, any>;
}

declare module '@tiptap/core' {
  interface Commands<ReturnType> {
    aiHighlight: {
      /**
       * 设置 AI 高亮
       */
      setAIHighlight: () => ReturnType;
      /**
       * 取消 AI 高亮
       */
      unsetAIHighlight: () => ReturnType;
    };
  }
}

export const AIHighlight = Mark.create<AIHighlightOptions>({
  name: 'aiHighlight',

  addOptions() {
    return {
      HTMLAttributes: {
        class: 'ai-highlight',
      },
    };
  },

  parseHTML() {
    return [
      {
        tag: 'mark.ai-highlight',
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    return ['mark', { ...this.options.HTMLAttributes, ...HTMLAttributes }, 0];
  },

  addCommands() {
    return {
      setAIHighlight:
        () =>
        ({ commands }) => {
          return commands.setMark(this.name);
        },
      unsetAIHighlight:
        () =>
        ({ commands }) => {
          return commands.unsetMark(this.name);
        },
    };
  },
});
