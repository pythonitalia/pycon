/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Container } from "@theme-ui/components";
import { graphql } from "gatsby";
import { Fragment, useContext } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "../../app/profile/hooks";
import { Alert } from "../../components/alert";
import IS_CFP_OPEN_QUERY from "../../components/cpf-page/is-cfp-open.graphql";
import { LoginForm } from "../../components/login-form";
import { MetaTags } from "../../components/meta-tags";
import { ConferenceContext, useConference } from "../../context/conference";
import { SubmissionQuery as FallbackSubmissionQuery } from "../../generated/graphql";
import {
  IsCfpOpenQuery,
  IsCfpOpenQueryVariables,
  IsVotingClosedQuery,
  IsVotingClosedQueryVariables,
  SubmissionQuery,
  SubmissionQueryVariables,
} from "../../generated/graphql-backend";
import IS_VOTING_CLOSED_QUERY from "./is-voting-closed.graphql";
import { Submission } from "./submission";
import SUBMISSION_QUERY from "./submission.graphql";

type PageContext = {
  id: string;
  socialCard: string;
  socialCardTwitter: string;
};

const NotLoggedIn: React.SFC<{
  title?: string;
  socialCard?: string;
  socialCardTwitter?: string;
}> = ({ title, socialCard, socialCardTwitter }) => (
  <Container>
    {title ? (
      <MetaTags
        title={title}
        imageUrl={socialCard}
        twitterImageUrl={socialCardTwitter}
      />
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
  title,
  submission,
  pageContext,
}: {
  submission?: SubmissionQuery["submission"];
  pageContext?: PageContext;
  title: string;
}) => {
  const [loggedIn, _] = useLoginState();
  const conferenceCode = useContext(ConferenceContext);

  const { data } = useQuery<IsVotingClosedQuery, IsVotingClosedQueryVariables>(
    IS_VOTING_CLOSED_QUERY,
    {
      variables: { conference: conferenceCode },
    },
  );

  console.log(data?.conference.isVotingClosed);

  if (!data?.conference.isVotingClosed && !loggedIn) {
    return (
      <NotLoggedIn
        title={submission?.title || title}
        socialCard={pageContext?.socialCard}
        socialCardTwitter={pageContext?.socialCardTwitter}
      />
    );
  }

  if (!submission) {
    return <NotFound />;
  }

  return <Submission submission={submission} pageContext={pageContext} />;
};

type Props = {
  pageContext?: PageContext;
  data?: FallbackSubmissionQuery;
} & RouteComponentProps<{ id: string }>;

export const SubmissionPage: React.SFC<Props> = ({
  id,
  pageContext,
  data: fallbackData,
}) => {
  const { loading, data } = useQuery<SubmissionQuery, SubmissionQueryVariables>(
    SUBMISSION_QUERY,
    {
      errorPolicy: "all",
      variables: {
        id: pageContext?.id || id!,
      },
      skip: typeof window === "undefined",
    },
  );

  return (
    <Container sx={{ maxWidth: "container", px: 3 }}>
      {loading && <Loading />}
      {!loading && (
        <Content
          title={fallbackData?.backend.submission?.title!}
          submission={data?.submission}
          pageContext={pageContext}
        />
      )}
    </Container>
  );
};

export default SubmissionPage;

export const query = graphql`
  query Submission($id: ID!) {
    backend {
      submission(id: $id) {
        title
      }
    }
  }
`;
