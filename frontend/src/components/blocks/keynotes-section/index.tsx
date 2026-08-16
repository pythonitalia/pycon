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
import {
  type Cta,
  queryKeynotesSection,
  useKeynotesSectionQuery,
} from "~/types";

import { KeynotesSpeakersCards } from "~/components/keynotes-speakers-cards";
import { createHref } from "../../link";

type Props = {
  title: string;
  cta: Cta | null;
};
export const KeynotersSection = ({ title, cta }: Props) => {
  const { data } = useKeynotesSectionQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });

  if (!data) {
    return null;
  }

  const {
    conference: { keynotes },
  } = data;

  if (keynotes.length === 0) {
    return null;
  }

  return (
    <Section noContainer spacingSize="3xl" background="yellow">
      <Container>
        <Heading size="display2" align="center">
          {title}
        </Heading>
        <Spacer size="2xl" />
      </Container>

      <KeynotesSpeakersCards keynotes={keynotes} />

      {cta && (
        <Container>
          <Spacer size="2xl" />
          <VerticalStack alignItems="center">
            <Button
              href={createHref({
                path: cta.link,
              })}
            >
              {cta.label}
            </Button>
          </VerticalStack>
        </Container>
      )}
    </Section>
  );
};

KeynotersSection.dataFetching = (client) => {
  return [
    queryKeynotesSection(client, {
      code: process.env.conferenceCode,
    }),
  ];
};
