import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [svelte()],
  build: { target: 'es2022', assetsInlineLimit: 0 },
  server: { port: 5180, proxy: { '/api': 'http://127.0.0.1:8821' } },
})
