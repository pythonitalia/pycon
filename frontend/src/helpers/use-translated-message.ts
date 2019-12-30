import { useCurrentLanguage } from "../context/language";
import { messages } from "../locale";

export const useTranslatedMessage = (id: keyof typeof messages["en"]) => {
  const language = useCurrentLanguage();

  const message = messages[language][id];

  if (!message) {
    console.warn(`Message with ${id} not found for language ${language}`);
  }

  return message;
};
