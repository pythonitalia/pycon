import { useMutation } from "@apollo/react-hooks";
import { navigate, Redirect, RouteComponentProps } from "@reach/router";
import { Box, Button, Grid, Input, Label, Text } from "@theme-ui/components";
import React from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useLoginState } from "../../app/profile/hooks";
import {
  LoginMutation,
  LoginMutationVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { InputWrapper } from "../input-wrapper";
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

  const getFieldErrors = (field: "validationEmail" | "validationPassword") =>
    (loginData &&
      loginData.login.__typename === "LoginErrors" &&
      loginData.login[field]) ||
    [];

  return (
    <Box
      sx={{
        px: 2,
      }}
    >
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          mb: 3,
        }}
      >
        {location?.state?.message && (
          <Alert variant={location.state.messageVariant || "alert"}>
            {location.state.message}
          </Alert>
        )}
        {errorMessage && <Alert variant="alert">{errorMessage}</Alert>}
      </Box>
      <Grid
        sx={{
          maxWidth: "container",
          mx: "auto",
          mt: 3,
          gridTemplateColumns: [null, null, "1fr 1fr"],
          gridColumnGap: 5,
        }}
      >
        <Box
          as="form"
          method="post"
          onSubmit={(e: React.FormEvent<HTMLFormElement>) => {
            e.preventDefault();

            login({ variables: formState.values });
          }}
        >
          <Text mb={4} as="h2">
            <FormattedMessage id="login.loginWithEmail" />
          </Text>

          <InputWrapper
            errors={getFieldErrors("validationEmail")}
            label={<FormattedMessage id="login.email" />}
          >
            <Input
              {...email("email")}
              placeholder="guido@python.org"
              required={true}
              type="email"
              mb={4}
            />
          </InputWrapper>

          <InputWrapper
            sx={{ mb: 0 }}
            errors={getFieldErrors("validationPassword")}
            label={<FormattedMessage id="login.password" />}
          >
            <Input
              id="login-password"
              {...password("password")}
              required={true}
              type="password"
            />
          </InputWrapper>

          <Link
            sx={{
              display: "block",
              mb: 4,
            }}
            href={`/${lang}/reset-password/`}
          >
            <FormattedMessage id="login.recoverPassword" />
          </Link>

          <Button
            size="medium"
            palette="primary"
            isLoading={loading}
            type="submit"
          >
            <FormattedMessage id="login.loginButton" />
          </Button>
        </Box>
        <Box>
          <Text mb={4} as="h2">
            <FormattedMessage id="login.loginWithSocial" />
          </Text>

          <Button href="/login/google/" as="a">
            <FormattedMessage id="login.useGoogle" />
          </Button>
        </Box>
      </Grid>
    </Box>
  );
};
