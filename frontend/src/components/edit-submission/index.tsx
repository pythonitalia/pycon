/** @jsx jsx */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { navigate, RouteComponentProps } from "@reach/router";
import { Box } from "@theme-ui/components";
import React, { useContext } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { ConferenceContext } from "../../context/conference";
import { useCurrentLanguage } from "../../context/language";
import {
  GetSubmissionQuery,
  GetSubmissionQueryVariables,
  UpdateSubmissionMutation,
  UpdateSubmissionMutationVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { CfpForm, CfpFormFields } from "../cfp-form";
import GET_SUBMISSION from "./get-submission.graphql";
import UPDATE_SUBMISSION from "./update-submission.graphql";

type Props = {
  id: string;
};

export const EditSubmission: React.SFC<RouteComponentProps<Props>> = ({
  id,
}) => {
  const lang = useCurrentLanguage();
  const conferenceCode = useContext(ConferenceContext);
  const [
    updateSubmission,
    {
      loading: updateSubmissionLoading,
      error: updateSubmissionError,
      data: updateSubmissionData,
    },
  ] = useMutation<UpdateSubmissionMutation, UpdateSubmissionMutationVariables>(
    UPDATE_SUBMISSION,
    {
      update(cache, { data }) {
        const query = cache.readQuery<
          GetSubmissionQuery,
          GetSubmissionQueryVariables
        >({
          query: GET_SUBMISSION,
          variables: {
            id: id!,
          },
        });

        if (!query || data?.mutationOp.__typename !== "Submission") {
          return;
        }

        cache.writeQuery<GetSubmissionQuery, GetSubmissionQueryVariables>({
          query: GET_SUBMISSION,
          data: {
            submission: {
              ...query.submission!,
              ...data!.mutationOp,
            },
          },
          variables: {
            id: id!,
          },
        });
      },
    },
  );

  const {
    loading: submissionLoading,
    error: submissionError,
    data: submissionData,
  } = useQuery<GetSubmissionQuery, GetSubmissionQueryVariables>(
    GET_SUBMISSION,
    {
      variables: {
        id: id!,
      },
    },
  );

  const onSubmit = async (input: CfpFormFields) => {
    const response = await updateSubmission({
      variables: {
        input: {
          instance: id!,
          title: input.title,
          abstract: input.abstract,
          topic: input.topic,
          languages: input.languages,
          type: input.type,
          duration: input.length,
          elevatorPitch: input.elevatorPitch,
          notes: input.notes,
          audienceLevel: input.audienceLevel,
          tags: input.tags,
          speakerLevel: input.speakerLevel,
          previousTalkVideo: input.previousTalkVideo,
        },
      },
    });

    if (response.data?.mutationOp.__typename === "Submission") {
      navigate(`/${lang}/submission/${response.data.mutationOp.id}/`);
    }
  };

  return (
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
      }}
    >
      {submissionError && (
        <Alert variant="alert">{submissionError.message}</Alert>
      )}
      {submissionLoading && (
        <Alert variant="info">
          <FormattedMessage id="cfp.loading" />
        </Alert>
      )}
      {submissionData && !submissionData.submission?.canEdit && (
        <Alert variant="alert">
          <FormattedMessage id="cfp.cannotEdit" />
        </Alert>
      )}
      {submissionData && submissionData.submission?.canEdit && (
        <CfpForm
          submission={submissionData.submission}
          loading={updateSubmissionLoading}
          error={updateSubmissionError}
          data={updateSubmissionData}
          onSubmit={onSubmit}
          conferenceCode={conferenceCode}
        />
      )}
    </Box>
  );
};
