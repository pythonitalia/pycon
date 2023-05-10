import { Heading, Section } from "@python-italia/pycon-styleguide";
import React, { useEffect } from "react";
import { FormattedMessage } from "react-intl";

import { useRouter } from "next/router";

import {
  CurrentUserQueryResult,
  TicketItem,
  TicketsQueryResult,
} from "~/types";

import { ProductsList } from "../products-list";
import { useLoginState } from "../profile/hooks";
import { CheckoutBar } from "./checkout-bar";
import { useCart } from "./use-cart";

type Props = {
  products: TicketItem[];
  hotelRooms: TicketsQueryResult["data"]["conference"]["hotelRooms"];
  conference: TicketsQueryResult["data"]["conference"];
  me: CurrentUserQueryResult["data"]["me"];
  business: boolean;
};

export const Tickets = ({
  products,
  hotelRooms,
  conference,
  business,
  me,
}: Props) => {
  const {
    updateIsBusiness,
    state: {
      invoiceInformation: { isBusiness },
    },
  } = useCart();
  const { push, query } = useRouter();
  const [loggedIn] = useLoginState();
  const voucherCode = query.voucher;

  const onCheckout = () => {
    if (loggedIn) {
      push("/tickets/checkout");
      return;
    }

    push("/login?next=/tickets/checkout");
  };

  useEffect(() => {
    if (isBusiness !== business) {
      updateIsBusiness(business);
    }
  }, []);

  return (
    <>
      <Section spacingSize="xl" illustration="snakeTailUp">
        <Heading size="display2">
          <FormattedMessage id="tickets.title" />
        </Heading>
      </Section>
      <ProductsList
        products={products}
        hotelRooms={hotelRooms}
        conference={conference}
        business={business}
        ignoreSoldOut={!!voucherCode}
        me={me}
      />
      <CheckoutBar
        onCheckout={onCheckout}
        products={products}
        hotelRooms={hotelRooms}
      />
    </>
  );
};
