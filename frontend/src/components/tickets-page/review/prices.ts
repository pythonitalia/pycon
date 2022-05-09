import { HotelRoom, OrderState, Voucher } from "../types";
import { TicketItem } from "~/types";

export const calculateProductPrice = (
  product: TicketItem,
  voucher?: Voucher | null,
): number => {
  const basePrice = parseFloat(product.defaultPrice);

  if (voucher) {
    const priceMode = voucher.priceMode;
    const value = parseFloat(voucher.value);

    switch (priceMode) {
      case "none": {
        return basePrice;
      }
      case "set": {
        return value;
      }
      case "subtract": {
        return basePrice - value;
      }
      case "percent": {
        const percentage = value / 100;
        return basePrice - basePrice * percentage;
      }
    }
  }

  return basePrice;
};

export const calculateTotalAmount = (
  state: OrderState,
  productsById: {
    [x: string]: TicketItem;
    [x: number]: TicketItem;
  },
  hotelRoomsById: {
    [x: string]: HotelRoom;
    [x: number]: HotelRoom;
  },
): number => {
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
