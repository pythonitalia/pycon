import type { ApolloError } from "@apollo/client";
import {
  Button,
  CardPart,
  Checkbox,
  Grid,
  Heading,
  HorizontalStack,
  Input,
  InputWrapper,
  Link,
  MultiplePartsCard,
  Select,
  Spacer,
  Text,
  Textarea,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import type React from "react";
import { Fragment, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useCurrentLanguage } from "~/locale/context";
import {
  type MultiLingualInput as MultiLingualInputType,
  type SendSubmissionMutation,
  type UpdateSubmissionMutation,
  useCfpFormQuery,
  useParticipantDataQuery,
} from "~/types";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { createHref } from "../link";
import { MultiLingualInput } from "../multilingual-input";
import {
  type ParticipantFormFields,
  PublicProfileCard,
} from "../public-profile-card";
import { TagsSelect } from "../tags-select";
import { AboutYouSection } from "./about-you-section";
import { AvailabilitySection } from "./availability-section";
import { ProposalSection } from "./proposal-section";

export type CfpFormFields = ParticipantFormFields & {
  type: string;
  title: { it?: string; en?: string };
  elevatorPitch: { it?: string; en?: string };
  length: string;
  audienceLevel: string;
  abstract: { it?: string; en?: string };
  notes: string;
  languages: string[];
  tags: string[];
  speakerLevel: string;
  previousTalkVideo: string;
  shortSocialSummary: string;
  acceptedPrivacyPolicy: boolean;
  selectedAvailabilities: { [time: number]: null | boolean };
};

export type SubmissionStructure = {
  type: { id: string };
  title: string;
  elevatorPitch: string;
  abstract: string;
  multilingualTitle: { it: string; en: string };
  multilingualElevatorPitch: { it: string; en: string };
  multilingualAbstract: { it: string; en: string };
  duration: { id: string };
  audienceLevel: { id: string };
  languages: { code: string }[];
  notes: string;
  previousTalkVideo: string;
  speakerLevel: string;
  tags: { id: string }[];
  shortSocialSummary: string;
};

type Props = {
  onSubmit: (input: CfpFormFields) => void;
  submission?: SubmissionStructure | null;
  conferenceCode: string;
  loading: boolean;
  error: ApolloError | undefined;
  data: SendSubmissionMutation | UpdateSubmissionMutation;
};

const filterOutInactiveLanguages = (
  value: MultiLingualInputType,
  languages: string[],
): MultiLingualInputType => {
  return Object.entries(value).reduce((newDict, [key, value]) => {
    if (!languages.includes(key)) {
      return newDict;
    }

    newDict[key] = value;
    return newDict;
  }, {});
};

export const CfpForm = ({
  onSubmit,
  conferenceCode,
  submission,
  loading: submissionLoading,
  error: submissionError,
  data: submissionData,
}: Props) => {
  const language = useCurrentLanguage();
  const [formState, formOptions] = useFormState<CfpFormFields>(
    {
      title: {
        en: "",
        it: "",
      },
      abstract: {
        en: "",
        it: "",
      },
      elevatorPitch: {
        en: "",
        it: "",
      },
      languages: [],
    },
    {
      withIds: true,
    },
  );

  const { checkbox } = formOptions;

  const { data: conferenceData } = useCfpFormQuery({
    variables: {
      conference: conferenceCode,
    },
  });

  const { data: participantData } = useParticipantDataQuery({
    variables: {
      conference: conferenceCode,
    },
  });

  const submitSubmission = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    onSubmit({
      title: filterOutInactiveLanguages(
        formState.values.title,
        formState.values.languages,
      ),
      abstract: filterOutInactiveLanguages(
        formState.values.abstract,
        formState.values.languages,
      ),
      languages: formState.values.languages,
      type: formState.values.type,
      length: formState.values.length,
      elevatorPitch: filterOutInactiveLanguages(
        formState.values.elevatorPitch,
        formState.values.languages,
      ),
      notes: formState.values.notes,
      audienceLevel: formState.values.audienceLevel,
      tags: formState.values.tags,
      speakerLevel: formState.values.speakerLevel,
      previousTalkVideo: formState.values.previousTalkVideo,
      shortSocialSummary: formState.values.shortSocialSummary,
      participantWebsite: formState.values.participantWebsite,
      participantBio: formState.values.participantBio,
      participantTwitterHandle: formState.values.participantTwitterHandle,
      participantInstagramHandle: formState.values.participantInstagramHandle,
      participantLinkedinUrl: formState.values.participantLinkedinUrl,
      participantFacebookUrl: formState.values.participantFacebookUrl,
      participantMastodonHandle: formState.values.participantMastodonHandle,
      participantPhoto:
        formState.values.participantPhoto ??
        participantData.me.participant?.photoId,
      acceptedPrivacyPolicy: formState.values.acceptedPrivacyPolicy,
    });
  };

  const allowedDurations = conferenceData?.conference.durations.filter(
    (d) =>
      d.allowedSubmissionTypes.findIndex(
        (i) => i.id === formState.values.type,
      ) !== -1,
  );

  useEffect(() => {
    if (!allowedDurations?.length) {
      return;
    }

    // When changing format we need to reset to the first
    // available duration of the new format, but only if the
    // duration is not allowed

    if (
      !allowedDurations.find(
        (duration) => duration.id === formState.values.length,
      )
    ) {
      formState.setField("length", allowedDurations[0].id);
    }
  }, [formState.values.type]);

  useEffect(() => {
    if (submission) {
      formState.setField("type", submission!.type.id);
      formState.setField("title", submission!.multilingualTitle);
      formState.setField(
        "elevatorPitch",
        submission!.multilingualElevatorPitch,
      );
      formState.setField("length", submission!.duration.id);
      formState.setField("audienceLevel", submission!.audienceLevel.id);
      formState.setField(
        "languages",
        submission!.languages.map((l) => l.code),
      );
      formState.setField("abstract", submission!.multilingualAbstract);
      formState.setField("notes", submission!.notes);
      formState.setField(
        "tags",
        submission!.tags.map((t) => t.id),
      );
      formState.setField("shortSocialSummary", submission!.shortSocialSummary);
      formState.setField("acceptedPrivacyPolicy", true);
    }

    if (participantData.me.participant) {
      formState.setField("participantBio", participantData.me.participant.bio);
      formState.setField(
        "participantPhoto",
        participantData.me.participant.photoId,
      );
      formState.setField(
        "speakerLevel",
        participantData.me.participant.speakerLevel,
      );
      formState.setField(
        "previousTalkVideo",
        participantData.me.participant.previousTalkVideo,
      );
      formState.setField(
        "participantWebsite",
        participantData.me.participant.website,
      );
      formState.setField(
        "participantTwitterHandle",
        participantData.me.participant.twitterHandle,
      );
      formState.setField(
        "participantInstagramHandle",
        participantData.me.participant.instagramHandle,
      );
      formState.setField(
        "participantLinkedinUrl",
        participantData.me.participant.linkedinUrl,
      );
      formState.setField(
        "participantFacebookUrl",
        participantData.me.participant.facebookUrl,
      );
      formState.setField(
        "participantMastodonHandle",
        participantData.me.participant.mastodonHandle,
      );
    }
  }, []);

  const hasValidationErrors =
    submissionData?.mutationOp.__typename === "SendSubmissionErrors";

  /* todo refactor to avoid multiple __typename? */
  const getErrors = (
    key:
      | "validationTitle"
      | "validationAbstract"
      | "validationLanguages"
      | "validationType"
      | "validationDuration"
      | "validationElevatorPitch"
      | "validationNotes"
      | "validationAudienceLevel"
      | "validationTags"
      | "validationSpeakerLevel"
      | "validationPreviousTalkVideo"
      | "validationShortSocialSummary"
      | "validationSpeakerBio"
      | "validationSpeakerWebsite"
      | "validationSpeakerPhoto"
      | "validationSpeakerTwitterHandle"
      | "validationSpeakerInstagramHandle"
      | "validationSpeakerLinkedinUrl"
      | "validationSpeakerFacebookUrl"
      | "validationSpeakerMastodonHandle"
      | "nonFieldErrors",
  ): string[] =>
    (submissionData?.mutationOp.__typename === "SendSubmissionErrors" &&
      submissionData!.mutationOp.errors[key]) ||
    [];

  const onChangeAvailability = (date, choice) => {
    formState.setField("selectedAvailabilities", {
      ...formState.values.selectedAvailabilities,
      [date]: choice,
    });
  };

  return (
    <form onSubmit={submitSubmission} autoComplete="off">
      <ProposalSection
        allowedDurations={allowedDurations}
        formState={formState}
        getErrors={getErrors}
        conferenceData={conferenceData}
        formOptions={formOptions}
      />

      <Spacer size="medium" />

      <AboutYouSection getErrors={getErrors} formOptions={formOptions} />

      <Spacer size="medium" />

      <AvailabilitySection
        onChangeAvailability={onChangeAvailability}
        selectedAvailabilities={formState.values.selectedAvailabilities}
        selectedDuration={allowedDurations.find(
          (duration) => duration.id === formState.values.length,
        )}
        conferenceData={conferenceData}
      />

      <Spacer size="medium" />

      <PublicProfileCard
        me={participantData.me}
        formOptions={formOptions}
        photoRequired={true}
        getParticipantValidationError={(field) =>
          getErrors(
            `validationSpeaker${field[0].toUpperCase()}${field.substring(1)}` as any,
          )
        }
      />

      <Spacer size="medium" />

      {!submission && (
        <>
          <label>
            <HorizontalStack gap="small" alignItems="center">
              <Checkbox
                {...checkbox("acceptedPrivacyPolicy")}
                checked={formState.values.acceptedPrivacyPolicy}
              />
              <Text size={2} weight="strong">
                <FormattedMessage
                  id="global.acceptPrivacyPolicy"
                  values={{
                    link: (
                      <Link
                        className="underline"
                        target="_blank"
                        href={createHref({
                          path: "/privacy-policy",
                          locale: language,
                        })}
                      >
                        Privacy Policy
                      </Link>
                    ),
                  }}
                />
              </Text>
            </HorizontalStack>
          </label>
          <Spacer size="medium" />
        </>
      )}

      <Grid cols={2}>
        <div>
          <Text weight="strong" uppercase color="grey-900" size="label3">
            <FormattedMessage id="cfp.grantsLabel" />
          </Text>
          <Spacer size="thin" />
          <Text color="grey-700" size="label3">
            <FormattedMessage
              id="cfp.grantsCheckbox"
              values={{
                grantsCta: (
                  <Link
                    href={createHref({
                      path: "/grants-info",
                      locale: language,
                    })}
                    target="_blank"
                  >
                    <Text
                      decoration="underline"
                      color="grey-700"
                      hoverColor="green"
                      size="label3"
                    >
                      <FormattedMessage id="cfp.grantsCta" />
                    </Text>
                  </Link>
                ),
              }}
            />
          </Text>
        </div>
        <div className="flex justify-center items-end flex-col">
          {(hasValidationErrors || submissionError?.message) && (
            <Text size="label3" color="red">
              <FormattedMessage id="cfp.validationErrors" />
            </Text>
          )}
          <Spacer size="small" />
          <Button
            fullWidth="mobile"
            variant="secondary"
            disabled={
              submissionLoading ||
              submissionData?.mutationOp?.__typename === "Submission" ||
              !formState.values.acceptedPrivacyPolicy
            }
          >
            {submissionLoading && <FormattedMessage id="cfp.loading" />}
            {!submissionLoading && <FormattedMessage id="cfp.submit" />}
          </Button>
        </div>
      </Grid>
    </form>
  );
};
