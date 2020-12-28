/** @jsxRuntime classic */
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
      <Heading mb={4} as="h2" sx={{ fontSize: 5 }}>
        <FormattedMessage id="profile.myOrders" />
      </Heading>

      {/* @ts-ignore */}
      <Box cellSpacing={0} as="table" sx={{ width: "100%", fontSize: 2 }}>
        <tr>
          <Box
            as="th"
            sx={{
              color: "orange",
              textTransform: "uppercase",
              textAlign: "left",
              pb: 3,
            }}
          >
            <FormattedMessage id="profile.orderId" />
          </Box>
          <Box
            as="th"
            sx={{
              color: "orange",
              textTransform: "uppercase",
              textAlign: "left",
              pb: 3,
            }}
          >
            <FormattedMessage id="profile.status" />
          </Box>
          <Box
            as="th"
            sx={{
              color: "orange",
              textTransform: "uppercase",
              textAlign: "left",
              pb: 3,
            }}
          >
            <FormattedMessage id="profile.price" />
          </Box>
        </tr>

        {orders.map((order) => (
          <Box key={order.code} as="tr">
            <td sx={{ py: 3, borderTop: "primary" }}>{order.code}</td>
            <td sx={{ borderTop: "primary" }}>{order.status}</td>
            <td sx={{ borderTop: "primary" }}>€{order.total}</td>

            <td sx={{ borderTop: "primary" }}>
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
