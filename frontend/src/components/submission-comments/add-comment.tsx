/** @jsx jsx */
import { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, jsx, Textarea } from "theme-ui";

import { Alert } from "~/components/alert";
import { InputWrapper } from "~/components/input-wrapper";
import { useSendCommentMutation } from "~/types";

import { Button } from "../button/button";

type Form = {
  comment: string;
};

type Props = {
  submissionId: string;
};

export const AddComment: React.SFC<Props> = ({ submissionId }) => {
  const [formState, { textarea }] = useFormState<Form>();
  const [
    sendComment,
    { loading, data: sendCommentData, error },
  ] = useSendCommentMutation();

  const onSubmit = useCallback(
    async (e) => {
      e.preventDefault();

      if (loading) {
        return;
      }

      const response = await sendComment({
        variables: {
          input: {
            text: formState.values.comment,
            submission: submissionId,
          },
        },
      });

      if (
        response.data?.sendSubmissionComment.__typename === "SubmissionComment"
      ) {
        formState.clear();
      }
    },
    [formState.values, loading],
  );

  const getErrors = (key: "validationText" | "nonFieldErrors") =>
    (sendCommentData?.sendSubmissionComment.__typename ===
      "SendSubmissionCommentErrors" &&
      sendCommentData.sendSubmissionComment[key]) ||
    [];

  const genericErrors = getErrors("nonFieldErrors");

  return (
    <Box as="form" onSubmit={onSubmit} sx={{ mb: 4 }}>
      <InputWrapper sx={{ mb: 2 }} errors={getErrors("validationText")}>
        <Textarea
          sx={{
            resize: "vertical",
            minHeight: 200,
          }}
          {...textarea("comment")}
          required={true}
          maxLength={500}
        />
      </InputWrapper>

      {error && <Alert variant="alert">{error.message}</Alert>}

      {genericErrors.length > 0 && (
        <Alert variant="alert">{genericErrors.join(",")}</Alert>
      )}

      {loading && (
        <Alert variant="info">
          <FormattedMessage id="submission.pleaseWait" />
        </Alert>
      )}

      <Button loading={loading}>
        <FormattedMessage id="submission.sendComment" />
      </Button>
    </Box>
  );
};
