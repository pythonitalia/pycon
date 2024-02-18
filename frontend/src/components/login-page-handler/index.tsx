import {
  BasicButton,
  Button,
  Grid,
  Heading,
  Input,
  InputWrapper,
  Link,
  Page,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import React, { useEffect, useRef } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useRouter } from "next/router";

import { MetaTags } from "~/components/meta-tags";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { LoginMutation, useLoginMutation } from "~/types";

import { createHref } from "../link";
import { LoginFlowLayout } from "../login-flow-layout";
import { useLoginState } from "../profile/hooks";

type LoginFormFields = {
  email: string;
  password: string;
};

const cleanRedirectUrl = (url: string) =>
  url.startsWith("/") ? url : "/profile";

export const LoginPageHandler = () => {
  const router = useRouter();
  const language = useCurrentLanguage();
  const [loggedIn, setLoggedIn] = useLoginState();
  const formRef = useRef<HTMLFormElement>();

  const nextUrl = cleanRedirectUrl((router.query.next as string) || "/profile");

  const onLoginCompleted = (data: LoginMutation) => {
    if (data && data.login.__typename === "LoginSuccess") {
      setLoggedIn(true);

      router.replace(nextUrl);
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
      router.replace(nextUrl);
    }
  }, [router.isReady]);

  const onLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formRef.current.reportValidity()) {
      return;
    }
    login({ variables: { input: formState.values } });
  };

  const getFieldErrors = (field: "email" | "password") =>
    (loginData &&
      loginData.login.__typename === "LoginErrors" &&
      (loginData.login.errors[field] ?? [])) ||
    [];

  const wrongCredentialsMessage = useTranslatedMessage(
    "login.wrongCredentials",
  );
  const loginError =
    loginData?.login?.__typename === "WrongEmailOrPassword"
      ? wrongCredentialsMessage
      : "";

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="login.title">
        {(title) => <MetaTags title={title} />}
      </FormattedMessage>

      <form onSubmit={onLogin} className="w-full" ref={formRef}>
        <LoginFlowLayout
          bottomSection={
            <>
              <Text size={3}>
                <FormattedMessage
                  id="login.dontHaveAccount"
                  values={{
                    createLink: (
                      <Link
                        href={createHref({
                          path: "/signup",
                          locale: language,
                        })}
                      >
                        <Text
                          decoration="underline"
                          size={3}
                          weight="strong"
                          color="none"
                        >
                          <FormattedMessage id="login.dontHaveAccount.create" />
                        </Text>
                      </Link>
                    ),
                  }}
                />
              </Text>
              <Button onClick={onLogin} disabled={loading} fullWidth="mobile">
                <FormattedMessage id="login.loginButton" />
              </Button>
            </>
          }
        >
          <div className="w-full">
            <Heading size="display2">
              <FormattedMessage id="login.title" />
            </Heading>
            <Spacer size="large" />
            <Heading size={2}>
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
            <Spacer size="large" />
            <Grid fullWidth cols={2}>
              <InputWrapper
                required
                title={<FormattedMessage id="login.email" />}
              >
                <Input
                  {...email("email")}
                  placeholder="guido@python.org"
                  data-testid="email-input"
                  required={true}
                  errors={[...getFieldErrors("email"), loginError]}
                />
              </InputWrapper>

              <InputWrapper
                required
                title={<FormattedMessage id="login.password" />}
              >
                <Input
                  {...password("password")}
                  placeholder="ilovepyconit"
                  data-testid="password-input"
                  required={true}
                  errors={getFieldErrors("password")}
                />
              </InputWrapper>
              <div />
              <div className="text-right">
                <BasicButton
                  href={createHref({
                    path: "/reset-password",
                    locale: language,
                  })}
                >
                  <FormattedMessage id="login.recoverPassword" />
                </BasicButton>
              </div>
            </Grid>
          </div>
        </LoginFlowLayout>
      </form>
    </Page>
  );
};
