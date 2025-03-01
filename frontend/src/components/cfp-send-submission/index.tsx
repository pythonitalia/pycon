import React from "react";

import { useRouter } from "next/router";

import { CfpForm, type CfpFormFields } from "~/components/cfp-form";
import { useCurrentLanguage } from "~/locale/context";
import {
  type SendSubmissionMutation,
  readMeSubmissionsQueryCache,
  useSendSubmissionMutation,
  writeMeSubmissionsQueryCache,
} from "~/types";

export const CfpSendSubmission = () => {
  const code = process.env.conferenceCode;
  const router = useRouter();
  const language = useCurrentLanguage();

  const [sendSubmission, { loading, error, data }] = useSendSubmissionMutation({
    update(cache, { data: updateData }) {
      const query = readMeSubmissionsQueryCache<SendSubmissionMutation>({
        cache,
        variables: {
          conference: code,
          language,
        },
      });

      if (!query || updateData?.mutationOp.__typename !== "Submission") {
        return;
      }

      writeMeSubmissionsQueryCache<SendSubmissionMutation>({
        cache,
        variables: {
          conference: code,
          language,
        },
        data: {
          me: {
            ...query.me,
            submissions: [...query.me.submissions, updateData!.mutationOp],
          },
        },
      });
    },
  });

  const onSubmit = async (input: CfpFormFields) => {
    if (loading) {
      return;
    }

    const response = await sendSubmission({
      variables: {
        input: {
          conference: code,
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
          speakerAvailabilities: input.speakerAvailabilities,
        },
        language,
      },
    });

    if (response.data?.mutationOp.__typename === "Submission") {
      const id = response.data.mutationOp.id;
      router.push("/submission/[id]", `/submission/${id}`);
    }
  };

  return (
    <CfpForm
      loading={loading}
      error={error}
      data={data}
      conferenceCode={code}
      onSubmit={onSubmit}
    />
  );
};
