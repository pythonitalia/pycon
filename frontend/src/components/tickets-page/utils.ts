import { OrderState } from "./types";

export const hasSelectedAtLeastOneProduct = (state: OrderState) =>
  Object.values(state.selectedProducts).length > 0 ||
  Object.values(state.selectedHotelRooms).length > 0;
