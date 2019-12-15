export type Ticket = {
  name: string;
  id: string;
  defaultPrice: string;
  description?: string | null;
  variations?: { id: string; value: string; defaultPrice: string }[];
};
