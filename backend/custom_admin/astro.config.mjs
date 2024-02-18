import { defineConfig } from "astro/config";
import react from "@astrojs/react";

import tailwind from "@astrojs/tailwind";
// Sec-Websocket-Accept:
// AW3KkaseWbPOHdkJmRJokz0C60Y=
// Sec-Websocket-Protocol:
// vite-hmr

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
