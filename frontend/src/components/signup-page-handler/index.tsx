import {
  Button,
  Checkbox,
  Grid,
  GridColumn,
  Heading,
  HorizontalStack,
  Input,
  InputWrapper,
  Link,
  Page,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import React, { useCallback, useLayoutEffect, useRef } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useRouter } from "next/router";

import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { PASSWORD_MIN_LENGTH } from "~/helpers/constants";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useSignupMutation } from "~/types";

import { createHref } from "../link";
import { LoginFlowLayout } from "../login-flow-layout";

type SignupFormProps = {
  fullname: string;
  email: string;
  password: string;
  password2: string;
  acceptPrivacyPolicy: boolean;
};

const getErrorMessageIfAny = (typename?: string) => {
  const existingAccountMessage = useTranslatedMessage("signup.existingAccount");

  switch (typename) {
    case "EmailAlreadyUsed":
      return existingAccountMessage;
    default:
      return null;
  }
};

export const SignupPageHandler = () => {
  const language = useCurrentLanguage();
  const passwordMismatchMessage = useTranslatedMessage(
    "signup.passwordMismatch",
  );
  const formRef = useRef<HTMLFormElement>();
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

  const [formState, { text, email, password, checkbox }] =
    useFormState<SignupFormProps>(
      {},
      {
        withIds: true,
      },
    );

  const passwordsAreNotMatching =
    formState.touched.password &&
    formState.touched.password2 &&
    formState.values.password !== formState.values.password2;

  const onFormSubmit = useCallback(
    (e) => {
      e.preventDefault();
      if (!formRef.current.reportValidity()) {
        return;
      }

      if (passwordsAreNotMatching) {
        return;
      }

      const email = formState.values.email;
      const password = formState.values.password;
      const fullname = formState.values.fullname;

      signup({
        variables: {
          input: {
            email,
            password,
            fullname,
          },
        },
      });
    },
    [signup, formState, passwordsAreNotMatching],
  );

  const errorMessage = getErrorMessageIfAny(data?.register?.__typename);

  const getFieldErrors = (field: "email" | "password" | "fullname") =>
    (data &&
      data.register.__typename === "RegisterErrors" &&
      (data.register.errors[field] ?? [])) ||
    [];

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="signup.title">
        {(title) => <MetaTags title={title} />}
      </FormattedMessage>
      <form
        onSubmit={onFormSubmit}
        method="post"
        className="w-full"
        ref={formRef}
      >
        <LoginFlowLayout
          bottomSection={
            <>
              <Text size={3}>
                <FormattedMessage
                  id="signup.alreadyHaveAccount"
                  values={{
                    loginLink: (
                      <Link
                        href={createHref({
                          path: "/login",
                          locale: language,
                        })}
                      >
                        <Text
                          decoration="underline"
                          size={3}
                          weight="strong"
                          color="none"
                        >
                          <FormattedMessage id="signup.alreadyHaveAccount.login" />
                        </Text>
                      </Link>
                    ),
                  }}
                />
              </Text>
              <Button
                onClick={onFormSubmit}
                disabled={loading}
                fullWidth="mobile"
              >
                <FormattedMessage id="signup.signupButton" />
              </Button>
            </>
          }
        >
          <div className="w-full">
            <Heading size="display2">
              <FormattedMessage id="signup.signupWithEmail" />
            </Heading>
            <Spacer size="large" />
            <Grid fullWidth cols={2}>
              <InputWrapper
                required={true}
                title={<FormattedMessage id="signup.fullname" />}
              >
                <Input
                  {...text("fullname")}
                  placeholder="Ada Lovelace"
                  required={true}
                  type="text"
                  tabIndex={0}
                  errors={getFieldErrors("fullname")}
                />
              </InputWrapper>

              <InputWrapper
                required={true}
                title={<FormattedMessage id="signup.email" />}
              >
                <Input
                  {...email("email")}
                  placeholder="ada@pycon.it"
                  required={true}
                  type="email"
                  tabIndex={0}
                  errors={[...getFieldErrors("email"), errorMessage]}
                />
              </InputWrapper>

              <InputWrapper
                required={true}
                title={<FormattedMessage id="signup.password" />}
              >
                <Input
                  {...password("password")}
                  required={true}
                  type="password"
                  placeholder="buyyourticket!"
                  tabIndex={0}
                  minLength={PASSWORD_MIN_LENGTH}
                  errors={getFieldErrors("password")}
                />
              </InputWrapper>

              <InputWrapper
                required={true}
                title={<FormattedMessage id="signup.password2" />}
              >
                <Input
                  {...password("password2")}
                  required={true}
                  type="password"
                  placeholder="becomeamember"
                  tabIndex={0}
                  minLength={PASSWORD_MIN_LENGTH}
                  errors={
                    passwordsAreNotMatching ? [passwordMismatchMessage] : []
                  }
                />
              </InputWrapper>

              <GridColumn colSpan={2}>
                <label>
                  <HorizontalStack gap="medium" alignItems="center">
                    <Checkbox
                      {...checkbox("acceptPrivacyPolicy")}
                      required
                      size="small"
                    />
                    <Text as="span" size={3}>
                      <FormattedMessage
                        id="signup.acceptPrivacyPolicy"
                        values={{
                          privacyPolicyLink: (
                            <Link
                              href={createHref({
                                path: "/privacy-policy",
                                locale: language,
                              })}
                            >
                              <Text
                                size={3}
                                decoration="underline"
                                color="none"
                              >
                                <FormattedMessage id="signup.privacyPolicy" />
                              </Text>
                            </Link>
                          ),
                        }}
                      />
                      *
                    </Text>
                  </HorizontalStack>
                </label>
              </GridColumn>
            </Grid>
          </div>
        </LoginFlowLayout>
      </form>
    </Page>
  );
};
