import { Page, Text } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import type { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { MyGrantOrForm } from "~/components/grant-form";
import { MetaTags } from "~/components/meta-tags";
import { formatDeadlineDateTime } from "~/helpers/deadlines";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import {
  DeadlineStatus,
  queryCurrentUser,
  queryGrantDeadline,
  queryMyGrant,
  useGrantDeadlineQuery,
} from "~/types";

import ErrorPage from "../_error";

const GrantsComingSoon = ({ start }: { start: string }) => {
  const language = useCurrentLanguage();

  return (
    <div>
      <Text>
        <FormattedMessage
          id="grants.comingSoon"
          values={{
            start: (
              <Text weight="strong">
                {formatDeadlineDateTime(start, language)}
              </Text>
            ),
          }}
        />
      </Text>
    </div>
  );
};

const GrantsClosed = () => {
  return (
    <div>
      <Text>
        <FormattedMessage id="grants.closed" />
      </Text>
    </div>
  );
};

export const GrantsPage = () => {
  const code = process.env.conferenceCode;

  const {
    data: {
      conference: { deadline },
    },
  } = useGrantDeadlineQuery({
    variables: {
      conference: code,
    },
  });

  if (!deadline) {
    return <ErrorPage statusCode={404} />;
  }

  const { status, start } = deadline;

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="grants.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      {status === DeadlineStatus.HappeningNow && <MyGrantOrForm />}
      {status === DeadlineStatus.InTheFuture && (
        <GrantsComingSoon start={start} />
      )}
      {status === DeadlineStatus.InThePast && <GrantsClosed />}
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
      queryGrantDeadline(client, {
        conference: process.env.conferenceCode,
      }),
      queryMyGrant(client, {
        conference: process.env.conferenceCode,
      }),
      queryCurrentUser(client, {
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

export default GrantsPage;
