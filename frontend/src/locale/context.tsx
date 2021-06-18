import React, { useContext } from "react";

import { Language } from "./get-initial-locale";

interface ContextProps {
  readonly locale: string;
  // readonly setLocale: (locale: string) => void;
}

export const AlternateLinksContext = React.createContext({
  it: "/it",
  en: "/en",
});

export const useAlternateLinks = () => useContext(AlternateLinksContext);

export const LocaleContext = React.createContext<ContextProps>({
  locale: "en",
  // setLocale: () => null,
});

export const LocaleProvider: React.FC<{ lang: string }> = ({
  lang,
  children,
}) => {
  React.useEffect(() => {
    if (lang !== localStorage.getItem("locale")) {
      localStorage.setItem("locale", lang);
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
