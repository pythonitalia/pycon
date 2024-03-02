import react from "@astrojs/react";
import { defineConfig } from "astro/config";

import tailwind from "@astrojs/tailwind";

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
  integrations: [react(), tailwind()],
  build: {
    format: "file",
    assetsPrefix: "/django-static/",
  },
});
