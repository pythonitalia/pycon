import { GetStaticPaths, GetStaticProps } from "next";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import { addApolloState } from "~/apollo/client";
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

export default SignupPage;
