export type ProductState = {
  quantity: number;
  variation?: string;
  id: string;
};

export type ProductsState = {
  [id: string]: ProductState;
};

export type ProductAction =
  | { type: "increment"; id: string; variation?: string }
  | { type: "decrement"; id: string; variation?: string };
