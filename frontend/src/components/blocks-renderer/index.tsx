import React from "react";

import { MapBlock } from "~/components/blocks/map";
import { TextSection } from "~/components/blocks/text-section";
import { Block } from "~/types";

import { CheckoutSection } from "../blocks/checkout-section";
import { HomeIntroSection } from "../blocks/home-intro-section";
import { HomepageHero } from "../blocks/homepage-hero";
import { InformationSection } from "../blocks/information-section";
import { KeynotersSection } from "../blocks/keynotes-section";
import { LiveStreamingSection } from "../blocks/live-streaming-section";
import { NewsGridSection } from "../blocks/news-grid-section";
import { SchedulePreviewSection } from "../blocks/schedule-preview-section";
import { SliderCardsSection } from "../blocks/slider-cards-section";
import { SocialsSection } from "../blocks/socials-section";
import { SpecialGuestSection } from "../blocks/special-guest-section";
import { SponsorsSection } from "../blocks/sponsors-section";

type Registry = {
  [key in Block["__typename"]]: any;
};

const REGISTRY: Registry = {
  TextSection,
  CMSMap: MapBlock,
  SliderCardsSection,
  HomeIntroSection,
  SchedulePreviewSection,
  KeynotersSection,
  SponsorsSection,
  SocialsSection,
  SpecialGuestSection,
  InformationSection,
  NewsGridSection,
  CheckoutSection,
  LiveStreamingSection,
  HomepageHero,
};

type Props = {
  blocks: Block[];
  blocksProps: any;
};

export const BlocksRenderer = ({ blocks, blocksProps }: Props) => {
  return (
    <>
      {blocks.map((block) => {
        const Component = REGISTRY[block.__typename];
        if (!Component) {
          return (
            <div key={block.id}>Invalid component: {block.__typename}</div>
          );
        }
        return (
          <Component {...block} {...blocksProps[block.id]} key={block.id} />
        );
      })}
    </>
  );
};

export const blocksDataFetching = (client, blocks, language) => {
  const promises = [];
  let staticProps = {};

  for (const block of blocks) {
    const component = REGISTRY[block.__typename];

    if (!component) {
      return {};
    }

    const dataFetching = component.dataFetching;
    if (dataFetching) {
      promises.push(...dataFetching(client, language));
    }

    const getStaticProps = component.getStaticProps;
    if (getStaticProps) {
      staticProps = {
        ...staticProps,
        [block.id]: getStaticProps(block),
      };
    }
  }

  return {
    dataFetching: Promise.all(promises),
    staticProps,
  };
};
