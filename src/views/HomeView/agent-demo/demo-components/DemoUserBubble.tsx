import { useMemo } from 'react';
import styles from '../../VibingHomePage.module.css';

interface DemoUserBubbleProps {
  text: string;
  progress: number; // 0-1
}

export default function DemoUserBubble({ text, progress }: DemoUserBubbleProps) {
  const displayText = useMemo(() => {
    if (progress >= 1) return text;
    const chars = [...text];
    const total = chars.length;
    let visibleCount = 0;
    let elapsed = 0;
    const perChar = 1 / total;

    for (let i = 0; i < total; i++) {
      if (elapsed > progress) break;
      const char = chars[i];
      // 逗号和句号暂停更久（约 200ms / 总时长）
      const isPause = char === '，' || char === '。' || char === '、';
      elapsed += isPause ? perChar * 3.3 : perChar;
      visibleCount++;
    }
    return chars.slice(0, visibleCount).join('');
  }, [text, progress]);

  return (
    <div className="flex justify-end">
      <div className="max-w-[80%] backdrop-blur-md border border-white/[0.1] text-white px-3 py-2 rounded-xl rounded-tr-sm text-[14px] leading-relaxed"
        style={{ background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.04) 100%)' }}
      >
        {displayText}
        {progress < 1 && (
          <span className={`ml-0.5 ${styles.cursorBlink}`}>|</span>
        )}
      </div>
    </div>
  );
}
