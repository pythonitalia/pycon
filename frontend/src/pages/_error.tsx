/* eslint-disable @typescript-eslint/ban-ts-comment */

/** @jsxRuntime classic */

/** @jsx jsx */
import * as Sentry from "@sentry/node";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx, Text } from "theme-ui";

import { GetStaticProps } from "next";
import NextErrorComponent from "next/error";

import { getApolloClient, addApolloState } from "~/apollo/client";
import { Link } from "~/components/link";
import { prefetchSharedQueries } from "~/helpers/prefetch";

const ErrorPage = ({ statusCode }) => (
  <Box sx={{ mt: 4, mx: "auto", maxWidth: "container", px: 3, pb: 6 }}>
    <Heading as="h2" sx={{ mb: 2 }}>
      Ops {statusCode}
    </Heading>

    {statusCode === 404 && (
      <Text>
        <FormattedMessage id="error404.message" />
        <Link path="/" sx={{ display: "block", mt: 2 }}>
          <FormattedMessage id="error404.goToHomepage" />
        </Link>
      </Text>
    )}

    <video
      sx={{
        position: "absolute",
        top: 0,
        left: 0,
        height: "100vh",
        width: "100vw",
        zIndex: -1,
        pointerEvents: "none",
        objectFit: "cover",
        opacity: 0.5,
      }}
      src="/videos/sad.mp4"
      autoPlay={true}
      muted={true}
      loop={true}
    />
  </Box>
);

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([prefetchSharedQueries(client, locale)]);

  return addApolloState(client, {
    props: {},
  });
};

export default ErrorPage;
