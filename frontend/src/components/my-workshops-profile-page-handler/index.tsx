import { Heading, Page, Section } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useMyProfileWithBookedWorkshopsQuery } from "~/types";

import { MetaTags } from "../meta-tags";
import { MyWorkshopsTable } from "./my-workshops-table";
import { NoWorkshops } from "./no-workshops";

export const MyWorkshopsProfilePageHandler = () => {
  const {
    data: {
      me: { bookedScheduleItems },
    },
  } = useMyProfileWithBookedWorkshopsQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
  });

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="profile.myWorkshops.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Section background="coral">
        <Heading size="display2">
          <FormattedMessage id="profile.myWorkshops" />
        </Heading>
      </Section>
      <Section>
        {bookedScheduleItems.length > 0 && (
          <MyWorkshopsTable workshops={bookedScheduleItems} />
        )}
        {bookedScheduleItems.length === 0 && <NoWorkshops />}
      </Section>
    </Page>
  );
};
