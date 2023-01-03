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
  const language = useCurrentLanguage();
  const moneyFormatter = new Intl.NumberFormat(language, {
    style: "currency",
    currency: "EUR",
  });

  const businessTicket = tickets.find(
    (ticket) => ticket.admission && ticket.type === TicketType.Business,
  );
  const personalTicket = tickets.find(
    (ticket) => ticket.admission && ticket.category !== "Tickets Student",
  );
  const membership = tickets.find(
    (ticket) => !ticket.admission && ticket.type === TicketType.Association,
  );

  const someHotelRoomsAreAvailable = hotelRooms.some((room) => !room.isSoldOut);
  const areTicketsAvailable = businessTicket && personalTicket;

  return (
    <Section containerSize="medium">
      <Heading size={1}>
        <FormattedMessage id="tickets.landing.title" />
      </Heading>
      <Spacer size="large" />

      {areTicketsAvailable && (
        <MultiplePartsCard>
          <CardPart
            icon="ticket"
            iconBackground="pink"
            title={<FormattedMessage id="tickets.landing.ticketsTitle" />}
            contentAlign="left"
          />
          <CardPart contentAlign="left" noBg>
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

      {someHotelRoomsAreAvailable && (
        <>
          <Spacer size="small" />
          <MultiplePartsCard>
            <CardPart
              icon="hotel"
              iconBackground="green"
              title={<FormattedMessage id="tickets.landing.hotelTitle" />}
              contentAlign="left"
            />
            <CardPart contentAlign="left" noBg>
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
        <CardPart
          icon="star"
          iconBackground="blue"
          title={<FormattedMessage id="tickets.landing.membershipTitle" />}
          contentAlign="left"
        />
        <CardPart contentAlign="left" noBg>
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
