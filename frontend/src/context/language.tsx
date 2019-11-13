import React, { useContext } from "react";

export const LanguageContext = React.createContext("en");

export const useCurrentLanguage = () => useContext(LanguageContext);
