import type { TicketItem } from "~/types";

import type { OrderState, Voucher } from "../types";

export const calculateProductPrice = (
  product: TicketItem,
  voucher?: Voucher | null,
): number => {
  const basePrice = Number.parseFloat(product.defaultPrice);

  if (voucher) {
    const priceMode = voucher.priceMode;
    const value = Number.parseFloat(voucher.value);

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
): number => {
  const ticketsPrice = Object.values(state.selectedProducts)
    .flat()
    .reduce(
      (sum, ticketInfo) =>
        sum +
        calculateProductPrice(productsById[ticketInfo.id], ticketInfo.voucher),
      0,
    );

  return ticketsPrice;
};

export const calculateSavedAmount = (
  state: OrderState,
  productsById: Record<number, TicketItem>,
): number => {
  const ticketsPrice = Object.values(state.selectedProducts)
    .flat()
    .filter((ticketInfo) => !!ticketInfo.voucher)
    .reduce(
      (sum, ticketInfo) =>
        sum +
        (calculateProductPrice(productsById[ticketInfo.id]) -
          calculateProductPrice(
            productsById[ticketInfo.id],
            ticketInfo.voucher,
          )),
      0,
    );

  return ticketsPrice;
};
