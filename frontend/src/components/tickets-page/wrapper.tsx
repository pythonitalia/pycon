import { Page, Section } from "@python-italia/pycon-styleguide";
import React, { useEffect } from "react";
import { FormattedMessage } from "react-intl";

import { useRouter } from "next/router";

import { Alert } from "~/components/alert";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useCurrentLanguage } from "~/locale/context";
import {
  CurrentUserQueryResult,
  TicketsQueryResult,
  TicketType,
  useTicketsQuery,
  TicketItem,
} from "~/types";

import { CartContext, createCartContext } from "./use-cart";
import { hasSelectedAtLeastOneProduct } from "./utils";

type Props = {
  children: (props: {
    tickets: TicketItem[];
    hotelRooms: TicketsQueryResult["data"]["conference"]["hotelRooms"];
    conference: TicketsQueryResult["data"]["conference"];
    me: CurrentUserQueryResult["data"]["me"];
  }) => React.ReactElement;
  cartCookie?: string;
};

export const TicketsPageWrapper = ({ children, cartCookie }: Props) => {
  const code = process.env.conferenceCode;
  const language = useCurrentLanguage();
  const [isLoggedIn] = useLoginState();
  const { user: me } = useCurrentUser({
    skip: !isLoggedIn,
  });

  const { loading, error, data } = useTicketsQuery({
    variables: {
      conference: code,
      language,
    },
  });

  const hotelRooms = data?.conference.hotelRooms || [];
  const tickets = data?.conference.tickets || [];
  const conference = data?.conference;
  const router = useRouter();

  const cartContext = createCartContext({ cartCookie });
  const state = cartContext.state;

  useEffect(() => {
    let ticketsHaveBeenUpdated = false;
    if (me?.isPythonItaliaMember) {
      // If the user is a member, remove the association membership from the cart
      const selectedProducts: any[] = Object.values(
        state.selectedProducts,
      ).flat();

      for (const product of selectedProducts) {
        const productInfo = tickets.filter(
          (ticket) =>
            ticket.id === product.id && ticket.type === TicketType.Association,
        );

        if (productInfo.length === 0) {
          continue;
        }

        cartContext.removeProduct(product.id);
        ticketsHaveBeenUpdated = true;
      }

      if (ticketsHaveBeenUpdated && typeof window !== "undefined") {
        // This is an hack because the products are not correctly removed :(
        window.location.reload();
      }
    }
  }, [me]);

  useEffect(() => {
    const isHome =
      location.pathname.endsWith("tickets") ||
      location.pathname.endsWith("tickets/personal") ||
      location.pathname.endsWith("tickets/business");

    if (isHome) {
      return;
    }

    if (!isLoggedIn) {
      router.replace("/login?next=/tickets/checkout");
      return;
    }

    if (!hasSelectedAtLeastOneProduct(state)) {
      router.replace("/tickets");
      return;
    }
  }, [typeof location === "undefined" ? null : location.pathname, tickets]);

  if (error) {
    return (
      <Page>
        <Section>
          <Alert variant="alert">{error.message}</Alert>
        </Section>
      </Page>
    );
  }

  return (
    <CartContext.Provider value={cartContext}>
      <FormattedMessage id="tickets.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Page endSeparator={false}>
        {loading && (
          <Section>
            <FormattedMessage id="tickets.loading" />
          </Section>
        )}

        {!loading &&
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-ignore
          children({ tickets, hotelRooms, conference, me })}
      </Page>
    </CartContext.Provider>
  );
};
