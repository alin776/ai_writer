/**
 * 内容解析 Hook
 * 将 HTML 内容解析为结构化的段落和句子数据
 */
import { useMemo } from 'react';

export interface ParsedSentence {
  index: number;
  text: string;
  startOffset: number;
  endOffset: number;
}

export interface ParsedParagraph {
  index: number;
  text: string;
  sentences: ParsedSentence[];
  commentCount: number;
}

export interface ParsedContent {
  paragraphs: ParsedParagraph[];
  rawText: string;
}

export interface CommentStats {
  chapter: number;
  paragraphs: Record<string, number>;
  sentences: Record<string, number>;
  total: number;
}

/**
 * 中文句子分割正则
 * 匹配：句号、问号、感叹号（包括全角和半角）
 * 注意：不在引号内的标点才分割
 */
const SENTENCE_END_REGEX = /([。！？.!?]+)/g;

/**
 * 解析段落为句子
 */
function parseSentences(paragraphText: string): ParsedSentence[] {
  const sentences: ParsedSentence[] = [];
  const text = paragraphText.trim();

  if (!text) return sentences;

  // 使用正则分割句子
  const parts = text.split(SENTENCE_END_REGEX);
  let currentOffset = 0;
  let sentenceIndex = 0;
  let currentSentence = '';

  for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    if (!part) continue;

    // 检查是否是句子结束标点
    if (SENTENCE_END_REGEX.test(part)) {
      // 将标点加到当前句子
      currentSentence += part;

      // 保存句子
      if (currentSentence.trim()) {
        sentences.push({
          index: sentenceIndex,
          text: currentSentence.trim(),
          startOffset: currentOffset - currentSentence.length + part.length,
          endOffset: currentOffset + part.length
        });
        sentenceIndex++;
      }
      currentSentence = '';
      currentOffset += part.length;
    } else {
      currentSentence += part;
      currentOffset += part.length;
    }
  }

  // 处理最后一个没有标点的句子
  if (currentSentence.trim()) {
    sentences.push({
      index: sentenceIndex,
      text: currentSentence.trim(),
      startOffset: currentOffset - currentSentence.length,
      endOffset: currentOffset
    });
  }

  // 如果没有分割出句子，整个段落作为一个句子
  if (sentences.length === 0 && text) {
    sentences.push({
      index: 0,
      text: text,
      startOffset: 0,
      endOffset: text.length
    });
  }

  return sentences;
}

/**
 * 从 HTML 中提取纯文本
 */
function extractTextFromHtml(html: string): string {
  const div = document.createElement('div');
  div.innerHTML = html;
  return div.textContent || div.innerText || '';
}

/**
 * 解析 HTML 内容为段落数组
 */
function parseHtmlContent(htmlContent: string): ParsedParagraph[] {
  const paragraphs: ParsedParagraph[] = [];

  if (!htmlContent) return paragraphs;

  // 创建临时 DOM 解析 HTML
  const div = document.createElement('div');
  div.innerHTML = htmlContent;

  // 获取所有段落元素（p, div 或直接的文本节点）
  const elements = div.querySelectorAll('p, div');

  if (elements.length > 0) {
    elements.forEach((el, index) => {
      const text = (el.textContent || '').trim();
      if (text) {
        paragraphs.push({
          index,
          text,
          sentences: parseSentences(text),
          commentCount: 0
        });
      }
    });
  } else {
    // 如果没有 p/div 标签，按换行符分割
    const rawText = extractTextFromHtml(htmlContent);
    const lines = rawText.split(/\n+/);

    lines.forEach((line, index) => {
      const text = line.trim();
      if (text) {
        paragraphs.push({
          index,
          text,
          sentences: parseSentences(text),
          commentCount: 0
        });
      }
    });
  }

  return paragraphs;
}

/**
 * 合并评论统计到段落数据
 */
function mergeCommentStats(
  paragraphs: ParsedParagraph[],
  stats: CommentStats | null
): ParsedParagraph[] {
  if (!stats) return paragraphs;

  return paragraphs.map(p => ({
    ...p,
    commentCount: stats.paragraphs[String(p.index)] || 0,
    sentences: p.sentences.map(s => ({
      ...s,
      commentCount: stats.sentences[`${p.index}-${s.index}`] || 0
    }))
  }));
}

/**
 * 内容解析 Hook
 *
 * @param htmlContent - HTML 格式的章节内容
 * @param commentStats - 评论位置统计数据
 * @returns 解析后的结构化内容
 */
export function useContentParser(
  htmlContent: string,
  commentStats: CommentStats | null = null
): ParsedContent {
  return useMemo(() => {
    const paragraphs = parseHtmlContent(htmlContent);
    const withStats = mergeCommentStats(paragraphs, commentStats);
    const rawText = extractTextFromHtml(htmlContent);

    return {
      paragraphs: withStats,
      rawText
    };
  }, [htmlContent, commentStats]);
}

/**
 * 根据点击位置检测所在的段落和句子
 */
export function detectLocationFromElement(
  element: HTMLElement | null
): { paragraphIndex: number; sentenceIndex?: number } | null {
  if (!element) return null;

  // 向上查找带有 data-paragraph-index 的元素
  let current: HTMLElement | null = element;
  while (current) {
    const paragraphIndex = current.dataset?.paragraphIndex;
    if (paragraphIndex !== undefined) {
      const sentenceIndex = current.dataset?.sentenceIndex;
      return {
        paragraphIndex: parseInt(paragraphIndex, 10),
        sentenceIndex: sentenceIndex !== undefined ? parseInt(sentenceIndex, 10) : undefined
      };
    }
    current = current.parentElement;
  }

  return null;
}

/**
 * 获取选中文本所在的句子
 */
export function getSelectedSentence(
  paragraphs: ParsedParagraph[],
  paragraphIndex: number,
  selectedText: string
): ParsedSentence | null {
  const paragraph = paragraphs[paragraphIndex];
  if (!paragraph) return null;

  // 查找包含选中文本的句子
  for (const sentence of paragraph.sentences) {
    if (sentence.text.includes(selectedText)) {
      return sentence;
    }
  }

  return null;
}

export default useContentParser;
