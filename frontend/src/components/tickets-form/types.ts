export type Ticket = {
  name: string;
  id: string;
  defaultPrice: string;
  description?: string | null;
  variations?: { id: string; value: string; defaultPrice: string }[];
  questions: {
    id: string;
    name: string;
    options: { id: string; name: string }[];
  }[];
};
