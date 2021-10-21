import React, { useContext } from "react";

import cookies from "next-cookies";

import { Language } from "~/locale/languages";

interface ContextProps {
  readonly locale: string;
}

export const AlternateLinksContext = React.createContext({
  it: "/it",
  en: "/en",
});

export const useAlternateLinks = () => useContext(AlternateLinksContext);

export const LocaleContext = React.createContext<ContextProps>({
  locale: "en",
});

export const LocaleProvider: React.FC<{ lang: string }> = ({
  lang,
  children,
}) => {
  React.useEffect(() => {
    const { pyconLocale } = cookies({
      req: { headers: { cookie: document.cookie } },
    });
    if (lang !== pyconLocale) {
      document.cookie = `pyconLocale=${lang}; path=/`;
    }
  }, [lang]);

  return (
    <LocaleContext.Provider value={{ locale: lang }}>
      {children}
    </LocaleContext.Provider>
  );
};

export const useCurrentLanguage = () => {
  const { locale } = useContext(LocaleContext);

  return locale as Language;
};
