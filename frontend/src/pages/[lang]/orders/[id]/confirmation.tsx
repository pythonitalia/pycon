/** @jsx jsx */
import { useRouter } from "next/router";
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx, Text } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";
import { Alert } from "~/components/alert";
import { PageLoading } from "~/components/page-loading";
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
      {data.order.status === "CANCELED" ? (
        <OrderCanceled />
      ) : (
        <OrderSucceeded url={data.order.url} />
      )}
    </Box>
  );
};

export default OrderConfirmationPage;
