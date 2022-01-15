/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx, Text } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { PageLoading } from "~/components/page-loading";
import { useLoginState } from "~/components/profile/hooks";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useOrderQuery } from "~/types";

const OrderCanceled = () => (
  <React.Fragment>
    <Heading sx={{ mb: 3 }}>
      <FormattedMessage id="orderConfirmation.heading.canceled" />
    </Heading>
  </React.Fragment>
);

const OrderSucceeded = ({ url }: { url: string }) => (
  <React.Fragment>
    <Heading sx={{ mb: 3 }}>
      <FormattedMessage id="orderConfirmation.heading" />
    </Heading>
    <Text>
      <FormattedMessage id="orderConfirmation.successMessage" />
    </Text>
    <a href={url} target="_blank" rel="noopener noreferrer">
      <FormattedMessage id="orderConfirmation.manage" />
    </a>
  </React.Fragment>
);

const OrderPending = ({ url, code }: { url: string; code: string }) => (
  <React.Fragment>
    <Heading sx={{ mb: 3 }}>
      <FormattedMessage id="orderConfirmation.heading.pending" />
    </Heading>
    <Text>
      <FormattedMessage id="orderConfirmation.pendingMessage" />
    </Text>
    <Text>
      <a href={url} target="_blank" rel="noopener noreferrer">
        <FormattedMessage id="orderConfirmation.pendingManage" />
      </a>
    </Text>
    <Text
      sx={{
        mt: 2,
      }}
    >
      <FormattedMessage
        id="orderConfirmation.bankMessage"
        values={{
          code: (
            <Text
              as="span"
              sx={{
                fontWeight: "bold",
              }}
            >
              {code}
            </Text>
          ),
          email: (
            <a target="_blank" href="mailto:info@pycon.it">
              info@pycon.it
            </a>
          ),
        }}
      />
    </Text>
  </React.Fragment>
);

export const OrderConfirmationPage = () => {
  const [loggedIn, _] = useLoginState();

  const router = useRouter();
  const code = router.query.id as string;

  const { data, loading, error } = useOrderQuery({
    variables: { code, conferenceCode: process.env.conferenceCode },
    skip: !loggedIn,
  });

  if (error) {
    return (
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        <Alert variant="alert">{error.message}</Alert>
      </Box>
    );
  }

  if (loading || !data) {
    return <PageLoading titleId="global.loading" />;
  }

  return (
    <Box sx={{ maxWidth: "container", px: 3, mx: "auto" }}>
      {data.order.status === "CANCELED" && <OrderCanceled />}
      {data.order.status === "PAID" && <OrderSucceeded url={data.order.url} />}
      {data.order.status === "PENDING" && (
        <OrderPending code={code} url={data.order.url} />
      )}
    </Box>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await prefetchSharedQueries(client, locale);

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default OrderConfirmationPage;
