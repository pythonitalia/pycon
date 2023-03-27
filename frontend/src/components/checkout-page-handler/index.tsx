import { Heading, Section, Spacer } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import {
  CurrentUserQueryResult,
  TicketItem,
  TicketsQueryResult,
} from "~/types";

import { BillingCard } from "./billing-card";
import { CreateOrderBar } from "./create-order-bar";
import { ProductsQuestions } from "./products-questions";
import { RecapCard } from "./recap-card";
import { VoucherCard } from "./voucher-card";

type Props = {
  products: TicketItem[];
  hotelRooms: TicketsQueryResult["data"]["conference"]["hotelRooms"];
  me: CurrentUserQueryResult["data"]["me"];
  conference: TicketsQueryResult["data"]["conference"];
};

export const CheckoutPageHandler = ({
  products,
  hotelRooms,
  me,
  conference,
}: Props) => {
  const productsById = Object.fromEntries(
    products.map((product) => [product.id, product]),
  );
  const hotelRoomsById = Object.fromEntries(
    hotelRooms!.map((room) => [room.id, room]),
  );

  return (
    <form onSubmit={(e) => e.preventDefault()} className="divide-y-3">
      <Section spacingSize="xl" illustration="snakeTailUp">
        <Heading size="display2">
          <FormattedMessage id="tickets.checkout.title" />
        </Heading>
      </Section>
      <Section>
        <ProductsQuestions productsById={productsById} />
        <BillingCard />
        <Spacer size="xs" />
        <VoucherCard />
        <Spacer size="xs" />
        <RecapCard
          hotelRoomsById={hotelRoomsById}
          productsById={productsById}
        />
      </Section>
      <CreateOrderBar
        productsById={productsById}
        hotelRoomsById={hotelRoomsById}
        conferenceTimeZone={conference.timeZone}
        userEmail={me?.email}
      />
    </form>
  );
};
