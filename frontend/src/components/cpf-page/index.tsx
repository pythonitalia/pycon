/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Container, Heading, Text } from "@theme-ui/components";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "../../app/profile/hooks";
import { MySubmissions } from "../../app/profile/my-submissions";
import { useConference } from "../../context/conference";
import {
  IsCfpOpenQuery,
  IsCfpOpenQueryVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { Link } from "../link";
import { LoginForm } from "../login-form";
import { MetaTags } from "../meta-tags";
import { Cfp } from "./cfp";
import { Introduction } from "./introduction";
import IS_CFP_OPEN_QUERY from "./is-cfp-open.graphql";

const CfpSectionOrClosedMessage: React.SFC<{ open: boolean }> = ({ open }) => {
  if (open) {
    return (
      <Fragment>
        <MySubmissions sx={{ mb: 4 }} />

        <Cfp />
      </Fragment>
    );
  }

  return (
    <Box sx={{ mt: 4, width: [null, null, "50%"] }}>
      <Heading sx={{ mb: 3 }}>
        <FormattedMessage id="cfp.closed.title" />
      </Heading>

      <Text sx={{ mb: 3 }}>
        <FormattedMessage id="cfp.closed.description" />
      </Text>

      <Text>
        <FormattedMessage id="cfp.closed.voting" />{" "}
        <Link href=":language/tickets">
          <FormattedMessage id="cfp.closed.buyTicket" />
        </Link>
      </Text>
    </Box>
  );
};

export const CFPPage: React.SFC<RouteComponentProps> = ({ location }) => {
  const [isLoggedIn, _] = useLoginState();
  const { code } = useConference();

  const { loading, data } = useQuery<IsCfpOpenQuery, IsCfpOpenQueryVariables>(
    IS_CFP_OPEN_QUERY,
    {
      variables: { conference: code },
    },
  );

  console.log(loading, data?.conference.isCFPOpen);

  return (
    <Fragment>
      <FormattedMessage id="cfp.pageTitle">
        {text => <MetaTags title={text} />}
      </FormattedMessage>
      <Introduction />

      <Box sx={{ px: 3 }}>
        <Container sx={{ maxWidth: "container", p: 0 }}>
          {isLoggedIn ? (
            !loading && (
              <CfpSectionOrClosedMessage
                open={data?.conference.isCFPOpen || false}
              />
            )
          ) : (
            <Fragment>
              <Alert variant="info" sx={{ mt: 4 }}>
                <FormattedMessage id="cfp.needToBeLoggedIn" />
              </Alert>

              <LoginForm sx={{ mt: 4 }} next={location?.pathname} />
            </Fragment>
          )}
        </Container>
      </Box>
    </Fragment>
  );
};
