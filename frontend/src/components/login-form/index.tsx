/** @jsx jsx */
import { Box, Grid, Input, Text } from "@theme-ui/components";
import Router, { useRouter } from "next/router";
import { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";
import { useMessages } from "~/helpers/use-messages";
import { useCurrentLanguage } from "~/locale/context";
import { LoginMutation, useLoginMutation } from "~/types";

import { Alert } from "../alert";
import { Button } from "../button/button";
import { InputWrapper } from "../input-wrapper";
import { Link } from "../link";

type LoginFormFields = {
  email: string;
  password: string;
};

type FormProps = {
  next?: string;
};

export const LoginForm: React.SFC<FormProps> = ({ next, ...props }) => {
  const lang = useCurrentLanguage();
  const router = useRouter();
  const [loggedIn, setLoggedIn] = useLoginState();

  // TODO: move this to parent layout?
  const [messages, _, clearMessages] = useMessages();

  const nextUrl = (router.query.next as string) || next || `/${lang}/profile`;

  const onLoginCompleted = (data: LoginMutation) => {
    if (data && data.login.__typename === "MeUser") {
      setLoggedIn(true);

      Router.push(nextUrl.replace(/^\/(en|it)/, "/[lang]"), nextUrl);
    }
  };

  const [login, { loading, error, data: loginData }] = useLoginMutation({
    onCompleted: onLoginCompleted,
  });
  const [formState, { email, password }] = useFormState<LoginFormFields>(
    {},
    {
      withIds: true,
    },
  );

  useEffect(() => {
    if (loggedIn) {
      Router.push(nextUrl.replace(/^\/(en|it)/, "/[lang]"), nextUrl);
    }

    clearMessages();
  });

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
        px: 3,
      }}
      {...props}
    >
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          mb: 3,
        }}
      >
        {messages.map((message) => (
          <Alert variant={message.type} key={message.message}>
            {message.message}
          </Alert>
        ))}

        {errorMessage && <Alert variant="alert">{errorMessage}</Alert>}
      </Box>
      <Grid
        gap={5}
        sx={{
          maxWidth: "container",
          mx: "auto",
          mt: 3,
          gridTemplateColumns: [null, null, "1fr 1fr"],
        }}
      >
        <form
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
            sx={{ mb: 0 }}
            errors={getFieldErrors("validationEmail")}
            label={<FormattedMessage id="login.email" />}
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
            path={`/${lang}/signup/`}
          >
            <FormattedMessage id="login.dontHaveAccount" />
          </Link>

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
            path={`/${lang}/reset-password/`}
          >
            <FormattedMessage id="login.recoverPassword" />
          </Link>

          <Button type="submit" loading={loading}>
            <FormattedMessage id="login.loginButton" />
          </Button>
        </form>
        <Box>
          <Text mb={4} as="h2">
            <FormattedMessage id="login.loginWithSocial" />
          </Text>

          <Link path="/login/google/" variant="google">
            <FormattedMessage id="login.useGoogle" />
          </Link>
        </Box>
      </Grid>
    </Box>
  );
};
