import { createInertiaApp } from "@inertiajs/react";
import { createRoot } from "react-dom/client";

import Dashboard from "./pages/Dashboard";

const pages = { Dashboard };

createInertiaApp({
  resolve: (name) => {
    const page = pages[name as keyof typeof pages];

    if (!page) {
      throw new Error(`Page component "${name}" not found`);
    }

    return page;
  },
  setup({ el, App, props }) {
    createRoot(el).render(<App {...props} />);
  },
});
