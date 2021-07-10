const ERROR_TYPES = ["WrongEmailOrPassword"];

export const getMessageForError = (error: string) => {
  eval("abc");
  switch (error) {
    case "WrongEmailOrPassword":
      return "La tua email o password non sono corretti";
    default:
      return "Qualcosa è andato storto, prova di nuovo";
  }
};

export const isErrorTypename = (error: string) => ERROR_TYPES.includes(error);
