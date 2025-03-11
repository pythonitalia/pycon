export type InvoiceInformationState = {
  isBusiness: boolean;
  companyName: string;
  firstName: string;
  lastName: string;
  fiscalCode: string;
  pec: string;
  sdi: string;
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

type ProductStateComplexErrors = {
  attendeeName?: {
    givenName: string[];
    familyName: string[];
  };
  answers?: {
    [key: string]: string[];
  };
};

type ProductStateGenericErrors = {
  [key: string]: string[];
};

export type ProductStateErrors = ProductStateComplexErrors &
  ProductStateGenericErrors;

export type ProductState = {
  variation?: string;
  id: string;
  index: number;
  answers: { [id: string]: string };
  attendeeGivenName: string;
  attendeeFamilyName: string;
  attendeeEmail: string;
  admission?: boolean;
  voucher?: Voucher | null;
  errors?: ProductStateErrors;
  isMe: boolean;
};

export type SelectedProducts = {
  [id: string]: ProductState[];
};

export type OrderState = {
  selectedProducts: SelectedProducts;
  invoiceInformation: InvoiceInformationState;
  voucherCode: string;
  voucherUsed: boolean;
  hasAdmissionTicket: boolean;
  acceptedPrivacyPolicy: boolean;
};

export type UpdateProductAction =
  | {
      type: "incrementProduct";
      id: string;
      variation?: string;
      admission?: boolean;
    }
  | { type: "decrementProduct"; id: string; variation?: string };

export type OrderAction =
  | UpdateProductAction
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
    }
  | {
      type: "updateAcceptedPrivacyPolicy";
      accepted: boolean;
    };
