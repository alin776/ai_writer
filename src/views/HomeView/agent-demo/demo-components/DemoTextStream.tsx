import { useMemo } from 'react';
import styles from '../../VibingHomePage.module.css';

interface DemoTextStreamProps {
  text: string;
  progress: number; // 0-1
}

export default function DemoTextStream({ text, progress }: DemoTextStreamProps) {
  const displayText = useMemo(() => {
    if (progress >= 1) return text;
    const chars = [...text];
    const count = Math.floor(chars.length * progress);
    return chars.slice(0, count).join('');
  }, [text, progress]);

  return (
    <div className="text-[14px] text-gray-400 leading-relaxed font-mono">
      <span className={progress < 1 ? styles.shimmerText : ''}>{displayText}</span>
      {progress < 1 && (
        <span className={`ml-0.5 ${styles.cursorBlink}`}>▍</span>
      )}
    </div>
  );
}
