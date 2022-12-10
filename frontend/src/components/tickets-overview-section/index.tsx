import {
  CardPart,
  SliderGridSection,
  MultiplePartsCard,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

export const TicketsOverviewSection = () => {
  const cta = {
    link: "/tickets",
    label: <FormattedMessage id="ticketsOverview.buyTickets.cta" />,
  };

  // TODO: We should implement a specific API in our BE to return the various tiers
  // the reason we are not doing it now is because are still deciding what will be in the CMS
  // and what not

  return (
    <SliderGridSection
      background="snake"
      title={<FormattedMessage id="ticketsOverview.buyTicketsSection" />}
      cols={3}
    >
      <MultiplePartsCard cta={cta}>
        <CardPart
          title={<FormattedMessage id="ticketsOverview.ticket.student.title" />}
        >
          <Text size={2}>
            <FormattedMessage id="ticketsOverview.ticket.student.description" />
          </Text>
        </CardPart>

        <CardPart title={`€ 60`} titleSize="large">
          <Text uppercase size={2}>
            <FormattedMessage id="ticketsOverview.flatPrice" />
          </Text>
        </CardPart>
      </MultiplePartsCard>

      <MultiplePartsCard cta={cta}>
        <CardPart
          title={
            <FormattedMessage id="ticketsOverview.ticket.personal.title" />
          }
        >
          <Text size={2}>
            <FormattedMessage id="ticketsOverview.ticket.personal.description" />
          </Text>
        </CardPart>

        <CardPart title={`€ 120`} titleSize="large">
          <Text uppercase size={2}>
            Early bird
          </Text>
        </CardPart>
      </MultiplePartsCard>

      <MultiplePartsCard cta={cta}>
        <CardPart
          title={
            <FormattedMessage id="ticketsOverview.ticket.business.title" />
          }
        >
          <Text size={2}>
            <FormattedMessage id="ticketsOverview.ticket.business.description" />
          </Text>
        </CardPart>

        <CardPart title={`€ 180`} titleSize="large">
          <Text uppercase size={2}>
            Early bird
          </Text>
        </CardPart>
      </MultiplePartsCard>
    </SliderGridSection>
  );
};
