import {
  ApolloGateway,
  LocalGraphQLDataSource,
  RemoteGraphQLDataSource,
} from "@apollo/gateway";

import { IS_DEV } from "./config";
import { schema as logoutSchema } from "./internal-services/logout";
import { getServices } from "./services";

const PASTAPORTO_X_HEADER = "x-pastaporto";
const BACKEND_TOKEN_X_HEADER = "x-backend-token";

class ServiceRemoteGraphQLDataSource extends RemoteGraphQLDataSource {
  async willSendRequest({
    request,
    context,
  }: Parameters<NonNullable<RemoteGraphQLDataSource["willSendRequest"]>>[0]) {
    if (context.pastaporto) {
      request!.http!.headers.set(PASTAPORTO_X_HEADER, context.pastaporto);
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
    const setCookie = headers.get("set-cookie");

    if (setCookie) {
      context.res.set("set-cookie", setCookie);
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
