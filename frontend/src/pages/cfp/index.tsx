import {
  Heading,
  Link,
  Page,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import type { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { Introduction } from "~/components/cfp-introduction";
import { CfpSendSubmission } from "~/components/cfp-send-submission";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  queryCfpForm,
  queryIsCfpOpen,
  queryTags,
  useIsCfpOpenQuery,
} from "~/types";

const CfpSectionOrClosedMessage = ({ open }: { open: boolean }) => {
  if (open) {
    return (
      <Fragment>
        <CfpSendSubmission />
      </Fragment>
    );
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
  const [isLoggedIn, _] = useLoginState();

  const code = process.env.conferenceCode;

  const { loading, data } = useIsCfpOpenQuery({
    variables: { conference: code },
  });

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="cfp.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Introduction
        deadline={
          data?.conference.isCFPOpen
            ? data?.conference.cfpDeadline?.end
            : undefined
        }
      />

      <Section>
        {isLoggedIn ? (
          !loading && (
            <CfpSectionOrClosedMessage
              open={data?.conference.isCFPOpen || false}
            />
          )
        ) : (
          <Alert variant="info">
            <FormattedMessage id="cfp.needToBeLoggedIn" />
          </Alert>
        )}
      </Section>
    </Page>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryIsCfpOpen(client, {
      conference: process.env.conferenceCode,
    }),
    queryCfpForm(client, {
      conference: process.env.conferenceCode,
    }),
    queryTags(client),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default CFPPage;
