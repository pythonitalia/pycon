import {
  Button,
  CardPart,
  Heading,
  MultiplePartsCard,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { compile } from "~/helpers/markdown";
import { useCurrentLanguage } from "~/locale/context";
import { TicketItem, TicketType, TicketsQueryResult } from "~/types";

import { createHref } from "../link";

type Props = {
  tickets: TicketItem[];
  hotelRooms: TicketsQueryResult["data"]["conference"]["hotelRooms"];
};

export const AvailableProductsLandingSection = ({ tickets }: Props) => {
  const language = useCurrentLanguage();
  const membership = tickets.find(
    (ticket) => !ticket.admission && ticket.type === TicketType.Association,
  );

  const socialEvents = tickets.filter(
    (product) => product.type === TicketType.SocialEvent,
  );

  return (
    <Section containerSize="2md">
      <Heading size={1}>
        <FormattedMessage id="tickets.landing.title" />
      </Heading>
      <Spacer size="large" />

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
              <Spacer size="2md" />
              <Button
                size="small"
                href={createHref({
                  path: "/social-events",
                  locale: language,
                })}
              >
                <FormattedMessage id="tickets.buyNow" />
              </Button>
            </CardPart>
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
      </MultiplePartsCard>
    </Section>
  );
};
