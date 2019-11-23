import { useQuery } from "@apollo/react-hooks";
import { Redirect, RouteComponentProps } from "@reach/router";
import { Box } from "@theme-ui/components";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useLoginState } from "../../app/profile/hooks";
import { SocialLoginCheckQuery } from "../../generated/graphql-backend";
import SOCIAL_LOGIN_CHECK from "./social-login-check.graphql";

type Props = {
  lang: string;
};

export const SocialLoginSuccess: React.SFC<RouteComponentProps<Props>> = ({
  lang,
}) => {
  const { loading, error, data } = useQuery<SocialLoginCheckQuery>(
    SOCIAL_LOGIN_CHECK,
  );
  const [loggedIn, setLoggedIn] = useLoginState();

  if (loggedIn) {
    return <Redirect to={`/${lang}/profile/`} noThrow={true} />;
  }

  if (!loading && !error && data!.me) {
    setLoggedIn(true);
    return <Redirect to={`/${lang}/profile/`} noThrow={true} />;
  }

  if (!loading && error) {
    return (
      <Redirect
        to={`/${lang}/login/`}
        state={{
          message: "Something went wrong, please try again",
        }}
        noThrow={true}
      />
    );
  }

  return (
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 2,
      }}
    >
      {loading && <FormattedMessage id="login.loading" />}
    </Box>
  );
};
