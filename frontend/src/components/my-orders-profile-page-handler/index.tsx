import { Heading, Page, Section } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useMyProfileWithOrdersQuery } from "~/types";

import { MyOrdersTable } from "./my-orders-table";
import { NoOrders } from "./no-orders";

export const MyOrdersProfilePageHandler = () => {
  const {
    data: {
      me: { orders },
    },
  } = useMyProfileWithOrdersQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
  });

  return (
    <Page endSeparator={false}>
      <Section background="purple">
        <Heading size={1}>
          <FormattedMessage id="profile.myOrders" />
        </Heading>
      </Section>
      <Section>
        {orders.length > 0 && <MyOrdersTable orders={orders} />}
        {orders.length === 0 && <NoOrders />}
      </Section>
    </Page>
  );
};
