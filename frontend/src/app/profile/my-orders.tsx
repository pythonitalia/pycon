/** @jsx jsx */
import { Box, Flex, Heading, Text } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { MyProfileQuery } from "../../generated/graphql-backend";

export const MyOrders: React.SFC<{
  orders: MyProfileQuery["me"]["orders"];
}> = ({ orders }) => (
  <Box
    sx={{
      borderTop: "primary",
    }}
  >
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        my: 4,
        px: 3,
      }}
    >
      <Heading mb={2} as="h2">
        <FormattedMessage id="profile.myOrders" />
      </Heading>

      <Box as="table" sx={{ width: "100%" }}>
        <tr>
          <Box as="th" sx={{ textAlign: "left" }}>
            <FormattedMessage id="profile.orderId" />
          </Box>
          <Box as="th" sx={{ textAlign: "left" }}>
            <FormattedMessage id="profile.status" />
          </Box>
          <Box as="th" sx={{ textAlign: "left" }}>
            <FormattedMessage id="profile.price" />
          </Box>
        </tr>

        {orders.map(order => (
          <Box key={order.code} as="tr">
            <td>{order.code}</td>
            <td>{order.status}</td>
            <td>€ {order.total}</td>

            <td>
              <a href={order.url} target="_blank" rel="noopener noreferrer">
                <FormattedMessage id="profile.manageOrder" />
              </a>
            </td>
          </Box>
        ))}
      </Box>
    </Box>
  </Box>
);
