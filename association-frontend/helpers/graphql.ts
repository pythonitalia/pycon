import { createClient } from "urql";

export const client = createClient({
  url: "http://localhost:3020/graphql",
});
