import moment from "moment";

import { Voucher } from "../../generated/graphql-backend";

export type InvoiceInformationState = {
  isBusiness: boolean;
  companyName: string;
  name: string;
  fiscalCode: string;
  vatId: string;
  address: string;
  zipCode: string;
  city: string;
  country: string;
};

export type ProductState = {
  variation?: string;
  id: string;
  answers: { [id: string]: string };
  attendeeName: string;
  attendeeEmail: string;
};

export type SelectedProducts = {
  [id: string]: ProductState[];
};

export type SelectedHotelRooms = {
  [id: string]: HotelRoomState[];
};

export type HotelRoomState = {
  id: string;
  checkin: moment.Moment;
  checkout: moment.Moment;
  numNights: number;
};

export type OrderState = {
  selectedProducts: SelectedProducts;
  invoiceInformation: InvoiceInformationState;
  selectedHotelRooms: SelectedHotelRooms;
};

export type UpdateProductAction =
  | { type: "incrementProduct"; id: string; variation?: string }
  | { type: "decrementProduct"; id: string; variation?: string };

export type UpdateHotelRoomAction =
  | {
      type: "addHotelRoom";
      id: string;
      checkin: moment.Moment;
      checkout: moment.Moment;
    }
  | { type: "removeHotelRoom"; id: string; index: number };

export type OrderAction =
  | UpdateProductAction
  | UpdateHotelRoomAction
  | { type: "updateInvoiceInformation"; data: InvoiceInformationState }
  | { type: "updateIsBusiness"; isBusiness: boolean }
  | {
      type: "updateTicketAnswer";
      id: string;
      index: number;
      question: string;
      answer: string;
    }
  | {
      type: "updateTicketInfo";
      id: string;
      index: number;
      key: string;
      value: string;
    }
  | {
      type: "applyVoucher";
      voucher: Voucher;
    };
