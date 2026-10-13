import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import fs from 'fs';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },

  server: {
    host: 'localhost',
    port: 5173,
    https: (() => {
      const keyPath = fs.existsSync(path.resolve(__dirname, '../certs/key.pem'))
        ? path.resolve(__dirname, '../certs/key.pem')
        : path.resolve(__dirname, '../certs/localhost.key');
      const certPath = fs.existsSync(path.resolve(__dirname, '../certs/cert.pem'))
        ? path.resolve(__dirname, '../certs/cert.pem')
        : path.resolve(__dirname, '../certs/localhost.crt');
      if (fs.existsSync(keyPath) && fs.existsSync(certPath)) {
        return {
          key: fs.readFileSync(keyPath),
          cert: fs.readFileSync(certPath)
        };
      }
      return false;
    })()
  },
})