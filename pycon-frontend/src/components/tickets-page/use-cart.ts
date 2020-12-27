import moment from "moment";
import { useCallback, useEffect, useReducer } from "react";

import { reducer } from "./reducer";
import { InvoiceInformationState, OrderState, Voucher } from "./types";

const cartReplacer = (key: string, value: any) => {
  if (key === "voucher" || key === "voucherUsed") {
    /*
      Remove the stored voucher state from the products.
      we want to make sure it's always up to date
      so we remove it and fetch it again when the user refreshes the page
    */
    return undefined;
  }

  return value;
};

export const useCart = () => {
  const emptyInitialCartReducer = {
    selectedProducts: {},
    invoiceInformation: {
      isBusiness: false,
      companyName: "",
      name: "",
      vatId: "",
      address: "",
      zipCode: "",
      city: "",
      country: "",
      fiscalCode: "",
    },
    selectedHotelRooms: {},
    voucherCode: "",
    voucherUsed: false,
  };

  let storedCart = null;

  if (typeof window !== "undefined") {
    storedCart = JSON.parse(
      window.localStorage.getItem("tickets-cart")!,
    ) as OrderState | null;

    if (storedCart) {
      /* restore the check-in and check-out as moment dates and not strings */
      Object.values(storedCart.selectedHotelRooms).forEach(
        (reservations: any) => {
          reservations.forEach((reservation) => {
            reservation.checkin = moment(reservation.checkin);
            reservation.checkout = moment(reservation.checkout);
          });
        },
      );
    }
  }

  const [state, dispatcher] = useReducer(
    reducer,
    storedCart || emptyInitialCartReducer,
  );

  useEffect(() => {
    window.localStorage.setItem(
      "tickets-cart",
      JSON.stringify(state, cartReplacer),
    );
  }, [state]);

  const addProduct = (id: string, variation?: string) =>
    dispatcher({
      type: "incrementProduct",
      id,
      variation,
    });

  const removeProduct = (id: string, variation?: string) =>
    dispatcher({
      type: "decrementProduct",
      id,
      variation,
    });

  const updateQuestionAnswer = useCallback(
    ({ id, index, question, answer }) =>
      dispatcher({
        type: "updateTicketAnswer",
        id,
        index,
        question,
        answer,
      }),
    [],
  );

  const updateTicketInfo = useCallback(
    ({ id, index, key, value }) =>
      dispatcher({
        type: "updateTicketInfo",
        id,
        index,
        key,
        value,
      }),
    [],
  );

  const updateIsBusiness = useCallback(
    (isBusiness: boolean) =>
      dispatcher({
        type: "updateIsBusiness",
        isBusiness,
      }),
    [],
  );

  const addHotelRoom = useCallback((id, checkin, checkout) => {
    dispatcher({
      type: "addHotelRoom",
      id,
      checkin,
      checkout,
    });
  }, []);

  const removeHotelRoom = useCallback((id, index) => {
    dispatcher({
      type: "removeHotelRoom",
      id,
      index,
    });
  }, []);

  const applyVoucher = useCallback(
    (voucher: Voucher) =>
      dispatcher({
        type: "applyVoucher",
        voucher,
      }),
    [],
  );

  const removeVoucher = useCallback(
    () =>
      dispatcher({
        type: "removeVoucher",
      }),
    [],
  );

  const updateInformation = useCallback(
    (invoiceData: InvoiceInformationState) =>
      dispatcher({
        type: "updateInvoiceInformation",
        data: invoiceData,
      }),
    [],
  );

  return {
    state,
    addHotelRoom,
    removeHotelRoom,
    removeProduct,
    addProduct,
    updateIsBusiness,
    applyVoucher,
    removeVoucher,
    updateQuestionAnswer,
    updateTicketInfo,
    updateInformation,
  };
};
