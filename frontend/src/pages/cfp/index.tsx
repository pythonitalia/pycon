import {
  Heading,
  Link,
  Page,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import type { GetServerSideProps, GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Introduction } from "~/components/cfp-introduction";
import { CfpSendSubmission } from "~/components/cfp-send-submission";
import { MetaTags } from "~/components/meta-tags";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  queryCfpForm,
  queryIsCfpOpen,
  queryParticipantData,
  queryTags,
  useIsCfpOpenQuery,
} from "~/types";

const CfpSectionOrClosedMessage = ({ open }: { open: boolean }) => {
  if (open) {
    return <CfpSendSubmission />;
  }

  return (
    <div>
      <Heading size={1}>
        <FormattedMessage id="cfp.closed.title" />
      </Heading>

      <Spacer size="small" />

      <Text as="p" size={1}>
        <FormattedMessage id="cfp.closed.description" />
      </Text>

      <Text as="p" size={1}>
        <FormattedMessage id="cfp.closed.voting" />{" "}
        <Link href="/tickets">
          <FormattedMessage id="cfp.closed.buyTicket" />
        </Link>
      </Text>
    </div>
  );
};

export const CFPPage = () => {
  const code = process.env.conferenceCode;
  const { data } = useIsCfpOpenQuery({
    variables: { conference: code },
  });

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="cfp.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Section>
        <Introduction deadline={data.conference.cfpDeadline?.end} />
        <CfpSectionOrClosedMessage open={data.conference.isCFPOpen || false} />
      </Section>
    </Page>
  );
};

export const getServerSideProps: GetServerSideProps = async ({
  req,
  locale,
}) => {
  const identityToken = req.cookies.pythonitalia_sessionid;
  if (!identityToken) {
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  const client = getApolloClient(null, req.cookies);
  try {
    await Promise.all([
      prefetchSharedQueries(client, locale),
      queryIsCfpOpen(client, {
        conference: process.env.conferenceCode,
      }),
      queryParticipantData(client, {
        conference: process.env.conferenceCode,
      }),
      queryCfpForm(client, {
        conference: process.env.conferenceCode,
      }),
      queryTags(client, {
        conference: process.env.conferenceCode,
      }),
    ]);
  } catch (e) {
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  return addApolloState(
    client,
    {
      props: {},
    },
    null,
  );
};

export default CFPPage;
