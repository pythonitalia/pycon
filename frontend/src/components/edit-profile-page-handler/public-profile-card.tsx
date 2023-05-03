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
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { FormState, Inputs, StateErrors } from "react-use-form-state";

import { Participant } from "~/types";

import { FileInput } from "../file-input";
import { MeUserFields } from "./types";

type Props = {
  formState: FormState<MeUserFields, StateErrors<MeUserFields, string>>;
  formOptions: Inputs<MeUserFields>;
  participant: Participant;
};

export const PublicProfileCard = ({
  formState,
  formOptions: { checkbox, raw, url, text },
  participant,
}: Props) => {
  console.log("participant", participant);

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
              <FormattedMessage id="profile.publicProfile.optInDescription" />
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
                  title="Your photo"
                  description="Your photo will make your personal page look more like yours!"
                >
                  <FileInput {...raw("participantPhoto")} />
                </InputWrapper>
              </GridColumn>
              <GridColumn colSpan={3}>
                <InputWrapper
                  title="Your bio"
                  description="Write a brief description about yourself! Your interests, hobbies, occupation and more!"
                >
                  <Textarea
                    {...text("participantBio")}
                    maxLength={1000}
                    rows={4}
                    placeholder="Type here..."
                  />
                </InputWrapper>
              </GridColumn>
              <GridColumn colSpan={3}>
                <InputWrapper
                  title="Your socials"
                  description="Where can people find you online? Add your socials here!"
                >
                  {null}
                </InputWrapper>
              </GridColumn>
              <InputWrapper title="Your website">
                <Input
                  {...url("participantWebsite")}
                  required={false}
                  maxLength={2048}
                />
              </InputWrapper>
              <InputWrapper title="Twitter handle">
                <Input
                  {...text("participantTwitterHandle")}
                  required={false}
                  maxLength={15}
                />
              </InputWrapper>
              <InputWrapper title="Mastodon handle">
                <Input
                  {...text("participantMastodonHandle")}
                  required={false}
                  maxLength={2048}
                />
              </InputWrapper>
              <InputWrapper title="Instagram handle">
                <Input
                  {...text("participantInstagramHandle")}
                  required={false}
                  maxLength={30}
                />
              </InputWrapper>
              <InputWrapper title="LinkedIn URL">
                <Input
                  {...url("participantLinkedinUrl")}
                  required={false}
                  maxLength={2048}
                />
              </InputWrapper>
              <InputWrapper title="Facebook URL">
                <Input
                  {...url("participantFacebookUrl")}
                  required={false}
                  maxLength={2048}
                />
              </InputWrapper>
            </>
          )}
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
