import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Container, Text } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { GrantForm } from "~/components/grant-form";
import { LoginForm } from "~/components/login-form";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { useMyGrantQuery } from "~/types";

const GrantPage = (): JSX.Element => {
  const code = process.env.conferenceCode;

  const { loading, data } = useMyGrantQuery({
    errorPolicy: "all",
    variables: {
      conference: code,
    },
    skip: typeof window === "undefined",
  });

  if (!loading) {
    return (
      <Text>
        <FormattedMessage id="grants.form.sent" />
      </Text>
    );
  }

  return (
    <>
      {" "}
      <GrantForm conference={code} />
    </>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([prefetchSharedQueries(client, locale)]);

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default GrantPage;
