import React from "react";
import { MultiplePartsCard, CardPart } from "../multiple-parts-card";
import { SliderGrid } from "./slider-grid";
import { Text } from "../text";
import { Heading } from "../heading";
import { Spacer } from "../spacer";

export const Default = () => {
  return (
    <div className="py-12">
      <SliderGrid background="snake" title="Buy your tickets!" cols={3}>
        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart>
            <Heading size={2}>Student</Heading>
            <Spacer size="xs" />
            <Text size={2}>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </Text>
          </CardPart>

          <CardPart>
            <Heading size={1}>€ 100</Heading>
            <Spacer size="xs" />
            <Text size={2}>flat price</Text>
          </CardPart>
        </MultiplePartsCard>

        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart>
            <Heading size={2}>Regular</Heading>
            <Spacer size="xs" />
            <Text size={2}>
              Buying now your ticket, you can save up to the 30%
            </Text>
          </CardPart>

          <CardPart>
            <Heading size={1}>€ 180</Heading>
            <Spacer size="xs" />
            <Text size={2}>Early bird</Text>
          </CardPart>
        </MultiplePartsCard>

        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart>
            <Heading size={2}>Business</Heading>
            <Spacer size="xs" />
            <Text size={2}>
              Buying now your ticket, you can save up to the 25%
            </Text>
          </CardPart>

          <CardPart>
            <Heading size={1}>€ 250</Heading>
            <Spacer size="xs" />
            <Text size={2}>Early bird</Text>
          </CardPart>
        </MultiplePartsCard>
      </SliderGrid>
    </div>
  );
};

export const DynamicCards = ({ cols, items }) => {
  return (
    <div className="py-12">
      <SliderGrid background="snake" title="Buy your tickets!" cols={cols}>
        {Array(items)
          .fill(0)
          .map((_, index) => (
            <MultiplePartsCard
              key={index}
              cta={{
                link: "/test",
                label: "Buy tickets",
              }}
            >
              <CardPart>
                <Heading size={2}>Student</Heading>
                <Spacer size="xs" />
                <Text size={2}>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                </Text>
              </CardPart>

              <CardPart>
                <Heading size={1}>€ 100</Heading>
                <Spacer size="xs" />
                <Text size={2}>flat price</Text>
              </CardPart>
            </MultiplePartsCard>
          ))}
      </SliderGrid>
    </div>
  );
};
DynamicCards.argTypes = {
  cols: {
    defaultValue: 2,
    control: {
      type: "number",
    },
  },
  items: {
    defaultValue: 2,
    control: {
      type: "number",
    },
  },
};

export default {
  title: "Slider Grid Section",
  component: Default,
};
