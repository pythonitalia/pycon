/** @jsx jsx */
import { ApolloProvider } from "@apollo/react-hooks";
import { css, Global } from "@emotion/core";
import { Box, Flex } from "@theme-ui/components";
import { Fragment } from "react";
import { Helmet } from "react-helmet";
import { IntlProvider } from "react-intl";
import { jsx, Styled } from "theme-ui";

import { client } from "../apollo/client";
import { ErrorBoundary } from "../components/error-boundary";
import { Footer } from "../components/footer";
import { Header } from "../components/header";
import { ConferenceContext } from "../context/conference";
import { LanguageContext } from "../context/language";
import messages from "../locale";

type Props = {
  element: any;
  props: {
    pageContext: {
      language: "en" | "it";
      conferenceCode: string;
    };
  };
};

const reset = css`
  * {
    margin: 0;
    padding: 0;
  }

  .article {
    line-height: 1.6;

    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    p,
    ol,
    ul {
      margin-bottom: 1em;
    }

    ol,
    ul,
    li {
      padding-left: 1em;
    }
  }
`;

export const wrapPageElement = ({ element, props }: Props) => {
  const titleTemplate =
    messages[props.pageContext.language || "en"].titleTemplate;

  return (
    <Fragment>
      <Global styles={reset} />

      {console.log(props.pageContext.language)}

      <Helmet titleTemplate={titleTemplate}>
        <link rel="stylesheet" href="https://use.typekit.net/mbr7dqb.css" />
      </Helmet>

      <Styled.root>
        <ConferenceContext.Provider value={props.pageContext.conferenceCode}>
          <LanguageContext.Provider value={props.pageContext.language}>
            <IntlProvider
              locale={props.pageContext.language}
              messages={messages[props.pageContext.language]}
            >
              <ApolloProvider client={client}>
                <Header />

                <Flex
                  sx={{
                    flexDirection: "column",
                    minHeight: "100vh",
                  }}
                >
                  <Box sx={{ mt: [100, 180] }}>
                    <ErrorBoundary>{element}</ErrorBoundary>
                  </Box>

                  <Footer />
                </Flex>
              </ApolloProvider>
            </IntlProvider>
          </LanguageContext.Provider>
        </ConferenceContext.Provider>
      </Styled.root>
    </Fragment>
  );
};
