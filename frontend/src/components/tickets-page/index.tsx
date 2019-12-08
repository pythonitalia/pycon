import { useQuery } from "@apollo/react-hooks";
import { Box, Heading, Text } from "@theme-ui/components";
import React, { useContext } from "react";
import { FormattedMessage } from "react-intl";

import { ConferenceContext } from "../../context/conference";
import { useCurrentLanguage } from "../../context/language";
import {
  TicketsQuery,
  TicketsQueryVariables,
} from "../../generated/graphql-backend";
import { MetaTags } from "../meta-tags";
import { HotelForm } from "./hotel-form";
import { TicketsForm } from "./tickets-form";
import TICKETS_QUERY from "./tickets.graphql";

type Props = {
  lang: string;
};

export const TicketsPage: React.SFC<Props> = () => {
  const conferenceCode = useContext(ConferenceContext);
  const language = useCurrentLanguage();

  const { loading, error, data } = useQuery<
    TicketsQuery,
    TicketsQueryVariables
  >(TICKETS_QUERY, {
    variables: {
      conference: conferenceCode,
      language,
    },
  });

  if (error) {
    throw new Error(error.message);
  }

  const tickets = data?.conference.tickets;

  return (
    <Box>
      <FormattedMessage id="tickets.pageTitle">
        {text => <MetaTags title={text} />}
      </FormattedMessage>

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        {loading && (
          <Text>
            <FormattedMessage id="tickets.loading" />
          </Text>
        )}

        {!loading && (
          <React.Fragment>
            <Heading sx={{ mb: 3 }}>Get some tickets</Heading>
            {tickets && <TicketsForm tickets={tickets} />}
            <Heading sx={{ mb: 3 }}>Book your hotel room!</Heading>
            <HotelForm />
          </React.Fragment>
        )}
      </Box>
    </Box>
  );
};
