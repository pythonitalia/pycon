/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Container } from "@theme-ui/components";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "../../app/profile/hooks";
import {
  SubmissionQuery,
  SubmissionQueryVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { LoginForm } from "../login-form";
import { MetaTags } from "../meta-tags";
import { Submission } from "./submission";
import SUBMISSION_QUERY from "./submission.graphql";

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
}: {
  submission?: SubmissionQuery["submission"];
}) => {
  const [loggedIn, _] = useLoginState();

  if (!loggedIn) {
    return <NotLoggedIn title={submission?.title} />;
  }

  if (!submission) {
    return <NotFound />;
  }

  return <Submission submission={submission} />;
};

export const SubmissionPage = ({ id }: RouteComponentProps<{ id: string }>) => {
  const { loading, data } = useQuery<SubmissionQuery, SubmissionQueryVariables>(
    SUBMISSION_QUERY,
    {
      errorPolicy: "all",
      variables: {
        id: id!,
      },
    },
  );

  return (
    <Container sx={{ maxWidth: "container", px: 3 }}>
      {loading && <Loading />}
      {!loading && <Content submission={data?.submission} />}
    </Container>
  );
};
