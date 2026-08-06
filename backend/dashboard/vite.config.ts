import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [tailwindcss(), react()],
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
    port: 5173,
    strictPort: true,
  },
});
