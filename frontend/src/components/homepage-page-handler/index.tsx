import {
  Text,
  Heading,
  Page,
  Spacer,
  Button,
  Section,
  Countdown,
  VerticalStack,
  SocialLinks,
  Separator,
  LayoutContent,
} from "@python-italia/pycon-styleguide";
import { parseISO } from "date-fns";
import React, { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import { HomepageHero } from "~/components/homepage-hero";
import { MetaTags } from "~/components/meta-tags";
import { NewsletterSection } from "~/components/newsletter";
import { SponsorsSection } from "~/components/sponsors-section";
import { TicketsOverviewSection } from "~/components/tickets-overview-section/index";
import { useCurrentLanguage } from "~/locale/context";
import {
  IndexPageQuery,
  queryIndexPage,
  queryKeynotesSection,
  queryMapWithLink,
  useIndexPageQuery,
} from "~/types";

import { Hills } from "./hills";

type Props = {
  cycle: "day" | "night";
};

export const HomePagePageHandler = ({ cycle }: Props) => {
  const language = useCurrentLanguage();
  const {
    data: { conference },
  } = useIndexPageQuery({
    variables: {
      code: process.env.conferenceCode,
      language,
    },
  });

  return (
    <Fragment>
      <FormattedMessage id="home.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>
      <HomepageHero cycle={cycle} />
      <LayoutContent showUntil="desktop">
        <Separator />
      </LayoutContent>

      <Page startSeparator={false}>
        <Section
          background="coral"
          spacingSize="xl"
          illustration="snakeLongNeck"
        >
          <Text uppercase size={1} weight="strong">
            {conference.introPretitle}
          </Text>
          <Spacer size="xl" />

          <Heading size="display1">{conference.introTitle}</Heading>

          <LayoutContent showFrom="desktop">
            <Spacer size="xl" />
          </LayoutContent>
        </Section>

        <TicketsOverviewSection />

        <Section spacingSize="3xl" containerSize="medium" background="yellow">
          <VerticalStack alignItems="center">
            <Heading size="display2">
              {conference.homepageCountdownSectionTitle}
            </Heading>
            <Spacer size="large" />
            <Text align="center" size={1}>
              {conference.homepageCountdownSectionText}
            </Text>
            <Spacer size="large" />

            <Countdown
              background="cream"
              deadline={parseISO(conference.votingDeadline.end)}
            />
            <Spacer size="xl" />

            <Button
              href={conference.homepageCountdownSectionCTALink}
              role="primary"
            >
              {conference.homepageCountdownSectionCTAText}
            </Button>
          </VerticalStack>
        </Section>

        {conference.sponsorsByLevel.length > 0 && (
          <Section spacingSize="3xl">
            <Heading size="display2">Sponsors</Heading>
            <Spacer size="large" />
            <SponsorsSection sponsorsByLevel={conference.sponsorsByLevel} />
          </Section>
        )}

        <div
          style={{
            backgroundColor: "#151C28",
            marginBottom: "-3px",
          }}
        >
          <Section spacingSize="3xl">
            <VerticalStack alignItems="center">
              <Text weight="strong" uppercase color="milk" size="label2">
                <FormattedMessage id="homepage.followUs" />
              </Text>
              <Spacer size="medium" />

              <SocialLinks
                color="cream"
                hoverColor="green"
                socials={[
                  {
                    icon: "twitter",
                    link: "https://twitter.com/pyconit",
                    rel: "me",
                  },
                  {
                    icon: "facebook",
                    link: "https://www.facebook.com/pythonitalia",
                    rel: "me",
                  },
                  {
                    icon: "instagram",
                    link: "https://www.instagram.com/python.it",
                    rel: "me",
                  },
                  {
                    icon: "linkedin",
                    link: "https://www.linkedin.com/company/pycon-italia",
                    rel: "me",
                  },
                  {
                    icon: "mastodon",
                    link: "https://social.python.it/@pycon",
                    rel: "me",
                  },
                ]}
              />
              <Spacer size="xl" />

              <Heading align="center" color="white" size="display1" fluid>
                #PyConIT2023
              </Heading>
            </VerticalStack>
          </Section>
          <Hills />
        </div>
      </Page>
    </Fragment>
  );
};
