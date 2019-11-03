/** @jsx jsx */
import { ApolloProvider } from "@apollo/react-hooks";
import { css, Global } from "@emotion/core";
import { Box } from "@theme-ui/components";
import { Fragment } from "react";
import Helmet from "react-helmet";
import { IntlProvider } from "react-intl";
import { jsx, Styled } from "theme-ui";

import { client } from "../apollo/client";
import { ErrorBoundary } from "../components/error-boundary";
import { Header } from "../components/header";
import { LanguageContext } from "../context/language";
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
  <Fragment>
    <Global styles={reset} />

    <Helmet>
      <link rel="stylesheet" href="https://use.typekit.net/mbr7dqb.css" />
    </Helmet>

    <Styled.root>
      <LanguageContext.Provider value={props.pageContext.language}>
        <IntlProvider
          locale={props.pageContext.language}
          messages={messages[props.pageContext.language]}
        >
          <ApolloProvider client={client}>
            <ErrorBoundary>
              <Header />

              <Box sx={{ mt: [100, 180] }}>{element}</Box>
            </ErrorBoundary>
          </ApolloProvider>
        </IntlProvider>
      </LanguageContext.Provider>
    </Styled.root>
  </Fragment>
);
