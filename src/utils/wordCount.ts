/**
 * 字数统计工具
 * 与后端算法保持一致
 */

/**
 * 将 HTML 转为保留换行的纯文本
 * - 先把常见块级/换行标签转成换行符，再用 DOM 去掉其它标签
 * - 最后规范换行，最大化保留段落结构
 */
export function htmlToPlainText(html: string): string {
  if (!html) return '';

  // 先把常见块级/换行标签转成换行
  const htmlWithBreaks = html
    .replace(/<(br)\s*\/?>/gi, '\n')
    .replace(
      /<\/(p|div|section|article|header|footer|aside|main|nav|figure|figcaption|blockquote|pre|li|ul|ol|h[1-6]|table|tr|td|th)>/gi,
      '\n'
    );

  const temp = document.createElement('div');
  temp.innerHTML = htmlWithBreaks;
  const text = temp.textContent || temp.innerText || '';

  // 规范换行与尾部空白：保留段落分隔，避免过多空行
  const normalized = text
    .replace(/\r\n?/g, '\n')
    .split('\n')
    .map((line) => line.replace(/\s+$/g, '')) // 去除行尾空白但保留前导空白
    .join('\n')
    .replace(/\n{3,}/g, '\n\n') // 最多保留一个空行作为段落分隔
    .trim();

  return normalized;
}

/**
 * 从HTML内容中提取纯文本（用于字数统计，折叠空白）
 * @param html HTML内容
 * @returns 纯文本
 */
export function stripHtml(html: string): string {
  const plainText = htmlToPlainText(html);
  if (!plainText) return '';
  return plainText.replace(/\s+/g, ' ').trim();
}

/**
 * 计算文本字数（与后端算法一致）
 * - 中文：按字符数
 * - 英文：按单词数
 * - 数字：按字符数
 * 
 * @param text 纯文本内容
 * @returns 字数
 */
export function calculateWordCount(text: string): number {
  if (!text) return 0;
  
  // 移除多余的空白字符
  text = text.replace(/\s+/g, ' ').trim();
  
  // 计算中文字符数
  const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  
  // 计算英文单词数
  const englishWords = (text.match(/[a-zA-Z]+/g) || []).length;
  
  // 计算数字字符数
  const digits = (text.match(/[0-9]/g) || []).length;
  
  // 返回总字数（中文 + 英文单词 + 数字）
  return chineseChars + englishWords + digits;
}

/**
 * 从HTML内容计算字数
 * @param html HTML内容
 * @returns 字数
 */
export function countWordsInHtml(html: string): number {
  const text = stripHtml(html);
  return calculateWordCount(text);
}

/**
 * 获取编辑器内容的字数
 * 兼容Tiptap编辑器
 * @param editor Tiptap编辑器实例
 * @returns 字数
 */
export function getEditorWordCount(editor: any): number {
  if (!editor) return 0;
  
  // 获取HTML内容
  const html = editor.getHTML();
  return countWordsInHtml(html);
}

/**
 * 计算字符数（不包括HTML标签）
 * @param html HTML内容
 * @returns 字符数
 */
export function countCharactersInHtml(html: string): number {
  const text = stripHtml(html);
  return text.length;
}
