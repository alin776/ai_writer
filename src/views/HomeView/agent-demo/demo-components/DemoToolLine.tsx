interface DemoToolLineProps {
  tool: string;
  args: string;
  progress: number; // 0-1
}

export default function DemoToolLine({ tool, args, progress }: DemoToolLineProps) {
  const isRunning = progress < 1;

  return (
    <div className="flex items-center gap-2 py-0.5 text-base font-mono">
      <span
        className={`inline-block w-2 h-2 rounded-full flex-shrink-0 ${
          isRunning ? 'bg-emerald-500 animate-pulse' : 'bg-gray-400 dark:bg-gray-500'
        }`}
      />
      <span className="text-gray-500 dark:text-gray-400 truncate">
        {tool}({JSON.stringify(args)})
      </span>
    </div>
  );
}
