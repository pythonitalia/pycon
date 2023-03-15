import {
  Text,
  Button,
  Heading,
  Link,
  Page,
  Spacer,
  InputWrapper,
  Input,
} from "@python-italia/pycon-styleguide";
import { useCallback, useRef } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useRouter } from "next/router";

import { useCurrentLanguage } from "~/locale/context";
import { useRequestPasswordResetMutation } from "~/types";

import { createHref } from "../link";
import { LoginFlowLayout } from "../login-flow-layout";
import { MetaTags } from "../meta-tags";

type FormFields = {
  email: string;
};

export const RequestResetPasswordPageHandler = () => {
  const language = useCurrentLanguage();
  const formRef = useRef<HTMLFormElement>();
  const router = useRouter();
  const [formState, { email }] = useFormState<FormFields>(
    {},
    {
      withIds: true,
    },
  );

  const [sendResetPassword, { loading, error }] =
    useRequestPasswordResetMutation();

  const onSubmit = useCallback(
    async (e) => {
      e.preventDefault();

      if (loading || !formState.validity || !formRef.current.reportValidity()) {
        return;
      }

      const response = await sendResetPassword({
        variables: {
          email: formState.values.email,
        },
      });
      if (
        response.data.requestResetPassword.__typename === "OperationSuccess"
      ) {
        router.push(
          createHref({
            path: "/reset-password/success",
            locale: language,
          }),
        );
      }
    },
    [loading, formState],
  );

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="requestResetPassword.title">
        {(title) => <MetaTags title={title} />}
      </FormattedMessage>

      <form onSubmit={onSubmit} ref={formRef} className="w-full">
        <LoginFlowLayout
          bottomSection={
            <>
              <Text size={3}>
                <FormattedMessage
                  id="requestResetPassword.backToLogin"
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
                          <FormattedMessage id="requestResetPassword.backToLogin.login" />
                        </Text>
                      </Link>
                    ),
                  }}
                />
              </Text>
              <Button
                role="secondary"
                disabled={loading}
                onClick={onSubmit}
                data-testid="login-button"
              >
                <FormattedMessage id="requestResetPassword.button" />
              </Button>
            </>
          }
        >
          <Heading size="display2">
            <FormattedMessage id="requestResetPassword.passwordForgotten" />
          </Heading>
          <Spacer size="large" />
          <div className="w-full">
            <InputWrapper
              required
              title={<FormattedMessage id="requestResetPassword.email" />}
            >
              <Input
                {...email("email")}
                placeholder="grace.hopper@pycon.it"
                data-testid="email-input"
                required={true}
                errors={[error?.message]}
              />
            </InputWrapper>
          </div>
        </LoginFlowLayout>
      </form>
    </Page>
  );
};
