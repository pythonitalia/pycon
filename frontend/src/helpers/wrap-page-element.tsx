import { ApolloProvider } from "@apollo/react-hooks";
import React from "react";
import { IntlProvider } from "react-intl";

import { client } from "../apollo/client";
import messages from "../locale";

import { EnvironmentContext } from "../context/environment";

type Props = {
  element: any;
  props: {
    pageContext: {
      language: "en" | "it";
      env: {
        stripePublishableKey: string;
        conferenceCode: string;
      };
    };
  };
};

export const wrapPageElement = ({ element, props }: Props) => (
  <IntlProvider
    locale={props.pageContext.language}
    messages={messages[props.pageContext.language]}
  >
    <ApolloProvider client={client}>
      <EnvironmentContext.Provider value={props.pageContext.env}>
        {element}
      </EnvironmentContext.Provider>
    </ApolloProvider>
  </IntlProvider>
);
