const DEFAULT_LOCALE = "en";

const VALID_LOCALES = [DEFAULT_LOCALE, "it"];

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
