import { defineConfig } from "astro/config";
import react from "@astrojs/react";

import tailwind from "@astrojs/tailwind";
export default defineConfig({
  vite: {
    server: {
      proxy: {
        "/admin/graphql": {
          target: "http://localhost:8000",
          changeOrigin: true,
        },
      },
    },
  },
  integrations: [react(), tailwind()],
  build: {
    format: "file",
    assetsPrefix: "//django-static/",
  },
});
