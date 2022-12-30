import React from "react";
import { CardPart, MultiplePartsCard } from "../multiple-parts-card";
import { GridSection } from "./grid-section";
import { Text } from "../text";

export const Primary = ({ showSnake, items = 2, cols = 2 }) => {
  return (
    <div className="py-12">
      <GridSection showSnake={showSnake} title="Buy tickets" cols={cols}>
        {Array(items)
          .fill(null, 0)
          .map((_, i) => (
            <MultiplePartsCard
              cta={{
                label: "Buy tickets",
                link: "/tickets/business/",
              }}
            >
              <CardPart title="Student">
                <Text size={2}>Body</Text>
              </CardPart>
            </MultiplePartsCard>
          ))}
      </GridSection>
    </div>
  );
};

export default {
  title: "Grid Section",
  argTypes: {
    items: {
      defaultValue: 2,
      control: {
        type: "number",
      },
    },
    cols: {
      defaultValue: 2,
      control: {
        type: "number",
      },
    },
    showSnake: {
      defaultValue: false,
      control: {
        type: "boolean",
      },
    },
  },
};
