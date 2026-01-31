/**
 * AIRevisionMark - TipTap 扩展
 * 用于显示 AI 修改的删除线和插入标记
 */

import { Mark, mergeAttributes } from '@tiptap/core';

/**
 * AI 删除标记 - 显示被删除的原文
 */
export const AIDeleted = Mark.create({
  name: 'aiDeleted',

  addOptions() {
    return {
      HTMLAttributes: {
        class: 'ai-deleted',
      },
    };
  },

  parseHTML() {
    return [
      {
        tag: 'del.ai-deleted',
      },
      {
        tag: 'del[data-ai-deleted]',
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    return ['del', mergeAttributes(this.options.HTMLAttributes, HTMLAttributes, { 'data-ai-deleted': '' }), 0];
  },

  addCommands() {
    return {
      setAIDeleted: () => ({ commands }) => {
        return commands.setMark(this.name);
      },
      toggleAIDeleted: () => ({ commands }) => {
        return commands.toggleMark(this.name);
      },
      unsetAIDeleted: () => ({ commands }) => {
        return commands.unsetMark(this.name);
      },
    };
  },
});

/**
 * AI 插入标记 - 显示新增的内容
 */
export const AIInserted = Mark.create({
  name: 'aiInserted',

  addOptions() {
    return {
      HTMLAttributes: {
        class: 'ai-inserted',
      },
    };
  },

  parseHTML() {
    return [
      {
        tag: 'ins.ai-inserted',
      },
      {
        tag: 'ins[data-ai-inserted]',
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    return ['ins', mergeAttributes(this.options.HTMLAttributes, HTMLAttributes, { 'data-ai-inserted': '' }), 0];
  },

  addCommands() {
    return {
      setAIInserted: () => ({ commands }) => {
        return commands.setMark(this.name);
      },
      toggleAIInserted: () => ({ commands }) => {
        return commands.toggleMark(this.name);
      },
      unsetAIInserted: () => ({ commands }) => {
        return commands.unsetMark(this.name);
      },
    };
  },
});

/**
 * 修订 ID 标记 - 用于关联删除和插入的内容
 */
export const AIRevisionId = Mark.create({
  name: 'aiRevisionId',

  addOptions() {
    return {
      HTMLAttributes: {},
    };
  },

  addAttributes() {
    return {
      revisionId: {
        default: null,
        parseHTML: element => element.getAttribute('data-revision-id'),
        renderHTML: attributes => {
          if (!attributes.revisionId) {
            return {};
          }
          return {
            'data-revision-id': attributes.revisionId,
          };
        },
      },
    };
  },

  parseHTML() {
    return [
      {
        tag: '[data-revision-id]',
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    return ['span', mergeAttributes(this.options.HTMLAttributes, HTMLAttributes), 0];
  },
});

// 类型扩展
declare module '@tiptap/core' {
  interface Commands<ReturnType> {
    aiDeleted: {
      setAIDeleted: () => ReturnType;
      toggleAIDeleted: () => ReturnType;
      unsetAIDeleted: () => ReturnType;
    };
    aiInserted: {
      setAIInserted: () => ReturnType;
      toggleAIInserted: () => ReturnType;
      unsetAIInserted: () => ReturnType;
    };
  }
}

export default { AIDeleted, AIInserted, AIRevisionId };
