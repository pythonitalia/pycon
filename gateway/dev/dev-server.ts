import "../config";

import { ApolloServer } from "apollo-server";
import { getPort } from "./utils";
import { gateway } from "../gateway";

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  context: ({ req }) => ({ headers: req.headers }),
});

server.listen({ port: getPort() }).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
