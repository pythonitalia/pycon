import React, { useContext, useMemo } from "react";

import cookies from "next-cookies";
import { useRouter } from "next/router";

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

export const LocaleProvider = ({
  children,
}: React.PropsWithChildren<{ lang: string }>) => {
  const language = useCurrentLanguage();

  React.useEffect(() => {
    const { pyconLocale } = cookies({
      req: { headers: { cookie: document.cookie } },
    });
    if (language !== pyconLocale) {
      document.cookie = `pyconLocale=${language}; path=/`;
    }
  }, [language]);

  const links = useMemo(() => {
    // language
    return {
      en: "/en/abc",
      it: "/it/abc",
    };
  }, [language]);

  return (
    <AlternateLinksContext.Provider value={links}>
      {children}
    </AlternateLinksContext.Provider>
  );
};

export const useCurrentLanguage = () => {
  const { locale } = useRouter();

  return locale as Language;
};
