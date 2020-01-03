import { useMutation } from "@apollo/react-hooks";
import { navigate, Redirect } from "@reach/router";
import { Box, Button, Heading, Text } from "@theme-ui/components";
import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";

import { Alert } from "../../components/alert";
import { LogoutMutation } from "../../generated/graphql-backend";
import { useLoginState } from "./hooks";
import LOGOUT_MUTATION from "./logout.graphql";
import { client } from "../../apollo/client";

export const Logout: React.SFC<{ lang: string }> = ({ lang }) => {
  const [logout, { error, loading, data }] = useMutation<LogoutMutation>(
    LOGOUT_MUTATION,
  );
  const [loggedIn, setLoggedIn] = useLoginState();

  const onLogout = useCallback(() => {
    if (loading) {
      return;
    }

    logout();
  }, [logout, loading]);

  if (data && data.logout.__typename === "OperationResult" && data.logout.ok) {
    setLoggedIn(false);
    client.resetStore();
    return <Redirect noThrow={true} to={`/${lang}/`} />;
  }

  return (
    <Box
      sx={{
        borderTop: "primary",
      }}
    >
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          my: 4,
          px: 3,
        }}
      >
        <Heading mb={2} as="h2">
          <FormattedMessage id="profile.logout" />
        </Heading>
        <Text mb={4}>
          <FormattedMessage id="profile.seeYourSoon" />
        </Text>
        <Button onClick={onLogout}>Logout</Button>

        {error && <Alert variant="alert">{error.message}</Alert>}
        {data && data.logout.__typename === "LogoutErrors" && (
          <Alert variant="alert">{data.logout.nonFieldErrors.join(",")}</Alert>
        )}
      </Box>
    </Box>
  );
};
