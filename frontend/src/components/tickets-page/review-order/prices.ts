import { HotelRoom, Voucher } from "../../../generated/graphql-backend";
import { Ticket } from "../../tickets-form/types";
import { OrderState } from "../types";

export const calculateProductPrice = (
  product: Ticket,
  voucher?: Voucher | null,
) => {
  const basePrice = parseFloat(product.defaultPrice);

  if (voucher) {
    const priceMode = voucher.priceMode;
    const value = parseFloat(voucher.value);

    switch (priceMode) {
      case "none":
        return basePrice;
      case "set":
        return value;
      case "subtract":
        return basePrice - value;
      case "percent":
        const percentage = value / 100;
        return basePrice - basePrice * percentage;
    }
  }

  return basePrice;
};

export const calculateTotalAmount = (
  state: OrderState,
  productsById: {
    [x: string]: Ticket;
    [x: number]: Ticket;
  },
  hotelRoomsById: {
    [x: string]: HotelRoom;
    [x: number]: HotelRoom;
  },
) => {
  const ticketsPrice = Object.values(state.selectedProducts)
    .flat()
    .reduce(
      (sum, ticketInfo) =>
        sum +
        calculateProductPrice(productsById[ticketInfo.id], ticketInfo.voucher),
      0,
    );

  const hotelRoomsPrice = Object.values(state.selectedHotelRooms)
    .flat()
    .reduce(
      (sum, roomInfo) =>
        sum +
        parseFloat(hotelRoomsById[roomInfo.id].price) * roomInfo.numNights,
      0,
    );

  return ticketsPrice + hotelRoomsPrice;
};
