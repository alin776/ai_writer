interface DemoCompletionProps {
  text: string;
  progress: number;
}

export default function DemoCompletion({ text, progress }: DemoCompletionProps) {
  if (progress <= 0) return null;

  return (
    <div
      className="flex items-center gap-2 py-1 text-base font-mono text-emerald-400"
      style={{ opacity: Math.min(progress * 3, 1) }}
    >
      <span>✓</span>
      <span>{text || '任务已完成'}</span>
    </div>
  );
}
