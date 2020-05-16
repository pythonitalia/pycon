/** @jsx jsx */
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Container, Heading, jsx, Text } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";
import { MySubmissions } from "~/app/profile/my-submissions";
import { useIsCfpOpenQuery } from "~/types";

import { Alert } from "../alert";
import { Link } from "../link";
import { LoginForm } from "../login-form";
import { MetaTags } from "../meta-tags";
import { Cfp } from "./cfp";
import { Introduction } from "./introduction";

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
        <Link path="/[lang]/tickets">
          <FormattedMessage id="cfp.closed.buyTicket" />
        </Link>
      </Text>
    </Box>
  );
};

export const CFPPage: React.SFC = () => {
  const [isLoggedIn, _] = useLoginState();
  const code = process.env.conferenceCode;

  const { loading, data } = useIsCfpOpenQuery({
    variables: { conference: code },
  });

  return (
    <Fragment>
      <FormattedMessage id="cfp.pageTitle">
        {(text) => <MetaTags title={text} />}
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
