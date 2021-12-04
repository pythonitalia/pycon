import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import { GetStaticPaths, GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { MetaTags } from "~/components/meta-tags";
import { SignupForm } from "~/components/signup-form";
import { prefetchSharedQueries } from "~/helpers/prefetch";

export const SignupPage = () => (
  <Fragment>
    <FormattedMessage id="signup.title">
      {(title) => <MetaTags title={title} />}
    </FormattedMessage>

    <SignupForm />
  </Fragment>
);

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await prefetchSharedQueries(client, locale);

  return addApolloState(client, {
    props: {},
  });
};

export default SignupPage;
