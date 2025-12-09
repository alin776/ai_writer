/**
 * AI 自动补全扩展（流式版本）
 *
 * 触发条件（需同时满足）：
 * 1. 文本长度达到最小字符数（默认 50）
 * 2. 光标停留足够长时间（默认 2 秒）
 * 3. 编辑器获得焦点
 * 4. 不在列表/标题/代码块/引用内
 */

import { Extension } from '@tiptap/core';
import { Plugin, PluginKey } from '@tiptap/pm/state';
import { Decoration, DecorationSet } from '@tiptap/pm/view';

export interface AIAutoCompleteOptions {
  delay: number; // 延迟时间（毫秒）
  minChars: number; // 最少字符数
  onTrigger: (text: string, onChunk: (chunk: string, fullText: string) => void) => Promise<string>;
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
      delay: 1500, // 默认1.5秒（从2秒优化）
      minChars: 50, // 至少50个字符才触发
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
    let lastTriggerPos = 0;
    let lastTriggerTime = 0;
    let muteUntil = 0;
    let generationId = 0; // 用于取消过期的生成
    let lastDecorationUpdate = 0; // 上次装饰器更新时间（用于防抖）
    const DECORATION_UPDATE_INTERVAL = 200; // 装饰器更新间隔（毫秒，优化为200ms避免显示不一致）
    const GENERATION_TIMEOUT = 15000; // 生成超时时间（毫秒，15秒）
    let awaitingDecision = false; // ⏸️ 已给出建议，等待用户 Tab/Esc 处理前不再生成
    let lastCachedSuggestion: { text: string; suggestion: string } | null = null; // 复用最近上下文的结果

    // 创建建议文字 widget（透明文字 + 小图标在左上角）
    const createSuggestionWidget = (text: string, isGenerating: boolean) => {
      const container = document.createElement('span');
      container.className = 'ai-suggestion-container';

      // 小图标（左上角定位）
      const icon = document.createElement('span');
      icon.className = `ai-suggestion-icon ${isGenerating ? 'generating' : ''}`;
      icon.textContent = isGenerating ? '○' : '✦';
      container.appendChild(icon);

      // 只有在生成完成且有内容时才显示 tooltip（Tab/Esc 提示）
      if (text && !isGenerating) {
        const tooltip = document.createElement('div');
        tooltip.className = 'ai-suggestion-tooltip';
        tooltip.innerHTML = `
          <span class="ai-tip-pair">
            <span class="ai-tip-key">Tab</span><span class="ai-tip-text">采纳</span>
          </span>
          <span class="ai-tip-divider"></span>
          <span class="ai-tip-pair">
            <span class="ai-tip-key">Esc</span><span class="ai-tip-text">撤销</span>
          </span>
        `;
        container.appendChild(tooltip);
      }

      // 透明建议文字
      const suggestion = document.createElement('span');
      suggestion.className = 'ai-suggestion';
      suggestion.textContent = text || (isGenerating ? '...' : '');
      container.appendChild(suggestion);

      return container;
    };

    // 更新装饰器显示建议文字（带防抖优化）
    const updateDecoration = (view: any, from: number, text: string, isGenerating: boolean = false, force: boolean = false) => {
      const now = Date.now();

      // 防抖：生成中状态下，限制更新频率（除非强制更新）
      if (isGenerating && !force && (now - lastDecorationUpdate < DECORATION_UPDATE_INTERVAL)) {
        return;
      }
      lastDecorationUpdate = now;

      const decoration = Decoration.widget(
        from,
        () => createSuggestionWidget(text, isGenerating),
        { side: 1 }
      );

      const { state, dispatch } = view;
      const tr = state.tr;
      tr.setMeta(AIAutoCompletePluginKey, {
        decorations: DecorationSet.create(state.doc, [decoration]),
      });
      dispatch(tr);
    };

    return [
      new Plugin({
        key: AIAutoCompletePluginKey,

        state: {
          init() {
            return DecorationSet.empty;
          },
          apply(tr, set) {
            if (tr.docChanged) {
              currentSuggestion = '';
              generationId++; // 取消正在进行的生成
              awaitingDecision = false; // 用户继续输入视为放弃当前建议，解锁后续生成
              lastCachedSuggestion = null;
              return DecorationSet.empty;
            }

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
            if (event.key === 'Tab') {
              if (currentSuggestion) {
                event.preventDefault();

                const { state, dispatch } = view;
                const tr = state.tr.insertText(currentSuggestion, suggestionFrom);
                dispatch(tr);
              }
              if (currentSuggestion || awaitingDecision) {
                currentSuggestion = '';
                awaitingDecision = false;
                muteUntil = Date.now(); // 立即允许再次触发
                lastTriggerPos = 0;
                lastTriggerTime = 0;
                lastCachedSuggestion = null; // 用户已处理，下一次重新生成
                return true;
              }
            }

            // Escape 键取消建议
            if (event.key === 'Escape') {
              if (currentSuggestion || awaitingDecision) {
                event.preventDefault();
                currentSuggestion = '';
                awaitingDecision = false;
                muteUntil = Date.now(); // 立刻允许后续生成
                lastTriggerPos = 0;
                lastTriggerTime = 0;
                lastCachedSuggestion = null; // 用户拒绝，下一次必须重新生成

                const { state, dispatch } = view;
                const tr = state.tr;
                tr.setMeta(AIAutoCompletePluginKey, {
                  decorations: DecorationSet.empty,
                });
                dispatch(tr);
                return true;
              }
            }

            return false;
          },
        },

        view() {
          return {
            update: async (view) => {
              // 从 storage 读取 enabled 状态
              if (!storage.enabled) return;

              // 只有编辑器获得焦点时才触发
              if (!view.hasFocus()) return;

              const { state } = view;
              const { selection } = state;

              // 已有生成结果且用户尚未处理（Tab/Esc），暂停后续触发，避免重复消耗
              if (awaitingDecision) return;

              // 清除之前的定时器
              if (timeout) {
                clearTimeout(timeout);
                timeout = null;
              }

              // 如果正在生成，不触发新的请求
              if (isGenerating) return;

              // 如果有选中内容，不触发
              if (!selection.empty) return;

              // 块级过滤
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

              // 获取光标前的文本
              const { from } = selection;
              const textBefore = state.doc.textBetween(
                Math.max(0, from - 200),
                from,
                ' '
              );
              const trimmed = textBefore.trim();

              // 文本太短不触发
              if (trimmed.length < minChars) return;

              const now = Date.now();

              // 静默期检查
              if (now < muteUntil) return;

              // 同一位置5秒内只触发一次
              if (from === lastTriggerPos && now - lastTriggerTime < 5000) return;

              // 命中缓存：相同上下文直接复用，避免重复生成
              if (lastCachedSuggestion?.text === trimmed && lastCachedSuggestion.suggestion) {
                currentSuggestion = lastCachedSuggestion.suggestion;
                suggestionFrom = from;
                lastTriggerPos = from;
                lastTriggerTime = now;
                updateDecoration(view, from, currentSuggestion, false, true);
                awaitingDecision = true;
                return;
              }

              // 设置定时器
              timeout = setTimeout(async () => {
                const currentGenId = ++generationId; // 记录当前生成 ID
                try {
                  console.log('[AI自动补全] 开始流式生成...');
                  isGenerating = true;
                  suggestionFrom = from;
                  lastTriggerPos = from;
                  lastTriggerTime = Date.now();
                  currentSuggestion = '';

                  // 显示生成中状态
                  updateDecoration(view, from, '', true);

                  // 创建超时 Promise
                  const timeoutPromise = new Promise<string>((_, reject) => {
                    setTimeout(() => reject(new Error('AI 续写超时')), GENERATION_TIMEOUT);
                  });

                  // 流式生成，边生成边更新显示（带超时保护）
                  await Promise.race([
                    onTrigger(textBefore, (chunk: string, fullText: string) => {
                      // 检查是否已被取消（用户输入导致 generationId 变化）
                      if (generationId !== currentGenId) return;

                      currentSuggestion = fullText.trim();
                      if (currentSuggestion) {
                        // 生成中，显示当前内容
                        updateDecoration(view, from, currentSuggestion, true);
                      }
                    }),
                    timeoutPromise
                  ]);

                  // 检查是否已被取消
                  if (generationId !== currentGenId) {
                    console.log('[AI自动补全] 生成已被取消');
                    return;
                  }

                  // 生成完成
                  if (currentSuggestion) {
                    // 有内容，显示最终结果（强制更新，确保不被防抖跳过）
                    updateDecoration(view, from, currentSuggestion, false, true);
                console.log('[AI自动补全] 完成:', currentSuggestion);
                awaitingDecision = true; // 锁定，等待 Tab / Esc
                lastCachedSuggestion = { text: trimmed, suggestion: currentSuggestion };
              } else {
                // 无内容，清除装饰器
                const { state: currentState, dispatch } = view;
                const tr = currentState.tr;
                tr.setMeta(AIAutoCompletePluginKey, {
                  decorations: DecorationSet.empty,
                });
                dispatch(tr);
                awaitingDecision = false;
                currentSuggestion = '';
              }
            } catch (error) {
              // 检查是否已被取消
              if (generationId !== currentGenId) return;

                  // 超时错误特殊处理：如果已有部分内容，仍然显示让用户采纳
                  if (error instanceof Error && error.message === 'AI 续写超时' && currentSuggestion) {
                    console.log('[AI自动补全] 超时，但已有部分内容:', currentSuggestion);
                    updateDecoration(view, from, currentSuggestion, false, true);
                    awaitingDecision = true;
                    lastCachedSuggestion = { text: trimmed, suggestion: currentSuggestion };
                    return;
                  }

              console.error('[AI自动补全] 失败:', error);
              currentSuggestion = '';
              awaitingDecision = false;
              lastCachedSuggestion = null;
              // 清除装饰器
              const { state: currentState, dispatch } = view;
              const tr = currentState.tr;
              tr.setMeta(AIAutoCompletePluginKey, {
                    decorations: DecorationSet.empty,
                  });
                  dispatch(tr);
                } finally {
                  if (generationId === currentGenId) {
                    isGenerating = false;
                  }
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





