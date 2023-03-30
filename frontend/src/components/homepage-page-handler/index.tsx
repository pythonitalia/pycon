import {
  Page,
  Separator,
  LayoutContent,
} from "@python-italia/pycon-styleguide";
import React, { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import { HomepageHero } from "~/components/homepage-hero";
import { MetaTags } from "~/components/meta-tags";
import { useCurrentLanguage } from "~/locale/context";
import { useIndexPageQuery } from "~/types";

import { KeynotersSection } from "../keynoters-section";
import { FollowUsSection } from "./follow-us-section";
import { IntroSection } from "./intro-section";
import { SchedulePreviewSection } from "./schedule-preview-section";
import { SpecialGuest } from "./special-guest";
import { SponsorsSection } from "./sponsors-section";
import { TicketsOverviewSection } from "./tickets-overview-section";

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
        <IntroSection conference={conference} />

        <SchedulePreviewSection days={conference.days} />

        <KeynotersSection />

        <SpecialGuest />

        <TicketsOverviewSection />

        {/* <InformationSection conference={conference} /> */}

        <SponsorsSection sponsorsByLevel={conference.sponsorsByLevel} />

        <FollowUsSection />
      </Page>
    </Fragment>
  );
};
