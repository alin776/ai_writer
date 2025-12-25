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

  return (
    <div className="my-3">
      <div className="text-[13px] text-slate-500 dark:text-slate-300 whitespace-pre-wrap leading-[1.7]">
        {content}
      </div>
    </div>
  );
}
