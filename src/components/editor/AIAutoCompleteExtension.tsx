/**
 * AI 自动补全扩展
 * 光标停留3秒后自动触发AI补全
 */
import { Extension } from '@tiptap/core';
import { Plugin, PluginKey } from '@tiptap/pm/state';
import { Decoration, DecorationSet } from '@tiptap/pm/view';

export interface AIAutoCompleteOptions {
  delay: number; // 延迟时间（毫秒）
  onTrigger: (text: string) => Promise<string>;
  enabled: boolean;
}

const AIAutoCompletePluginKey = new PluginKey('aiAutoComplete');

export const AIAutoCompleteExtension = Extension.create<AIAutoCompleteOptions>({
  name: 'aiAutoComplete',

  addOptions() {
    return {
      delay: 3000, // 默认3秒
      onTrigger: async () => '',
      enabled: true,
    };
  },

  addProseMirrorPlugins() {
    const { delay, onTrigger, enabled } = this.options;
    let timeout: NodeJS.Timeout | null = null;
    let currentSuggestion = '';
    let suggestionFrom = 0;
    let isGenerating = false;

    return [
      new Plugin({
        key: AIAutoCompletePluginKey,

        state: {
          init() {
            return DecorationSet.empty;
          },
          apply(tr, set) {
            // 如果文档有变化，清除建议
            if (tr.docChanged) {
              currentSuggestion = '';
              return DecorationSet.empty;
            }

            // 获取插件元数据
            const pluginMeta = tr.getMeta(AIAutoCompletePluginKey);
            if (pluginMeta?.decorations) {
              return pluginMeta.decorations;
            }

            return set.map(tr.mapping, tr.doc);
          },
        },

        props: {
          decorations(state) {
            return this.getState(state);
          },

          handleKeyDown(view, event) {
            // Tab 键接受建议
            if (event.key === 'Tab' && currentSuggestion) {
              event.preventDefault();

              const { state, dispatch } = view;
              const tr = state.tr.insertText(currentSuggestion, suggestionFrom);
              dispatch(tr);

              // 清除建议
              currentSuggestion = '';
              return true;
            }

            // Escape 键取消建议
            if (event.key === 'Escape' && currentSuggestion) {
              event.preventDefault();
              currentSuggestion = '';

              // 清除装饰器
              const { state, dispatch } = view;
              const tr = state.tr;
              tr.setMeta(AIAutoCompletePluginKey, {
                decorations: DecorationSet.empty,
              });
              dispatch(tr);
              return true;
            }

            return false;
          },
        },

        view() {
          return {
            update: async (view) => {
              if (!enabled) return;

              const { state } = view;
              const { selection } = state;

              // 清除之前的定时器
              if (timeout) {
                clearTimeout(timeout);
                timeout = null;
              }

              // 如果正在生成，不触发新的请求
              if (isGenerating) return;

              // 如果有选中内容，不触发
              if (!selection.empty) return;

              // 获取光标前的文本（最近200个字符）
              const { from } = selection;
              const textBefore = state.doc.textBetween(
                Math.max(0, from - 200),
                from,
                ' '
              );

              // 如果文本太短，不触发
              if (textBefore.trim().length < 10) return;

              // 设置新的定时器
              timeout = setTimeout(async () => {
                try {
                  console.log('[AI自动补全] 开始生成建议...');
                  isGenerating = true;
                  suggestionFrom = from;

                  // 调用 AI 生成
                  const suggestion = await onTrigger(textBefore);

                  if (suggestion && suggestion.trim()) {
                    currentSuggestion = suggestion.trim();
                    console.log('[AI自动补全] 建议:', currentSuggestion);

                    // 创建装饰器显示建议
                    const decoration = Decoration.widget(
                      from,
                      () => {
                        const span = document.createElement('span');
                        span.className = 'ai-suggestion';
                        span.textContent = currentSuggestion;
                        return span;
                      },
                      { side: 1 }
                    );

                    // 更新装饰器
                    const { state: currentState, dispatch } = view;
                    const tr = currentState.tr;
                    tr.setMeta(AIAutoCompletePluginKey, {
                      decorations: DecorationSet.create(currentState.doc, [decoration]),
                    });
                    dispatch(tr);
                  }
                } catch (error) {
                  console.error('[AI自动补全] 失败:', error);
                } finally {
                  isGenerating = false;
                }
              }, delay);
            },

            destroy: () => {
              if (timeout) {
                clearTimeout(timeout);
              }
            },
          };
        },
      }),
    ];
  },
});
