import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import { GetStaticPaths, GetStaticProps } from "next";

import { addApolloState } from "~/apollo/client";
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

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const lang = params.lang as string;

  await prefetchSharedQueries(lang);

  return addApolloState({
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default LoginPage;
