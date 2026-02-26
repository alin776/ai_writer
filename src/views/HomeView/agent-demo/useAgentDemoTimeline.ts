import { useState, useEffect, useRef, useCallback } from 'react';
import type { VisibleStep } from './types';
import { timelineSteps, TOTAL_DURATION, FADE_DURATION } from './timeline-data';

type Phase = 'playing' | 'fading' | 'resetting';

export function useAgentDemoTimeline(isActive: boolean) {
  const [visibleSteps, setVisibleSteps] = useState<VisibleStep[]>([]);
  const [checkedIndices, setCheckedIndices] = useState<Map<string, Set<number>>>(new Map());
  const [phase, setPhase] = useState<Phase>('playing');

  const rafRef = useRef<number>(0);
  const startTimeRef = useRef<number>(0);
  const pausedAtRef = useRef<number>(0);

  const reset = useCallback(() => {
    setVisibleSteps([]);
    setCheckedIndices(new Map());
    setPhase('playing');
    startTimeRef.current = 0;
    pausedAtRef.current = 0;
  }, []);

  useEffect(() => {
    if (!isActive) {
      // 暂停：记录已经过时间
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = 0;
      }
      return;
    }

    const tick = (now: number) => {
      if (startTimeRef.current === 0) {
        startTimeRef.current = now - pausedAtRef.current;
      }

      const elapsed = now - startTimeRef.current;

      if (phase === 'resetting') {
        reset();
        startTimeRef.current = now;
        rafRef.current = requestAnimationFrame(tick);
        return;
      }

      if (phase === 'fading') {
        // 淡出阶段结束后重置
        if (elapsed >= TOTAL_DURATION + FADE_DURATION) {
          setPhase('resetting');
        }
        rafRef.current = requestAnimationFrame(tick);
        return;
      }

      // playing 阶段
      if (elapsed >= TOTAL_DURATION) {
        setPhase('fading');
        rafRef.current = requestAnimationFrame(tick);
        return;
      }

      // 过滤已进入的步骤
      const newVisible: VisibleStep[] = [];
      const newChecked = new Map<string, Set<number>>();

      for (const step of timelineSteps) {
        if (step.enterAt > elapsed) continue;

        const stepElapsed = elapsed - step.enterAt;
        const progress = Math.min(stepElapsed / step.duration, 1);

        if (step.type === 'todo-check') {
          const todoId = step.data.todoId as string;
          const index = step.data.index as number;
          if (!newChecked.has(todoId)) {
            newChecked.set(todoId, new Set());
          }
          newChecked.get(todoId)!.add(index);
          continue; // todo-check 不作为可见步骤渲染
        }

        newVisible.push({ step, stepElapsed, progress });
      }

      setVisibleSteps(newVisible);
      setCheckedIndices(newChecked);
      pausedAtRef.current = elapsed;

      rafRef.current = requestAnimationFrame(tick);
    };

    rafRef.current = requestAnimationFrame(tick);

    return () => {
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = 0;
      }
    };
  }, [isActive, phase, reset]);

  // 组件卸载时清理
  useEffect(() => {
    return () => {
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
      }
    };
  }, []);

  return { visibleSteps, checkedIndices, phase };
}
