import { useMutation } from "@apollo/react-hooks";
import { navigate, Redirect, RouteComponentProps } from "@reach/router";
import { Alert, FieldSet, FieldWrapper, Input, Label } from "fannypack";
import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useLoginState } from "../../app/profile/hooks";
import {
  SignupMutation,
  SignupMutationVariables,
} from "../../generated/graphql-backend";
import { Button } from "../button";
import { Form } from "../form";
import SIGNUP_MUTATION from "./signup.graphql";

type SignupFormProps = {
  email: string;
  password: string;
};

export const SignupForm: React.SFC<RouteComponentProps<{ lang: string }>> = ({
  lang,
  location,
}) => {
  const [loggedIn, setLoggedIn] = useLoginState(false);
  const profileUrl = `/${lang}/profile`;
  const onSignupComplete = (signupData: SignupMutation) => {
    if (!signupData || signupData.register.__typename !== "MeUser") {
      return;
    }

    setLoggedIn(true);
    navigate(profileUrl);
  };
  const [signup, { loading, error, data }] = useMutation<
    SignupMutation,
    SignupMutationVariables
  >(SIGNUP_MUTATION, {
    onCompleted: onSignupComplete,
  });
  const [formState, { label, email, password }] = useFormState<SignupFormProps>(
    {},
    {
      withIds: true,
    },
  );

  const onFormSubmit = useCallback(
    e => {
      e.preventDefault();
      signup({
        variables: formState.values,
      });
    },
    [signup, formState],
  );

  if (loggedIn) {
    return <Redirect to={profileUrl} noThrow={true} />;
  }

  const errorMessage =
    data && data.register.__typename === "RegisterErrors"
      ? data.register.nonFieldErrors.join(" ")
      : error;

  const getFieldError = (field: "validationEmail" | "validationPassword") =>
    (data &&
      data.register.__typename === "RegisterErrors" &&
      data.register[field].join(", ")) ||
    "";
  const emailError = getFieldError("validationEmail");
  const passwordError = getFieldError("validationPassword");

  return (
    <Form onSubmit={onFormSubmit} method="post">
      {location && location.state && location.state.message && (
        <Alert marginBottom="major-3" type="info">
          {location.state.message}
        </Alert>
      )}

      <FieldSet>
        {errorMessage && <Alert type="error">{errorMessage}</Alert>}

        <Label htmlFor="signup-email" {...label("email")}>
          <FormattedMessage id="signup.email" />
        </Label>

        <FieldWrapper
          validationText={emailError}
          state={emailError ? "danger" : ""}
        >
          <Input
            inputProps={{
              id: "signup-email",
              ...email("email"),
              required: true,
            }}
            placeholder="guido@python.org"
            isRequired={true}
            type="email"
          />
        </FieldWrapper>

        <Label htmlFor="signup-password">
          <FormattedMessage id="signup.password" />
        </Label>
        <FieldWrapper
          validationText={passwordError}
          state={passwordError ? "danger" : ""}
        >
          <Input
            inputProps={{
              id: "signup-password",
              ...password("password"),
              required: true,
            }}
            isRequired={loading}
            type="password"
          />
        </FieldWrapper>

        <Button
          size="medium"
          palette="primary"
          isLoading={loading}
          type="submit"
        >
          <FormattedMessage id="signup.signupButton" />
        </Button>
      </FieldSet>
    </Form>
  );
};
