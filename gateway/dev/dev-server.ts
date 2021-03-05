import { ApolloServer } from "apollo-server";
import { getPort } from "./utils";
import { gateway } from "../gateway";
import { createPastaporto } from "../pastaporto";

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  context: async ({ req }) => ({
    pastaporto: await createPastaporto(req.headers["authorization"]),
  }),
});

server.listen({ port: getPort() }).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
