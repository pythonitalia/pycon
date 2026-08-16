import { Section } from "@python-italia/pycon-styleguide";
import React from "react";
import { KeynotesSpeakersCards } from "~/components/keynotes-speakers-cards";
import { useKeynotesSectionQuery } from "~/types";

export const KeynotersContent = () => {
  const { data } = useKeynotesSectionQuery({
    variables: {
      code: process.env.conferenceCode,
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
