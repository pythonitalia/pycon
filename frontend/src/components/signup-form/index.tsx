import { useMutation } from "@apollo/react-hooks";
import { navigate, Redirect, RouteComponentProps } from "@reach/router";
import { Box, Button, Input, Label } from "@theme-ui/components";
import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useLoginState } from "../../app/profile/hooks";
import {
  SignupMutation,
  SignupMutationVariables,
} from "../../generated/graphql-backend";
import SIGNUP_MUTATION from "./signup.graphql";

type SignupFormProps = {
  email: string;
  password: string;
};

export const SignupForm: React.SFC<RouteComponentProps<{ lang: string }>> = ({
  lang,
}) => {
  const [loggedIn, setLoggedIn] = useLoginState();
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
      : (error || "").toString();

  const getFieldError = (field: "validationEmail" | "validationPassword") =>
    (data &&
      data.register.__typename === "RegisterErrors" &&
      data.register[field].join(", ")) ||
    "";
  const emailError = getFieldError("validationEmail");
  const passwordError = getFieldError("validationPassword");

  return (
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
      }}
      as="form"
      onSubmit={onFormSubmit}
      method="post"
    >
      {errorMessage && <div>{errorMessage}</div>}
      <Label {...label("email")}>
        <FormattedMessage id="signup.email" />
      </Label>
      <div>{emailError}</div>
      <Input
        {...email("email")}
        placeholder="guido@python.org"
        required={true}
        type="email"
      />
      <Label {...label("password")}>
        <FormattedMessage id="signup.password" />
      </Label>

      <div>{passwordError}</div>
      <Input {...password("password")} required={true} type="password" />
      <Button type="submit">
        <FormattedMessage id="signup.signupButton" />
      </Button>
    </Box>
  );
};
