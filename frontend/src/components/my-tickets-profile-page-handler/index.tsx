import { Grid, Heading, Page, Section } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { useMyProfileWithTicketsQuery } from "~/types";

import { NoTickets } from "./no-tickets";
import { TicketCard } from "./ticket-card";

export const MyTicketsProfilePageHandler = () => {
  const language = useCurrentLanguage();
  const {
    data: {
      me: { tickets, email },
    },
  } = useMyProfileWithTicketsQuery({
    variables: {
      conference: process.env.conferenceCode,
      language: language,
    },
  });

  return (
    <Page endSeparator={false}>
      <Section background="pink">
        <Heading size="display2">
          <FormattedMessage id="profile.myTickets" />
        </Heading>
      </Section>
      {tickets.length > 0 && (
        <Section>
          <Grid cols={3} equalHeight>
            {tickets.map((ticket) => (
              <TicketCard key={ticket.id} ticket={ticket} />
            ))}
          </Grid>
        </Section>
      )}
      {tickets.length === 0 && (
        <Section>
          <NoTickets email={email} />
        </Section>
      )}
    </Page>
  );
};
