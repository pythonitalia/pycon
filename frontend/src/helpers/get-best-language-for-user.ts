import { DEFAULT_LOCALE, VALID_LOCALES } from "~/locale/get-initial-locale";

export const getBestLanguageForUser = (
  acceptLanguage: string,
): typeof VALID_LOCALES[number] => {
  const sections = acceptLanguage
    .split(",")
    .map((l) => {
      const qualifier = l.split(";");
      return qualifier ? qualifier[0].trim() : l.trim();
    })
    .map((language) => VALID_LOCALES.find((l) => language.indexOf(l) !== -1))
    .filter((l) => l);

  return sections.length > 0 ? sections[0] : DEFAULT_LOCALE;
};
