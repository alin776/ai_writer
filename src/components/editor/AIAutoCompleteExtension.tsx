/**
 * AI 自动补全扩展
 *
 * 触发条件（需同时满足）：
 * 1. 文本长度达到最小字符数（默认 120）
 * 2. 光标停留足够长时间（默认 3 秒）
 * 3. 1 秒内按键不超过 2 次（避免快速输入时打扰）
 * 4. 在句末或长停顿；Esc 后静默 30 秒
 * 5. 块级过滤：列表/标题/代码块/引用内不触发
 */

import { Extension } from '@tiptap/core';
import { Plugin, PluginKey } from '@tiptap/pm/state';
import { Decoration, DecorationSet } from '@tiptap/pm/view';

export interface AIAutoCompleteOptions {
  delay: number; // 延迟时间（毫秒）
  minChars: number; // 最少字符数
  onTrigger: (text: string) => Promise<string>;
  enabled: boolean;
}

export interface AIAutoCompleteStorage {
  enabled: boolean;
}

const AIAutoCompletePluginKey = new PluginKey('aiAutoComplete');

export const AIAutoCompleteExtension = Extension.create<AIAutoCompleteOptions, AIAutoCompleteStorage>({
  name: 'aiAutoComplete',

  addOptions() {
    return {
      delay: 3000, // 默认3秒，降低打扰
      minChars: 120, // 至少120个字符才触发
      onTrigger: async () => '',
      enabled: true,
    };
  },

  addStorage() {
    return {
      enabled: this.options.enabled,
    };
  },

  addProseMirrorPlugins() {
    const { delay, onTrigger, minChars } = this.options;
    const storage = this.storage;
    let timeout: NodeJS.Timeout | null = null;
    let currentSuggestion = '';
    let suggestionFrom = 0;
    let isGenerating = false;
    let lastKeystrokeTime = 0;
    let keystrokeCount = 0;
    let lastTriggerPos = 0;
    let lastTriggerTime = 0;
    let muteUntil = 0;

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

            // 读取插件元数据
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

            // Escape 键取消建议并暂停一段时间
            if (event.key === 'Escape') {
              event.preventDefault();
              currentSuggestion = '';
              muteUntil = Date.now() + 30000; // 30s 内不再自动弹出

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
            // 从 storage 读取 enabled 状态（支持动态更新）
            if (!storage.enabled) return;

            // 只有编辑器获得焦点时才触发自动补全
            if (!view.hasFocus()) return;

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

            // 如果光标处于列表/标题/代码块/引用等块级节点，不触发，避免干扰结构化编辑
            const $from = selection.$from;
            const parent = $from.parent;
            if (
              parent.type.name === 'bulletList' ||
              parent.type.name === 'orderedList' ||
              parent.type.name === 'heading' ||
              parent.type.name === 'codeBlock' ||
              parent.type.name === 'blockquote'
            ) {
              return;
            }

            // 获取光标前的文本（最近200个字符）
            const { from } = selection;
            const textBefore = state.doc.textBetween(
              Math.max(0, from - 200),
              from,
              ' '
            );
            const trimmed = textBefore.trim();

            // 如果文本太短，不触发（使用配置的最小字符数）
            if (trimmed.length < minChars) return;

            const now = Date.now();

            // 用户主动按下 Esc 后，短时间内不再弹出
            if (now < muteUntil) return;

            // 检测用户是否正在快速输入（键盘速度检测）
            if (now - lastKeystrokeTime < 1000) {
              // 1秒内有新按键，说明正在快速输入
              keystrokeCount++;
            } else {
              // 超过1秒，重置计数
              keystrokeCount = 1;
            }
            lastKeystrokeTime = now;

            // 如果用户正在快速输入（1秒内超过2个按键），不触发
            if (keystrokeCount > 2) return;

            // 检查是否在句子末尾（中英文句号、问号、感叹号），否则仅在停顿时触发
            const isSentenceEnd = /[.!?。！？]$/.test(trimmed);

            // 只在句子末尾或长时间停顿时触发
            if (!isSentenceEnd && keystrokeCount > 1) return;

            // 同一位置10秒内只触发一次，降低频率
            if (from === lastTriggerPos && now - lastTriggerTime < 10000) return;

            // 设置新的定时器
            timeout = setTimeout(async () => {
              try {
                console.log('[AI自动补全] 开始生成建议...');
                isGenerating = true;
                suggestionFrom = from;
                lastTriggerPos = from;
                lastTriggerTime = Date.now();

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





