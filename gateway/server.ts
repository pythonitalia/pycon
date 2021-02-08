import { ApolloServer } from "apollo-server";
import { ApolloGateway, RemoteGraphQLDataSource } from "@apollo/gateway";
import { getPort, getServices } from "./services";

const gateway = new ApolloGateway({
  serviceList: getServices(),
  experimental_pollInterval: 5000,
  buildService({ url }) {
    return new RemoteGraphQLDataSource({
      url,
      willSendRequest({ request, context }) {
        const authorization = context.headers?.authorization;

        if (authorization) {
          request!.http!.headers.set(
            "authorization",
            context.headers?.authorization,
          );
        }
      },
    });
  },
});

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  context: ({ req }) => ({ headers: req.headers }),
});

server.listen({ port: getPort() }).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
