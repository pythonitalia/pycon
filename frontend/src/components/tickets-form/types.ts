export type Ticket = {
  name: string;
  id: string;
  defaultPrice: string;
  type: "BUSINESS" | "STANDARD";
  description?: string | null;
  variations?: { id: string; value: string; defaultPrice: string }[];
  questions: {
    id: string;
    name: string;
    required: boolean;
    options: { id: string; name: string }[];
  }[];
};
