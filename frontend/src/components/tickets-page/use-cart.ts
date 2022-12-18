import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useReducer,
} from "react";

import { reducer } from "./reducer";
import { InvoiceInformationState, OrderState, Voucher } from "./types";

type CartContextType = {
  state: OrderState;
  addProduct: (id: string, variation?: string) => void;
  removeProduct: (id: string, variation?: string) => void;
  addHotelRoom: (
    id: string,
    checkin: string,
    checkout: string,
    beds: string,
  ) => void;
  removeHotelRoom: (id: string, index: number) => void;
  updateIsBusiness: (isBusiness: boolean) => void;
  applyVoucher: (voucher: Voucher) => void;
  removeVoucher: () => void;
  updateQuestionAnswer: ({ id, index, question, answer }) => void;
  updateTicketInfo: ({ id, index, key, value }) => void;
  updateInformation: (invoiceInformation: InvoiceInformationState) => void;
};

export const CartContext = createContext<CartContextType>(null);

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
  return useContext(CartContext);
};

export const createCartContext = () => {
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
      window.sessionStorage.getItem("tickets-cart-v4")!,
    ) as OrderState | null;
  }

  const [state, dispatcher] = useReducer(
    reducer,
    storedCart || emptyInitialCartReducer,
  );

  useEffect(() => {
    window.sessionStorage.setItem(
      "tickets-cart-v4",
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

  const addHotelRoom = useCallback((id, checkin, checkout, beds) => {
    dispatcher({
      type: "addHotelRoom",
      id,
      checkin,
      checkout,
      beds,
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
