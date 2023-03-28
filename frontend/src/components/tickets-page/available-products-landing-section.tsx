import {
  MultiplePartsCard,
  CardPart,
  Spacer,
  Section,
  Heading,
  Grid,
  Text,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useMoneyFormatter } from "~/helpers/formatters";
import { compile } from "~/helpers/markdown";
import { useCurrentLanguage } from "~/locale/context";
import { TicketsQueryResult, TicketType, TicketItem } from "~/types";

type Props = {
  tickets: TicketItem[];
  hotelRooms: TicketsQueryResult["data"]["conference"]["hotelRooms"];
};

export const AvailableProductsLandingSection = ({
  hotelRooms,
  tickets,
}: Props) => {
  const moneyFormatter = useMoneyFormatter();

  const businessTicket = tickets.find(
    (ticket) => ticket.admission && ticket.type === TicketType.Business,
  );
  const personalTicket = tickets.find(
    (ticket) =>
      ticket.admission && ticket.categoryInternalName === "Personal Tickets",
  );
  const membership = tickets.find(
    (ticket) => !ticket.admission && ticket.type === TicketType.Association,
  );

  const socialEvents = tickets.filter(
    (product) => product.type === TicketType.SocialEvent,
  );

  const someHotelRoomsAreAvailable = hotelRooms.some((room) => !room.isSoldOut);
  const areTicketsAvailable = businessTicket && personalTicket;

  return (
    <Section containerSize="2md">
      <Heading size={1}>
        <FormattedMessage id="tickets.landing.title" />
      </Heading>
      <Spacer size="large" />

      {areTicketsAvailable && (
        <MultiplePartsCard>
          <CardPart icon="tickets" iconBackground="pink" contentAlign="left">
            <Heading size={2}>
              <FormattedMessage id="tickets.landing.ticketsTitle" />
            </Heading>
          </CardPart>
          <CardPart contentAlign="left" background="milk">
            <Text size={2}>
              <FormattedMessage id="tickets.landing.ticketsCopy" />
            </Text>
          </CardPart>
          <Grid cols={2} gap="none" divide={true}>
            <CardPart contentAlign="left">
              <Text size="label3">{personalTicket.name}</Text>
              <Heading size={2}>
                {moneyFormatter.format(Number(personalTicket.defaultPrice))}
              </Heading>
            </CardPart>
            <CardPart contentAlign="left">
              <Text size="label3">{businessTicket.name}</Text>
              <Heading size={2}>
                {moneyFormatter.format(Number(businessTicket.defaultPrice))}
              </Heading>
            </CardPart>
          </Grid>
        </MultiplePartsCard>
      )}

      {socialEvents.length > 0 && (
        <>
          <Spacer size="small" />
          <MultiplePartsCard>
            <CardPart icon="drink" iconBackground="coral" contentAlign="left">
              <Heading size={2}>
                <FormattedMessage id="tickets.landing.socialEvents.title" />
              </Heading>
            </CardPart>
            <CardPart contentAlign="left" background="milk">
              <Text size={2}>
                <FormattedMessage id="tickets.landing.socialEvents.copy" />
              </Text>
            </CardPart>
          </MultiplePartsCard>
        </>
      )}

      {someHotelRoomsAreAvailable && (
        <>
          <Spacer size="small" />
          <MultiplePartsCard>
            <CardPart icon="hotel" iconBackground="green" contentAlign="left">
              <Heading size={2}>
                <FormattedMessage id="tickets.landing.hotelTitle" />
              </Heading>
            </CardPart>
            <CardPart contentAlign="left" background="milk">
              <Text size={2}>
                <FormattedMessage id="tickets.landing.hotelCopy" />
              </Text>
            </CardPart>
            <Grid cols={3} gap="none" divide={true}>
              {[...hotelRooms]
                .sort((a, b) => Number(a.price) - Number(b.price))
                .map((room) => (
                  <CardPart key={room.id} contentAlign="left">
                    <Text size="label3">{room.name}</Text>
                    <Heading size={2}>
                      {moneyFormatter.format(Number(room.price))}
                    </Heading>
                  </CardPart>
                ))}
            </Grid>
          </MultiplePartsCard>
        </>
      )}

      <Spacer size="small" />
      <MultiplePartsCard>
        <CardPart icon="star" iconBackground="blue" contentAlign="left">
          <Heading size={2}>
            <FormattedMessage id="tickets.landing.membershipTitle" />
          </Heading>
        </CardPart>
        <CardPart contentAlign="left" background="milk">
          <Text size={2}>{compile(membership.description).tree}</Text>
        </CardPart>
        <CardPart contentAlign="left">
          <FormattedMessage id="tickets.landing.membership.cta" />
          <Heading size={2}>{moneyFormatter.format(10)}</Heading>
        </CardPart>
      </MultiplePartsCard>
    </Section>
  );
};
