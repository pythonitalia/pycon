import { InvoiceInformationState, OrderState } from "./types";

export const hasSelectedAtLeastOneProduct = (state: OrderState) =>
  Object.values(state.selectedProducts).length > 0 ||
  Object.values(state.selectedHotelRooms).length > 0;

type InvoiceInformationKeys = (keyof InvoiceInformationState)[];

export const hasOrderInformation = (state: OrderState) => {
  const requiredKeys: InvoiceInformationKeys = [
    "name",
    "address",
    "zipCode",
    "city",
    "country",
  ];

  if (state.invoiceInformation.isBusiness) {
    requiredKeys.push("companyName");
    requiredKeys.push("vatId");
  } else if (
    !state.invoiceInformation.isBusiness &&
    state.invoiceInformation.country === "IT"
  ) {
    requiredKeys.push("fiscalCode");
  }

  if (requiredKeys.some(k => state.invoiceInformation[k] === "")) {
    return false;
  }

  return true;
};

export const hasAnsweredTicketsQuestions = (
  state: OrderState,
  tickets: { id: string; questions: { id: string; required: boolean }[] }[],
) => {
  const selectedProducts = Object.values(state.selectedProducts).flat();

  if (
    selectedProducts.some(product => {
      const ticket = tickets.find(t => t.id === product.id);

      if (!ticket) {
        return true;
      }

      if (ticket.questions.length === 0) {
        return false;
      }

      if (!product.attendeeEmail || !product.attendeeName) {
        return true;
      }

      const answers = product.answers;

      for (const question of ticket.questions) {
        if (
          question.required &&
          (!answers.hasOwnProperty(question.id) || answers[question.id] === "")
        ) {
          return true;
        }
      }

      return false;
    })
  ) {
    return false;
  }

  return true;
};
