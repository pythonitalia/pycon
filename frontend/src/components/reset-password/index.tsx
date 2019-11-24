/** @jsx jsx */

import { useMutation } from "@apollo/react-hooks";
import { navigate, Redirect, RouteComponentProps } from "@reach/router";
import { Box, Button, Flex, Grid, Heading, Input } from "@theme-ui/components";
import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import {
  ResetPasswordMutation,
  ResetPasswordMutationVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { InputWrapper } from "../input-wrapper";
import RESET_PASSWORD_MUTATION from "./reset-password.graphql";

type Props = {
  lang: string;
  userId: string;
  token: string;
};

type FormFields = {
  password: string;
};

export const ResetPassword: React.SFC<RouteComponentProps<Props>> = ({
  lang,
  userId,
  token,
}) => {
  const [changePassword, { loading, error, data }] = useMutation<
    ResetPasswordMutation,
    ResetPasswordMutationVariables
  >(RESET_PASSWORD_MUTATION);
  const [formState, { password }] = useFormState<FormFields>(
    {},
    {
      withIds: true,
    },
  );
  const onSubmit = useCallback(
    e => {
      e.preventDefault();

      if (loading) {
        return;
      }

      changePassword({
        variables: {
          token: token!,
          userId: userId!,
          password: formState.values.password,
        },
      });
    },
    [formState, loading, token, userId],
  );

  if (
    data?.resetPassword.__typename === "OperationResult" &&
    data.resetPassword.ok
  ) {
    return (
      <FormattedMessage id="resetPassword.youCanNowLogin">
        {text => (
          <Redirect
            to={`/${lang}/login`}
            state={{
              message: text,
              messageVariant: "success",
            }}
            noThrow={true}
          />
        )}
      </FormattedMessage>
    );
  }

  const getErrors = (key: "token" | "password") =>
    (data?.resetPassword.__typename === "ResetPasswordMutationErrors" &&
      data?.resetPassword[key]) ||
    [];

  const tokenErrors = getErrors("token");

  return (
    <Box
      as="form"
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
      }}
      onSubmit={onSubmit}
    >
      {error && <Alert variant="alert">{error.message}</Alert>}
      {tokenErrors.length > 0 && (
        <Alert variant="alert">{tokenErrors.join(", ")}</Alert>
      )}

      <Heading mb={4} as="h1">
        <FormattedMessage id="resetPassword.changeYourPassword" />
      </Heading>

      <InputWrapper
        errors={getErrors("password")}
        sx={{
          mb: 3,
        }}
        label={<FormattedMessage id="resetPassword.newPassword" />}
      >
        <Input {...password("password")} />
      </InputWrapper>
      <Button>
        <FormattedMessage id="resetPassword.changePassword" />
      </Button>
    </Box>
  );
};
