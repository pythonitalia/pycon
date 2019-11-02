import { ApolloProvider } from "@apollo/react-hooks";
import React from "react";
import Helmet from "react-helmet";
import { IntlProvider } from "react-intl";

import { client } from "../apollo/client";
import messages from "../locale";

type Props = {
  element: any;
  props: {
    pageContext: {
      language: "en" | "it";
    };
  };
};

export const wrapPageElement = ({ element, props }: Props) => (
  <IntlProvider
    locale={props.pageContext.language}
    messages={messages[props.pageContext.language]}
  >
    <Helmet>
      <link rel="stylesheet" href="https://use.typekit.net/mbr7dqb.css" />
    </Helmet>
    <ApolloProvider client={client}>{element}</ApolloProvider>
  </IntlProvider>
);
