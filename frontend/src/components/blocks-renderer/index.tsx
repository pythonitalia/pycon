import React from "react";

import { getApolloClient } from "~/apollo/client";
import { Map } from "~/components/blocks/map";
import { TextSection } from "~/components/blocks/text-section";
import { Block, queryPagePreview } from "~/types";

import { CheckoutSection } from "../blocks/checkout-section";
import { HomeIntroSection } from "../blocks/home-intro-section";
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
  CMSMap: Map,
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
};

type Props = {
  blocks: Block[];
};

export const BlocksRenderer = ({ blocks }: Props) => {
  const { isPreview, previewBlocks } = usePagePreview();
  console.log("isPreview", isPreview);
  return (
    <>
      {(previewBlocks || blocks).map((block) => {
        const Component = REGISTRY[block.__typename];
        if (!Component) {
          return <div>Invalid component: {block.__typename}</div>;
        }
        return <Component key={block.id} {...block} />;
      })}
    </>
  );
};

export const blocksDataFetching = (client, blocks, language) => {
  const promises = [];

  for (const block of blocks) {
    const component = REGISTRY[block.__typename];
    const dataFetching = component.dataFetching;

    if (dataFetching) {
      promises.push(...dataFetching(client, language));
    }
  }

  return Promise.all(promises);
};

const usePagePreview = () => {
  const [previewState, setPreviewState] = React.useState({
    content_type: "",
    token: "",
  });
  const [previewBlocks, setPreviewBlocks] = React.useState<Block[]>([]);

  React.useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    console.log(
      "window.location.search",
      params.get("content_type"),
      params.get("token"),
    );
    // setIsPreview(params.has("content_type") && params.has("token"));
    setPreviewState({
      content_type: params.get("content_type") || "",
      token: params.get("token") || "",
    });
  }, []);

  React.useEffect(() => {
    if (!previewState.token) {
      return;
    }

    const fetchData = async () => {
      const apolloClient = getApolloClient();
      const response = await queryPagePreview(apolloClient, {
        contentType: previewState.content_type,
        token: previewState.token,
      });
      setPreviewBlocks(response.data.pagePreview.body);
      console.log("data", response);
    };

    fetchData();
  }, [previewState]);

  return { isPreview: previewState.token !== "", previewBlocks };
};
