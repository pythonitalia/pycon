import {
  Heading,
  Text,
  Page,
  Spacer,
  InputWrapper,
  Input,
  Button,
  Grid,
} from "@python-italia/pycon-styleguide";
import { useRef } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import router from "next/router";

import { PASSWORD_MIN_LENGTH } from "~/helpers/constants";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useResetPasswordMutation } from "~/types";

import { createHref } from "../link";
import { LoginFlowLayout } from "../login-flow-layout";
import { MetaTags } from "../meta-tags";

type FormFields = {
  password: string;
  password2: string;
};

export const ResetPasswordPageHandler = () => {
  const language = useCurrentLanguage();
  const formRef = useRef<HTMLFormElement>();
  const passwordMismatchMessage = useTranslatedMessage(
    "signup.passwordMismatch",
  );
  const [changePassword, { loading, error, data }] = useResetPasswordMutation();
  const [formState, { password }] = useFormState<FormFields>(
    {},
    {
      withIds: true,
    },
  );
  const getErrors = (key: "token" | "newPassword") =>
    (data?.resetPassword.__typename === "ResetPasswordErrors" &&
      (data?.resetPassword.errors[key] ?? [])) ||
    [];

  const onSubmit = async (e) => {
    e.preventDefault();

    if (loading || !formRef.current.reportValidity()) {
      return;
    }

    const token = router.query.token as string;
    const result = await changePassword({
      variables: {
        token,
        password: formState.values.password,
      },
    });

    if (result.data?.resetPassword.__typename === "OperationSuccess") {
      router.push(
        createHref({
          path: "/reset-password/password-changed",
          locale: language,
        }),
      );
    }
  };

  const passwordsAreNotMatching =
    formState.touched.password &&
    formState.touched.password2 &&
    formState.values.password !== formState.values.password2;

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="resetPassword.title">
        {(title) => <MetaTags title={title} />}
      </FormattedMessage>

      <form onSubmit={onSubmit} className="w-full" ref={formRef}>
        <LoginFlowLayout illustration="none">
          <Heading size="display2">
            <FormattedMessage id="resetPassword.changeYourPassword" />
          </Heading>
          <Spacer size="2md" />
          <Text size={2}>
            <FormattedMessage id="resetPassword.changeYourPassword.body" />
          </Text>
          <Spacer size="large" />
          <div className="w-full">
            <Grid cols={2}>
              <InputWrapper
                required
                title={<FormattedMessage id="resetPassword.newPassword" />}
              >
                <Input
                  {...password("password")}
                  placeholder="checkoursocialevents"
                  minLength={PASSWORD_MIN_LENGTH}
                  errors={[
                    ...getErrors("newPassword"),
                    ...getErrors("token"),
                    error?.message,
                  ]}
                  required
                />
              </InputWrapper>
              <InputWrapper
                required
                title={
                  <FormattedMessage id="resetPassword.confirmNewPassword" />
                }
              >
                <Input
                  {...password("password2")}
                  placeholder="checkoursocialevents"
                  minLength={PASSWORD_MIN_LENGTH}
                  errors={
                    passwordsAreNotMatching ? [passwordMismatchMessage] : []
                  }
                  required
                />
              </InputWrapper>
            </Grid>
            <Spacer size="large" />
            <div className="flex justify-end">
              <Button role="secondary" disabled={loading} onClick={onSubmit}>
                <FormattedMessage id="resetPassword.changePassword" />
              </Button>
            </div>
          </div>
        </LoginFlowLayout>
      </form>
    </Page>
  );
};
