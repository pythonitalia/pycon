import { FormattedMessage } from "react-intl";
import { Box, Heading } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { GrantForm } from "~/components/grant-form";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useMyGrantQuery } from "~/types";

import { useUpdateGrantMutation, UpdateGrantInput } from "../../../types";

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
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
        my: 5,
      }}
    >
      <Heading mb={4} as="h1">
        <FormattedMessage id="grants.form.edit.title" />
      </Heading>
      <GrantForm
        conference={code}
        grant={grant}
        onSubmit={onSubmit}
        loading={updateLoading}
        error={updateError}
        data={updateData}
      />
    </Box>
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
