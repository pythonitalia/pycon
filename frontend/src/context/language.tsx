import React, { useContext } from "react";

export const LanguageContext = React.createContext<"en" | "it">("en");
export const AlternateLinksContext = React.createContext({
  it: "/it",
  en: "/en",
});

export const useCurrentLanguage = () => useContext(LanguageContext);
export const useAlternateLinks = () => useContext(AlternateLinksContext);
