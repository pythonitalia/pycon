import { useMutation } from "@apollo/react-hooks";
import { navigate, Redirect, RouteComponentProps } from "@reach/router";
import { Box, Button, Input, Label } from "@theme-ui/components";
import React from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useLoginState } from "../../app/profile/hooks";
import {
  LoginMutation,
  LoginMutationVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { Link } from "../link";
import LOGIN_MUTATION from "./login.graphql";

type LoginFormFields = {
  email: string;
  password: string;
};

export const LoginForm: React.SFC<RouteComponentProps<{ lang: string }>> = ({
  lang,
  location,
}) => {
  const profileUrl = `/${lang}/profile`;

  const [loggedIn, setLoggedIn] = useLoginState();

  const onLoginCompleted = (data: LoginMutation) => {
    if (data && data.login.__typename === "MeUser") {
      setLoggedIn(true);

      navigate(profileUrl);
    }
  };

  const [login, { loading, error, data: loginData }] = useMutation<
    LoginMutation,
    LoginMutationVariables
  >(LOGIN_MUTATION, { onCompleted: onLoginCompleted });
  const [formState, { label, email, password }] = useFormState<LoginFormFields>(
    {},
    {
      withIds: true,
    },
  );

  if (loggedIn) {
    return <Redirect to={profileUrl} noThrow={true} />;
  }

  const errorMessage =
    loginData && loginData.login.__typename === "LoginErrors"
      ? loginData.login.nonFieldErrors.join(" ")
      : (error || "").toString();

  return (
    <Box
      as="form"
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
      }}
      method="post"
      onSubmit={(e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        login({ variables: formState.values });
      }}
    >
      {errorMessage && <div>{errorMessage}</div>}
      {location?.state?.message && (
        <Alert variant={location.state.messageVariant || "success"}>
          {location.state.message}
        </Alert>
      )}

      <Label {...label("email")}>
        <FormattedMessage id="login.email" />
      </Label>
      <Input
        {...email("email")}
        placeholder="guido@python.org"
        required={true}
        type="email"
      />

      <Label htmlFor="login-password">
        <FormattedMessage id="login.password" />
      </Label>
      <Input
        id="login-password"
        {...password("password")}
        required={true}
        type="password"
      />

      <Link
        sx={{
          display: "block",
          my: 2,
        }}
        href={`/${lang}/reset-password/`}
      >
        <FormattedMessage id="login.recoverPassword" />
      </Link>

      <Button size="medium" palette="primary" isLoading={loading} type="submit">
        <FormattedMessage id="login.loginButton" />
      </Button>
    </Box>
  );
};
