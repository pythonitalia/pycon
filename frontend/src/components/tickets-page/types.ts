export type HotelRoom = {
  id: string;
  name: string;
  description: string;
  price: string;
  isSoldOut: boolean;
  capacityLeft: number;
};

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

export type Voucher = {
  id: string;
  code: string;
  validUntil?: string;
  value: string;
  items: string[];
  allItems: boolean;
  redeemed: number;
  maxUsages: number;
  priceMode: string;
  variationId?: string;
};

export type ProductState = {
  variation?: string;
  id: string;
  answers: { [id: string]: string };
  attendeeName: string;
  attendeeEmail: string;
  admission?: boolean;
  voucher?: Voucher | null;
  errors?: { [id: string]: string };
};

export type SelectedProducts = {
  [id: string]: ProductState[];
};

export type SelectedHotelRooms = {
  [id: string]: HotelRoomState[];
};

export type HotelRoomState = {
  id: string;
  checkin: string;
  checkout: string;
  beds: string;
  numNights: number;
};

export type OrderState = {
  selectedProducts: SelectedProducts;
  invoiceInformation: InvoiceInformationState;
  selectedHotelRooms: SelectedHotelRooms;
  voucherCode: string;
  voucherUsed: boolean;
  hasAdmissionTicket: boolean;
};

export type UpdateProductAction =
  | {
      type: "incrementProduct";
      id: string;
      variation?: string;
      admission?: boolean;
    }
  | { type: "decrementProduct"; id: string; variation?: string };

export type UpdateHotelRoomAction =
  | {
      type: "addHotelRoom";
      id: string;
      checkin: string;
      checkout: string;
      beds: string;
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
    }
  | {
      type: "removeVoucher";
    };
