import React, { useState, useEffect, useCallback } from 'react';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import {
  Undo,
  Redo,
  Bold,
  Italic,
  Underline,
  Strikethrough,
  List,
  ListOrdered,
  Link,
  Image,
  Sparkles,
  AlignLeft,
  AlignCenter,
  AlignRight,
  CheckSquare,
  Paperclip,
  Minus,
  PenTool,
} from 'lucide-react';

interface NovelEditorWrapperProps {
  content: string;
  onSave: (content: string, json: any) => void;
  placeholder?: string;
  autoSave?: boolean;
  autoSaveInterval?: number;
}

// HTML 转纯文本的辅助函数
const htmlToPlainText = (html: string): string => {
  if (!html) return '';

  // 创建一个临时 div 来解析 HTML
  const temp = document.createElement('div');
  temp.innerHTML = html;

  // 获取纯文本
  return temp.textContent || temp.innerText || '';
};

// 纯文本转 HTML 的辅助函数（保存时使用）
const plainTextToHtml = (text: string): string => {
  if (!text) return '';

  // 将换行符转换为段落
  const paragraphs = text.split('\n\n').filter(p => p.trim());
  if (paragraphs.length === 0) return '';

  return paragraphs.map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`).join('');
};

export function NovelEditorWrapper({
  content: initialContent,
  onSave,
  placeholder = '开始写作...',
  autoSave = true,
  autoSaveInterval = 3000,
}: NovelEditorWrapperProps) {
  // 将 HTML 内容转换为纯文本
  const [content, setContent] = useState(() => htmlToPlainText(initialContent));
  const [wordCount, setWordCount] = useState(0);
  const [charCount, setCharCount] = useState(0);
  const [isSaved, setIsSaved] = useState(true);

  // 更新字数统计
  useEffect(() => {
    const text = content.trim();
    // 中文字符数
    const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    // 英文单词数
    const englishWords = text.split(/\s+/).filter(word => /[a-zA-Z]/.test(word)).length;
    setWordCount(chineseChars + englishWords);
    setCharCount(content.length);
  }, [content]);

  // 自动保存
  useEffect(() => {
    if (!autoSave) return;

    const timer = setTimeout(() => {
      if (!isSaved) {
        // 将纯文本转换回 HTML 格式保存
        const htmlContent = plainTextToHtml(content);
        onSave(htmlContent, {});
        setIsSaved(true);
      }
    }, autoSaveInterval);

    return () => clearTimeout(timer);
  }, [content, autoSave, autoSaveInterval, onSave, isSaved]);

  // 内容变化处理
  const handleContentChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setContent(e.target.value);
    setIsSaved(false);
  }, []);

  // 同步外部内容变化
  useEffect(() => {
    const plainText = htmlToPlainText(initialContent);
    setContent(plainText);
  }, [initialContent]);

  return (
    <div className="h-full flex flex-col bg-white">
      {/* 工具栏 - 添加轻微阴影 */}
      <div className="px-3 py-1.5 flex items-center gap-1.5 border-b border-zinc-100 bg-white shadow-sm shadow-zinc-100/50">
        {/* 撤销重做 */}
        <div className="flex items-center">
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-400 hover:text-zinc-700 hover:bg-zinc-50 transition-all">
            <Undo className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-400 hover:text-zinc-700 hover:bg-zinc-50 transition-all">
            <Redo className="h-3 w-3" />
          </Button>
        </div>

        <div className="w-px h-4 bg-zinc-200" />

        {/* 标题 */}
        <div className="flex items-center">
          <Button variant="ghost" size="sm" className="h-7 px-2 text-[11px] text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            H1
          </Button>
          <Button variant="ghost" size="sm" className="h-7 px-2 text-[11px] text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            H2
          </Button>
          <Button variant="ghost" size="sm" className="h-7 px-2 text-[11px] text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            H3
          </Button>
        </div>

        <div className="w-px h-4 bg-zinc-200" />

        {/* 文本样式 */}
        <div className="flex items-center">
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <Bold className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <Italic className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <Underline className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <Strikethrough className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <PenTool className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <code className="text-[10px]">&lt;/&gt;</code>
          </Button>
        </div>

        <div className="w-px h-4 bg-zinc-200" />

        {/* 列表 */}
        <div className="flex items-center">
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <List className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <ListOrdered className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <CheckSquare className="h-3 w-3" />
          </Button>
        </div>

        <div className="w-px h-4 bg-zinc-200" />

        {/* 对齐 */}
        <div className="flex items-center">
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <AlignLeft className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <AlignCenter className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <AlignRight className="h-3 w-3" />
          </Button>
        </div>

        <div className="w-px h-4 bg-zinc-200" />

        {/* 插入 */}
        <div className="flex items-center">
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <Paperclip className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <Minus className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <Link className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-all">
            <Image className="h-3 w-3" />
          </Button>
        </div>

        <div className="flex-1" />

        {/* AI续写 */}
        <Button size="sm" className="h-7 bg-zinc-900 hover:bg-zinc-800 text-white px-3 text-[12px] transition-all">
          <Sparkles className="h-3 w-3 mr-1.5" />
          AI 续写
        </Button>
      </div>

      {/* 状态栏 */}
      <div className="px-5 py-1.5 flex items-center justify-between text-[11px] border-b border-zinc-100 bg-zinc-50/40">
        <div className="flex items-center gap-4 text-zinc-400">
          <span>字数 {wordCount.toLocaleString()}</span>
          <span>字符 {charCount.toLocaleString()}</span>
        </div>
        <div className={`flex items-center gap-1.5 ${isSaved ? 'text-emerald-500' : 'text-amber-500'}`}>
          <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {isSaved ? (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            )}
          </svg>
          <span>{isSaved ? '已保存' : '保存中...'}</span>
        </div>
      </div>

      {/* 编辑区 - 优化行高和字间距 */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full mx-auto px-8 py-8 flex flex-col" style={{ maxWidth: '900px' }}>
          <Textarea
            value={content}
            onChange={handleContentChange}
            className="w-full h-full border-none shadow-none focus:ring-0 focus:outline-none focus-visible:ring-0 focus-visible:outline-none resize-none text-zinc-700 bg-transparent p-0 overflow-y-auto custom-scrollbar"
            style={{
              fontSize: '15px',
              lineHeight: '2',
              letterSpacing: '0.02em',
              outline: 'none',
              boxShadow: 'none',
            }}
            placeholder={placeholder}
          />
        </div>
      </div>
    </div>
  );
}
