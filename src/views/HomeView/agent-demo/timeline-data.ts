import type { TimelineStep } from './types';

const PROSE_TEXT =
  '\u3000\u3000清晨的薄雾笼罩着青云山脉，层叠的山峦在云海中若隐若现，宛如仙境。' +
  '一条蜿蜒的石阶从山脚延伸至云端，两侧古松苍翠，偶有仙鹤掠过长空。\n\n' +
  '\u3000\u3000林风背着简陋的包袱，仰望着那似乎永无尽头的石阶，目光中满是坚定与期待。' +
  '三年前那个风雪之夜，师父临终前的话语犹在耳畔——' +
  '"去青云宗，那里有你想要的答案。"';

export const TOTAL_DURATION = 19000; // ms
export const FADE_DURATION = 800;    // ms

export const timelineSteps: TimelineStep[] = [
  {
    id: 'user-1',
    type: 'user-bubble',
    enterAt: 0,
    duration: 1800,
    data: { text: '帮我写第一章，林风初入宗门' },
  },
  {
    id: 'agent-1',
    type: 'agent-text',
    enterAt: 2000,
    duration: 800,
    data: { text: '正在分析创作意图...' },
  },
  {
    id: 'tool-1',
    type: 'tool-line',
    enterAt: 3000,
    duration: 800,
    data: { tool: 'Explore', args: '第一章相关设定' },
  },
  {
    id: 'tool-2',
    type: 'tool-line',
    enterAt: 4000,
    duration: 800,
    data: { tool: 'Read', args: 'chapters/00-序章.md' },
  },
  {
    id: 'todo-1',
    type: 'todo-block',
    enterAt: 5000,
    duration: 500,
    data: {
      header: 'Planning',
      items: ['分析序章人物关系', '构建第一章场景大纲', '创作正文内容'],
    },
  },
  {
    id: 'check-0',
    type: 'todo-check',
    enterAt: 6000,
    duration: 400,
    data: { todoId: 'todo-1', index: 0 },
  },
  {
    id: 'check-1',
    type: 'todo-check',
    enterAt: 6500,
    duration: 400,
    data: { todoId: 'todo-1', index: 1 },
  },
  {
    id: 'check-2',
    type: 'todo-check',
    enterAt: 7500,
    duration: 400,
    data: { todoId: 'todo-1', index: 2 },
  },
  {
    id: 'tool-3',
    type: 'tool-line',
    enterAt: 8000,
    duration: 800,
    data: { tool: 'SmartCreate', args: '生成第一章' },
  },
  {
    id: 'output-1',
    type: 'output-card',
    enterAt: 9000,
    duration: 600,
    data: { intro: '为您创作第一章内容：', title: '第一章：踏入仙门' },
  },
  {
    id: 'prose-1',
    type: 'prose-stream',
    enterAt: 10000,
    duration: 6000,
    data: { text: PROSE_TEXT, outputId: 'output-1' },
  },
  {
    id: 'revision-1',
    type: 'revision-card',
    enterAt: 16500,
    duration: 600,
    data: { filename: 'chapters/01-踏入仙门.md', additions: 86 },
  },
  {
    id: 'revision-accept-1',
    type: 'revision-accept',
    enterAt: 17500,
    duration: 400,
    data: { revisionId: 'revision-1' },
  },
  {
    id: 'completion-1',
    type: 'completion',
    enterAt: 18000,
    duration: 600,
    data: { text: '任务已完成' },
  },
];
