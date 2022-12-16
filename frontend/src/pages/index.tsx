/** @jsxRuntime classic */

/** @jsx jsx */
import {
  Text,
  Heading,
  SplitSection,
  SectionsWrapper,
  Marquee,
  Spacer,
  Button,
  Section,
  SnakeCountdown,
  Separator,
} from "@python-italia/pycon-styleguide";
import {
  Cathedral,
  Snake2,
} from "@python-italia/pycon-styleguide/illustrations";
import { parseISO } from "date-fns";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { HomepageHero } from "~/components/homepage-hero";
import { MetaTags } from "~/components/meta-tags";
import { NewsletterSection } from "~/components/newsletter";
import { SponsorsSection } from "~/components/sponsors-section";
import { TicketsOverviewSection } from "~/components/tickets-overview-section/index";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import {
  IndexPageQuery,
  queryIndexPage,
  queryKeynotesSection,
  queryMapWithLink,
  useIndexPageQuery,
} from "~/types";

const getDeadlinesTableData = (conference: IndexPageQuery["conference"]) => {
  const deadlines: IndexPageQuery["conference"]["cfpDeadline"][] = [];

  if (conference.cfpDeadline) {
    deadlines.push(conference.cfpDeadline);
  }

  if (conference.grantsDeadline) {
    deadlines.push(conference.grantsDeadline);
  }

  if (conference.votingDeadline) {
    deadlines.push(conference.votingDeadline);
  }

  return deadlines;
};

export const HomePage = () => {
  const language = useCurrentLanguage();
  const {
    data: { conference, blogPosts },
  } = useIndexPageQuery({
    variables: {
      code: process.env.conferenceCode,
      language,
    },
  });

  const comingUpDeadlines = getDeadlinesTableData(conference);
  console.log("conference.cfpDeadline", conference.cfpDeadline.end);

  return (
    <Fragment>
      <FormattedMessage id="home.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>
      <HomepageHero hideBuyTickets={true} />
      <Separator />
      <Marquee speed="slow" separator="/">
        {conference.marquee}
      </Marquee>
      <SectionsWrapper>
        <Section>
          <Heading size="display1">{conference.introTitle}</Heading>
        </Section>

        <TicketsOverviewSection />

        <SplitSection
          sideContent={
            <SnakeCountdown
              snakeLookingAt="right"
              deadline={parseISO(conference.cfpDeadline.end)}
            />
          }
          invert
          sideContentType="other"
          hideSideContentOnMobile
          spacing="larger-content"
          title={conference.homepageCountdownSectionTitle}
        >
          <Spacer size="medium" />
          <Heading size={2}>
            {conference.homepageCountdownSectionSubtitle}
          </Heading>
          <Spacer size="medium" />
          <SnakeCountdown
            deadline={parseISO(conference.cfpDeadline.end)}
            className="lg:hidden"
          />
          <Spacer size="medium" />
          <Text size={1}>{conference.homepageCountdownSectionText}</Text>
          <Spacer size="large" />
          <Button
            linkTo={conference.homepageCountdownSectionCTALink}
            role="secondary"
          >
            {conference.homepageCountdownSectionCTAText}
          </Button>
        </SplitSection>

        <SplitSection
          sideContent={<Snake2 />}
          sideContentBackground={Snake2.backgroundColor}
          invert
          title={<FormattedMessage id="home.grants.title" />}
        >
          <Text size={1}>
            <FormattedMessage id="home.grants.description" />
          </Text>
          <Spacer size="large" />
          <Button linkTo="/grants-info" role="secondary">
            <FormattedMessage id="home.grants.cta" />
          </Button>
        </SplitSection>

        {conference.sponsorsByLevel.length > 0 && (
          <Section>
            <Heading size="display2">Sponsors</Heading>
            <Spacer size="large" />
            <SponsorsSection sponsorsByLevel={conference.sponsorsByLevel} />
          </Section>
        )}

        <SplitSection
          sideContent={<Cathedral />}
          sideContentBackground={Cathedral.backgroundColor}
          title={<FormattedMessage id="newsletter.header" />}
        >
          <NewsletterSection />
        </SplitSection>
      </SectionsWrapper>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryKeynotesSection(client, {
      code: process.env.conferenceCode,
      language: locale,
    }),
    queryMapWithLink(client, {
      code: process.env.conferenceCode,
    }),
    queryIndexPage(client, {
      language: locale,
      code: process.env.conferenceCode,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default HomePage;
