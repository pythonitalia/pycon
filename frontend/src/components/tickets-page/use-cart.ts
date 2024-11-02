import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useReducer,
} from "react";

import { reducer } from "./reducer";
import type { InvoiceInformationState, OrderState, Voucher } from "./types";

type CartContextType = {
  state: OrderState;
  addProduct: (id: string, variation?: string, admission?: boolean) => void;
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
  updateAcceptedPrivacyPolicy: (accepted: boolean) => void;
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

function toBinaryStr(str) {
  const encoder = new TextEncoder();
  // 1: split the UTF-16 string into an array of bytes
  const charCodes = encoder.encode(str);
  // 2: concatenate byte data to create a binary string
  // eslint-disable-next-line
  // @ts-ignore
  return String.fromCharCode(...charCodes);
}

function fromBinaryStr(binary) {
  // 1: create an array of bytes
  const bytes = Uint8Array.from({ length: binary.length }, (_, index) =>
    binary.charCodeAt(index),
  );

  // 2: decode the byte data into a string
  const decoder = new TextDecoder("utf-8");
  return decoder.decode(bytes);
}

export const EMPTY_INITIAL_CART_REDUCER = {
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
    pec: "",
    sdi: "",
  },
  voucherCode: "",
  voucherUsed: false,
  hasAdmissionTicket: false,
};

export const createCartContext = ({
  cartCookie = "",
}: {
  cartCookie?: string;
}) => {
  let storedCart = null;

  try {
    if (typeof window !== "undefined") {
      storedCart = JSON.parse(
        window.sessionStorage.getItem("tickets-cart-v6")!,
      ) as OrderState | null;
    } else if (cartCookie) {
      storedCart = JSON.parse(
        atob(fromBinaryStr(cartCookie)),
      ) as OrderState | null;
    }
  } catch (e) {
    console.error("unable to restore cart", e);
    storedCart = null;
  }

  const [state, dispatcher] = useReducer(
    reducer,
    storedCart || EMPTY_INITIAL_CART_REDUCER,
  );

  useEffect(() => {
    const cartAsJson = JSON.stringify(state, cartReplacer) || "{}";
    window.sessionStorage.setItem("tickets-cart-v6", cartAsJson);
    document.cookie = `tickets-cart-v6=${btoa(
      toBinaryStr(cartAsJson),
    )}; path=/;`;
  }, [state]);

  const addProduct = (id: string, variation?: string, admission?: boolean) =>
    dispatcher({
      type: "incrementProduct",
      id,
      variation,
      admission,
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

  const updateAcceptedPrivacyPolicy = useCallback(
    (accepted: boolean) =>
      dispatcher({
        type: "updateAcceptedPrivacyPolicy",
        accepted,
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
    updateAcceptedPrivacyPolicy,
  };
};
