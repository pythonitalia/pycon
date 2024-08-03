import {
  CardPart,
  Grid,
  GridColumn,
  Heading,
  Input,
  InputWrapper,
  MultiplePartsCard,
  Textarea,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import type { Inputs } from "react-use-form-state";

import { useTranslatedMessage } from "~/helpers/use-translated-message";

import { FileInput } from "../file-input";

export type ParticipantFormFields = {
  participantBio: string;
  participantPhoto: any;
  participantWebsite: string;
  participantTwitterHandle: string;
  participantInstagramHandle: string;
  participantLinkedinUrl: string;
  participantFacebookUrl: string;
  participantMastodonHandle: string;
};

type Props<T extends ParticipantFormFields> = {
  formOptions: Inputs<T>;
  me: {
    participant?: {
      photo?: string;
    };
  };
  getParticipantValidationError: (key: string) => string[] | null;
};

export const PublicProfileCard = <T extends ParticipantFormFields>({
  me,
  formOptions: { raw, url, text },
  getParticipantValidationError,
}: Props<T>) => {
  const inputPlaceholder = useTranslatedMessage("input.placeholder");

  return (
    <MultiplePartsCard>
      <CardPart contentAlign="left">
        <Heading size={3}>
          <FormattedMessage id="profile.publicProfile.heading" />
        </Heading>
      </CardPart>
      <CardPart background="milk" contentAlign="left">
        <Grid cols={3}>
          <GridColumn colSpan={3}>
            <InputWrapper
              title={<FormattedMessage id="profile.publicProfile.yourPhoto" />}
              description={
                <FormattedMessage id="profile.publicProfile.yourPhoto.description" />
              }
            >
              <FileInput
                {...raw("participantPhoto")}
                accept="image/png,image/jpg,image/jpeg,image/webp"
                previewUrl={me.participant.photo}
                errors={getParticipantValidationError("photo")}
                type="participant_avatar"
              />
            </InputWrapper>
          </GridColumn>
          <GridColumn colSpan={3}>
            <InputWrapper
              title={<FormattedMessage id="profile.publicProfile.yourBio" />}
              description={
                <FormattedMessage id="profile.publicProfile.yourBio.description" />
              }
            >
              <Textarea
                {...text("participantBio")}
                maxLength={1000}
                rows={4}
                placeholder={inputPlaceholder}
                errors={getParticipantValidationError("bio")}
              />
            </InputWrapper>
          </GridColumn>
          <GridColumn colSpan={3}>
            <InputWrapper
              title={
                <FormattedMessage id="profile.publicProfile.yourSocials" />
              }
            >
              {null}
            </InputWrapper>
          </GridColumn>
          <InputWrapper title="Website">
            <Input
              {...url("participantWebsite")}
              required={false}
              maxLength={2048}
              placeholder={inputPlaceholder}
              errors={getParticipantValidationError("website")}
            />
          </InputWrapper>
          <InputWrapper title="Twitter">
            <Input
              {...text("participantTwitterHandle")}
              required={false}
              maxLength={15}
              placeholder={inputPlaceholder}
              errors={getParticipantValidationError("twitterHandle")}
            />
          </InputWrapper>
          <InputWrapper title="Mastodon">
            <Input
              {...text("participantMastodonHandle")}
              required={false}
              maxLength={2048}
              placeholder={inputPlaceholder}
              errors={getParticipantValidationError("mastodonHandle")}
            />
          </InputWrapper>
          <InputWrapper title="Instagram">
            <Input
              {...text("participantInstagramHandle")}
              required={false}
              maxLength={30}
              placeholder={inputPlaceholder}
              errors={getParticipantValidationError("instagramHandle")}
            />
          </InputWrapper>
          <InputWrapper title="LinkedIn URL">
            <Input
              {...url("participantLinkedinUrl")}
              required={false}
              maxLength={2048}
              placeholder={inputPlaceholder}
              errors={getParticipantValidationError("linkedinUrl")}
            />
          </InputWrapper>
          <InputWrapper title="Facebook URL">
            <Input
              {...url("participantFacebookUrl")}
              required={false}
              maxLength={2048}
              placeholder={inputPlaceholder}
              errors={getParticipantValidationError("facebookUrl")}
            />
          </InputWrapper>
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
