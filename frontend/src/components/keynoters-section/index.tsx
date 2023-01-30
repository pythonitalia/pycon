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
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { useKeynotesSectionQuery } from "~/types";

import { createHref } from "../link";

export const KeynotersSection = () => {
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
    <Section noContainer spacingSize="3xl" background="caramel">
      <Container>
        <Heading size="display2" align="center">
          Keynotes
        </Heading>
        <Spacer size="2xl" />
      </Container>
      <SliderGrid mdCols={2} cols={3} justifyContent="center" wrap="wrap">
        {keynotes.map((keynote) => (
          <Link
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

      <Container>
        <Spacer size="2xl" />
        <VerticalStack alignItems="center">
          <Button
            href={createHref({
              path: "/tickets",
              locale: language,
            })}
          >
            <FormattedMessage id="ticketsOverview.buyTicketsSection" />
          </Button>
        </VerticalStack>
      </Container>
    </Section>
  );
};
