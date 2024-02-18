import {
  Button,
  Heading,
  HorizontalStack,
  Page,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import * as yup from "yup";

import { MetaTags } from "~/components/meta-tags";
import {
  MyEditProfileQuery,
  useMyEditProfileQuery,
  useUpdateProfileMutation,
} from "~/types";

import { ErrorsList } from "../errors-list";
import { EmailPreferencesCard } from "./email-preferences-card";
import { MainProfileCard } from "./main-profile-card";
import { PublicProfileCard } from "./public-profile-card";
import { MeUserFields } from "./types";

const schema = yup.object().shape({
  name: yup.string().required().ensure(),
  fullName: yup.string().required().ensure(),
  gender: yup.string().required().ensure(),
  dateBirth: yup.date(),
  country: yup.string().required().ensure(),
  openToRecruiting: yup.boolean(),
  openToNewsletter: yup.boolean(),
});

const onMyProfileFetched = (data: MyEditProfileQuery, formState) => {
  const { me } = data;

  formState.setField("name", me.name ? me.name : "");
  formState.setField("fullName", me.fullName ? me.fullName : "");
  formState.setField("gender", me.gender ? me.gender : "");
  formState.setField(
    "dateBirth",
    me.dateBirth ? new Date(me.dateBirth) : new Date(),
  );
  formState.setField("country", me.country ? me.country : "");
  formState.setField(
    "openToRecruiting",
    me.openToRecruiting ? me.openToRecruiting : false,
  );
  formState.setField(
    "openToNewsletter",
    me.openToNewsletter ? me.openToNewsletter : false,
  );

  // Public profile - participant
  formState.setField("participantPublicProfile", me.participant?.publicProfile);
  formState.setField("participantPhoto", me.participant?.photo ?? "");
  formState.setField("participantBio", me.participant?.bio ?? "");
  formState.setField("participantWebsite", me.participant?.website ?? "");
  formState.setField(
    "participantSpeakerLevel",
    me.participant?.speakerLevel ?? "",
  );
  formState.setField(
    "participantPreviousTalkVideo",
    me.participant?.previousTalkVideo ?? "",
  );
  formState.setField(
    "participantTwitterHandle",
    me.participant?.twitterHandle ?? "",
  );
  formState.setField(
    "participantInstagramHandle",
    me.participant?.instagramHandle ?? "",
  );
  formState.setField(
    "participantLinkedinUrl",
    me.participant?.linkedinUrl ?? "",
  );
  formState.setField(
    "participantFacebookUrl",
    me.participant?.facebookUrl ?? "",
  );
  formState.setField(
    "participantMastodonHandle",
    me.participant?.mastodonHandle ?? "",
  );
};

const toTileCase = (word: string) =>
  word.charAt(0).toUpperCase() + word.slice(1);

export const EditProfilePageHandler = () => {
  const [formState, formOptions] = useFormState<MeUserFields>(
    {},
    {
      withIds: true,
    },
  );

  const {
    data: profileData,
    loading,
    error,
  } = useMyEditProfileQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
    onCompleted: (data) => onMyProfileFetched(data, formState),
  });

  if (error) {
    throw new Error(`Unable to fetch profile, ${error}`);
  }

  const getValidationError = (
    key:
      | "name"
      | "fullName"
      | "gender"
      | "dateBirth"
      | "country"
      | "openToRecruiting"
      | "openToNewsletter",
  ) => {
    const validationKey = `validation${toTileCase(key)}`;
    const validationError =
      (updateProfileData &&
        updateProfileData.updateProfile.__typename === "UpdateProfileErrors" &&
        (updateProfileData.updateProfile as any).errors[validationKey]
          .map((e) => e.message)
          .join(", ")) ||
      "";
    return validationError;
  };

  const getParticipantValidationError = (key: string) => {
    const validationError =
      (updateProfileData &&
        updateProfileData.updateParticipant.__typename ===
          "UpdateParticipantErrors" &&
        (updateProfileData.updateParticipant as any).errors[key]) ||
      [];
    return validationError;
  };

  const [
    update,
    {
      loading: updateProfileLoading,
      data: updateProfileData,
      error: updateProfileError,
    },
  ] = useUpdateProfileMutation();

  useEffect(() => {
    if (profileData && !loading) {
      onMyProfileFetched(profileData, formState);
    }
  }, []);

  const onFormSubmit = useCallback(
    async (e) => {
      e.preventDefault();

      try {
        await schema.validate(formState.values, { abortEarly: false });

        formState.errors = {};

        const updateProfileResponse = await update({
          variables: {
            input: {
              name: formState.values.name,
              fullName: formState.values.fullName,
              gender: formState.values.gender,
              dateBirth: formState.values.dateBirth.toISOString().split("T")[0],
              country: formState.values.country,
              openToRecruiting: formState.values.openToRecruiting,
              openToNewsletter: formState.values.openToNewsletter,
            },
            updateParticipantInput: {
              conference: process.env.conferenceCode,
              publicProfile: formState.values.participantPublicProfile,
              photo: formState.values.participantPhoto,
              bio: formState.values.participantBio,
              website: formState.values.participantWebsite,
              speakerLevel: formState.values.participantSpeakerLevel,
              previousTalkVideo: formState.values.participantPreviousTalkVideo,
              twitterHandle: formState.values.participantTwitterHandle,
              instagramHandle: formState.values.participantInstagramHandle,
              linkedinUrl: formState.values.participantLinkedinUrl,
              facebookUrl: formState.values.participantFacebookUrl,
              mastodonHandle: formState.values.participantMastodonHandle,
            },
          },
        });

        const updateParticipantResult =
          updateProfileResponse.data?.updateParticipant;
        if (updateParticipantResult?.__typename === "Participant") {
          formState.setField(
            "participantPhoto",
            updateParticipantResult.photo ?? "",
          );
        }
      } catch (err) {
        err.inner.forEach((item) => {
          formState.setFieldError(item.path, item.message);
        });
      }
    },
    [update, formState],
  );

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="profile.edit.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Section background="blue">
        <Heading size="display2">
          <FormattedMessage id="profile.myProfile" />
        </Heading>
      </Section>

      <Section>
        <form onSubmit={onFormSubmit}>
          <MainProfileCard
            formState={formState}
            formOptions={formOptions}
            getValidationError={getValidationError}
            profileData={profileData}
          />

          <Spacer size="medium" />

          <PublicProfileCard
            me={profileData.me}
            formState={formState}
            formOptions={formOptions}
            getParticipantValidationError={getParticipantValidationError}
          />

          <Spacer size="medium" />

          <EmailPreferencesCard
            formState={formState}
            formOptions={formOptions}
          />
          <Spacer size="large" />

          <HorizontalStack
            wrap="wrap"
            alignItems="center"
            gap="medium"
            justifyContent="spaceBetween"
          >
            <div>
              <ErrorsList errors={[updateProfileError?.message]} />
            </div>
            <HorizontalStack
              wrap="wrap"
              alignItems="center"
              gap="medium"
              justifyContent="spaceBetween"
            >
              {updateProfileData?.updateProfile?.__typename === "User" &&
                updateProfileData?.updateParticipant?.__typename ===
                  "Participant" && (
                  <Text size="label2">
                    <FormattedMessage id="profile.edit.success" />
                  </Text>
                )}
              <Button disabled={updateProfileLoading}>
                <FormattedMessage id="buttons.save" />
              </Button>
            </HorizontalStack>
          </HorizontalStack>
        </form>
      </Section>
    </Page>
  );
};
