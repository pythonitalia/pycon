import { ApolloServer } from "apollo-server-lambda";
import { createPastaporto } from "./pastaporto";
import { gateway } from "./gateway";

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  context: async ({ event }) => ({
    pastaporto: await createPastaporto(event.headers["authorization"]),
  }),
});

exports.graphqlHandler = server.createHandler();
