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

  const current: ProductState = state.selectedProducts[id]
    ? state.selectedProducts[id]
    : { id: action.id, variation: action.variation, quantity: 0 };

  switch (action.type) {
    case "incrementProduct":
      current.quantity += 1;
      break;
    case "decrementProduct":
      current.quantity = Math.max(0, current.quantity - 1);
  }

  return {
    ...state,
    selectedProducts: { ...state.selectedProducts, [id]: current },
  };
};

export const reducer = (state: OrderState, action: OrderAction): OrderState => {
  switch (action.type) {
    case "incrementProduct":
    case "decrementProduct":
      return updateProductReducer(state, action);
    case "updateInvoiceInformation":
      return {
        ...state,
        invoiceInformation: action.data,
      };
  }
};
