import "./config";

import { ApolloServer } from "apollo-server-lambda";
import { gateway } from "./gateway";

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  context: async ({ event }) => ({ headers: event.headers }),
});

exports.graphqlHandler = server.createHandler();
