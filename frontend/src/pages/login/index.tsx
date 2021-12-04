import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import { GetStaticPaths, GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { LoginForm } from "~/components/login-form";
import { MetaTags } from "~/components/meta-tags";
import { prefetchSharedQueries } from "~/helpers/prefetch";

export const LoginPage = () => (
  <Fragment>
    <FormattedMessage id="login.title">
      {(title) => <MetaTags title={title} />}
    </FormattedMessage>

    <LoginForm />
  </Fragment>
);

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await prefetchSharedQueries(client, locale);

  return addApolloState(client, {
    props: {},
  });
};

export default LoginPage;
