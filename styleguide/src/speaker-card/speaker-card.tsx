import React from "react";
import { Heading } from "../heading";
import { Text } from "../text";
import { CardPart, MultiplePartsCard } from "../multiple-parts-card";
import { Spacer } from "../spacer";

type Props = {
  talkTitle?: string;
  talkInfoLeft?: string;
  talkInfoRight?: string;
  portraitUrl?: string;
  speakerName?: string;
};

export const SpeakerCard = ({
  portraitUrl,
  talkTitle,
  speakerName,
  talkInfoRight,
  talkInfoLeft,
}: Props) => {
  return (
    <MultiplePartsCard>
      <CardPart shrink={false} size="none">
        <img
          style={{
            objectFit: "cover",
          }}
          className="w-full aspect-[1/0.74]"
          src={portraitUrl}
        />
      </CardPart>
      <CardPart fullHeight contentAlign="left">
        {(talkInfoRight || talkInfoLeft) && (
          <>
            <div className="flex justify-between">
              {talkInfoLeft ? (
                <Text size="label3" weight="strong" uppercase>
                  {talkInfoLeft}
                </Text>
              ) : (
                <span></span>
              )}
              {talkInfoRight && (
                <Text color="grey-500" size="label4" align="right">
                  {talkInfoRight}
                </Text>
              )}
            </div>
            <Spacer size="xs" />
          </>
        )}
        <Heading size={4}>{talkTitle}</Heading>
      </CardPart>
      <CardPart shrink={false} background="milk" contentAlign="left">
        <Heading size={6}>{speakerName}</Heading>
      </CardPart>
    </MultiplePartsCard>
  );
};
