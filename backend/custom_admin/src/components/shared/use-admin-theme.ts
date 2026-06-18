import { useEffect, useState } from "react";

type Resolved = "light" | "dark";

/**
 * Resolves the appearance the Django admin is currently using.
 *
 * The admin's theme switch persists the preference in localStorage under the
 * "theme" key ("auto" | "light" | "dark"); "auto" follows the OS preference.
 * Custom admin pages are served from the same origin, so we can read it
 * directly and pass the result as the Radix `appearance`.
 */
const resolveAdminTheme = (): Resolved => {
  if (typeof window === "undefined") {
    return "light";
  }

  let stored: string | null = null;
  try {
    stored = window.localStorage.getItem("theme");
  } catch {
    stored = null;
  }

  if (stored === "dark") {
    return "dark";
  }
  if (stored === "light") {
    return "light";
  }

  // "auto" or unset: follow the operating system preference.
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
};

export const useAdminTheme = (): Resolved => {
  const [theme, setTheme] = useState<Resolved>(resolveAdminTheme);

  useEffect(() => {
    const update = () => setTheme(resolveAdminTheme());

    const media = window.matchMedia("(prefers-color-scheme: dark)");
    media.addEventListener("change", update);
    // Fires when the admin theme is toggled in another tab/window.
    window.addEventListener("storage", update);

    return () => {
      media.removeEventListener("change", update);
      window.removeEventListener("storage", update);
    };
  }, []);

  return theme;
};
