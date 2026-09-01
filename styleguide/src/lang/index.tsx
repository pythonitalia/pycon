import { messages as italianMessages } from "./it";

export const getMessagesForLocale = (locale: string) => {
  if (locale === "it") {
    return italianMessages;
  }

  return {};
};
