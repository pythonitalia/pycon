import {
  OrderAction,
  OrderState,
  ProductState,
  UpdateProductAction,
} from "./types";

const updateProductReducer = (
  state: OrderState,
  action: UpdateProductAction,
): OrderState => {
  const id = `${action.id}${action.variation || ""}`;
  const productItems = state.selectedProducts[id]
    ? [...state.selectedProducts[id]]
    : [];

  switch (action.type) {
    case "incrementProduct":
      productItems.push({
        id: action.id,
        variation: action.variation,
        answers: {},
        attendeeName: "",
        attendeeEmail: "",
      });
      break;
    case "decrementProduct":
      if (productItems.length > 0) {
        productItems.splice(0, 1);
      }
      break;
  }

  return {
    ...state,
    selectedProducts: {
      ...state.selectedProducts,
      [id]: productItems,
    },
  };
};

export const reducer = (state: OrderState, action: OrderAction): OrderState => {
  switch (action.type) {
    case "incrementProduct":
    case "decrementProduct":
      return updateProductReducer(state, action);
    case "updateTicketAnswer": {
      const products = state.selectedProducts[action.id];
      const newProduct = {
        ...products[action.index],
        answers: {
          ...products[action.index].answers,
          [action.question]: action.answer,
        },
      };

      products[action.index] = newProduct;

      return {
        ...state,
        selectedProducts: {
          ...state.selectedProducts,
          [action.id]: products,
        },
      };
    }
    case "updateTicketInfo": {
      const products = state.selectedProducts[action.id];
      const newProduct = {
        ...products[action.index],
        [action.key]: action.value,
      };

      products[action.index] = newProduct;

      return {
        ...state,
        selectedProducts: {
          ...state.selectedProducts,
          [action.id]: products,
        },
      };
    }
    case "updateInvoiceInformation":
      return {
        ...state,
        invoiceInformation: action.data,
      };
  }
};
