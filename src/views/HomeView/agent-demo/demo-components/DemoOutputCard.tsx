import { useMemo } from 'react';
import styles from '../../VibingHomePage.module.css';

interface DemoOutputCardProps {
  intro: string;
  title: string;
  proseText?: string;
  proseProgress?: number; // 0-1, 由 prose-stream 步骤驱动
  progress: number;       // output-card 自身的进场 progress
}

export default function DemoOutputCard({
  intro,
  title,
  proseText,
  proseProgress = 0,
}: DemoOutputCardProps) {
  const visibleProse = useMemo(() => {
    if (!proseText || proseProgress <= 0) return '';
    if (proseProgress >= 1) return proseText;
    const chars = [...proseText];
    const count = Math.floor(chars.length * proseProgress);
    return chars.slice(0, count).join('');
  }, [proseText, proseProgress]);

  const isStreaming = proseText && proseProgress > 0 && proseProgress < 1;

  return (
    <div>
      <div className="text-[14px] text-[#ccc] mb-3 leading-[1.7]">
        {intro}
      </div>
      <h3 className="text-[15px] font-bold text-slate-200 mb-2">{title}</h3>
      {visibleProse && (
        <div className="text-[14px] text-slate-300 leading-[1.8] [&_p]:mb-2.5 [&_p]:indent-8">
          {visibleProse.split('\n\n').map((para, i) => (
            <p key={i}>{para}</p>
          ))}
          {isStreaming && (
            <span className={`ml-0.5 text-amber-400 ${styles.cursorBlink}`}>▍</span>
          )}
        </div>
      )}
    </div>
  );
}
