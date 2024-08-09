import { Heading, Page, Section } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { useMyProfileWithSubmissionsQuery } from "~/types";

import { MetaTags } from "../meta-tags";
import { MyProposalsTable } from "../my-proposals-profile-page-handler/my-proposals-table";
import { NoProposals } from "../my-proposals-profile-page-handler/no-proposals";
import { MyGrantTable } from "./my-grants-table";

export const MyGrantProfilePageHandler = () => {
  const {
    data: {
      me: { grant },
      conference: { deadline },
    },
  } = useMyProfileWithGrantQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
  });

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="profile.myGrant.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Section background="green">
        <Heading size="display2">
          <FormattedMessage id="profile.myGrant" />
        </Heading>
      </Section>
      <Section>
        {grant.length > 0 && <MyGrantTable grant={grant} />}
        {grant.length === 0 && <NoProposals deadline={deadline} />}
      </Section>
    </Page>
  );
};
