/** @jsx jsx */
import { useRouter } from "next/router";
import React, { useCallback, useLayoutEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Grid, Input, jsx, Text } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";
import { useCurrentLanguage } from "~/locale/context";
import { useSignupMutation } from "~/types";

import { Alert } from "../alert";
import { Button } from "../button/button";
import { InputWrapper } from "../input-wrapper";
import { Link } from "../link";

type SignupFormProps = {
  email: string;
  password: string;
};

export const SignupForm: React.SFC = () => {
  const [loggedIn, setLoggedIn] = useLoginState();
  const language = useCurrentLanguage();
  const router = useRouter();

  useLayoutEffect(() => {
    if (loggedIn) {
      router.push("/[lang]/profile", `/${language}/profile`);
    }
  });

  const [signup, { loading, error, data }] = useSignupMutation({
    onCompleted(signupData) {
      if (!signupData || signupData.register.__typename !== "MeUser") {
        return;
      }

      setLoggedIn(true);

      router.push("/[lang]/profile", `/${language}/profile`);
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
        variables: formState.values,
      });
    },
    [signup, formState],
  );

  const errorMessage =
    data && data.register.__typename === "RegisterErrors"
      ? data.register.nonFieldErrors.join(" ")
      : (error || "").toString();

  const getFieldErrors = (field: "validationEmail" | "validationPassword") =>
    (data &&
      data.register.__typename === "RegisterErrors" &&
      data.register[field]) ||
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
            errors={getFieldErrors("validationEmail")}
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
            path={`/[lang]/login/`}
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
              tabIndex={2}
              mb={4}
            />
          </InputWrapper>

          <Button type="submit" loading={loading}>
            <FormattedMessage id="signup.signupButton" />
          </Button>
        </form>
        <Box>
          <Text mb={4} as="h2">
            <FormattedMessage id="signup.signupWithSocial" />
          </Text>

          <Link path="/login/google/" variant="google">
            <FormattedMessage id="signup.useGoogle" />
          </Link>
        </Box>
      </Grid>
    </Box>
  );
};
