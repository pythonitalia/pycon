import React from "react";
import { MultiplePartsCard, CardPart } from "../multiple-parts-card";
import { SliderGridSection } from "./slider-grid-section";
import { Text } from "../text";

export const Default = () => {
  return (
    <div className="py-12">
      <SliderGridSection background="snake" title="Buy your tickets!" cols={3}>
        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart title="Student">
            <Text size={2}>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </Text>
          </CardPart>

          <CardPart title="€ 100" titleSize="large">
            <Text size={2}>flat price</Text>
          </CardPart>
        </MultiplePartsCard>

        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart title="Regular">
            <Text size={2}>
              Buying now your ticket, you can save up to the 30%
            </Text>
          </CardPart>

          <CardPart title="€ 180" titleSize="large">
            <Text size={2}>Early bird</Text>
          </CardPart>
        </MultiplePartsCard>

        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart title="Business">
            <Text size={2}>
              Buying now your ticket, you can save up to the 25%
            </Text>
          </CardPart>

          <CardPart title="€ 250" titleSize="large">
            <Text size={2}>Early bird</Text>
          </CardPart>
        </MultiplePartsCard>
      </SliderGridSection>
    </div>
  );
};

export const With2Cards = () => {
  return (
    <div className="py-12">
      <SliderGridSection background="snake" title="Buy your tickets!" cols={3}>
        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart title="Student">
            <Text size={2}>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </Text>
          </CardPart>

          <CardPart title="€ 100" titleSize="large">
            <Text size={2}>flat price</Text>
          </CardPart>
        </MultiplePartsCard>

        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart title="Regular">
            <Text size={2}>
              Buying now your ticket, you can save up to the 30%
            </Text>
          </CardPart>

          <CardPart title="€ 180" titleSize="large">
            <Text size={2}>Early bird</Text>
          </CardPart>
        </MultiplePartsCard>
      </SliderGridSection>
    </div>
  );
};

export default {
  title: "Slider Grid Section",
  component: Default,
};
