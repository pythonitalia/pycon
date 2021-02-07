import { ApolloServer } from "apollo-server";
import { ApolloGateway, RemoteGraphQLDataSource } from "@apollo/gateway";

const gateway = new ApolloGateway({
  serviceList: [
    {
      name: "users",
      url: "http://localhost:8050/graphql",
    },
  ],
  buildService({ url }) {
    return new RemoteGraphQLDataSource({
      url,
      willSendRequest({ request, context }) {
        const authorization = context.headers?.authorization;

        if (authorization) {
          request!.http!.headers.set(
            "authorization",
            context.headers?.authorization
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

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
