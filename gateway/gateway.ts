import { ApolloGateway, RemoteGraphQLDataSource } from "@apollo/gateway";
import { getServices } from "./services";
import { IS_DEV } from "./config";

export const gateway = new ApolloGateway({
  serviceList: getServices(),
  experimental_pollInterval: IS_DEV ? 5000 : 0,
  buildService({ url }) {
    return new RemoteGraphQLDataSource({
      url,
      willSendRequest({ request, context }) {
        const authorization = context.headers?.authorization;
        if (authorization) {
          request!.http!.headers.set("authorization", authorization);
        }
      },
    });
  },
});
