import {
  Button,
  Container,
  Grid,
  Heading,
  Link,
  Page,
  Section,
  Spacer,
  SpeakerCard,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
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
  const englishText = useTranslatedMessage("global.english");
  const dateFormatter = new Intl.DateTimeFormat(language, {
    day: "numeric",
    month: "long",
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
                talkInfoLeft={
                  keynote.start
                    ? dateFormatter.format(new Date(keynote.start))
                    : null
                }
                talkInfoRight={englishText}
                speakerName={keynote.speakers
                  .map((speaker) => speaker.participant.fullname)
                  .join(", ")}
              />
            </Link>
          ))}
        </Grid>
        <Spacer size="large" />
        <VerticalStack alignItems="center">
          <Button
            variant="secondary"
            href={createHref({
              path: "/schedule",
              locale: language,
            })}
          >
            <FormattedMessage id="homepage.schedulePreviewSection.goToSchedule" />
          </Button>
        </VerticalStack>
      </Section>
    </Page>
  );
};
