import {
  CardPart,
  Grid,
  Heading,
  Input,
  InputWrapper,
  MultiplePartsCard,
  Select,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { useTranslatedMessage } from "~/helpers/use-translated-message";

const SPEAKER_LEVEL_OPTIONS = [
  {
    value: "",
    disabled: true,
    messageId: "cfp.selectSpeakerLevel",
  },
  {
    disabled: false,
    value: "new",
    messageId: "cfp.speakerLevel.new",
  },
  {
    disabled: false,
    value: "intermediate",
    messageId: "cfp.speakerLevel.intermediate",
  },
  {
    disabled: false,
    value: "experienced",
    messageId: "cfp.speakerLevel.experienced",
  },
];

export const AboutYouSection = ({ formOptions, getErrors }) => {
  const inputPlaceholder = useTranslatedMessage("input.placeholder");
  const { select, url } = formOptions;

  return (
    <MultiplePartsCard>
      <CardPart contentAlign="left">
        <Heading size={3}>
          <FormattedMessage id="cfp.aboutYou" />
        </Heading>
      </CardPart>
      <CardPart background="milk" contentAlign="left">
        <Grid cols={1} gap="medium">
          <Text size={2}>
            <FormattedMessage id="cfp.aboutYouDescription" />
          </Text>
          <InputWrapper
            required={true}
            title={<FormattedMessage id="cfp.speakerLevel" />}
            description={<FormattedMessage id="cfp.speakerLevelDescription" />}
          >
            <Select
              {...select("speakerLevel")}
              required={true}
              errors={getErrors("validationSpeakerLevel")}
            >
              {SPEAKER_LEVEL_OPTIONS.map(({ value, disabled, messageId }) => (
                <FormattedMessage id={messageId} key={messageId}>
                  {(copy) => (
                    <option disabled={disabled} value={value}>
                      {copy}
                    </option>
                  )}
                </FormattedMessage>
              ))}
            </Select>
          </InputWrapper>

          <InputWrapper
            title={<FormattedMessage id="cfp.previousTalkVideo" />}
            description={
              <FormattedMessage id="cfp.previousTalkVideoDescription" />
            }
          >
            <Input
              {...url("previousTalkVideo")}
              required={false}
              maxLength={2048}
              errors={getErrors("validationPreviousTalkVideo")}
              placeholder={inputPlaceholder}
            />
          </InputWrapper>
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
