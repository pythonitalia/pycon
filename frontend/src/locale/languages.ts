export const DEFAULT_LOCALE = "en" as const;
export const VALID_LOCALES = [DEFAULT_LOCALE] as const;

export type Language = (typeof VALID_LOCALES)[number];
