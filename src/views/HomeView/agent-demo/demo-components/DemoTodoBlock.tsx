import styles from '../../VibingHomePage.module.css';

interface DemoTodoBlockProps {
  header: string;
  items: string[];
  checkedIndices: Set<number>;
  progress: number; // 0-1
}

export default function DemoTodoBlock({ header, items, checkedIndices, progress }: DemoTodoBlockProps) {
  const allDone = checkedIndices.size === items.length;

  return (
    <div className="py-1">
      {/* 标题行 — 复刻 TodoBlock.tsx */}
      <div className="flex items-center gap-2 text-base font-mono">
        <span
          className={`inline-block w-2 h-2 rounded-full flex-shrink-0 ${
            allDone ? 'bg-gray-400 dark:bg-gray-500' : 'bg-emerald-500 animate-pulse'
          }`}
        />
        <span className="text-gray-500 dark:text-gray-400">{header}</span>
      </div>

      {/* 子项清单 */}
      {progress > 0 && (
        <div className="ml-4 mt-1 space-y-0.5">
          {items.map((item, idx) => {
            const isChecked = checkedIndices.has(idx);
            return (
              <div key={idx} className="flex items-start gap-2 text-base font-mono">
                <span className="flex-shrink-0 w-4 text-center">
                  {isChecked ? (
                    <span className={styles.checkPop}>✅</span>
                  ) : (
                    '☐'
                  )}
                </span>
                <span
                  className={
                    isChecked
                      ? 'text-gray-400 dark:text-gray-500 line-through'
                      : 'text-gray-600 dark:text-gray-300'
                  }
                >
                  {item}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
