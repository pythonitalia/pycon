import { ApolloProvider } from "@apollo/react-hooks";
import { css, Global } from "@emotion/core";
import React from "react";
import Helmet from "react-helmet";
import { IntlProvider } from "react-intl";
import { Styled } from "theme-ui";

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

const reset = css`
  * {
    margin: 0;
    padding: 0;
  }
`;

export const wrapPageElement = ({ element, props }: Props) => (
  <>
    <Global styles={reset} />

    <Helmet>
      <link rel="stylesheet" href="https://use.typekit.net/mbr7dqb.css" />
    </Helmet>

    <Styled.root>
      <IntlProvider
        locale={props.pageContext.language}
        messages={messages[props.pageContext.language]}
      >
        <ApolloProvider client={client}>{element}</ApolloProvider>
      </IntlProvider>
    </Styled.root>
  </>
);
