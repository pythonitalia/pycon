const ERROR_TYPES = [
  "EmailAlreadyUsed",
  "RegisterValidationError",
  "WrongEmailOrPassword",
];

export const getMessageForError = (error: string) => {
  switch (error) {
    case "WrongEmailOrPassword":
      return "La tua email o password non sono corretti";
    case "RegisterValidationError":
      return "Email o password non validi";
    case "EmailAlreadyUsed":
      return "L'indirizzo email è già stato registrato";
    default:
      return "Qualcosa è andato storto, prova di nuovo";
  }
};

export const isErrorTypename = (error: string) => ERROR_TYPES.includes(error);
