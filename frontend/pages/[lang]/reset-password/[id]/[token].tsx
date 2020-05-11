/** @jsx jsx */
import { Box, Button, Heading, Input } from "@theme-ui/components";
import { useRouter } from "next/router";
import { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { InputWrapper } from "~/components/input-wrapper";
import { useMessages } from "~/helpers/use-messages";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useResetPasswordMutation } from "~/types";

type FormFields = {
  password: string;
};

export default () => {
  const router = useRouter();
  const language = useCurrentLanguage();
  const [_, addMessage] = useMessages();
  const successMessage = useTranslatedMessage("resetPassword.youCanNowLogin");

  const [changePassword, { loading, error, data }] = useResetPasswordMutation({
    onCompleted(data) {
      if (
        data?.resetPassword.__typename === "OperationResult" &&
        data.resetPassword.ok
      ) {
        addMessage({
          message: successMessage,
          type: "success",
        });

        router.push("/[lang]/login", `/${language}/login`);
      }
    },
  });
  const [formState, { password }] = useFormState<FormFields>(
    {},
    {
      withIds: true,
    },
  );

  const token = router.query.token as string;
  const userId = router.query.userId as string;

  const onSubmit = useCallback(
    (e) => {
      e.preventDefault();

      if (loading) {
        return;
      }

      changePassword({
        variables: {
          token,
          userId,
          password: formState.values.password,
        },
      });
    },
    [formState, loading, token, userId],
  );

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
