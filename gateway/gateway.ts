import { ApolloGateway, RemoteGraphQLDataSource } from "@apollo/gateway";
import { getServices } from "./services";
import { IS_DEV } from "./config";
import { Pastaporto } from "./pastaporto/entities";
import { getPastaportoActionFromToken } from "./actions";

const PASTAPORTO_ACTION_X_HEADER = "x-pastaporto-action";

class ServiceRemoteGraphQLDataSource extends RemoteGraphQLDataSource {
  // @ts-ignore
  async willSendRequest({ request, context }) {
    const pastaporto: Pastaporto = context.pastaporto;
    if (pastaporto) {
      request!.http!.headers.set("x-pastaporto", await pastaporto.sign());
    }
  }

  // @ts-ignore
  didReceiveResponse({ response, request, context }) {
    const headers = response.http!.headers;
    const pastaportoAction = headers.get(PASTAPORTO_ACTION_X_HEADER);

    if (pastaportoAction) {
      context.pastaportoAction = getPastaportoActionFromToken(pastaportoAction);
    }

    return response;
  }

  // @ts-ignore
  async process({ request, context }) {
    const response = await super.process({
      request,
      context,
    });

    if (context.pastaportoAction) {
      await context.pastaportoAction.apply(context);
    }

    return response;
  }
}

export const gateway = new ApolloGateway({
  serviceList: getServices(),
  experimental_pollInterval: IS_DEV ? 5000 : 0,
  buildService({ url }) {
    return new ServiceRemoteGraphQLDataSource({
      url,
    });
  },
});
