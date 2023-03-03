import { Heading, Page, Section } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { useMyProfileWithSubmissionsQuery } from "~/types";

import { MyProposalsTable } from "./my-proposals-table";
import { NoProposals } from "./no-proposals";

export const MyProposalsProfilePageHandler = () => {
  const language = useCurrentLanguage();

  const {
    data: {
      me: { submissions },
      conference: { deadline },
    },
  } = useMyProfileWithSubmissionsQuery({
    variables: {
      conference: process.env.conferenceCode,
      language,
    },
  });

  return (
    <Page endSeparator={false}>
      <Section background="green">
        <Heading size="display2">
          <FormattedMessage id="profile.myProposals" />
        </Heading>
      </Section>
      <Section>
        {submissions.length > 0 && (
          <MyProposalsTable submissions={submissions} />
        )}
        {submissions.length === 0 && <NoProposals deadline={deadline} />}
      </Section>
    </Page>
  );
};
