const MESSAGES_KEY = "messages";

type Message = {
  message: string;
  type: "alert" | "success";
};

const getMessages: () => Message[] = () => {
  const value =
    typeof window === "undefined"
      ? null
      : window.sessionStorage.getItem(MESSAGES_KEY);

  if (!value) {
    return [];
  }

  try {
    return JSON.parse(value);
  } catch {
    return [];
  }
};

export const useMessages: () => [
  Message[],
  (message: Message) => void,
  () => void,
] = () => {
  const messages = getMessages();

  const addMessage = ({ message, type }: Message) => {
    const previousMessages = getMessages();

    window.sessionStorage.setItem(
      MESSAGES_KEY,
      JSON.stringify([
        ...previousMessages,
        {
          message,
          type,
        },
      ]),
    );
  };

  const clearMessages = () => window.sessionStorage.removeItem(MESSAGES_KEY);

  return [messages, addMessage, clearMessages];
};
