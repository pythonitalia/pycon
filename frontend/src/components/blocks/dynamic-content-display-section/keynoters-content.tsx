import { Section } from "@python-italia/pycon-styleguide";
import React from "react";
import { KeynotesSpeakersCards } from "~/components/keynotes-speakers-cards";
import { useCurrentLanguage } from "~/locale/context";
import { useKeynotesSectionQuery } from "~/types";

export const KeynotersContent = () => {
  const language = useCurrentLanguage();
  const { data } = useKeynotesSectionQuery({
    variables: {
      code: process.env.conferenceCode,
      language,
    },
  });
  return (
    <Section noContainer>
      <KeynotesSpeakersCards
        keynotes={data.conference.keynotes}
        justifyContent="left"
      />
    </Section>
  );
};
