import { SelectedProducts } from "./types";

export const hasSelectedAtLeastOneProduct = (
  selectedProducts: SelectedProducts,
) => Object.values(selectedProducts).length > 0;
