export const DEFAULT_LOCALE = "en" as const;
export const VALID_LOCALES = [DEFAULT_LOCALE, "it"] as const;

export type Language = typeof VALID_LOCALES[number];
