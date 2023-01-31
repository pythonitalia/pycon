import { Heading, Page, Section } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { GrantForm } from "~/components/grant-form";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  useMyGrantQuery,
  useUpdateGrantMutation,
  UpdateGrantInput,
} from "~/types";

const GrantPage = (): JSX.Element => {
  const code = process.env.conferenceCode;

  const { loading, data } = useMyGrantQuery({
    errorPolicy: "all",
    variables: {
      conference: code,
    },
    skip: typeof window === "undefined",
  });

  const grant = data && data?.me?.grant;
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

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([prefetchSharedQueries(client, locale)]);

  return addApolloState(client, {
    props: {},
  });
};

export default GrantPage;
