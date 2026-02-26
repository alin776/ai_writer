import { useRef, useEffect } from 'react';
import type { VisibleStep } from './types';
import DemoUserBubble from './demo-components/DemoUserBubble';
import DemoTextStream from './demo-components/DemoTextStream';
import DemoToolLine from './demo-components/DemoToolLine';
import DemoTodoBlock from './demo-components/DemoTodoBlock';
import DemoOutputCard from './demo-components/DemoOutputCard';
import DemoRevisionCard from './demo-components/DemoRevisionCard';
import DemoCompletion from './demo-components/DemoCompletion';
import styles from '../VibingHomePage.module.css';

interface AgentDemoPlayerProps {
  visibleSteps: VisibleStep[];
  checkedIndices: Map<string, Set<number>>;
}

export default function AgentDemoPlayer({ visibleSteps, checkedIndices }: AgentDemoPlayerProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // 自动滚动到底部
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [visibleSteps]);

  // 查找 prose-stream 步骤（用于注入到 OutputCard）
  const proseStep = visibleSteps.find(v => v.step.type === 'prose-stream');
  // 查找 revision-accept 步骤
  const acceptedRevisions = new Set(
    visibleSteps
      .filter(v => v.step.type === 'revision-accept')
      .map(v => v.step.data.revisionId as string)
  );

  return (
    <div ref={scrollRef} className="max-h-[60vh] overflow-y-auto space-y-1 px-4 py-3 custom-scrollbar" style={{ scrollbarGutter: 'stable' }}>
      {visibleSteps.map((vs) => {
        const { step, progress } = vs;
        const key = step.id;

        switch (step.type) {
          case 'user-bubble':
            return (
              <div key={key} className={styles.stepFadeIn}>
                <DemoUserBubble text={step.data.text as string} progress={progress} />
              </div>
            );

          case 'agent-text':
            return (
              <div key={key} className={styles.stepFadeIn}>
                <DemoTextStream text={step.data.text as string} progress={progress} />
              </div>
            );

          case 'tool-line':
            return (
              <div key={key} className={styles.stepFadeInFast}>
                <DemoToolLine
                  tool={step.data.tool as string}
                  args={step.data.args as string}
                  progress={progress}
                />
              </div>
            );

          case 'todo-block':
            return (
              <div key={key} className={styles.stepFadeInFast}>
                <DemoTodoBlock
                  header={step.data.header as string}
                  items={step.data.items as string[]}
                  checkedIndices={checkedIndices.get(step.id) ?? new Set()}
                  progress={progress}
                />
              </div>
            );

          case 'output-card': {
            const linkedProse = proseStep && proseStep.step.data.outputId === step.id
              ? proseStep
              : undefined;
            return (
              <div key={key} className={styles.stepFadeIn}>
                <DemoOutputCard
                  intro={step.data.intro as string}
                  title={step.data.title as string}
                  proseText={linkedProse ? linkedProse.step.data.text as string : undefined}
                  proseProgress={linkedProse ? linkedProse.progress : 0}
                  progress={progress}
                />
              </div>
            );
          }

          case 'revision-card':
            return (
              <div key={key} className={styles.stepFadeIn}>
                <DemoRevisionCard
                  filename={step.data.filename as string}
                  additions={step.data.additions as number}
                  accepted={acceptedRevisions.has(step.id)}
                />
              </div>
            );

          case 'completion':
            return (
              <div key={key}>
                <DemoCompletion
                  text={step.data.text as string}
                  progress={progress}
                />
              </div>
            );

          // prose-stream 和 revision-accept / todo-check 不直接渲染
          default:
            return null;
        }
      })}
    </div>
  );
}
