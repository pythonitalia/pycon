const ERROR_TYPES = ["WrongEmailOrPassword"];

export const getMessageForError = (error: string) => {
  switch (error) {
    case "WrongEmailOrPassword":
      return "Your email or password are incorrect";
    default:
      return "Something went wrong! Please try again";
  }
};

export const isErrorTypename = (error: string) => ERROR_TYPES.includes(error);
