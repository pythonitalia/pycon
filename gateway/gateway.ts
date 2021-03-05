import { ApolloGateway, RemoteGraphQLDataSource } from "@apollo/gateway";
import { getServices } from "./services";
import { IS_DEV } from "./config";
import { Pastaporto } from "./pastaporto/entities";

export const gateway = new ApolloGateway({
  serviceList: getServices(),
  experimental_pollInterval: IS_DEV ? 5000 : 0,
  buildService({ url }) {
    return new RemoteGraphQLDataSource({
      url,
      async willSendRequest({ request, context }) {
        const pastaporto: Pastaporto = context.pastaporto;
        if (pastaporto) {
          request!.http!.headers.set("x-pastaporto", await pastaporto.sign());
        }
      },
    });
  },
});
