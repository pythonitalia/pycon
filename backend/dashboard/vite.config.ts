import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [tailwindcss(), react()],
  resolve: {
    alias: {
      "@": new URL("./src", import.meta.url).pathname,
    },
  },
  build: {
    emptyOutDir: true,
    manifest: true,
    outDir: "../assets/build",
    rollupOptions: {
      input: "src/app.tsx",
    },
  },
  server: {
    host: "0.0.0.0",
    origin: "http://localhost:5173",
    port: 5173,
    strictPort: true,
  },
});
