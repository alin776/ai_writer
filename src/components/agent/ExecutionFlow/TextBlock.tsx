/**
 * TextBlock - AI 说明文字组件
 * 样式与 preview-execution-trace.html 一致
 */

interface TextBlockProps {
  content: string;
}

export function TextBlock({ content }: TextBlockProps) {
  return (
    <p className="text-[14px] text-slate-600 dark:text-slate-300 leading-[1.6] my-2.5">
      {content}
    </p>
  );
}
