/** @jsxRuntime classic */

/** @jsx jsx */
import { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Heading, Input, jsx } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";

import { addApolloState } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { Button } from "~/components/button/button";
import { InputWrapper } from "~/components/input-wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useRequestPasswordResetMutation } from "~/types";

type FormFields = {
  email: string;
};

export const RequestResetPasswordPage = () => {
  const [formState, { email }] = useFormState<FormFields>(
    {},
    {
      withIds: true,
    },
  );

  const [sendResetPassword, { loading, error, data }] =
    useRequestPasswordResetMutation();

  const onSubmit = useCallback(
    (e) => {
      e.preventDefault();
      if (loading || !formState.validity) {
        return;
      }

      sendResetPassword({
        variables: {
          email: formState.values.email,
        },
      });
    },
    [loading, formState],
  );

  return (
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
      }}
    >
      <Heading mb={4} as="h1">
        <FormattedMessage id="requestResetPassword.passwordForgotten" />
      </Heading>

      {loading && (
        <Alert
          sx={{
            mb: 3,
          }}
          variant="info"
        >
          <FormattedMessage id="login.waitWhileSendingResetPasswordRequest" />
        </Alert>
      )}

      {error && (
        <Alert
          sx={{
            mb: 3,
          }}
          variant="alert"
        >
          {error.message}
        </Alert>
      )}

      {data?.requestResetPassword.__typename === "OperationSuccess" &&
        data.requestResetPassword.ok && (
          <Alert
            sx={{
              mb: 3,
            }}
            variant="success"
          >
            <FormattedMessage id="login.checkYourEmails" />
          </Alert>
        )}

      <Box as="form" onSubmit={onSubmit}>
        <InputWrapper
          label={<FormattedMessage id="requestResetPassword.email" />}
        >
          <Input required={true} {...email("email")} />
        </InputWrapper>
        <Button loading={loading}>Send email</Button>
      </Box>
    </Box>
  );
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const lang = params.lang as string;

  await prefetchSharedQueries(lang);

  return addApolloState({
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default RequestResetPasswordPage;
