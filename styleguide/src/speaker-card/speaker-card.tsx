import React from "react";
import { Heading } from "../heading";
import { CardPart, MultiplePartsCard } from "../multiple-parts-card";

type Props = {
  talkTitle?: string;
  portraitUrl?: string;
  speakerName?: string;
};

export const SpeakerCard = ({ portraitUrl, talkTitle, speakerName }: Props) => {
  return (
    <MultiplePartsCard>
      <CardPart shrink={false} size="none">
        <img
          style={{
            objectFit: "cover",
          }}
          className="w-full aspect-square"
          src={portraitUrl}
        />
      </CardPart>
      <CardPart fullHeight contentAlign="left">
        <Heading size={4}>{talkTitle}</Heading>
      </CardPart>
      <CardPart shrink={false} background="milk" contentAlign="left">
        <Heading size={6}>{speakerName}</Heading>
      </CardPart>
    </MultiplePartsCard>
  );
};
