import { Heading, Page, Section } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { MetaTags } from "../meta-tags";

export const MyProfileSponsorSection = () => {
  // const {
  //   data: {
  //     me: { orders },
  //   },
  // } = useMyProfileWithOrdersQuery({
  //   variables: {
  //     conference: process.env.conferenceCode,
  //   },
  // });

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="profile.sponsorSection.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Section background="purple">
        <Heading size="display2">
          <FormattedMessage id="profile.myOrders" />
        </Heading>
      </Section>

      <Section>Empty</Section>
    </Page>
  );
};
