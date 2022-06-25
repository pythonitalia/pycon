import * as NodeSentry from "@sentry/node";
import * as ServerlessSentry from "@sentry/serverless";
import { ApolloError } from "apollo-server";
import { ApolloServerPlugin } from "apollo-server-plugin-base";
import { GraphQLRequestContextDidEncounterErrors } from "apollo-server-types";
import { GraphQLError } from "graphql";

import { ENV, SENTRY_DSN } from "../config";
import { Pastaporto } from "../pastaporto/entities";

type ApolloContext = {
  pastaporto: Pastaporto;
};

export const initSentry = (isServerless: boolean) => {
  if (!SENTRY_DSN) {
    return;
  }

  const wrapper = isServerless ? ServerlessSentry.AWSLambda : NodeSentry;

  wrapper.init({
    dsn: SENTRY_DSN,
    environment: ENV,
    tracesSampleRate: 0.1,
  });
};

const shouldSkipError = (error: GraphQLError) => {
  if (error instanceof ApolloError) {
    return true;
  }

  return false;
};

const PPI_FIELDS = [
  "password",
  "addressLine1",
  "firstName",
  "lastName",
  "phoneNumber",
  "postcode",
  "country",
  "city",
  "email",
];

export const removePIIs = (
  data: { [name: string]: any } | undefined | null,
) => {
  /* This function removes personal information from an object.
     If the value is not empty and it is a personal information field
     it will be replace with [REDACTED].
     We don't replace falsy (null, empty strings) values, as it might be useful
     to know that they were falsy for debugging.
  */
  if (!data) {
    return data;
  }

  for (const [key, value] of Object.entries(data)) {
    if (typeof value == "object") {
      data[key] = removePIIs(value);
    } else {
      if (PPI_FIELDS.includes(key) && value) {
        data[key] = "[REDACTED]";
      }
    }
  }

  return data;
};

const configureScope = (
  scope: NodeSentry.Scope,
  context: GraphQLRequestContextDidEncounterErrors<ApolloContext>,
) => {
  if (context.context.pastaporto.userInfo) {
    scope.setUser({
      id: `${context.context.pastaporto.userInfo.id}`,
      ip_address: "{{auto}}",
    });
  } else {
    scope.setUser(null);
  }

  scope.setTag("kind", context.operation!.operation);
  scope.setExtra("query", context.request.query);
  scope.setExtra("variables", removePIIs(context.request.variables));
};

export const SentryPlugin = (isServerless: boolean): ApolloServerPlugin => {
  const Sentry = isServerless ? ServerlessSentry : NodeSentry;

  return {
    async requestDidStart() {
      return {
        async didEncounterErrors(
          context: GraphQLRequestContextDidEncounterErrors<ApolloContext>,
        ) {
          if (!context.operation) {
            return;
          }

          for (const err of context.errors) {
            if (shouldSkipError(err)) {
              continue;
            }

            Sentry.configureScope((scope) => {
              configureScope(scope, context);
              if (err.path) {
                scope.addBreadcrumb({
                  category: "query-path",
                  message: err.path.join(" > "),
                });
              }

              // this allows to group errors more granularly based on the error message
              scope.setFingerprint(["{{ default }}", err.message]);
              Sentry.captureException(err);
            });
          }
        },
      };
    },
  };
};
