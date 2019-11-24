import { useMutation } from "@apollo/react-hooks";
import { navigate, Redirect, RouteComponentProps } from "@reach/router";
import { Box, Button, Grid, Input, Label, Text } from "@theme-ui/components";
import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useLoginState } from "../../app/profile/hooks";
import {
  RegisterErrors,
  SignupMutation,
  SignupMutationVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { InputWrapper } from "../input-wrapper";
import { Link } from "../link";
import SIGNUP_MUTATION from "./signup.graphql";

type SignupFormProps = {
  email: string;
  password: string;
};

export const SignupForm: React.SFC<RouteComponentProps<{ lang: string }>> = ({
  lang,
  location,
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

  const getFieldErrors = (field: "validationEmail" | "validationPassword") =>
    (data &&
      data.register.__typename === "RegisterErrors" &&
      data.register[field]) ||
    [];

  return (
    <Box
      sx={{
        px: 2,
      }}
    >
      {location?.state?.message && (
        <Alert variant="alert">{location.state.message}</Alert>
      )}

      <Grid
        sx={{
          maxWidth: "container",
          mx: "auto",
          mt: 3,
          gridTemplateColumns: [null, null, "1fr 1fr"],
          gridColumnGap: 5,
        }}
      >
        <Box as="form" onSubmit={onFormSubmit} method="post">
          <Text mb={4} as="h2">
            <FormattedMessage id="signup.signupWithEmail" />
          </Text>

          {errorMessage && <div>{errorMessage}</div>}

          <InputWrapper
            sx={{ mb: 0 }}
            errors={getFieldErrors("validationEmail")}
            label={<FormattedMessage id="signup.email" />}
          >
            <Input
              {...email("email")}
              placeholder="guido@python.org"
              required={true}
              type="email"
            />
          </InputWrapper>

          <Link
            sx={{
              display: "block",
              mb: 4,
            }}
            href={`/${lang}/login/`}
          >
            <FormattedMessage id="signup.alreadyHaveAccount" />
          </Link>

          <InputWrapper
            errors={getFieldErrors("validationPassword")}
            label={<FormattedMessage id="signup.password" />}
          >
            <Input
              {...password("password")}
              required={true}
              type="password"
              mb={4}
            />
          </InputWrapper>

          <Button type="submit">
            <FormattedMessage id="signup.signupButton" />
          </Button>
        </Box>
        <Box>
          <Text mb={4} as="h2">
            <FormattedMessage id="signup.signupWithSocial" />
          </Text>

          <Button href="/login/google/" as="a">
            <FormattedMessage id="signup.useGoogle" />
          </Button>
        </Box>
      </Grid>
    </Box>
  );
};
