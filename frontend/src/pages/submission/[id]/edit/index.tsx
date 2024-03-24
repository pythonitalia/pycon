import { Page, Section } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
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
  } = useGetSubmissionQuery({ variables: { id, language } });

  const onSubmit = async (input: CfpFormFields) => {
    const response = await updateSubmission({
      variables: {
        input: {
          instance: id!,
          title: input.title,
          abstract: input.abstract,
          languages: input.languages,
          type: input.type,
          duration: input.length,
          elevatorPitch: input.elevatorPitch,
          notes: input.notes,
          audienceLevel: input.audienceLevel,
          tags: input.tags,
          speakerLevel: input.speakerLevel,
          previousTalkVideo: input.previousTalkVideo,
          shortSocialSummary: input.shortSocialSummary,
          speakerWebsite: input.speakerWebsite,
          speakerBio: input.speakerBio,
          speakerPhoto: input.speakerPhoto,
          speakerTwitterHandle: input.speakerTwitterHandle,
          speakerInstagramHandle: input.speakerInstagramHandle,
          speakerLinkedinUrl: input.speakerLinkedinUrl,
          speakerFacebookUrl: input.speakerFacebookUrl,
          speakerMastodonHandle: input.speakerMastodonHandle,
        },
        language,
      },
    });

    if (response.data?.mutationOp.__typename === "Submission") {
      router.push(
        "/submission/[id]",
        `/submission/${response.data.mutationOp.id}/`,
      );
    }
  };

  return (
    <Page endSeparator={false}>
      <Section>
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
        {submissionData?.submission?.canEdit && (
          <CfpForm
            submission={submissionData.submission as SubmissionStructure}
            loading={updateSubmissionLoading}
            error={updateSubmissionError}
            data={updateSubmissionData}
            onSubmit={onSubmit}
            conferenceCode={code}
          />
        )}
      </Section>
    </Page>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryTags(client),
    queryCfpForm(client, {
      conference: process.env.conferenceCode,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default EditSubmissionPage;
