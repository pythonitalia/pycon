import { ProductAction, ProductsState, ProductState } from "./types";

export const reducer = (
  state: ProductsState,
  action: ProductAction,
): ProductsState => {
  const id = `${action.id}${action.variation || ""}`;

  const current: ProductState = state[id]
    ? state[id]
    : { id: action.id, variation: action.variation, quantity: 0 };

  switch (action.type) {
    case "increment":
      current.quantity += 1;
      break;
    case "decrement":
      current.quantity = Math.max(0, current.quantity - 1);
  }

  return { ...state, [id]: current };
};
