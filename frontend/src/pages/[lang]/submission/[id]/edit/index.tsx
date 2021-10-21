/** @jsxRuntime classic */

/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState } from "~/apollo/client";
import { Alert } from "~/components/alert";
import {
  CfpForm,
  CfpFormFields,
  SubmissionStructure,
} from "~/components/cfp-form";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import {
  queryCfpForm,
  queryTags,
  useGetSubmissionQuery,
  useUpdateSubmissionMutation,
} from "~/types";

export const EditSubmissionPage = () => {
  const code = process.env.conferenceCode;
  const router = useRouter();
  const id = router.query.id as string;
  const language = useCurrentLanguage();

  const [
    updateSubmission,
    {
      loading: updateSubmissionLoading,
      error: updateSubmissionError,
      data: updateSubmissionData,
    },
  ] = useUpdateSubmissionMutation();

  const {
    loading: submissionLoading,
    error: submissionError,
    data: submissionData,
  } = useGetSubmissionQuery({ variables: { id } });

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
      router.push(
        "/[lang]/submission/[id]",
        `/${language}/submission/${response.data.mutationOp.id}/`,
      );
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
          submission={submissionData.submission as SubmissionStructure}
          loading={updateSubmissionLoading}
          error={updateSubmissionError}
          data={updateSubmissionData}
          onSubmit={onSubmit}
          conferenceCode={code}
        />
      )}
    </Box>
  );
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const language = params.lang as string;

  await Promise.all([
    prefetchSharedQueries(language),
    queryTags(),
    queryCfpForm({
      conference: process.env.conferenceCode,
    }),
  ]);

  return addApolloState({
    props: {},
    revalidate: 1,
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default EditSubmissionPage;
