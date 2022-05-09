/** @jsxRuntime classic */

/** @jsx jsx */
import React, { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx, Text } from "theme-ui";

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

import { useCart } from "./use-cart";
import {
  hasAnsweredTicketsQuestions,
  hasOrderInformation,
  hasSelectedAtLeastOneProduct,
} from "./utils";

type Props = {
  children: (props: {
    tickets: TicketItem[];
    hotelRooms: TicketsQueryResult["data"]["conference"]["hotelRooms"];
    conference: TicketsQueryResult["data"]["conference"];
    me: CurrentUserQueryResult["data"]["me"];
  }) => React.ReactElement;
};

export const TicketsPageWrapper: React.FC<Props> = ({ children }) => {
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

  const { state, removeProduct } = useCart();

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

        removeProduct(product.id);
        ticketsHaveBeenUpdated = true;
      }

      if (ticketsHaveBeenUpdated && typeof window !== "undefined") {
        // This is an hack because the products are not correctly removed :(
        window.location.reload();
      }
    }
  }, [me]);

  useEffect(() => {
    const isHome = location.pathname.endsWith("tickets/");

    if (isHome) {
      return;
    }

    const isReview = location.pathname.endsWith("review/");

    if (!isReview) {
      return;
    }

    if (!isLoggedIn) {
      router.replace("/login");
      return;
    }

    if (!hasSelectedAtLeastOneProduct(state)) {
      router.replace("/tickets");
      return;
    }

    if (!hasOrderInformation(state)) {
      router.replace("/information");
      return;
    }
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    if (tickets.length > 0 && !hasAnsweredTicketsQuestions(state, tickets)) {
      router.replace("/questions");
      return;
    }
  }, [typeof location === "undefined" ? null : location.pathname, tickets]);

  if (error) {
    return (
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        <Alert variant="alert">{error.message}</Alert>
      </Box>
    );
  }

  return (
    <Box mb={5}>
      <FormattedMessage id="tickets.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Box
        sx={{
          borderTop: "primary",
          pt: 5,
        }}
      >
        {loading && (
          <Box
            sx={{
              maxWidth: "container",
              mx: "auto",
              px: 3,
            }}
          >
            <Text>
              <FormattedMessage id="tickets.loading" />
            </Text>
          </Box>
        )}

        {!loading &&
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-ignore
          children({ tickets, hotelRooms, conference, me })}
      </Box>
    </Box>
  );
};
