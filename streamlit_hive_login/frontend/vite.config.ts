import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import inject from "@rollup/plugin-inject";
import rollupNodePolyFill from "rollup-plugin-node-polyfills";
import type { Plugin } from "vite";  
export default defineConfig({
  base: "./",
  plugins: [react()],
  resolve: {
    alias: {
      buffer: "buffer",
      process: "process/browser",
    },
  },
  define: {
    global: "globalThis",
  },
  optimizeDeps: {
    include: ["buffer", "process"],
  },
  build: {
    outDir: '../frontend/build',
    emptyOutDir: true,
    rollupOptions: {
      plugins: [
        inject({
          Buffer: ["buffer", "Buffer"],
          process: "process",
        }) as unknown as Plugin,               
        rollupNodePolyFill() as unknown as Plugin,
      ],
    },
  },
});
