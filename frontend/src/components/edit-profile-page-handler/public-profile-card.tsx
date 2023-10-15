import {
  CardPart,
  Text,
  Heading,
  Checkbox,
  MultiplePartsCard,
  Grid,
  HorizontalStack,
  GridColumn,
  InputWrapper,
  Textarea,
  Input,
  Link,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { FormState, Inputs, StateErrors } from "react-use-form-state";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { MyEditProfileQuery } from "~/types";

import { FileInput } from "../file-input";
import { createHref } from "../link";
import { MeUserFields } from "./types";

type Props = {
  formState: FormState<MeUserFields, StateErrors<MeUserFields, string>>;
  formOptions: Inputs<MeUserFields>;
  me: MyEditProfileQuery["me"];
  getParticipantValidationError: (key: string) => string[] | null;
};

export const PublicProfileCard = ({
  me,
  formState,
  formOptions: { checkbox, raw, url, text },
  getParticipantValidationError,
}: Props) => {
  const language = useCurrentLanguage();
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
            <Text size={2}>
              <FormattedMessage
                id="profile.publicProfile.optInDescription"
                values={{
                  viewProfile: (
                    <Link
                      href={createHref({
                        path: `/profile/${me.hashid}`,
                        locale: language,
                      })}
                    >
                      <FormattedMessage id="profile.publicProfile.viewProfile" />
                    </Link>
                  ),
                }}
              />
            </Text>
          </GridColumn>
          <GridColumn colSpan={3}>
            <label>
              <HorizontalStack
                wrap="wrap"
                gap="small"
                justifyContent="spaceBetween"
              >
                <Text size={2} weight="strong">
                  {!formState.values.participantPublicProfile && (
                    <FormattedMessage id="profile.publicProfile.optedOut" />
                  )}
                  {formState.values.participantPublicProfile && (
                    <FormattedMessage id="profile.publicProfile.optedIn" />
                  )}
                </Text>
                <Checkbox
                  {...checkbox("participantPublicProfile")}
                  checked={formState.values.participantPublicProfile}
                />
              </HorizontalStack>
            </label>
          </GridColumn>
          {formState.values.participantPublicProfile && (
            <>
              <GridColumn colSpan={3}>
                <InputWrapper
                  title={
                    <FormattedMessage id="profile.publicProfile.yourPhoto" />
                  }
                  description={
                    <FormattedMessage id="profile.publicProfile.yourPhoto.description" />
                  }
                >
                  <FileInput
                    {...raw("participantPhoto")}
                    errors={getParticipantValidationError("photo")}
                  />
                </InputWrapper>
              </GridColumn>
              <GridColumn colSpan={3}>
                <InputWrapper
                  title={
                    <FormattedMessage id="profile.publicProfile.yourBio" />
                  }
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
            </>
          )}
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
