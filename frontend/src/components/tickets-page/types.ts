export type InvoiceInformationState = {
  isBusiness: string;
  companyName: string;
  name: string;
  vatId: string;
  address: string;
  zipCode: string;
  city: string;
  country: string;
};

export type ProductState = {
  quantity: number;
  variation?: string;
  id: string;
};

export type SelectedProducts = {
  [id: string]: ProductState;
};

export type OrderState = {
  selectedProducts: SelectedProducts;
  invoiceInformation: InvoiceInformationState | null;
};

export type UpdateProductAction =
  | { type: "incrementProduct"; id: string; variation?: string }
  | { type: "decrementProduct"; id: string; variation?: string };

export type OrderAction =
  | UpdateProductAction
  | { type: "updateInvoiceInformation"; data: InvoiceInformationState };
