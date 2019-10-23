import { useMutation } from "@apollo/react-hooks";
import { navigate, Redirect, RouteComponentProps } from "@reach/router";
import { Alert, FieldSet, Input, Label } from "fannypack";
import React from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useLoginState } from "../../app/profile/hooks";
import {
  LoginMutation,
  LoginMutationVariables,
} from "../../generated/graphql-backend";
import { Button } from "../button";
import { Form } from "../form";
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

  const [loggedIn, setLoggedIn] = useLoginState(false);

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
      : error;

  return (
    <Form
      method="post"
      onSubmit={e => {
        e.preventDefault();

        login({ variables: formState.values });
      }}
    >
      {location && location.state && location.state.message && (
        <Alert marginBottom="major-3" type="info">
          {location.state.message}
        </Alert>
      )}
      <FieldSet>
        {errorMessage && <Alert type="error">{errorMessage}</Alert>}

        <Label {...label("email")}>
          <FormattedMessage id="login.email" />
        </Label>
        <Input
          inputProps={{ ...email("email"), required: true }}
          placeholder="guido@python.org"
          isRequired={true}
          type="email"
        />

        <Label htmlFor="login-password">
          <FormattedMessage id="login.password" />
        </Label>
        <Input
          inputProps={{
            id: "login-password",
            ...password("password"),
            required: true,
          }}
          isRequired={loading}
          type="password"
        />

        <Button
          size="medium"
          palette="primary"
          isLoading={loading}
          type="submit"
        >
          <FormattedMessage id="login.loginButton" />
        </Button>
      </FieldSet>
    </Form>
  );
};
