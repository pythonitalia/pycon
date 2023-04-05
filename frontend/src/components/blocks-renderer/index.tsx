import React from "react";

import { Map } from "~/components/blocks/map";
import { TextSection } from "~/components/blocks/text-section";
import { Block } from "~/types";

import { SliderCardsSection } from "../blocks/slider-cards-section";

type Registry = {
  [key in Block["__typename"]]: any;
};

const REGISTRY: Registry = {
  TextSection: TextSection,
  CMSMap: Map,
  SliderCardsSection,
};

type Props = {
  blocks: Block[];
};

export const BlocksRenderer = ({ blocks }: Props) => {
  return (
    <>
      {blocks.map((block) => {
        const Component = REGISTRY[block.__typename];
        if (!Component) {
          return <div>Invalid component: {block.__typename}</div>;
        }
        return <Component key={block.id} {...block} />;
      })}
    </>
  );
};
