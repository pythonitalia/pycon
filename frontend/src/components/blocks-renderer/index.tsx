import React from "react";

import { Map } from "~/components/blocks/map";
import { TextSection } from "~/components/blocks/text-section";
import { Block } from "~/types";

import { HomeIntroSection } from "../blocks/home-intro-section";
import { InformationSection } from "../blocks/information-section";
import { KeynotersSection } from "../blocks/keynotes-section";
import { SchedulePreviewSection } from "../blocks/schedule-preview-section";
import { SliderCardsSection } from "../blocks/slider-cards-section";
import { SocialsSection } from "../blocks/socials-section";
import { SpecialGuestSection } from "../blocks/special-guest-section";
import { SponsorsSection } from "../blocks/sponsors-section";

type Registry = {
  [key in Block["__typename"]]: any;
};

const REGISTRY: Registry = {
  TextSection: TextSection,
  CMSMap: Map,
  SliderCardsSection,
  HomeIntroSection,
  SchedulePreviewSection,
  KeynotersSection,
  SponsorsSection,
  SocialsSection,
  SpecialGuestSection,
  InformationSection,
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
