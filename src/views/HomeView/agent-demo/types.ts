export type DemoStepType =
  | 'user-bubble'
  | 'agent-text'
  | 'tool-line'
  | 'todo-block'
  | 'todo-check'
  | 'output-card'
  | 'prose-stream'
  | 'revision-card'
  | 'revision-accept'
  | 'completion';

export interface TimelineStep {
  id: string;
  type: DemoStepType;
  enterAt: number;   // ms
  duration: number;  // ms
  data: Record<string, unknown>;
}

export interface VisibleStep {
  step: TimelineStep;
  stepElapsed: number; // 该步已经过的时间(ms)
  progress: number;    // 0-1 clamp
}
