import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './', // crucial for Streamlit component
  build: {
    outDir: '../frontend/build',
    emptyOutDir: true
  }
})