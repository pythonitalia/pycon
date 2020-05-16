/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, Flex, Heading, jsx, Text } from "theme-ui";

type Props = {
  orders: {
    code: string;
    status: string;
    total: string;
    url: string;
  }[];
};

export const MyOrders: React.SFC<Props> = ({ orders }) => (
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
        <tbody>
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

          {orders.map((order) => (
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
        </tbody>
      </Box>
    </Box>
  </Box>
);
