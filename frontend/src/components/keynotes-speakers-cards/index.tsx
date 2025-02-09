import {
  Button,
  Container,
  Heading,
  Link,
  Section,
  SliderGrid,
  Spacer,
  SpeakerCard,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import type { KeynotesSectionQueryResult } from "~/types";
import { createHref } from "../link";

export const KeynotesSpeakersCards = ({
  keynotes,
  justifyContent = "center",
}: {
  keynotes: KeynotesSectionQueryResult["data"]["conference"]["keynotes"];
  justifyContent?: "left" | "center" | "right";
}) => {
  const language = useCurrentLanguage();
  const englishText = useTranslatedMessage("global.english");
  const dateFormatter = new Intl.DateTimeFormat(language, {
    day: "numeric",
    month: "long",
  });

  return (
    <SliderGrid mdCols={2} cols={3} justifyContent={justifyContent} wrap="wrap">
      {keynotes.map((keynote) => (
        <Link
          key={keynote.id}
          noHover
          href={createHref({
            path: `/keynotes/${keynote.slug}`,
            locale: language,
          })}
        >
          <SpeakerCard
            talkTitle={keynote.title}
            talkInfoLeft={
              keynote.start
                ? dateFormatter.format(new Date(keynote.start))
                : null
            }
            talkInfoRight={englishText}
            portraitUrl={keynote.speakers[0].participant.photo}
            speakerName={keynote.speakers[0].fullName}
          />
        </Link>
      ))}
    </SliderGrid>
  );
};
