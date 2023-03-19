import {
  CardPart,
  DynamicHTMLText,
  Heading,
  MultiplePartsCard,
  Section,
  SliderGrid,
} from "@python-italia/pycon-styleguide";

import { SliderCardsSection as SliderCardsSectionType } from "~/types";

type Props = {
  cards: SliderCardsSectionType["cards"];
};

export const SliderCardsSection = ({ cards }: Props) => {
  return (
    <Section spacingSize="xl" noContainer>
      <SliderGrid cols={3}>
        {cards.map((card) => (
          <MultiplePartsCard
            cta={
              card.cta
                ? {
                    label: card.cta.label,
                    link: card.cta.link,
                  }
                : null
            }
          >
            <CardPart shrink={false} contentAlign="center">
              <Heading size={3}>{card.title}</Heading>
            </CardPart>
            <CardPart fullHeight background="milk" contentAlign="left">
              <DynamicHTMLText text={card.body} baseTextSize={2} />
            </CardPart>
          </MultiplePartsCard>
        ))}
      </SliderGrid>
    </Section>
  );
};
