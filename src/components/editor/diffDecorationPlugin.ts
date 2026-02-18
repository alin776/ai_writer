/**
 * diffDecorationPlugin — ProseMirror 内联 Diff 装饰插件
 *
 * 在编辑器文档中定位 oldString，用 Decoration 标记红删绿增，
 * 不修改文档内容（docChanged === false），不触发自动保存。
 *
 * 触发方式：
 *   tr.setMeta(diffPluginKey, { oldString, newString })  — 显示 Diff
 *   tr.setMeta(diffPluginKey, { clear: true })            — 清除 Diff
 */

import DiffMatchPatch from 'diff-match-patch';
import { Plugin, PluginKey } from '@milkdown/prose/state';
import { Decoration, DecorationSet } from '@milkdown/prose/view';
import type { EditorState, Transaction } from '@milkdown/prose/state';
import type { Node as PmNode } from '@milkdown/prose/model';

export const diffPluginKey = new PluginKey<DecorationSet>('inlineDiff');

interface DiffMeta {
  oldString?: string;
  newString?: string;
  clear?: boolean;
  append?: boolean;   // true: 追加装饰而非替换（同文件多次编辑）
}

/**
 * 字符级位置映射：每个字符在 fullText 中的 index ↔ ProseMirror doc 中的 pos
 * docPos === -1 表示合成换行符（段落间隙），不对应实际文档位置
 */
interface CharInfo {
  docPos: number;
  char: string;
}

/**
 * 遍历 ProseMirror 文档，构建字符级位置映射。
 * 段落之间用 '\n' 分隔（和 Markdown 的 '\n\n' 不同！）
 */
function buildCharMap(doc: PmNode): CharInfo[] {
  const result: CharInfo[] = [];

  doc.descendants((node, pos) => {
    if (node.isText && node.text) {
      for (let i = 0; i < node.text.length; i++) {
        result.push({ docPos: pos + i, char: node.text[i] });
      }
    } else if (node.isBlock && result.length > 0 && result[result.length - 1].char !== '\n') {
      result.push({ docPos: -1, char: '\n' });
    }
    return true;
  });

  return result;
}

/**
 * 在 charMap 构建的 fullText 中查找 target 文本的起始索引。
 * 多策略匹配：精确 → 折叠换行 → 去除行首空白 → 去 Markdown 语法 → 首行模糊
 */
function findMatchIndex(fullText: string, target: string): { index: number; normalizedTarget: string } | null {
  // 策略 1：精确匹配
  let idx = fullText.indexOf(target);
  if (idx !== -1) return { index: idx, normalizedTarget: target };

  // 策略 2：折叠多换行（\n\n → \n）— Markdown 段落间距 vs ProseMirror 单换行
  const collapsed = target.replace(/\n{2,}/g, '\n');
  if (collapsed !== target) {
    idx = fullText.indexOf(collapsed);
    if (idx !== -1) return { index: idx, normalizedTarget: collapsed };
  }

  // 策略 3：去除每行行首空白（全角/半角空格缩进差异）
  const stripLeading = (s: string) => s.split('\n').map(l => l.replace(/^[\s\u3000]+/, '')).join('\n');
  const strippedTarget = stripLeading(collapsed);
  const strippedDoc = stripLeading(fullText);
  idx = strippedDoc.indexOf(strippedTarget);
  if (idx !== -1) {
    // 映射回原 fullText 的位置：按行逐一定位
    const targetLines = strippedTarget.split('\n');
    const firstLine = targetLines[0];
    // 在 fullText 各行中找第一行
    const docLines = fullText.split('\n');
    let charOffset = 0;
    for (const docLine of docLines) {
      const trimmed = docLine.replace(/^[\s\u3000]+/, '');
      if (trimmed.startsWith(firstLine)) {
        const leadingLen = docLine.length - trimmed.length;
        return { index: charOffset + leadingLen, normalizedTarget: strippedTarget };
      }
      charOffset += docLine.length + 1; // +1 for the '\n'
    }
  }

  // 策略 4：去除 Markdown 语法标记后匹配
  // Agent 返回原始 Markdown（含 ### - ** 等），ProseMirror 渲染后无这些标记
  const stripMd = (s: string) => s
    .replace(/^#{1,6}\s+/gm, '')                        // 标题标记
    .replace(/^[\s]*[-*+]\s+/gm, '')                    // 无序列表标记
    .replace(/^[\s]*(\*{3,}|-{3,}|_{3,})[\s]*$/gm, '')  // 水平线 *** --- ___
    .replace(/\*\*(.+?)\*\*/g, '$1')                    // 粗体
    .replace(/\*([^*\n]+)\*/g, '$1')                    // 斜体（排除 * 和换行）
    .replace(/\n{2,}/g, '\n')                           // 折叠多余换行
    .replace(/^\n+|\n+$/g, '');                         // 去头尾换行
  const mdStripped = stripMd(collapsed);
  if (mdStripped !== collapsed) {
    idx = fullText.indexOf(mdStripped);
    if (idx !== -1) return { index: idx, normalizedTarget: mdStripped };
  }

  // 策略 5：用首行做模糊定位（Markdown frontmatter/标题差异时降级）
  const firstTargetLine = collapsed.split('\n').find(l => l.trim().length > 10);
  if (firstTargetLine) {
    const trimmedFirst = firstTargetLine.trim();
    idx = fullText.indexOf(trimmedFirst);
    if (idx !== -1) {
      return { index: idx, normalizedTarget: collapsed };
    }
  }

  return null;
}

/**
 * 找到最近的有效 docPos（跳过 -1 的合成换行符）
 */
function nearestDocPos(charMap: CharInfo[], idx: number, direction: 'forward' | 'backward'): number {
  if (direction === 'forward') {
    for (let i = idx; i < charMap.length; i++) {
      if (charMap[i].docPos !== -1) return charMap[i].docPos;
    }
  } else {
    for (let i = idx; i >= 0; i--) {
      if (charMap[i].docPos !== -1) return charMap[i].docPos + 1;
    }
  }
  return 1; // fallback: doc start
}

/**
 * 段落信息：文档中一个段落节点的位置
 */
interface ParagraphInfo {
  text: string;
  paraNodeStart: number;
  paraNodeEnd: number;
}

/**
 * 从 charMap 的匹配区域构建段落列表。
 * 每遇到 docPos===-1 的合成 '\n' 就切一段。
 */
function buildParagraphMap(
  doc: PmNode,
  charMap: CharInfo[],
  startIdx: number,
  endIdx: number,
): ParagraphInfo[] {
  const paragraphs: ParagraphInfo[] = [];
  let segStart = startIdx;

  for (let i = startIdx; i <= endIdx; i++) {
    const atEnd = i === endIdx;
    const atNewline = !atEnd && charMap[i].docPos === -1 && charMap[i].char === '\n';

    if (atEnd || atNewline) {
      let text = '';
      let nodeStart = -1;
      let nodeEnd = -1;

      for (let j = segStart; j < i; j++) {
        text += charMap[j].char;
        if (nodeStart === -1 && charMap[j].docPos !== -1) {
          const $pos = doc.resolve(charMap[j].docPos);
          nodeStart = $pos.before($pos.depth);
          nodeEnd = nodeStart + $pos.parent.nodeSize;
        }
      }

      if (nodeStart !== -1) {
        paragraphs.push({ text, paraNodeStart: nodeStart, paraNodeEnd: nodeEnd });
      }
      segStart = i + 1;
    }
  }

  return paragraphs;
}

/**
 * 分割 diff_charsToLines_ 输出的文本为行数组
 * 每行在 DMP 输出中以 '\n' 结尾，最后一行可能没有
 */
function splitDiffLines(text: string): string[] {
  if (!text) return [];
  return text.endsWith('\n') ? text.slice(0, -1).split('\n') : text.split('\n');
}

/**
 * 创建绿色 INSERT widget（块级，每行独立）
 */
function createInsertWidget(pos: number, lines: string[]): Decoration {
  return Decoration.widget(pos, () => {
    const container = document.createElement('div');
    container.className = 'diff-ins-block';
    container.style.cssText = 'overflow:hidden;margin-left:-20px;margin-right:-20px;';

    for (const line of lines) {
      if (!line && lines.length > 1) continue;
      const row = document.createElement('div');
      row.style.cssText = 'display:flex;background:rgba(34,197,94,0.10);padding:1px 20px;line-height:1.6;';

      const prefix = document.createElement('span');
      prefix.style.cssText = 'width:16px;flex-shrink:0;text-align:center;color:#4ade80;font-size:13px;user-select:none;line-height:1.6;';
      prefix.textContent = '+';

      const content = document.createElement('span');
      content.style.cssText = 'flex:1;color:#4ade80;white-space:pre-wrap;word-break:break-all;line-height:1.6;';
      content.textContent = line;

      row.appendChild(prefix);
      row.appendChild(content);
      container.appendChild(row);
    }
    return container;
  }, { side: 1 });
}

/**
 * 创建带字符级高亮的绿色 INSERT widget（配对 DEL+INS 时使用）
 */
function createCharHighlightedInsertWidget(pos: number, charDiffs: [number, string][]): Decoration {
  return Decoration.widget(pos, () => {
    const container = document.createElement('div');
    container.className = 'diff-ins-block';
    container.style.cssText = 'overflow:hidden;margin-left:-20px;margin-right:-20px;';

    const row = document.createElement('div');
    row.style.cssText = 'display:flex;background:rgba(34,197,94,0.05);padding:1px 20px;line-height:1.6;';

    const prefix = document.createElement('span');
    prefix.style.cssText = 'width:16px;flex-shrink:0;text-align:center;color:#4ade80;font-size:13px;user-select:none;line-height:1.6;';
    prefix.textContent = '+';

    const content = document.createElement('span');
    content.style.cssText = 'flex:1;color:#4ade80;white-space:pre-wrap;word-break:break-all;line-height:1.6;';

    for (const [op, text] of charDiffs) {
      if (op === -1) continue; // 跳过删除的字符
      const span = document.createElement('span');
      span.textContent = text;
      if (op === 1) {
        span.style.cssText = 'background:rgba(34,197,94,0.35);border-radius:3px;padding:0 1px;';
      }
      content.appendChild(span);
    }

    row.appendChild(prefix);
    row.appendChild(content);
    container.appendChild(row);
    return container;
  }, { side: 1 });
}

/**
 * 构建 Decoration 列表（行级 diff）：
 * - EQUAL 段落 → 无装饰
 * - DELETE 段落 → Decoration.node() 红色背景 + "−" widget
 * - INSERT 段落 → Decoration.widget() 绿色块
 * - 配对 DEL+INS → 红 node + 绿 widget（单行时含字符级高亮）
 */
function buildDecorations(
  doc: PmNode,
  oldString: string,
  newString: string,
): DecorationSet {
  const decorations: Decoration[] = [];

  // 特殊情况：create 操作（oldString 为空），全部作为 INSERT 处理
  if (!oldString.trim()) {
    const lines = newString.split('\n');
    decorations.push(createInsertWidget(1, lines));
    return DecorationSet.create(doc, decorations);
  }

  const charMap = buildCharMap(doc);
  const fullText = charMap.map(c => c.char).join('');

  const match = findMatchIndex(fullText, oldString);
  if (!match) {
    console.warn('[DiffPlugin] oldString 未在文档中找到匹配');
    return DecorationSet.empty;
  }

  const matchEnd = match.index + match.normalizedTarget.length;
  const paragraphs = buildParagraphMap(doc, charMap, match.index, matchEnd);

  // 规范化 newString（与 findMatchIndex 的规范化保持一致）
  let normalizedNew = newString;
  if (match.normalizedTarget !== oldString) {
    normalizedNew = newString.replace(/\n{2,}/g, '\n');
  }

  // 行级 diff：用 diff_linesToChars_ / diff_charsToLines_ 做段落级比对
  const matchedText = fullText.substring(match.index, matchEnd);
  const dmp = new DiffMatchPatch();
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const d = dmp as any;
  const lineEnc = d.diff_linesToChars_(matchedText, normalizedNew);
  const diffs: [number, string][] = dmp.diff_main(lineEnc.chars1, lineEnc.chars2, false);
  d.diff_charsToLines_(diffs, lineEnc.lineArray);
  dmp.diff_cleanupSemantic(diffs);

  // 段落游标：跟踪当前处理到第几个旧段落
  let paraIdx = 0;

  for (let i = 0; i < diffs.length; i++) {
    const [op, text] = diffs[i];
    const lines = splitDiffLines(text);

    if (op === 0) {
      // EQUAL — 跳过，推进段落游标
      paraIdx += lines.length;

    } else if (op === -1) {
      // DELETE — 给对应段落加红色背景
      const isNextInsert = i + 1 < diffs.length && diffs[i + 1][0] === 1;

      for (let li = 0; li < lines.length; li++) {
        const para = paragraphs[paraIdx + li];
        if (!para) continue;

        decorations.push(
          Decoration.node(para.paraNodeStart, para.paraNodeEnd, {
            style: 'background-color:rgba(239,68,68,0.08);color:#f87171;margin-left:-20px;margin-right:-20px;padding-left:20px;padding-right:20px;',
            class: 'diff-del-line',
          }),
        );
        decorations.push(
          Decoration.widget(para.paraNodeStart + 1, () => {
            const s = document.createElement('span');
            s.style.cssText = 'color:#f87171;font-size:13px;user-select:none;margin-right:4px;line-height:1;';
            s.textContent = '−';
            return s;
          }, { side: -1 }),
        );
      }

      // 配对 DEL+INS：紧接 INSERT 时一起处理
      if (isNextInsert) {
        i++;
        const insLines = splitDiffLines(diffs[i][1]);
        const lastPara = paragraphs[paraIdx + lines.length - 1];
        const insertPos = lastPara ? lastPara.paraNodeEnd : 1;

        // 单行配对：用字符级高亮显示差异
        if (lines.length === 1 && insLines.length === 1) {
          const charDiffs = dmp.diff_main(lines[0], insLines[0]);
          dmp.diff_cleanupSemantic(charDiffs);

          // 删除行字符级高亮：用 Decoration.inline 标记被删除的字符
          const delPara = paragraphs[paraIdx];
          if (delPara) {
            const textStart = delPara.paraNodeStart + 1; // +1 跳过段落节点本身
            let charOffset = 0;
            for (const [cdOp, cdText] of charDiffs as [number, string][]) {
              if (cdOp === -1) {
                // 被删除的字符 — 红色高亮
                const from = textStart + charOffset;
                const to = from + cdText.length;
                if (to <= delPara.paraNodeEnd) {
                  decorations.push(
                    Decoration.inline(from, to, {
                      style: 'background:rgba(239,68,68,0.35);border-radius:3px;padding:0 1px;',
                    }),
                  );
                }
                charOffset += cdText.length;
              } else if (cdOp === 0) {
                // 未变化的字符 — 推进偏移
                charOffset += cdText.length;
              }
              // op === 1 (插入) 不占删除行的位置，跳过
            }
          }

          decorations.push(createCharHighlightedInsertWidget(insertPos, charDiffs as [number, string][]));
        } else {
          decorations.push(createInsertWidget(insertPos, insLines));
        }
      }

      paraIdx += lines.length;

    } else if (op === 1) {
      // 独立 INSERT（前面没有配对的 DELETE）
      const insertPos = paraIdx > 0 && paragraphs[paraIdx - 1]
        ? paragraphs[paraIdx - 1].paraNodeEnd
        : (paragraphs[0] ? paragraphs[0].paraNodeStart : 1);
      decorations.push(createInsertWidget(insertPos, lines));
    }
  }

  if (decorations.length === 0) return DecorationSet.empty;
  return DecorationSet.create(doc, decorations);
}

export function createDiffDecorationPlugin(): Plugin {
  return new Plugin({
    key: diffPluginKey,
    state: {
      init(): DecorationSet {
        return DecorationSet.empty;
      },
      apply(tr: Transaction, prev: DecorationSet, _oldState: EditorState, newState: EditorState): DecorationSet {
        const meta = tr.getMeta(diffPluginKey) as DiffMeta | undefined;
        if (meta) {
          if (meta.clear) {
            return DecorationSet.empty;
          }
          if (meta.oldString !== undefined && meta.newString) {
            const newDecs = buildDecorations(newState.doc, meta.oldString, meta.newString);
            if (meta.append && prev !== DecorationSet.empty) {
              // 追加模式：合并已有装饰 + 新装饰
              const existing = prev.find();
              const added = newDecs.find();
              return DecorationSet.create(newState.doc, [...existing, ...added]);
            }
            return newDecs;
          }
        }
        // 文档变化时，映射已有装饰位置
        if (tr.docChanged && prev !== DecorationSet.empty) {
          return prev.map(tr.mapping, tr.doc);
        }
        return prev;
      },
    },
    props: {
      decorations(state: EditorState): DecorationSet {
        return diffPluginKey.getState(state) ?? DecorationSet.empty;
      },
    },
  });
}
