/** @jsx jsx */
import { useMutation } from "@apollo/react-hooks";
import { Box, Button, Textarea } from "@theme-ui/components";
import { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { Alert } from "../../components/alert";
import { InputWrapper } from "../../components/input-wrapper";
import {
  SendCommentMutation,
  SendCommentMutationVariables,
  SubmissionQuery,
  SubmissionQueryVariables,
} from "../../generated/graphql-backend";
import SEND_COMMENT from "./send-comment.graphql";
import SUBMISSION from "./submission.graphql";

type Form = {
  comment: string;
};

type Props = {
  submissionId: string;
};

export const AddComment: React.SFC<Props> = ({ submissionId }) => {
  const [formState, { textarea }] = useFormState<Form>();
  const [sendComment, { loading, data: sendCommentData, error }] = useMutation<
    SendCommentMutation,
    SendCommentMutationVariables
  >(SEND_COMMENT, {
    update(cache, { data }) {
      if (
        data?.sendSubmissionComment.__typename === "SendSubmissionCommentErrors"
      ) {
        return;
      }

      const cachedData = cache.readQuery<
        SubmissionQuery,
        SubmissionQueryVariables
      >({
        query: SUBMISSION,
        variables: {
          id: submissionId,
        },
      });

      cache.writeQuery<SubmissionQuery, SubmissionQueryVariables>({
        query: SUBMISSION,
        data: {
          submission: {
            ...cachedData!.submission!,
            comments: [
              ...cachedData!.submission!.comments,
              data!.sendSubmissionComment,
            ],
          },
        },
      });
    },
  });

  const onSubmit = useCallback(
    async e => {
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
    <Box as="form" onSubmit={onSubmit}>
      <InputWrapper sx={{ mb: 2 }} errors={getErrors("validationText")}>
        <Textarea
          sx={{
            resize: "vertical",
            minHeight: 200,
          }}
          {...textarea("comment")}
          required={true}
          maxLength="500"
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

      <Button>
        <FormattedMessage id="submission.sendComment" />
      </Button>
    </Box>
  );
};
