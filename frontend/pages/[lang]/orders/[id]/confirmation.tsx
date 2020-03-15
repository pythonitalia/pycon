/** @jsx jsx */
import { Box, Heading, Text } from "@theme-ui/components";
import { useRouter } from "next/router";
import React from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { useOrderQuery } from "~/types";

const OrderDetail = () => {
  const router = useRouter();
  const code = router.query.id as string;

  const { data, loading, error } = useOrderQuery({
    variables: { code, conferenceCode: process.env.conferenceCode },
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
    return null;
  }

  return (
    <React.Fragment>
      <a href={data.order?.url} target="_blank" rel="noopener noreferrer">
        <FormattedMessage id="orderConfirmation.manage" />
      </a>
    </React.Fragment>
  );
};

export default () => (
  <Box sx={{ maxWidth: "container", px: 3, mx: "auto" }}>
    <Heading sx={{ mb: 3 }}>
      <FormattedMessage id="orderConfirmation.heading" />
    </Heading>

    <Text>
      <FormattedMessage id="orderConfirmation.successMessage" />
    </Text>

    <OrderDetail />
  </Box>
);
