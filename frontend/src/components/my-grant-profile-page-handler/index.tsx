import { Heading, Page, Section } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useMyProfileWithGrantQuery } from "~/types";

import { MyGrant } from "~/components/my-grant-profile-page-handler/my-grant";
import { NoGrant } from "~/components/my-grant-profile-page-handler/no-grant";
import { MetaTags } from "../meta-tags";

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
      <FormattedMessage id="profile.myGrant">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Section background="green">
        <Heading size="display2">
          <FormattedMessage id="profile.myGrant" />
        </Heading>
      </Section>

      <Section>
        {grant && <MyGrant grant={grant} deadline={deadline} />}
        {!grant && <NoGrant deadline={deadline} />}
      </Section>
    </Page>
  );
};
