import {
  CardPart,
  Container,
  Heading,
  MultiplePartsCard,
  Section,
  SliderGrid,
  Spacer,
  StyledHTMLText,
  Text,
} from "@python-italia/pycon-styleguide";

import { useMoneyFormatter } from "~/helpers/formatters";
import {
  PriceCard as PriceCardType,
  SimpleTextCard as SimpleTextCardType,
  SliderCardsSection as SliderCardsSectionType,
  Spacing,
} from "~/types";

type Props = {
  title: string;
  spacing: Spacing;
  snakeBackground: boolean;
  cards: SliderCardsSectionType["cards"];
};

const getSpacing = (spacing: Spacing) => {
  switch (spacing) {
    case Spacing.Xl:
      return "xl";
    case Spacing["3Xl"]:
      return "3xl";
  }
};

export const SliderCardsSection = ({
  title,
  cards,
  spacing,
  snakeBackground,
}: Props) => {
  return (
    <Section spacingSize={getSpacing(spacing)} noContainer>
      {title && (
        <>
          <Container>
            <Heading size="display2" className="text-center md:text-left">
              {title}
            </Heading>
          </Container>
          <Spacer size="xl" />
        </>
      )}
      <SliderGrid
        background={snakeBackground ? "snake" : "none"}
        cols={3}
        wrap={snakeBackground ? "nowrap" : "wrap"}
      >
        {cards.map((card) => {
          switch (card.__typename) {
            case "SimpleTextCard":
              return <SimpleTextCard card={card} />;
            case "PriceCard":
              return <PriceCard card={card} />;
            default:
              return null;
          }
        })}
      </SliderGrid>
    </Section>
  );
};

const SimpleTextCard = ({ card }: { card: SimpleTextCardType }) => {
  const cta = card.cta;
  return (
    <MultiplePartsCard
      cta={
        cta
          ? {
              label: cta.label,
              link: cta.link,
            }
          : null
      }
    >
      <CardPart shrink={false} contentAlign="center">
        <Heading size={3}>{card.title}</Heading>
      </CardPart>
      <CardPart fullHeight background="milk" contentAlign="left">
        <StyledHTMLText text={card.body} baseTextSize={2} />
      </CardPart>
    </MultiplePartsCard>
  );
};

const PriceCard = ({ card }: { card: PriceCardType }) => {
  const cta = card.cta;
  const moneyFormatter = useMoneyFormatter({ fractionDigits: 0 });
  return (
    <MultiplePartsCard
      cta={
        cta
          ? {
              label: cta.label,
              link: cta.link,
            }
          : null
      }
    >
      <CardPart>
        <Heading size={2}>{card.title}</Heading>
        <Spacer size="xs" />
        <StyledHTMLText text={card.body} baseTextSize={2} />
      </CardPart>

      <CardPart>
        <Heading size={1}>
          {moneyFormatter.format(parseFloat(card.price))}
        </Heading>
        <Spacer size="xs" />
        <Text uppercase size={2}>
          {card.priceTier}
        </Text>
      </CardPart>
    </MultiplePartsCard>
  );
};
