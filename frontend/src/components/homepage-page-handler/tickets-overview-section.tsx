import {
  CardPart,
  SliderGrid,
  MultiplePartsCard,
  Text,
  Heading,
  Spacer,
  Section,
  Container,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";

export const TicketsOverviewSection = () => {
  const cta = {
    link: "/tickets",
    label: <FormattedMessage id="ticketsOverview.buyTickets.cta" />,
  };

  const language = useCurrentLanguage();
  const moneyFormatter = new Intl.NumberFormat(language, {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0,
    minimumFractionDigits: 0,
  });

  // TODO: We should implement a specific API in our BE to return the various tiers
  // the reason we are not doing it now is because are still deciding what will be in the CMS
  // and what not

  return (
    <Section noContainer spacingSize="3xl">
      <Container>
        <Heading size="display2" className="text-center md:text-left">
          <FormattedMessage id="ticketsOverview.buyTicketsSection" />
        </Heading>
      </Container>
      <Spacer size="xl" />
      <SliderGrid background="snake" cols={3} wrap="nowrap">
        <MultiplePartsCard cta={cta}>
          <CardPart>
            <Heading size={2}>
              <FormattedMessage id="ticketsOverview.ticket.student.title" />
            </Heading>
            <Spacer size="xs" />
            <Text size={2}>
              <FormattedMessage id="ticketsOverview.ticket.student.description" />
            </Text>
          </CardPart>

          <CardPart>
            <Heading size={1}>{moneyFormatter.format(60)}</Heading>
            <Spacer size="xs" />
            <Text uppercase size={2}>
              <FormattedMessage id="ticketsOverview.flatPrice" />
            </Text>
          </CardPart>
        </MultiplePartsCard>

        <MultiplePartsCard cta={cta}>
          <CardPart>
            <Heading size={2}>
              <FormattedMessage id="ticketsOverview.ticket.personal.title" />
            </Heading>
            <Spacer size="xs" />
            <Text size={2}>
              <FormattedMessage id="ticketsOverview.ticket.personal.description" />
            </Text>
          </CardPart>

          <CardPart>
            <Heading size={1}>{moneyFormatter.format(150)}</Heading>
            <Spacer size="xs" />
            <Text uppercase size={2}>
              <FormattedMessage id="ticketsOverview.ticket.personal.fareType" />
            </Text>
          </CardPart>
        </MultiplePartsCard>

        <MultiplePartsCard cta={cta}>
          <CardPart>
            <Heading size={2}>
              <FormattedMessage id="ticketsOverview.ticket.business.title" />
            </Heading>
            <Spacer size="xs" />
            <Text size={2}>
              <FormattedMessage id="ticketsOverview.ticket.business.description" />
            </Text>
          </CardPart>

          <CardPart>
            <Heading size={1}>{moneyFormatter.format(230)}</Heading>
            <Spacer size="xs" />
            <Text uppercase size={2}>
              <FormattedMessage id="ticketsOverview.ticket.personal.fareType" />
            </Text>
          </CardPart>
        </MultiplePartsCard>
      </SliderGrid>
    </Section>
  );
};
