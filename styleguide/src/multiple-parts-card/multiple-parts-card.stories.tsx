import React from "react";
import { Text } from "../text";
import { MultiplePartsCard } from "./multiple-parts-card";
import { CardPart } from "./card-part";

export default {
  title: "Multiple Parts Card",
};

export const Primary = () => (
  <div className="p-6">
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
  </div>
);

export const CardWithContentAndOnePart = () => (
  <div className="p-6">
    <MultiplePartsCard
      cta={{
        link: "/test",
        label: "Request info",
      }}
    >
      <CardPart title="General info" titleSize="small" />
      <CardPart contentAlign="left" noBg>
        <Text size={2}>
          We are here to help you! Let us know how we can do it
        </Text>
      </CardPart>
    </MultiplePartsCard>
  </div>
);
