/** @jsx jsx */
import { useMutation } from "@apollo/react-hooks";
import { navigate, Redirect, RouteComponentProps } from "@reach/router";
import {
  Box,
  Button,
  Flex,
  Grid,
  Heading,
  Input,
  Text,
} from "@theme-ui/components";
import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import {
  RequestPasswordResetMutation,
  RequestPasswordResetMutationVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { InputWrapper } from "../input-wrapper";
import REQUEST_PASSWORD_RESET_MUTATION from "./request-password-reset.graphql";

type Props = {
  lang: string;
};

type FormFields = {
  email: string;
};

export const RequestPasswordReset: React.SFC<RouteComponentProps<Props>> = ({
  lang,
}) => {
  const [formState, { email }] = useFormState<FormFields>(
    {},
    {
      withIds: true,
    },
  );

  const [sendResetPassword, { loading, error, data }] = useMutation<
    RequestPasswordResetMutation,
    RequestPasswordResetMutationVariables
  >(REQUEST_PASSWORD_RESET_MUTATION);

  const onSubmit = useCallback(
    e => {
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

      {data?.requestPasswordReset.__typename === "OperationResult" &&
        data.requestPasswordReset.ok && (
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
        <Button>Send email</Button>
      </Box>
    </Box>
  );
};
