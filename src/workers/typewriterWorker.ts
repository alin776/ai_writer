// 打字机效果 Web Worker
// 用于在后台标签页时保持定时器不被节流

let timerId: ReturnType<typeof setInterval> | null = null;

self.onmessage = (e: MessageEvent) => {
  const { type, speed } = e.data;

  if (type === 'start') {
    if (timerId !== null) return; // 已经在运行
    timerId = setInterval(() => {
      self.postMessage({ type: 'tick' });
    }, speed || 10);
  } else if (type === 'stop') {
    if (timerId !== null) {
      clearInterval(timerId);
      timerId = null;
    }
  }
};
