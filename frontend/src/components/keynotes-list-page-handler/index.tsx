import {
  Grid,
  Heading,
  Page,
  Section,
  Spacer,
  Text,
  SpeakerCard,
  Link,
  Container,
} from "@python-italia/pycon-styleguide";
import React from "react";

import { useCurrentLanguage } from "~/locale/context";
import { useKeynotesPageQuery } from "~/types";

import { createHref } from "../link";
import { MetaTags } from "../meta-tags";

export const KeynotesListPageHandler = () => {
  const language = useCurrentLanguage();
  const {
    data: {
      conference: { title, subtitle, keynotes },
    },
  } = useKeynotesPageQuery({
    variables: {
      conference: process.env.conferenceCode,
      language,
    },
  });

  return (
    <Page endSeparator={false}>
      <MetaTags title="Keynotes" />
      <Section illustration="snakeHead">
        <Heading size="display1">{title}</Heading>
      </Section>
      <Section spacingSize="xl">
        <Container size="medium" center={false} noPadding>
          <Heading size={1}>{subtitle}</Heading>
        </Container>
        <Spacer size="large" />
        <Grid cols={3} mdCols={2} equalHeight>
          {keynotes.map((keynote) => (
            <Link
              noLayout
              noHover
              href={createHref({
                path: `/keynotes/${keynote.slug}`,
                locale: language,
              })}
            >
              <SpeakerCard
                talkTitle={keynote.title}
                portraitUrl={keynote.speakers[0].participant.photo}
                speakerName={keynote.speakers
                  .map((speaker) => speaker.fullName)
                  .join(", ")}
              />
            </Link>
          ))}
        </Grid>
      </Section>
    </Page>
  );
};
