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

export type OrderState = {
  selectedProducts: SelectedProducts;
  invoiceInformation: InvoiceInformationState;
};

export type UpdateProductAction =
  | { type: "incrementProduct"; id: string; variation?: string }
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
    };
