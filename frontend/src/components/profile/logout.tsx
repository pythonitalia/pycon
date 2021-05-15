/** @jsxRuntime classic */
/** @jsx jsx */
import { useApolloClient } from "@apollo/client";
import Router from "next/router";
import { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx, Text } from "theme-ui";

import { Alert } from "~/components/alert";
import { Button } from "~/components/button/button";
import { useLogoutMutation } from "~/types";

import { useLoginState } from "./hooks";

export const Logout = () => {
  const [logout, { error, loading }] = useLogoutMutation({
    onCompleted: () => {
      setLoggedIn(false);
      window.location.href = "/";
    },
  });
  const [_, setLoggedIn] = useLoginState();

  const onLogout = useCallback(() => {
    if (loading) {
      return;
    }

    logout();
  }, [logout, loading]);

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
          my: 5,
          px: 3,
        }}
      >
        <Heading mb={2} as="h2" sx={{ fontSize: 5 }}>
          <FormattedMessage id="profile.logout" />
        </Heading>

        <Text mb={4}>
          <FormattedMessage id="profile.seeYourSoon" />
        </Text>

        <Button loading={loading} onClick={onLogout}>
          Logout
        </Button>

        {error && <Alert variant="alert">{error.message}</Alert>}
      </Box>
    </Box>
  );
};
