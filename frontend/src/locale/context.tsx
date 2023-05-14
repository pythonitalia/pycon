import React from "react";

import cookies from "next-cookies";

// import { useRouter } from "next/navigation";
import { Language } from "~/locale/languages";

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

  return <>{children}</>;
};

export const useCurrentLanguage = () => {
  // const { locale } = useRouter();
  // return locale as Language;
  return "en";
};
