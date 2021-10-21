/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Container, jsx } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { LoginForm } from "~/components/login-form";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { Submission } from "~/components/submission";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  queryIsVotingClosed,
  SubmissionQuery,
  useIsVotingClosedQuery,
  useSubmissionQuery,
} from "~/types";

const NotLoggedIn: React.SFC<{
  title?: string;
}> = ({ title }) => (
  <Container>
    {title ? (
      <MetaTags title={title} />
    ) : (
      <FormattedMessage id="submission.notFound">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>
    )}

    <Alert variant="info">
      You need to logged in and have a ticket to see this submission
    </Alert>

    <LoginForm />
  </Container>
);

const Loading = () => (
  <FormattedMessage id="submission.loading">
    {(text) => (
      <Fragment>
        <MetaTags title={text} />

        <Alert variant="info">{text}</Alert>
      </Fragment>
    )}
  </FormattedMessage>
);

const NotFound = () => (
  <FormattedMessage id="submission.notFound">
    {(text) => (
      <Fragment>
        <MetaTags title={text} />

        <Alert variant="alert">{text}</Alert>
      </Fragment>
    )}
  </FormattedMessage>
);

const Content = ({
  submission,
}: {
  submission?: SubmissionQuery["submission"];
}) => {
  const [loggedIn, _] = useLoginState();
  const code = process.env.conferenceCode;

  const { data } = useIsVotingClosedQuery({
    variables: { conference: code },
  });

  if (!data?.conference.isVotingClosed && !loggedIn) {
    return <NotLoggedIn title={submission?.title} />;
  }

  if (!submission) {
    return <NotFound />;
  }

  return <Submission submission={submission} />;
};

export const SubmissionPage = () => {
  const router = useRouter();

  const id = router.query.id as string;

  const { loading, data } = useSubmissionQuery({
    errorPolicy: "all",
    variables: {
      id,
    },
    skip: typeof window === "undefined",
  });

  return (
    <Container sx={{ maxWidth: "container", px: 3 }}>
      {loading && <Loading />}
      {!loading && <Content submission={data?.submission} />}
    </Container>
  );
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const language = params.lang as string;

  await Promise.all([
    prefetchSharedQueries(language),
    queryIsVotingClosed({
      conference: process.env.conferenceCode,
    }),
  ]);

  return addApolloState({
    props: {},
    revalidate: 1,
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default SubmissionPage;
