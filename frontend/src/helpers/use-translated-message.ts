import { messages } from "../locale";

export const useTranslatedMessage = (id: keyof typeof messages) =>
  getTranslatedMessage(id);

export const getTranslatedMessage = (id: keyof typeof messages): string => {
  const message = messages[id];

  if (!message) {
    console.warn(`Message with ${id} not found`);
  }

  return message;
};
