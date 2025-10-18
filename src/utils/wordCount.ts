/**
 * 字数统计工具
 * 与后端算法保持一致
 */

/**
 * 从HTML内容中提取纯文本
 * @param html HTML内容
 * @returns 纯文本
 */
export function stripHtml(html: string): string {
  if (!html) return '';
  
  // 创建临时DOM元素来解析HTML
  const temp = document.createElement('div');
  temp.innerHTML = html;
  
  // 获取纯文本
  return temp.textContent || temp.innerText || '';
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
