import { Button, Tag, Text } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useMoneyFormatter } from "~/helpers/formatters";
import { MyProfileWithOrdersQuery } from "~/types";

import { Table } from "../table";

type Props = {
  orders: MyProfileWithOrdersQuery["me"]["orders"];
};
export const MyOrdersTable = ({ orders }: Props) => {
  const moneyFormatter = useMoneyFormatter();

  return (
    <Table
      cols={4}
      rowGetter={(data) => [
        <Text weight="strong" size={2}>
          {data.code}
        </Text>,
        <OrderStatusTag status={data.status} />,
        <Text size={2}>{moneyFormatter.format(parseFloat(data.total))}</Text>,
        <Button href={data.url} variant="secondary">
          <FormattedMessage id="profile.myOrders.open" />
        </Button>,
      ]}
      keyGetter={(order) => order.code}
      data={orders}
    />
  );
};

const OrderStatusTag = ({ status }: { status: string }) => {
  switch (status.toLowerCase()) {
    case "pending":
      return (
        <Tag color="yellow">
          <FormattedMessage id="profile.myOrders.orderStatus.pending" />
        </Tag>
      );
    case "paid":
      return (
        <Tag color="green">
          <FormattedMessage id="profile.myOrders.orderStatus.paid" />
        </Tag>
      );
    case "canceled":
      return (
        <Tag color="red">
          <FormattedMessage id="profile.myOrders.orderStatus.canceled" />
        </Tag>
      );
    case "expired":
      return (
        <Tag color="red">
          <FormattedMessage id="profile.myOrders.orderStatus.expired" />
        </Tag>
      );
  }
};
