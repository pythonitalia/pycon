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
import { MetaTags } from "../components/meta-tags";
import { ConferenceContext } from "../context/conference";
import { AlternateLinksContext, LanguageContext } from "../context/language";
import messages from "../locale";

type Props = {
  element: any;
  props: {
    path: string;
    location: { pathname: string };
    pageContext: {
      language: "en" | "it";
      alternateLinks: { en: string; it: string };
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

const isSocial = (props: Props["props"]) => {
  const suffix = "/social";
  const suffixSquare = "/social-square";
  const suffixTwitter = "/social-twitter";

  return (
    props.location.pathname.endsWith(suffix) ||
    props.location.pathname.endsWith(suffixSquare) ||
    props.location.pathname.endsWith(suffixTwitter) ||
    props.path.endsWith(suffix) ||
    props.path.endsWith(suffixSquare) ||
    props.path.endsWith(suffixTwitter)
  );
};

const getAlternateLinks = (props: Props["props"]) => {
  if (typeof window !== "undefined") {
    /*
      when we are not SSO,
      use the location's pathname to generate
      more specific URLs:

      Example /en/submission/{ID} cannot be generated server side,
      so we replace it with the current pathname.
    */
    const pathname = window.location.pathname
      .replace("/en/", "")
      .replace("/it/", "");

    return {
      en: `/en/${pathname}`,
      it: `/it/${pathname}`,
    };
  }

  return props.pageContext.alternateLinks;
};

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
          {isSocial(props) ? (
            element
          ) : (
            <ConferenceContext.Provider
              value={props.pageContext.conferenceCode}
            >
              <AlternateLinksContext.Provider value={getAlternateLinks(props)}>
                <ApolloProvider client={client}>
                  <MetaTags />

                  <Header />

                  <Flex
                    sx={{
                      flexDirection: "column",
                      minHeight: "100vh",
                    }}
                  >
                    <Box sx={{ mt: [100, 130] }}>
                      <ErrorBoundary>{element}</ErrorBoundary>
                    </Box>

                    <Footer />
                  </Flex>
                </ApolloProvider>
              </AlternateLinksContext.Provider>
            </ConferenceContext.Provider>
          )}
        </IntlProvider>
      </LanguageContext.Provider>
    </Styled.root>
  </Fragment>
);
