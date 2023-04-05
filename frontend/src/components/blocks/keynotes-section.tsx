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

import { useCurrentLanguage } from "~/locale/context";
import { Cta, useKeynotesSectionQuery } from "~/types";

import { createHref } from "../link";

type Props = {
  title: string;
  cta: Cta | null;
};
export const KeynotersSection = ({ title, cta }: Props) => {
  const language = useCurrentLanguage();
  const { data } = useKeynotesSectionQuery({
    variables: {
      code: process.env.conferenceCode,
      language,
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
      <SliderGrid mdCols={2} cols={3} justifyContent="center" wrap="wrap">
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
              portraitUrl={keynote.speakers[0].participant.photo}
              speakerName={keynote.speakers[0].fullName}
            />
          </Link>
        ))}
      </SliderGrid>

      {cta && (
        <Container>
          <Spacer size="2xl" />
          <VerticalStack alignItems="center">
            <Button
              href={createHref({
                path: cta.link,
                locale: language,
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
