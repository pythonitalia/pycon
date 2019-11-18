/** @jsx jsx */
import { ApolloProvider } from "@apollo/react-hooks";
import { css, Global } from "@emotion/core";
import { Box, Flex } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
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
    path: string;
    location: { pathname: string };
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

const isSocial = (props: Props["props"]) => {
  const suffix = "/social";

  return (
    props.location.pathname.endsWith(suffix) || props.path.endsWith(suffix)
  );
};

const Meta = ({ titleTemplate }: { titleTemplate: string }) => {
  const {
    site: { siteMetadata },
  } = useStaticQuery(graphql`
    {
      site {
        siteMetadata {
          siteUrl
        }
      }
    }
  `);

  const socialCard = `${siteMetadata.siteUrl}/social/social.png`;

  return (
    <Helmet
      titleTemplate={titleTemplate}
      meta={[
        {
          name: "twitter:card",
          content: "summary_large_image",
        },
        {
          property: "og:image",
          content: socialCard,
        },
        {
          name: "twitter:image",
          content: socialCard,
        },
      ]}
    >
      <link rel="stylesheet" href="https://use.typekit.net/mbr7dqb.css" />
    </Helmet>
  );
};

export const wrapPageElement = ({ element, props }: Props) => {
  const titleTemplate =
    messages[props.pageContext.language || "en"].titleTemplate;

  return (
    <Fragment>
      <Global styles={reset} />

      <Meta titleTemplate={titleTemplate} />

      <Styled.root>
        {isSocial(props) ? (
          element
        ) : (
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
                    <Box sx={{ mt: [100, 130] }}>
                      <ErrorBoundary>{element}</ErrorBoundary>
                    </Box>

                    <Footer />
                  </Flex>
                </ApolloProvider>
              </IntlProvider>
            </LanguageContext.Provider>
          </ConferenceContext.Provider>
        )}
      </Styled.root>
    </Fragment>
  );
};
