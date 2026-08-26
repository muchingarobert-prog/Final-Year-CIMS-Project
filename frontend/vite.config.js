import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: process.env.VITE_DEV_API_PROXY
      ? { '/api': process.env.VITE_DEV_API_PROXY }
      : undefined,
  }
});
