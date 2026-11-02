import react from "@astrojs/react";
import { defineConfig } from "astro/config";

export default defineConfig({
  vite: {
    logLevel: "info",
    server: {
      strictPort: true,
      port: 3002,
      hmr: {
        clientPort: 3003,
      },
    },
  },
  integrations: [react()],
  build: {
    format: "file",
    assetsPrefix: "/django-static/",
  },
  compressHTML: true,
  devToolbar: {
    enabled: false,
  },
});
