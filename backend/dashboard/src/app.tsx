import { createInertiaApp } from "@inertiajs/react";
import { createRoot } from "react-dom/client";

import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import "./styles.css";

const pages = { Dashboard, Login };

createInertiaApp({
  title: (title) => (title ? `${title} · Dashboard` : "Dashboard"),
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
