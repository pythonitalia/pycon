/** @jsx jsx */
import { RouteComponentProps } from "@reach/router";
import { Box, Container } from "@theme-ui/components";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "../../app/profile/hooks";
import { MySubmissions } from "../../app/profile/my-submissions";
import { Alert } from "../alert";
import { LoginForm } from "../login-form";
import { MetaTags } from "../meta-tags";
import { Cfp } from "./cfp";
import { Introduction } from "./introduction";

export const CFPPage: React.SFC<RouteComponentProps> = ({ location }) => {
  const [isLoggedIn, _] = useLoginState();

  return (
    <Fragment>
      <FormattedMessage id="cfp.pageTitle">
        {text => <MetaTags title={text} />}
      </FormattedMessage>
      <Introduction />

      <Box sx={{ px: 3 }}>
        <Container sx={{ maxWidth: "container", p: 0 }}>
          {isLoggedIn ? (
            <Fragment>
              <MySubmissions sx={{ mb: 4 }} />

              <Cfp />
            </Fragment>
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
