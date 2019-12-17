/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Heading, Text } from "@theme-ui/components";
import React, { useContext } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { ConferenceContext } from "../../context/conference";
import { OrderQuery } from "../../generated/graphql-backend";
import ORDER_QUERY from "./order.graphql";

const OrderDetail: React.SFC<{ code: string }> = ({ code }) => {
  const conferenceCode = useContext(ConferenceContext);

  const { data, loading, error } = useQuery<OrderQuery>(ORDER_QUERY, {
    variables: {
      code,
      conferenceCode,
    },
  });

  if (error) {
    throw new Error(error.message);
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

export const OrderConfirmationScreen: React.SFC<RouteComponentProps<{
  code: string;
}>> = ({ code }) => (
  <Box sx={{ maxWidth: "container", px: 3, mx: "auto" }}>
    <Heading sx={{ mb: 3 }}>Order confirmation!</Heading>

    <Text>
      Thanks for the order! You should receive an email confirmation soon!
    </Text>

    <OrderDetail code={code!} />
  </Box>
);
