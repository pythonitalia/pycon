export type Ticket = {
  name: string;
  id: string;
  defaultPrice: string;
  category: string;
  type: "HOTEL" | "BUSINESS" | "STANDARD";
  description?: string | null;
  variations?: { id: string; value: string; defaultPrice: string }[];
  availableUntil?: string;
  soldOut?: boolean;
  questions: {
    id: string;
    name: string;
    required: boolean;
    options: { id: string; name: string }[];
  }[];
};
