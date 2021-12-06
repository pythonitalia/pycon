/** @jsxRuntime classic */

/** @jsx jsx */
import React, { useCallback, useLayoutEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Grid, Input, jsx, Text } from "theme-ui";

import { useRouter } from "next/router";

import { useLoginState } from "~/components/profile/hooks";
import { useSignupMutation } from "~/types";

import { Alert } from "../alert";
import { Button } from "../button/button";
import { InputWrapper } from "../input-wrapper";
import { Link } from "../link";

type SignupFormProps = {
  email: string;
  password: string;
};

const getErrorMessageIfAny = (typename?: string) => {
  switch (typename) {
    case "EmailAlreadyUsed":
      return "An account with this email already exists";
    default:
      return null;
  }
};

export const SignupForm: React.SFC = () => {
  const [loggedIn, setLoggedIn] = useLoginState();
  const router = useRouter();

  useLayoutEffect(() => {
    if (loggedIn) {
      router.push("/profile");
    }
  });

  const [signup, { loading, data }] = useSignupMutation({
    onCompleted(signupData) {
      if (!signupData || signupData.register.__typename !== "RegisterSuccess") {
        return;
      }

      setLoggedIn(true);

      router.push("/profile");
    },
  });

  const [formState, { email, password }] = useFormState<SignupFormProps>(
    {},
    {
      withIds: true,
    },
  );

  const onFormSubmit = useCallback(
    (e) => {
      e.preventDefault();
      signup({
        variables: { input: formState.values },
      });
    },
    [signup, formState],
  );

  const errorMessage = getErrorMessageIfAny(data?.register?.__typename);

  const getFieldErrors = (field: "email" | "password") =>
    (data &&
      data.register.__typename === "RegisterValidationError" &&
      (data.register.errors[field] ?? []).map((e) => e.message)) ||
    [];

  // TODO reuse from login page (or make it visible in all pages)
  // {location?.state?.message && (
  //   <Alert variant="alert">{location.state.message}</Alert>
  // )}

  return (
    <Box
      sx={{
        px: 3,
      }}
    >
      {errorMessage && <Alert variant="alert">{errorMessage}</Alert>}

      <Grid
        gap={5}
        sx={{
          maxWidth: "container",
          mx: "auto",
          mt: 3,
          gridTemplateColumns: [null, null, "1fr 1fr"],
        }}
      >
        <form onSubmit={onFormSubmit} method="post">
          <Text mb={4} as="h2">
            <FormattedMessage id="signup.signupWithEmail" />
          </Text>

          <InputWrapper
            sx={{ mb: 0 }}
            errors={getFieldErrors("email")}
            label={<FormattedMessage id="signup.email" />}
          >
            <Input
              {...email("email")}
              placeholder="guido@python.org"
              required={true}
              type="email"
              tabIndex={1}
            />
          </InputWrapper>

          <Link
            sx={{
              display: "block",
              mb: 4,
            }}
            path={`/login/`}
          >
            <FormattedMessage id="signup.alreadyHaveAccount" />
          </Link>

          <InputWrapper
            errors={getFieldErrors("password")}
            label={<FormattedMessage id="signup.password" />}
          >
            <Input
              {...password("password")}
              required={true}
              type="password"
              tabIndex={2}
              mb={4}
            />
          </InputWrapper>

          <Button type="submit" loading={loading}>
            <FormattedMessage id="signup.signupButton" />
          </Button>
        </form>
        {/* <Box>
          <Text mb={4} as="h2">
            <FormattedMessage id="signup.signupWithSocial" />
          </Text>

          <Link external={true} path="/login/google/" variant="google">
            <FormattedMessage id="signup.useGoogle" />
          </Link>
        </Box> */}
      </Grid>
    </Box>
  );
};
