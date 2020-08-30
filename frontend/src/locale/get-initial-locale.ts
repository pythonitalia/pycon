export const DEFAULT_LOCALE = "en" as const;
export const VALID_LOCALES = [DEFAULT_LOCALE, "it"] as const;

export type Language = typeof VALID_LOCALES[number];

// VALID_LOCALES is a ReadonlyArray, so includes wants only "en" or "it"
// but we want to check if any locale (string) is included in the list of not
// @ts-ignore
export const isLocale = (locale: string) => VALID_LOCALES.includes(locale);

export function getInitialLocale(): string {
  // preference from the previous session
  const localSetting = localStorage.getItem("locale");

  if (localSetting && isLocale(localSetting)) {
    return localSetting;
  }

  // the language setting of the browser
  const [browserSetting] = navigator.language.split("-");

  if (isLocale(browserSetting)) {
    return browserSetting;
  }

  return DEFAULT_LOCALE;
}
