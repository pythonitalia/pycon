import React from "react";

import { DEFAULT_LOCALE, type Language } from "~/locale/languages";

export const LocaleProvider = ({
  children,
}: React.PropsWithChildren<{ lang: string }>) => {
  return <>{children}</>;
};

export const useCurrentLanguage = (): Language => {
  return DEFAULT_LOCALE;
};
