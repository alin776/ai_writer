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
    watch: {
      ignored: ['**/backend/**', '**/opencode/**', '**/node_modules/**', '**/.git/**'],
    },
    proxy: {
      // WebSocket 代理需要单独配置
      '/api/v1/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        changeOrigin: true,
      },
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
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
