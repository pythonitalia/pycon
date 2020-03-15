/** @jsx jsx */
import { useRouter } from "next/router";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import {
  MeSubmissionsDocument,
  MeSubmissionsQuery,
  MeSubmissionsQueryVariables,
  useSendSubmissionMutation,
} from "~/types";

import { CfpForm, CfpFormFields } from "../cfp-form";

export const Cfp: React.SFC = () => {
  const lang = useCurrentLanguage();
  const code = process.env.conferenceCode;
  const router = useRouter();

  const [sendSubmission, { loading, error, data }] = useSendSubmissionMutation({
    update(cache, { data: updateData }) {
      const query = cache.readQuery<
        MeSubmissionsQuery,
        MeSubmissionsQueryVariables
      >({
        query: MeSubmissionsDocument,
        variables: {
          conference: code,
        },
      });

      if (!query || updateData?.mutationOp.__typename !== "Submission") {
        return;
      }

      cache.writeQuery<MeSubmissionsQuery, MeSubmissionsQueryVariables>({
        query: MeSubmissionsDocument,
        data: {
          me: {
            ...query.me,
            submissions: [...query.me.submissions, updateData!.mutationOp],
          },
        },
        variables: {
          conference: code,
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
      const id = response.data.mutationOp.id;
      router.push(`/[lang]/submission/[id]`, `/${lang}/submission/${id}`);
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
