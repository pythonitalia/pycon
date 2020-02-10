import {
  OrderAction,
  OrderState,
  UpdateHotelRoomAction,
  UpdateProductAction,
} from "./types";
import { Voucher } from "../../generated/graphql-backend";

const updateProductReducer = (
  state: OrderState,
  action: UpdateProductAction,
): OrderState => {
  // const id = `${action.id}${action.variation || ""}`;
  const id = action.id;
  const selectedProducts = { ...state.selectedProducts };
  const productItems = selectedProducts[id] ? [...selectedProducts[id]] : [];

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
      let indexToRemove = 0;

      if (action.variation) {
        indexToRemove = productItems.findIndex(
          product => product.variation === action.variation
        )
      }

      if (indexToRemove !== -1) {
        productItems.splice(indexToRemove, 1);
      }
      break;
  }

  if (productItems.length === 0) {
    delete selectedProducts[id];
  } else {
    selectedProducts[id] = productItems;
  }

  return {
    ...state,
    selectedProducts,
  };
};

const updateHotelRoomReducer = (
  state: OrderState,
  action: UpdateHotelRoomAction,
): OrderState => {
  const id = action.id;
  const hotelRooms = { ...state.selectedHotelRooms };
  const hotelRoomById = hotelRooms[action.id] ? [...hotelRooms[id]] : [];

  switch (action.type) {
    case "addHotelRoom":
      hotelRoomById.push({
        id,
        checkin: action.checkin,
        checkout: action.checkout,
        numNights: action.checkout.diff(action.checkin, "days"),
      });
      break;
    case "removeHotelRoom":
      hotelRoomById.splice(action.index, 1);
      break;
  }

  if (hotelRoomById.length === 0) {
    delete hotelRooms[id];
  } else {
    hotelRooms[id] = hotelRoomById;
  }

  return {
    ...state,
    selectedHotelRooms: hotelRooms,
  };
};

const applyVoucher = (state: OrderState, voucher: Voucher): OrderState => {
  // This code assumes we only support 1 voucher per order.

  const items = voucher.items;
  const includeAllItems = voucher.allItems;
  const selectedProducts = { ...state.selectedProducts };

  let usagesLeft = voucher.maxUsages - voucher.redeemed;

  // We go over all the selected products either to:
  // 1. Apply the voucher code if possible
  // 2. Remove any previous stored vouchers.
  Object.entries(selectedProducts).forEach(([itemId, products]) => {
    selectedProducts[itemId] = products.map(product => {
      if (
        (!includeAllItems && items.indexOf(itemId) === -1) ||
        (voucher.variationId && product.variation !== voucher.variationId) ||
        usagesLeft === 0
      ) {
        /*
          If the item is not in the voucher code
          or there are no usages left,
          reset the stored voucher
        */
        return {
          ...product,
          voucher: null,
        };
      }

      usagesLeft--;

      // We cannot calculate the new price here.
      // we only say "here you voucher, use it when you can calculate the price"
      return {
        ...product,
        voucher,
      };
    });
  });

  return {
    ...state,
    voucherCode: voucher.code,
    selectedProducts,
  };
};

const removeVoucher = (state: OrderState) => {
  const selectedProducts = { ...state.selectedProducts };

  Object.entries(selectedProducts).forEach(([itemId, products]) => {
    selectedProducts[itemId] = products.map(product => {
      return {
        ...product,
        voucher: null,
      };
    });
  });

  return {
    ...state,
    voucherCode: "",
    selectedProducts,
  };
};

export const reducer = (state: OrderState, action: OrderAction): OrderState => {
  switch (action.type) {
    case "incrementProduct":
    case "decrementProduct":
      return updateProductReducer(state, action);
    case "addHotelRoom":
    case "removeHotelRoom":
      return updateHotelRoomReducer(state, action);
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
    case "updateIsBusiness":
      return {
        ...state,
        selectedProducts: {},
        invoiceInformation: {
          ...state.invoiceInformation,
          isBusiness: action.isBusiness,
        },
      };
    case "applyVoucher":
      return applyVoucher(state, action.voucher);
    case "removeVoucher":
      return removeVoucher(state);
  }
};
