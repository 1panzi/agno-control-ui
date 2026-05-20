import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      imports: ['vue', 'vue-router', 'pinia'],
      resolvers: [ElementPlusResolver({ importStyle: false })],
      dts: false,
    }),
    Components({
      resolvers: [ElementPlusResolver({ importStyle: false })],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  optimizeDeps: {
    include: ['element-plus', 'markdown-it', 'highlight.js'],
  },
  server: {
    host: '0.0.0.0',
    allowedHosts: true,
    port: 5173,
    hmr: false,
    proxy: {
      '/api': {
        target: 'http://localhost:8006',
        changeOrigin: true
      },
      '/agents': { target: 'http://localhost:8006', changeOrigin: true },
      '/teams': { target: 'http://localhost:8006', changeOrigin: true },
      '/workflows': { target: 'http://localhost:8006', changeOrigin: true },
      '/sessions': { target: 'http://localhost:8006', changeOrigin: true },
      '/traces': { target: 'http://localhost:8006', changeOrigin: true },
      '/trace_session_stats': { target: 'http://localhost:8006', changeOrigin: true },
      '/memories': { target: 'http://localhost:8006', changeOrigin: true },
      '/memory_topics': { target: 'http://localhost:8006', changeOrigin: true },
      '/user_memory_stats': { target: 'http://localhost:8006', changeOrigin: true },
      '/optimize-memories': { target: 'http://localhost:8006', changeOrigin: true },
      '/metrics': { target: 'http://localhost:8006', changeOrigin: true },
      '/registry': { target: 'http://localhost:8006', changeOrigin: true },
      '/components': { target: 'http://localhost:8006', changeOrigin: true },
      '/schedules': { target: 'http://localhost:8006', changeOrigin: true },
      '/approvals': { target: 'http://localhost:8006', changeOrigin: true },
      '/eval-runs': { target: 'http://localhost:8006', changeOrigin: true },
      '/knowledge': { target: 'http://localhost:8006', changeOrigin: true },
      '/databases': { target: 'http://localhost:8006', changeOrigin: true }
    }
  }
})
