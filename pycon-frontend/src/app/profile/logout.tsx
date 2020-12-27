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
  const client = useApolloClient();

  const [logout, { error, loading, data }] = useLogoutMutation({
    onCompleted: (d) => {
      if (d?.logout?.__typename === "OperationResult" && d?.logout?.ok) {
        setLoggedIn(false);

        client.resetStore();
        Router.push("/");
        return null;
      }
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
        <Button loading={loading} onClick={onLogout}>
          Logout
        </Button>

        {error && <Alert variant="alert">{error.message}</Alert>}
        {data && data.logout.__typename === "LogoutErrors" && (
          <Alert variant="alert">{data.logout.nonFieldErrors.join(",")}</Alert>
        )}
      </Box>
    </Box>
  );
};
