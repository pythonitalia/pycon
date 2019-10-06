import { useMutation } from "@apollo/react-hooks";
import { Redirect, RouteComponentProps } from "@reach/router";
import { Alert, FieldSet, Input, Label } from "fannypack";
import * as React from "react";
import { useFormState } from "react-use-form-state";

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
}) => {
  const [login, { loading, error, data }] = useMutation<
    LoginMutation,
    LoginMutationVariables
  >(LOGIN_MUTATION, {});
  const [formState, { label, email, password }] = useFormState<LoginFormFields>(
    {},
    {
      withIds: true,
    },
  );

  // TODO: on success, store that we are logged in

  if (data && data.login.__typename === "MeUser") {
    return <Redirect to={`/${lang}/profile`} noThrow={true} />;
  }

  const errorMessage =
    data && data.login.__typename === "LoginErrors"
      ? data.login.nonFieldErrors.join(" ")
      : error;

  return (
    <Form
      method="post"
      onSubmit={e => {
        e.preventDefault();

        login({ variables: formState.values });
      }}
    >
      <FieldSet>
        {errorMessage && <Alert type="error">{errorMessage}</Alert>}

        <Label {...label("email")}>Email</Label>
        <Input
          inputProps={{ ...email("email"), required: true }}
          placeholder="guido@python.org"
          isRequired={true}
          type="email"
        />

        <Label htmlFor="login-password">Password</Label>
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
          Login 👉
        </Button>
      </FieldSet>
    </Form>
  );
};
