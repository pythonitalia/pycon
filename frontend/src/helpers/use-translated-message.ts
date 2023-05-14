import { Language } from "~/locale/languages";

import { messages } from "../locale";

// import { useCurrentLanguage } from "../locale/context";

export const useTranslatedMessage = (id: keyof (typeof messages)["en"]) => {
  // const language = useCurrentLanguage();
  const language = "en";
  return getTranslatedMessage(id, language);
};

export const getTranslatedMessage = (
  id: keyof (typeof messages)["en"],
  language: Language,
) => {
  const message = messages[language][id];

  if (!message) {
    console.warn(`Message with ${id} not found for language ${language}`);
  }

  return message;
};
