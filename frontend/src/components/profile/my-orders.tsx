/** @jsxRuntime classic */

/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { Table } from "~/components/table";
import { useTranslatedMessage } from "~/helpers/use-translated-message";

type Props = {
  orders: {
    code: string;
    status: string;
    total: string;
    url: string;
  }[];
};

export const MyOrders = ({ orders }: Props) => {
  const orderIdHeader = useTranslatedMessage("profile.orderId");
  const statusHeader = useTranslatedMessage("profile.status");
  const priceHeader = useTranslatedMessage("profile.price");

  return (
    <Box
      sx={{
        borderTop: "primary",
      }}
    >
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          my: 5,
          px: 3,
        }}
      >
        <Heading mb={5} as="h2" sx={{ fontSize: 5 }}>
          <FormattedMessage id="profile.myOrders" />
        </Heading>

        <Table
          headers={[orderIdHeader, statusHeader, priceHeader, ""]}
          mobileHeaders={[orderIdHeader, statusHeader, priceHeader, ""]}
          data={orders}
          keyGetter={(item) => item.code}
          rowGetter={(item) => [
            item.code,
            item.status,
            `€${item.total}`,
            <a
              key="manageOrder"
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              sx={{
                textDecoration: "underline",
              }}
            >
              <FormattedMessage id="profile.manageOrder" />
            </a>,
          ]}
        />
      </Box>
    </Box>
  );
};
