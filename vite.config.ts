import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    open: true,
  },
  build: {
    // 提高块体积警告阈值，避免开发阶段误报
    chunkSizeWarningLimit: 2000,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('/components/agent/')) return 'agent';
          if (id.includes('/components/worldview/')) return 'worldview';
          if (id.includes('/components/editor/NovelEditor')) return 'editor';
          return undefined;
        },
      },
    },
  },
})
