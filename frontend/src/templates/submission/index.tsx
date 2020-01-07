/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Container } from "@theme-ui/components";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "../../app/profile/hooks";
import { Alert } from "../../components/alert";
import { LoginForm } from "../../components/login-form";
import { MetaTags } from "../../components/meta-tags";
import {
  SubmissionQuery,
  SubmissionQueryVariables,
} from "../../generated/graphql-backend";
import { Submission } from "./submission";
import SUBMISSION_QUERY from "./submission.graphql";

type PageContext = {
  id: string;
  socialCard: string;
  socialCardTwitter: string;
};

const NotLoggedIn: React.SFC<{ title?: string }> = ({ title }) => (
  <Container>
    {title ? (
      <MetaTags title={title} />
    ) : (
      <FormattedMessage id="submission.notFound">
        {text => <MetaTags title={text} />}
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
    {text => (
      <Fragment>
        <MetaTags title={text} />

        <Alert variant="info">{text}</Alert>
      </Fragment>
    )}
  </FormattedMessage>
);

const NotFound = () => (
  <FormattedMessage id="submission.notFound">
    {text => (
      <Fragment>
        <MetaTags title={text} />

        <Alert variant="alert">{text}</Alert>
      </Fragment>
    )}
  </FormattedMessage>
);

const Content = ({
  submission,
  pageContext,
}: {
  submission?: SubmissionQuery["submission"];
  pageContext?: PageContext;
}) => {
  const [loggedIn, _] = useLoginState();

  if (!loggedIn) {
    return <NotLoggedIn title={submission?.title} />;
  }

  if (!submission) {
    return <NotFound />;
  }

  return <Submission submission={submission} pageContext={pageContext} />;
};

type Props = {
  pageContext?: PageContext;
} & RouteComponentProps<{ id: string }>;

export const SubmissionPage: React.SFC<Props> = ({ id, pageContext }) => {
  const { loading, data } = useQuery<SubmissionQuery, SubmissionQueryVariables>(
    SUBMISSION_QUERY,
    {
      errorPolicy: "all",
      variables: {
        id: pageContext?.id || id!,
      },
    },
  );

  return (
    <Container sx={{ maxWidth: "container", px: 3 }}>
      {loading && <Loading />}
      {!loading && (
        <Content submission={data?.submission} pageContext={pageContext} />
      )}
    </Container>
  );
};

export default SubmissionPage;
