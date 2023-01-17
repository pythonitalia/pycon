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
      conference: { title, subtitle, description, keynotes },
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
        <Container noPadding center={false} size="small">
          <Heading size="display1">{title}</Heading>
          <Spacer size="medium" />
          <Text weight="strong" as="p" size={1}>
            {subtitle}
          </Text>
          <Text as="p" size={2} color="grey-900">
            {description}
          </Text>
        </Container>
      </Section>
      <Section>
        <Grid cols={3} mdCols={2}>
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
                portraitUrl={keynote.speakers[0].photo}
                speakerName={keynote.speakers
                  .map((speaker) => speaker.name)
                  .join(", ")}
              />
            </Link>
          ))}
        </Grid>
      </Section>
    </Page>
  );
};
