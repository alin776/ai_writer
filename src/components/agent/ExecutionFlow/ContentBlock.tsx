/**
 * ContentBlock - 流式内容组件
 * 纯文本样式，无边框无背景，与现有 AIPanel 一致
 */

interface ContentBlockProps {
  content: string;
}

export function ContentBlock({ content }: ContentBlockProps) {
  if (!content) {
    return null;
  }

  const normalized = content
    .split(/\r?\n/)
    .map((line) => line.replace(/^[\s\u00a0\u2000-\u200b\u202f\u205f\u3000\uFEFF]+/, ''))
    .join('\n');

  return (
    <div className="my-3">
      <div className="text-[13px] text-slate-500 dark:text-slate-300 whitespace-pre-wrap leading-[1.7]">
        {normalized}
      </div>
    </div>
  );
}
