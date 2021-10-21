import {
  ApolloGateway,
  LocalGraphQLDataSource,
  RemoteGraphQLDataSource,
} from "@apollo/gateway";

import { getPastaportoActionFromToken } from "./actions";
import { IS_DEV } from "./config";
import { schema as logoutSchema } from "./internal-services/logout";
import { Pastaporto } from "./pastaporto/entities";
import { getServices } from "./services";

const PASTAPORTO_X_HEADER = "x-pastaporto";
const PASTAPORTO_ACTION_X_HEADER = "x-pastaporto-action";
const BACKEND_TOKEN_X_HEADER = "x-backend-token";

class ServiceRemoteGraphQLDataSource extends RemoteGraphQLDataSource {
  async willSendRequest({
    request,
    context,
  }: Parameters<NonNullable<RemoteGraphQLDataSource["willSendRequest"]>>[0]) {
    const pastaporto: Pastaporto = context.pastaporto;
    if (pastaporto) {
      request!.http!.headers.set(PASTAPORTO_X_HEADER, pastaporto.sign());
    }

    const gatewayRequestHeaders = context.allHeaders;
    if (
      gatewayRequestHeaders &&
      gatewayRequestHeaders[BACKEND_TOKEN_X_HEADER]
    ) {
      request!.http!.headers.set(
        BACKEND_TOKEN_X_HEADER,
        gatewayRequestHeaders[BACKEND_TOKEN_X_HEADER],
      );
    }
  }

  didReceiveResponse({
    response,
    context,
  }: Parameters<
    NonNullable<RemoteGraphQLDataSource["didReceiveResponse"]>
  >[0]) {
    const headers = response.http!.headers;
    const pastaportoAction = headers.get(PASTAPORTO_ACTION_X_HEADER);

    if (pastaportoAction) {
      context.pastaportoAction = getPastaportoActionFromToken(pastaportoAction);
    }

    return response;
  }

  async process({
    request,
    context,
  }: Parameters<NonNullable<RemoteGraphQLDataSource["process"]>>[0]) {
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

export const createGateway = () => {
  const options: any = {};

  if (IS_DEV) {
    options.serviceList = getServices();
    options.experimental_pollInterval = 5000;
  }

  return new ApolloGateway({
    ...options,
    buildService({ name, url }) {
      if (name === "logout") {
        return new LocalGraphQLDataSource(logoutSchema);
      }

      return new ServiceRemoteGraphQLDataSource({
        url,
      });
    },
  });
};
