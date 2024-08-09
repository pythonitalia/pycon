import { Page, Section } from "@python-italia/pycon-styleguide";
import type { GetServerSideProps } from "next";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import {
  CfpForm,
  type CfpFormFields,
  type SubmissionStructure,
} from "~/components/cfp-form";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import {
  queryCfpForm,
  queryGetSubmission,
  queryIsCfpOpen,
  queryParticipantData,
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

  const { error: submissionError, data: submissionData } =
    useGetSubmissionQuery({ variables: { id, language } });

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
          speakerWebsite: input.participantWebsite,
          speakerBio: input.participantBio,
          speakerPhoto: input.participantPhoto,
          speakerTwitterHandle: input.participantTwitterHandle,
          speakerInstagramHandle: input.participantInstagramHandle,
          speakerLinkedinUrl: input.participantLinkedinUrl,
          speakerFacebookUrl: input.participantFacebookUrl,
          speakerMastodonHandle: input.participantMastodonHandle,
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

export const getServerSideProps: GetServerSideProps = async ({
  req,
  params,
  locale,
}) => {
  const identityToken = req.cookies.pythonitalia_sessionid;
  if (!identityToken) {
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  const id = params.id as string;
  const client = getApolloClient(null, req.cookies);
  try {
    await Promise.all([
      prefetchSharedQueries(client, locale),
      queryIsCfpOpen(client, {
        conference: process.env.conferenceCode,
      }),
      queryParticipantData(client, {
        conference: process.env.conferenceCode,
      }),
      queryCfpForm(client, {
        conference: process.env.conferenceCode,
      }),
      queryTags(client),
      queryGetSubmission(client, {
        id,
        language: locale,
      }),
    ]);
  } catch (e) {
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  return addApolloState(
    client,
    {
      props: {},
    },
    null,
  );
};

export default EditSubmissionPage;
