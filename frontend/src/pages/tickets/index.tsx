import {
  CardPart,
  MultiplePartsCard,
  Text,
  Heading,
  Container,
  Spacer,
  Grid,
  Section,
} from "@python-italia/pycon-styleguide";
import { SnakeHead } from "@python-italia/pycon-styleguide/illustrations";
import { FormattedMessage } from "react-intl";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { AvailableProductsLandingSection } from "~/components/tickets-page/available-products-landing-section";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryTickets } from "~/types";

export const TicketsPage = () => {
  return (
    <TicketsPageWrapper>
      {({ hotelRooms, tickets }) => (
        <div>
          <Container>
            <Spacer size="xl" />
            <Heading size="display1">
              <FormattedMessage id="tickets.buyTickets" />
            </Heading>
            <Spacer size="large" />
            <Heading size={1}>
              <FormattedMessage id="tickets.buyTicketsSubtitle" />
            </Heading>
          </Container>
          <Section>
            <SnakeHead className="relative ml-auto w-32 lg:w-52 mr-6 md:mr-12 -mt-36 md:-mt-24 lg:-mt-44 hidden md:block" />
            <Grid cols={2} equalHeight>
              <MultiplePartsCard
                cta={{
                  label: <FormattedMessage id="tickets.buyTicketsCta" />,
                  link: "/tickets/personal/",
                }}
              >
                <CardPart>
                  <Heading size={2}>
                    <FormattedMessage id="tickets.personal.title" />
                  </Heading>
                  <Spacer size="xs" />
                  <Text size={2}>
                    <FormattedMessage id="tickets.personal.description" />
                  </Text>
                </CardPart>
              </MultiplePartsCard>

              <MultiplePartsCard
                cta={{
                  label: <FormattedMessage id="tickets.buyTicketsCta" />,
                  link: "/tickets/business/",
                }}
              >
                <CardPart>
                  <Heading size={2}>
                    <FormattedMessage id="tickets.business.title" />
                  </Heading>
                  <Spacer size="xs" />
                  <Text size={2}>
                    <FormattedMessage id="tickets.business.description" />
                  </Text>
                </CardPart>
              </MultiplePartsCard>
            </Grid>
          </Section>
          <AvailableProductsLandingSection
            tickets={tickets}
            hotelRooms={hotelRooms}
          />
        </div>
      )}
    </TicketsPageWrapper>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryTickets(client, {
      conference: process.env.conferenceCode,
      language: "it",
    }),
    queryTickets(client, {
      conference: process.env.conferenceCode,
      language: "en",
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default TicketsPage;
