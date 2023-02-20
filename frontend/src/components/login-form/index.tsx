/** @jsxRuntime classic */

/** @jsx jsx */
import { Text } from "@python-italia/pycon-styleguide";
import { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Grid, Input, jsx, Heading, ThemeUIStyleObject } from "theme-ui";

import Router, { useRouter } from "next/router";

import { useLoginState } from "~/components/profile/hooks";
import { useMessages } from "~/helpers/use-messages";
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
  sx?: ThemeUIStyleObject;
};

const cleanRedirectUrl = (url: string) =>
  url.startsWith("/") ? url : "/profile";

export const LoginForm = ({ next, ...props }: FormProps) => {
  const router = useRouter();
  const [loggedIn, setLoggedIn] = useLoginState();

  const { messages, clearMessages } = useMessages();

  const nextUrl = cleanRedirectUrl(
    (router.query.next as string) || next || `/profile`,
  );

  const onLoginCompleted = (data: LoginMutation) => {
    if (data && data.login.__typename === "LoginSuccess") {
      setLoggedIn(true);
      clearMessages();

      Router.replace(nextUrl);
    }
  };

  const [login, { loading, data: loginData }] = useLoginMutation({
    onCompleted: onLoginCompleted,
  });
  const [formState, { email, password }] = useFormState<LoginFormFields>(
    {},
    {
      withIds: true,
    },
  );

  useEffect(() => {
    if (router.isReady && loggedIn) {
      Router.replace(nextUrl);
    }

    clearMessages();
  }, [router.isReady]);

  const getFieldErrors = (field: "email" | "password") =>
    (loginData &&
      loginData.login.__typename === "LoginValidationError" &&
      (loginData.login.errors[field] ?? []).map((e) => e.message)) ||
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

        {loginData?.login?.__typename === "WrongEmailOrPassword" && (
          <Alert variant="alert">Wrong username or password</Alert>
        )}
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
            clearMessages();

            login({ variables: { input: formState.values } });
          }}
        >
          <Heading as="h2">
            <FormattedMessage id="login.loginWithEmail" />
          </Heading>

          <Text size={1}>
            {nextUrl === "/tickets/checkout" && (
              <FormattedMessage id="login.redirectFromTicketsCheckout" />
            )}
            {nextUrl === "/cfp" && (
              <FormattedMessage id="login.redirectFromCFP" />
            )}
            {nextUrl === "/grants" && (
              <FormattedMessage id="login.redirectFromGrants" />
            )}
            {nextUrl.startsWith("/schedule") && (
              <FormattedMessage id="login.redirectFromSchedule" />
            )}
          </Text>

          <InputWrapper
            sx={{ mt: 4, mb: 0 }}
            errors={getFieldErrors("email")}
            label={<FormattedMessage id="login.email" />}
          >
            <Input
              {...email("email")}
              placeholder="guido@python.org"
              required={true}
              type="email"
              data-testid="email-input"
            />
          </InputWrapper>

          <Link
            sx={{
              display: "block",
              mb: 4,
              textDecoration: "underline",
            }}
            path="/signup"
          >
            <FormattedMessage id="login.dontHaveAccount" />
          </Link>

          <InputWrapper
            sx={{ mb: 0 }}
            errors={getFieldErrors("password")}
            label={<FormattedMessage id="login.password" />}
          >
            <Input
              id="login-password"
              {...password("password")}
              required={true}
              type="password"
              data-testid="password-input"
            />
          </InputWrapper>

          <Link
            sx={{
              display: "block",
              mb: 4,
              textDecoration: "underline",
            }}
            path="/reset-password"
          >
            <FormattedMessage id="login.recoverPassword" />
          </Link>

          <Button type="submit" loading={loading}>
            <FormattedMessage id="login.loginButton" />
          </Button>
        </form>
      </Grid>
    </Box>
  );
};
