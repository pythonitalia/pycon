/** @jsx jsx */
import { RouteComponentProps } from "@reach/router";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Container, jsx } from "theme-ui";

import { useLoginState } from "../../app/profile/hooks";
import { MySubmissions } from "../../app/profile/my-submissions";
import { Alert } from "../alert";
import { LoginForm } from "../login-form";
import { MetaTags } from "../meta-tags";
import { Cfp } from "./cfp";
import { Introduction } from "./introduction";

export const CFPPage: React.SFC<RouteComponentProps> = () => {
  const [isLoggedIn, _] = useLoginState();

  return (
    <Fragment>
      <FormattedMessage id="cfp.pageTitle">
        {text => <MetaTags title={text} />}
      </FormattedMessage>

      <Introduction />

      {isLoggedIn ? (
        <Fragment>
          <MySubmissions />

          <Cfp sx={{ mt: 4 }} />
        </Fragment>
      ) : (
        <Fragment>
          <Box sx={{ px: 3 }}>
            <Container sx={{ maxWidth: "container", p: 0 }}>
              <Alert variant="info" sx={{ mt: 4 }}>
                <FormattedMessage id="cfp.needToBeLoggedIn" />
              </Alert>
            </Container>
          </Box>

          <LoginForm sx={{ mt: 4 }} />
        </Fragment>
      )}
    </Fragment>
  );
};
