import { Heading, Page, Section } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import type { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { GrantForm } from "~/components/grant-form";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  type UpdateGrantInput,
  queryCurrentUser,
  queryGrantDeadline,
  queryMyGrant,
  queryParticipantData,
  useMyGrantQuery,
  useUpdateGrantMutation,
} from "~/types";

import type { JSX } from "react";

const GrantPage = (): JSX.Element => {
  const code = process.env.conferenceCode;

  const { loading, data } = useMyGrantQuery({
    errorPolicy: "all",
    variables: {
      conference: code,
    },
  });

  const grant = data?.me?.grant;
  const [
    updateGrant,
    { loading: updateLoading, error: updateError, data: updateData },
  ] = useUpdateGrantMutation();

  const onSubmit = async (input: UpdateGrantInput) => {
    updateGrant({
      variables: {
        input: {
          instance: grant.id,
          ...input,
        },
      },
    });
  };

  if (loading) {
    return null;
  }

  return (
    <Page endSeparator={false}>
      <Section>
        <Heading size="display2">
          <FormattedMessage id="grants.form.edit.title" />
        </Heading>
      </Section>
      <Section>
        <GrantForm
          conference={code}
          grant={grant}
          onSubmit={onSubmit}
          loading={updateLoading}
          error={updateError}
          data={updateData}
        />
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
      queryGrantDeadline(client, {
        conference: process.env.conferenceCode,
      }),
      queryMyGrant(client, {
        conference: process.env.conferenceCode,
      }),
      queryCurrentUser(client, {
        conference: process.env.conferenceCode,
      }),
      queryParticipantData(client, {
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

export default GrantPage;
